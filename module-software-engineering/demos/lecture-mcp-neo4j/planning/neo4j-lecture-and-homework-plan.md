# Plan for a Neo4j MCP lecture, in-class demo, and own-graph homework

> Planning record, written 2026-11-18. It proposes a third MCP lecture
> (`lecture-mcp-neo4j`) between the adoption lecture and the dice lecture, an
> in-class demo on the fictional music fixture, and a two-part homework that ends
> with each student connecting Claude Code to a graph database of their own.
> Section 15 records the instructor's decisions of 2026-11-18: all recommended
> defaults were approved except D2/D5, which were replaced. The homework stays on
> the music fixture and gains a general recipe; the OpenFlights mini-project from
> the planning repository becomes the follow-on, unscripted homework. The pilot
> instructions are in [`../PILOT.md`](../PILOT.md).

## 1 Goal and outcome

Students leave the lecture and homework able to

1. create a Neo4j Desktop instance, install APOC on it, and create a database in it;
2. declare the official Neo4j MCP server in a repository's `.mcp.json` so that
   Claude Code launches it as a local stdio process against that database;
3. ask Claude questions that are answered by Cypher the student can read, review
   before execution, and verify directly in Desktop's Query tool;
4. make a controlled update through the server's write tool, verify it, and
   explain the three places that control whether a write can happen (provider
   read-only flag, host permission, database role);
5. state the recipe for doing all of this against a database of their own; the
   follow-on OpenFlights homework is where they first apply it unscripted.

The lecture connects to the adoption lecture by reusing its objects: the
`mcpServers` map in `.mcp.json`, the `tools/list` result with its `inputSchema`,
the `tools/call` request and `content`/`isError` result, the model-visible
`mcp__<server>__<tool>` name, and the "connected is not used; used is not
grounded" evidence discipline. What is new is the transport (`stdio` with
`command`, `args`, `env`), a tool whose argument is a program (Cypher) that the
student must read, and a write.

## 2 What exists today and what becomes of it

| Resource | Where | State | Disposition |
|---|---|---|---|
| Adoption lecture (notes, slides, outline) | `module-software-engineering/{lecture-notes,slides,lectures-instructor-notes}/lecture-mcp-adoption.md` | Taught; notes promise "a subsequent lecture" on Neo4j reads and writes | Keep. Shrink its 8-minute music preview (slides 22–24, notes §12) to a 2–3 minute teaser; it no longer launches the homework. |
| Music preview script | `demos/lecture-mcp-adoption/neo4j-preview.md` | Fallback notes for the preview | Retire; content moves into the new demo's `DEMO.md`. |
| Instructor key | `demos/lecture-mcp-adoption/neo4j-music-instructor-key/` | Expected answers, LLM-free `live.json` | Move to `demos/lecture-mcp-neo4j/instructor-key/` (key sits beside the launching lecture, Lecture 05 precedent). Expected answers for Question A stay valid. |
| Music homework package | `neo4j/02-neo4j-music-mcp/` | Complete, read-only, 2–3 h, 100-point rubric, 10 submission files, custom launcher | Keep the fixture, loader, checks, primer, reference queries, tests. Rewrite `README.md` as the two-part homework. Replace `launch_server.py` with the general `.mcp.json` recipe. Shrink `SETUP.md` to fixture-specific steps and point at the general setup guide. |
| Chapter 1 Cypher exercise | `neo4j/01-intro-to-neo4j-cypher/` | Students install Desktop and work through the book | Keep as the prerequisite that supplies Desktop, an instance, and basic Cypher. |
| Desktop screenshots | public `neo4j/01-.../resources/` (instance, database, import folder, Query view); planning repo `Neo4j/02-connect-claude-to-neo4j/resources/` (three-dots menu, plugin tab, APOC install) | Partial coverage | Reuse; add the missing ones during the pilot (config edit if needed, `/mcp` drill-down for the Neo4j server, permission prompt). |
| Older "Connect Claude to Neo4j" draft | planning repo `Neo4j/02-connect-claude-to-neo4j/ReadMe.md` | Uses the retired Neo4j Labs servers and the Spotify-derived medium data | Mine for shape only: it already had the write tool, the "read the Cypher before you approve" warning, and the three try-it prompts. Do not import package names or data. |
| OpenFlights mini-project and August transcripts | planning repo `Neo4j/03-use-neo4j-on-new-data/` | Design + explore sessions with reads and a write (`travelCost`) | Becomes the follow-on homework: unscripted database design and MCP integration after the music homework. Migrate to `neo4j/03-openflights-mcp/` under its own short plan; the Neo4j lecture previews it. |
| Diagrams | `slides/diagrams/neo4j-processes`, `music-graph`, `adoption-connections` | Rendered | Reuse all three; add two (Section 9). |
| Dice lecture | `lecture-mcp-dice.*` | Has a 3-minute recap of "adoption and music" at 58–61 and a notes section "Connect this provider to the music homework" | Repoint both at the Neo4j lecture; otherwise unchanged. |

## 3 Facts established while planning (2026-11-18)

- **Provider.** `neo4j-mcp-server` 2.1.1 (released 2026-11-10) is the current
  release of the official server. It exposes `get-schema`, `read-cypher`,
  `write-cypher`, and `list-gds-procedures` (the last only when GDS is present).
  `NEO4J_MCP_READ_ONLY=true` removes `write-cypher` from `tools/list` and takes
  precedence over `NEO4J_MCP_TOOLS`. Since 2.0.0 the server fails `initialize`
  with a descriptive error when APOC is missing. Defaults: read-only off,
  telemetry on, schema sample size 100, request timeout 3 min.
- **Tool contracts** (from the instructor key's `live.json`, protocol 2026-07-28):
  `get-schema` takes `{}`; `read-cypher` takes `{"query": string (required),
  "params": object}`. Results are text content blocks whose text is itself JSON:
  the schema is an array of `{key, value:{type, properties, relationships}}`
  entries, and query results are an array of row objects. This "JSON inside the
  JSON envelope" is a teaching point.
- **Pilot results of 2026-11-18 (Parts A and B3).** Desktop 2.3.0 installs
  APOC 2026.10.0-core from the plugin tab in seconds and writes
  `dbms.security.procedures.unrestricted=apoc.*` and `allowlist=apoc.*` into
  the instance configuration itself, so `apoc.meta.schema` runs with no
  manual step. `CREATE DATABASE music` works on the bundled Enterprise
  edition. The server 2.1.1 initialized against Neo4j 2026.10.0 ("initialize
  requirements verified"), listed `get-schema`/`read-cypher` in read-only
  mode and added `write-cypher` with the flag off, and answered `get-schema`
  and `read-cypher`. The instance card shows the address as
  `neo4j://127.0.0.1:7687`; that scheme works end to end, so all examples use
  it. Without GDS the server logs an ERROR line about `gds.version` at every
  `tools/list` and omits `list-gds-procedures`; this is expected noise, to be
  explained in the setup guide. Decision D7 is settled: standardize on
  Desktop's default version. Details in `../reports/desktop-pilot.md`.
- **Pilot results of 2026-11-18 (Parts C, D, D5a, D5b; D6 skipped).** Full
  record in `../reports/desktop-pilot.md`, with a screenshot index. What
  changes the plan:
  - *Permission mode.* The instructor's Claude Code defaults to **auto**
    mode, in which no tool dialog appears and `write-cypher` ran on the word
    "approved" alone (model courtesy, not a host control). The demo and the
    student guide therefore launch `claude --permission-mode manual` (the
    mode line reads `manual mode on`) and ship a project
    `.claude/settings.json` allowing `mcp__neo4j__get-schema` and
    `mcp__neo4j__read-cypher`; without it, manual mode prompts for every
    read as well ("1 of 3" for batches). The write dialog's wording is
    captured (`mcp-neo4j-24-write-permission-prompt.png`): "Tool use / neo4j —
    Write Cypher Tool: (MCP) / query … / About the … / Do you want to proceed?
    1. Yes 2. Yes, and don't ask again for … 3. No". Section 7's 45–60 row,
    Section 8's §6, Section 9's diagrams and Section 11's guide must say so.
  - *Deny rule.* `permissions.deny` withholds the tool from the model's
    catalogue (ToolSearch no longer finds it) while `/mcp` still lists it; no
    refusal text exists. Denied the tool, the model blamed the server
    configuration and then proposed a route other than the MCP tool; the
    instructor declined and the database stayed unchanged. The three-control
    slide must state what each control does not prevent and that the
    database account is the control that holds on every route.
    `neo4j-write-controls.mmd` draws it that way.
  - *Database role.* Not exercised (D6 skipped for time). The notes describe
    the `reader` role as the third control and mark it untested on 2026.10;
    no error text is quoted.
  - *Demo script.* D2 and D3 in one session: with no antecedent the model
    inferred "the four shared tracks" from a popularity query (correctly) and
    recalled a memory file written in an earlier session of the same
    directory. Each rehearsal uses a fresh `mktemp -d` directory. The model
    read `.mcp.json` as an ordinary file in both write sessions; passwords
    stay `${VAR}` references.
  - *Evidence sources.* Claude Code's per-server log
    (`~/Library/Caches/claude-cli-nodejs/<project-slug>/mcp-logs-neo4j/`)
    carries the real cause behind terse `/mcp` failures, and the instance's
    `logs/query.log` (Enterprise default) records every statement with its
    client (`Go Driver/6.4.0`, `MCP4NEO4J/2.1.1`) and an `EXPLAIN` before
    each read. Both go into the notes' diagnosis section.
  - *Timing.* A ≈ 35 min, B ≈ 20, C ≈ 45, D ≈ 31, D5a ≈ 24, D5b ≈ 15 for an
    instructor taking notes and screenshots.
- **General launch form works.** `uvx neo4j-mcp-server@2.1.1 -v` prints
  `neo4j-mcp version: 2.1.1` on this machine in under a second after the first
  download. The wheel wraps a Go binary; students need only `uv`, which they
  have from the Beads exercise.
- **Desktop on the instructor's machine (checked 2026-11-18).** Neo4j Desktop
  2.3.0 with one instance, `book-music-db-exercises`, running **Neo4j 2026.10.0
  Enterprise** (Developer license) on `bolt://127.0.0.1:7687`, with databases
  `chapter01`, `neo4j`, and `system`. No plugin is installed yet, but the
  instance directory bundles `labs/apoc-2026.10.0-core.jar` and
  `products/neo4j-graph-data-science-2026.10.0.jar`, so the plugin tab should
  install the matching APOC without a download. Students who installed Desktop 2
  recently will have the same layout and version. The homework's `SETUP.md` pins
  **5.26.0 Community + APOC 5.26.0** from a command-line rehearsal; the provider
  has not yet been run against 2026.10. `pilot_desktop_check.py` in the demo
  folder runs the remaining checks (Section 13) once APOC is installed.
- **Multi-database is available.** The Desktop edition is Enterprise, so one
  instance can hold several databases (`CREATE DATABASE music`). Students already
  created a database named `chapter01` by button in exercise 01, and the
  instructor's instance has it. This removes the
  need for a second instance, a second APOC install, and Bolt-port confusion.
- **Known failure modes** (from `neo4j/02-neo4j-music-mcp/evidence/failure-cases.json`):
  provider `initialize` rejected when APOC absent; `get-schema` returned
  `isError=true` when `apoc.meta.schema` was sandboxed, fixed by
  `dbms.security.procedures.unrestricted=apoc.meta.*`. Whether Desktop's plugin
  installer sets this automatically is a pilot question.
- **Claude Code.** 2.1.311 here. `.mcp.json` expands `${VAR}` and
  `${VAR:-default}` in `command`, `args`, `env`, `url`, `headers`; an unset
  variable loads as literal text and is flagged in `/mcp`. Project servers need
  one-time approval; `claude mcp reset-project-choices` resets it. The
  model-visible tool name will be `mcp__neo4j__read-cypher` for a server keyed
  `neo4j`. A host-level block is a `permissions.deny` entry for
  `mcp__neo4j__write-cypher` in `.claude/settings.json`.

## 4 Teaching sequence and placement

| Lecture | Role of the student | Core question | Launches |
|---|---|---|---|
| MCP 1 Adoption (exists) | Consumer of a remote server | How do I connect my repository's agent to an existing capability, and how do I know the model used it? | nothing (teaser only) |
| **MCP 2 Neo4j (new)** | Consumer of a local server that fronts a database, reading and writing | How do I put a database behind my agent, and how do I keep the agent's queries and updates honest? | Music homework (fixture + recipe); OpenFlights homework follows it |
| MCP 3 Dice (exists) | Provider | What do the provider and the host each do when a model calls a tool, and how is each layer tested? | — |

Order adoption → Neo4j → dice follows the promise in the adoption notes'
motivation section ("we will see how we can use MCP to connect to Neo4j ...
reads and writes ... then develop our own MCP servers"). The dice lecture's
"no database required" stance is unaffected. The Neo4j lecture is unnumbered
like its siblings: `lecture-mcp-neo4j`.

Prerequisites stated to students: exercise 01 completed (Desktop installed, one
instance, Chapter 1 Cypher) or at least Desktop installed; `uv` and Claude Code
working; the adoption lecture. The Cypher primer covers what the homework needs
for students who skipped the book.

## 5 Student-testable lecture objectives

After the lecture, students can

1. write a stdio server entry in `.mcp.json` and say what each of `type`,
   `command`, `args`, `env`, and `${NEO4J_MCP_PASSWORD}` does, and why the password
   is never in the file;
2. name the three processes involved (host, provider, database) and say which
   one executes the Cypher, which one proposes it, and which one asks permission;
3. read a `tools/list` excerpt for the Neo4j server and explain why
   `write-cypher` is present or absent;
4. given a question in English and a proposed Cypher query, check label and
   direction against `get-schema` output and check whether a count is a path
   count or a distinct count;
5. verify an agent-reported result by running the same query in Desktop's Query
   tool, and verify an update by reading back the changed data;
6. list the three independent controls on writes (provider flag, host
   permission or deny rule, database role) and give the failure each one does
   not prevent.

## 6 The configuration students learn

One general recipe, shown in class and reused in both homework parts and for
any later database:

```json
{
  "mcpServers": {
    "neo4j": {
      "type": "stdio",
      "command": "uvx",
      "args": ["neo4j-mcp-server@2.1.1"],
      "env": {
        "NEO4J_MCP_URI": "${NEO4J_MCP_URI:-neo4j://127.0.0.1:7687}",
        "NEO4J_MCP_USERNAME": "${NEO4J_MCP_USERNAME:-neo4j}",
        "NEO4J_MCP_PASSWORD": "${NEO4J_MCP_PASSWORD}",
        "NEO4J_MCP_DATABASE": "music",
        "NEO4J_MCP_READ_ONLY": "true",
        "NEO4J_MCP_TELEMETRY": "false"
      }
    }
  }
}
```

Teaching moves that tie it to the adoption lecture:

- Put the adoption lecture's `microsoft-learn` entry (`http`, `url`) beside this
  one. Same map, same key-is-our-name point; `url` is replaced by a program to
  start and the environment to start it with.
- `env` values are what the provider process receives; `${...}` is Claude Code
  expanding the host's environment before launch, not shell syntax and not JSON.
- The same file with `NEO4J_MCP_READ_ONLY` set to `false` is the write
  configuration. The difference is visible in `/mcp` as a different tool count,
  which demonstrates that discovery is dynamic and provider-controlled.
- Switching `NEO4J_MCP_DATABASE` to another database (Part 2 of the homework)
  is a one-field change. Two entries (`music`, `pkb`) in the same map show that
  the host can hold several providers at once, as the adoption connections
  diagram already draws.
- Mention `claude mcp add --scope project --transport stdio -e ... neo4j -- uvx
  neo4j-mcp-server@2.1.1` as the command that writes the same file; teach the
  file.

JSON objects to show, all from real captures (Section 12 says which script
produces them): the `tools/list` result in read-only mode (two tools) and write
mode (three), the `inputSchema` of `read-cypher` next to the adoption lecture's
`microsoft_docs_fetch` schema, one `tools/call` for `read-cypher` with its
`arguments.query` and the row array inside `content[0].text`, the `get-schema`
result read against the music-graph diagram, and the `/mcp` drill-down
screenshots for the `neo4j` server (mirroring adoption notes §4.1).

## 7 In-class demo progression

Everything runs against a prepared instance; no installation in class. Scratch
repository holds only `README.md` and `.mcp.json`. Fallback for every live beat
is a labeled capture (screenshots + JSON) produced during the pilot.

| Minutes | Beat | What students see | Fallback or cut |
|---|---|---|---|
| 0–5 | Cold open | In the scratch repo: "Inspect the music database's schema, then tell me which five artists appear in the most distinct playlists." Expand the `get-schema` and `read-cypher` calls, the Cypher argument, the rows, the answer. | Captured session screenshots; LLM-free `live.json`. |
| 5–15 | Same JSON, new transport | Adoption `.mcp.json` beside today's. Three-process diagram. `tools/list` excerpt with `read-cypher` schema beside `microsoft_docs_fetch`. "JSON inside the envelope." | Cut the schema comparison to one sentence. |
| 15–30 | What you will do at home | Desktop: instance card, plugin tab with APOC, `CREATE DATABASE music`, `RETURN 1`, `SHOW PROCEDURES ... apoc.meta`. Terminal: `read -s` password, `uv run python database.py load`/`check`, `claude`, `/mcp`, drill into `neo4j` → tools → `read-cypher`. One deliberate failure: start Claude without the password variable set; read the `/mcp` Issue row; fix. | Screenshot sequence (pilot output). Keep the failure beat even if everything else is screenshots: it is the layer-diagnosis lesson. |
| 30–45 | Reading with review | Two-prompt pattern: propose the Cypher first, review it against the schema (labels, direction, `count(DISTINCT p)`), then run. Paste the same Cypher into Desktop's Query tool; compare rows. Ask "which artist is most popular?" and let the class name two meanings. | If short, drop the Query-tool replay to the notes; keep the review step. |
| 45–60 | Writing with control | Restart with `NEO4J_MCP_READ_ONLY=false`; `/mcp` now shows `write-cypher`. Prompt: "Create playlist P09 'Class Demo' owned by U01 containing the tracks shared by P02 and P03, positions from 1. Show the Cypher first." Approve the host's permission prompt. Verify by reading P09 back in Query. Run `database.py check` → readiness mismatch (the guard noticed). Prompt: "Delete playlist P09 and only its relationships; show the Cypher first." `check` passes. Slide: provider flag / host deny rule / database role, and what each does not prevent. | Captured write session. If behind, show the three-control slide and the before/after `check` output only. |
| 60–70 | The recipe, and what comes next | The recipe slide: instance and database, APOC, password in the environment, the stdio entry, `/mcp`, schema first, propose-review-run, verify in Query, writes behind three controls. Homework slide: reproduce today's demo on the fixture. Preview of the OpenFlights homework: unscripted design and loading of a real dataset with the same server. Optional three minutes: Claude builds a ten-node graph in an empty `demo` database from a description, to show the recipe starting from nothing. | Cut the optional build first; keep the recipe and the OpenFlights preview. |
| 70–75 | Exit and bridge | Exit question: name one field of the stdio entry and one observation that proves a write happened. Next lecture: the provider side with dice. | — |

The write beat is designed so that the fixture is intact afterwards: create,
verify, revert, `check`. The uniqueness constraints already in `load.cypher`
make `MERGE` on `id` safe. Do not run `database.py reset` in class.

## 8 Lecture notes plan (`lecture-notes/lecture-mcp-neo4j.md`)

Full tutorial, student-facing, no length cap, same voice as the adoption notes.
Each setup section has starting directory, prerequisites, exact file contents,
commands, expected observation, and recovery.

| § | Section | Content |
|---|---|---|
| 0 | Where this fits | What the adoption lecture established; what changes when the server fronts a database you own; reads then writes; the dice lecture next. |
| 1 | The three processes | Host/client, provider process, database; who proposes, who routes, who asks permission, who executes. `neo4j-processes` and `adoption-connections` diagrams. Stopping Claude does not stop Desktop. |
| 2 | One instance, several databases | Instance vs database vs Bolt address; APOC as an instance-level plugin; `CREATE DATABASE`; why we keep `chapter01`, `music`, and your own database apart. |
| 3 | The stdio entry, field by field | The Section 6 JSON; adoption entry beside it; `${VAR}` expansion; what the provider receives; `claude mcp add` equivalence; project scope and approval; the `/mcp` drill-down with screenshots. |
| 4 | Discovery you can read | `tools/list` in read-only and write mode; `read-cypher` and `write-cypher` schemas; `get-schema` output annotated against the music-graph diagram; model-visible names. |
| 5 | A read, end to end | Exact prompts; proposed Cypher; the review checklist (labels, directions, distinct vs paths, ties, bounds, no write clauses); the `tools/call` and result JSON; the answer; the Query-tool replay. Reuses the primer's constructed P1/P2/T1/T2 example. |
| 6 | A write, end to end | Why writes need three controls; the write configuration; the permission prompt; create P09; read it back; `check` mismatch as a feature; revert; `check` passes. What a `permissions.deny` rule looks like. Optional: a read-only database user in the Developer edition. |
| 7 | Diagnose by layer | Table from observation to layer to next check: variable unset, instance stopped, wrong database name, APOC missing (provider `initialize` error text), `apoc.meta` sandboxed, server connected but no call made, rows right but prose wrong, write tool absent when expected. |
| 8 | A recipe for a database of your own | The general recipe as a numbered procedure with the reason for each step: a database per activity; APOC once per instance; password in the environment; the stdio entry and the one field that changes; `/mcp` before any prompt; schema before any query; propose-review-run; verify in Query; constraints first and `MERGE` when loading; writes behind three controls; checking counts against the source. A worked miniature (ten-node graph from a description). Pointer to the OpenFlights homework as the first unscripted application, and to the course's Neo4j team project after it. |
| 9 | Recipe and self-checks | The reusable adoption recipe specialized to a database; explained self-checks ("Does a connected server prove the query ran?", "Which control stopped this write?"); vocabulary additions (instance, database, Bolt, APOC, read-only mode, constraint, MERGE). |

## 9 Slides and diagrams (`slides/lecture-mcp-neo4j.md`)

About 22 slides, module style block copied from the adoption deck, speaker notes
as HTML comments with minute ranges matching Section 7. Diagrams:

- reuse `neo4j-processes.svg`, `music-graph.svg`, `adoption-connections.svg`;
- new `neo4j-write-sequence.mmd`: prompt → model proposes `write-cypher` →
  host permission prompt → provider → database → student reads back in Query;
- new `neo4j-write-controls.mmd`: the three controls as gates on that path,
  each labeled with what it does not catch;
- a table slide (not a diagram) for the http-vs-stdio field comparison.

Images: Desktop screenshots and `/mcp` drill-down captures go in
`slides/images/mcp-neo4j-*.png` (the module convention established for the
adoption screenshots).

## 10 Homework (rewrite of `neo4j/02-neo4j-music-mcp/README.md`)

Working title: **Connect Claude Code to Neo4j: the music fixture.** Budget
about one hour after Desktop is installed, setup included. Completion-based,
like the module's other exercises. The two non-negotiables carried over from
the current homework are "review the Cypher before it runs" and "verify outside
the conversation."

**Tasks (reproduce the class demo on the music fixture).**

1. Follow the general setup guide: APOC on your instance, `CREATE DATABASE
   music`, readiness checks.
2. From the homework package: `uv sync --locked`, set the password variable,
   `database.py load`, `database.py check`.
3. In your homework repository: `.mcp.json` from the example (read-only),
   `claude`, `/mcp`; record the tool list.
4. Question A (five artists by distinct playlists) with the two-prompt pattern;
   record proposed Cypher, your review, rows, answer. Paste the Cypher into
   Query and compare.
5. Switch to the write configuration; perform the create-verify-revert cycle
   from class with a playlist of your own naming; record the permission prompt,
   the read-back, the `check` mismatch, and the passing `check` after revert.
6. Reflection, one paragraph: what Claude proposed that you changed or
   rejected, and what you could only know by checking outside the conversation.

**The recipe section.** The README closes with the general recipe from the
lecture notes (Section 8, §8), stated as a checklist the student can apply to
any Neo4j database, and a one-paragraph preview of the OpenFlights homework,
which is where they apply it without a script.

**Submission** (one folder in the student repo):

```text
neo4j-mcp-homework/
  .mcp.json              # sanitized: variables, no password
  evidence.md            # tool list, Question A evidence, write cycle evidence, reflection
```

**Rubric** (completion-based, 15 points): setup evidence 5 (connected server,
tool list, `check` output); read 4 (Cypher, review, rows, Query replay); write
4 (prompt, read-back, mismatch and passing `check`); reflection 2. Keep the
setup checkpoint: submit setup evidence within two days of release so Desktop
and APOC problems surface before the due date. An instructor-supplied
recorded-evidence path remains the accommodation when live access fails,
labeled as such.

**Dropped from the current homework** (recoverable from git history): Question
B, the ambiguity task, the six-file evidence template, the 100-point rubric, the
custom launcher. Question B and the ambiguity question become optional
extensions at the end of the README. `PRIMER.md` stays as the Cypher reference
and gains a short "writing data" section (constraints, `MERGE`, `SET`,
`DETACH DELETE`).

**Follow-on: the OpenFlights homework.** The planning repository's
`Neo4j/03-use-neo4j-on-new-data/` (brief, OpenFlights data under ODbL with its
license file, an example solution, and two August 2026 Claude sessions on design
and exploration) becomes the next homework: students design a graph for the
route data, load it with Claude's help through `write-cypher`, and answer the
travel question, applying the recipe without a script. It needs its own short
plan when the music homework is done: data download instructions, whether to
reintroduce the Neo4j Labs data-modeling server or stay with the official server
alone, size guidance, and a rubric. The Neo4j lecture only previews it.

## 11 General setup guide (`neo4j/neo4j-desktop-mcp-setup.md`)

Student-facing, Desktop-specific, reused by both homework parts and by any later
course use of Neo4j. Screenshots in `neo4j/resources/`.

1. Install Desktop (link to exercise 01) and open your instance; note the Bolt
   address on the instance card; start only the instance you mean to use.
2. Install APOC from the instance's plugin tab (reuse the three planning-repo
   screenshots); restart; `SHOW PROCEDURES YIELD name WHERE name STARTS WITH
   'apoc.meta.'`; `CALL apoc.meta.schema()`; if sandboxed, the one config line
   and where Desktop exposes the config editor (pilot determines).
3. Create a database for the activity (`CREATE DATABASE music` or the Desktop
   button); `RETURN 1`.
4. Set the password variable in your shell (bash, zsh, PowerShell variants)
   without echoing it; start Claude Code from that shell.
5. The `.mcp.json` entry (Section 6), field by field; approve the project
   server; `/mcp`; drill down.
6. Troubleshooting by layer (the Section 8 §7 table, student edition).
7. Stopping: exit Claude; the instance keeps running until you stop it in Desktop.

`neo4j/02-neo4j-music-mcp/SETUP.md` keeps only the fixture-specific steps
(environment sync, load, check, reset) and links to this guide.

## 12 Repository changes

New:

- `module-software-engineering/lectures-instructor-notes/lecture-mcp-neo4j.md`,
  `lecture-notes/lecture-mcp-neo4j.md`, `slides/lecture-mcp-neo4j.md`;
  `slides/diagrams/neo4j-write-sequence.mmd`, `neo4j-write-controls.mmd` and
  their SVGs; `slides/images/mcp-neo4j-*.png`.
- `module-software-engineering/demos/lecture-mcp-neo4j/`: `README.md`,
  `DEMO.md` (exact prompts and commands for Section 7),
  `pilot_desktop_check.py` (already written: direct and provider readiness
  checks against a Desktop instance, password prompted, report password-free),
  `.mcp.json.example`
  (read-only) and `.mcp.json.write.example` (both written), `PILOT.md` (the
  instructor's pilot instructions, written), `capture_demo.py` (LLM-free
  capture of `tools/list` in both modes, a `read-cypher` call, a `write-cypher`
  create and revert, written to `evidence/`), `instructor-key/` (moved),
  `planning/` (this file), `reports/` (pilot report template written; pilot
  and rehearsal records).
- `neo4j/neo4j-desktop-mcp-setup.md` and `neo4j/resources/`.
- Later, under its own plan: `neo4j/03-openflights-mcp/` migrated from the
  planning repository.

Modified:

- `neo4j/02-neo4j-music-mcp/`: `README.md` (Section 10), `SETUP.md` (Section 11),
  `.mcp.json.example` (Section 6 form, database `music`), `PRIMER.md` (writing
  section), `verify_live.py` (launch `uvx neo4j-mcp-server@2.1.1` with
  `NEO4J_MCP_READ_ONLY=true` instead of `launch_server.py`; tolerate
  `list-gds-procedures` if present), `export_students.py` (file list),
  `pyproject.toml` (drop the `neo4j-mcp-server` dependency if the launcher goes;
  keep `mcp` and `neo4j` for the loader and verifier). Remove `launch_server.py`.
- `neo4j/README.md`: table gains the setup guide and describes the two-part
  homework; key location updated.
- Adoption lecture: slides 22–24 and notes §12 become a teaser; outline rows
  62–70 shrink; `demos/lecture-mcp-adoption/neo4j-preview.md` removed and the
  key moved; links in `DEMO.md` and `README.md` updated.
- Dice lecture: recap row and notes section point at the Neo4j lecture.
- `module-software-engineering/README.md`: arc table (MCP 1/2/3), MCP lectures
  table gains a column, exercises table row for the homework (assigned at the
  Neo4j lecture; due date to set), demos list.
- `technical-concepts.md`: entry for "MCP stdio server with environment
  variables" and "Neo4j via MCP" pointing at the new notes.

Licensing: notes, slides, guides, screenshots are CC BY 4.0; `.mcp.json`
examples, `capture_demo.py`, Cypher, and the fixture stay MIT, as the homework
package's two license files already state.

## 13 Pilot checklist and risks

The pilot is the first task; the lecture and homework text depend on its
answers. Run it on the instructor's Desktop 2 install and record it in
`demos/lecture-mcp-neo4j/reports/desktop-pilot.md`.

1. Install APOC on `book-music-db-exercises` from the plugin tab (the matching
   2026.10.0 core jar is already bundled) and restart; run
   `pilot_desktop_check.py`. Decide: standardize on Desktop's default version
   (recommended, lightest for students) or require 5.26 LTS.
2. After installing APOC through Desktop, does `CALL apoc.meta.schema()` run,
   or is the `dbms.security.procedures.unrestricted` line still needed? If
   needed, where is the config editor in Desktop 2 and what is the exact line?
3. `CREATE DATABASE music` in the Developer edition: confirm, and confirm the
   loader targets it with `NEO4J_MCP_DATABASE=music` and refuses a nonempty one.
4. `uvx neo4j-mcp-server@2.1.1` from `.mcp.json`: first-run download time;
   `/mcp` status; tool counts in both modes; the exact `Issue:` text when the
   password variable is unset, when the instance is stopped, and when APOC is
   missing (capture all three).
5. Claude Code session: the Section 7 read and write beats end to end, with
   screenshots of the permission prompt and the `/mcp` drill-down; record host
   version and date. Confirm the model-visible tool names.
6. `database.py check` before and after the P09 write and after the revert.
7. Optional: the ten-node graph build in an empty `demo` database for the
   lecture's optional beat; capture its Cypher and schema.
8. Windows: `uvx` and the PowerShell password variable are unrehearsed; find a
   student volunteer or mark the guide's Windows steps as unverified.

Risks: Desktop UI drift between the pilot and class (keep screenshots dated);
GDS plugin present on some student instances adds `list-gds-procedures` (harmless,
explain it); students with the Chapter 1 instance on 7687 starting a second
instance on another port (the guide says read the card); model variability in
proposed Cypher (the review step is the lesson, not identical output); first
`uvx` download in class on a slow network (pre-warm the cache).

## 14 Implementation order and completion criteria

1. **Pilot** (Section 13). Done when every row of the demo table has a live
   path or a labeled capture and the version decision is recorded.
   **Done 2026-11-18** except the optional database-role step (D6).
2. **Setup guide and homework rewrite** (Sections 10–11), including the
   package changes and the moved key. Done when `export_students.py` produces a
   bundle that a fresh directory can follow without the instructor, and
   `verify_live.py` passes against the piloted database.
3. **Lecture notes** (Section 8), written from the pilot captures. Done when
   each objective in Section 5 has an explanation, a worked example, and a
   self-check.
4. **Outline and slides** (Sections 7 and 9), from the notes. Done when
   `slides/build.sh` renders the deck and diagrams and the timing table sums to
   75 with slack.
5. **Reconciliation** (Section 12 "Modified"): adoption teaser, dice pointers,
   READMEs, concept index. Done when every link resolves and the three
   artifacts of each MCP lecture agree on names, versions, and prompts.
6. **Authenticated rehearsal** by the instructor in a scratch repository; set
   the due date and checkpoint date in the module README.

## 15 Decisions

Taken 2026-11-18: D1, D3, D4, D6, D7, and D8 as recommended. D2 and D5 were
replaced: the homework stays on the music fixture and adds a general recipe;
applying the recipe to a database of the student's own is the OpenFlights
follow-on homework, not part of this one. The table is kept for the record.
Added after the pilot (2026-11-18 evening): D9, D10 and D11 below, from the
Part D findings.

| # | Decision | Recommended default | Alternative |
|---|---|---|---|
| D1 | Lecture order | adoption → Neo4j → dice | adoption → dice → Neo4j (then the dice recap stays as is and the Neo4j lecture closes the MCP block) |
| D2 | Homework shape | ~~One two-part homework~~ **Decided:** one homework on the music fixture plus a recipe section; Question B and ambiguity become optional | Keep the current homework unchanged |
| D3 | Student launch form | `uvx neo4j-mcp-server@2.1.1` in `.mcp.json`, read-only flag in `env` | Keep the `uv run --directory ... launch_server.py` launcher (locks tools down, but is fixture-specific and does not transfer) |
| D4 | Writes | Yes, in class and in both homework parts, with create-verify-revert on the fixture | Reads only; writes shown in class but not assigned |
| D5 | Own-data application | ~~Student's choice within a size cap~~ **Decided:** the OpenFlights mini-project becomes the follow-on homework for unscripted design and integration | Student's choice of data inside this homework |
| D6 | Database layout | One instance, APOC once, one database per activity (`chapter01`, `music`, own) | One instance per activity (current `SETUP.md`) |
| D7 | Neo4j version | Whatever Desktop 2 offers by default, APOC from the plugin tab, confirmed by the pilot | Require 5.26 LTS to match the current pin |
| D8 | Instructor key location | Move beside the Neo4j lecture | Leave in the adoption demo folder and link |
| D9 | Permission mode for demo and homework | `claude --permission-mode manual` plus a project `.claude/settings.json` that allows the two read tools; the write prompts | Auto mode (no dialog; the write gate disappears) |
| D10 | Third control in the lecture | Describe the `reader` database role as the route-independent control, marked untested | Pilot it (D6 in PILOT.md) before the lecture if time appears |
| D11 | Demo session hygiene | One session for the read and the write that depends on it; fresh scratch directory per rehearsal | Reuse a directory (the model recalls earlier memory files) |
