# Connect Claude Code to Neo4j: the music fixture

Reproduce the Neo4j lecture's demo on your own machine: put a prepared,
fictional music database behind Claude Code through the official Neo4j MCP
server, ask one question whose answer you can check (by observation
and by running the generated Cypher query yourself via Neo4j Desktop's
interface), make one controlled change and undo it, and write down 
what you observed at each step. You use an existing server (Neo4j's
provided MCP server); you do not implement one, design a database, or 
learn a recommendation algorithm.

Budget about one hour once Neo4j Desktop is installed - example database and
exercise setup included. The homework is completion-based, like the 
module's other exercises. Two rules
run through every task: **review the Cypher before it runs**, and **verify
outside the conversation**.

Submit the setup evidence (Tasks 1 to 3) within two days of release and the
complete work within one week, unless the instructor sets other dates. If
setup takes more than 45 minutes, stop and send the instructor your evidence
so far, including the exact error text, rather than changing unrelated
settings.

## Before you start

You need the Neo4j Desktop instance from exercise 01 (any instance will do),
`uv`, and Claude Code. The previous MCP adoption lecture explains the concepts this
homework uses (`.mcp.json`, `/mcp`, `tools/list`, grounded answers); the
Neo4j lecture shows this exact sequence in class.

Three documents go with this one:

- [`../neo4j-desktop-mcp-setup.md`](../neo4j-desktop-mcp-setup.md), the general
  setup guide: installing the Neo4j APOC plug-in on your instance to
  provide the Neo4j MCP server, introducing a new database for your
  instance to support this specific activities on this homework,
  managing the Neo4j password for the database instance in your shell, 
  the setting up the `.mcp.json` entry, the permission dialog, diagnosis by layer.
  Tasks 1 and 3 follow it.
- [`SETUP.md`](SETUP.md), the fixture-specific steps: the Python environment,
  loading and checking the data. Task 2 follows it.
- [`PRIMER.md`](PRIMER.md), a graph and Cypher primer to give you some
  hints and background for the homework: this provides you with enough
  information to read every Cypher query in this homework, the write included.

The data is `fictional-music-v1` ([manifest](fixture/manifest.json),
[provenance](fixture/PROVENANCE.md)): 36 tracks, 8 artists, 6 albums, 8
playlists, 4 users, all invented. Nothing in it says anything about real
listeners, real popularity, or any streaming catalogue.

"Work in this folder". It is the project directory Claude Code starts in, and it
ships the two configuration files the host reads: `.mcp.json.example` (you
copy it to `.mcp.json` in Task 3) and `.claude/settings.json` (already in
place; it pre-approves the two read tools so that only writes prompt).

## Tasks

### 1 Make the instance ready (setup guide, sections 1 to 3)

As shown in the setup guide, start your instance, 
install APOC from its Plugins tab, and create the
`music` database. Finish with the guide's two checks in Desktop's Query tool:
`SHOW PROCEDURES ... 'apoc.meta.'` lists procedure names, and
`CALL apoc.meta.schema()` returns `{}` on the empty database. Record the
Neo4j version from the instance card and the APOC version from the Plugins
tab.

### 2 Load the fixture (SETUP.md)

Following the steps in `SETUP.md`, in a terminal in your homework
folder: `uv sync --locked`, set the connection variables (the password
is typed, never pasted into a file), then

```sh
uv run --frozen python database.py load
uv run --frozen python database.py check
```

Record the `check` output. It must show `"database": "music"` and exactly
these counts: Track 36, Artist 8, Album 6, Playlist 8, User 4, OWNS 8,
PLAYLIST_HAS_TRACK 89, ALBUM_HAS_TRACK 36, ARTIST 48. The `check` command
is also the guard you will use in Task 5.

### 3 Connect Claude Code and record the tool list (setup guide, sections 4 to 6)

Copy `.mcp.json.example` to `.mcp.json`. Read it once, field by field, with
the guide's table beside it. From the terminal of Task 2 start

```sh
claude --permission-mode manual
```

approve the project server when asked, and confirm that the line under the
input box reads `manual mode on`. Type `/mcp`, select `neo4j`, open its tool
list, then open each tool. Record:

- the server status and the tool count (`2 tools` in this configuration);
- the two tool names as the model sees them, `mcp__neo4j__get-schema` and
  `mcp__neo4j__read-cypher`, and the parameters of `read-cypher`;
- the permission mode line.

Then ask for the schema, and nothing else via the following Claude prompt:

> Use the neo4j MCP server to inspect the schema of the music database.
> Summarize the node labels, relationship types, and relationship directions
> in a short table. Do not run any other query yet.

Compare the table with the diagram in the primer. Expect one `get-schema`
tool call to appear in Claude's activity. 
Note anything the model says that the schema does not support.

**Setup checkpoint.** Tasks 1 to 3 are the checkpoint: send the `check`
output, the tool list, and your `.mcp.json` within two days of release, so
that Desktop or APOC trouble surfaces early. If you are stuck, send what you
have with the exact error text; section 8 of the setup guide names the layer
for each message you are likely to see.

### 4 Question A: propose, review, run, replay

This question walks you through various agent-supported read / queries
of the database.

First, we state a question in natural language, and then we show how
we want you to ask the agent to help you with it.

**Question A.** Which five artists appear in the greatest number of distinct
playlists in this fixture? Credit every artist on a collaboration. Count a
playlist at most once per artist. Return artist ID, name, and playlist
count; order by count descending, then artist ID ascending for ties.

Ask for the query first, without execution:

> Which five artists appear in the greatest number of distinct playlists?
> Credit every artist on a collaboration; count a playlist at most once per
> artist; return artist id, name, and playlist count; order by count
> descending, then artist id ascending. Propose a bounded read-only Cypher
> query and explain how it avoids counting paths instead of playlists. Show
> the query and do not execute it yet.

Review the proposal with the primer's checklist: labels and directions match
the schema; the pattern starts at `Playlist`, not `Album` (both have
`HAS_TRACK`); `count(DISTINCT p)`, not `count(*)`; both sort keys; a
`LIMIT`; no write clause. Write down what you checked and anything you
changed. Then:

> Run that query with the neo4j read tool and answer from the returned rows.
> State that the result describes the fictional-music-v1 fixture.

Expect one `read-cypher` call whose `query` argument is the reviewed Cypher.
Expand the call in Claude Code and record the argument, the returned rows,
and the model's answer. A prompt is not an execution boundary: if the host
ran something before you asked, record that rather than tidying the history.
Keep a mistaken first query and its correction; a clean first attempt is not
what is assessed.

Now verify outside the conversation. In Desktop's Query tool, **set the
Database selector in the header to `music`** (it defaults to `neo4j`, and a
query against the wrong database returns nothing), paste the Cypher the model
ran, and run it. Compare IDs, counts, and order with the agent's rows, and
with [`queries/question-a.cypher`](queries/question-a.cypher) if the two
differ. The reference query is supplied on purpose: the task assesses your
review and comparison, not whether you can hide an answer from an agent.

### 5 One controlled write, verified and reverted

Now we experiment with write functionality.

Exit Claude Code. In `.mcp.json`, change `NEO4J_MCP_READ_ONLY` from
`"true"` to `"false"`; nothing else changes. Start Claude Code again with the
same command, run `/mcp`, and record the tool count: `3 tools` now, with
`write-cypher`. Discovery is dynamic and decided by the server's
configuration, which is the first of the three controls on writes.

Choose a name for a new playlist and three to five track IDs from the fixture
(`T01` to `T36`; `MATCH (t:Track) RETURN t.id, t.name ORDER BY t.id` in
Query lists them). Then:

> Create a new playlist with id P09 named "<your name>", owned by user U01,
> containing exactly the tracks <your track ids> at positions 1 to <N>. Use
> MERGE so that nothing is duplicated. Show me the Cypher and wait for my
> approval before running it.

Review the proposal with the primer's "Writing data" section: `MERGE` on
`id` for the new node, `MATCH` (not `MERGE`) for the user and the tracks
that already exist, a `position` on each `HAS_TRACK`, nothing touched beyond
`P09` and its own relationships. Approve in words. Before the call runs,
Claude Code stops with a dialog headed `Tool use` and `neo4j — Write Cypher
Tool: (MCP)`, showing the full `query` and three options: `1. Yes`,
`2. Yes, and don't ask again for ...`, `3. No`. Record its wording. Choose
**1. Yes**. Never choose option 2 for a write tool: it writes a standing
allow rule into `.claude/settings.local.json`, and later writes run unseen.
The model's request for your approval is a courtesy whose wording varies; the
dialog is the host's control.

A dialog may also appear for a shell command the model wants to run. Read it
like any other; one of its options offers to switch to auto mode. Decline that
offer for this homework: in auto mode the write dialog disappears.

Verify in Query (database `music`):

```cypher
MATCH (u:User)-[:OWNS]->(p:Playlist {id:'P09'})-[h:HAS_TRACK]->(t:Track)
RETURN u.id AS owner, p.name AS playlist, h.position AS position, t.id AS track, t.name AS title
ORDER BY position;
```

Record the rows. Then run the fixture check without leaving the session: a
line that starts with `!` runs in the session's own shell, which inherited
your variables:

```text
! uv run --frozen python database.py check
```

Expect `Readiness mismatch` with Playlist 9, OWNS 9, and PLAYLIST_HAS_TRACK
89 plus the number of tracks you added, every other count unchanged. Record
the output. The mismatch is the point: a check outside the conversation
noticed the change.

The database keeps its own record in a log of every statement it executed. To see what
the server sent on your behalf, including the write, run in a second terminal
in this folder:

```sh
uv run --frozen python query_log.py --last 10
```

The above command runs a utility script (written by Claude).
It reads the instance's `logs/query.log` (found automatically for a single
Desktop instance on macOS; otherwise pass `--log PATH`) and prints each
statement with its time, database, outcome, and transaction. Compare it with
what Claude says it ran; the two should agree.

Revert:

> Delete playlist P09 and only its own relationships. Do not touch any other
> node. Show the Cypher first.

Expect `MATCH (p:Playlist {id:'P09'}) DETACH DELETE p` or an equivalent.
Approve once in the dialog. Rerun the `!` check line; it must pass with the
original counts. Record both. If it does not pass, look at the database in
Query before doing anything else; do not run `database.py reset`.

Finally set `NEO4J_MCP_READ_ONLY` back to `"true"` in `.mcp.json`. That is
the file you submit.

### 6 Reflection

One paragraph: what Claude proposed that you changed or rejected, and what
you could only know by looking outside the conversation (Query, `check`,
`/mcp`, the dialog). Name the step at which each thing became visible.

## The recipe

What you did here works for any Neo4j database. As a checklist:

1. One instance, APOC installed once, one database per activity
   (`CREATE DATABASE <name> IF NOT EXISTS`).
2. The password in the shell's environment; Claude Code started from that
   shell; `.mcp.json` carries `${NEO4J_MCP_PASSWORD}`, never the value.
3. One stdio entry. `NEO4J_MCP_DATABASE` is the field that changes between
   activities, `NEO4J_MCP_READ_ONLY` the field that changes between reading
   and writing.
4. `claude --permission-mode manual`, a `.claude/settings.json` that allows
   the two read tools, and `/mcp` before the first prompt: connected, the
   right tool count, the right names.
5. Schema first, every session.
6. Propose, review, run: labels and directions against the schema, distinct
   counts against path counts, ties, bounds, no write clause in a read.
7. Verify in Query with the right database selected, or with a check that does
   not depend on the model.
8. Loading data: uniqueness constraints first, then `MERGE` on the ids, so
   that a repeated load repeats nothing.
9. Writes behind three controls: the server's read-only flag (does the tool
   exist), the host's dialog or deny rule (may the model call it), the
   database account's privileges (what any client with that password may do;
   the only control that holds on every route).
10. Count what you loaded against the source, and read back what you wrote.

**What comes next.** The follow-on homework applies this recipe without a
script: the OpenFlights airline data (airports, airlines, routes), which you
model as a graph yourself, load through `write-cypher` with Claude's help
behind the same dialog, and query for a travel question. The data is real and
larger than this fixture, there is no loader and no `check`, and the schema
is yours to defend. Its brief will be released separately.

## Submission

One folder in your course repository:

```text
neo4j-music-homework/
  .mcp.json          # as submitted: ${NEO4J_MCP_PASSWORD} reference, READ_ONLY "true"
  evidence.md        # setup, Question A, write cycle, reflection
```

Copy [`EVIDENCE.md`](EVIDENCE.md) to `evidence.md` as the template; its
headings follow the tasks. Paste small result tables and the exact texts
(Cypher, dialog, `check` output); screenshots are welcome beside readable
text, not instead of it. Exclude passwords, account identifiers, and
unrelated conversation. Exact model wording and a prescribed number of tool
calls are not requirements; a record that connects question, Cypher, call,
rows, and answer is.

| Criterion | Points |
|---|---:|
| Setup evidence: connected server, tool list and names, passing `check`, `.mcp.json` with the password referenced | 5 |
| Read: proposed Cypher, your review, call and rows, Query replay and comparison | 4 |
| Write: tool count change, proposal and review, dialog, read-back, `check` mismatch, passing `check` after revert | 4 |
| Reflection | 2 |
| Total | 15 |

If Desktop, APOC, or Claude Code access cannot be made to work, submit the
evidence you have at the checkpoint with the error texts. The instructor can
supply a recorded session (schema, calls, rows, dialog) for a labeled
evidence-analysis path and arrange a later live check. Recorded analysis is
not a live connection; label it as such.

## Optional extensions

- **Question B.** For playlist P01, which other playlists share at least one
  distinct track? Exclude P01; return the top five playlist IDs, names, and
  shared-track counts, ordered by count descending, then ID ascending.
  "Shared" means the same track ID, not a similar title or a common artist.
  Same pattern as Task 4; the reference is
  [`queries/question-b.cypher`](queries/question-b.cypher).
- **Ambiguity.** Give two meanings of "Which artist is most popular?", choose
  the one this fixture supports, restate it precisely, and say what data the
  other would need.
- **Diagnosis.** Pick one failure you met, or one from
  [`evidence/failure-cases.json`](evidence/failure-cases.json): name the
  layer (shell variables, host configuration, credentials, database, instance
  plugin, server configuration, host rule, model) and the next check.

Optional at any point: `query_log.py` lists the statements the database
received from the server, and its lecture notes section explains the record.

Instructional prose follows [CC BY 4.0](LICENSE-CC-BY-4.0); code,
configuration, and the fictional fixture follow [MIT](LICENSE-MIT), as
[fixture/PROVENANCE.md](fixture/PROVENANCE.md) states. `export_students.py`
copies this student package alone into an empty directory.
