# Connecting an agent to existing MCP servers

75-minute instructor outline. This meeting precedes the dice implementation
lecture and launches the music homework. Students know the basic agent loop
and toy-agent exercise; no database is needed for the main lecture. The
[student notes](../lecture-notes/lecture-mcp-adoption.md) provide the full tutorial
and optional depth. Do not compress them to match classroom time.

## Outcomes and evidence

Students should explain, with reference to the toy agent, why a declared server
replaces per-tool edits to the harness; explain server configuration vs discovered tool contracts,
configure a project-scoped integration, distinguish model API/MCP/backend
connections, inspect actual tool use, verify a source-based answer, and diagnose
a failure by layer. In class, collect one small documentation evidence record.
Homework adds graph semantics and independent result verification.

Use [DEMO.md](../demos/lecture-mcp-adoption/DEMO.md) for exact prompts and scratch commands,
[the homework](../../neo4j/02-neo4j-music-mcp/README.md) for task wording, and
[verification](../demos/lecture-mcp-adoption/reports/adoption-and-music-verification.md) for what actually ran.
The instructor supplied a [2026-11-17 session record](../demos/lecture-mcp-adoption/claude-session/mcp-microsoft-learn-transcript.md)
and [walkthrough](../demos/lecture-mcp-adoption/claude-session/mcp-microsoft-learn-tutorial.md).
The record was written by Claude from its context after the live run. Use it
as a labeled account of model-visible requests/results/answers, distinct from
independent SDK captures and illustrative protocol/API envelopes.

## Before class

- Install dependencies and rehearse the public endpoint before students arrive.
  Have working host access, project configuration, `/mcp`, discovered schemas,
  the source article, and actual protocol evidence ready.
- Have exercise 04 Steps 5, 6 and 8 at hand; the motivation slides quote simplified
  versions of that code and students should recognize their own loop.
- Use a scratch repository. Do not register global servers or activate the
  example in this repository. Isolate competing integrations if needed,
  explaining the explicit session config as a rehearsal measure.
- Prepare two versions of the file: correct URL and a disposable incorrect path.
  Inspect actual failure behavior instead of promising an HTTP status.
- Load the fictional music fixture into a separate instance beforehand. Verify
  matching APOC/meta configuration, counts, provider tools, and one read query.
  Keep the actual direct/MCP capture and source-based explanation as fallback.
- Review the compact slides and full notes together. The notes teach JSON,
  schema, environment variables, transports, and failures more gently than can
  be covered live. Point students to the relevant section when cutting detail.

## Timed sequence

| Minutes | Slides | Actions and expected observations | Fallback or cut |
|---|---|---|---|
| 0–8 | 1–2 | Run the exact Get-ChildItem documentation task. Expand call, arguments, result, citation and answer. | Show saved independent capture plus source article, label LLM-free. No PowerShell execution. |
| 8–18 | 3–6 | Motivation. Show the simplified toy-agent registrations and loop; ask what Step 8 made you edit. Contrast a per-tool schema with a per-server declaration. Walk the connections diagram: host client discovers, model selects, host routes. State the two benefits and the caveats. | If short, cut slide 6 to its two bold lines; the full argument is notes Section 1. |
| 18–28 | 7–9 | Open empty scratch repo. Add complete `.mcp.json`, explain each field, start fresh host session, inspect `/mcp` and tools. | Have prepared scratch repo/capture. Keep configuration explanation even if network fails. |
| 28–36 | 10–12 | Map toy-agent artifacts onto the host now that `/mcp` has been seen, separate provider discovery from ToolSearch loading, trace paired search/fetch requests. | Cut the ToolSearch detail to one sentence; retain configuration/schema/call distinction. |
| 36–46 | 13–15 | Classify claims against source evidence, then students ask the hidden-items question and use the evidence template. Discuss what proves tool use and what supports the answer. | Pair or defer live check; use recorded analysis explicitly if service unavailable. |
| 46–54 | 16–18 | In disposable copy break endpoint path, observe, restore. Classify failure layer. Discuss permissions and costs with concrete examples. | Use a captured failure if live diagnosis drags. Never spend remaining class changing accounts. |
| 54–62 | 19–21 | Compare URL vs process launch, show Neo4j three-process diagram, give reusable adoption recipe. | Cut alternate-host discussion; no additional host setup required. |
| 62–70 | 22–24 | Show prepared music schema and one bounded count query. Explain distinct counts and launch homework/checkpoint. | Use instructor live capture. No database install in class. |
| 70–75 | 25 | Transition to dice, exit questions and slack. | Ask students to explain one field and one grounding observation. |

## Main walkthrough

The finished question asks about recursive directory listing depth, an accessible
file-oriented task connecting to toy-agent file operations. Search/fetch operate
on documentation, so neither Microsoft credentials nor PowerShell installation
is needed for the provider task. Normal host account/model access remains needed.

After showing the finished behavior, reconstruct configuration. `mcpServers`
contains connection entries; the chosen `microsoft-learn` key is not necessarily
a tool name. `http` and `url` tell the host how and where to connect. JSON syntax
is not executable shell syntax. Discuss project vs local vs user scope and the
misleading local-scope name; share the repository file, not user credentials.

The motivation now comes right after the cold open, before any configuration
detail. Put the simplified toy-agent code on the screen and let students name
what Step 8 made them edit: a schema in `TOOLS_SCHEMA`, a function, and a
dispatch entry in `TOOLS_DICTIONARY`, for every tool, in every harness. Then
show that the server declaration contains none of those, and walk the basic
connections diagram: the developer declares a server, the host's client
discovers its tools with `tools/list`, the model is shown the definitions and
requests a call, the host routes it with `tools/call`. In the toy agent, adding
dice means editing schemas and dispatch mappings in harness code; in an
MCP-capable host it means declaring the server and discovering its catalogue. Reuse across hosts and models comes from the standard provider
interface plus each host's model adaptation. Both approaches can already add
tools without retraining. Distinguish host/client protocol discovery from any
model-guided search over tool metadata; the model does not directly connect to
the declared servers or receive the raw configuration as its tool catalogue.

Explain discovery with the actual listing. Model API definitions are adapted
by the host; MCP requests are not directly sent by the model. Match the query
argument with returned material and the final claim. A successful fetch does
not automatically prove the final explanation. A citation alone does not prove
the integration ran.

Use the instructor session as the worked example. Transcript 1.1 shows three
deferred names and a ToolSearch request loading two schemas. Distinguish provider
catalogue discovery, definitions made available to the model, and actual tool
requests. Show the provider/model-facing fetch names to explain host adaptation.
ToolSearch is a host facility, not the model directly emitting tools/list.

Transcript 1.2 requests search and fetch together. The diagram therefore routes
each request rather than requiring search-before-fetch. Same-response requests
permit concurrency; no execution timing is established by this account.

For grounding, show the first answer, then ask students to classify selected
claims before revealing transcript 2.3. Directory-level control is explicit
parameter text, recursion without Recurse is illustrated by Example 8, rejection
of negatives is inferred from UInt32, and Depth 0 is not explicit in the cited
passage. Include the extension of LiteralPath advice if time permits. An inference
may be correct but still needs distinct support. Claude's self-check is another
claim to inspect, not an automatic verification verdict.

The independent SDK connection negotiated 2025-06-18. That does not establish
Claude Code's negotiated version. The dice/music captures use 2026-07-28.
Use this contrast to explain why illustrative startup envelopes must be scoped
to a protocol revision. Do not infer hidden request counts, permission decisions
or API bodies from a model-visible reconstruction.

## Student activity and understanding checks

Have students save the exact task/prompt, connection and tool identity, actual
arguments, relevant result excerpt, citation, final answer and their acceptance
reason. Use [EVIDENCE.md](../demos/lecture-mcp-adoption/EVIDENCE.md). Tool call count and final
wording may vary. Do not grade a prescribed sequence where the evidence supports
another valid path.

Ask who executes the operation, why a URL in `.mcp.json` differs from a URL in a
fetch argument, why cloned configuration may still fail elsewhere, and whether
a connected server guarantees use. Ask which checks work without a model:
direct service/client checks can, while model selection/grounding cannot.

For diagnosis, compare invalid JSON, wrong endpoint, missing local executable,
stopped database, and incorrect final interpretation. Keep the observed symptom
attached to its layer. Real preparation failures included missing APOC and then
sandboxed `apoc.meta.schema`; they are in the homework failure record.

## Homework launch and instructor key

The homework fixture is original fictional music data with collaborations,
duplicate occurrences, shared tracks, tied rankings and duplicate display names.
It is reproducible, not a claim about a real catalogue. Setup uses a separate
instance and external password references. The database loader refuses nonempty
data. Provider querying exposes only schema/read tools; explain the difference
between provider restrictions, host approvals, and database roles.

The two questions require distinct-playlist counts per artist and distinct-track
overlap with P01. Direct query replay and student explanation are required.
The [instructor key](../demos/lecture-mcp-neo4j/instructor-key/README.md) contains actual
results, the CSV oracle comparison, rubric guidance, and export procedure.
Keep it out of the student bundle. A setup checkpoint comes before the due date;
adjust the default relative dates to the course calendar.

After class, review whether the 10-minute student attempt was realistic, measure
setup burden, and rehearse projection/pacing. The supplied record documents instructor documentation use; raw host/network
traffic, music host use, GUI screenshots and additional OS instructions remain
separate checks. Do not present the new record as completing those other checks.
No public migration or numbering is part of this package.
