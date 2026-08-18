# The Cost Hook — Stage C Porting Assignment

`log-cost-on-end.ps1` is the original SessionEnd cost hook from the course's own
experiments. **The .ps1 is your spec** (Lecture 12): port it to cross-platform
Python as `.claude/hooks/log_cost_on_end.py`, behavior-preserving.

## The port contract

1. **Pricing table** — per-million rates for input / output / cache-write /
   cache-read, per model, editable in one place; unknown model ids priced at the
   fallback and *named* in the CSV with an `(unknown-rate)` marker.
2. **Transcript collection** — the session's main transcript plus any subagent
   transcripts in the conventional `<transcript-dir>/<base>/subagents/` tree.
3. **The walk** — JSONL lines; only lines with a `message.usage` block count;
   malformed lines are skipped silently.
4. **Dedupe by message id** — each message id counted exactly once across all
   files. (Test this one first: two files sharing a message, tokens counted
   once.)
5. **Output contract** — append one row to `Documentation/session-costs.csv`,
   same columns, same order: Timestamp, SessionId, Reason, Models, InputTokens,
   OutputTokens, CacheWriteTokens, CacheReadTokens, EstCostUSD (rounded to 2).
   Create directory and header if missing.
6. **The iron rule** — the whole program in one try/except; always exit 0. A
   logging hook never blocks session exit.

## Cross-platform notes

- Paths with `pathlib`, never string concatenation.
- Open the CSV with `newline=""` or Windows double-spaces it.
- Registration (`.claude/settings.json`, SessionEnd) invokes `python3` on
  macOS/Linux and typically `python` on Windows — your README must say so,
  because `settings.json` is committed and your grader's OS is not yours.

## A porting tip that is also a lesson

Trace what the original does with a *dated* model id — say
`claude-haiku-4-5-20251001`, the exact id Exercise 4 had you use — against a
pricing table keyed by short names. Is that behavior you should preserve
faithfully, or a finding for your stage report? Either answer can be right;
silently "fixing" it without a note is the only wrong one. (You met this move in
Stage A: the port is a spec review.)
