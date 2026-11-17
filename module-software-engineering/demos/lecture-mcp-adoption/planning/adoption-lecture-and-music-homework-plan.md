# Plan for an MCP adoption lecture and Neo4j music homework

> Authoring record. Written 2026-11-16 in the planning repository (`mcp-lecture/planning/`) and
> migrated here on 2026-11-17 with its links repointed. Paths quoted in the text refer to the
> planning layout: `demos/adoption/` is now `module-software-engineering/demos/lecture-mcp-adoption/`,
> `homework/neo4j-music/` is `neo4j/02-neo4j-music-mcp/`, and `instructor-materials/neo4j-music/` is
> `demos/lecture-mcp-adoption/neo4j-music-instructor-key/`. The fictional-fixture option was selected.

Prepare a 75-minute lecture on connecting to and using existing MCP servers,
followed by a homework on querying a prepared Neo4j music database through
Claude Code. Place this lecture before the existing dice implementation lecture.
Students first configure, discover, use, and verify a provider's tools, then learn
how to implement that provider interface themselves.

Use Microsoft Learn's remote documentation server for the main lecture example.
It avoids database installation during students' first encounter with MCP. Use a
prepared music database for a short instructor preview and the subsequent
homework. Keep database loading separate from agent querying so that the
homework assesses integration and evidence, rather than database construction.

The student notes must provide a gentle, self-contained explanation with worked
examples and troubleshooting. There is **no length limit on student notes**.
The 75-minute classroom limit governs presentation choices, not the depth of
the written material. Expand the dice notes to the same standard as part of
reconciling the two lectures.

Implementation status is recorded in the [current verification report](../reports/adoption-and-music-verification.md). The fictional-fixture option below was selected.

This is the implementation plan, dated 2026-11-16. It specifies proposed teaching
artifacts and acceptance criteria; it does not mark the new lecture or homework
as implemented. Continue authoring in this planning repository. Public curation,
lecture numbering, and course placement remain later work.

## 1 Teaching sequence and scope

| Element | Student role | Main question | Evidence |
|---|---|---|---|
| Adoption lecture | Consumer of an existing integration | How do I connect my repository's agent to this capability? | Configuration, discovery, actual call, grounded answer |
| Music homework | Consumer who checks a database answer | Does the generated query mean what I asked, and do the results support the answer? | Schema, Cypher, rows, independent comparison |
| Dice lecture | Provider of a small integration | How do I expose and test an accurate tool contract? | Function, schemas, protocol calls, host rehearsal |

Students need the basic agent loop and the toy-agent exercise. They need not
know Neo4j to attend the adoption lecture. Supply a graph/Cypher primer and a
setup checkpoint for the homework; do not silently require completion of the
book chapter. Students who already completed the existing Cypher activities
can use the primer as review.

Launch the homework at the end of the adoption lecture. Allow approximately one
week, with a setup checkpoint early in that interval. The dice lecture can take
place while the homework is underway; successful database installation is not
a prerequisite for learning the dice implementation.

Do not add graph modeling, music recommendations, user similarity algorithms,
a second agent host, or a survey of many servers to the required work. A single
well-explained integration and its evidence are more useful here than numerous
installation recipes.

## 2 Existing material and implications

Use these sources without modifying them as part of the initial implementation:

- Neo4j introduction (planning repository, `Neo4j/ReadMe.md`) and
  [Cypher preparation](../../../../neo4j/01-intro-to-neo4j-cypher/ReadMe.md).
- Connecting Claude to the music database (planning repository, `Neo4j/02-connect-claude-to-neo4j/ReadMe.md`).
- Existing music loader (planning repository, `Neo4j/02-connect-claude-to-neo4j/ingest-and-setup-database.cypher`).
- [Small music data](../../../../neo4j/01-intro-to-neo4j-cypher/import/) and
  [medium music data](../../../../neo4j/01-intro-to-neo4j-cypher/import/medium/).
- Airline mini-project (planning repository, `Neo4j/03-use-neo4j-on-new-data/ReadMe.md`), which
  is a separate activity and should not be imported into this homework.
- [Dice instructor outline](../../../lectures-instructor-notes/lecture-mcp-dice.md),
  [notes](../../../lecture-notes/lecture-mcp-dice.md), and
  [verification](../../lecture-mcp-dice/reports/verification.md).

Inspection of the local CSVs establishes the following planning facts. Counts
are parsed data records, excluding headers; they are not database node counts.

| Data | Track records | Playlist records | Distinct track IDs | Distinct playlists |
|---|---:|---:|---:|---:|
| Small | 97 | 97 | 76 | 40 |
| Medium | 93,923 | 93,924 | 69,878 | 200 |

The small files contain 89 distinct artist IDs and 40 users. All playlist track
IDs have metadata in the small track file. There are 20 duplicate
playlist/track/position tuples, only one track shared between distinct playlists,
and only one or two distinct represented tracks per playlist. These files are
small enough to explain but too sparse for a rich playlist-overlap exercise
without checking the chosen examples carefully. Do not interpret the original
`total_tracks` field as the count represented in this sample.

The existing loader reads the medium files, creates node-key and relationship
type constraints, and derives similarity relationships. Prepare a simpler
loader for the new fixture: confirm compatibility with the selected database
edition, use suitable ID uniqueness constraints, and omit similarity construction.
The existing music connection guide also names older Neo4j Labs packages. Select
and rehearse one current official server rather than combining old package
names, new environment variables, and untested launch commands.

The OpenFlights attribution file belongs to the airline data. Establish the
music dataset's own provenance and redistribution terms before bundling an
excerpt; do not apply the airline terms to music data.

## 3 Lecture outcomes

After the adoption lecture, students should be able to:

1. Explain why server configuration is different from a tool definition or a
   prompt asking the model to use a tool.
2. Create a project-scoped server declaration and explain each field.
3. Distinguish a remote endpoint from a local server process, and distinguish
   both from the host's model API connection.
4. Inspect connection status and discovered tool contracts.
5. Trace a documentation search/retrieval through the host, server, and model.
6. Check that a final answer follows from actual tool results and sources.
7. Diagnose whether a failure concerns configuration, connection, discovery,
   selection, execution, or answer grounding.
8. Identify what is shared with the repository and what each student must
   supply locally, including credentials where an integration needs them.

The in-class artifact is a small evidence record, not a substantial graded
assignment. Homework adds database semantics and independent verification.

## 4 Primary lecture example and configuration

The Microsoft Learn server uses Streamable HTTP at
`https://learn.microsoft.com/api/mcp`; Microsoft documents access without
server authentication. Its documentation lists search, article-fetch, and
code-sample tools. Discover the actual tools and schemas during rehearsal;
remote deployments can change. Sources:
[overview](https://learn.microsoft.com/en-us/training/support/mcp) and
[developer reference](https://learn.microsoft.com/en-us/training/support/mcp-developer-reference).

Students still need a working Claude Code account or institution-provided host
access. No Microsoft account, database, PowerShell installation, or Azure
subscription is required for the proposed documentation task. Network access
and the host's normal model usage are still needed. Do not equate an endpoint
with no authentication with an agent interaction that has no model cost.

Use an isolated teaching repository containing an initially empty or minimal
configuration. The intended Claude Code project configuration is:

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

Explain the braces and nesting before adding more entries: `mcpServers` is the
host's configuration map; `microsoft-learn` is our chosen connection name;
`type` identifies how to connect; `url` identifies the provider endpoint.
The connection name is not necessarily the name of any discovered tool.

This belongs in `.mcp.json` at the repository root for Claude Code project
scope. The file is a host configuration convention, not a universal MCP file
format that all products must interpret identically. Compare project, local,
and user scope. In particular, Claude Code's local scope is stored in a home
configuration file even though its effect is limited to a project. Use the
project-scoped file to make the lecture's repository artifact visible. Follow
current workspace trust and server approval behavior rather than disabling it.
[Claude Code configuration reference](https://code.claude.com/docs/en/mcp).

Explain that cloning the configuration does not install the agent host, provide
an account, authenticate private integrations, or guarantee provider uptime.
A public documentation endpoint needs no credential fields; the later database
example makes environment-based configuration concrete.

Do not activate this configuration in the planning repository merely to author
its teaching example. Store it as an example for students to copy into their
scratch repository during the eventual implementation.

## 5 Lecture demonstration progression

### Finished behavior

Opening prompt:

> Use the Microsoft Learn MCP tools to find the official documentation for
> PowerShell Get-ChildItem. Explain how to limit recursive directory listing
> depth. Cite the relevant page. Do not execute shell commands.

The subject is directory listing, which is accessible without prior PowerShell
knowledge and connects to the toy agent's file tools. Supply a short directory
tree in the notes so the documentation question has a concrete purpose.

Expand actual calls, arguments, returned material, and final answer. Inspect
whether the cited passage supports the answer. Do not promise a fixed call
count or require both search and fetch if the actual search result already
supports the requested answer. For the explicit retrieval walkthrough, issue
a follow-up asking the host to fetch and inspect the relevant article.

### Reproduce the integration

Move to the unconfigured scratch repository. Show its files, add `.mcp.json`,
explain every field, and demonstrate the host's documented reload or restart
procedure. Inspect `/mcp`, connection status, and available tool definitions.
Show the difference between configured and connected before repeating the task.

If preinstalled integrations already answer the same question, use a prepared
session configuration to isolate the teaching server. Keep the visible
project-scoped configuration demonstration, and explain any isolation flags
used during instructor rehearsal. Evidence must identify the actual provider
rather than infer it from a correct answer.

### Trace discovery and the call

Use the host's tool view and an LLM-free Inspector/client capture to distinguish:
configuration fields; discovered name/description/schema; model-selected
arguments; provider result; final explanation. Label captured JSON separately
from shortened teaching examples. Verify negotiation against this remote peer;
the dice server's modern discovery trace is not automatically its trace.

Bridge to the toy agent explicitly: hand-maintained tool schema becomes
discovery plus model adaptation; the dispatch dictionary becomes server routing;
results still have to enter model context; host execution limits remain relevant.
Keep resources and prompts as orientation, with fuller notes, rather than
inventing a use for every protocol feature.

### Student attempt

Give students a different bounded documentation question about the same command,
such as locating an example that includes hidden files. Ask for the appropriate
documentation and explanation, without command execution. Have them record the
server/tool identity, one invocation, relevant result excerpt, citation, and a
sentence explaining why the answer is supported.

### Diagnose one failure

In a disposable copy, change the path to a deliberately invalid endpoint.
Observe the error, identify which layer failed, restore the value, and reconnect.
Do not corrupt a student's working configuration or make changes to user scope.
Keep an additional captured example of a connected server whose tools were not
used; discuss how a correct-looking answer can still lack integration evidence.

### Preview the music homework

Use the instructor's already prepared database. Ask for schema inspection and
one small read query. Show a diagram of the model and a few returned rows.
Explain that the local MCP process and the database are separate processes.
Stop after establishing how the adoption workflow transfers to a database.
If the database is unavailable, use a labeled recording and actual saved results.

## 6 Classroom timing and fallbacks

| Minutes | Activity | Instructor preparation | Student observation |
|---|---|---|---|
| 0–8 | Finished documentation task | Rehearsed prompt and captured fallback | Call evidence precedes claims about the answer |
| 8–20 | Repository configuration | Clean scratch repo and config example | Connection name, type, URL, scope |
| 20–33 | Discovery and search/retrieval | Tool schema and actual trace | Configuration is different from tool metadata |
| 33–45 | Short student attempt | Bounded prompt and evidence template | One independently checked interaction |
| 45–55 | Diagnose a failure | Disposable broken URL example | Identify the failing layer before changing things |
| 55–63 | Remote HTTP and local stdio | Architecture diagrams and sample process config | Local process, remote service, and model API differ |
| 63–70 | Music preview and homework | Loaded fixture, one read call, fallback recording | Same integration pattern with database semantics |
| 70–75 | Questions and slack | Exit question | Explain one field and one item of grounding evidence |

Before class, test reachability, account access, and configuration loading on
the teaching machine. Capture tool definitions and successful results. Have a
copy of the relevant source article and screenshots of tool invocation ready.
A documentation-server outage should switch to the saved evidence, with the
student live attempt deferred or completed in pairs; it must not consume the
rest of the class. A recording is evidence analysis, not a student live pass.

If time runs short, shorten the alternate question and detailed protocol
inspection. Keep configuration, one real tool call, result checking, and the
homework explanation. Move transport internals and additional failures to the
notes. Never use lecture time for database installation.

## 7 Student notes depth and organization

Write a substantial tutorial, not a transcript of slide bullets. Introduce each
term in ordinary language, show a complete example, explain what the example
means, then provide a variation or failure case. Use progressive disclosure:
a clear main narrative followed by optional deeper sections. Optional material
may be longer than the material presented in class.

Every setup procedure needs a starting directory, prerequisites, complete file
contents or a precise edit, commands, expected observations, a verification step,
and a recovery path. Separate portable student instructions from instructor
machine paths. Define JSON, schema, process, endpoint, transport, and environment
variable when they first matter; do not assume those words explain themselves.

The planned notes should contain these sections:

| Section | Explanation and examples to supply |
|---|---|
| 1 A task the agent cannot complete from memory alone | Documentation may change; inspect a tool-backed answer and its source. A confident answer is not proof of retrieval. |
| 2 The agent loop revisited | Reconstruct the toy agent's schema, dispatch, and result message in small annotated examples. |
| 3 What MCP standardizes | Define host/client/server, contrast with model API and ordinary HTTP API, and compare fairly with CLI integration. |
| 4 Connecting a repository | Walk through the complete config above line by line; include a file tree, scopes, loading, approvals, and clone-to-another-machine implications. |
| 5 Watching discovery | Annotate a real listing and explain name, description, input schema, defaults, required fields, and provider changes. |
| 6 Following one documentation task | Present exact prompt, actual call arguments, result excerpts, article passage, final answer, and verification reasoning. |
| 7 Search and retrieval | Explain why snippets can be enough sometimes and why opening the source is sometimes necessary; include an unsupported-answer counterexample. |
| 8 Reading the information exchanged | Annotate configuration, tool definition, call request, tool result, and model message as different objects; show request/result association without protocol overload. |
| 9 Local and remote connections | Explain stdio pipes vs HTTP, server startup, package runners, model inference location, and the Neo4j three-process arrangement. |
| 10 A systematic troubleshooting walkthrough | Worked cases for invalid JSON, bad URL, missing local command, missing environment variable, stopped database, tools not selected, and wrong final answer. |
| 11 Permissions and shared configuration | Explain server access vs host approval vs downstream authorization, credential references, and why repository configuration should be reviewed. |
| 12 Costs and context | Distinguish local work, downstream services, model turns, and context; demonstrate host-dependent deferred discovery without invented token counts. |
| 13 Music database bridge | Introduce nodes, relationships, IDs, a small graph, one Cypher query, distinct counts, and a source-to-answer evidence chain. |
| 14 Reusable adoption recipe | Task, provider, transport, configuration, discovery, bounded call, verification, troubleshooting, and removal/disable procedure. |
| 15 Practice and reference | Self-checks with explained answers, glossary, full configuration examples, evidence template, primary references, and optional deeper protocol material. |

The notes should explain what students can infer from an observation. For
example, a sample passage could read:

> Putting a server in `.mcp.json` tells Claude Code where it can obtain a set of
> capabilities. It does not itself tell the model every available tool, and it
> does not request that any tool run. The host first has to interpret the
> configuration and communicate with the server. The server then describes
> the tools it offers. When the host makes an appropriate tool available to the
> model, the model can request an invocation. The host routes that request and
> returns its result to the conversation.

A second passage should unpack the common status confusion:

> A server can be connected even when the answer did not use it. Connection
> status tells us that communication with the provider is working. To establish
> use, inspect the actual tool invocation. Then check a separate question:
> does the final answer follow from what the tool returned? These checks solve
> different problems. A successful connection does not establish correct tool
> selection, and a successful tool call does not establish a correct explanation.

Include a tiny, explicitly constructed music example to make duplication visible:
playlist P1 contains tracks T1 and T2; both tracks credit artist A; P2 also
contains T1. Artist A appears in two distinct playlists, although three
playlist-to-track paths reach A. Add one repeated CSV record and explain why
it must not inflate either answer. Label this as a teaching example, separate
from the eventual measured fixture.

Use diagrams alongside prose and include text explanations that remain useful
without the diagrams. Add guided questions such as “Which component executes the
query?” and “What would still work if the model service were unavailable?”
Provide explanations with the answers, not just correct letters or terms.

The notes are complete when a student who missed class can reproduce the
integration, interpret its evidence, diagnose common failures, and understand
the music homework without guessing omitted steps. Do not impose a word target
or condense prose merely to match slide count.

## 8 Homework outcomes and workload

Working title: **Using MCP to explore and verify a music database**.

Students should configure a database integration, discover its schema, translate
precise questions into reviewed read queries with agent assistance, and check
answers independently. They should explain at least one distinction between
natural-language intent and database semantics.

Budget approximately 2–3 hours after host access is working, including an
estimated 30–45 minutes for setup and a short Cypher primer. Pilot these estimates
with a fresh student-style account; reduce tasks if setup dominates. Provide an
early checkpoint so installation difficulties surface before the submission day.

Required prior knowledge is the adoption lecture and supplied graph/Cypher
primer. The primer must explain labels, relationships, property/ID distinction,
MATCH patterns, RETURN, count, DISTINCT, ORDER BY, LIMIT, and how to interpret
returned rows. Advanced recommendations, similarity metrics, graph algorithms,
and database schema design remain optional later work.

## 9 Music fixture and database preparation

### Fixture choice

Prepare one deterministic, small fixture with approximately 6–10 playlists and
30–60 distinct tracks as a design target. Prefer a curated, complete subset of
the medium data if its distribution terms permit the intended course bundle.
Keep the existing small files available for a simpler introductory example;
their sparse overlap should not dictate misleading similarity questions.

Select playlist IDs by a deterministic rule, then take all their playlist rows
and the complete metadata for all referenced tracks, including all credited
artists and albums. If that exceeds the target size, choose a different set
of playlists. Do not truncate metadata records or arbitrarily cut playlist rows
while still presenting playlist coverage as complete.

Require at least two playlists sharing tracks, a collaboration with multiple
artists, an artist with several tracks in one playlist, and tied counts that
exercise deterministic ordering. Check these properties programmatically before
finalizing the fixture. If provenance cannot support redistribution, author an
explicitly fictional music fixture with equivalent features; identify it as
fictional and keep the same homework contract.

Publish a fixture manifest with dataset version, source/provenance, extraction
rule, file hashes, parsed row counts, distinct IDs, graph counts, and duplicate
policy. Expected answers must name the fixture version they were computed from.

### Proposed graph contract

Use familiar names from the existing music loader:

```text
(User)-[:OWNS]->(Playlist)-[:HAS_TRACK {position}]->(Track)
(Album)-[:HAS_TRACK]->(Track)-[:ARTIST]->(Artist)
```

IDs identify entities; names are display values and may not be unique. Preserve
collaborations as separate Track-to-Artist relationships. Collapse exact duplicate
playlist/track/position rows. Distinct occurrences of the same track at different
positions may remain separate; queries asking for distinct playlists or tracks
must still count correctly. Required questions do not depend on album joins or
assume every track has a single credited artist.

Derive expected graph counts after applying these rules, rather than assuming
that CSV row counts equal graph counts. Check references and reject or explicitly
report inconsistent identifiers before loading.

### Setup path

Use Neo4j Desktop as the primary student path, consistent with the existing
local course material, with a tested database version/edition. Supply a single
loading procedure, instance naming instructions, import paths, a readiness check,
and a separate reset procedure restricted to the disposable homework database.
Do not run destructive resets automatically or against a student's other data.

Validate the simplified loader against the chosen edition. Avoid requiring APOC
or similarity computation solely because they appear in the older exercises.
If the chosen server's schema operation needs an extension, test and document
that actual requirement before distributing setup instructions.

Do not make Docker and cloud provisioning competing required tracks. An
institution-provided isolated database can be an accommodation if available;
do not assume such a service exists. The default homework remains local.

## 10 Neo4j server and repository configuration

Select one tested release of the current official Neo4j server, record its
artifact/package version, and pin its actual launch command. The current
provider source lists `get-schema`, `read-cypher`, and `write-cypher`; it also
documents a read-only setting that disables writes. Check the chosen release's
actual discovery output and configuration rather than treating these moving
names as the assignment's permanent schema.
[Official source](https://github.com/neo4j/mcp) and
[configuration reference](https://neo4j.com/docs/mcp/current/configuration/).

Supply a `.mcp.json.example` for Claude Code using stdio and the tested launcher.
The template must specify the URI, database, and username through documented
configuration and obtain the password from a locally supplied environment
variable. Explain how to set it in each supported shell and how to start the
host with that environment. A `.env.example` alone does not guarantee that a
host or launcher reads `.env`; verify and teach the actual mechanism.

Keep credentials and local environment files out of version control. Test a
missing-password diagnostic. Record that MCP server startup and database startup
are separate readiness conditions. Do not copy placeholder passwords from the
old guide into a working class configuration.

Load data through the provided setup procedure before attaching the agent.
Configure read-only operation for the querying phase and use restricted database
credentials where supported by the selected edition. Verify actual available
tools, a benign read, and the chosen permission boundary. Provider read-only
checks, host approvals, and database authorization are separate controls; do
not claim that the provider flag alone proves every possible query is harmless.
The assignment requires no write prompt or destructive testing.

## 11 Homework tasks and evidence

### Task 1 Setup checkpoint

Create the designated homework instance, load the versioned fixture, and verify
the supplied counts. Configure the server in the homework repository, inspect
connection status, and record the discovered tools. Submit a short checkpoint
record containing versions, manifest identity, readiness checks, and sanitized
configuration. Students should resolve setup failures before attempting queries.

### Task 2 Explain the schema

Ask the agent to inspect the schema and explain how a playlist connects to an
artist. Include the actual schema-tool evidence, a small diagram, and the student's
own explanation of the relationship direction and intermediate Track node.
A generic description of music data is insufficient.

### Task 3 Answer two precise questions

Required question A:

> Which five artists appear in the greatest number of distinct playlists in
> this fixture? Credit each artist on a collaboration. Count a playlist at most
> once per artist. Return artist ID, name, and playlist count, ordered by count
> descending and artist ID ascending for ties.

Required question B:

> For the designated playlist ID supplied with the fixture, which other
> playlists share at least one distinct track? Exclude the designated playlist.
> Return the top five playlist IDs, names, and shared-track counts, ordered by
> shared-track count descending and playlist ID ascending for ties.

These questions are deliberately about the loaded fixture. They do not establish
commercial popularity, listening frequency, or musical similarity in general.
No result should imply those broader interpretations.

For each question, students specify intent, ask the agent to inspect the schema,
review the generated query, execute a bounded read, and compare final prose to
the returned rows. The host may combine some of these actions; evidence should
reflect the actual sequence rather than a fabricated ideal transcript. Where
human review before execution is required, use a two-step prompt and the host's
appropriate interaction rather than assuming a single prompt guarantees it.

Starting prompt pattern:

> Use the configured music MCP server. First inspect the schema. For the
> following question, propose a bounded read-only Cypher query and explain how
> you avoid duplicate counting. Show me the query before executing it: [question].

Follow-up after review:

> Run the reviewed query using the music MCP tool. Present the returned rows
> and a concise answer grounded in those rows. State that these results describe
> the supplied fixture.

Required evidence per question: exact prompt(s), actual tool name and arguments,
Cypher, returned rows, final answer, and a student explanation of the count and
tie rules. If the first query is wrong, preserve the mistake and correction;
assess the final reasoning and honest diagnosis rather than first-attempt success.

### Task 4 Independently verify

Run at least one supplied reference query directly in Neo4j's query interface,
outside the model conversation. Compare IDs, counts, ordering, and empty-result
behavior with the agent-assisted result. Matching prose is not sufficient.
Explain how the reference query implements the specification.

A proposed reference for question A is:

```cypher
MATCH (p:Playlist)-[:HAS_TRACK]->(:Track)-[:ARTIST]->(a:Artist)
RETURN a.id AS artist_id, a.name AS artist_name,
       count(DISTINCT p) AS playlist_count
ORDER BY playlist_count DESC, artist_id ASC
LIMIT 5
```

This query must be executed and checked against the final fixture before it
becomes an answer key. Question B's reference must similarly count distinct
tracks and exclude the source playlist. Supply a selected fixture ID so students
do not have to guess a display name or choose a playlist with no overlap.

The instructor also computes expected answers with an independent CSV-based
oracle. That oracle deduplicates playlist occurrences, builds track-to-artist
and playlist-to-track sets, and calculates the specified rankings without the
agent or Cypher. Agreement with the reference queries helps catch a bad answer
key or loader. Direct query replay is independent of model narration, but is
not by itself an independent implementation of the data semantics.

### Task 5 Clarify an ambiguous request

Respond to “Which artist is most popular?” with at least two possible meanings,
then choose one that the fixture can support and restate it precisely. Explain
why the other interpretation cannot be inferred from the available data, if
that is the case. No extra database query is required when question A already
answers the clarified version.

### Task 6 Record a diagnosis and reflection

Use one encountered failure or a provided captured failure to identify the
failing layer and explain the next diagnostic step. Students need not induce a
failure in a working setup. Finish with a brief reflection on what the agent
helped with and what still required student judgment.

## 12 Submission and assessment

Proposed submission structure:

```text
music-mcp-homework/
  README.md                 # versions, fixture identity, reproduction
  .mcp.json                 # portable configuration, no secrets
  evidence/
    connection.md
    schema.md
    question-a.md
    question-b.md
    verification.md
  queries/
    question-a.cypher
    question-b.cypher
  reflection.md
```

Allow a sanitized tool export or screenshots plus text where host export support
varies. Screenshots alone should not make queries or IDs impossible to inspect.
Keep result tables small and provide tool-result excerpts rather than an entire
account conversation. Students may use agents throughout, but must explain the
queries, record assistance, and preserve the evidence supporting their answers.

| Criterion | Points | What earns credit |
|---|---:|---|
| Reproducible setup and configuration | 15 | Correct project scope, versions, fixture, external credentials |
| Schema understanding | 10 | Accurate graph path, identifiers, relationship direction |
| Queries and intended semantics | 25 | Correct distinct counts, exclusions, ties, bounds |
| Tool and answer evidence | 20 | Actual calls/results and answers supported by rows |
| Independent verification | 20 | Direct reference execution, precise comparison, explanation |
| Ambiguity and diagnosis reflection | 10 | Explicit interpretation and reasoned diagnostic step |
| Total | 100 | |

Do not grade identical model wording or a prescribed number/order of tool calls.
Do grade query semantics and evidence. A provider outage should not become a
judgment about student understanding: offer a separately labeled evidence-analysis
path with supplied schema/results while arranging a later live setup check or
an available isolated database. That path cannot be reported as successful live
integration. Provide the accommodation policy before the due date.

## 13 Artifact layout

Keep the dice package in place and add descriptive, unnumbered filenames until
course placement is settled. The following paths are proposed deliverables,
not links to already implemented files:

| Area | Proposed artifacts |
|---|---|
| Instructor | `lectures-instructor-notes/lecture-mcp-adoption.md` |
| Student notes | `lecture-notes/lecture-mcp-adoption.md` |
| Slides | `slides/lecture-mcp-adoption.md` with concise text and fuller speaker notes |
| Diagrams | Mermaid and SVG for configuration/discovery/call, remote vs local, Neo4j processes, and music graph |
| Documentation demo | `demos/adoption/README.md`, `DEMO.md`, `.mcp.json.example`, evidence template, actual captures, verification |
| Homework handout | `homework/neo4j-music/README.md`, graph/Cypher primer, setup guide, evidence examples |
| Homework fixture | `homework/neo4j-music/fixture/` with CSVs, provenance, manifest, deterministic extraction or authored source |
| Homework tooling | Loader, readiness checks, instructor reference queries, CSV oracle, verification report |
| Instructor key | `instructor-materials/neo4j-music/` with expected answers, rubric examples, common mistakes; exclude from student export |
| Reconciliation | Expanded dice notes, revised lecture introductions, workspace README and source map |

Use the established three-artifact lecture pattern and purple slide style.
Preserve Mermaid sources and SVGs; treat generated slide PDF/HTML as preview
artifacts. Update the existing slide build script to render both decks and all
required diagrams without relying on author-specific paths.

## 14 Required expansion of the dice notes

The current dice notes are a useful first draft but are too compressed for the
requested tutorial standard. Plan a substantive rewrite rather than a few
extra paragraphs. Preserve the tested MCPServer implementation and version pin
unless a concrete compatibility issue requires a change.

Add a guided direct-function/CLI example; a complete minimal server before
showing later refinements; annotated signatures, defaults, decorators, and
schemas; a line-by-line explanation of actual discovered input/output; and a
full valid call with text and structured result compared side by side. Trace
where the dice sum is calculated and where the comparison with 12 occurs.

Explain each validation layer with concrete valid and invalid inputs. Walk
through count=0, count as a string, unsupported sides, and malformed protocol
requests, showing which component detects each and what the caller observes.
Discuss strict types and the difference between a schema constraint and a
semantic invariant such as total=sum(rolls).

Walk through a controlled-randomness test, a schema/result test, and a real
subprocess test. Explain what each can establish and what remains for a model
integration test. Include complete fresh-checkout commands and a troubleshooting
narrative for a wrong interpreter, broken path, and stdout logging.

Connect configuration back to the adoption lecture: a remote URL is replaced
by a launch command, while discovery and the host loop remain recognizable.
Provide resources/prompts orientation, CLI/MCP decision examples, costs/context
examples, a glossary, and explained self-checks. Keep historical transcripts,
constructed teaching examples, and newly executed evidence distinguishable.
The notes must support independent learning; slide brevity must not constrain
them.

The adoption lecture will carry most first-use setup and provider survey content.
The dice classroom walkthrough should retain a brief recap but use recovered
time for contracts, validation, result representation, and testing. Reconcile
outline, slides, and notes together rather than quietly changing only one.

## 15 Implementation order and completion criteria

### Phase 1 Rehearse the adoption example

Create an isolated scratch repository and verify Microsoft Learn connection,
discovery, actual search/retrieval, and a grounded answer with Claude Code.
Capture versions/date and an LLM-free check. Confirm that the main question is
answerable from the provider's current corpus. If it is not, select another
bounded file/documentation task with the same teaching purpose and update all
three lecture artifacts consistently. Do not spend time building another server.

Completion: tested configuration, actual tool contracts, successful calls,
checked citations, and an outage fallback. Keep model/host account data out of
captures. Record remote service date rather than claiming the deployment is pinned.

### Phase 2 Finalize and verify the music fixture

Resolve provenance, select deterministic complete data, write the manifest,
prepare the simple loader, and implement the independent expected-answer oracle.
Choose and test the database/server release combination and student launch path.

Completion: clean load, correct counts and references, correct duplicate policy,
question coverage, deterministic answers, tested read-only querying, and expected
answers matching the independent oracle. Verify documented recovery on an empty
homework instance. No result from the medium dataset may be reused as a small
fixture answer without recomputation.

### Phase 3 Author the student explanations and instructor materials

Draft the expanded notes first so the conceptual narrative is fully developed.
Write the instructor outline and slides from that narrative, keeping classroom
and optional depth explicit. Prepare the homework handout, primer, evidence
templates, answer key, rubric, and setup checkpoint. Expand the dice notes and
adjust the two lectures' overlap.

Completion: each objective has an explanation, worked example, student check,
and evidence expectation. Every technical setup step has expected observations
and recovery advice. A student can follow the package without the instructor
supplying omitted prerequisites.

### Phase 4 Verify the complete student path

Rehearse from a clean student-style directory and database instance. Check
project configuration, tool discovery, data readiness, both homework questions,
reference-query replay, exact result comparisons, and the bounded lecture task.
Test configuration failures independently of model failures. Inspect exported
student files for accidental answer-key inclusion or credentials.

Render all diagrams and both slide decks, inspect projection readability and
layout, check local links, and reconcile stage names, prompts, schema names,
version pins, and expected observations. Record actual pass/fail/skipped checks
with specific reasons. If host authentication is unavailable, finish independent
checks and clearly identify the host rehearsal that remains.

Completion: the verification report supports each claimed execution, clean
setup is reproducible on the supported platform, artifacts agree, and instructor
fallbacks are usable. Mark any additional OS instructions as unverified until
rehearsed; do not imply universal platform coverage from one machine.

### Phase 5 Instructor review and later curation

Review pacing, note depth, homework workload, fixtures, and expected answers.
Choose lecture numbers/destination only when integrating the pair into the
course. Keep content/media and code/config licensing boundaries consistent
with the public course, and handle data attribution separately. Public migration
is a later task; frozen `course-materials/` remains read-only.

## 16 Decisions and dependencies

Proceed with these defaults: Microsoft Learn as the lecture candidate, Claude
Code as the first host, project-scoped repository configuration, Neo4j Desktop
as the primary homework database path, a curated small music fixture, two precise
read questions, and independent result verification. These choices do not
require another planning approval before routine implementation.

Resolve technical dependencies through rehearsal: the exact Neo4j/server pin,
required database extensions, supported edition/permission configuration,
fixture extraction and redistribution, and the final source-playlist ID.
Course-calendar placement, grading weight within the course, due date, and any
institution-provided database accommodation remain instructor scheduling choices;
they do not block authoring the materials with relative dates and the proposed
100-point rubric.
