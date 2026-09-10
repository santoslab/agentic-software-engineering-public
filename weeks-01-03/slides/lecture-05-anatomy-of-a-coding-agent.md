---
marp: true
theme: default
size: 16:9
paginate: true
footer: 'Agentic Software Engineering · Lecture 5 · Harness Primitives'
style: |
  section {
    font-size: 26px;
    line-height: 1.35;
    padding: 44px 56px 60px;
  }
  h1, h2 { color: #310066; }
  h1 { font-size: 48px; }
  h2 { font-size: 36px; }
  pre { font-size: 21px; line-height: 1.28; }
  table { font-size: 23px; }
  th, td { padding: 8px 12px; }
  footer { font-size: 14px; bottom: 20px; }
  section.lead { background: #310066; color: #ffffff; }
  section.lead h1, section.lead h2 { color: #ffffff; }
  section.lead footer { color: #ddd1ef; }
  section.code-dense pre { font-size: 19px; }
  section.source {
    background: #090909;
    padding: 20px 60px 54px;
  }
  section.source p { margin: 0; line-height: 1; }
  section.source img {
    display: block;
    width: 1120px;
    height: 630px;
    object-fit: contain;
  }
  section.source footer, section.source footer a { color: #dfd5ec; }
  section.references { font-size: 23px; }
---

<!-- _class: lead -->

# Anatomy of a Coding Agent
## Harness Primitives

Agentic Software Engineering · Lecture 5
Week 3 · Meeting 1 of 2

An effective coding agent depends on engineering around the model:
what the model sees, how it acts, what bounds those actions,
and what survives afterward.

<!-- 0–8 min: motivation and vocabulary. This deck is authored from lecture-notes/lecture-05-anatomy-of-a-coding-agent.md. The taxonomy and the reproduced diagram slides are from The Carbon Layer's Harness Engineering Masterclass; today covers the first six primitives, through durable state. -->

---

## The problem the harness solves

Ask an LLM to fix a failing test in code that calculates shopping discounts.

- The model knows Python and common discount calculations.
  It does not know the contents of your `discount.py`.
  Someone must supply that information.
- If the model proposes an edit, someone must perform the edit.
- If you close the agent halfway through, something must preserve the work.

These responsibilities belong to the system around the model,
called the **harness**.

<!-- This is the recurring example for the whole lecture. Every primitive today is one of these responsibilities made explicit. -->

---

## Source material for this lecture

We follow the first six primitives in The Carbon Layer's
*Harness Engineering Masterclass*, through durable state.

- The repository includes a
  [local summary of the primitives](../../carbon-layer/harness-architecture-primitives.md)
  and the [video transcript](../../carbon-layer/harness-engineering-masterclass-transcript.md).
- Harness engineering is new: there is no generally accepted way to
  categorize harness features. This categorization is the best we have seen.
- It is backed by a complete, step-by-step Python implementation of a
  harness on [GitHub](https://github.com/thecarbonlayer/carbon), matching the video.

<!-- Video: https://www.youtube.com/watch?v=mQfTdNVCOB0 . The Carbon implementation is reference material; it is not the toy agent assigned in Exercise 4. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 1:01](https://youtu.be/mQfTdNVCOB0?t=61)' -->

![A model receives input and produces output](../../carbon-layer/02-model-inputs-outputs.png)

<!-- The model operates only on the input supplied to a call, using what it learned in training. Everything else on this slide's diagram has to be put there by the harness. -->

---

## What the model receives and returns

The model operates on the input supplied to a call, using what it
learned during training.

- The input can include instructions, conversation history, file
  contents, and tool descriptions. Assembling that input effectively
  is the harness's job.
- The output can contain ordinary text or structured requests for tools.
- The model does not execute the Python functions or shell commands
  those requests name.
- Missing project information can lead the model to guess. Good harness
  design gives it ways to obtain evidence or ask for clarification.

<!-- Emphasize the division: the model decides; execution happens elsewhere. Guessing under missing information is a harness-design problem as much as a model problem. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 2:39](https://youtu.be/mQfTdNVCOB0?t=159)' -->

![The runtime repeats observation, decision, and action](../../carbon-layer/03-ReAct-pattern.png)

<!-- Connect to the ReAct paper by Yao et al. from the earlier suggested reading. The cycle here is the same one students will implement in Exercise 4. -->

---

## The runtime cycle

The runtime repeats a cycle:

1. Give the model the current context.
2. Receive a decision.
3. Execute any permitted tool requests.
4. Return the observations for another decision.

Yao et al. first proposed this approach and named the cycle **ReAct**:
an interleaving of reasoning and action.

The visible record contains requests and results. It is not a complete
account of the model's internal reasoning.

<!-- The ReAct paper was suggested reading in an earlier lecture. The last point matters when students later read verbose logs: the log is evidence about interactions, not the model's full internal state. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 3:30](https://youtu.be/mQfTdNVCOB0?t=210)' -->

![Model, runtime, and harness have different responsibilities](../../carbon-layer/04-ReAct-separation.png)

<!-- Three names for three responsibilities. In real code they need not be three modules. -->

---

## Three responsibilities, not necessarily three modules

- The **model** produces decisions and responses.
- The **runtime** drives the repeated interaction.
- The **harness** supplies context, tools, boundaries, and continuity
  around the model.

In actual code, these responsibilities need not be separate modules.
Exercise 4 puts much of the harness and runtime into one Python file.

<!-- The vocabulary is for analysis. When something goes wrong later in the course, the question will be which responsibility failed, regardless of which file implements it. -->

---

## How this lecture uses Exercise 4

Exercise 4 starts with a chat bot and supplies code that you add in
stages. You are expected to understand, assemble, and experiment with
that code — not to invent a coding agent unaided.

For each addition, ask: what could the program do before?
What can it do now? Which lines caused that change?

- The toy uses OpenCode Zen with the **Chat Completions** message
  format: `tool_calls` and `role: "tool"` messages, not Anthropic's
  `tool_use` blocks. Claude Code shows the same architecture with
  different implementation and API details.
- The running example is the three-file checkout project:
  `cart.py`, `discount.py`, and `test_checkout.py`. You ask the agent
  to fix the discount bug; you run `pytest` yourself.

<!-- Code excerpts in this deck come from the exercise and its starter (exercise-04-starter/toy_agent.py); comments may be omitted and lines wrapped for presentation. -->

---

## The six primitives covered today

| Primitive | Responsibility |
|---|---|
| Instructions | Establish how the agent should work |
| Context delivery | Bring the actual task into view |
| Context management | Keep the current input useful |
| Tool interfaces | Turn requests into operations and feedback |
| Execution environments | Enforce the boundaries of action |
| Durable state | Preserve progress beyond current attention |

For each: why it is needed, how Claude Code provides it,
how the toy implements it, and where the toy stops.

<!-- This four-part structure repeats for every primitive. The later, dimmed primitives visible in the source images (orchestration and beyond) are outside today's scope. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 3:45](https://youtu.be/mQfTdNVCOB0?t=225)' -->

![Instructions establish recurring expectations](../../carbon-layer/05-Instructions.png)

<!-- 8–14 min: instructions. -->

---

## Instructions: why this primitive is needed

A request to fix a bug leaves many choices open:

- the architecture of the project,
- the primary technologies and tools used,
- preferences for documenting tests and summarizing test results.

Instructions establish recurring expectations so the user does not
need to restate them every turn.

<!-- Instructions are the standing part of the context; the user's prompt supplies the particular task. -->

---

## Instructions in Claude Code

- Claude Code's system prompt, which we cannot see directly,
  is "Instructions" in this categorization.
- The most visible form is project guidance: `CLAUDE.md` files and
  rules under `.claude/rules/`. Claude Code loads applicable guidance
  into context.
- These files can specify conventions and test commands, but their text
  is guidance, not an access-control mechanism. To keep Claude Code
  out of other projects or away from certain tools, use its
  permissions and sandboxing features.
- Other harnesses use names such as `AGENTS.md`. Claude Code does not
  treat `AGENTS.md` as `CLAUDE.md` without an import or other setup.

<!-- Documentation: https://code.claude.com/docs/en/memory . The guidance-versus-enforcement distinction returns in the execution-environment section. -->

---

## Instructions in the toy agent

Step 2 provides this prompt skeleton:

```python
SYSTEM = """You are ...

Follow these rules while working.
- Always read a file before you write or edit it.
- ...
"""
```

The starter makes it the first conversation message:

```python
messages = [{"role": "system", "content": SYSTEM}]
```

Changing `SYSTEM` changes the instructions the model receives when a
new conversation starts. It does not change which Python functions
exist or which paths they can access.

<!-- The exercise's stylistic experiments make the distinction observable: a pirate-voice prompt changes responses, not filesystem permissions. -->

---

## Instructions: limits and a possible extension

- Instructions influence the model's choices; they do not guarantee a
  particular tool sequence. One run may show no behavioral difference.
- Exercise question: identify an instruction whose effect you could
  observe in a log.
- **Toy limit:** it does not discover or automatically load repository
  instruction files.
- **Possible extension:** read a project instruction file (for example,
  an `AGENTS.md` in the sandbox) at startup and add it to the initial
  context.

<!-- Extensions named in this deck are ideas for reasoning about the design, not additional Exercise 4 requirements. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 5:17](https://youtu.be/mQfTdNVCOB0?t=317)' -->

![Instructions cannot discover the project facts they refer to](../../carbon-layer/06-context-delivery.png)

<!-- Transition. An instruction to follow the project's discount policy cannot reveal that policy. The model needs the actual requirements and code, which is context delivery. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 6:15](https://youtu.be/mQfTdNVCOB0?t=375)' -->

![Context delivery supplies relevant files and other evidence](../../carbon-layer/07-context-delivery-02.png)

<!-- 14–21 min: context delivery. -->

---

## Context delivery: why this primitive is needed

Suppose tool calls have not been added yet. Then the only material
that reaches the model comes from the instructions and what you type
in the conversation.

To make the model understand a particular file, you would have to
type or paste its contents into the dialog.

Context delivery is the harness's job of assembling the model's input
from a variety of sources. The conversation text is only one of them.
This primitive gives the developer additional, controlled ways to
build the context.

<!-- The general idea is broad (the harness assembles input from many sources); the concrete illustration at this point in the course is developer-controlled file inclusion. -->

---

## File inclusion in Claude Code: the `@` mechanism

```text
Explain @discount.py alongside @test_checkout.py
```

- The harness inserts the contents of the referenced files into the
  context. This is not a tool call; it works like an include that the
  harness processes on your behalf.
- The distinction is who decides. With `@filename`, the developer
  pushes the content into context. With a file-reading tool (covered
  under tool interfaces), the model pulls content in by its own decision.
- Referencing a directory supplies a listing, not every file's contents.

<!-- Documentation: https://code.claude.com/docs/en/common-workflows#reference-files-and-directories . Mentioning a filename in prose usually leads the model to issue a read tool call instead; the @ form bypasses that decision. -->

---

## Delivery policy is a harness decision

For an include mechanism, the harness must define:

- which marker syntax counts as a reference,
- how injected blocks are labeled,
- where they appear relative to the question,
- how large they may be.

The `@` syntax is a convention selected by Claude Code.

**Toy limit:** no `@file` handling and no repository search.
**Possible extensions:** expand explicit file references (after the
same path checks), or add a focused search tool. A test-running tool
could return failures directly, but executing code raises the
execution-environment concerns covered later.

<!-- Transition: context delivery answers how information reaches the model. With a large repository or a long session, we must also choose how much information, and which information, belongs in the context now. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 7:02](https://youtu.be/mQfTdNVCOB0?t=422)' -->

![Unselected context can become too large or distracting](../../carbon-layer/08-context-management.png)

<!-- 21–29 min: context management. -->

---

## Context management: why this primitive is needed

The model's context window is finite. On a large project it will
eventually fill up. What then?

- Clear the entire context and start over?
- Replace the context with a summary? Then what determines what
  the summary keeps?

Problems appear even before the window is full:

- Reading an entire session log to find one failure spends context
  on irrelevant lines.
- Keeping an early, incorrect hypothesis in every request can
  distract the model from newer evidence.

Material that fits in the window is not necessarily useful for the
next decision.

<!-- Two separate problems: capacity (the window fills) and relevance (what is present may not help). Both cost money as well as quality; Lecture 6 quantifies the costs. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 8:14](https://youtu.be/mQfTdNVCOB0?t=494)' -->

![Context management selects, ranks, compresses, and assembles input](../../carbon-layer/09-context-management-02.png)

<!-- The mechanisms: retrieval, ranking, bounding, summarization, assembly. -->

---

## What context management does

Context management chooses what enters the current request:

- retrieve relevant material and rank candidate results,
- bound the size of outputs,
- summarize older exchanges,
- assemble an input that retains the current task and constraints.

Three related terms, kept distinct:

- **Retrieval-augmented generation (RAG)** is one approach to finding
  external material for a request. Not every agent needs it.
- **Compaction** replaces detail with a shorter account and can lose
  information.
- **Prompt caching** reduces repeated processing cost. It does not
  remove irrelevant content or make the window larger.

<!-- Students often conflate caching with filtering; the last bullet is there to prevent that. -->

---

## Context management in Claude Code

- `/context` reports context usage.
- `/compact` requests compaction; the harness also compacts
  automatically as needed.
- The purpose is to make room for continued work.
- A summary can omit details, so a resumed line of reasoning may
  require reading the source files again.

<!-- Documentation: https://code.claude.com/docs/en/how-claude-code-works#the-context-window -->

---

## Context management in the toy: accumulation only

After Step 5, each request includes this payload fragment:

```python
json={"model": MODEL, "messages": messages, "tools": tools},
```

- Step 6 keeps appending assistant messages and tool results. Every
  request resends the growing list, plus the tool schemas.
- This works for a small checkout project. For a large log or repeated
  file reads, the toy has no policy for reducing what it resends.
- A file read is a snapshot: an old result does not update when the
  file on disk changes.
- Step 7's `MAX_TURNS` counts model calls during one interaction. It
  prevents an endless tool loop, but it does not bound the size of a
  tool result, the accumulated history, or the monetary cost.

<!-- The append mechanism admits a useful source read and a huge unrelated log alike; the toy delivers context without judging its value. -->

---

## Context management: limits and a possible extension

**Possible extension:** a command similar to `/compact`, or an
automated preparation step before `call_zen`:

- preserve standing instructions and the current task,
- limit large tool outputs, with explicit truncation notices,
- summarize older completed exchanges.

Two constraints on any such mechanism:

- Keep a tool request and its required results together; arbitrary
  message deletion can leave an invalid conversation.
- Summaries should preserve unresolved questions and point back to
  files that can be reread.

<!-- This is an extension idea, not Exercise 4 work. Lecture 6 develops the cost and context tradeoffs. Transition: useful context supports a decision, but to change the checkout code the model needs a structured way to request an action. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 10:46](https://youtu.be/mQfTdNVCOB0?t=646)' -->

![Tool interfaces let the model request structured actions](../../carbon-layer/11-tool-interface.png)

<!-- 29–39 min: tool interfaces. This is the largest block; most of the Exercise 4 code lives here. -->

---

## Tool interfaces: why this primitive is needed

So far the agent can hold a conversation, follow instructions, and
answer questions about files the harness injects. Everything it
produces is still prose. A reply saying "change the discount
calculation" does not edit a file.

The tool interface closes the loop that makes the system an agent:

1. The model returns structured tool calls.
2. The harness executes them and appends each result to the conversation.
3. The harness calls the model again, until it produces a final answer.

A tool interface names an operation, describes when and how to use it,
and specifies its arguments. The request, the execution, and the result
are separate events that we can inspect when something fails.

<!-- Before this primitive the system can only talk about changes; after it, the system can make them. The inspectability point pays off in the verbose-mode work in Exercise 4. -->

---

## A tool is a function plus a schema

In harness engineering, a "tool" is a function paired with a schema:
a plain Python callable plus a JSON-schema contract that names it,
describes it, and types its parameters.

- Tool specifications live in a **registry**.
- Every registered tool is presented to the model in a protocol the
  model is trained on and obeys.
- The harness uses the registry to do two jobs: call the correct tool
  function for each request from the model (parsing the JSON arguments
  the model wrote into Python parameters), and return the function's
  string output into the context.

**In Claude Code:** built-in tools cover file operations, search, and
shell execution. MCP can expose additional tools through connected
servers; it is an interface mechanism, not a grant of unlimited authority.

<!-- Documentation: https://code.claude.com/docs/en/how-claude-code-works#tools and https://code.claude.com/docs/en/mcp -->

---

<!-- _class: code-dense -->

## The schema: declaring the operation to the model (Step 5)

```python
READ_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Get the full contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "The path of the file to read",
                },
            },
            "required": ["file_name"],
        },
    },
}
```

The name identifies the tool. The description helps the model decide
when to use it. `parameters` tells the model how to format the JSON
arguments, which the harness will parse into actual parameters.

<!-- This is Python data describing the tool in the format sent to the API. The model receives this metadata; it never receives the function itself. -->

---

## The registry: what the model sees, what the harness keeps

With only a read tool, the toy's registry is:

```python
TOOLS_DICTIONARY = {"read_file": read_file}
TOOLS_SCHEMA = [READ_FILE_SCHEMA]
```

- `TOOLS_SCHEMA` is sent to the model as data. It says which tools are
  available, what each one does, and how to format a call as JSON.
- `TOOLS_DICTIONARY` stays in the harness. It maps the string
  identifier from the model (`"read_file"`) to the Python function to
  call (`read_file`).

<!-- Two structures, two recipients. The model can only request; the harness resolves and executes. -->

---

## The agentic loop (Step 6)

```python
def agentic_loop(messages: list) -> None:
    while True:
        message = call_zen(messages, TOOLS_SCHEMA)
        messages.append(message)
        if message.get("content"):
            print(message["content"])

        tool_calls = message.get("tool_calls")
        if not tool_calls:
            break
```

- Appending the response keeps the assistant's request in history.
- Printing content is independent of handling tool calls: a response
  can contain tool requests even when there is no text to print.
- A response with no tool calls ends this inner loop; the outer chat
  loop can then accept another user prompt. Stopping is not evidence
  that the task was done correctly.

<!-- Comments omitted from the supplied code. This is the intermediate version; Step 7 adds the required turn cap. -->

---

<!-- _class: code-dense -->

## Dispatch: executing each requested call (Step 6)

```python
for tc in tool_calls:
    name = tc["function"]["name"]
    raw_arguments = tc["function"].get("arguments") or "{}"

    if name not in TOOLS_DICTIONARY:
        result = f"ERROR: unknown tool: {name} - available: {list(TOOLS_DICTIONARY)}"
    else:
        try:
            result = TOOLS_DICTIONARY[name](**json.loads(raw_arguments))
        except Exception as e:
            result = f"ERROR: {name} failed: {type(e).__name__}: {e}"
    messages.append({"role": "tool", "tool_call_id": tc["id"], "content": str(result)})
```

An unknown tool gets an explicit result. Malformed argument JSON,
unexpected keyword arguments, and exceptions from the function become
readable errors. This does not handle every failure of the program:
an HTTP error in `call_zen` occurs elsewhere.

<!-- json.loads turns the argument string into a dictionary; ** passes its entries as keyword arguments. Errors are results too, so the model receives evidence for its next decision. -->

---

## One request, followed all the way around

1. The model requests `read_file` with ID `call_1` and arguments
   encoded as the string `{"file_name":"discount.py"}`.
2. `json.loads` turns the string into a dictionary; `**` passes its
   entries as keyword arguments to `read_file`.
3. The function reads the permitted file.
4. The harness appends the result with `tool_call_id` equal to `call_1`.
5. On the next iteration, the model receives both its request and the
   matching result, and can decide what to do next.

<!-- An illustrative trace, not a recorded run. Step 9's verbose mode prints tool names, arguments, and results so students can watch this happen. -->

---

## Four protocol details that matter

1. Keep the returned assistant message rather than rebuilding it from
   just `content`. Rebuilding can lose tool calls and omit fields some
   providers require, such as `reasoning_content` for certain
   thinking models.
2. Supply a result for every requested call, including rejected or
   unknown tools. Otherwise the next API request can contain an
   incomplete tool exchange.
3. Match each result using `tool_call_id`, not its position in a list.
4. Give actionable feedback. "File not found" and an empty file should
   not look the same. Step 4's suggested error improvement adds a
   directory listing, so the model has evidence for another choice.

<!-- These are the four places where student implementations most often go subtly wrong. Each one produces confusing failures several turns later, not at the point of the mistake. -->

---

## Tool interfaces: stages in the toy, and limits

- Step 5 can produce a tool request that nothing executes.
- Step 6 executes the request and returns the observation.
- Step 8 adds `list_files` and `write_file` (or `edit_file`),
  enabling discovery and editing.
- Step 9's verbose mode prints tool names, arguments, and results.
  It does not print every API payload or expose internal reasoning.

**Toy limit:** filesystem tools only; no Bash tool and no MCP.
Adding either would be an interesting extension.

<!-- Students run pytest themselves; test output does not automatically enter the toy's context. -->

---

## Once the agent can act, it needs guardrails

Guardrails are mechanisms built into the harness to control unwanted
actions by the model. Two are needed as soon as tools exist:

- An **approval gate that fails closed** for boundary-crossing tools:
  a tool call that violates the configured permissions does not run
  unless the user explicitly confirms it.
- A **minimal sandbox**: a defined area of the file system that the
  agent is allowed to touch, so that a `bash` tool never runs directly
  against your host shell.

The next primitive is where such boundaries are enforced.

<!-- The distinction from instructions: guardrails hold even when the model requests the wrong thing. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 12:20](https://youtu.be/mQfTdNVCOB0?t=739)' -->

![Execution environments bound what tool actions can affect](../../carbon-layer/13-execution-environment.png)

<!-- 39–47 min: execution environments. -->

---

## Execution environments: why this primitive is needed

A syntactically valid `write_file` request could still name a file
outside the exercise project.

The harness must decide where tools run and what they may read,
write, or contact.

This is different from asking the model to be careful: the
restrictions must hold even when the model requests the wrong thing.

<!-- Guidance shapes behavior; enforcement bounds it. Both are needed. -->

---

## Execution boundaries in Claude Code

- The working directory where you launch Claude Code establishes the
  project context.
- Permission controls determine whether a tool call is allowed or
  needs approval.
- When configured, the sandboxed Bash tool applies operating-system
  restrictions to filesystem and network access, for commands and
  their child processes.
- Permissions and sandboxing serve different roles. A Git worktree
  separates working files but does not by itself restrict a process's
  access to the rest of the machine.

<!-- Documentation: https://code.claude.com/docs/en/sandboxing#how-sandboxing-relates-to-permissions-and-permission-modes -->

---

<!-- _class: code-dense -->

## The toy's sandbox helper (Step 3)

```python
from pathlib import Path

SANDBOX_DIR = (Path(__file__).resolve().parent / "sandbox").resolve()
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)

def resolve_in_sandbox(file_name: str) -> Path:
    resolved = (SANDBOX_DIR / file_name).resolve()
    if not resolved.is_relative_to(SANDBOX_DIR):
        raise ValueError(f"path escapes the sandbox: {file_name}")
    return resolved
```

- The sandbox is a directory next to the running script. `resolve()`
  normalizes the candidate path, including `..` and existing symlinks.
- `is_relative_to` checks path containment, not string prefixes.
  An outside path raises `ValueError`; an allowed path is returned.

<!-- Complete supplied helper, comments omitted. __file__ anchors the sandbox to the script's location, not the shell's current directory. Joining root and name constructs a candidate; only the resolve-and-check confines access. mkdir creates the directory if necessary. -->

---

## The check constrains only the operations that use it

- Step 4's read and Step 8's write skeleton both call
  `resolve_in_sandbox` before touching a file. The dispatcher turns a
  rejected path into an error result for the model.
- A helper that nobody calls constrains nothing. Every file operation
  must go through it.

| Requested path | Outcome |
|---|---|
| `discount.py` | Resolves inside the sandbox; the operation may proceed |
| `../../secrets.txt` | Rejected before any file I/O |

- A permitted path can still fail for ordinary reasons, such as a
  missing file.
- The restriction is enforced by Python even if the model asks to
  ignore its instructions.

<!-- Ask students what is constrained if Step 3 is added but the tools never call the helper. Answer: nothing about file access. -->

---

## Execution environments: what the helper does not do

The helper checks paths passed to these filesystem functions. It does
not:

- isolate the Python process or restrict network access,
- remove credentials from the environment,
- safely confine arbitrary executed code,
- defend against filesystem changes between checking and using a path.

Adding a shell or test runner expands the boundary: even `pytest`
executes project code. A future version would need restricted process
execution, filesystem and network policy, controlled credentials,
timeouts, and appropriate approval decisions. A command allowlist
alone does not supply all of that.

<!-- Transition: what happens if the agent is interrupted? Nothing so far records what was accomplished and what remains. That calls for durable state. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 14:16](https://youtu.be/mQfTdNVCOB0?t=856)' -->

![Durable state keeps artifacts and progress outside the current context](../../carbon-layer/15-durable-state.png)

<!-- 47–55 min: durable state, the last primitive today. -->

---

## Durable state: why this primitive is needed

An agent might edit `discount.py`, record a hypothesis, and stop
before testing. To continue later, it needs the changed file and an
account of what remains uncertain.

- Progress stored outside the active conversation survives process
  exit and can be inspected by another person or agent.
- Examples: source files, plans, diffs, test logs, saved sessions,
  memory notes.
- Persistence does not make a claim correct: a note saying "tests
  passed" is only as good as the evidence behind it.
- Durable state also enables handoffs: from one agent to another, or
  between different models within the same agent. This will grow in
  importance as agentic software engineering matures.

<!-- The handoff point is worth stating explicitly; it previews the multi-agent material later in the course. -->

---

## Durable state in Claude Code

- Conversation history is saved locally and can be reopened with
  `claude --continue` or `claude --resume`. This differs from starting
  a fresh session.
- `CLAUDE.md` and auto-memory notes provide persistent information for
  later sessions. They serve a different purpose from replaying a
  whole conversation.
- A plan file or a Git diff also makes work inspectable outside the
  active context.

<!-- Documentation: https://code.claude.com/docs/en/how-claude-code-works#work-with-sessions and https://code.claude.com/docs/en/memory -->

---

## What survives restarting the toy?

| State | Survives? | How would the model receive it? |
|---|---|---|
| `messages` list | No | Would require a new save/load mechanism |
| Hardcoded `SYSTEM` in the script | Yes | Inserted into messages at startup |
| Edited files in `sandbox/` | Yes | A new tool read delivers current contents |
| Logs copied by the student | Yes | Supplied by the student; not auto-loaded |
| Next steps mentioned only in chat | No | Would need to be saved and delivered |

Each startup runs the initialization again; there is no
`load_session`:

```python
messages = [{"role": "system", "content": SYSTEM}]
```

<!-- The toy is partial, not absent: Step 8's write changes real files, and Part 2 has students copy verbose output and test results into log files. Those survive; the conversation and its reasoning do not. -->

---

## Storage, retrieval, and current context are different things

If the agent writes the fix and you exit: the edit remains, but the
new conversation has no record of why the edit was made or whether the
tests were run.

**Possible extension:** save the conversation and a task identifier
after completed interactions, and keep a small task-summary file with
the goal, changes, evidence, and unfinished work. Save to a temporary
file and replace the prior save only when complete, to reduce the risk
of a half-written session file.

Recovery needs an explicit boundary: a tool might write a file and the
process might stop before recording the result. On recovery, inspect
the actual files and pending operations before repeating effects.
Saving a transcript is not a transaction across the transcript and the
filesystem.

<!-- Three ideas that are easy to conflate: what is stored, what is retrieved, and what is currently in context. The table on the previous slide separates them concretely. -->

---

## The primitives connect

- Durable state keeps a plan or log available.
- Context delivery brings it back into the model's input.
- Context management chooses the relevant portion.

That is why one file may participate in several primitives.

State preserves work, but it does not decide when to retry or which
step should execute next. The Carbon Layer calls that responsibility
**orchestration** — beyond today's scope.

<!-- Keep this short; orchestration and subagents come later in the course. -->

---

<!-- _class: lead -->

## Demonstration: identify the responsibilities

While watching the Claude Code demonstration, identify the evidence
for each responsibility:

the instructions supplied · the information delivered
the context retained · the tool action and its result
the boundary that constrained it · the progress that was saved

The demo works this lecture's checkout micro-task. Its project files
and script are in the repository under `demos/lecture-05-claude-code-demo/`
— recreate it yourself after class.

<!-- Demo segments follow demos/lecture-05-claude-code-demo/demo-script.md: run them interleaved after each primitive's block, or consecutively at 55–70 min. Rehearse beforehand and capture the fallback screenshots at the script's marked points. -->

---

## Check your understanding

1. The model suggests a generic discount fix without reading the
   project. What information is missing, and how could it enter the
   next request?
2. Every request contains a huge obsolete log. Which primitive should
   decide what to retain? Why does a 25-turn cap not solve this?
3. A file tool rejects `../../secrets.txt`. Which code enforces the
   boundary, and which code tells the model about the rejection?
4. The agent edits a file and exits. On restart, what survives, what
   is missing, and what would be needed to continue confidently?

<!-- 70–75 min: synthesis. These map to context delivery, context management, execution environment plus tool feedback, and durable state. A single successful checkout run can involve all six primitives; the diagnostic question when something fails is which harness responsibility was missing or inadequate, alongside questions about model capability. -->

---

## Exercise 4: due at the start of week 4

Work through the additions manually, following the exercise's
restriction on coding-agent assistance.

- Predict the effect of each supplied chunk, add it, run the suggested
  interaction, and explain what changed.
- Complete the indicated prompt, tools, turn cap, and reflection
  portions.
- Use verbose logs for both micro-tasks; run the tests yourself and
  record the results.
- The reflection asks for two Claude Code capabilities your toy lacks,
  and where you would add them.

Extensions discussed in this lecture are examples for reasoning,
not extra implementation requirements.

**Before next lecture:** Project 0 will be given at the end of the
next lecture.

<!-- Launch the unchanged exercise. The toy's limited context management and session persistence are exactly where the reflection questions point. -->

---

<!-- _class: references -->

## Sources and attribution

The primitive sequence and the reproduced slide images are from The Carbon Layer's
[*Harness Engineering Masterclass*](https://www.youtube.com/watch?v=mQfTdNVCOB0); each image slide links to the relevant moment.
They are third-party images, not newly authored course diagrams — see the repository's
[licensing notes](../../LICENSING.md). The dimmed later primitives in the images are outside this lecture.

[Local primitive summary](../../carbon-layer/harness-architecture-primitives.md) · [Transcript](../../carbon-layer/harness-engineering-masterclass-transcript.md) ·
[Lecture notes](../lecture-notes/lecture-05-anatomy-of-a-coding-agent.md) · [Exercise 4](../exercises/exercise-04-toy-agent.md) · [Demo](../demos/lecture-05-claude-code-demo/demo-script.md)

The local `ch-*.md` files describe a separate, more extensive staged implementation;
they are not the toy assigned in Exercise 4. Code excerpts are from the exercise and
its starter, with comments omitted and lines wrapped for presentation.

Claude Code references: [memory and instructions](https://code.claude.com/docs/en/memory), [file references](https://code.claude.com/docs/en/common-workflows#reference-files-and-directories),
[tools, context, and sessions](https://code.claude.com/docs/en/how-claude-code-works), [sandboxing](https://code.claude.com/docs/en/sandboxing), [MCP](https://code.claude.com/docs/en/mcp) — checked September 8, 2026.
Product commands and configuration can change; the architectural responsibilities
provide the stable comparison.
