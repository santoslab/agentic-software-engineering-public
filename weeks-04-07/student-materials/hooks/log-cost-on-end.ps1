# SessionEnd hook: append one row per session to Documentation/session-costs.csv.
#
# The SessionEnd hook input (stdin JSON) carries transcript_path/session_id/reason/cwd
# but NO cost, so cost is recomputed from the transcript's per-event token usage using
# the pricing table below. Numbers are API-equivalent estimates (same basis as
# Documentation/AgenticPracticesReview.md), not a subscription bill.
#
# A logging hook must never block session exit: everything is wrapped in try/catch and
# the script always exits 0.

try {
    # --- Pricing per MILLION tokens (USD). Edit here when rates change. -------------
    # Rate types: input, output, cache write (5-min TTL = 1.25x input), cache read (0.1x input).
    $pricing = @{
        'claude-opus-4-8'   = @{ in = 5.0;  out = 25.0; cw = 6.25;  cr = 0.50 }
        'claude-sonnet-4-6' = @{ in = 3.0;  out = 15.0; cw = 3.75;  cr = 0.30 }
        'claude-haiku-4-5'  = @{ in = 1.0;  out = 5.0;  cw = 1.25;  cr = 0.10 }
        'claude-fable-5'    = @{ in = 10.0; out = 50.0; cw = 12.50; cr = 1.00 }
    }
    $fallbackModel = 'claude-opus-4-8'   # unknown model ids priced at Opus rates

    # --- Read hook input ------------------------------------------------------------
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }
    $hook = $raw | ConvertFrom-Json

    $transcript = $hook.transcript_path
    $sessionId  = $hook.session_id
    $reason     = $hook.reason
    if (-not $transcript -or -not (Test-Path $transcript)) { exit 0 }

    $projectDir = $env:CLAUDE_PROJECT_DIR
    if (-not $projectDir) { $projectDir = $hook.cwd }
    if (-not $projectDir) { exit 0 }

    # --- Collect transcript files: main + any subagent transcripts ------------------
    $files = @($transcript)
    $dir   = Split-Path $transcript -Parent
    $base  = [IO.Path]::GetFileNameWithoutExtension($transcript)
    $subDir = Join-Path (Join-Path $dir $base) 'subagents'
    if (Test-Path $subDir) {
        $files += (Get-ChildItem -Path $subDir -Filter *.jsonl -Recurse -ErrorAction SilentlyContinue |
                   Select-Object -ExpandProperty FullName)
    }

    # --- Accumulate token usage, deduped by message.id ------------------------------
    $seen   = [System.Collections.Generic.HashSet[string]]::new()
    $models = @{}   # modelId -> @{ in; out; cw; cr }
    $hadUnknown = $false

    foreach ($file in $files) {
        foreach ($line in [System.IO.File]::ReadLines($file)) {
            if ([string]::IsNullOrWhiteSpace($line)) { continue }
            try { $obj = $line | ConvertFrom-Json } catch { continue }

            $msg = $obj.message
            if (-not $msg -or -not $msg.usage) { continue }
            $id = $msg.id
            if (-not $id) { continue }
            if (-not $seen.Add([string]$id)) { continue }   # already counted

            $model = if ($msg.model) { [string]$msg.model } else { $fallbackModel }
            if (-not $models.ContainsKey($model)) {
                $models[$model] = @{ in = 0L; out = 0L; cw = 0L; cr = 0L }
            }
            $u = $msg.usage
            $models[$model].in  += [int64]($u.input_tokens)
            $models[$model].out += [int64]($u.output_tokens)
            $models[$model].cw  += [int64]($u.cache_creation_input_tokens)
            $models[$model].cr  += [int64]($u.cache_read_input_tokens)
        }
    }

    if ($models.Count -eq 0) { exit 0 }

    # --- Cost + totals --------------------------------------------------------------
    $cost = 0.0
    $tIn = 0L; $tOut = 0L; $tCw = 0L; $tCr = 0L
    $modelNames = @()
    foreach ($model in $models.Keys) {
        $t = $models[$model]
        if ($pricing.ContainsKey($model)) {
            $p = $pricing[$model]
            $modelNames += $model
        } else {
            $p = $pricing[$fallbackModel]
            $modelNames += "$model(unknown-rate)"
            $hadUnknown = $true
        }
        $cost += ($t.in * $p.in + $t.out * $p.out + $t.cw * $p.cw + $t.cr * $p.cr) / 1000000.0
        $tIn += $t.in; $tOut += $t.out; $tCw += $t.cw; $tCr += $t.cr
    }

    # --- Append CSV row -------------------------------------------------------------
    $docDir = Join-Path $projectDir 'Documentation'
    if (-not (Test-Path $docDir)) { New-Item -ItemType Directory -Path $docDir -Force | Out-Null }
    $csv = Join-Path $docDir 'session-costs.csv'

    $row = [PSCustomObject]@{
        Timestamp        = (Get-Date -Format o)
        SessionId        = $sessionId
        Reason           = $reason
        Models           = ($modelNames -join ';')
        InputTokens      = $tIn
        OutputTokens     = $tOut
        CacheWriteTokens = $tCw
        CacheReadTokens  = $tCr
        EstCostUSD       = [math]::Round($cost, 2)
    }

    if (Test-Path $csv) {
        $row | Export-Csv -Path $csv -NoTypeInformation -Append
    } else {
        $row | Export-Csv -Path $csv -NoTypeInformation
    }
} catch {
    # Never block session exit on a logging failure.
}
exit 0
