# Connecting an agent to a database through a local MCP server: Neo4j

## 0 Where this fits

The [adoption lecture](lecture-mcp-adoption.md) provided an
introduction to basic MCP concepts.  You saw four key things. A
repository declares that it wants to use an MCP server by configuring
info about the server in `.mcp.json`; the host's (e.g., Claude Code)
internal MCP client connects to the the declared MCP server 
and discovers its tools via the MCP operation `tools/list`; as the model works it gets
assistance by selecting appropriate tools from the list and sending
requests to the host to make tool calls, the host routes the 
call to the MCP server via the MCP operation `tools/call`.  The tool
call response from the MCP server is added to the session conversation
and sent back to the model.  The server in that lecture was a remote public documentation
service reached over HTTP, and the calls were reads of documentation text.

This lecture keeps every one of those objects (the configuration of
MCP servers for the Claude Code host via `.mcp.json`) and changes three things.

1. The MCP server is now a local program on your own machine (not
   remote) that the host starts as a child process and talks to 
   over its standard input and output.
2. That program is not itself the capability. It is an adapter in front of a
   third process, a Neo4j database that you own, that it reaches with the
   Neo4j driver protocol.
3. The tool's argument is a program, a Cypher statement (a Neo4j database query
   or operation), that the database executes with the privileges of
   the account the server logged in with. One of the MCP tools used updates
   the database.

The above set up will enable us to use natural language (via talking
to Claude) to query and update the database instead of having to write
Cypher queries.  Claude will take care of converting our natural
language requests to Cyber and sending them to Neo4j via the MCP set
up above.

The example database that we will use is a simple fictional music database,
similar to what you used in your first Neo4j homework.  

This lecture will lead you into a new homework.  The homework, [Connect Claude Code to Neo4j: the music fixture](../../neo4j/02-neo4j-music-mcp/README.md),
guides you through reproducing what is shown in class on the music
database.  The main goal of this is to give you enough information so
that you would be able to set up a similar MCP approach for your own
Neo4j database.

In both the previous lecture and in this lecture, we use existing MCP servers.
The upcoming [dice lecture](lecture-mcp-dice.md) then builds a server
of our own.  That lecture will help you understand how to extend any
of your own application with MCP capabilities so that agents can work
with them directly.

We don't want to clutter the conceptual themes of this lecture with
too many lower level details.  So two supporting documents are
provided to help with the details.  The
[general setup guide](../../neo4j/neo4j-desktop-mcp-setup.md) says how to
prepare a Neo4j Desktop instance for use with MCP, how to do things
like handle the database password, what to write in
`.mcp.json`, and how to confirm that Claude is hooked up to the Neo4j
MCP server using the Claude `/mcp` command. The homework's
[SETUP.md](../../neo4j/02-neo4j-music-mcp/SETUP.md) says how to load and check
the fixture (the sample database). 
The lecture notes in this file focus on the high-level issues of the
meaning of those detailed steps and what the host, the
server, and the database each do when you follow them.

Everything quoted below, every prompt, statement, dialog, log line, and error
text, was observed in the instructor's pilot of 2026-11-18 on Neo4j Desktop
2.3.0 running Neo4j 2026.10.0 Enterprise with APOC 2026.10.0-core,
`neo4j-mcp-server` 2.1.1, and Claude Code 2.1.311 on macOS. The record is
[`reports/desktop-pilot.md`](../demos/lecture-mcp-neo4j/reports/desktop-pilot.md)
in the lecture's demo folder. Where the notes describe something the pilot did
not exercise, they say so. Text produced by the model is labeled as model
output: it is what one session produced, not what every session will produce.

In class the instructor runs the demonstration on a prepared example
database instance. Each section
below names the part of the demonstration it accompanies and shows the
captured screenshots from the instructor's pilot run, 
so that the notes can be read without the demonstration.

## 1 What changes architecturally

The adoption lecture's server declaration was two fields:

```json
{
  "mcpServers": {
    "microsoft-learn": {
      "type": "http",
      "url": "https://learn.microsoft.com/api/mcp"
    }
  }
}
```

This lecture's declaration is:

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

The JSON map structure, the key that names the connection, and the absence of any tool
definition (we describe the server providing tools, not the tools
themselves) are the same. Every other difference between the two entries is
one of the architectural changes this section explains.

### 1.1 From a remote endpoint to a child process

With `type: "http"`, the host (Claude Code) opened a network connection to a program that
someone else runs remotely. The host did not start it, could not stop it, and learned
nothing about it except what it answered over the protocol.

With `type: "stdio"`, the host **starts the program**. At the beginning of a
session Claude Code reads `.mcp.json`, runs `uvx neo4j-mcp-server@2.1.1` as a
child process with the environment given in `env`, connects the child's
standard input and standard output to its internal MCP client, and keeps the child's
standard error as a log. The protocol messages are the same JSON-RPC messages
that went over HTTP in the adoption lecture; only the pipe they travel on is
different. When the session ends the child is terminated. When you ask `/mcp`
to reconnect, the host stops the old child and starts a new one; the pilot's
host log shows exactly that sequence, a `SIGINT` and a `SIGTERM` to the old
process and a fresh start.

Three consequences follow.

**The host needs a program to run.** `uvx` is the `uv` tool runner. The first
time it is asked for `neo4j-mcp-server@2.1.1` it downloads that release of
the server, a wheel of about 10 MB wrapping a Go binary, into its cache. In
the pilot the cold start took 1.3 s on the instructor's network and later
starts 0.07 s. The program is resolved through the `PATH` of the shell that
started Claude Code, which is one reason the guide insists that Claude Code be
started from a prepared terminal.

**The server's lifetime is the session's.** Exiting Claude Code ends the
server. It does not end the database, which Neo4j Desktop keeps running until you
stop it. The adoption lecture's remote service existed before and after your
session; this server exists only during it.

**Failures move onto your machine.** A missing program, a missing variable,
a server that cannot reach its database: each of these is now something that
happened on your computer, and each leaves a trace in a file you can read.
Section 3.5 shows two of them and Section 7 says where the traces are.

![Host, model service, and one declared server, from the adoption lecture](../slides/diagrams/adoption-connections-basic.svg)

### 1.2 The server is an adapter in front of a third process

In the adoption lecture the server was the capability. Microsoft's service
searched its own documentation and returned the text. Here the server does
almost nothing itself. `neo4j-mcp-server` holds one connection to a Neo4j
database, using the official Go driver (the database's log identifies it as
`Go Driver/6.4.0`), and translates between two protocols: MCP on the side of
the host, and the Neo4j driver protocol, Bolt, on the side of the database.
A `tools/call` for `read-cypher` becomes a Cypher statement sent over that
connection; the rows that come back become the text of the tool result.

![Three processes and their responsibilities](../slides/diagrams/neo4j-processes.svg)

So there are three processes and two protocols, and the question "who did
what" has a different answer at every step:

| Step | Who | Evidence of it |
|---|---|---|
| Decides that a tool call is wanted and composes its argument, the Cypher | The model | The tool call in the session, with its `query` argument |
| Shows the call to you, applies permission rules, routes the call to the server | The host, Claude Code | The permission dialog; the host's per-server log |
| Receives the call, checks the statement, sends it to the database, returns rows as JSON | The server, `neo4j-mcp-server` | The server's own log lines on standard error |
| Executes the statement and records it | The database, Neo4j | The instance's `query.log`, with the client identified as `MCP4NEO4J/2.1.1` |

The MCP server also talks to the database on its own, not only when the
model asks. At startup it runs three statements, visible in the database's
query log: `RETURN 1 as first` to confirm the connection,
`SHOW PROCEDURES YIELD name WHERE name = 'apoc.meta.schema' RETURN count(name) > 0 AS apocMetaSchemaAvailable`
to confirm that the APOC plugin used by the MCP server is present, and `RETURN gds.version() as gdsVersion`
to probe for the optional Graph Data Science library. The third fails on an
instance without that library and the failure is logged as an error on both
sides. It is expected to fail (its presence would disturb our simple demo
MCP setup), and it is why the guide tells students not to install
the GDS library: with it the server offers a fourth tool, and tool counts in
class and at home would differ.

Note: APOC (Awesome Procedures On Cypher) is a Java-based add-on library for Neo4j that provides hundreds of custom procedures and functions callable directly from Cypher queries. It extends standard Cypher capabilities for tasks like data integration, data conversion, graph refactoring, and graph inspection.

Returning to the table above, each process in the table 
knows different things. The model sees tool definitions and tool
results. The host sees the configuration file, the environment, every call
and every result. The server sees the connection details and every
Cypher statement. The database sees a Bolt client that logged in as `neo4j`, with a client
application name of `MCP4NEO4J/2.1.1`, sending statements. The database does
not know that a language model composed the Cypher statements.

### 1.3 The configuration now carries the provider's settings

The adoption entry configured nothing about the server; a URL was all the
host needed. The stdio entry's `env` block is the **server's** configuration,
passed through the host. Each process reads a different part of the file:

- Claude Code reads `type`, `command`, `args`, and the *keys* of `env`. It
  replaces `${NAME}` with the value of `NAME` in its own environment, and
  `${NAME:-default}` with the default when `NAME` is unset. This expansion is
  Claude Code's, not the shell's and not JSON's. If a variable without a
  default is unset, the host notices before launching and reports it in
  `/mcp` (Section 3.5).
- `neo4j-mcp-server` reads the `NEO4J_MCP_*` values it receives: where the
  database is, who to log in as, which database to use, whether to offer the
  write tool, whether to report telemetry.
- Neo4j sees only the connection: an address, a username, a password, a
  database name.

The password is referenced, never written. `.mcp.json` is meant to be
committed and shared; the environment variable is not. This separation
matters more than it did in the adoption lecture because the model can read
files in the project with ordinary tools. In the pilot, the first thing the
model did in a fresh session was `ls -la` and `cat .mcp.json`. It saw the
string `${NEO4J_MCP_PASSWORD}`, not a password, because that is what the file
contains. Had the value been written into the file, the model would have had
it in its context (which is a potential security problem).

The configuration also shapes discovery. `NEO4J_MCP_READ_ONLY` decides
whether `write-cypher` appears in `tools/list` at all. Changing that one
field and restarting changes the tool count shown in `/mcp` from two to
three. The adoption lecture said that discovery is dynamic and controlled by
the provider; this is the first place you can see it happen by changing a
provider setting yourself.

### 1.4 The argument is a program, and the result is data inside the envelope

The adoption lecture's tools took data as arguments: a search string, a URL.
Their schemas said so:

```json
{"name": "microsoft_docs_fetch",
 "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}}
```

The schema of `read-cypher`, taken from the pilot's `tools/list` capture, is
almost as small:

```json
{"name": "read-cypher",
 "description": "read-cypher can run only read-only Cypher statements. For write operations (CREATE, MERGE, DELETE, SET, etc...), schema/admin commands, or PROFILE queries, use write-cypher instead.",
 "inputSchema": {"type": "object",
   "properties": {"query": {"type": "string", "description": "The Cypher query to execute"},
                  "params": {"type": "object", "description": "Parameters to pass to the Cypher query", "additionalProperties": true}},
   "required": ["query"], "additionalProperties": false}}
```

The above declaration for the `read-cypher` tool says that a field
name named `query` whose value is a string is required. 
But that string is a program (a Cypher query). It has a
grammar, a meaning, and an effect, and the database will execute whatever it
says (which could be wrong, or even dangerous -- i.e., an improperly
written delete operations). 
The schema can tell the host that the argument is a string;
it cannot tell anyone whether the string "does the right thing", e.g.,
whether it counts paths or distinct playlists, or whether it contains a clause that
changes data. That is why this lecture adds a step the adoption lecture did
not need: the query statement is proposed first by the model and
displayed to the user.  The user is then given a chance to confirm
that the query looks appropriate before it is sent through the MCP
connection.

The tool call result is also different in kind. A documentation fetch returned prose.
A `read-cypher` call returns a text content block whose text is itself JSON,
an array of row objects:

```json
{"content": [{"type": "text", "text": "[\n  {\n    \"artist_id\": \"A07\",\n    \"artist_name\": \"Glass Meadow\",\n    \"playlist_count\": 8\n  },\n  ..."}],
 "isError": false}
```

JSON (following the protocol for Neo4J programmatic interactions) inside the JSON envelope
(following the protocol for MCP). The envelope is MCP's; the host handles it.
The inner array is the Neo4j MCP server's; it is what the model reads.
Interesting, you can double-check the queries that the model proposes
to send through MCP by running them yourself in the query panel of
Neo4j desktop.  The `get-schema`
result has the same shape, an array of `{key, value}` entries describing
labels, relationship types, and properties (Section 4).

Two further facts about `read-cypher`. The Neo4j MCP server enforces "read-only" by
classification: before executing a statement it runs `EXPLAIN` on it and
inspects the plan, which is why every read in the database's log is preceded
by an `EXPLAIN` of the same text. The server's documentation adds that
procedures misclassified as read-only can slip past this check. And the
statement runs with the database privileges of the account in
`NEO4J_MCP_USERNAME`. In the course setup that is `neo4j`, the administrator.
The read-only flag is a property of the server, not of the account.

### 1.5 Writes are a new class of operation

Nothing in the adoption lecture changed state anywhere (for example,
we didn't update the documentation on the Microsoft Learn server). 
The `write-cypher` tool, when enabled in your MCP configuration, 
executes any Cypher with write access. Its description, shown by the
host in the permission dialog, is one sentence: "write-cypher executes any
arbitrary Cypher query, with write access, against the user-configured Neo4j
database." A write that succeeds is committed when the call returns. The
tool offers no way to begin a transaction in one call and roll it back in
another, so once the result is back there is nothing to undo through the
tool (!).

There are several ways to guard against "bad things happening with `write-cypher`".
Section 6 follows one write from prompt to verification and names the three
places that decide whether a write can happen at all: the server's read-only
flag, the host's permission rules, and the database account's privileges.
Section 10 says what to do when you work on a database that cannot simply be
reloaded.

### 1.6 Verification routes that do not pass through the model

In the adoption lecture, checking an answer meant opening the cited article.
The evidence and the claim lived in the same document, and the only
independent party was the reader.

Here the data is yours and sits in a database you can query directly. That
gives three routes to the same facts that do not involve the model at all:

- **Desktop's Query tool.** Paste the statement the model ran, select the
  same database, run it, compare the rows.
- **A check that knows what the data should be.** The homework's
  `database.py check` is a little utility program that compares 
  aspects of the database state (e.g., counts of entries of a certain
  kind) against the fixture's manifest (i.e., an indication of
  expected results) and reports exactly which counts changed after a write.
- **The database's own log.** Neo4j records every statement it executed,
  with the client that sent it. Section 7 shows how to read it.

The discipline the adoption lecture taught, that a connected server does not
show a call happened and a call does not show the answer follows from its
rows, becomes checkable at every link.

### 1.7 The two lectures side by side

| | Adoption lecture | This lecture |
|---|---|---|
| Transport | HTTP to a remote endpoint | stdio to a child process the host starts |
| Who runs the server | The vendor | You, through the host, for the session |
| Configuration | A URL | The server's settings in `env`, expanded by the host |
| Credentials | None | A database password, referenced from the environment |
| What the server is | The capability itself | An adapter to a database, a third process |
| Tool arguments | Data: a query string, a URL | A program: Cypher |
| Tool results | Text | JSON rows inside the text block |
| Operations | Reads | Reads and writes |
| Controls on effects | The host's permission policy | Server flag, host rules, database account |
| Checking an answer | Read the cited source | Replay the statement; run a check; read the database's log |
| Where failures appear | In `/mcp`, from the network | In `/mcp`, in the host's per-server log, in the database's logs |

## 2 The database side, briefly

The procedure is in sections 1 to 3 of the [setup guide](../../neo4j/neo4j-desktop-mcp-setup.md).
What follows is the vocabulary the rest of these notes rely on.

An **instance** is one running Neo4j server, managed by Neo4j Desktop,
listening on one address. The instance card shows the address as a
Connection URI, `neo4j://127.0.0.1:7687`, and the version. Desktop does not
use the word Bolt anywhere; the `neo4j://` scheme is what the server will be
given and it works as written for a local instance.

![The instance card](../../neo4j/resources/desktop-01-instance-card.png)

An instance holds several **databases**. The edition Desktop installs is
Enterprise under a developer license, so `CREATE DATABASE music IF NOT EXISTS`
works, and `SHOW DATABASES` lists `system`, `neo4j`, the `chapter01` database
from exercise 01, and `music`. One database per activity means that loading
or deleting one activity's data cannot touch another's, and that the MCP
server, which is pointed at exactly one database by `NEO4J_MCP_DATABASE`,
cannot reach the others.

![SHOW DATABASES with music starting](../../neo4j/resources/desktop-08-show-databases.png)

**APOC** is a plugin of the instance, installed once from the instance's
Plugins tab and serving every database in it. The MCP server needs it for two
reasons: since version 2.0.0 it refuses to initialize when APOC is absent,
and its `get-schema` tool is a call to `apoc.meta.schema`. In the pilot,
Desktop's installer also wrote the procedure permissions APOC needs into the
instance's configuration, so no file was edited.

One habit from the pilot that the homework repeats: Desktop's Query tool has
a Database selector in its header, and it defaults to `neo4j`. A statement
that returns nothing is very often a statement run against the wrong
database. Every replay in these notes was done with the selector on `music`.

## 3 Activating the local server

This section follows what the host does with the declaration from Section 1,
from the file to a connected server with a tool list. The guide gives the
same steps as instructions; here the point is what each step causes.

### 3.1 The entry, field by field

Below is a summary of all of the fields in the `.mcp.json` MCP
configuration file for Cluade.

| Field | Read by | Meaning |
|---|---|---|
| `"neo4j"` | Host | The name of this connection. It becomes the prefix of the model-visible tool names, `mcp__neo4j__read-cypher`, and the name `/mcp` shows. |
| `"type": "stdio"` | Host | Start a program and exchange MCP messages over its standard streams. The adoption entry had `"type": "http"` and a `url`. |
| `"command"`, `"args"` | Host | The program to start and its arguments: `uvx neo4j-mcp-server@2.1.1`. The version is pinned so that every student runs the release the pilot tested. |
| `"env"` | Host, then server | Variables for the child process. The host expands `${...}` references; the server reads the results. |
| `NEO4J_MCP_URI`, `NEO4J_MCP_USERNAME`, `NEO4J_MCP_PASSWORD` | Server | Where to connect and as whom. The first two have defaults that match a Desktop instance; the password has none, on purpose. |
| `NEO4J_MCP_DATABASE` | Server | The one database this server will query. The only field that changes between activities. |
| `NEO4J_MCP_READ_ONLY` | Server | `"true"`: offer `get-schema` and `read-cypher`. `"false"`: offer `write-cypher` as well. |
| `NEO4J_MCP_TELEMETRY` | Server | `"false"` stops the server from reporting usage to its vendor. |

The command `claude mcp add --scope project --transport stdio -e
NEO4J_MCP_URI=... neo4j -- uvx neo4j-mcp-server@2.1.1` writes an entry
of the same shape.  In our lectures, we emphasize defining the
`.mcp.json` file because the file is what you will read, review, and
commit. 

### 3.2 What happens when a session starts

1. Claude Code reads `.mcp.json` in the project directory. The first time it
   sees a project server it asks whether to use it; the answer is recorded in
   `.claude/settings.local.json`, which is personal and not committed.
2. It expands the `${...}` references against its own environment. A
   reference without a default that is unset is reported at this point
   (Section 3.5); nothing is launched.
3. It starts `uvx neo4j-mcp-server@2.1.1` with the resulting environment.
   `uvx` fetches the release into its cache if it is not there yet, then
   runs it.
4. The host's MCP client sends `initialize` to the server. The server does not simply
   acknowledge: it connects to the Neo4j database and runs its requirement checks
   (the three statements of Section 1.2). If the database is unreachable, the
   password is wrong, or APOC is missing, `initialize` fails with an error and
   the host marks the server as failed.
5. The client sends `tools/list`. The server answers with the tools its
   configuration allows (in our case, tools to report database schemas and to
   handle read and write Cypher queries).
6. The host presents the tools to the model. In Claude Code they may be
   presented as deferred names that the model loads on demand; in the pilot
   the model announced "I'll load the read tool" before its first call. This
   is the host facility the adoption lecture described, not a
   standardized MCP approach.

The server's own log for this sequence, captured in the pilot from standard
error, reads:

```text
time=2026-11-18T12:25:07.969-06:00 level=INFO msg="Telemetry disabled."
time=2026-11-18T12:25:07.971-06:00 level=INFO msg="Registered server tools" count=2 tools="[get-schema read-cypher]"
time=2026-11-18T12:25:07.971-06:00 level=INFO msg="request started" mcp_method=server/discover
time=2026-11-18T12:25:07.971-06:00 level=INFO msg="Handshake request: verifying requirements..." mcp_method=server/discover
time=2026-11-18T12:25:07.985-06:00 level=INFO msg="initialize requirements verified"
time=2026-11-18T12:25:07.987-06:00 level=INFO msg="request started" mcp_method=tools/list
```

In read-only mode the server also logs `Ignoring tool 'write-cypher': not
available in read-only mode`. On an instance without Graph Data Science, each
`tools/list` logs an `ERROR` whose message ends in
`Unknown function 'gds.version'`, followed by
`list-gds-procedures omitted from tools/list reason=gds_unavailable`. The
error line is the probe from Section 1.2 failing as expected.

### 3.3 Reading `/mcp`

After Claude Code is started with an appropriately configured
`.mcp.json` file, `/mcp` can be used to see information about the
host's MCP connections. 
`/mcp` is the host's view of the servers it connects to. The pilot's five
screens, in the same order the adoption lecture used for its documentation
server:

![Typing /mcp](../slides/images/mcp-neo4j-01-slash-mcp.png)

![The server list](../slides/images/mcp-neo4j-02-server-list.png)

The project server `neo4j` is listed as connected with 2 tools, under the
heading for project servers, that is, servers declared by the repository's
`.mcp.json` rather than by the user's own configuration.

![The server detail](../slides/images/mcp-neo4j-03-server-detail.png)

The detail shows the command the host ran, `uvx neo4j-mcp-server@2.1.1`, the
negotiated protocol version `2026-07-28`, the capability `tools`, the
configuration file the entry came from, and three actions: view tools,
reconnect, disable.

![The tool list](../slides/images/mcp-neo4j-04-tool-list.png)

Two tools, shown by the titles the server declared, Get Neo4j Schema and Read
Cypher, each tagged `read-only · open-world`. The tags are the server's tool
annotations (`readOnlyHint`, `openWorldHint` in the `tools/list` capture),
displayed by the host. They are declarations by the server, not something the
host verified.

![The read-cypher detail](../slides/images/mcp-neo4j-05-read-cypher-detail.png)

The tool's own name `read-cypher`, its full model-visible name
`mcp__neo4j__read-cypher`, its description, and its parameters:
`query (required): string` and `params: object`. This is the contract from
Section 1.4 as the host renders it.

### 3.4 Permission modes and the companion settings file

Claude Code has several permission modes, and which one a session is in
decides whether you will ever see a dialog as you to approve an MCP
tool call.  The line under the input box
names the mode. In **auto** mode the host approves tool calls itself
(based on its own heuristics about whether the tool call will be
"safe" or not); no dialog appears for anything, database writes
included.  In **manual** mode the
host asks the user before each tool call. The course starts sessions with
`claude --permission-mode manual`, and the line then reads `manual mode on`:

![The mode line in manual mode](../slides/images/mcp-neo4j-17-manual-mode-line.png)

Manual mode asks about reads as well as writes. In the pilot the first
schema call produced this dialog:

![A dialog for get-schema](../slides/images/mcp-neo4j-18-schema-permission-prompt.png)

and three read calls issued together produced three dialogs labeled 1 of 3,
2 of 3, and 3 of 3:

![Three batched read dialogs](../slides/images/mcp-neo4j-20-read-permission-prompt-1of3.png)

Seven database tool approval dialogs and two shell dialogs preceded the first write in that
session. A lecture or a homework cannot spend its time this way, and the two
read tools cannot change anything, so the course ships a project
`.claude/settings.json` beside `.mcp.json`:

```json
{
  "permissions": {
    "allow": ["mcp__neo4j__get-schema", "mcp__neo4j__read-cypher"]
  }
}
```

With it, reads run silently (no approvals are asked)
and only `write-cypher` triggers approval requests. The names of the
tools in the `allow` list above are the model-visible names from
Section 3.3.   This file is a host rule, the
second of the three controls of Section 6.7; it is also, like everything else
in this lecture, a JSON object you can read.

One more observation from the pilot. The dialog for a shell command carried a
suggestion: "Tip: auto mode handles these prompts for you", with an option
"Yes, and switch to auto mode".

![A shell dialog with the auto-mode suggestion](../slides/images/mcp-neo4j-19-bash-permission-prompt-auto-tip.png)

Taking that offer removes the write dialog for the rest of the session. The
homework asks you to decline it (we want you to experience the
guardrails provided for the write tool call).

### 3.5 Two failures as the host shows them

Both were produced on purpose in the pilot and both are failures students
produce by accident.

**The password variable is unset.** Claude Code was started from a terminal
where the environment variables of the guide had not been set. `/mcp` opened with a
diagnostics block:

```text
MCP config diagnostics ⚠

[Contains warnings] Project config (shared via .mcp.json)
Location: /private/var/folders/.../tmp.c2qo5QVNmd/.mcp.json
[Warning] [neo4j] mcpServers.neo4j: Missing environment variables: NEO4J_MCP_PASSWORD
```

and the server list showed `✘ neo4j`; its detail showed `Status: ✘ failed`.

![Missing variable: the diagnostics](../slides/images/mcp-neo4j-07-issue-no-password-a.png)

![Missing variable: the failed server](../slides/images/mcp-neo4j-07-issue-no-password-b.png)

The host detected the unexpanded reference before any process started and
named the variable. This is the easiest failure to diagnose, and it belongs
to the host configuration layer: the file is right, the environment is not.
The host's per-server log adds what happened next: the server was launched
anyway with the literal text `${NEO4J_MCP_PASSWORD}` as its password, and
its requirement check failed with
`Neo4jError: Neo.ClientError.Security.Unauthorized (The client is unauthorized due to authentication failure.)`.

**The instance is stopped.** To illustrate the effect of trying to
make an MCP tool call to a database instance that is not active, 
the database instance was manually stopped in the Neo4j Desktop. 
Asking `/mcp` to reconnect printed one line:

```text
Failed to reconnect to neo4j: 0
```

![Stopped instance: the failed reconnect](../slides/images/mcp-neo4j-08-issue-db-stopped-a.png)

![Stopped instance: the server detail](../slides/images/mcp-neo4j-08-issue-db-stopped-b.png)

The number is the JSON-RPC error code the server returned from `initialize`;
the host shows nothing else. The cause is in the host's per-server log,
written 16 seconds after the reconnect was requested:
`ConnectivityError: Unable to retrieve routing table from 127.0.0.1:7687: dial tcp 127.0.0.1:7687: connect: connection refused`.
After the instance was started again, reconnect printed
`Reconnected to neo4j.`, and the log recorded
`Successfully connected (transport: stdio) in 1208ms`.

![Stopped instance: reconnected](../slides/images/mcp-neo4j-08-issue-db-stopped-c.png)

The lesson these two failures teach together: `/mcp` tells you *that* a
server failed and sometimes *which variable* is missing; the reason a server
could not reach its database is in the server's own words, in the per-server
log. Section 7 gives its location and Section 8 the full table of
observations and layers.

## 4 Discovery you can read

The adoption lecture read a `tools/list` result for the documentation server.
The same result for this server, from the pilot's LLM-free capture
[`reports/live-desktop.json`](../demos/lecture-mcp-neo4j/reports/live-desktop.json),
has two entries in read-only mode:

```json
{"tools": [
  {"name": "get-schema",
   "description": "Retrieve the schema information from the Neo4j database, including node labels, relationship types, and property keys. If the database contains no data, no schema information is returned.",
   "inputSchema": {"type": "object", "properties": {}},
   "annotations": {"title": "Get Neo4j Schema", "readOnlyHint": true, "destructiveHint": false, "idempotentHint": true, "openWorldHint": true}},
  {"name": "read-cypher",
   "description": "read-cypher can run only read-only Cypher statements. For write operations (CREATE, MERGE, DELETE, SET, etc...), schema/admin commands, or PROFILE queries, use write-cypher instead.",
   "inputSchema": {"type": "object",
     "properties": {"query": {"type": "string", "description": "The Cypher query to execute"},
                    "params": {"type": "object", "description": "Parameters to pass to the Cypher query", "additionalProperties": true}},
     "required": ["query"], "additionalProperties": false},
   "annotations": {"title": "Read Cypher", "readOnlyHint": true, "destructiveHint": false, "idempotentHint": true, "openWorldHint": true}}
]}
```

`get-schema` takes no arguments. `read-cypher` takes the statement and an
optional map of parameters; parameters are the right way to pass values such
as an id into a statement, and the server itself uses them (Section 7 shows
`{sampleSize: 100}` in its schema call). With `NEO4J_MCP_READ_ONLY` set to
`false` the list gains `write-cypher`, with the same `query` and `params`
schema and the description quoted in Section 1.5. The pilot's readiness check
recorded both lists: `["get-schema", "read-cypher"]` and
`["get-schema", "read-cypher", "write-cypher"]`. A fourth tool,
`list-gds-procedures`, appears only when the Graph Data Science library is
installed.

The annotations are worth some further explanation. `readOnlyHint` and `destructiveHint`
are the server's own description of each tool. Claude Code displays them as
tags. It does not, in manual mode, exempt a read-only tool from the dialog;
that is what the allow rules of Section 3.4 are for.

The result of the Neo4j MCP tool `get-schema`, 
from the same capture, describes the music graph as
an array of entries, one per label and one per relationship type. Two of
them, reformatted:

```json
{"key": "Playlist",
 "value": {"type": "node",
           "properties": {"id": "STRING", "name": "STRING"},
           "relationships": {"HAS_TRACK": {"direction": "out", "labels": ["Track"], "properties": {"position": "INTEGER"}},
                             "OWNS": {"direction": "in", "labels": ["User"]}}}}
{"key": "Track",
 "value": {"type": "node",
           "properties": {"id": "STRING", "name": "STRING"},
           "relationships": {"ARTIST": {"direction": "out", "labels": ["Artist"]},
                             "HAS_TRACK": {"direction": "in", "labels": ["Album", "Playlist"], "properties": {"position": "INTEGER"}}}}}
```

Compare the JSON structure above to the following diagram:

![The music graph](../slides/diagrams/music-graph.svg)

A Playlist has `HAS_TRACK` going out to Track, with a `position` on the
relationship, and `OWNS` coming in from User. A Track has `ARTIST` going out
to Artist and `HAS_TRACK` coming in from two labels, Album and Playlist. That
last entry is the one that matters for the question in Section 5: a pattern
that starts at any node with `HAS_TRACK` will count album membership as well
as playlist membership. The model noticed this unprompted in the pilot; a
reviewer must notice it whether or not the model does.

The model sees these tools under the names `mcp__neo4j__get-schema`,
`mcp__neo4j__read-cypher`, and, when offered, `mcp__neo4j__write-cypher`.
Those names are what `.claude/settings.json` rules refer to, and they are
what the transcript records.

## 5 A read, end to end

The demonstration opens with one prompt against the prepared `music`
database, in a scratch repository that holds only `README.md`, `.mcp.json`,
and `.claude/settings.json`:

> Inspect the music database's schema, then tell me which five artists appear
> in the most distinct playlists.

Then it slows down and does the same thing in three prompts, which is the
pattern the homework asks for. The pilot's record of those three prompts
follows.

### 5.1 Schema first

> Use the neo4j MCP server to inspect the schema of the music database.
> Summarize the node labels, relationship types, and relationship directions
> in a short table. Do not run any other query yet.

To respond to the prompt above, Claude will issue `get-schema` call and no
other.  The model's table (model output) listed
the five labels with their properties and four relationship rows, User OWNS
Playlist, Playlist HAS_TRACK Track with `position`, Album HAS_TRACK Track, and
Track ARTIST Artist, and added two observations: that playlists and albums
both reach tracks through the same `HAS_TRACK` type, and that there is no
direct Album-to-Artist or User-to-Track relationship. Both are supported by
the `get-schema` result of Section 4.

Why ask for the schema at all when you have the diagram? Because the model
does not have the diagram, and a model that has not seen the labels and
properties guesses them. Every session in the pilot and in the homework
starts this way.

### 5.2 Propose without executing

> Which five artists appear in the greatest number of distinct playlists?
> Credit every artist on a collaboration; count a playlist at most once per
> artist; return artist id, name, and playlist count; order by count
> descending, then artist id ascending. Propose a bounded read-only Cypher
> query and explain how it avoids counting paths instead of playlists. Show
> the query and do not execute it yet.

The host executed nothing. The model proposed (model output):

```cypher
MATCH (p:Playlist)-[:HAS_TRACK]->(:Track)-[:ARTIST]->(a:Artist)
WITH a, count(DISTINCT p) AS playlistCount
RETURN a.id AS artistId, a.name AS artistName, playlistCount
ORDER BY playlistCount DESC, artistId ASC
LIMIT 5
```

with an explanation that is worth quoting in part because it is the review a
person should do, written out by the model: "Each row produced by the MATCH
is one path: a playlist, a track in it, and an artist on that track. One
playlist can reach the same artist many times, through several of their
tracks or through the same track listed at several positions. A plain count
of rows would count those paths. The DISTINCT inside the aggregate collapses
rows by playlist node identity, so a playlist contributes at most one to each
artist's total." And on the schema: "The schema shows HAS_TRACK coming from
both Album and Playlist. Anchoring the pattern on Playlist keeps album
membership out of the count."

A fluent explanation is a claim to check, not a check (i.e., the claim
gives a specific reviewable description of a property). The review, with the
question and the schema beside the statement:

| Check | In this statement |
|---|---|
| Labels and directions exist in the schema | `Playlist -HAS_TRACK-> Track -ARTIST-> Artist`: all three present, directions as `get-schema` reported |
| The pattern is anchored where the question is | `(p:Playlist)`, not an unlabeled node and not `Album` |
| Distinct count, not path count | `count(DISTINCT p)`, not `count(*)` |
| Collaborations credited to every artist | The pattern ends at `(a:Artist)` with no filter; a track with two `ARTIST` relationships yields two rows |
| The requested tie rule | `ORDER BY playlistCount DESC, artistId ASC` |
| Bounded | `LIMIT 5` |
| No write clause | `MATCH`, `WITH`, `RETURN`, `ORDER BY`, `LIMIT` only |

The reference statement in the homework,
[`queries/question-a.cypher`](../../neo4j/02-neo4j-music-mcp/queries/question-a.cypher),
differs only cosmetically: no `WITH` stage, and snake_case aliases. The pilot
counted this as a pass; the review step, not identical text, is the lesson.
Different sessions produce different statements, and the homework assesses
the review, not the match.

### 5.3 Run, and read the call

> Run that query with the neo4j read tool and answer from the returned rows.
> State that the result describes the fictional-music-v1 fixture.

![The read call, its argument, its rows, and the answer](../slides/images/mcp-neo4j-06-read-call.png)

One `read-cypher` tool call. Its `query` argument is the proposed statement,
character for character. Its result is five rows:

| artistId | artistName | playlistCount |
|---|---|---:|
| A07 | Glass Meadow | 8 |
| A08 | Indigo Current | 8 |
| A01 | Amber Circuit | 5 |
| A02 | Blue Orchard | 5 |
| A03 | Copper Kite | 4 |

The answer (model output) named the fixture, explained the tie-break by id,
and noted that an artist tied with Copper Kite at four playlists would have
been cut by the limit, so the table is a strict top five under the requested
ordering and not a list of everyone with that count. That last sentence is
the kind of thing a reviewer checks against the statement: `LIMIT 5` after
the ordering does exactly that.

Three records agree here: the argument shown in the host, the rows shown in
the host, and the prose. The homework asks you to keep all three because
they can disagree, and when they do, the disagreement locates the problem:
a wrong statement, a wrong database, or a wrong reading of right rows.

### 5.4 Replay outside the conversation

In Desktop's Query tool, with the Database selector on `music`, the
reference statement was pasted and run:

![The replay in Query](../../neo4j/resources/desktop-09-question-a-replay.png)

Same five rows, in 12 ms. What the replay establishes: this statement, run
against this database by a client that is not the model, returns these rows.
What it does not establish: that the statement answers the English question
(that was the review), or that the fixture was loaded correctly (that is
`database.py check`, and behind it the CSV oracle in the homework package
that computes the same answer without Neo4j).

### 5.5 A question the data cannot answer as asked

"Which artist is most popular?" has at least two readings: most streams, or
most playlist appearances. This graph has no streams and no listening
history; it can support "appears in the most distinct playlists in
fictional-music-v1" and nothing wider. A model asked the vague question will
pick a reading. The review step is where you check which one it picked and
whether the data supports it. Ask the class to name the two readings before
the model does.

## 6 A write, end to end

Everything in the database interactions in Section 5 left the database
as it was. This section gives a Cypher program that changes the
database, checks the change, and undoes it, and in doing so shows where the control over
writes sits.

### 6.1 One field, one restart, three tools

Exit Claude Code. Set `NEO4J_MCP_READ_ONLY` to `"false"` in `.mcp.json`.
Start again. `/mcp` now shows three tools:

![Three tools in the write configuration](../slides/images/mcp-neo4j-09-three-tools.png)

Nothing in the repository, the prompt, or the host's rules changed; the
server's configuration did, and discovery followed. (The server's log says
`Registered server tools count=4`: it registered `list-gds-procedures` too,
then omitted it at `tools/list` because the probe for Graph Data Science
failed. The host shows the three it was told about.)

### 6.2 A read that the write depends on

> Which tracks do playlists P02 and P03 have in common? Return track id and
> track name, ordered by track id.

![The shared tracks](../slides/images/mcp-neo4j-10-shared-tracks-answer.png)

One `read-cypher` call; four rows, T03 Signal 03 to T06 Signal 06. These are
the tracks the write will use. In a fresh session with no such turn, a prompt
that said "those four shared tracks" made the model infer which tracks were
meant (it chose correctly, and said it was inferring). The homework spells
the ids out.

### 6.3 The write, proposed

> Create a new playlist with id P09 named "Class Demo", owned by user U01,
> containing exactly the tracks T03, T04, T05 and T06 at positions 1 to 4.
> Use MERGE so that nothing is duplicated. Show me the Cypher and wait for
> my approval before running it.

Before drafting anything, the model ran one read on its own (model
behavior, observed in both write sessions): a statement that checks that
`U01` exists, that no `P09` exists yet, and that all four tracks are present.
The database's log has it:

```cypher
OPTIONAL MATCH (u:User {id: 'U01'})
OPTIONAL MATCH (p:Playlist {id: 'P09'})
OPTIONAL MATCH (t:Track) WHERE t.id IN ['T03','T04','T05','T06']
RETURN u.id AS user_found, p.id AS p09_exists, collect(t.id) AS tracks_found
```

Then it proposed (model output; the statement that later ran under the
permission dialog):

```cypher
MATCH (u:User {id: 'U01'})
MERGE (p:Playlist {id: 'P09'})
  SET p.name = 'Class Demo'
MERGE (u)-[:OWNS]->(p)
WITH p
UNWIND [['T03', 1], ['T04', 2], ['T05', 3], ['T06', 4]] AS row
MATCH (t:Track {id: row[0]})
MERGE (p)-[r:HAS_TRACK]->(t)
  SET r.position = row[1]
RETURN p.id AS playlist, p.name AS name, r.position AS position, t.id AS track, t.name AS trackName
ORDER BY position
```

![The proposed write](../slides/images/mcp-neo4j-11-write-proposed-cypher.png)

The earlier session's version differed in detail (`ON CREATE SET` instead of
`SET`, a list of maps instead of pairs, a collected return). Both are
correct; neither is canonical. The review for a write is in the homework's
[primer, "Writing data"](../../neo4j/02-neo4j-music-mcp/PRIMER.md): existing
nodes are matched, not merged, so a typo in an id yields zero rows rather
than a phantom node; only the new playlist and its own relationships are
merged, on an `id` that a uniqueness constraint protects; every `HAS_TRACK`
gets a `position`; nothing in the statement reaches beyond `P09`.

### 6.4 Two approvals that are not the same thing

The prompt asked the model to wait for approval, and it did, ending its
proposal by asking for the word "approved" (in another session, for "go").
What happened after that word depended on the host's permission mode, and the
pilot captured both cases.

**In auto mode**, the instructor's default, the statement ran as soon as the
model received the word. No dialog appeared, no rule was written anywhere;
the host approved the call itself.

![Auto mode: approved, run, verified, no dialog](../slides/images/mcp-neo4j-12-write-model-approval-and-run.png)

**In manual mode**, the host stopped between the model's request and the
server:

![The write dialog](../slides/images/mcp-neo4j-24-write-permission-prompt.png)

```text
Tool use
neo4j — Write Cypher Tool: (MCP)

query:
  │ MATCH (u:User {id: 'U01'})
  │ MERGE (p:Playlist {id: 'P09'})
  │   SET p.name = 'Class Demo'
  │ ...
  │ ORDER BY position

About the neo4j — Write Cypher Tool:
│ write-cypher executes any arbitrary Cypher query, with write access, against the user-configured
│ Neo4j database.

Do you want to proceed?
❯ 1. Yes
  2. Yes, and don't ask again for neo4j — Write Cypher commands in /private/var/folders/2t/vhj81c…
  3. No
```

The dialog shows the tool's title, the complete statement, the tool's own
description from `tools/list`, and three options. The first runs this call
once. The second writes a standing allow rule into
`.claude/settings.local.json`, after which every later write in this project
runs without a dialog; it is never the right choice for a write tool. The
third refuses. The records show how long the dialog was open: the transcript
has the model's request at 17:38:32 and the host's log has the call reaching
the server at 17:41:05. For two and a half minutes the statement existed only
as a request, and the person reading it could still have said no.

The two approvals differ in kind. The model's "say approved" is a courtesy
that its own wording varies ("approved" in one session, "go" in the next)
and that nothing enforces: the model could run the call without asking, and
a model asked to skip the courtesy would. The dialog is a control: it sits in
the host, between the model's request and the server, and the call does not
happen until a person answers it. Ask for both. Rely on the second.

### 6.5 Verify the write

Read it back in Desktop's Query tool, database `music`:

```cypher
MATCH (u:User)-[:OWNS]->(p:Playlist {id:'P09'})-[h:HAS_TRACK]->(t:Track)
RETURN u.id AS owner, p.name AS playlist, h.position AS position, t.id AS track, t.name AS title
ORDER BY position;
```

![The read-back in Query](../../neo4j/resources/desktop-10-p09-readback-query.png)

Four rows, owner `U01`, positions 1 to 4, tracks T03 to T06. Then the
fixture check, run from inside the session with a line that starts with `!`,
which Claude Code executes in the session's own shell:

```text
Readiness mismatch: {"expected": {"Track": 36, "Artist": 8, "Album": 6, "Playlist": 8, "User": 4, "OWNS": 8, "PLAYLIST_HAS_TRACK": 89, "ALBUM_HAS_TRACK": 36, "ARTIST": 48}, "observed": {"Track": 36, "Artist": 8, "Album": 6, "Playlist": 9, "User": 4, "OWNS": 9, "PLAYLIST_HAS_TRACK": 93, "ALBUM_HAS_TRACK": 36, "ARTIST": 48}}
```

![The check reports the change](../slides/images/mcp-neo4j-13-check-mismatch.png)

Playlist 9 where 8 were expected, OWNS 9 where 8, PLAYLIST_HAS_TRACK 93 where
89: one playlist, one ownership, four tracks. Every other count unchanged.
The mismatch is the check working. It noticed the change without being told
what the change was, and it reported exactly what moved. (In the pilot the
model, seeing the output, produced the same three-row difference table and
observed that `check` "is a 'database is pristine' test, not a correctness
test for your work". Model output, and correct.)

### 6.6 Revert

> Delete playlist P09 and only its own relationships. Do not touch any other
> node. Show the Cypher first.

```cypher
MATCH (p:Playlist {id: 'P09'})
DETACH DELETE p
RETURN count(*) AS deleted
```

![The proposed revert](../slides/images/mcp-neo4j-14-revert-proposed-cypher.png)

A second dialog in manual mode, answered once with Yes. The model verified
with reads of its own; the instructor's `check` passed with all nine counts.

![The revert ran](../slides/images/mcp-neo4j-15-revert-run-and-counts.png)

![The check passes](../slides/images/mcp-neo4j-16-check-passes.png)

The sequence create, verify, revert, check leaves the fixture as it was and
is the homework's Task 5. It is also, in miniature, the shape of any
responsible write: know what you are about to change, change it, confirm from
outside that exactly that changed, and know how to put it back.

![The path of a write, from prompt to read-back](../slides/diagrams/neo4j-write-sequence.svg)

### 6.7 Three controls, and what each does not prevent

![Three controls on the path of a write](../slides/diagrams/neo4j-write-controls.svg)

**The server's flag.** `NEO4J_MCP_READ_ONLY=true` removes `write-cypher`
from `tools/list`; the model has no write tool to call. It does not prevent
anyone with access to `.mcp.json` from setting the flag to `false` and
restarting, and it does not prevent the account from writing by any other
route. It is a property of one server process.

**The host's rules.** In manual mode the dialog stops every write for a
person to read. A standing rule in `.claude/settings.json` can go further:

```json
{"permissions": {"allow": ["mcp__neo4j__get-schema", "mcp__neo4j__read-cypher"],
                 "deny": ["mcp__neo4j__write-cypher"]}}
```

The pilot tested this file. The allow rules removed every read dialog. The
deny rule worked, but not where one might look for it: `/mcp` still listed
three tools, while the model's catalogue no longer contained the write tool.
There was no refusal message at all; the refusal was an absence. Asked for
the P09 write, the model ran its precondition read and reported (model
output): "One blocker: this session's Neo4j MCP server only exposes the
read-only tool, so I cannot execute writes here. You'll need to run the
statement in Neo4j Browser or cypher-shell, or enable write-cypher in
.mcp.json and I'll run it after your approval."

![The model's explanation under the deny rule](../slides/images/mcp-neo4j-25-deny-rule-a.png)

Two things are wrong in that sentence and both are instructive. The server
was configured for writes; the host rule, not the server, had withheld the
tool, and the model attributed the gap to the wrong layer. And the model's
proposed remedies were other routes to the same goal. When the instructor
replied "approved", it announced that it would "look at the Neo4j connection
config and run the write through a direct connection instead" and began with
a shell command to look for `cypher-shell`, the driver, and the connection
variables. That command produced a dialog of its own, which the instructor
declined. The database was not changed.

![The declined shell command](../slides/images/mcp-neo4j-25-deny-rule-b.png)

So a host rule on one tool closes one path. It does not prevent the model
from seeking another path, and in a session with shell access and the
connection variables in the environment, other paths exist.

**The database account.** The only control that holds on every route is the
privilege of the account the password belongs to. A client that logs in as
a user with the built-in `reader` role cannot write, whatever program it is
and whatever tool asked. Neo4j's Enterprise edition, which Desktop installs,
has roles and the statements to create a restricted user and grant it that
role. The pilot did not exercise this control (it was planned as an optional
step and skipped for time), so these notes do not quote its error text; the
homework does not require it. For a database that matters it is the first
thing to set up, and Section 10 returns to it.

### 6.8 What the model can read

One last observation from the write sessions. In each fresh session the
model's first actions were `ls -la` and `cat .mcp.json`, through its ordinary
file tools, before any MCP call. It read the project's configuration the way
it reads any file. The file contained `${NEO4J_MCP_PASSWORD}`, so that is
what the model saw. In one session it piped the file through `sed` to mask
any password field, a courtesy; the protection is that there was nothing to
mask. Secrets stay as references.

## 7 Three records of what ran

The conversation shows what the model says it did. Three other records show
what happened, and they are kept by three different parties.

### 7.1 The host's record

Claude Code shows each tool call in the session with its arguments; expanding
the call (as in the screenshot of Section 5.3) shows the full `query`. The
session transcript, a JSON Lines file under
`~/.claude/projects/<project-path-slug>/<session-id>.jsonl` on macOS, keeps
every `tool_use` with its arguments and a timestamp, and every result. This
is the file from which the pilot read the request time of the write in
Section 6.4. The host also keeps a per-server log,
`~/Library/Caches/claude-cli-nodejs/<project-path-slug>/mcp-logs-neo4j/<timestamp>.jsonl`,
holding the server's standard error and the host's own connection events. It
records that a call completed and how long it took
(`msg="tool call completed" tool=read-cypher success=true duration_ms=10`),
not the statement's text.

### 7.2 The server's record

The server's standard error is what the per-server log captures: startup,
requirement checks, tool registration, each `tools/list` and `tools/call`,
and errors. Useful for "did the server see a call" and "why did the server
fail to start"; it does not carry the Cypher.

### 7.3 The database's record

The Enterprise edition that Desktop installs writes a query log by default.
The instance's `conf/neo4j.conf` shows the default as a comment,
`#db.logs.query.enabled=VERBOSE`, and the file is `logs/query.log` in the
instance's folder. On macOS the instance folders live under
`~/Library/Application Support/neo4j-desktop/Application/Data/dbmss/dbms-<id>/`.
From any client, the statement

```cypher
SHOW SETTINGS YIELD name, value WHERE name IN ['server.directories.logs', 'db.logs.query.enabled'] RETURN name, value;
```

returns the logs directory and the setting. This log is the database's own
account of every statement it executed, by every client, and it is the one
record of the three that no party on the model's side of the boundary can
influence.

In VERBOSE mode each statement produces two entries, one when it starts and
one when it completes, and a statement with several lines occupies several
lines of the log. The completion entry of the write from Section 6.3, as
recorded (the statement's middle lines elided):

```text
2026-11-18 23:41:05.269+0000 INFO  id:327 - transaction id:197 - 79 ms: (planning: 75, waiting: 0) - 12816 B - 35 page hits, 0 page faults - bolt-session	bolt	Go Driver/6.4.0		client/127.0.0.1:59409	server/127.0.0.1:7687>	music - neo4j - MATCH (u:User {id: 'U01'})
MERGE (p:Playlist {id: 'P09'})
  SET p.name = 'Class Demo'
...
ORDER BY position - {} - runtime=pipelined - {app: 'MCP4NEO4J/2.1.1'}
```

The fields that matter for our purposes: the time, the transaction id, the
database (`music`), the user (`neo4j`), the statement, its parameters (`{}`
here), and the client metadata, in which the MCP server identifies itself as
`MCP4NEO4J/2.1.1`. Desktop's Query tool appears in the same log as
`neo4j-javascript/6.0.1` with `app: 'nx'`. Three patterns in the pilot's log
confirm things said earlier in these notes:

- Every `read-cypher` statement is preceded by an `EXPLAIN` of the same text
  in its own transaction: the server's read-only check of Section 1.4.
  Writes have no `EXPLAIN` before them.
- Each statement has its own transaction id. The write of Section 6.3 is one
  transaction; the delete of Section 6.6 is another. There is no transaction
  spanning several calls.
- The `get-schema` tool is the statement
  `CALL apoc.meta.schema({sample: $sampleSize}) YIELD value ...` with the
  parameter `{sampleSize: 100}`: the server's schema sample size, visible as
  a logged parameter.
- A failed statement is an `ERROR` entry with the message appended; the
  server's startup probe appears as
  `RETURN gds.version() as gdsVersion ... Unknown function 'gds.version'`.

Parameters are logged by default. For a database that holds sensitive values
passed as parameters, the setting `db.logs.query.parameter_logging_enabled=false`
turns that part off; the music fixture has nothing sensitive.

### 7.4 A standard way to read it

The homework package ships
[`query_log.py`](../../neo4j/02-neo4j-music-mcp/query_log.py), a script that
reads a `query.log`, reassembles multi-line statements, and prints one block
per completed statement with the local time, the outcome, the database, the
user, the client application, the elapsed time, the transaction id, and the
statement. By default it shows only the MCP server's statements and hides the
server's `EXPLAIN` pre-checks. On a Mac with one Desktop instance it finds
the log itself:

```sh
uv run --frozen python query_log.py --last 10
uv run --frozen python query_log.py --since 2026-11-18T17:30 --explain
uv run --frozen python query_log.py --all --last 20        # every client, including Query
uv run --frozen python query_log.py --log /path/to/logs/query.log
```

Output from the instructor's log after the pilot (abridged):

```text
2026-11-18 17:58:42 -0600  success  music  neo4j  MCP4NEO4J/2.1.1  9 ms  tx 223
    CALL apoc.meta.schema({sample: $sampleSize})
            YIELD value
            ...
    params: {sampleSize: 100}

2026-11-18 17:58:47 -0600  success  music  neo4j  MCP4NEO4J/2.1.1  3 ms  tx 225
    MATCH (p2:Playlist {id: 'P02'})-[:HAS_TRACK]->(t:Track)<-[:HAS_TRACK]-(p3:Playlist {id: 'P03'})
    RETURN DISTINCT t.id AS track_id, t.name AS track_name
    ORDER BY t.id

2026-11-18 18:18:52 -0600  fail     <none>  neo4j  MCP4NEO4J/2.1.1  10 ms  tx -1
    RETURN gds.version() as gdsVersion
    error: Unknown function 'gds.version' (line 1, column 8 (offset: 7))
```

Nothing in the script talks to the database or to the model. It reads a file
the database wrote.

### 7.5 A prompt recipe: the model's account against the database's

At the end of a session, before exiting, ask:

> List every Cypher statement you executed in this session through the neo4j
> server, in order, with the tool you used for each and one sentence on what
> it returned or changed. Do not run anything new.

Then run `query_log.py --since <the session's start time>` and compare. The
two lists should agree on the statements and their order. Differences are
findings, not failures of the exercise: a precondition read the model ran
and did not mention, a statement it described more loosely than it was
written, a call that failed and was retried. In the pilot the model's account
was accurate; the point is that you can check it, and that the check costs
one command.

For explanations, paste the script's output back and ask:

> For each statement below, explain in two or three sentences what it
> matches, what it returns or changes, and which clause, if any, could modify
> data. Do not run anything.

The result is model output, to be read against the primer like any other
explanation. For the database's own view of a statement, the Query tool's
`EXPLAIN` prefix produces the execution plan without executing the statement,
for writes as well as reads; the plan names the operators, so a `Merge` or
`DetachDelete` operator shows what the statement would do. (Neo4j documents
`EXPLAIN` as never executing; the pilot observed only the server's own
`EXPLAIN` calls, not a student's use of it.)

## 8 Diagnosis by layer

The guide's troubleshooting table, extended with the evidence sources of
Section 7. Every quoted text was observed in the pilot except where a date
says otherwise.

| What you see | Layer | Next check |
|---|---|---|
| `/mcp` opens with `MCP config diagnostics` and `Missing environment variables: NEO4J_MCP_PASSWORD`; `✘ neo4j` | Host configuration: shell variable unset | Exit; set the variables in the terminal; start Claude Code from it. |
| Server `✘ failed` right after start although the variable is set; per-server log says `Neo.ClientError.Security.Unauthorized` | Database credentials | Wrong password. The instance's `logs/security.log` says `failed to log in: invalid principal or credentials`. Retype it. |
| `Failed to reconnect to neo4j: 0`; per-server log says `dial tcp 127.0.0.1:7687: connect: connection refused` | Database not reachable | The instance is stopped, or another instance holds the port. Start it in Desktop; reconnect from `/mcp`. |
| Server fails and its log mentions APOC (observed 2026-11-16 on a command-line instance, not with Desktop's installer) | Instance plugin | Install APOC from the Plugins tab; restart the instance. |
| `get-schema` returns `isError: true` mentioning a sandboxed procedure (2026-11-16, same rehearsal; did not recur with Desktop's installer) | Instance configuration | `dbms.security.procedures.unrestricted=apoc.*` in the instance's `conf/neo4j.conf`; Desktop wrote it in the pilot. |
| A statement returns nothing in Query although the model's call returned rows | Query tool | The Database selector is on `neo4j`. Select `music`. |
| `/mcp` shows 2 tools when you expected 3 | Server configuration | `NEO4J_MCP_READ_ONLY` is `"true"`. Change it and restart Claude Code. |
| The model says it has no write tool although `/mcp` shows three | Host rule | A `permissions.deny` entry in a `settings.json` withholds the tool from the model. Read the project's `.claude/settings.json` and your user settings. |
| The server is connected but the answer cites no call | Model selection | Name the server in the prompt. Check the transcript and `query_log.py`: if the database's log has no statement, nothing ran. |
| Rows are right, the prose is wrong | Model | Not a setup failure. Keep the rows, correct the explanation, record both. |
| An `ERROR` line about `gds.version` in the server's log or the query log | Nothing | The probe for Graph Data Science. Expected on an instance without it. |

Three places to look, in order: `/mcp` for which server failed; the host's
per-server log for the server's own words about why; the instance's `logs/`
folder, `security.log` for logins and `query.log` for statements, for what
the database saw.

## 9 A recipe for a database of your own

Everything in this lecture transfers to any Neo4j database with no change
except one field. Stated as a procedure with the reason for each step and the
failure it prevents:

1. **One instance, one database per activity.** `CREATE DATABASE <name> IF
   NOT EXISTS`. Damage from a wrong write is confined to that database; the
   server can reach only the database it was given.
2. **Activate the APOC plugin once per instance.** 
   The server will not start without it, and
   `get-schema` is a call to it.
3. **The password in the shell, never in a file.** `.mcp.json` carries
   `${NEO4J_MCP_PASSWORD}`; the model reads project files.
4. **One stdio entry.** Copy the Section 1 entry; set `NEO4J_MCP_DATABASE`.
   Between reading and writing only `NEO4J_MCP_READ_ONLY` changes.
5. **Manual mode, allow the reads, prompt the writes.**
   `claude --permission-mode manual` and the Section 3.4 settings file. Read
   the mode line.
6. **Use `/mcp` before the first prompt to check the status of the
   connection to the MCP server.** Connected, the expected tool count,
   the expected names. A failed server here costs a minute; discovered after
   ten prompts it costs the prompts.
7. **Schema first, every session.** The model writes against the labels it
   has seen.
8. **Propose, review, run.** Labels and directions against the schema;
   distinct counts against path counts; the anchor label; ties; bounds; no
   write clause in a read; for a write, the checklist of the primer.
9. **Verify outside the conversation.** Replay in Query with the right
   database selected; a check that knows what the data should be; the query
   log.
10. **Loading data: constraints first, then `MERGE`.** A uniqueness
    constraint per label on the identifying property, then `MERGE` on that
    property, so that a repeated load repeats nothing and a partial load can
    be completed by running again. Count what you loaded against the source.

**A described exercise.** Create an empty database `demo`, point a second
entry at it in your `.mcp.json` file, and give the model a description of a small world: a reading
group of five members who have read some of three books and met at two
meetings, each meeting discussing one book and attended by some members.
Ask for the schema the model would use, then for the constraints, then for
`MERGE` statements that load it, each shown before it runs. Then ask for the
two counting statements that every database can answer:

```cypher
MATCH (n) UNWIND labels(n) AS label RETURN label, count(*) AS nodes ORDER BY label;
MATCH ()-[r]->() RETURN type(r) AS relationship, count(*) AS count ORDER BY relationship;
```

and compare the counts with your description. The pilot did not run this
exercise, so these notes claim nothing about what a model will produce for
it; its purpose is to apply steps 7 to 10 on data that is not the fixture.

In a **follow-on flight database homework** you need to be able to
carry out the actions above without a script.  You will also be
working with real data:
the OpenFlights airports, airlines, and routes, which you model, load through
`write-cypher` behind the dialog, and query for a travel question. Its brief
is released separately.

## 10 Containment and recovery on a database that matters

In this lecture, we use what is called a *fixture* to check starting
state of the database against documented expected results.
The fixture is small and has a loader; if anything goes wrong, the whole
database can be rebuilt in seconds.  With a realistic database
project, you won't be able to do this type of check.
In this section, we give some advice about what you can do about
possible mistakes that the model makes when manipulating your data via
MCP.  In particular, there are some things that you probably want to 
set up before the first write session on a database you cannot afford to
lose.

### 10.1 What the tool gives you, and what it does not

Each `write-cypher` call sends one statement, and the database executes it
in one transaction. The query log shows this: one transaction id per
statement, a new id for the next. A statement is atomic: if it fails part
way, none of it is committed. Once the call returns a result, the
transaction has committed, and the tool has no operation to roll it back.
Neo4j has no undo. Recovery after a committed mistake means doing one of two
things: (1) running a Cypher query that acts as an inverse (undo) 
statement that you can write because you know exactly
what changed, or (2) making a copy of the database from before the change.

### 10.2 Before the session: contain

- **One database per activity**, and the server pointed at exactly one. A
  mistake cannot reach the others.
- **Read-only configuration by default.** Keep `NEO4J_MCP_READ_ONLY` at
  `"true"` in the committed `.mcp.json`. Flip it for the session that needs
  writes and flip it back; the diff is one line and shows up in version
  control.
- **A standing deny rule** for `mcp__neo4j__write-cypher` in sessions that
  must not write, and the dialog in manual mode for sessions that may.
  Section 6.7 says what each does not prevent.
- **A restricted database account** for exploration sessions. A user with the
  `reader` role cannot write whatever route a program takes; use the
  administrator account only in the session that loads or changes data.
  Documented by Neo4j for the Enterprise edition; not exercised in the pilot.
- **A snapshot of the counts.** Run the two statements of Section 9 before
  the session and save the output. After the session, run them again. For
  the fixture this is what `database.py check` does with the manifest; for
  any database the two statements do it against the saved file.

### 10.3 Before the session: a copy

The Neo4j documentation gives two routes to a file copy of a database, and
the pilot exercised neither; they are stated here from the documentation and
from the help text of the tools on the instructor's instance, and they are
for the instructor to rehearse before they are relied on in a project.

**Through Desktop.** With the instance stopped, the instance card's menu
offers an export of selected databases to `.dump` files, which Desktop
writes to the instance's dumps folder and which its menu can open. The same
menu loads a `.dump` file as a *new* database named after the file; the
Desktop manual says the load does not overwrite an existing database of the
same name. So a dump taken before a session can be loaded under another name
for comparison, or loaded in place of the original after the original has
been dropped. The menu labels observed on Desktop 2.3.0 are "Export
databases" and "Load database from file".

**Through the command line.** The instance folder's `bin/neo4j-admin`
(version 2026.10.0 on the instructor's machine) has `database dump
<database> --to-path=<dir>` and `database load <database> --from-path=<dir>
--overwrite-destination=true`. The documentation says the database must not
be mounted in a running server when it is dumped or loaded; on Enterprise,
`STOP DATABASE <name>` against the `system` database takes one database
offline while the instance keeps running, and `START DATABASE <name>` brings
it back. The tool needs Java 21 or newer; Desktop ships a runtime it uses for
the instance (on the instructor's Mac under
`~/Library/Application Support/neo4j-desktop/Application/Cache/runtime/`),
and `JAVA_HOME` must point at it for the command to run from a terminal.

Either route gives you a file that `load` can turn back into the database as
it was. For a database of any size, take the copy before the first write
session and after each session you want to keep.

### 10.4 During the session: dry runs

- **Read before write.** Ask for the read that shows what the write would
  touch, run it through `read-cypher`, and look at the ids and counts. The
  model did this unprompted in the pilot (Section 6.3); make it a standing
  request.
- **Anchor on ids.** A write that begins `MATCH (p:Playlist {id: 'P09'})`
  can touch one node. One that begins `MATCH (p:Playlist)` can touch them
  all. Read the first line of every write for its anchor.
- **Return what you changed.** Ask every write to `RETURN` the ids or counts
  of what it created, set, or deleted, as the pilot's statements did. The
  result is the first evidence; the read-back is the second.
- **`EXPLAIN` in Query** shows a write's plan without running it. A reviewer
  who is unsure what a statement will do can see its operators first.
- **Inverse first.** For a change that must be reversible, ask for the
  inverse statement at the same time as the change, and read both before
  approving the first. The P09 cycle is this pattern.

### 10.5 After an unexpected change

1. **Stop writing.** Exit the session, set `NEO4J_MCP_READ_ONLY` to
   `"true"`, or add the deny rule. Nothing else should change while you
   look.
2. **Establish what ran.** `query_log.py --since <time>` lists every
   statement the server sent, in order, with its transaction id and outcome.
   This is the database's record, not the model's recollection.
3. **Measure the change.** The two counting statements against the saved
   snapshot; targeted reads for the ids the statements named.
4. **Decide.** If the change is small and fully known, write the inverse
   statement, review it with the same care, and run it under the dialog; then
   measure again. If it is not fully known, restore the copy from Section
   10.3 and reload anything legitimate that happened after it.
5. **Record it.** The statement, the time, the measurement, and the repair
   belong in the project's evidence, as the homework's mismatch and passing
   check do.

## 11 The homework and what comes next

The [homework](../../neo4j/02-neo4j-music-mcp/README.md) reproduces this
lecture on a provided fictional music database in about an hour. Its six tasks: make the
instance ready (guide, sections 1 to 3); load and check the fixture
(SETUP.md); connect Claude Code and record the tool list, with the schema
prompt of Section 5.1; Question A with the three prompts of Section 5 and the
replay in Query; the write cycle of Section 6 with a playlist and tracks of
your own choosing, the dialog recorded, the check's mismatch and its pass;
and a reflection on what you changed or rejected and what you could only know
from outside the conversation. Tasks 1 to 3 are a checkpoint due two days
after release, so that Desktop and APOC trouble surfaces early. The
submission is two files, a sanitized `.mcp.json` and an `evidence.md`.
Question B, the ambiguity question, and a diagnosis are optional extensions.

The exit question for the lecture: name one field of the stdio entry and say
which process reads it, and name one observation that proves a write
happened that did not come from the model.

The [dice lecture](lecture-mcp-dice.md) is next. It takes an ordinary Python
function and makes it a server that a host can discover and call, and it
tests the result at the boundaries this lecture and the adoption lecture
observed from the outside.

## 12 Explained self-checks and vocabulary

**Does a connected server show that a query ran?** No. `/mcp` shows the
host's connection to the server. A statement ran if the host shows the call,
the server's log shows `tool call completed`, and the database's query log
has the statement with `MCP4NEO4J` as the client. Any one of the three is
evidence; the third is the database's own.

**Which process executed the Cypher?** The database. The model composed it,
the host routed it and, in manual mode, asked you first, the server sent it.
The query log records the execution with the server as the client.

**Why did `/mcp` list three tools while the model had two?** A
`permissions.deny` rule withholds a tool from the model's catalogue but does
not change what the server offers or what `/mcp` displays. Two views, two
layers.

**What does `${NEO4J_MCP_PASSWORD}` look like to the model?** Exactly that
string. The host expands it only in the environment it gives the server
process. The model reading `.mcp.json` sees the reference.

**Why did the write dialog not appear in the auto-mode session?** In auto
mode the host approves tool calls itself. The model's "say approved" is not a
host control; the dialog is, and only a prompting mode shows it. Read the
mode line.

**Which control would have held if the model had taken another route to the
database?** The database account's privileges. The server flag governs one
server; the host rule governs one tool in one host; the account governs every
client that logs in with it.

**Where is the record of a statement the model says it ran?** In three
places: the session transcript (the host's record of the call), the
per-server log (the server saw a call and completed it), and the instance's
`query.log` (the database executed this text in this transaction).
`query_log.py` reads the third.

**A write went wrong on a database that matters. First three steps?** Stop
writing (read-only flag or deny rule). List what ran from the query log.
Measure against the count snapshot. Then decide between an inverse statement
and a restore from the copy taken before the session.

| Term | Meaning in these notes |
|---|---|
| Instance | One running Neo4j server, managed by Desktop, with one address |
| Database | A named graph inside an instance; `system`, `neo4j`, `chapter01`, `music` |
| `neo4j://` URI | The address a driver connects to; what the instance card shows; Bolt is the protocol underneath |
| APOC | A plugin of the instance; the server requires it and `get-schema` calls it |
| stdio child | A program the host starts and talks to over its standard streams; ends with the session |
| `env` | The environment the host gives that program; here, the server's configuration |
| Read-only mode | `NEO4J_MCP_READ_ONLY=true`; the server omits `write-cypher` from discovery |
| Permission mode | Claude Code's policy for tool calls: auto approves, manual asks; shown under the input box |
| Allow and deny rule | Standing host rules in `.claude/settings.json`, by model-visible tool name |
| Constraint | A uniqueness rule on a label's property; what makes `MERGE` on an id safe |
| `MERGE` | Match the pattern, or create it if absent |
| `DETACH DELETE` | Delete a node with its relationships |
| Transaction | The unit in which the database executes a statement; one per `write-cypher` call |
| Query log | The instance's `logs/query.log`: every statement, its client, its outcome |
| Per-server log | Claude Code's record of one server's standard error and connection events |
| Dump | A single-file copy of a database that `load` can turn back into a database |

References: the [Neo4j MCP server](https://github.com/neo4j/mcp) and its
[documentation](https://neo4j.com/docs/mcp/current/); Claude Code's
[MCP](https://code.claude.com/docs/en/mcp) and
[permissions](https://code.claude.com/docs/en/permissions) documentation;
the Neo4j operations manual on
[query logging](https://neo4j.com/docs/operations-manual/current/monitoring/logging/),
[dumping](https://neo4j.com/docs/operations-manual/current/backup-restore/offline-backup/)
and [loading](https://neo4j.com/docs/operations-manual/current/backup-restore/restore-dump/)
a database, and
[starting and stopping databases](https://neo4j.com/docs/operations-manual/current/database-administration/standard-databases/start-stop-databases/);
the [Neo4j Desktop manual on database management](https://neo4j.com/docs/desktop/current/operations/database-management/);
the [Cypher manual](https://neo4j.com/docs/cypher-manual/current/) and
[APOC](https://neo4j.com/docs/apoc/current/). The pilot record,
[`reports/desktop-pilot.md`](../demos/lecture-mcp-neo4j/reports/desktop-pilot.md),
is the source of every observation in these notes, and
[`reports/live-desktop.json`](../demos/lecture-mcp-neo4j/reports/live-desktop.json)
of every JSON excerpt.
