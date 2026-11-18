# Documentation adoption demonstration

Prepare a working authenticated Claude Code session before class. The instructor
supplied a [2026-11-17 session account](claude-session/mcp-microsoft-learn-transcript.md)
and [reviewed tutorial](claude-session/mcp-microsoft-learn-tutorial.md). Claude
wrote the account from its context after the live run; it is not a raw host
export. Use its requests/results/answers as recorded examples, while labeling
the independent SDK capture as LLM-free and API/protocol envelopes as illustrative.

## Opening prompt

> Use the Microsoft Learn MCP tools to find the official documentation for
> PowerShell Get-ChildItem. Explain how to limit recursive directory listing
> depth. Cite the relevant page. Do not execute shell commands.

Expand calls in the host. Check the server/tool identity, query argument, source
URL, result, and final claims. The documentation's Depth parameter bounds directory
levels; the host should distinguish that from a count of returned files. Read the
actual [Get-ChildItem article](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.5)
to check exact behavior. A correct-looking answer without calls is not a pass.
If search snippets support the answer, no fixed call count is required. To
teach article retrieval explicitly, follow with:

> Use the Microsoft Learn fetch tool to open the relevant article and check
> the Depth parameter section against your explanation.

In the instructor record, search and fetch were requested in the same response,
after ToolSearch selected their definitions. Do not require a sequential path or
claim measured concurrency. For the follow-up, have students classify the first
answer's individual claims against the parameter text and Example 8 before
showing the model's own qualifications in transcript section 2.3.

## Configure a fresh repository

Start in this example directory. Keep the active configuration in a scratch
repository so this repository's integrations are unaffected:

```sh
ADOPTION_EXAMPLE_DIR="$PWD"
ADOPTION_REHEARSAL_DIR="$(mktemp -d)"
cp .mcp.json.example "$ADOPTION_REHEARSAL_DIR/.mcp.json"
cd "$ADOPTION_REHEARSAL_DIR"
git init
claude
```

Inspect the complete JSON and explain the `mcpServers` map, connection name,
transport, and endpoint. Approve the project server in the normal host
UI.

Invoke the `/mcp` slash command and work down through the menu
hierarchy to show the tool definitions for the Microsoft Learn server.
Fallback if the live session cannot connect: the lecture notes' Section 4.1
walks through the same five screens with screenshots from the 2026-11-17
instructor session (`../../slides/images/mcp-adoption-0*.png`).
 
If already in a session when adding the `.mcp.json` file,
exit and start a fresh session for a reproducible load. If unrelated integrations
can answer the same task, use an instructor scratch session with explicit config:

```sh
claude --strict-mcp-config --mcp-config .mcp.json
```

Explain that this isolates configured servers for rehearsal; it is not the basic
project-scoped configuration mechanism. Do not switch off permission controls.
Check host version and managed policy if the server is absent. Do not register
user-scoped servers merely to make an example appear.

## Student attempt and failure exercise

Alternate prompt:

> Use Microsoft Learn MCP documentation tools to find how Get-ChildItem can
> include hidden items. Cite the relevant documentation. Do not execute commands.

Record one actual invocation, a relevant result excerpt, citation, and your
reason for accepting or rejecting the answer. Use the evidence template.

In a disposable copy, change only the URL's path to `/api/mcp-lecture-invalid`.
Start a new scratch session and inspect the actual error. Classify whether the
failure occurs before discovery, restore the URL, and reconnect. Do not predict
a particular HTTP status: providers can redirect or change routing. For an
independent diagnosis, from the example directory run:

```sh
uv run --frozen python check_remote.py --endpoint https://learn.microsoft.com/api/mcp-lecture-invalid --output /tmp/adoption-invalid.json
```

A failed request should not produce a success report. If routing unexpectedly
succeeds, inspect what service answered rather than pretending the test failed.
The exact error text is provider/runtime dependent. Capture it with date and
remove account data; do not invent an exception to illustrate the expected lesson.

## LLM-free fallback

From this directory:

```sh
uv sync --locked
uv run --frozen python check_remote.py
```

Open `evidence/remote.json`. Point out discovery fields and the two actual argument
objects. Response lengths/hashes identify the captured bodies; only a short
excerpt is retained. The independent client intentionally requests both search
and fetch so both operations can be inspected. That is client code, not evidence
that a model chose either operation.

If the endpoint is down during class, inspect the saved capture and source URL;
label the activity recorded-evidence analysis. Defer the live student check or
pair students who have working access. Do not spend the class trying unrelated
servers or account changes. An external endpoint opening as an ordinary browser
page is not an MCP compatibility check.

## Music preview

Prepare the homework fixture beforehand using its setup guide. Show the music
graph and ask:

> Inspect the music schema, then show the five artist IDs and names with the
> largest distinct-playlist counts, breaking ties by artist ID.

Use actual query/call/results if the host is rehearsed. Otherwise show the
homework's `evidence/live.json`, explicitly LLM-free, and instructor CSV oracle.
Contrast the remote URL with a local MCP launch command and a separate running
database. Installation belongs to the homework checkpoint, not the preview.

## Before marking the host rehearsal complete

Record host/model versions, exact prompts, discovered tool names, actual calls,
results, final answer and source comparison. Inspect `/context` for loaded or
deferred tools without claiming every definition always enters every prompt.
The supplied session accounts for documentation use, but is not a raw host/API
export and does not include the music preview. Rehearse music separately and
record host versions/calls/results where available. Keep account data external.
