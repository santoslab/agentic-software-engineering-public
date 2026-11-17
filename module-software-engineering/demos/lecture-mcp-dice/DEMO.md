# Demonstration script and fallbacks

All relative commands below run from `demos/lecture-mcp-dice/`. Run `uv sync --locked` first.
Prepare terminals, the slide deck, `dice.py`, `dice_server.py`, and captured JSON.
Do not install packages during the 75-minute lecture.

## Opening: finished behavior (0–5 minutes)

Use the scratch host configuration below after authenticating Claude Code.
Exact prompt:

> Use the dice MCP tool to roll three six-sided dice once. Show each die and the
> total, then say whether the total is below, equal to, or above 12. Base the
> answer on the tool result; do not simulate a roll yourself.

Expand the host's tool invocation. Check `count=3`, `sides=6`, three outcomes in
1–6, their sum, and the comparison with 12. The comparison is model reasoning;
it is not a server field. Do not reroll to obtain a preferred result.

If the host is unavailable, display `evidence/protocol-E.json`: the captured roll
is `[2,4,5]`, total 11, below 12. These are actual protocol results, with the
comparison computed by the instructor; there is no captured model answer.

## A–C: ordinary program, adapter, wire

```sh
uv run --frozen python dice.py roll --count 3 --sides 6
uv run --frozen python protocol_demo.py --stage B --output evidence/protocol-B.json
```

Read the plain function first. Show the B branch's import, constructor, decorator,
parameters, description, and string return. Find the same fields in discovery.
Open `evidence/wire-B.jsonl`: read paired request/response IDs. The first request
is `server/discover`, followed by `tools/list`, then calls. Modern requests carry
protocol/client metadata. This capture has no `initialize` or
`notifications/initialized`; a legacy client can use a different compatibility
path. Do not hand-code a handshake for this SDK's client.

## D–E: validation, output, second tool

```sh
uv run --frozen python protocol_demo.py --stage D --output evidence/protocol-D.json
uv run --frozen python protocol_demo.py --stage E --output evidence/protocol-E.json
uv run --frozen pytest -q
```

Compare B `count=0` (`isError=false`, Error text) with D (`isError=true`, SDK
validation). `count="many"` fails SDK integer validation even in B. `sides=7`
passes the integer schema but fails the function's whitelist; D raises ToolError.
Show D's `outputSchema`, text JSON, and matching `structuredContent`.
For a JSON-RPC failure read the malformed `tools/call` test: missing tool name,
`error.code=-32602`, no `result`. These are different failure layers.

Second host prompt:

> Use dice MCP tools to roll two d20 and flip five coins. Show each returned
> outcome, the dice total, and both coin tallies. Do not substitute shell commands.

Expand both calls; check tallies against the H/T string and dice sum against the
individual dice. Record host/model versions, exact prompt, arguments, raw results,
and final answer before calling this an integration pass. A tool appearing in
`/mcp` alone does not verify tool selection or answer grounding.

## Inspector (independent of an LLM)

Node must satisfy the pinned Inspector's engine requirement (2.15.0:
`^22.23.4 || ^24.22.1 || >=26.12.1`). The generic web documentation's minimum
is less restrictive than this package's current engine declaration.

```sh
npx -y @modelcontextprotocol/inspector@2.15.0 --cli .venv/bin/python dice_server.py --method tools/list
npx -y @modelcontextprotocol/inspector@2.15.0 --cli .venv/bin/python dice_server.py --method tools/call --tool-name roll --tool-arg count=3 --tool-arg sides=6
npx -y @modelcontextprotocol/inspector@2.15.0 .venv/bin/python dice_server.py
```

In the web UI connect stdio, list tools, inspect both schemas, call valid and
invalid arguments, and inspect messages. Keep per-launch Inspector tokens out of
screenshots. Browser interaction is a manual rehearsal check; the SDK client is
the prepared fallback if Inspector startup fails.

## Scratch Claude Code setup

Use a separate empty directory and a supplied config for this session. No global
registration is needed. From the demo directory:

```sh
DICE_DEMO_DIR="$PWD"
DICE_REHEARSAL_DIR="$(mktemp -d)"
uv run --frozen python -c 'import json,pathlib,sys; p=pathlib.Path(sys.argv[1]); pathlib.Path(sys.argv[2]).write_text(json.dumps({"mcpServers":{"dice":{"type":"stdio","command":str(p/".venv/bin/python"),"args":[str(p/"dice_server.py")]}}}))' "$DICE_DEMO_DIR" "$DICE_REHEARSAL_DIR/dice.json"
cd "$DICE_REHEARSAL_DIR"
claude --strict-mcp-config --mcp-config dice.json
```

Authenticate beforehand using your normal Claude Code setup. Inspect `/mcp`,
then run both prompts above and inspect `/context` for loaded/deferred tools.
Approve tool execution in the ordinary host UI if requested. Save the evidence
only after removing account data. Exit the scratch session when finished.

For teaching registration separately, the documented project-scope form is:
`claude mcp add --transport stdio --scope project dice -- /absolute/path/to/.venv/bin/python /absolute/path/to/dice_server.py`.
This creates project configuration; use a scratch project. Local scope is stored
in the user's home config, despite its name. Neither form was registered here.

## Optional two-minute extension

Specify `roll_meets_target(count, sides, target)` with the same dice bounds and
an integer target in 1–400. Return rolls, total, target, and `meets = total >= target`.
Before implementation, propose one controlled valid case and invalid cases for
each bound. Require grounded answers. Do this only if time remains; it is not a
new assignment or a promise that a model will choose the correct tool.
