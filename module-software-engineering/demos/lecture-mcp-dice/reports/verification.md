# Verification report — 2026-11-15

> Authoring record, migrated from the planning repository on 2026-11-17 with links repointed.
> Commands and paths below refer to the planning layout (`mcp-lecture/demos/dice/`); the example
> now lives in `module-software-engineering/demos/lecture-mcp-dice/`, and the module's shared
> `slides/build.sh` renders the deck. The layout-measurement script `check-layout.cjs` named below
> stayed in the planning repository; [`slide-layout.json`](slide-layout.json) is its saved output.

This is the original dice-package verification snapshot. The subsequent
adoption lecture, music homework, and expanded notes are covered by the
[current implementation report](../../lecture-mcp-adoption/reports/adoption-and-music-verification.md).

Implemented the handoff's first draft in `mcp-lecture/`: A–E examples, locked
setup, tests, demonstration script, development prompt, instructor outline,
student notes, 21-slide Marp deck, editable/rendered diagrams, and Neo4j preview.
No frozen course files or public repository files were edited. No commit or
publication was performed. Instructor pacing/content review remains appropriate
for a first draft.

## Environment and pins

| Item | Observed / selected |
|---|---|
| Platform | macOS, arm64 |
| Python | CPython 3.14.7; project requires >=3.12 |
| uv | 0.12.23 |
| MCP SDK | Official `mcp==2.3.0`, `MCPServer` imported from `mcp.server` |
| Protocol types | `mcp-types==2.3.0` via lock |
| Pydantic | 2.14.3 via lock |
| pytest | 9.0.2 |
| Runtime trace revision | 2026-07-28 |
| Node / npm | 23.11.0 / 10.9.2 |
| Inspector | 2.15.0 |
| Mermaid CLI | 12.2.0 |
| Marp CLI | 4.5.1 |
| Claude Code | 2.1.311; `auth status` reported `loggedIn: false` |

`pyproject.toml` pins SDK and test runner; `uv.lock` fixes transitive resolution.
SDK APIs and the tagged/current official documentation were checked against the
installed package. The project does not import the older server implementation
or a standalone third-party adapter library. Python 3.12/3.13 were not separately
tested. Node 23 is outside Inspector 2.15.0's declared engine range
`^22.23.4 || ^24.22.1 || >=26.12.1`: its CLI checks succeeded with a warning, so
use a supported runtime for classroom rehearsal. Do not treat that warning as a
verified support claim.

## Commands and results

Commands below are relative to `demos/dice/` unless stated otherwise.

| Check | Command | Result |
|---|---|---|
| Resolve/install | `uv sync --locked` | Locked environment installed; 33 packages |
| Tests | `.venv/bin/python -m pytest -q` | **34 passed**; [captured output](pytest.txt) |
| Fresh environment | Copy pyproject, lock, code, tests into empty temp dir; `uv sync --locked --project TEMP_DIR`, then its Python `-m pytest -q` | New venv installed from lock; **34 passed** (2.18s), using shared package cache |
| B protocol | `.venv/bin/python protocol_demo.py --stage B --output evidence/protocol-B.json` | One tool, text output and ordinary Error text |
| D protocol | `.venv/bin/python protocol_demo.py --stage D --output evidence/protocol-D.json` | One tool, bounds/output schemas, explicit errors |
| E protocol | `.venv/bin/python protocol_demo.py --stage E --output evidence/protocol-E.json` | Both tools discovered and called through real stdio |
| Independent discovery | `npx -y @modelcontextprotocol/inspector@2.15.0 --cli .venv/bin/python dice_server.py --method tools/list` | Both tools with input/output schemas |
| Independent call | Same Inspector command with `--method tools/call --tool-name roll --tool-arg count=3 --tool-arg sides=6` | Successful structured/text dice result |
| Render diagrams | `npx -y @mermaid-js/mermaid-cli@12.2.0 -i SOURCE.mmd -o TARGET.svg` | Component, full sequence, compact sequence rendered |
| Render deck (repo root) | `npx -y @marp-team/marp-cli@4.5.1 --no-stdin --allow-local-files mcp-lecture/slides/lecture-mcp-dice.md -o mcp-lecture/slides/lecture-mcp-dice.html` (also `.pdf`) | Both previews rendered |

The server prints no diagnostic text to stdout. Its expected SDK validation
warnings appear on stderr. The subprocess checks parse stdout as JSON. Network
and cache access required tool escalation in the authoring sandbox; this is not
a student dependency. Initial rendering uncovered a Mermaid semicolon parsing
issue and sequence slide overflow; both were corrected and rerendered.

## Evidence and interpretation

- [B capture](../evidence/protocol-B.json),
  [D capture](../evidence/protocol-D.json),
  [E capture](../evidence/protocol-E.json).
- [B wire](../evidence/wire-B.jsonl),
  [D wire](../evidence/wire-D.jsonl),
  [E wire](../evidence/wire-E.jsonl): actual newline-delimited JSON-RPC,
  client/server directions, request/response IDs and metadata.
- [Inspector discovery](../evidence/inspector-list.json) and
  [Inspector roll](../evidence/inspector-roll.json).
- [Malformed request](../evidence/protocol-error.json): `tools/call`
  lacks a name but includes the required modern envelope fields. Response is a
  JSON-RPC `error` with code -32602, rather than a tool result.

The SDK client's auto stdio path starts with `server/discover`, receives
`supportedVersions=["2026-07-28"]`, capabilities and instructions, then performs
`tools/list` and `tools/call`. No initialize/initialized exchange occurs in these
captures. Legacy-client compatibility is not separately tested. The diagrams'
model API interactions explain the host loop and are not represented as captured
model traffic.

E's recorded roll is `[2,4,5]`, total 11, sides 6; coins are `HHTHH`, heads 4,
tails 1. Counts, outcomes, sums, and tallies are consistent. The instructor can
compute 11 < 12 as an explicit LLM-free fallback. Inspector's separate roll
is `[4,5,5]`, total 14 (see saved evidence; random outcomes vary). B's invalid
count=0 is successful Error text; D/E invalid count=0 is an SDK validation tool
error, and sides=7 is a domain failure mapped to ToolError. Both D/E failures
use `isError=true`. Structured success content agrees with the JSON text.
Tests additionally cover strict types, every allowed die size, boundaries,
controlled random sequences, coin tallies, and a real stdio launch from a
separate process. They do not establish fairness or cryptographic suitability.

## Presentation and consistency review

[Slide layout measurements](slide-layout.json) record all 21 sections at
1280×720 with no scroll overflow and both embedded SVGs loaded. Headless Chrome
screenshots were reviewed as a contact sheet plus the call diagram at full
size. The full sequence was retained as a separate SVG for zooming/notes, and
a compact sequence is used on slide 7. The component labels and final slide's
link contrast were improved during review. HTML/PDF remain ignored local
previews; SVGs and Mermaid sources are retained.

All 60 local Markdown links and the slide image paths were checked for local
existence, including authoring sources. Direct CLI roll and coin commands also
ran successfully. External links were consulted for primary technical sources;
this is not a crawl of every historical link. The outline's 75-minute schedule,
slide order, notes, commands, stage names, failure distinctions, cost discussion,
and demonstration prompts were reconciled. No inherited calendar/game-project
assignment is presented as a prerequisite. The public transfer map remains in
the workspace README and the authoring source map.

## Remaining rehearsal and review

1. Authenticate Claude Code in the teaching environment, follow the exact
   scratch-session instructions in [DEMO.md](../DEMO.md), capture real
   calls to both tools and final answers, and verify arithmetic/grounding.
   No host registration, model call, or model transcript is claimed here.
2. Run Inspector's web UI on a supported Node version; its browser interaction
   and classroom screenshots remain unverified. CLI discovery/call checks above
   did run. Inspect `/context` in the host rather than assuming loading behavior.
3. Rehearse pacing, projection readability, and opening fallback with the
   instructor. The historical Neo4j preview was not newly run against a database.
4. Select course placement/number and curate licenses/links when public migration
   is requested. No migration is part of this task.
