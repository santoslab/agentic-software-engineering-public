# Music fixture setup

This file covers what is specific to the music fixture: the Python
environment, the connection variables, loading the data into the `music`
database, checking it, and resetting it. Everything about Neo4j Desktop, APOC,
creating the database, the `.mcp.json` entry, starting Claude Code, and
diagnosing failures in the host is in the general guide,
[`../neo4j-desktop-mcp-setup.md`](../neo4j-desktop-mcp-setup.md), which every
Neo4j activity in the course shares.

Observed on 2026-11-18 (instructor pilot, macOS): Neo4j Desktop 2.3.0 running
Neo4j 2026.10.0 Enterprise (the edition Desktop installs, with its Developer
license) with APOC 2026.10.0-core from the Plugins tab; `neo4j-mcp-server`
2.1.1 started by `uvx`; uv 0.12.23; Claude Code 2.1.311. Use the Neo4j
version Desktop offers you; nothing here pins an older one. The Python side is
locked: `uv.lock` fixes the driver `neo4j==6.0.3`, the MCP client
`mcp==2.3.0`, and their dependencies; Python 3.12 or newer. The server itself
is not a Python dependency of this package: `uvx` downloads it once (about
10 MB) the first time Claude Code or `verify_live.py` starts it.

## 1 Before this file

Please make sure that you go through Sections 1 to 3 of the general
guide to get the Neo4j MCP setup for an instance.  
You should end up with the Neo4j instance running, APOC is
installed and both verification queries pass, and `CREATE DATABASE music IF
NOT EXISTS` has been run. The loader does not create the database for you, and
it refuses to load into a database that already holds data.

## 2 The Python environment

Open a terminal in this folder (it contains `pyproject.toml`) and run

```sh
uv sync --locked
uv run --frozen python -m pytest -q
```

Expect the tests to pass. They touch neither Neo4j nor a model; they check
that the fixture files are intact and that the shipped configuration has the
expected shape. A failed download is a network or installation problem, not a
fixture problem; do not update the lock to make it go away. On Python 3.14 the
driver may print a `DeprecationWarning` about `asyncio.iscoroutinefunction`;
it is harmless.

## 3 Connection variables

The loader, the check, the verifier, and the MCP server all read the same
`NEO4J_MCP_*` variables, so you set them once per terminal and start Claude
Code from that terminal. These are the general guide's lines (its section 4)
plus the database name. In **zsh** (the macOS default):

```sh
export NEO4J_MCP_URI='neo4j://127.0.0.1:7687'
export NEO4J_MCP_USERNAME='neo4j'
export NEO4J_MCP_DATABASE='music'
read -r -s 'NEO4J_MCP_PASSWORD?Password for neo4j: '; export NEO4J_MCP_PASSWORD; echo
```

In **bash**:

```sh
export NEO4J_MCP_URI='neo4j://127.0.0.1:7687'
export NEO4J_MCP_USERNAME='neo4j'
export NEO4J_MCP_DATABASE='music'
read -r -s -p 'Password for neo4j: ' NEO4J_MCP_PASSWORD; export NEO4J_MCP_PASSWORD; echo
```

In **PowerShell 7** (not rehearsed on Windows):

```powershell
$env:NEO4J_MCP_URI = 'neo4j://127.0.0.1:7687'
$env:NEO4J_MCP_USERNAME = 'neo4j'
$env:NEO4J_MCP_DATABASE = 'music'
$env:NEO4J_MCP_PASSWORD = Read-Host -MaskInput 'Password for neo4j'
```

Read the URI off your instance card; `neo4j://127.0.0.1:7687` is what Desktop
shows for a single local instance. The password is typed, shown as nothing,
and lives only in this terminal: a new window needs the lines again. If you no
longer know it, section 4 of the guide says how to set a new one. Never paste
it into `.mcp.json`, a transcript, or your submission.

`database.py` targets `music` when `NEO4J_MCP_DATABASE` is unset, so the
fixture cannot land in the `neo4j` default database by accident; set the
variable anyway, so that every tool in the chain agrees.

## 4 Load and check

```sh
uv run --frozen python database.py load
uv run --frozen python database.py check
```

Both print the fixture identity, the database, and the counts. Expected:

```json
{
  "fixture": "fictional-music-v1",
  "database": "music",
  "counts": {
    "Track": 36, "Artist": 8, "Album": 6, "Playlist": 8, "User": 4,
    "OWNS": 8, "PLAYLIST_HAS_TRACK": 89, "ALBUM_HAS_TRACK": 36, "ARTIST": 48
  }
}
```

The CSVs hold 92 playlist rows, but three are exact duplicates of another
row, so 89 `HAS_TRACK` relationships result; P01 lists T01 at two positions,
which are two occurrences of one track. The loader reads the CSVs itself and
passes the rows as query parameters to
[`queries/load.cypher`](queries/load.cypher): uniqueness constraints on `id`
first, then `MERGE`. There is no import folder and no `LOAD CSV`.

`check` compares the live counts with the manifest and exits with
`Readiness mismatch` and both sets of counts when they differ. It is a
"fixture is pristine" test. Task 5 of the homework relies on it noticing one
added playlist.

## 5 Reset, only when needed

`load` refuses a nonempty database (`Load refused: database is not empty`).
If an interrupted load left partial data, look at the database in Desktop's
Query tool (Database selector on `music`) before deleting anything. The reset
runs only against a database that matches the complete fixture:

```sh
uv run --frozen python database.py reset --confirm-fixture fictional-music-v1
```

For a half-loaded database it refuses; in that case run
`MATCH (n) DETACH DELETE n` in Query **with `music` selected**, then `load`
and `check` again. Neither command is part of normal setup, and neither may
be pointed at `chapter01` or any other database.

## 6 Optional: the whole chain without a model

```sh
uv run --frozen python verify_live.py
```

This connects with the driver, checks the fixture, runs the two reference
queries, then starts `uvx neo4j-mcp-server@2.1.1` in read-only mode exactly
as `.mcp.json` does, lists its tools, calls `get-schema` and `read-cypher`,
and compares every result with a CSV-based oracle. It writes
`evidence/live.json` (ignored by git). The server's own log lines
(`Telemetry disabled.`, `Registered server tools`, `initialize requirements
verified`, `tool call completed`) appear on stderr; one `ERROR` line
mentioning `gds.version` means Graph Data Science is not installed, which is
intended. A pass here means the database, APOC, your credentials, and the
server all work; what remains is the host, which Task 3 of the homework
checks with `/mcp`.

## 7 The database's own record

You may find it useful in your projects to be able to see a log of
everything that was passed through the MCP interface into Neo4j.  

This homework provides an example script to support that.
`query_log.py` prints the Cypher statements the instance executed, read from
its `logs/query.log`. By default it shows the statements sent by the MCP
server and hides the `EXPLAIN` the server runs before each read:

```sh
uv run --frozen python query_log.py --last 10
uv run --frozen python query_log.py --all --since 2026-11-18T17:30
```

On macOS with one Desktop instance it finds the log itself; otherwise pass
`--log PATH`. The directory is also the answer to
`SHOW SETTINGS YIELD name, value WHERE name = 'server.directories.logs' RETURN value`
in Query. The log is written by the database, not by Claude Code or the
server, which is what makes it useful.

## 8 Next

Section 5 of the general guide: copy `.mcp.json.example` to `.mcp.json` in
this folder (`.claude/settings.json` is already here), then its section 6,
then the tasks in [`README.md`](README.md).

## When the loader fails

| What you see | Layer | What to do |
|---|---|---|
| `Missing environment variables: NEO4J_MCP_PASSWORD` (or other names) | This shell | Run the section 3 lines in this terminal. The names are the problem, not the values. |
| `AuthError` with `Neo.ClientError.Security.Unauthorized` and `authentication failure` | Database credentials | Wrong password for `neo4j`. Retype it (section 3). The instance's `logs/security.log` records `failed to log in: invalid principal or credentials`. |
| A connection error naming `127.0.0.1:7687` | Database not reachable | The instance is stopped, or another instance holds the port. Start it in Desktop and check the card. |
| An error saying the database `music` does not exist | Database | `CREATE DATABASE music IF NOT EXISTS;` in Query; wait for `online` in `SHOW DATABASES`. |
| `Load refused: database is not empty` | Target database | Section 5. Confirm that `NEO4J_MCP_DATABASE` is `music`, not a database you care about. |
| `Readiness mismatch` right after `load` | Data | Read both count sets. A previous partial load or a stray write; section 5. |

For failures in Claude Code (`MCP config diagnostics`, `Failed to reconnect
to neo4j: 0`, a missing write tool), use section 8 of the general guide.
