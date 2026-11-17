# Music homework setup

This path uses Neo4j Desktop, a disposable Neo4j **5.26.0** database, matching
**APOC 5.26.0**, Python 3.12+, uv, and Claude Code. Database/driver/MCP checks
were rehearsed with Neo4j Community 5.26.0 and Java 21 on macOS arm64, using
an isolated command-line instance. Desktop GUI steps and Windows shell variants
below require instructor rehearsal on the teaching machines. Newer Desktop
releases may offer different database versions; use the tested pair where
available, or have the instructor verify another matching version before class.
Do not downgrade or alter an existing database to do this assignment.

The pinned provider is official **neo4j-mcp-server 2.1.1**, which packages its
provider executable in a Python wheel. Its release requires APOC meta procedures.
The loader itself needs no APOC. The Python client is official `mcp==2.3.0` and
the driver is `neo4j==6.0.3`; `uv.lock` fixes their transitive dependencies.

## 1 Prepare a disposable instance

Install [Neo4j Desktop](https://neo4j.com/download/) and create a separate instance
named `music-mcp-homework`. Select the tested database version and choose your
own password. Start it. In its plugin controls, install the APOC version matching
the database and restart the instance. Do not install an arbitrary latest JAR.
If the provider reports missing meta procedures, inspect APOC installation and
procedure configuration before changing agent prompts.

Use the instance's actual Bolt address; `bolt://127.0.0.1:7687` is the normal
local default, not a promise that your instance uses that port. The database
inside the instance is named `neo4j`. The instance display name and database
name are different. This package uses Community-compatible uniqueness constraints
and does not need the older loader's node keys, typed relationships, or similarity
precomputation. Some Desktop distributions use an Enterprise edition; database
role controls must be verified in that actual edition.

Open Query in Desktop. Run:

```cypher
RETURN 1 AS ready;
```

You should receive one row, `ready = 1`. Then verify the plugin:

```cypher
SHOW PROCEDURES YIELD name
WHERE name STARTS WITH 'apoc.meta.'
RETURN name ORDER BY name;
```

You should receive meta procedure names. Empty results are not a readiness pass.
Presence alone is insufficient: during rehearsal, the schema call still failed
because `apoc.meta.schema` was sandboxed. For this disposable instance, open its
configuration and set the following once (edit an existing setting rather than
adding a duplicate), then restart:

```properties
dbms.security.procedures.unrestricted=apoc.meta.*
```

This permits the trusted plugin's meta family; do not replace it with an
unrestricted `apoc.*` or `*` merely to suppress an error. If your deployment has
an explicit procedure allowlist, have the instructor reconcile it as well.
Test actual execution:

```cypher
CALL apoc.meta.schema() YIELD value RETURN value;
```

Expect a schema map. Review [APOC installation](https://neo4j.com/docs/apoc/current/installation/)
and [procedure security](https://neo4j.com/docs/apoc/current/security-guidelines/)
when configuring a different version or a shared database.
The provider's own requirement check is the next compatibility check. See
[Neo4j MCP](https://github.com/neo4j/mcp) for current provider requirements.

## 2 Prepare the Python environment

Start a terminal **in this homework directory**, which contains `pyproject.toml`.

```sh
uv sync --locked
uv run --frozen python -m pytest -q
```

Expect the fixture tests to pass. They do not connect to Neo4j or a model. A
failed download is an installation/network problem, not a bad music query.
Do not update the lock to conceal an installation failure. `uv` must be on the
PATH of the shell used to launch Claude Code as well as your interactive terminal.

## 3 Set connection values without storing your password

For bash or zsh on macOS/Linux:

```sh
export MUSIC_MCP_DIR="$PWD"
export MUSIC_DB_URI='bolt://127.0.0.1:7687'
export MUSIC_DB_USER='neo4j'
```

Read the password without echoing it. In **bash**:

```sh
read -r -s -p 'Homework database password: ' MUSIC_DB_PASSWORD
export MUSIC_DB_PASSWORD
```

In **zsh**:

```sh
read -r -s 'MUSIC_DB_PASSWORD?Homework database password: '
export MUSIC_DB_PASSWORD
```

Then map these values for the direct loader/check commands:

```sh
export NEO4J_MCP_URI="$MUSIC_DB_URI"
export NEO4J_MCP_USERNAME="$MUSIC_DB_USER"
export NEO4J_MCP_PASSWORD="$MUSIC_DB_PASSWORD"
export NEO4J_MCP_DATABASE='neo4j'
```

For **PowerShell** (syntax provided; not platform-rehearsed):

```powershell
$env:MUSIC_MCP_DIR = (Get-Location).Path
$env:MUSIC_DB_URI = 'bolt://127.0.0.1:7687'
$env:MUSIC_DB_USER = 'neo4j'
$musicSecret = Read-Host 'Homework database password' -AsSecureString
$env:MUSIC_DB_PASSWORD = [System.Net.NetworkCredential]::new('', $musicSecret).Password
$env:NEO4J_MCP_URI = $env:MUSIC_DB_URI
$env:NEO4J_MCP_USERNAME = $env:MUSIC_DB_USER
$env:NEO4J_MCP_PASSWORD = $env:MUSIC_DB_PASSWORD
$env:NEO4J_MCP_DATABASE = 'neo4j'
```

No `.env` loader is implied. These are process environment variables inherited
by programs started from this terminal. Launching the host elsewhere may not
inherit them. Do not paste the password into `.mcp.json` or a submitted transcript.

## 4 Load and check

Ensure the target instance is your new disposable one. The loader refuses a
nonempty database instead of mixing the fixture into existing data.

```sh
uv run --frozen python database.py load
uv run --frozen python database.py check
```

Both print fixture identity and counts. Expected counts are 36 Track, 8 Artist,
6 Album, 8 Playlist, 4 User nodes; 8 OWNS, 89 playlist HAS_TRACK, 36 album
HAS_TRACK, and 48 ARTIST relationships. There are 92 playlist CSV records but
89 occurrence relationships because three exact duplicates collapse. P01 still
has two occurrences of T01 at different positions.

The loader reads CSVs itself and passes rows as query parameters. There is no
Desktop import-folder copying or `LOAD CSV` URL configuration. Graph relationships
are built by `queries/load.cypher`. Preserve this distinction when comparing the
older course exercises.

If a previous interrupted load left partial data, inspect the disposable instance
in Desktop and recreate it rather than guessing which rows to delete. An optional
reset exists only for a recognized complete fixture:

```sh
uv run --frozen python database.py reset --confirm-fixture fictional-music-v1
```

This deletes fixture nodes and relationships in the selected database. It refuses
unrecognized counts/identities; nevertheless verify the instance and URI yourself.
It is never part of normal setup and must never target other course databases.
After a deliberate reset, rerun `load`, then `check`.

## 5 Configure and use the MCP provider

In a separate homework repository, copy `.mcp.json.example` from this package to
`.mcp.json`. Keep `MUSIC_MCP_DIR` pointing to this package, since the pinned project
and `launch_server.py` live here. The configuration's `uv run --directory` argument
makes the provider launch independent of the host repository's working directory.

Start `claude` from that repository **in the terminal with the variables above**.
Inspect `/mcp`, approve the project server through the ordinary host interface,
and confirm `music` is connected. The example expands variables in Claude Code;
the provider receives `NEO4J_MCP_*` values. This is different from JSON doing shell
expansion by itself. Project configuration is safe to share only after inspection.

The launcher requires connection values, forces `READ_ONLY=true`, disables provider
telemetry, and filters tools to `get-schema` and `read-cypher`. No write tool should
appear. These are provider settings, not a claim that Community credentials enforce
an independent database read role. Use a restricted database user where your tested
edition supports it; host approval and downstream authorization remain distinct.
The exercise uses trusted supplied read queries and a disposable dataset.

Test without a model first if needed:

```sh
uv run --frozen python verify_live.py
```

This launches the official provider as a real child process, calls the schema
and reference queries, and writes actual results to `evidence/live.json`. It also
compares direct query answers to a CSV-based oracle. It does not establish model
tool selection or final-answer grounding. Instructor expected answers are kept
outside the student export, although the verification code is intentionally open.

Now return to the tasks in [README.md](README.md). Ask the host to inspect the
schema before proposing queries. Keep results bounded and inspect IDs/counts.

## 6 Troubleshooting by layer

| Observation | Check next |
|---|---|
| Missing-variable message on stderr | Start from the shell where the variables are set; verify names, not secret values |
| Connection refused | Is the instance started and is the Bolt address correct? |
| Authentication rejected | Did you supply the instance's chosen password and username? |
| Direct reads work, provider requires APOC meta | Install matching APOC, restart, inspect procedure availability |
| `/mcp` has no music server | Check project root, filename, JSON, approval/loading, and host scope |
| Provider process cannot find uv | Check the host's inherited PATH |
| Connected but no actual query call | Inspect discovered tools and prompt/host selection |
| Rows correct but answer wrong | Compare final claims against row IDs/counts; ask for correction with evidence |

Exit the host and stop the disposable instance when finished. Closing Claude Code
stops its stdio child; it does not necessarily stop Neo4j Desktop's database.
