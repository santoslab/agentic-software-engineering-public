# Chapter 5 — Tools: the model requests actions, the harness executes them

Through ch-04 the agent can hold a conversation, obey an instruction layer, and answer questions about files the harness injects with `@path` — but everything it produces is still prose. This stage closes the loop that makes it an agent: the model returns structured tool calls, the harness executes them, appends each result to the conversation, and calls the model again until it produces a final answer. Folded into the same primitive are the two guardrails that make action tolerable: an approval gate that fails closed for boundary-crossing tools, and a minimal sandbox so `bash` never runs on your host shell.

## The primitive

A tool is a function plus a schema — a plain Python callable paired with a JSON-schema contract that names it, describes it, and types its parameters. The tools live in a registry with exactly two jobs: render every registered tool into the wire-format specs the model is shown (`specs()`), and dispatch an incoming call by name (`call(name, arguments)`), parsing the JSON arguments and returning a string result.

What this unlocks is the agentic loop. Until now, `send()` was one model call: assemble the payload, get text, return it. Now each turn may take several round trips: the harness sends the conversation *plus the tool specs*; if the model answers with tool calls instead of text, the harness runs them, appends the raw results to the conversation, and calls the model again — which now sees what its actions produced and can keep going. The model can compute instead of guess, write files, run code, and build on each result.

The reason this primitive must live in the harness is almost definitional. A model cannot execute anything; a "tool call" is just tokens shaped like JSON. Something outside the model has to decide which tools exist, whether a given request will be honored, where it runs, and what the model sees afterward — and all four of those are policy. The module docstring in [tools.py](../stages/ch-05-tools/harness/tools.py) frames tools as "an API surface you expose to a model: keep the list small, keep each contract narrow, and validate arguments." The split that the whole chapter turns on: the model decides *what* to do; the harness decides *how* — and whether — and is the only thing that ever runs anything.

## From the video

The walkthrough opens the chapter at [11:16](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=676s) by taking stock: the agent holds a conversation, follows instructions from the system prompt or `AGENTS.md`, and can read a file via the `@` symbol — "but notice it is still only talking." It can describe a fix; it cannot make one. Tools are what change that.

The definition is deliberately deflationary. At [11:56](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=716s): "It's just a function plus a schema. That's it." The registry in `tools.py` hands the model the specs and dispatches each call by name — and then the sentence that names the design split, at [12:07](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=727s): "The model decides what to call, but the harness decides how and then actually runs it." The loop itself is described as simple — send with the tool specs, and if the model reaches for a tool, run it, hand back the result, and go again — with the harness "capping it at six steps so that it doesn't spin forever."

Then the guardrails, briskly: file tools are scoped to a workspace the agent owns — a scratch dir for now, so an experiment can't touch your real repository — and bash doesn't run on your shell but in a sandbox the harness controls, Docker if it's there or a local subprocess if not. The dangerous stuff must ask for permission: the calculator runs free, but bash and file writes hit an approval gate, and if nobody is wired up to approve, "it just fails and says no." Approvals are scarce on purpose. The demo shows both faces: asked for a multiplication, the model reaches for the calculator instead of guessing and comes back exact; asked to write a file, it pauses at the gate for a y/N. The chapter closes at [13:54](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=834s) with the whole shape in one line — "The model asks, the harness decides, and the dangerous stuff waits for a human" — and a warning that sets up ch-06: every one of those calls and results is landing in the same conversation, and that conversation has a limit.

## The code

The diff touches four harness modules and adds a test episode plus acceptance checks. The `model/`
package does not change: `chat()` has accepted a `tools` parameter, and `LLMResponse` has contained
a `tool_calls` field, since chapter 1
([model/client.py](../stages/ch-05-tools/model/client.py)). Chapter 5 is the first stage whose agent
supplies and consumes those values.

### The `Tool` contract and `ToolRegistry`

Start in [harness/tools.py](../stages/ch-05-tools/harness/tools.py), which is new. A tool is a
dataclass:

```python
@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    func: Callable[..., str]
```

The four fields separate model-facing metadata from executable behavior. `name` is both the model's
selection key and the registry lookup key. `description` helps the model choose. `parameters` is a
JSON Schema dictionary advertised to the provider. `func` is the Python callable the harness will
invoke. The registry does not validate arguments against `parameters`; it relies on the model/API
to produce a suitable object and on the callable invocation to reject mismatches.

The registry interface is:

| Interface | Input | Return/state | Failure behavior |
|---|---|---|---|
| `ToolRegistry()` | None. | Creates an empty name → tool dictionary. | No external work. |
| `register(tool)` | A `Tool`. | Stores it under `tool.name`; returns `None`. | A duplicate name silently replaces the previous registration. |
| `specs()` | None. | Returns a new list of OpenAI-shaped function specifications in insertion order. | Does not validate the schemas. |
| `call(name, arguments)` | Tool name and a JSON string, with `""` treated as `{}`. | Calls `func(**args)` and converts the result to `str`. | Unknown name, malformed JSON, bad argument shape, and any callable exception become `error:` strings. |
| `len(registry)` | Python's built-in `len(...)` protocol. | Number of currently registered names. | No side effects. |

`ToolRegistry.specs()` wraps each one as
`{"type": "function", "function": {...}}` — the OpenAI tool-spec shape compatible endpoints
expect — and `call()` is the dispatch side, with a convention worth internalizing: operational
errors become a *string result* rather than escaping through the agent loop.

```python
    def call(self, name: str, arguments: str) -> str:
        tool = self._tools.get(name)
        if tool is None:
            return f"error: unknown tool {name!r}"
        try:
            args = json.loads(arguments) if arguments else {}
        except json.JSONDecodeError:
            return f"error: could not parse arguments {arguments!r}"
        try:
            return str(tool.func(**args))
        except Exception as exc:  # noqa: BLE001 — tool errors are fed back to the model
            return f"error: {exc}"
```

`json.loads()` parses JSON text into Python values. For the expected string
`{"expression":"47 * 89"}`, it returns a dictionary; `tool.func(**args)` then expands that
dictionary into keyword arguments, equivalent to `tool.func(expression="47 * 89")`. Valid JSON of
the wrong shape is not caught by the parsing block: a list, number, or wrongly keyed dictionary
fails during `**args` or the function call, and the broader second `except` turns that failure into
an error string. This is parsing plus runtime rejection, not full schema validation.

The broad `except Exception` is localized at the tool boundary. Calls made directly to
`calculator()` or `read_file()` can still raise; calls through the registry are normalized for the
model to read.

### Built-in tools and arithmetic evaluation

`default_tools()` registers two starters: `calculator`, which evaluates arithmetic by walking a
parsed abstract syntax tree (AST) against a whitelist of operators — model-authored input never
reaches `eval` — and `read_file`, which returns a file's contents or an error string. The nested
`ev(node)` function recursively evaluates only numeric constants, allowed binary operations, and
unary minus. Unsupported syntax raises `ValueError`; division by zero and extreme arithmetic can
raise their ordinary Python errors, all of which the registry converts to text.

`read_file` is deliberately unscoped here (it can read any path the process can); the docstring
flags that confining it is “the execution-environment concern of ch-08.” Its schema calls the file
UTF-8, but `Path.read_text()` actually uses the platform default encoding because no explicit
encoding is passed.

### Agent construction and the bounded tool loop

[harness/agent.py](../stages/ch-05-tools/harness/agent.py) grows three constructor parameters —
`tools` (a registry), `approve` (a callback), and `approval_required` (a set of tool names) — and
`DEFAULT_SYSTEM` gains a nudge: “Use tools when they help.”

| New constructor input | Default | Stored meaning |
|---|---|---|
| `tools: ToolRegistry | None` | `None` | No specs are advertised, and returned tool calls cannot be executed. |
| `approve: Callable[[str, str], bool] | None` | `None` | Callback receives a tool name and raw JSON arguments. Absence means a gated tool is denied. |
| `approval_required: set[str] | None` | `None` | Names requiring the callback. `None` and an empty set both become a new empty set. |

`send()` still does the ch-04 work, injecting `@path` context and appending the user turn, but
instead of one `chat()` call it now ends in `_run()`:

```python
    def _run(self) -> str:
        """Drive the model, executing tool calls until it produces a final answer."""
        specs = self.tools.specs() if self.tools else None
        for _ in range(MAX_TOOL_STEPS):
            resp = chat(self._payload(), model=self.model, tools=specs, provider=self.provider)
            if resp.tool_calls and self.tools is not None:
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": resp.content or "",
                        "tool_calls": resp.tool_calls,
                    }
                )
```

### Tool-loop execution trace

For a response that requests a calculator call and then supplies a final answer, the control flow
is:

1. Render the tool specs once for the turn.
2. Each iteration re-sends the full payload — system head plus the entire history — with the specs attached.
3. If the reply carries tool calls (and a registry is wired), the assistant turn is recorded *with its `tool_calls`* first; the wire format requires the request to precede its results in the transcript.
4. Each call is then executed — through the approval gate if its name is in `approval_required` — and its string result is appended as a `role: "tool"` message tagged with the `tool_call_id` it answers.
5. `continue`: the next `chat()` sees its own requests and their results, and decides what to do next.
6. A reply with no tool calls is the final answer — append it and return.
7. If `MAX_TOOL_STEPS` (six) iterations pass without one, give up with `"error: exceeded tool-step budget"`.

The budget counts **model responses**, not individual tool calls. One response can contain several
tool calls; all of them run before the next iteration. The final budget error is returned but not
appended as an assistant message, so callers see it while the retained history ends at the most
recent tool results. Model-client exceptions still propagate because `_run()` does not catch them.

If a response contains `tool_calls` while `self.tools is None`, the condition is false and the
response is treated as a final assistant reply. This fallback preserves the one-call behavior but
discards the requested actions; the normal path avoids it by advertising no specs when no registry
exists.

Steps 4–7 in the source:

```python
                for tc in resp.tool_calls:
                    fn = tc.get("function", {})
                    name = fn.get("name", "")
                    args = fn.get("arguments", "")
                    # A boundary-crossing tool must clear the approval gate first.
                    if name in self.approval_required and not self._approved(name, args):
                        result = "[denied by approval gate]"
                    else:
                        result = self.tools.call(name, args)
                    self.messages.append(
                        {"role": "tool", "tool_call_id": tc.get("id", ""), "content": result}
                    )
                continue
            self.messages.append({"role": "assistant", "content": resp.content})
            return resp.content
        return "error: exceeded tool-step budget"
```

The gate itself is three lines, and the important one is the fallback:

```python
    def _approved(self, name: str, args: str) -> bool:
        # Fail closed: a tool marked as requiring approval with no approver is denied.
        return self.approve(name, args) if self.approve else False
```

A gated tool with no approver wired is denied, never run. Denial is not an exception either —
`[denied by approval gate]` goes back to the model as an ordinary tool result, so it knows the
action was refused and can report that instead of hallucinating success. If the approval callback
itself raises, the exception propagates; the fail-closed rule covers absence and false results, not
a broken callback.

### Workspace tool factories and closures

[harness/workspace.py](../stages/ch-05-tools/harness/workspace.py) has existed since ch-03 as a
path-confined directory class; now that there is a tool interface, it grows `write_file_tool(ws)`
and `edit_file_tool(ws)` — factories that retain a `Workspace` so every model-supplied path is
funneled through the confinement check:

```python
    def _safe(self, path: str) -> Path:
        p = (self.root / path).resolve()
        if p != self.root and self.root not in p.parents:
            raise ValueError(f"path escapes workspace: {path}")
        return p
```

Each factory returns a `Tool` whose `func` is a bound method such as `ws.write`. A bound method
retains the particular `ws` object even after the factory returns. `bash_tool` below uses the same
idea with a nested function: `run_bash` closes over both `sandbox` and `workdir`. These **closures**
turn configuration supplied once during wiring into behavior that needs only model-facing
arguments at call time.

Files written this way persist across calls, which matters for the next piece. Workspace methods
return their expected model-facing failures as strings, while path escape still raises
`ValueError`; the registry converts that exception to the same `error:` channel.

### The `Sandbox` execution seam

[harness/sandbox.py](../stages/ch-05-tools/harness/sandbox.py) is new: all shell execution is routed
through `Sandbox.run()`.

| Interface | Inputs and defaults | Return | Failure behavior |
|---|---|---|---|
| `Sandbox(image="busybox", timeout=15.0, prefer_docker=True)` | Container image, per-command seconds, and backend preference. | Stores configuration and an initially unknown cached Docker status. | Does not probe Docker until first use. |
| `run(command, workdir=None)` | Shell string and optional persistent directory. | `SandboxResult(stdout, stderr, exit_code, backend)`. | Docker unavailability selects local; execution timeout or process-start errors propagate to the registry. |
| `bash_tool(sandbox, workdir=None)` | A configured sandbox and optional workspace. | A `Tool` whose result begins `[exit N via backend]`. | The registry converts raised sandbox errors to `error:` strings. |

`Sandbox.run()` probes for a Docker daemon once (and caches the result), preferring Docker when
available and otherwise using a local subprocess. The Docker path is a temporary `busybox`
container:

```python
    def _run_docker(self, command: str, workdir: str | None) -> SandboxResult:
        work = ["-v", f"{workdir}:/work"] if workdir else ["--tmpfs", "/work:rw,size=16m"]
        argv = [
            "docker", "run", "--rm",
            *work,
            "-w", "/work",
            self.image,
            "sh", "-c", command,
        ]  # fmt: skip
```

`bash_tool(sandbox, workdir=...)` wraps this as a tool whose result is `[exit N via docker]` (or `via local`) plus the captured output — the model only ever sees text. The `workdir` parameter is the workspace seam: pass the workspace root and commands run there (bind-mounted at `/work` under Docker, as the cwd locally), so a `bash` command can see the file `write_file` just created. The REPL `main()` wires exactly that composition, plus a console approver:

`subprocess.run(...)` starts a child process and waits for it. Unlike chapter 0's
`subprocess.call`, `capture_output=True` retains stdout and stderr, `text=True` decodes them into
strings, `cwd=...` chooses the child's current directory, and `timeout=...` raises if it runs too
long. The command is deliberately passed to `sh -c` or `bash -c`, so shell syntax in the
model-authored string is interpreted. The outer Docker argument list is not shell-parsed; only the
string after `-c` is.

### Runtime composition in the REPL

```python
    workspace = Workspace()
    tools = default_tools()
    tools.register(write_file_tool(workspace))
    tools.register(edit_file_tool(workspace))
    tools.register(bash_tool(Sandbox(), workdir=str(workspace.root)))

    def approve(name: str, args: str) -> bool:
        return input(f"  approve {name}({args})? [y/N] ").strip().lower() in ("y", "yes")

    agent = Agent(
        system=DEFAULT_SYSTEM,
        tools=tools,
        approve=approve,
        approval_required={"bash", "write_file", "edit_file"},
    )
```

### Offline tests and live acceptance evidence

[tests/episodes/test_ch05.py](../stages/ch-05-tools/tests/episodes/test_ch05.py) is the verify-gate
side: it scripts the model by patching `chat` with an iterator of `LLMResponse` objects — first a
tool call, then a final answer — so the loop runs deterministically offline. `next(responses)`
advances the iterator one scripted response at a time; too many model calls would raise
`StopIteration` and fail the test rather than silently pass.

The approval gate gets a four-way matrix: denied → the function never executes and `[denied`
appears in a tool message; approved → it executes; no approver at all → fails closed; not in
`approval_required` → runs freely without consulting the approver. Workspace tests cover the
write/read/edit round trip, the `../escape.py` `ValueError`, and `bash` reading a file the workspace
wrote.

The accept gate in [tasks/checks.py](../stages/ch-05-tools/tasks/checks.py) checks three behaviors
against a real model: `_accept_ch05_tools` requires the reply to contain 4183 *and* a
`role: "tool"` message in history (so a direct textual answer alone does not pass);
`_accept_ch05_approval` wires a deny-everything approver, asks for `echo SHOULD_NOT_RUN`, and asserts
the gate was consulted and the denial recorded; `_accept_ch05_fileedit` has the agent create
`hello.py` in its workspace and run it with `python3`, asserting the file exists on disk and
`WORKSPACE_OK` came back through a tool result. The live checks demonstrate model selection of the
advertised tools; the offline tests supply exact branch and non-execution evidence.

## Design decisions & gotchas

- **The chapter-1 interface already contains the required fields.** No `model/` file changes in this stage because `chat()` already accepts `tools` and `LLMResponse` already contains `tool_calls`. Chapter 5 changes how the harness supplies and processes those fields. This demonstrates the compatibility benefit—and chapter-1 comprehension cost—of introducing the fields before their first use.
- **Fail closed, and report denial to the model.** The default answer to a gated call is no; an unwired approver means denied, not "run it this once." The denial is appended as a tool result rather than raised as an exception, so the model can respond to the refusal. The tests check denied, approved, missing-approver, and ungated cases.
- **Errors are strings across the tool boundary.** Unknown tool, malformed JSON, a raised exception — all become `error: ...` strings the model can read and recover from. The broad `except Exception` in `ToolRegistry.call` (with its `noqa` justification) is deliberate: a tool exception escaping into `_run` would kill the whole turn instead of giving the model a chance to retry.
- **The step budget bounds the loop, not the side effects.** When six iterations expire, `_run` returns an error string — but the tool calls from earlier iterations already ran, and their results sit in history. A budget prevents spinning; it is not a transaction.
- **Wire-format ordering is required by the provider API.** The assistant message carrying `tool_calls` must precede the `role: "tool"` results with matching `tool_call_id`s, and its `content` must be a string (`resp.content or ""`). Reversing the order or omitting the identifiers causes an OpenAI-compatible endpoint to reject the next payload.
- **Scoping is asymmetric, on purpose.** Writes and edits are confined by `Workspace._safe`; `read_file` can still read any path on the host. At this stage the approval gate is the only thing between the model and your filesystem for reads. Closing that is explicitly deferred to ch-08.
- **The sandbox call is centralized, but not yet strongly isolated.** The local fallback runs `bash` on the host in a scratch working directory with the inherited environment; the Docker path keeps default networking and runs as root. Chapter 8 adds no-network, non-root, and environment-scrubbing policies. `busybox` has no `python3`, so the workspace acceptance check explicitly sets `prefer_docker=False` to exercise the local backend.
- **Everything lands in messages.** Every iteration re-sends the entire history, and every tool result grows it. Tool use is exactly what turns context from a convenience into a budget — the problem ch-06 exists to solve.

## Study pointers

Read the stage in this order:

1. [harness/tools.py](../stages/ch-05-tools/harness/tools.py) — the `Tool` contract, the registry, the error-string convention, the two starter tools.
2. [harness/agent.py](../stages/ch-05-tools/harness/agent.py) — `_run()` top to bottom, then `main()` for how a real deployment wires tools, workspace, sandbox, and approver together.
3. [harness/workspace.py](../stages/ch-05-tools/harness/workspace.py) — `_safe` and the two tool factories.
4. [harness/sandbox.py](../stages/ch-05-tools/harness/sandbox.py) — the Docker/local split and the `workdir` seam.
5. [tests/episodes/test_ch05.py](../stages/ch-05-tools/tests/episodes/test_ch05.py) — how to test an agent loop offline by scripting `chat`.
6. [tasks/checks.py](../stages/ch-05-tools/tasks/checks.py) — the three ch-05 acceptance checks.

Things to try: `uv run verify` is fully offline; the demo, accept check, and REPL need LM Studio (or any OpenAI-compatible endpoint) serving a local model. Run `uv run agent` and ask for an awkward multiplication, then ask it to write a file and answer `n` at the prompt — watch `[denied by approval gate]` come back and see how the model reports the refusal. Then register a tool of your own in `main()` and watch the model discover it from nothing but the spec.

Previous: [ch-04 — context delivery](ch-04-context-delivery.md) · Next: [ch-06 — context management](ch-06-context-management.md)

Later chapters lean directly on this primitive: ch-08 hardens the sandbox and scopes the file tools, ch-12 has the agent verify its own code through these same tools, ch-13 traces every tool call as a span, and ch-14 turns the console `y/N` into a TUI approval modal.
