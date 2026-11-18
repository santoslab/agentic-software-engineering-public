# Desktop pilot: instructions for the instructor

This pilot establishes, on your own Neo4j Desktop installation, every fact the
Neo4j lecture and homework will state. Nothing in the lecture notes, slides,
setup guide, or homework is written until the pilot has produced a real
observation for it: the exact Desktop steps, the error texts, the tool counts,
the screenshots. Students who installed Neo4j Desktop 2 recently have the same
version and layout you do, so what you see is what they will see.

Allow about 90 minutes. You need Neo4j Desktop open, a terminal at the course
repository root, Claude Code authenticated, and the password of the `neo4j`
user of your instance `book-music-db-exercises`. All commands below are for
zsh on macOS and start from the repository root unless a step says otherwise.
Record what you observe in [`reports/desktop-pilot.md`](reports/desktop-pilot.md);
its headings follow the steps here.

## What the pilot decides

| Question | Why it matters |
|---|---|
| Does the official server (2.1.1) work against the Neo4j version Desktop installs today (2026.10.0 Enterprise)? | The homework setup guide currently pins 5.26 Community from a command-line rehearsal. If 2026.10 works, students use what Desktop gives them and the guide pins nothing. |
| Does installing APOC from Desktop's plugin tab make `apoc.meta.schema` executable, or is a configuration line still needed? | The server's `get-schema` tool runs that procedure. In the earlier rehearsal it was sandboxed and failed with `isError=true`. The setup guide must say exactly what students do. |
| Can one instance hold a separate `music` database beside `chapter01`? | The plan keeps one instance per student with one database per activity. This avoids a second instance, a second APOC install, and port confusion. |
| What does each failure look like in `/mcp`? | The lecture's diagnose-by-layer table may only quote error text that was actually observed. |
| Do the read and write beats of the demo run as scripted, and what are the exact tool names, prompts, and rows? | The demo script and the slides quote them. |

## About the sample data

The sample database is the fictional music fixture already in
`neo4j/02-neo4j-music-mcp/fixture/` (`tracks.csv`, `playlists.csv`): 36 tracks,
8 artists, 6 albums, 8 playlists, 4 users. The loader `database.py load` creates
it in a database you name. It is not the Chapter 1 data, for three reasons: the
distribution terms of the Chapter 1 sample were never established, so we do not
redistribute it; the fixture was built to contain exactly the features the
questions need (collaborations, repeated rows, shared tracks, tied counts, two
playlists with the same name) and comes with a CSV oracle and expected answers;
and your `chapter01` database stays untouched as the artifact of exercise 01.
Desktop's cached statistics show `chapter01` with zero nodes, which does not
affect anything here.

## Part A — database side, in Neo4j Desktop (about 15 minutes)

### A1 Confirm the instance

Open Desktop. The instance card for `book-music-db-exercises` should show it
running on Neo4j 2026.10.0 with the Bolt address `127.0.0.1:7687`. Note the
exact version and edition text Desktop displays and where the Bolt address is
shown on the card.

*Why:* the setup guide will tell students to read the Bolt address and version
from this card rather than assume defaults. The lecture standardizes on the
version Desktop installs today.

Screenshot: `neo4j/resources/desktop-01-instance-card.png`.

### A2 Install APOC on the instance

Open the instance's menu (the three dots on the card) and find the plugins
view. Install **APOC**. Desktop should offer the version matching 2026.10.0;
the jar `apoc-2026.10.0-core.jar` is already in the instance's `labs/` folder,
so no download is expected. Restart the instance when Desktop asks, or restart
it anyway. Do **not** install Graph Data Science, even though it is offered.

*Why:* since version 2.0.0 the official server refuses to initialize when APOC
is absent, and its schema tool calls `apoc.meta.schema`. GDS stays off because
installing it adds a fourth tool, `list-gds-procedures`, which would make your
tool counts differ from students'.

Record: the exact menu labels you clicked, whether a restart was required, the
APOC version shown. Screenshots: `desktop-02-instance-menu.png`,
`desktop-03-plugins-tab.png`, `desktop-04-apoc-installed.png`.

### A3 Verify APOC and resolve sandboxing

Open the Query tool for the instance (database selector set to `neo4j`). Run:

```cypher
SHOW PROCEDURES YIELD name WHERE name STARTS WITH 'apoc.meta.' RETURN name ORDER BY name;
```

Expect a list of names. Then run:

```cypher
CALL apoc.meta.schema() YIELD value RETURN value;
```

On an empty database this returns one row holding an empty map. That is a pass.
A failure mentioning *sandboxed* or *unrestricted* means Desktop did not permit
the procedure. In that case add this line to the instance's settings and restart:

```properties
dbms.security.procedures.unrestricted=apoc.meta.*
```

Look first for a settings or configuration entry in the same instance menu as
the plugins view and record what it is called. If there is none, stop the
instance and edit the file directly:

```text
~/Library/Application Support/neo4j-desktop/Application/Data/dbmss/dbms-28aaa094-b2be-4d57-ad36-2a91bee08950/conf/neo4j.conf
```

Find the commented example line `#dbms.security.procedures.unrestricted=...`
and add the uncommented line beneath it; then start the instance and rerun both
queries.

*Why:* the earlier rehearsal connected and discovered tools successfully but
`get-schema` still failed because this one procedure was sandboxed. Whether
Desktop's installer sets the permission for you is the single most important
unknown for the student setup guide.

Record: pass on first try, or the exact error text and the path you took.

### A4 Create the `music` database

Still in Query (any database selected), run:

```cypher
CREATE DATABASE music IF NOT EXISTS;
SHOW DATABASES YIELD name, currentStatus RETURN name, currentStatus;
```

Expect `music` listed as `online` beside `chapter01`, `neo4j`, and `system`.
Desktop also has a "Create database" button (exercise 01 used it); if you prefer
it, record where it is.

*Why:* this is the multi-database layout the plan adopts. It only works because
Desktop's bundled edition is Enterprise (Developer license); the step confirms
that on a real install. Students will create `music` the same way, and later an
`openflights` database for the follow-on homework.

Screenshot: `desktop-05-show-databases.png`.

## Part B — terminal side, no model involved (about 15 minutes)

### B1 Prepare the locked environment and run the fixture tests

```sh
cd neo4j/02-neo4j-music-mcp
uv sync --locked
uv run --frozen python -m pytest -q
```

Expect the tests to pass; they touch no database. Stay in this directory for
the rest of Part B.

*Why:* the lock file fixes the driver (`neo4j==6.0.3`), the MCP client
(`mcp==2.3.0`), and the server wheel (`neo4j-mcp-server==2.1.1`). The tests
prove the fixture files are intact before anything is loaded.

### B2 Set the connection variables

```sh
export NEO4J_HW_DIR="$PWD"
export NEO4J_DEMO_DIR="$PWD/../../module-software-engineering/demos/lecture-mcp-neo4j"
export NEO4J_MCP_URI='bolt://127.0.0.1:7687'
export NEO4J_MCP_USERNAME='neo4j'
export NEO4J_MCP_DATABASE='music'
read -r -s 'NEO4J_MCP_PASSWORD?Password for neo4j: '
export NEO4J_MCP_PASSWORD
echo
```

The first two lines only remember where the homework package and the demo
folder are, so later steps can refer to them from any directory.

*Why:* these are the names the official server itself reads, so the same
variables serve the loader, the check script, the LLM-free verifier, and the
`.mcp.json` entry that Claude Code expands. The password lives only in this
shell's environment. Every later step that starts Claude Code must start it from
**this** shell, because a child process inherits the environment of the shell
that launches it.

### B3 Run the readiness check

```sh
uv run --frozen python ../../module-software-engineering/demos/lecture-mcp-neo4j/pilot_desktop_check.py
```

It prints one PASS or FAIL line per step and writes a password-free report to
`module-software-engineering/demos/lecture-mcp-neo4j/reports/pilot-report.json`.
Expected: `connect`, `server` (version 2026.10.0, edition enterprise),
`databases`, `apoc.meta procedures present`, `apoc.meta.schema executes`,
`relevant settings`; then for the server launched by `uvx` in read-only mode a
tools list of exactly `get-schema` and `read-cypher`, a successful `get-schema`,
and `read-cypher RETURN 1` returning `[{"ok": 1}]`; then in write mode a tools
list that adds `write-cypher`. The first `uvx` launch downloads the wheel once;
note how long it took.

*Why:* this is the whole chain with no model in it: driver to database, then a
real MCP client to the real server child process. If it passes, every later
failure is in the host or the prompt, not in the database or the server. The
read-only versus write listing is the lecture's "discovery is provider-controlled"
observation, captured as JSON.

If `apoc.meta.schema executes` fails, go back to A3. If the provider session
fails with an APOC message, the server did not see the plugin; confirm the
restart. Record each FAIL verbatim even if you then fix it.

### B4 Load and check the fixture

```sh
uv run --frozen python database.py load
uv run --frozen python database.py check
```

Both print the fixture identity and counts. Expect exactly: Track 36, Artist 8,
Album 6, Playlist 8, User 4, OWNS 8, PLAYLIST_HAS_TRACK 89, ALBUM_HAS_TRACK 36,
ARTIST 48. The loader refuses a nonempty database, so if `music` already has
data you created a different way, recreate it empty rather than guessing.

*Why:* this is the demo database. The `check` command is also the guard the
write demo relies on in Part D: after an agent writes to the database, `check`
reports a mismatch, and after the revert it passes again.

### B5 Capture an LLM-free reference run on this Neo4j version

```sh
uv run --frozen python verify_live.py --output ../../module-software-engineering/demos/lecture-mcp-neo4j/reports/live-desktop.json
```

Expect `Direct reference queries agree with CSV oracle; schema/read MCP calls succeeded.`

*Why:* the instructor key's existing `live.json` was captured on 5.26 Community.
This produces the same evidence for the version students will have: the
reference queries, the schema tool's output, and the two read calls, all checked
against the CSV oracle. The slides quote the JSON from this file.

## Part C — Claude Code rehearsal, read-only (about 20 minutes)

### C1 Scratch repository and connection

From the same shell (the variables must still be set):

```sh
NEO4J_PILOT_DIR="$(mktemp -d)"
cp "$NEO4J_DEMO_DIR/.mcp.json.example" "$NEO4J_PILOT_DIR/.mcp.json"
cd "$NEO4J_PILOT_DIR"
git init
claude
```

Approve the project server when asked. Run `/mcp`, select `neo4j`, and drill
down: server status, the tool list, then `read-cypher` and `get-schema`
individually. Take one screenshot per screen, as the adoption lecture did:
`module-software-engineering/slides/images/mcp-neo4j-01-slash-mcp.png`,
`-02-server-detail.png`, `-03-tool-list.png`, `-04-read-cypher-detail.png`,
`-05-get-schema-detail.png`. Note the model-visible tool names (expected
`mcp__neo4j__get-schema`, `mcp__neo4j__read-cypher`) and the tool count shown
for the server (expected 2).

*Why:* this is the exact sequence students perform at home and the lecture
reproduces on screen. The screenshots replace the live session if the classroom
network or account fails, and the notes' drill-down section is written from
them. `uvx` is resolved through the PATH of the shell that started Claude Code,
which is why the scratch repository is started from this terminal.

### C2 Schema, then a reviewed read

Prompt 1:

> Use the neo4j MCP server to inspect the schema of the music database.
> Summarize the node labels, relationship types, and relationship directions in
> a short table. Do not run any other query yet.

Expect one `get-schema` call and a table consistent with User → OWNS → Playlist
→ HAS_TRACK (with `position`) → Track → ARTIST → Artist, and Album → HAS_TRACK → Track.

Prompt 2:

> Which five artists appear in the greatest number of distinct playlists?
> Credit every artist on a collaboration; count a playlist at most once per
> artist; return artist id, name, and playlist count; order by count
> descending, then artist id ascending. Propose a bounded read-only Cypher
> query and explain how it avoids counting paths instead of playlists. Show
> the query and do not execute it yet.

Read the proposed query against the schema: label and direction of each
pattern element, `count(DISTINCT p)` rather than `count(*)`, the two sort keys,
a `LIMIT`. Record the query exactly as proposed, and whether the host executed
anything despite the instruction.

Prompt 3:

> Run that query with the neo4j read tool and answer from the returned rows.
> State that the result describes the fictional-music-v1 fixture.

Expect one `read-cypher` call whose `query` argument is the reviewed Cypher,
and these rows: A07 Glass Meadow 8, A08 Indigo Current 8, A01 Amber Circuit 5,
A02 Blue Orchard 5, A03 Copper Kite 4. Expand the call in the host and
screenshot the arguments and the result: `mcp-neo4j-06-read-call.png`.

*Why:* the two-prompt pattern (propose, then run) is the homework's central
discipline. The pilot shows whether the current host actually waits, which the
notes must describe truthfully. The expected rows come from the CSV oracle, so
a difference is a finding, not a matter of taste.

### C3 Verify outside the conversation

In Desktop's Query tool, with `music` selected, paste the contents of
`neo4j/02-neo4j-music-mcp/queries/question-a.cypher` and run it. Compare the
five rows with the agent's. Screenshot: `desktop-06-question-a-replay.png`.

*Why:* "verify outside the conversation" is the second non-negotiable of the
homework. The screenshot is what students will be asked to produce.

### C4 Two failures, captured

Exit Claude Code. Failure 1, missing password: open a **new** terminal (so no
variables are set), `cd` to the scratch directory, start `claude`, run `/mcp`,
open the `neo4j` entry, and record the status and the `Issue:` text verbatim.
Also note whether `/mcp` warns about the unexpanded `${NEO4J_MCP_PASSWORD}`.
Screenshot `mcp-neo4j-07-issue-no-password.png`. Exit and close that terminal.

Failure 2, stopped database: back in the original shell, start `claude` in the
scratch directory, confirm `/mcp` shows connected, then stop the instance in
Desktop, run `/mcp`, open `neo4j`, and choose its reconnect action (or run
`/mcp reconnect all`). Record the error text. Screenshot `mcp-neo4j-08-issue-db-stopped.png`.
Start the instance again and reconnect; confirm it recovers.

*Why:* the lecture teaches diagnosis by layer with a table of observation to
layer to next check. The plan forbids inventing error text. These two failures
are the ones students are most likely to produce, and they occur in different
layers (host expansion and authentication versus provider-to-database connection).

## Part D — Claude Code rehearsal, writes (about 20 minutes)

### D1 Switch to the write configuration

Exit Claude Code. In the scratch directory:

```sh
cp "$NEO4J_DEMO_DIR/.mcp.json.write.example" .mcp.json
```

Start `claude` again from the shell with the variables set.
Run `/mcp`; the `neo4j` server should now show 3 tools, including `write-cypher`.
Screenshot `mcp-neo4j-09-three-tools.png`.

*Why:* the only change is `NEO4J_MCP_READ_ONLY` from `true` to `false`. The tool
list changed because the provider's configuration changed, not because anything
in the repository or the prompt did. This is the first of the three write
controls the lecture names.

### D2 A read that the write depends on

> Which tracks do playlists P02 and P03 have in common? Return track id and
> track name, ordered by track id.

Expect T03 Signal 03, T04 Signal 04, T05 Signal 05, T06 Signal 06 (four tracks).
P02 is "Mix 2", owned by U01; P03 is "Evening", owned by U02.

### D3 The write, with the host's permission prompt

> Create a new playlist with id P09 named "Class Demo", owned by user U01,
> containing exactly those four shared tracks at positions 1 to 4 in track id
> order. Use MERGE so that nothing is duplicated. Show me the Cypher and wait
> for my approval before running it.

Review the Cypher, then let it run. Claude Code should ask permission for
`mcp__neo4j__write-cypher`. Choose the one-time allow, not "always allow", so
the prompt remains visible for students. Screenshot the prompt:
`mcp-neo4j-10-write-permission.png`. Record the prompt's exact wording and the
Cypher that ran.

Verify in Desktop's Query tool (database `music`):

```cypher
MATCH (u:User)-[:OWNS]->(p:Playlist {id:'P09'})-[h:HAS_TRACK]->(t:Track)
RETURN u.id AS owner, p.name AS playlist, h.position AS position, t.id AS track, t.name AS title
ORDER BY position;
```

Expect four rows, owner U01, positions 1 to 4, tracks T03 to T06.

Then run the fixture check without leaving the session. Typing a line that
starts with `!` in Claude Code runs it as a shell command in the session's own
shell, which has inherited your variables:

```text
! cd "$NEO4J_HW_DIR" && uv run --frozen python database.py check
```

Expect a **readiness mismatch** naming Playlist 9, OWNS 9, and
PLAYLIST_HAS_TRACK 93 against the expected 8, 8, and 89. Save the output.

*Why:* this is the demo's write beat end to end: provider allows the tool, host
asks the human, database executes, and a check outside the conversation notices
the change. The mismatch is the point; it shows the guard working.

### D4 The revert

> Delete playlist P09 and only its own relationships. Do not touch any other
> node. Show the Cypher first.

Expect `MATCH (p:Playlist {id:'P09'}) DETACH DELETE p` or an equivalent. Approve
once. Rerun the same `!` check line; it should pass with the original counts.

*Why:* the demo must leave the fixture exactly as it was, and students perform
the same create-verify-revert cycle in the homework.

### D5 Optional: a host-level block

If time permits, add to the scratch repository's `.claude/settings.json`:

```json
{ "permissions": { "deny": ["mcp__neo4j__write-cypher"] } }
```

Restart Claude Code and repeat the D3 prompt. Record what the host does.

*Why:* it is the second of the three write controls (provider flag, host rule,
database role), shown as a JSON object like the others in this lecture.

## Part E — record and hand back (about 15 minutes)

Fill in `reports/desktop-pilot.md`. Move or confirm these files:

- `reports/pilot-report.json` (from B3) and `reports/live-desktop.json` (from B5);
- Desktop screenshots in `neo4j/resources/desktop-*.png`;
- Claude Code screenshots in `module-software-engineering/slides/images/mcp-neo4j-*.png`.

Then exit Claude Code and leave the instance running or stop it as you prefer;
the `music` database stays loaded for the next rehearsal.

## If something fails

| Observation | Likely layer | Next check |
|---|---|---|
| Desktop offers no matching APOC | Desktop version | Record the versions offered; if none matches, this becomes the version decision (5.26 LTS) |
| `apoc.meta.schema` sandboxed after the plugin install | Instance configuration | A3 configuration line; record where you set it |
| `CREATE DATABASE` not permitted | Edition | Record the edition text from `CALL dbms.components()`; fall back to a second instance and say so in the report |
| `pilot_desktop_check.py`: `connect` fails | Instance stopped, wrong port, wrong password | Instance card, Bolt address, retype the password in B2 |
| provider session fails with an APOC message | Server did not see the plugin | Restart the instance; rerun A3 queries |
| `/mcp` shows `neo4j` failed right after start | Password variable not set in the launching shell | This is Failure 1 of C4; start from the shell of B2 |
| Server connected but Claude answered without calling a tool | Host selection | Record it; rephrase to name the server explicitly, as the prompts above do |
| Rows right, prose wrong | Model grounding | Record it; this is a teaching example, not a setup failure |
