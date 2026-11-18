# Adoption lecture and music homework verification

> Authoring record, migrated from the planning repository on 2026-11-17 with links repointed.
> Commands and paths below refer to the planning layout (`demos/adoption/`, `homework/neo4j-music/`,
> `instructor-materials/`); see the [module README](../../../README.md) for the public locations.
> The pinned `mcp-lecture/slides/build.sh` (Mermaid CLI 12.2.0, Marp CLI 4.5.1) and `check-layout.cjs`
> were not migrated; the module's shared `slides/build.sh` renders these decks and diagrams.

Implemented 2026-11-16 in this planning repository. The package now contains the
preceding adoption lecture, fictional music homework, expanded dice tutorial,
coordinated instructor/slides artifacts, diagrams, scripts, tests, export and
actual independent evidence. [Module index](../../../README.md) links the deliverables.
No public migration, commit, global host registration, or frozen snapshot edit
was performed.

## Motivation block added on 2026-11-17, after migration

The adoption deck gained a four-slide motivation block after the cold open:
simplified toy-agent registrations and loop, a per-tool schema beside a
per-server declaration, a new connections diagram without the database
(`adoption-connections-basic`), and the two benefits with caveats. The former
"From wired-in tools" slide became the toy-agent mapping table and the Neo4j
connections slide was dropped, so the deck has 25 slides; it was re-rendered
with the module's shared build. The notes gained Section 1, "Why MCP", merging
the former toy-agent and participants sections, and later sections were
renumbered; the instructor outline's timing moved the student attempt to ten
minutes. The slide-layout measurement below predates this change and was not
re-run.

Later the same day the instructor captured five screenshots of the `/mcp`
drill-down (command palette, server list, server detail, tool list, tool
detail) from a session started in a `mktemp -d` directory. They are tracked as
`../../../slides/images/mcp-adoption-01` through `-05` and explained in the
notes' new Section 4.1; the demo script names them as the fallback when the
live connection fails. The tool annotations and names visible in the
screenshots match the 2026-11-16 SDK capture.

## Instructor session update on 2026-11-17

The instructor subsequently supplied a live documentation session account and
companion tutorial, now in [adoption/claude-session](../claude-session/mcp-microsoft-learn-transcript.md).
Claude generated the account from its context after the run. It documents
reported ToolSearch loading, same-response search/fetch requests, results and
follow-up claim checking; it is not an independent verbatim host/API export.
The original transcript is preserved unchanged. The tutorial, notes, slides,
diagrams and instructor/demo guidance now distinguish that account from the
2026-11-16 independent SDK capture and reconstructed protocol/API examples.
This does not supply a raw Claude negotiation trace, execution timing, exact
context/billing measurements or a music-model rehearsal.

After integrating the session, eight Mermaid/SVG diagrams and both deck previews
were rebuilt. Headless Chrome checked all 43 slides with zero overflow or unloaded
images; slides 8–10 were also visually inspected. Nine strict JSON examples in
the companion walkthrough parsed. The original transcript SHA-256 remains
`dd84e27223bb7af8d6963f6684d4e1ee0f40f93099fa4b2a557887433435ab3f`.
These are documentation/rendering checks; runtime code was not changed.
 The original execution
checks below remain a dated record of what ran during initial implementation.

## Teaching artifacts

- [Adoption notes](../../../lecture-notes/lecture-mcp-adoption.md): approximately 4,200
  words, 15 sections, complete configuration walkthrough, annotated contracts,
  observed calls, failure examples, permissions/costs, glossary and explained checks.
- [Expanded dice notes](../../../lecture-notes/lecture-mcp-dice.md): approximately 4,750
  words, including complete minimal server, schemas/results, validation layers,
  tests, process diagnostics and consumer-to-provider bridge. This more than
  doubles the original approximately 2,070-word draft. No note-length cap was imposed.
- [Adoption outline](../../../lectures-instructor-notes/lecture-mcp-adoption.md), 22-slide
  [deck](../../../slides/lecture-mcp-adoption.md), demo script, configuration example,
  student activity and fallbacks.
- [Dice outline](../../../lectures-instructor-notes/lecture-mcp-dice.md) and 21-slide
  [deck](../../../slides/lecture-mcp-dice.md), revised to spend five minutes recapping
  adoption and give implementation/testing more time.
- [Homework](../../../../neo4j/02-neo4j-music-mcp/README.md), setup, Cypher primer, precise
  questions, evidence template, reference queries and 100-point rubric.
- [Instructor key](../neo4j-music-instructor-key/README.md), separate from
  student export; expected answers, real capture and grading/diagnosis guidance.
- Seven Mermaid/SVG pairs: three existing dice diagrams plus adoption connections,
  adoption call, Neo4j process boundaries and music graph. The homework receives
  a portable copy of the graph SVG during builds.

Notes are intentionally more detailed than slides. The authored main tutorials,
primer and worked examples support students reading independently. Pacing and
student workload estimates still need instructor classroom review.

## Environment and release choices

| Item | Actual version or behavior |
|---|---|
| OS | macOS arm64 |
| Python | 3.14.7; projects require >=3.12 |
| uv | 0.12.23 |
| MCP client / dice server library | Official `mcp==2.3.0` |
| Neo4j driver | 6.0.3 |
| Official Neo4j provider | `neo4j-mcp-server==2.1.1`; installed wheel launches bundled provider executable |
| Database rehearsal | Neo4j Community 5.26.0, isolated temporary instance |
| Java | Existing Java 21 runtime, used to start the isolated instance |
| APOC | 5.26.0 Core; meta procedure execution configured |
| pytest | 9.0.2 |
| Microsoft Learn negotiation | 2025-06-18 |
| Neo4j MCP negotiation | 2026-07-28 |
| Node | 23.11.0 |
| Mermaid / Marp CLI | 12.2.0 / 4.5.1 |
| Layout inspection | Puppeteer Core 24.43.1 with installed headless Chrome |
| Claude Code | 2.1.311; auth status reported loggedIn=false |

Each Python project has a tested pin and `uv.lock`. The remote documentation
provider itself is not pinned; evidence records capture date and discovered
schema. The existing dice MCPServer pin was preserved.

The database tar distribution was downloaded from Neo4j's official distribution
host; matching APOC from the official release. Its files and ports were separate
from the user's Desktop databases. The Desktop installation's Java runtime was
read to launch the disposable Community instance; existing DB data/configuration
was not changed. Classroom Desktop GUI steps describe the same backend needs
but were not executed through the GUI. Additional OS instructions are labeled
unrehearsed.

## Commands and actual results

Commands are relative to the directory named in the first column. External
credentials must be supplied as in SETUP.md; none are bundled.

| Directory | Command/check | Result |
|---|---|---|
| demos/adoption | `uv sync --locked` | Environment installed from lock |
| demos/adoption | `uv run --frozen python check_remote.py` | Real HTTP discovery, search and fetch succeeded |
| demos/adoption | Same client with invalid endpoint path | Failed with nonzero exit; no success report written |
| homework/neo4j-music | `uv sync --locked` | Pinned driver/provider/client environment installed |
| homework/neo4j-music | `python fixture/build_fixture.py` | Deterministic original fixture and manifest generated |
| homework/neo4j-music | `python database.py load` and `check` | Clean disposable database loaded with expected counts |
| homework/neo4j-music | `python verify_live.py --output ../../instructor-materials/neo4j-music/live.json` | Exact graph identity, direct reference queries and both MCP result tables agree with CSV oracle; schema succeeds |
| homework/neo4j-music | `python -m pytest -q` | **10 passed**; [output](music-tests.txt) |
| demos/dice | `python -m pytest -q` | **34 passed**; [output](../../lecture-mcp-dice/reports/dice-tests.txt) |
| Student tutorial | Extract complete minimal-server block; start with pinned interpreter and official stdio client | Discovery and roll succeeded |
| Repo root | `mcp-lecture/slides/build.sh` | Seven SVGs and both HTML/PDF decks rendered |
| Repo root | `node mcp-lecture/slides/check-layout.cjs PUPPETEER_MODULE CHROME_EXECUTABLE` | **43 slides**, zero scroll overflow, all embedded SVGs loaded |

The Neo4j driver emits Python deprecation warnings about `asyncio.iscoroutinefunction`
on Python 3.14. They are retained in test output; they did not cause failures.
No statistical fairness claim is made by the dice tests. No model price/token
measurement is claimed.

## Evidence and interpretation

[Remote capture](../evidence/remote.json) contains real discovered
tool definitions, exact search/fetch arguments, response types, lengths and
hashes, plus a short source excerpt. The full third-party article is not bundled.
Its source is the Get-ChildItem reference linked in the notes. The response
summaries are labeled summaries, not fabricated complete protocol responses.
[Invalid endpoint observation](../evidence/invalid-endpoint.json)
records the actual failed independent check. The independent client requested
search and fetch deliberately; neither operation was selected by a model.

[Music capture](../neo4j-music-instructor-key/live.json) includes actual
schema, tool listing, query arguments, returned rows and direct results. The
launcher forces read-only mode and filters discovery to `get-schema` and
`read-cypher`; no write tool appears. Benign reads succeeded. No write operation
was executed. This demonstrates the tested provider exposure/settings, not a
proof that Community administrator credentials enforce an independent database
read role or that every possible procedure is harmless.

The provider's live requirement check initially failed because APOC meta was
absent. After plugin installation, discovery succeeded but schema execution
returned a sandboxing error for `apoc.meta.schema`. Configuring the trusted meta
procedure family and restarting resolved it. These real observations are saved
in [failure cases](../../../../neo4j/02-neo4j-music-mcp/evidence/failure-cases.json) and explained
in setup/notes. Their distinction is pedagogically useful: direct database reads,
provider initialization, discovery and schema execution are separate checks.

## Fixture, oracle and export

The plan's explicitly permitted original-fictional-data alternative was selected.
No records from the older music CSVs or airline dataset are redistributed in
this fixture. [Provenance](../../../../neo4j/02-neo4j-music-mcp/fixture/PROVENANCE.md) and the
[manifest](../../../../neo4j/02-neo4j-music-mcp/fixture/manifest.json) accompany the generator/data.

There are 48 metadata rows, 92 playlist rows, 36 distinct tracks, 8 artists,
6 albums, 8 playlists and 4 users. Three exact input duplicates collapse into
89 playlist occurrence edges; a repeated T01 occurrence at another P01 position
remains. Twelve tracks have collaboration credits. Duplicate display names,
shared tracks and tied rankings are deliberate. Expected graph identity includes
properties and edge endpoints, not just counts.

The CSV oracle uses sets of track credits and playlist track membership rather
than Cypher. Hand-computed tiny cases test distinct counts, collaboration,
duplicate invariance, tie ordering and empty overlap. Fixture tests also check
hash corruption, regeneration, credential diagnostics and student export.
Direct Cypher answers and actual MCP-returned JSON tables match the oracle exactly.

The student exporter was run into an empty temporary directory. A new virtual
environment installed with `uv sync --locked` there; its **10 tests passed**.
The exported environment also launched the official provider against the rehearsal
instance and reproduced the schema and query comparisons. This verifies portable
code/asset packaging, not a new Desktop GUI installation. The first load was into
an empty temporary database; later export checks used that same recognized fixture.

The exporter excludes instructor answers/live capture, local environment,
credentials and caches. It includes the open oracle/verification source and
reference queries intentionally: assessment requires explanation and actual
evidence rather than hiding computable results. Local Markdown/image links in
both the source package and export were checked for existence. The student SVG
copy is byte-identical to its rendered source artifact.

## Presentation and remaining rehearsal

[Layout measurements](../../lecture-mcp-dice/reports/slide-layout.json) cover 22 adoption and 21 dice slides at
1280×720. Contact sheets and full-size architecture, sequence and music diagrams
were visually inspected. Both decks have speaker notes and use the public course's
purple style. HTML/PDF/screenshots are ignored previews; SVG and Mermaid sources
remain editable artifacts. Markdown links, script syntax, tutorial Python blocks,
relative assets, timing totals and rubric total were checked. All 138 local
source Markdown links and the exported package links resolved. A targeted scan
found no rehearsal credential or author workspace path in the new example,
homework, or instructor package sources.

Remaining work is specific:

1. Use the supplied documentation session as a model-generated record of the
   instructor run; capture a raw host export if exact API/transport claims are
   needed. Rehearse the music prompts separately. Initial authoring checks did
   not run an authenticated host, and the later account does not change that history.
2. Rehearse Desktop's GUI, plugin/settings screens and the selected version pair
   on teaching machines. Verify additional OS/shell instructions before treating
   them as platform-tested. The backend/protocol checks above did execute.
3. Review pacing, projection readability, homework setup burden and workload with
   students or an instructor. Set calendar dates and course-level grading weight.
4. Choose public placement/number and curate exports/licensing when requested.
   The planning repository remains the working destination.
