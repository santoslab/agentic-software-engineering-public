# Desktop pilot report

Date: 2026-__-__ · Recorded by: instructor · Follows [PILOT.md](../PILOT.md)

## Environment

- Neo4j Desktop version:
- Instance name, Neo4j version, edition (from `CALL dbms.components()`):
- APOC version installed:
- Server: neo4j-mcp-server 2.1.1 via `uvx` · first-download time:
- Claude Code version (`claude --version`):
- uv version:

## Decisions this pilot settles

- **Neo4j version to standardize on** (Desktop default vs 5.26 LTS) and why:
- **APOC sandboxing**: did `CALL apoc.meta.schema()` run right after the plugin install? If not, the exact error and the exact place you set `dbms.security.procedures.unrestricted=apoc.meta.*`:
- **Multi-database**: did `CREATE DATABASE music` succeed on this edition?

## Part A (Desktop)

- A1 instance card: version/edition text and where the Bolt address appears:
- A2 exact menu labels for plugins; restart required?; APOC version shown:
- A3 result of both queries (pass first try / error text / fix path):
- A4 `SHOW DATABASES` result:
- Screenshots taken (list file names):

## Part B (terminal, no model)

- B1 `pytest -q` result:
- B3 `pilot_desktop_check.py`: PASS/FAIL per step (paste the lines); any FAIL text verbatim:
- B4 `check` counts (paste JSON):
- B5 `verify_live.py` final line and output path:

## Part C (Claude Code, read-only)

- C1 `/mcp` tool count; model-visible tool names; screenshots taken:
- C2 Prompt 1: number of calls; schema table matched the diagram?
- C2 Prompt 2: proposed Cypher (verbatim); did the host wait before executing?
- C2 Prompt 3: `read-cypher` arguments; rows matched the key (A07 8, A08 8, A01 5, A02 5, A03 4)?
- C3 Query-tool replay matched?
- C4 Failure 1 (no password): status and `Issue:` text verbatim; `${...}` warning shown?
- C4 Failure 2 (instance stopped): error text verbatim; recovery after restart?

## Part D (Claude Code, writes)

- D1 tool count with read-only off; screenshot:
- D2 shared tracks returned (expect T03–T06):
- D3 permission prompt wording verbatim; Cypher that ran; Query-tool read-back rows; `check` mismatch output (paste):
- D4 revert Cypher; `check` passed?
- D5 (optional) effect of the deny rule:

## Timing

| Part | Minutes |
|---|---|
| A | |
| B | |
| C | |
| D | |
| E | |

## Surprises, UI drift, and anything the setup guide must say differently

-

## Open items for the next session

-
