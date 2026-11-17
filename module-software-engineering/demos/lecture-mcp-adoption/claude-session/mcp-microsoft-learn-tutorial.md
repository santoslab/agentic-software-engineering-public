# Tutorial: following one task through MCP

This walkthrough follows the first turn of the recorded session in
`mcp-microsoft-learn-transcript.md` step by step, from the moment the host reads `.mcp.json` to the
moment the model's answer appears in the terminal. Each step names who is talking to whom. Model-visible examples come from the
Claude-generated session record; protocol and API envelopes are illustrative reconstructions. The steps are numbered so they can be matched against the
"Follow the task" message sequence chart in `slides/lecture-mcp-adoption.md`.

## Evidence boundaries

The instructor ran this session on 2026-11-17, then asked Claude to record it
from its context. The [transcript](mcp-microsoft-learn-transcript.md) is that
model-generated record, preserved unchanged. It is useful evidence of the live
interaction, but is not a verbatim host export, packet trace, or independent
measurement of host internals. Read reported calls and answers as that record.

The separate [SDK capture](../evidence/remote.json) directly records definitions,
arguments, summaries and a negotiated version for an independent run on
2026-11-16. It used the PowerShell 7.5 page; the instructor session's results
refer to 7.6. Its version and sizes do not measure the instructor's session.

The request IDs, HTTP/API envelopes and hidden routing decisions below explain
possible implementations. They are not captured Claude Code traffic. Distinguish
what the record shows, what a protocol requires, and what remains inferred.

## The three participants

The chart has three lifelines. Here is what each one was in the recorded session.

| Chart participant | In this session | What it speaks |
|---|---|---|
| **Host / client** | Claude Code CLI in the instructor's terminal. It contains an MCP *client* that owns the connection to the server. | To the user: terminal text. To the model: the Anthropic Messages API (HTTPS, JSON). To the server: MCP, which is JSON-RPC 2.0 over Streamable HTTP. |
| **Model API** | The Anthropic Messages API serving Claude Fable 5.1. | Receives a system prompt, a list of tool definitions, and the conversation. Returns content blocks, some of which are `tool_use` requests. |
| **Learn server** | `https://learn.microsoft.com/api/mcp`, a remote MCP server operated by Microsoft. | MCP. Exposes three tools: `microsoft_docs_search`, `microsoft_code_sample_search`, `microsoft_docs_fetch`. |

The single most important fact for reading the chart: **the model never speaks MCP.** The model
only ever emits a tool name plus an arguments object. The host translates that into a JSON-RPC
request, sends it to the server, receives the result, and feeds the result back to the model as
text. Students should trace every arrow and ask "which of the three protocols is this?"

## Mapping the diagrams to this walkthrough

The [call diagram](../../../slides/diagrams/adoption-call.mmd) follows the reported
same-response search/fetch requests. The [discovery and loading diagram](../../../slides/diagrams/adoption-discovery.mmd)
separates MCP discovery from host tool search. Both are schematic explanations,
not wire traces. The full student explanation is in
[notes sections 7–9](../../../lecture-notes/lecture-mcp-adoption.md).

| Tutorial steps | Boundary and observation |
|---|---|
| 1–3 | Configuration and host/client discovery; protocol startup reconstructed |
| 4–5 | Model-visible deferred names, ToolSearch, and selected definitions |
| 6 | Model requests search and fetch in one response |
| 7–8 | Host routes each operation and returns provider data; envelopes illustrative |
| 9 | Follow-up fetch to check individual claims |
| 10–11 | Model-visible results and explanation; API framing illustrative |

Two requests in one response permit concurrent execution. They do not establish
that the host actually executed them concurrently; no timing trace is supplied.

---

## Step 1. Configuration: the host learns a server exists

**Boundary:** none yet. This is a file on disk.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

The scratch repository contained one file:

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

Field by field:

- `mcpServers` is a map. Each key is a **connection name** chosen by whoever wrote the file. The name
  `microsoft-learn` reappears later as the middle segment of every tool name the model sees.
- `type: "http"` selects the **Streamable HTTP** transport. The host will send HTTP POST requests to
  the URL. Compare the local alternative from the "Remote HTTP or local stdio" slide: a `command` and
  `args` that the host would launch as a child process and talk to over stdin/stdout.
- `url` is the endpoint. Nothing else is needed for this public server. A private server would add
  headers or an OAuth flow here.

Because the file sits in the repository root, it is **project-scoped**: anyone who clones the repo
gets the same declaration. Claude Code asks the user to approve a project-scoped server the first time
it is loaded. That approval is a host policy, not part of MCP.

The model does not read this file. It has no idea the file exists unless someone shows it to it.

---

## Step 2. Connect and initialize

**Boundary:** Host ↔ Server, JSON-RPC 2.0 over HTTP.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

In the older 2025-06-18 protocol path illustrated here, startup uses `initialize`
and then `notifications/initialized`. The client proposes a version/capabilities;
the server responds with its selected version, capabilities, identity and optional
instructions. This is not universal: the package's modern dice capture uses
`server/discover` under revision 2026-07-28. [SDK protocol changes](https://py.sdk.modelcontextprotocol.io/whats-new/).

> **Evidence note.** The model never sees this traffic, so the envelopes below are reconstructed from
> the MCP specification (revision 2025-06-18). The independent SDK capture records
> `"protocol_version": "2025-06-18"` for its own connection to this endpoint;
> it does not confirm Claude Code's negotiated version. The session record reports
> model-visible server instructions (section 0.1), but does not prove the host's
> exact system-message serialization or the instruction string's wire provenance.
> IDs, client/server identities and HTTP details below are illustrative.

Request, sent as the body of an HTTP POST to `https://learn.microsoft.com/api/mcp` with
`Content-Type: application/json` and `Accept: application/json, text/event-stream`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": { "name": "claude-code", "version": "<host version>" }
  }
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": { "tools": {} },
    "serverInfo": { "name": "<server name>", "version": "<server version>" },
    "instructions": "# Microsoft Learn MCP Server\n\nThis server gives structured access to official Microsoft and Azure documentation via three tools:\n\n## Tools\n\n### microsoft_docs_search\nSearch official documentation and return up to 10 concise, high-quality content chunks ... \n\n## Workflow\n\n1. Use `microsoft_docs_search` to find relevant documents.\n2. If you need code examples or practical snippets, use `microsoft_code_sample_search`.\n3. If deeper or complete information is needed, use `microsoft_docs_fetch`.\n\n**Search gives breadth. Code Sample Search gives practical examples. Fetch gives depth.**\n\n..."
  }
}
```

The client then sends a notification. Notifications have no `id` and receive no reply:

```json
{ "jsonrpc": "2.0", "method": "notifications/initialized" }
```

Things to point out:

- `jsonrpc`, `id`, `method`, `params` on the way out; `jsonrpc`, `id`, `result` (or `error`) on the
  way back. Request, result, error and notification envelopes differ; the examples show the relevant forms.
- `capabilities.tools` in the response is how the server says "I have tools; you may call
  `tools/list`." A server might instead, or also, advertise `resources` or `prompts`. This task needs
  only tools.
- `instructions` is prose written by the server operator for the model. The record reports it as
  model-visible instruction text. Host presentation is separate from the MCP wire format.
- Later HTTP requests on this connection carry an `MCP-Protocol-Version: 2025-06-18` header, and a
  `Mcp-Session-Id` header if the server issued one.

---

## Step 3. Discover the tools

**Boundary:** Host ↔ Server.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

Request:

```json
{ "jsonrpc": "2.0", "id": 2, "method": "tools/list" }
```

Response, showing the fetch tool in full and the other two elided. The independent run's normalized listing is saved in [remote.json](../evidence/remote.json).
This is an illustrative envelope around that listing, not the session's raw response.

```jsonc
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      { "name": "microsoft_docs_search", /* ... */ },
      { "name": "microsoft_code_sample_search", /* ... */ },
      {
        "name": "microsoft_docs_fetch",
        "title": "Microsoft Docs Fetch",
        "description": "Fetch and convert a Microsoft Learn documentation webpage to markdown format. ...\n\n## When to Use This Tool\n- When search results provide incomplete information or truncated content\n...\n## Usage Pattern\nUse this tool AFTER microsoft_docs_search when you identify specific high-value pages that need complete content. ...\n\n## URL Requirements\n- The URL must be a valid HTML documentation webpage from the microsoft.com domain\n- Binary files (PDF, DOCX, images, etc.) are not supported\n\n## Output Format\nmarkdown with headings, code blocks, tables, and links preserved.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "url": {
              "description": "URL of the Microsoft documentation page to read",
              "type": "string"
            }
          },
          "required": ["url"]
        },
        "annotations": {
          "title": "Microsoft Docs Fetch",
          "readOnlyHint": true,
          "destructiveHint": false,
          "idempotentHint": true
        }
      }
    ]
  }
}
```

What each field is for:

| Field | Audience | Purpose |
|---|---|---|
| `name` | host and model | The identifier used in `tools/call`. |
| `title` | humans | Display name for a host UI such as the `/mcp` menu. |
| `description` | the model | Prose that tells the model what the tool does and *when to use it*. Note that Microsoft wrote a "Usage Pattern" into it. The reported session used search and fetch; this does not isolate what caused that choice. |
| `inputSchema` | host and model | JSON Schema for the `arguments` object. The host can validate before sending; the model uses it to shape its output. |
| `outputSchema` | host | Present on the two search tools, absent on fetch. Declares the shape of `structuredContent` in results. |
| `annotations` | host | Hints for policy and UI. A host may consult these hints, but its actual policy decision is not captured here. They are not guarantees. |

The record reports available tools at startup. It does not expose every MCP exchange,
so the absence of repeated model-visible discovery cannot prove no refresh occurred.

---

## Step 4. Adapt the definitions for the model

**Boundary:** inside the host.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

The Messages API has its own tool-definition format, and the host also has to keep tools from
different servers from colliding. The record presents these model-visible differences from the independently captured provider definitions:

| Server said (`tools/list`) | Model saw |
|---|---|
| `"name": "microsoft_docs_fetch"` | `"name": "mcp__microsoft-learn__microsoft_docs_fetch"` |
| `"inputSchema": {...}` | `"parameters": {...}` (the Messages API calls this `input_schema`; the host's rendering to the model used `parameters`) |
| `"description": "..."` | passed through unchanged |
| `"title"`, `"outputSchema"`, `"annotations"` | absent from the displayed definitions; internal host retention is not established |
| `initialize.result.instructions` | reported as model-visible instructions under `# MCP Server Instructions / ## microsoft-learn` |

The name pattern is `mcp__<connection name>__<tool name>`. Other servers connected in the same
session, such as a Claude Docs connector, produced names like `mcp__claude_ai_Claude_Docs__batch`.
This visible namespace identifies a provider association; the host's exact routing data structure is not visible.

One more adaptation specific to this host: the three definitions were **deferred**. The system prompt
listed only their names and told the model to load a schema on demand:

```
The following deferred tools are now available via ToolSearch. Their schemas are NOT loaded —
calling them directly will fail with InputValidationError. Use ToolSearch with query
"select:<name>[,<name>...]" to load tool schemas before calling them:
mcp__microsoft-learn__microsoft_code_sample_search
mcp__microsoft-learn__microsoft_docs_fetch
mcp__microsoft-learn__microsoft_docs_search
```

Deferring unused definitions can reduce context occupied by schemas. This is a
host loading policy, not a universal MCP requirement. Definitions loaded earlier
can remain in conversation context. Neither this record nor the independent
capture measures tokens, cache behavior or billing for the session. See
[Claude Code tool search](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search).

---

## Step 5. Task and adapted definitions reach the model

**Boundary:** Host → Model API.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

The instructor typed:

> Use the Microsoft Learn MCP tools to find the official documentation for PowerShell Get-ChildItem. Explain how to limit recursive directory listing depth. Cite the relevant page. Do not execute shell commands.

The host assembled a Messages API request. Reconstructed shape, with the parts relevant to MCP:

```jsonc
{
  "model": "claude-fable-5-1",
  "system": "... # MCP Server Instructions ... ## microsoft-learn ... (text from Step 2) ... The following deferred tools are now available via ToolSearch: ... mcp__microsoft-learn__microsoft_docs_fetch ...",
  "tools": [
    { "name": "ToolSearch", "description": "Fetches full schema definitions for deferred tools ...", "input_schema": { /* ... */ } },
    /* other host tools: Bash, Read, Write, ... */
    /* the three microsoft-learn tools are NOT here yet; only their names are in the system prompt */
  ],
  "messages": [
    { "role": "user", "content": "Use the Microsoft Learn MCP tools to find the official documentation for PowerShell Get-ChildItem. ..." }
  ]
}
```

The model's first move was to fetch the two schemas it needed. This is a call to a **host** tool,
not a direct request to the Learn MCP tool. Loading definitions may involve
host caches or refreshes; this record does not prove whether additional provider
communication occurred:

```json
{
  "type": "tool_use",
  "id": "toolu_<1>",
  "name": "ToolSearch",
  "input": {
    "query": "select:mcp__microsoft-learn__microsoft_docs_search,mcp__microsoft-learn__microsoft_docs_fetch"
  }
}
```

The host answered with the two adapted definitions. They are reproduced in full in transcript
section 1.1. From this point on, the model holds the contract: the names, the descriptions with
Microsoft's usage guidance, and the parameter schemas. Arrow (b) is now complete.

Notice what the record does not show being requested: `microsoft_code_sample_search`.
Only the search and fetch definitions were selected in the reported ToolSearch call.

---

## Step 6. The model requests a documentation search

**Boundary:** Model API → Host.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

The record reports a short status line and two tool requests in one response.
The API envelope and `stop_reason` below illustrate the Messages API convention,
not fields obtained from a raw API capture:

```jsonc
{
  "role": "assistant",
  "stop_reason": "tool_use",
  "content": [
    {
      "type": "text",
      "text": "I'll load the Microsoft Learn MCP tools, search for the Get-ChildItem reference page, and pull the section on limiting recursion depth."
    },
    {
      "type": "tool_use",
      "id": "toolu_<A>",
      "name": "mcp__microsoft-learn__microsoft_docs_search",
      "input": { "query": "PowerShell Get-ChildItem -Depth parameter limit recursion" }
    },
    {
      "type": "tool_use",
      "id": "toolu_<B>",
      "name": "mcp__microsoft-learn__microsoft_docs_fetch",
      "input": { "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem" }
    }
  ]
}
```

This is the whole of the model's contribution to the MCP exchange: a name and an arguments object
that conforms to the `inputSchema`. The model did not open a socket, did not form an HTTP request,
and did not need the server's endpoint URL to form these arguments.

Three things worth discussing with students:

1. **Why both tools at once?** The search tool's description said fetch is "a required step for
   comprehensive results," the server instructions said "Fetch gives depth," and the user asked for a
   citation of a page. The model supplied an article URL without waiting for this search result.
   The record establishes that choice, not its internal cause or the host's execution
   timing. Description/instruction text is one possible influence, not a controlled
   explanation of why it chose the pair.
2. **The arguments are exactly the schema's shape.** `query` is a string. `url` is a string. No extra
   fields.
3. **"Do not execute shell commands" constrained the model, not the server.** The model had a Bash
   tool available and did not use it. MCP tool use and local shell use are separate decisions.

---

## Step 7. The host sends `tools/call`

**Boundary:** Host → Server, JSON-RPC 2.0.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

For each requested provider tool, the host must associate the name with a
connection, apply its execution policy and route the call. Namespacing is visible;
exact prefix parsing, permission evaluation and hidden requests are not. In
particular, this record does not establish whether read-only hints determined
approval. The following two JSON-RPC requests are illustrative reconstructions,
not captured traffic or a JSON-RPC batch:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "microsoft_docs_search",
    "arguments": { "query": "PowerShell Get-ChildItem -Depth parameter limit recursion" }
  }
}
```

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "microsoft_docs_fetch",
    "arguments": { "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem" }
  }
}
```

The `arguments` object is the model's `input` object, copied through. The `name` is the server's
original name. Everything else in the envelope is the host's.

---

## Step 8. The server returns source material

**Boundary:** Server → Host.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

A `tools/call` result carries a `content` array of typed blocks, an optional `isError` indicator, and optionally
`structuredContent`. An output schema is optional; if supplied, structured results
must conform to it. Absence of a schema does not prohibit structured content.
See the [2025-06-18 output contract](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema).

Search result. The server did the retrieval against its index, assembled ten chunks, and returned
them. Because `microsoft_docs_search` declares an `outputSchema`, the specified structured-result contract applies; serialized text is also recommended
for compatibility, rather than universally mandatory. What reached the model was the text
block, so the `structuredContent` field below is inferred from the schema, not directly observed:

```jsonc
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"results\":[{\"title\":\"Get-ChildItem-Description\",\"content\":\"# Get-ChildItem\\r\\n\\r\\n- Module:\\r\\n ... \",\"contentUrl\":\"https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6\"}, ... ]}"
      }
    ],
    "structuredContent": {
      "results": [
        { "title": "Get-ChildItem-Description", "content": "# Get-ChildItem\r\n\r\n- Module: ...", "contentUrl": "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6" }
        /* ... 9 more ... */
      ]
    },
    "isError": false
  }
}
```

Fetch result. The server downloaded the HTML page, converted it to Markdown, and returned one text
block in the model-visible record. The independent listing has no output schema
for fetch. That does not establish that its wire result lacked structured content;
the following text-only envelope is an illustrative possibility:

```jsonc
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "# Get-ChildItem\n\n- Module:\n    - [Microsoft.PowerShell.Management Module](./?view=powershell-7.6)\n\nGets the items and child items in one or more specified locations.\n\n## Syntax\n\n ... (about 42,000 characters) ..."
      }
    ],
    "isError": false
  }
}
```

Two points for class:

- **Both payloads are text.** MCP results can also carry `image`, `audio`, and `resource` blocks, but
  documentation tools return text. The search result is JSON *inside* a text block. The model receives a textual representation; a client could also parse such JSON programmatically.
- **Size.** The LLM-free capture in `remote.json` measured an equivalent search at roughly 38,000
  characters and the fetch at roughly 42,000. These are character counts for a different run/page version, not measurements
  of this host session, transport bytes, tokens or billing. The useful lesson is
  that results can be much larger than the arguments and may burden context.

---

## Step 9. Fetch the article if needed, inspect the source

**Boundary:** Host ↔ Server, then the human reader.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

In the chart this is drawn as an optional follow-up. The session showed it in two forms.

**Turn 1:** the model requested fetch in the same response as search (Steps 6 through 8 above already covered
it). Its answer referred to the article; the record does not isolate which input
supported each generated sentence. The answer began: "The official page confirms everything needed, so no further lookups are
required."

**Turn 2:** the instructor asked for a deliberate check:

> Use the Microsoft Learn fetch tool to open the relevant article and check the Depth parameter section against your explanation.

The model issued one call:

```json
{
  "type": "tool_use",
  "id": "toolu_<C>",
  "name": "mcp__microsoft-learn__microsoft_docs_fetch",
  "input": { "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6" }
}
```

The record shows one fetch request and no further ToolSearch request in this turn.
It does not show hidden negotiation, cache or discovery traffic, so we cannot
conclude that no such communication occurred.

The model then compared its Turn 1 answer against the `-Depth` section and separated explicit parameter text, support from an example elsewhere on the page,
and extrapolations in its earlier answer (transcript section 2.3). This is the
"check the claim against that material" step from the "Search, retrieve, check" slide. The fetched
text is the evidence. The model's summary is a claim about the evidence. The two are not the same
thing, and Turn 2 exists to show the gap.

Students should do this check themselves: open the cited URL, find "### -Depth", and read it.

---

## Step 10. Adapted tool results go back to the model

**Boundary:** Host → Model API.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

The Messages API convention pairs `tool_result` blocks with preceding `tool_use`
blocks through `tool_use_id`. The following illustrates that convention; the
recorded model-visible wrappers do not establish Claude Code's exact API body:

```jsonc
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_<A>",
      "content": "{\"results\":[{\"title\":\"Get-ChildItem-Description\",\"content\":\"# Get-ChildItem\\r\\n ... \"}, ... ]}"
    },
    {
      "type": "tool_result",
      "tool_use_id": "toolu_<B>",
      "content": "# Get-ChildItem\n\n- Module:\n    - [Microsoft.PowerShell.Management Module](./?view=powershell-7.6)\n\n ... "
    }
  ]
}
```

In the model's context this appeared as the wrapper shown in transcript section 1.3:

```
<result>
<name>mcp__microsoft-learn__microsoft_docs_search</name>
<output>{"results":[ ... ]}</output>
</result>
<result>
<name>mcp__microsoft-learn__microsoft_docs_fetch</name>
<output># Get-ChildItem ... </output>
</result>
```

The displayed results are adapted representations rather than raw JSON-RPC.
They do not prove that the host discarded `isError` or `structuredContent`
internally, or reveal all information it transmitted through the model API.

The session record describes collapsed tool-call lines in the UI. It does not
provide screenshots or exact input-size measurements for this host interaction. Students can expand a tool call in the host
UI to see it, which is how the EVIDENCE.md template expects them to record "actual invocation" and
"returned material."

---

## Step 11. Explanation and citation

**Boundary:** Model API → Host → User.
**Diagram:** see the schematic discovery/loading and call diagrams linked above.

The record presents the question, selected definitions, retrieved material and
a final answer (transcript section 1.4). It does not provide a token/context
measurement for that request.

How the summary was built from the raw material:

| Sentence in the answer | Where it came from in the fetched page |
|---|---|
| "Use the `-Depth` parameter. It limits how many subdirectory levels Get-ChildItem descends into" | Description paragraph: "use the **Depth** parameter to limit the number of levels to recurse" |
| "`-Depth 2` returns the directory given in Path, its first level of subdirectories, and its second level" | `-Depth` entry: "For example, `-Depth 2` includes the **Path** parameter's directory, first level of subdirectories, and second level of subdirectories." |
| "Added in PowerShell 5.0" | `-Depth` entry, first sentence |
| "Type is an unsigned integer" | `-Depth` parameter properties table: `UInt32` |
| "Empty directories are omitted" | Example 8: "Empty directories are excluded from the output." |
| The `Get-ChildItem -Path C:\Parent -Depth 2` code block and the Level1/Level2/Level3 walk-through | Example 8 command and output |
| "Prefer LiteralPath over Path when recursing" | Notes discuss Recurse; extending this advice to Depth was an inference |
| "Symbolic links are not followed by default ... PowerShell 6.0" | `-FollowSymlink` entry |
| The URL at the end | The `url` argument the model itself sent, plus the `contentUrl` values in the search chunks |

This is the compression step: tens of thousands of characters of tool output became a page of
prose, with the parts relevant to the question pulled forward and everything else dropped. The final answer is visible in the record. A raw API stop reason was not captured.

Two cautions that Turn 2 made concrete:

- Summarization is lossy. The answer omitted the tree.com note and the "directory names and
  filenames are included by default" sentence.
- Summarization can add. "Negative values are rejected" and "Depth 0 lists only the immediate
  contents" are not in the page. They are reasonable inferences from `UInt32` and from the counting
  rule, but the model presented them in the same voice as the documented facts. When asked to check,
  it separated the two. A citation at the bottom of an answer does not mean every sentence above it
  is in the cited page.

---

## The loop repeats: Turn 3

Turn 3 ("find how Get-ChildItem can include hidden items") ran Steps 6 through 11 again with no
setup:

- Model → Host: two `tool_use` blocks, a search with query
  `"Get-ChildItem show hidden files -Force -Hidden -Attributes"` and a fetch of the
  `about_FileSystem_Provider` article.
- Host → Server: two `tools/call` requests.
- Server → Host: ten search chunks from five different pages, and one Markdown article.
- Host → Model: two `tool_result` blocks.
- Model → User: an answer citing three pages, distinguishing `-Force` (adds hidden items to the
  listing) from `-Hidden` (returns only hidden items) from `-Attributes` (custom filter), and noting
  which parameters are FileSystem-provider dynamic parameters.

No additional model-visible schema load is reported in Turn 3. Reuse of loaded
definitions is consistent with that record; exact counts of hidden handshakes
and discovery requests cannot be inferred from it.

---

## The three protocols side by side

| Boundary | Protocol | Outbound shape | Inbound shape |
|---|---|---|---|
| User ↔ Host | terminal | prompt text | Markdown rendered as text |
| Host ↔ Model API | Anthropic Messages API, HTTPS + JSON | `{ system, tools: [{name, description, input_schema}], messages: [...] }` | `{ content: [{type: "text"}, {type: "tool_use", id, name, input}], stop_reason }` then `{ role: "user", content: [{type: "tool_result", tool_use_id, content}] }` on the next request |
| Host ↔ MCP server | MCP = JSON-RPC 2.0 over Streamable HTTP | `{ jsonrpc, id, method: "initialize" \| "tools/list" \| "tools/call", params }` | `{ jsonrpc, id, result: {...} }` with `result.content[]`, `result.isError`, optional `result.structuredContent` |

The host is the only participant that speaks all three. That is the whole point of the
"From wired-in tools to configured providers" slide: a provider written once against MCP can be used
by compatible hosts with their supported tool-capable models. Adaptation and
schema/feature compatibility still matter; the standard does not guarantee every pairing.

---

## What kind of evidence is this?

The EVIDENCE.md template asks students to distinguish live use, LLM-free protocol use, recorded
evidence, and constructed teaching examples. Applied to these two files:

| Material | Kind | Where |
|---|---|---|
| User prompts, model `tool_use` names and arguments, tool results as the model saw them, model answers | **Instructor live session, model-generated record**; not an independent verbatim export | transcript, sections 0 through 3 |
| `tools/list` payload, negotiated protocol version, result sizes and hashes | **LLM-free protocol evidence**, captured by `check_remote.py` without any model involved | `demos/adoption/evidence/remote.json` |
| JSON-RPC envelopes for `initialize`, `tools/list`, `tools/call`; Messages API envelopes; `structuredContent` field | **Reconstructed** from the MCP specification (2025-06-18) and the Messages API documentation. Illustrative conventions, not measurements of this host; IDs and identities are placeholders. | this tutorial, Steps 2, 3, 5 through 8, 10 |

The diagrams are schematic. The transcript preserves the model-generated
account of the instructor run; the independent capture establishes only its own
connection. Neither should be promoted into a packet trace of the other.

How students can verify each layer themselves:

- **Configuration:** read `.mcp.json`.
- **Connection and discovery:** run `/mcp` inside Claude Code and open the server's tool list, or run
  `uv run --frozen python check_remote.py` from `demos/lecture-mcp-adoption` to do discovery with no model.
- **Model's requests and results:** expand the tool calls in the host UI during a live session.
- **Grounding:** open the cited URL and find the quoted section.

---

## Things to notice

1. **Provider prose can guide tool use.** The `description` of `microsoft_docs_search`
   contains "This is a required step for comprehensive results." The `instructions` block says
   "Fetch gives depth." The model requested fetch, but that observation does not prove causation.
   A tool's text is part of its interface.
2. **Namespacing is the host's job.** `mcp__microsoft-learn__microsoft_docs_fetch` keeps this
   server's `fetch` from colliding with another server's `fetch`. The server never sees the prefix.
3. **Discovery is not the same as loading.** Three tools were discovered; two schemas were loaded;
   both of those were called. The "Which layer failed?" slide's row "Tool unavailable: discovery and
   host exposure" covers exactly this distinction.
4. **The model's output is data, not an action.** A `tool_use` block is a request. The host decides
   whether to honor it, and the host performs the I/O.
5. **Verification has its own evidence.** Turn 2 reports one fetch and a
   claim-by-claim review. Hidden discovery traffic is not visible.
6. **Large results require selective explanation.** The independent run shows
   large returned texts; session-specific token/cost figures are unavailable.
7. **Approval, policy and task instructions differ.** The record reports a
   project setup and no shell use for the documentation tasks. It does not audit
   per-call host decisions or prove that read-only hints determined approval.
   A user instruction is not a downstream authorization mechanism.
