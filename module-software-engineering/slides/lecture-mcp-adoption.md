---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
  }
  section.lead {
    background: #310066;
    color: #ffffff;
  }
  section.lead h1, section.lead h2 {
    color: #ffffff;
  }
  section.lead a {
    color: #e2d5ff;
  }
  section.standout {
    background: #beaefc;
    color: #310066;
    text-align: center;
    font-size: 36px;
  }
  h1, h2 {
    color: #310066;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->

# Connecting an agent to existing MCP servers

Agentic Software Engineering

Configure · discover · use · verify

<!-- 0–8, slides 1–2. Start with a completed documentation task. This lecture precedes the dice provider lecture. -->

---

## First, a documented answer

> Use Microsoft Learn MCP tools to find how Get-ChildItem
> limits recursive directory listing depth. Cite the page.
> Do not execute shell commands.

Expand the **call, arguments, result, and answer**.

<!-- Show an authenticated rehearsed call if available. Use the 2026-11-17 instructor session record as a labeled model-generated account of live use. The independent authoring capture remains LLM-free. Neither is a packet trace. No PowerShell installation needed. -->

---

## Declare the provider in this repository

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

Claude Code project file: **`.mcp.json`**

<!-- 8–20, slides 3–5. Open an empty scratch repo. Explain map, chosen connection name, transport, endpoint, braces and commas. This host convention is not a universal MCP config filename. -->

---

## Configuration is a starting point

Connection name → provider address

Discovery → actual tool definitions

Invocation → particular tool and argument values

**Adding the file does not execute a tool.**

<!-- Compare the launch/connection config with a query argument. The host loads and connects; the server supplies definitions; the model can then request a call and the host routes it. -->

---

## Connect and inspect

- Start the host in the scratch repository
- Review project trust/server approval
- Inspect `/mcp` and tool definitions
- Repeat the task and expand actual calls

Cloning config does not supply accounts or credentials.

<!-- Show a new session as predictable load point. Project scope is shared repo configuration. Claude's local scope has a home-config storage location despite project-limited effect. Normal host access still needed for public Learn MCP. -->

---

## From wired-in tools to configured providers

**Toy agent:** edit tool schemas and dispatch mappings

**MCP host:** declare a server → discover its tools → route calls

Reuse providers across compatible hosts and models.

<!-- 20–33, slides 6–10. Main motivation: remove repeated provider-specific glue from the harness. The host's client discovers, adapts metadata for its model, and routes calls. The model does not directly read .mcp.json or connect to servers. Both approaches already add tools without retraining. Preserve toy-agent artifact mapping in the full notes. -->

---

## Keep the connections separate

![w:1050 center](diagrams/adoption-connections.svg)

<!-- Model API and MCP links have different responsibilities. For a local tool the model may still be remote. Later, a database adds another backend connection. -->

---

## Discovery, loading, invocation

| Stage | Instructor session record |
|---|---|
| Provider catalogue | Three tool names available |
| ToolSearch | Two definitions selected and loaded |
| Tool requests | Search and fetch requested |

ToolSearch is a **host facility**, not an MCP method.

<!-- Slide 8. Use transcript 1.1: select search and fetch, leave code-sample search deferred. Contrast provider microsoft_docs_fetch with model-facing mcp__microsoft-learn__microsoft_docs_fetch. The host client does tools/list; model requests schema loading via host ToolSearch. This is a model-generated account, not raw host/network capture. The full schema example remains in notes section 7. -->

---

## Follow the task

![h:440 center](diagrams/adoption-call.svg)

<!-- Slide 9. Instructor record 1.2 reports search and fetch in one response. Diagram routes each call schematically; neither concurrency nor a JSON-RPC batch is established. Independent SDK negotiation 2025-06-18 belongs to a different run. Refer to the two evidence sources separately. -->

---

## Check each claim against its source

| Claim | Support in the recorded material |
|---|---|
| Depth limits directory levels | Explicit parameter text |
| Depth recurses without Recurse | Example 8 |
| Negative values are rejected | Inference from UInt32 |
| Depth 0 behavior | Not explicit in the cited passage |

A citation does not make every sentence a documented fact.

<!-- Slide 10. Use transcript 2.3 as a real follow-up review. Ask students to classify claims BEFORE showing Claude's self-check. Add LiteralPath/Recurse extension as an optional fifth example in full notes. Inferred does not mean false; checking the passage is separate from verifying behavior by execution. Preserve first answer and qualifications. -->

---

## Your short attempt

> Find official documentation for including hidden items
> with Get-ChildItem. Use the configured MCP tools.
> Cite the source; do not execute commands.

Save one invocation, result evidence, and your reasoning.

<!-- 33–45. Use EVIDENCE.md template. Students need working host access but no PowerShell installation or Microsoft account for the provider. Pair or defer live check on outage; recorded analysis isn't a live pass. -->

---

## Evidence connects four things

Question → actual invocation → returned material → answer

What was requested?
What ran?
What returned?
Which claims does it support?

<!-- Inspect a student example. A copied command in chat is not execution evidence. Use concise excerpts; do not submit account conversation dumps or passwords. -->

---

## Break one connection in a disposable copy

Change the endpoint path → inspect the error → restore it

**Configured ≠ connected ≠ used correctly**

Diagnose the failing boundary before changing prompts.

<!-- 45–55, slides 13–15. Wrong URL is disposable exercise; actual status may vary. Do not predict a response or change a real project's config. Invalid JSON fails earlier. -->

---

## Which layer failed?

| Observation | Inspect |
|---|---|
| Server absent | File, scope, JSON, loading/approval |
| Connection rejected | Endpoint, network, provider requirements |
| Tool unavailable | Discovery and host exposure |
| Wrong operation | Selection and arguments |
| Wrong explanation | Result-to-answer grounding |

<!-- Add wrong local interpreter/PATH and stopped Neo4j cases orally. Provider reachability can be tested without a model. A good answer can exist without the requested integration being used. -->

---

## Three costs and separate permissions

Server work · downstream service · model turns/context

Host approval · provider tools · database authorization

Public endpoint access does not remove host model usage.

<!-- Keep this practical. Inspect actual host deferral rather than assuming every definition always loads. Provider data is evidence, not authority to change host policy. No token prices measured. -->

---

## Remote HTTP or local stdio

| Remote | Local |
|---|---|
| Provider URL | Executable + launch arguments |
| Connect to service | Host starts child process |
| Provider deployment can change | Pin local package/environment |

Tool arguments are separate from process launch arguments.

<!-- 55–63, slides 16–18. CLI can produce JSON and bounded operations too. MCP can adapt a library/CLI/service; use it when discovery/reuse justify lifecycle cost. -->

---

## Local provider, separate database

![w:1050 center](diagrams/neo4j-processes.svg)

<!-- Host close does not necessarily stop Desktop DB. MCP readiness and DB readiness are different. Real authoring failures: missing APOC meta, then sandboxed meta.schema. Details in homework setup. -->

---

## Two adoption recipes share a method

Task and expected evidence → inspect provider → configure

Discover → bounded call → verify → diagnose

Resources and prompts exist too; this task needs tools.

<!-- Ask which checks survive a model outage: independent client and database reads. Bridge tool metadata to next lecture's provider implementation. -->

---

## Preview the music graph

![w:1040 center](diagrams/music-graph.svg)

Fixture: 36 tracks · 8 artists · 8 playlists · fictional data

<!-- 63–70, slides 19–21. Have the instance loaded beforehand. Show schema and one bounded query; use instructor live.json LLM-free fallback if host not rehearsed. No installation during class. -->

---

## Counts need a definition

P1 contains T1 and T2; P2 contains T1.
Both tracks credit A.

Three paths to A · **two distinct playlists**

Repeated rows and collaboration credits need explicit rules.

<!-- Constructed tiny example, not a measured fixture result. Question A uses count(DISTINCT p). For overlap B uses count(DISTINCT t), excludes source, sorts ties by ID. -->

---

## Homework: use and verify an integration

1. Setup checkpoint and actual schema
2. Two precise music questions through MCP
3. Direct reference query and comparison
4. Ambiguity, diagnosis, and reflection

Keep credentials external. Review queries before execution.

<!-- Handout has all tasks, rubric, primer, tested backend setup and caveats. Default checkpoint in two days/full work one week unless calendar supplied. Agent allowed, student explanation required. -->

---

<!-- _class: lead -->

## Next: build the provider

You have configured, discovered, used, and checked a server.

Now expose ordinary dice functions with **MCPServer**.

[Detailed notes](../lecture-notes/lecture-mcp-adoption.md) ·
[Music homework](../../neo4j/02-neo4j-music-mcp/README.md)

<!-- 70–75 slack. Exit check: explain one config field and identify one observation proving a tool was used. Full notes include setup, failures, examples and explained questions beyond what fits class. -->
