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

## Screenshots and paths

You take every screenshot; nothing in this pilot is captured for you. A line
such as *Screenshot: `neo4j/resources/desktop-01-instance-card.png`* means:
take a screenshot of what that step describes and save it under that name.

Paths in this document are relative to the repository root,
`/Users/hatcliff/Dev/git-repos/agentic-software-engineering-public-git`.
`neo4j/` is a top-level folder there, beside `module-software-engineering/`; it
holds the Chapter 1 exercise, the music homework package, and now
`neo4j/resources/` for the Desktop screenshots. There are two destinations:

| Name pattern | Destination | Why there |
|---|---|---|
| `desktop-NN-<slug>.png` | `neo4j/resources/` | The student setup guide that will live in `neo4j/` embeds them |
| `mcp-neo4j-NN-<slug>.png` | `module-software-engineering/slides/images/` | Beside the adoption lecture's `/mcp` screenshots, which the notes and slides embed |

On macOS, Shift-Command-4 (drag a region) or Shift-Command-5 saves a file named
`Screenshot <date> at <time>.png` on your Desktop. Right after taking one, from
the repository root run

```sh
module-software-engineering/demos/lecture-mcp-neo4j/pilot_shot.sh desktop-01-instance-card
```

It moves the newest screenshot on your Desktop to the destination the name
implies, prints the file's time so you can confirm it is the one you just took,
and refuses to overwrite. Add `--dry-run` to see what it would do first. Saving
by hand to the same path is equally fine.

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

Screenshot: `neo4j/resources/desktop-01-instance-card.png` (take it, then run the `pilot_shot.sh` line from the section above).

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
export NEO4J_MCP_URI='neo4j://127.0.0.1:7687'
export NEO4J_MCP_USERNAME='neo4j'
export NEO4J_MCP_DATABASE='music'
read -r -s 'NEO4J_MCP_PASSWORD?Password for neo4j: '
export NEO4J_MCP_PASSWORD
echo
```

The first two lines only remember where the homework package and the demo
folder are, so later steps can refer to them from any directory. The URI uses
the `neo4j://` scheme exactly as the instance card shows it (Part A finding),
so the pilot tests what students will copy; `bolt://` would also work for a
single local instance.

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
`-02-server-list.png`, `-03-server-detail.png`, `-04-tool-list.png`,
`-05-read-cypher-detail.png`, and optionally `-05b-get-schema-detail.png`
(the same five screens as the adoption lecture's `mcp-adoption-0N-*.png`). Note the model-visible tool names (expected
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

## Part D — Claude Code rehearsal, writes (about 30 minutes, plus 15 for D5)

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
`mcp-neo4j-24-write-permission-prompt.png`. Record the prompt's exact wording and the
Cypher that ran.

*Pilot note (2026-11-18): the dialog only appears when the session is in a
prompting permission mode. D3 was run in auto mode, where the host approves
tool calls itself, so no dialog appeared and the Cypher ran as soon as Claude
received the word "approved". The dialog is captured in D5a instead.*

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

### D5 The host's own gate: the permission prompt, then a standing deny rule (about 15 minutes)

**Pilot finding (2026-11-18).** Parts C and D ran in Claude Code's *auto*
permission mode (the session transcript records `"permissionMode":"auto"`), in
which the host approves tool calls itself. That is why D3 showed no "Do you
want to proceed?" dialog and why "one-time allow" never came up: the only gate
was the conversational "approved" that the prompt asked for, which is a
courtesy of the model, not a host control. The demo's "host asks the human"
beat therefore still has to be captured, in the mode students are most likely
to be in. Claude Code 2.1.311 calls the prompting mode `manual`
(`claude --help` lists `acceptEdits`, `auto`, `bypassPermissions`, `manual`,
`dontAsk`, `plan`).

#### D5a Capture the prompt in manual mode

1. Exit Claude Code. From the scratch directory, with the variables still
   set, start it in the prompting mode:

   ```sh
   claude --permission-mode manual
   ```

   Look at the line under the input box. It should read
   `⏸ manual mode on · ? for shortcuts` (observed 2026-11-18 in 2.1.311,
   screenshot `mcp-neo4j-17-manual-mode-line.png`). This version labels the
   prompting mode too, so a labelled line is the confirmation, not a sign
   that the flag was ignored. Shift+Tab cycles modes if the label names a
   different one. When you next start `claude` without the flag, note what
   the line says in your default mode, so the setup guide can quote both.
2. Run `/mcp`. The server should still show 3 tools; nothing in the
   configuration changed.
3. Repeat the D3 prompt word for word and reply `approved` when Claude shows
   the Cypher. Before `write-cypher` executes, the host should now stop with
   a permission dialog for the tool. Screenshot it:
   `mcp-neo4j-24-write-permission-prompt.png`. Copy the dialog's exact wording
   and the exact text of each option into the report. Choose the plain
   one-time "Yes". Do not choose any "don't ask again" option: that would
   write an allow rule into the scratch repository's
   `.claude/settings.local.json` and hide the prompt from later runs.
   Also note whether the read calls Claude makes before the write (schema,
   precondition check) prompted or ran silently.
4. Confirm the write with the `!` check line from D3; the 9 / 9 / 93
   mismatch is enough (the Query read-back is optional this time).
5. Repeat the D4 prompt, reply `approved`, and expect a second dialog for the
   delete. Screenshot `mcp-neo4j-24b-revert-permission-prompt.png` only if it
   differs from the first. Approve once. Rerun the `!` check; it must pass.

*Why:* this is the per-call host control that the lecture's write sequence
diagram draws between the model's request and the server's execution.
Students should see it once with its real wording, and should learn that the
mode line tells them whether it is active at all.

#### D5b Standing host rules: allow the reads, deny the write

D5a showed that manual mode prompts for every call, reads included (seven
database dialogs before the write). The demo cannot spend its minutes on read
dialogs, so the standing rule the lecture teaches has two halves: allow the
two read tools, and leave the write tool to prompt. For this test the write is
denied outright, so that both kinds of rule are observed in one run.

1. Exit Claude Code. In the scratch directory create `.claude/settings.json`,
   a new file beside the existing `settings.local.json`:

   ```sh
   mkdir -p .claude && cat > .claude/settings.json <<'EOF'
   {
     "permissions": {
       "allow": ["mcp__neo4j__get-schema", "mcp__neo4j__read-cypher"],
       "deny": ["mcp__neo4j__write-cypher"]
     }
   }
   EOF
   ```

2. Start `claude --permission-mode manual` again. Run `/mcp` and record
   whether the tool list still shows 3 tools or now 2.
3. Ask the D2 question (tracks shared by P02 and P03). Expect T03–T06 with
   **no dialog** for the schema or read calls; that is the allow rule
   working. Record whether any dialog appeared.
4. Ask the D3 prompt with the ids spelled out, since this is a fresh session:

   > Create a new playlist with id P09 named "Class Demo", owned by user U01,
   > containing exactly the tracks T03, T04, T05 and T06 at positions 1 to 4.
   > Use MERGE so that nothing is duplicated. Show me the Cypher and wait for
   > my approval before running it.

   Reply as Claude asks. Expect the write to be refused by the host rule
   rather than offered in a dialog. Screenshot what you see:
   `mcp-neo4j-25-deny-rule.png`. Copy the exact refusal text (Claude's words
   and any host message) into the report.
5. Rerun the `!` check line; it must still pass, since no write happened.
6. Remove the file so it does not leak into later parts:
   `rm .claude/settings.json`. Leave `settings.local.json` alone; it records
   the project-server approval.
7. Start `claude` once more with no flag, in your usual mode, and write down
   what the line under the input box says. Exit. (The guide will quote both
   this text and `manual mode on`.)

**Pilot finding (2026-11-18).** The allow rules removed every read dialog.
The deny rule removed the write tool from the model's catalogue (ToolSearch no
longer found it) while `/mcp` still listed three tools, so there was no
refusal message, only an absent tool. The model attributed the gap to the
server configuration and, once told "approved", proposed reaching the
database by a route other than the MCP tool; the instructor declined the
shell dialog and the database stayed unchanged. A host rule closes one path.
The control that holds on every path is the database account, which D6 tests.

*Why:* minus its deny line, this file is the demo repository's future
`.claude/settings.json`: reads silent, writes prompting. It is the second of
the three write controls the lecture names (provider flag
`NEO4J_MCP_READ_ONLY`, host rule, database role), and a JSON object like
everything else in this lecture. Whether a deny rule also hides the tool from
`/mcp`, and what the host says when the model asks for a denied tool, are the
two facts the pilot records rather than assumes.

### D7 Optional: a copy and a restore of the `music` database (about 15 minutes)

Added 2026-11-18. The lecture notes' Section 10 describes two routes to a
file copy of a database from the Neo4j documentation and from the help text
of the bundled `neo4j-admin`; neither was exercised. Rehearse one before a
project relies on it, and record what you see.

1. Desktop route. Stop the instance. In the instance card's menu choose the
   export entry (observed label "Export databases"), select `music`, export
   to a folder, and note the file name and the folder Desktop opens. Then
   choose the load entry (observed label "Load database from file") with the
   file renamed to `musiccopy.dump`, and confirm that a database
   `musiccopy` appears in `SHOW DATABASES` with the fixture's counts
   (`NEO4J_MCP_DATABASE=musiccopy uv run --frozen python database.py check`).
   Drop it afterwards with `DROP DATABASE musiccopy` against `system`.
2. Command-line route. With the instance running, in Query against `system`:
   `STOP DATABASE music`. In a terminal, with `JAVA_HOME` set to Desktop's
   runtime (`~/Library/Application Support/neo4j-desktop/Application/Cache/runtime/zulu21.*/Contents/Home`),
   run the instance folder's `bin/neo4j-admin database dump music --to-path=/tmp/neo4j-dumps`,
   then `START DATABASE music`. Record the file produced and any error text.
   Optionally test the restore the same way with `database load music
   --from-path=/tmp/neo4j-dumps --overwrite-destination=true` while the
   database is stopped.

*Why:* the notes say plainly that these routes are documented but untested;
a rehearsal lets them say "observed" and lets students on project databases
rely on the procedure.

### D6 Optional: the database role (about 10 minutes)

Desktop's Enterprise edition has roles, so the third control can be shown
with real error text. Students on Community edition do not have it, and the
notes will say so.

1. In Desktop Query, select database `system` and run:

   ```cypher
   SHOW ROLES;
   CREATE USER mcp_reader SET PASSWORD '<throwaway password>' SET PASSWORD CHANGE NOT REQUIRED;
   GRANT ROLE reader TO mcp_reader;
   ```

   Expect `reader` among the built-in roles. Screenshot the role list:
   `neo4j/resources/desktop-11-show-roles.png`.
2. In the shell of B2, switch the connection to that user:

   ```sh
   export NEO4J_MCP_USERNAME=mcp_reader
   read -r -s 'NEO4J_MCP_PASSWORD?Password for mcp_reader: '; export NEO4J_MCP_PASSWORD; echo
   ```

   Keep the write `.mcp.json`. Create `.claude/settings.json` with only the
   two allow rules (the D5b file without its `deny` line).
3. Start `claude --permission-mode manual`. `/mcp` should show 3 tools: the
   provider allows writes. Ask the D2 question (no dialog, T03–T06). Ask the
   D3 prompt with the ids spelled out, reply as asked, and accept the write
   dialog with the one-time Yes. Expect the tool call to come back with a
   database error naming the user and its roles. Screenshot
   `mcp-neo4j-26-database-role-forbidden.png` and copy the error text into
   the report. Note how Claude explains it.
4. Rerun the `!` check line; it passes.
5. Clean up: `export NEO4J_MCP_USERNAME=neo4j` and re-enter the `neo4j`
   password with the B2 line; remove `.claude/settings.json`; in Query on
   `system`, `DROP USER mcp_reader;` or keep the user and say so in the
   report.

*Why:* this is the one control among the three that does not depend on which
tool the model picks or on the host's mode. The lecture's three-control slide
needs its real failure text beside the other two.

## Part E — record and hand back (about 15 minutes)

Fill in `reports/desktop-pilot.md`. Move or confirm these files:

- `reports/pilot-report.json` (from B3) and `reports/live-desktop.json` (from B5);
- Desktop screenshots in `neo4j/resources/desktop-*.png`;
- Claude Code screenshots in `module-software-engineering/slides/images/mcp-neo4j-*.png`.

Then exit Claude Code and leave the instance running or stop it as you prefer;
the `music` database stays loaded for the next rehearsal.

Also, from the D5 sessions: the scratch repository's `.claude/settings.json`
has been removed; the scratch directory can be deleted
(`rm -rf "$NEO4J_PILOT_DIR"`); and Claude Code keeps a memory folder for that
directory under `~/.claude/projects/`, which the next rehearsal avoids by
using a fresh `mktemp -d` directory. Record the mode line of your default
mode (D5b step 7) if not yet done.

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
| No permission dialog before a write; Claude runs the Cypher as soon as you say "approved" | Host permission mode (auto) | The mode line under the input box; restart with `claude --permission-mode manual` (D5a) |
