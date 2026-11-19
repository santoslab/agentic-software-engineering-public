# Neo4j lecture demonstration

Exact commands, prompts, and fallbacks for the in-class demonstration, in the
order of the [outline](../../lectures-instructor-notes/lecture-mcp-neo4j.md)'s
timed sequence. Every prompt below was run in the 2026-11-18 pilot
([report](reports/desktop-pilot.md)); the expected observations are what that
pilot produced. Model output varies between sessions; the beats are designed
so that variation is part of the lesson, not a failure of the demo.

## Before class

In the homework package, with the instance running, APOC installed, and
`music` created:

```sh
cd neo4j/02-neo4j-music-mcp
export NEO4J_HW_DIR="$PWD"
export NEO4J_DEMO_DIR="$PWD/../../module-software-engineering/demos/lecture-mcp-neo4j"
export NEO4J_MCP_URI='neo4j://127.0.0.1:7687'
export NEO4J_MCP_USERNAME='neo4j'
export NEO4J_MCP_DATABASE='music'
read -r -s 'NEO4J_MCP_PASSWORD?Password for neo4j: '; export NEO4J_MCP_PASSWORD; echo
uv run --frozen python database.py check    
uvx neo4j-mcp-server@2.1.1 -v               
```

Then the scratch repository, fresh for every rehearsal and for class (the
model recalls memory files from earlier sessions in the same directory):

```sh
NEO4J_DEMO_REPO="$(mktemp -d)"
cp "$NEO4J_DEMO_DIR/.mcp.json.example" "$NEO4J_DEMO_REPO/.mcp.json"
mkdir -p "$NEO4J_DEMO_REPO/.claude" && cp "$NEO4J_HW_DIR/.claude/settings.json" "$NEO4J_DEMO_REPO/.claude/"
printf '# Neo4j MCP demo\n' > "$NEO4J_DEMO_REPO/README.md"
cd "$NEO4J_DEMO_REPO" && git init -q
```

Have open: this terminal; a second terminal in `$NEO4J_HW_DIR` with the same
variables for `query_log.py`; Desktop's Query tool with the Database selector
on `music`; the slides. Start every session with

```sh
claude --permission-mode manual
```

and read the line under the input box: `manual mode on`. In auto mode the
write dialog never appears. Approve the project server when asked (once per
scratch directory).

## 0–5 Cold open

> Inspect the music database's schema, then tell me which five artists appear
> in the most distinct playlists.

Expect one `get-schema` call, one `read-cypher` call, five rows (A07 Glass
Meadow 8, A08 Indigo Current 8, A01 Amber Circuit 5, A02 Blue Orchard 5, A03
Copper Kite 4), and an answer. Expand the calls so the Cypher argument and the
rows are on screen. Fallback: `../../slides/images/mcp-neo4j-06-read-call.png`
and the rows in `reports/live-desktop.json`.

## 15–27 Activation and one failure

In the session: `/mcp`, select `neo4j`, view tools, select Read Cypher. Expect
2 tools, `Command: uvx neo4j-mcp-server@2.1.1`, `Protocol: 2026-07-28`, the
tags `read-only · open-world`, and `Full name: mcp__neo4j__read-cypher`.
Fallback: images `mcp-neo4j-01` to `05`.

The failure beat. Open a **new** terminal (no variables), `cd` to the scratch
directory, `claude --permission-mode manual`, `/mcp`. Expect:

```text
MCP config diagnostics ⚠
[Warning] [neo4j] mcpServers.neo4j: Missing environment variables: NEO4J_MCP_PASSWORD
```

and `✘ neo4j`. Name the layer: host configuration, before any process starts.
Exit and close that terminal. The server's own words are in
`~/Library/Caches/claude-cli-nodejs/<project-slug>/mcp-logs-neo4j/`: the
literal `${NEO4J_MCP_PASSWORD}` was sent as the password and the database
answered `Neo.ClientError.Security.Unauthorized`. Fallback: images
`mcp-neo4j-07-issue-no-password-a/b`. The stopped-instance failure
(`Failed to reconnect to neo4j: 0`) is shown from images `08-a/b/c`; do not
stop the instance in class.

## 27–40 Reading with review

Back in the prepared terminal's session, three prompts:

> Use the neo4j MCP server to inspect the schema of the music database.
> Summarize the node labels, relationship types, and relationship directions
> in a short table. Do not run any other query yet.

Expect one `get-schema` call and a table matching the music-graph diagram;
in the pilot the model noted unprompted that `HAS_TRACK` comes from both
Playlist and Album.

> Which five artists appear in the greatest number of distinct playlists?
> Credit every artist on a collaboration; count a playlist at most once per
> artist; return artist id, name, and playlist count; order by count
> descending, then artist id ascending. Propose a bounded read-only Cypher
> query and explain how it avoids counting paths instead of playlists. Show
> the query and do not execute it yet.

Expect no execution and a statement to review on screen: anchored on
`Playlist`, `count(DISTINCT p)`, both sort keys, `LIMIT 5`, no write clause.
The pilot's proposal used a `WITH` stage and camelCase aliases; say that the
text varies and the review is the lesson.

> Run that query with the neo4j read tool and answer from the returned rows.
> State that the result describes the fictional-music-v1 fixture.

Expect one `read-cypher` call with the reviewed statement as `query` and the
five rows. Then in Desktop's Query tool, Database selector on `music`, paste
the statement the model ran and run it: same rows. Fallback:
`neo4j/resources/desktop-09-question-a-replay.png`. Ask the class for two
meanings of "which artist is most popular?" before moving on.

## 40–56 Writing with control

Exit the session. Switch the configuration and restart:

```sh
cp "$NEO4J_DEMO_DIR/.mcp.json.write.example" .mcp.json
claude --permission-mode manual
```

`/mcp`: 3 tools. Fallback: image `09`. Then, in this one session, the
dependent read and the write:

> Which tracks do playlists P02 and P03 have in common? Return track id and
> track name, ordered by track id.

Expect T03 to T06. Fallback: image `10`.

> Create a new playlist with id P09 named "Class Demo", owned by user U01,
> containing exactly the tracks T03, T04, T05 and T06 at positions 1 to 4.
> Use MERGE so that nothing is duplicated. Show me the Cypher and wait for
> my approval before running it.

Expect a precondition read (user, tracks, no P09) and a proposed MERGE
statement; read it clause by clause (matched user and tracks, merged
playlist and relationships, a position on each, a `RETURN`). Reply
`approved`. Expect the host dialog:

```text
Tool use
neo4j — Write Cypher Tool: (MCP)
query: ...
Do you want to proceed?
❯ 1. Yes
  2. Yes, and don't ask again for neo4j — Write Cypher commands in ...
  3. No
```

Read it aloud. Choose **1**. Never choose 2 in a demo or a rehearsal: it
writes a standing allow rule into the scratch repository's
`.claude/settings.local.json` and hides the dialog from every later run.
Fallback: images `11`, `24`, `12` (the auto-mode session, for contrast).

Verify in Query (`music`):

```cypher
MATCH (u:User)-[:OWNS]->(p:Playlist {id:'P09'})-[h:HAS_TRACK]->(t:Track)
RETURN u.id AS owner, p.name AS playlist, h.position AS position, t.id AS track, t.name AS title
ORDER BY position;
```

Four rows. Fallback: `neo4j/resources/desktop-10-p09-readback-query.png`.
Then, in the session, the check (a line starting with `!` runs in the
session's shell, which inherited the variables):

```text
! cd "$NEO4J_HW_DIR" && uv run --frozen python database.py check
```

Expect `Readiness mismatch` with Playlist 9, OWNS 9, PLAYLIST_HAS_TRACK 93.
Fallback: image `13`. Revert:

> Delete playlist P09 and only its own relationships. Do not touch any other
> node. Show the Cypher first.

Expect `MATCH (p:Playlist {id: 'P09'}) DETACH DELETE p` or an equivalent, a
second dialog, option 1, and a passing check from the same `!` line.
Fallback: images `14`, `15`, `16`.

The three controls are a slide. The deny-rule finding is told from the pilot
(images `25-a/b`): with `"deny": ["mcp__neo4j__write-cypher"]` in
`.claude/settings.json`, `/mcp` still listed three tools, the model's
catalogue had two, the model attributed the gap to the server and proposed a
direct connection, and the instructor declined the shell dialog. To show it
live, add the deny line to the scratch repository's settings file, restart,
and repeat the write prompt; remove the line afterwards.

## 56–64 Records and recovery

In the second terminal:

```sh
uv run --frozen python query_log.py --last 12
uv run --frozen python query_log.py --last 6 --explain
```

Expect the session's statements in order with local times, `success` or
`fail`, database `music`, user `neo4j`, client `MCP4NEO4J/2.1.1`, one
transaction id per statement; the write as one multi-line statement; with
`--explain`, an `EXPLAIN` of each read immediately before it; the three
startup probes, the `gds.version` one failing. Optional prompt in the
session, to compare with the log:

> List every Cypher statement you executed in this session through the neo4j
> server, in order, with the tool you used for each and one sentence on what
> it returned or changed. Do not run anything new.

Recovery is a slide; nothing runs.

## 64–72 Recipe, homework, bridge

Slides only. The exit question: name one field of the stdio entry and which
process reads it; name one observation that proves a write happened that did
not come from the model.

## After class

```sh
cd "$NEO4J_HW_DIR" && uv run --frozen python database.py check
```

If it reports a `P09`, revert it in Query with
`MATCH (p:Playlist {id:'P09'}) DETACH DELETE p` on `music` and check again.
Leave `.mcp.json` in the package in its read-only form. Note the session's
Claude Code version and anything that differed from the pilot in
`reports/desktop-pilot.md` under open items.

## LLM-free fallback for the whole chain

From the homework package with the variables set:

```sh
uv run --frozen python verify_live.py --output ../../module-software-engineering/demos/lecture-mcp-neo4j/reports/live-desktop.json
```

It starts the server the way `.mcp.json` does, lists its tools, calls
`get-schema` and the two reference queries, and compares every result with
the CSV oracle; `reports/live-desktop.json` is the 2026-11-18 capture. The
pilot's readiness script, `pilot_desktop_check.py`, lists tools in both
modes and is the quickest proof that the database, APOC, the credentials,
and the server all work before Claude Code enters the picture.
