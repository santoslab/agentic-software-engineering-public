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

What the model sees. How it acts.
What bounds those actions. What survives afterward.

<!-- 0–8 min: foundation. The taxonomy and source images are from The Carbon Layer's Harness Engineering Masterclass. Cover the first six primitives only. -->

---

## Learn by adding one chunk at a time

Exercise 4 supplies code for you to understand and assemble.

**Predict → add → observe → explain**

For every chunk: what changed in the agent's behavior, and why?

Our recurring example: fix the checkout discount bug using
`cart.py`, `discount.py`, and `test_checkout.py`.

The toy uses **Chat Completions through OpenCode Zen**.
Students run the tests themselves.

<!-- We may quote any supplied exercise code. Students are not expected to invent the implementation without it. Keep the indicated student-authored portions as exercise work. The discount project is an explanatory example; the live-demo scenario is still to be selected. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 1:01](https://youtu.be/mQfTdNVCOB0?t=61)' -->

![A model receives input and produces output](../../carbon-layer/02-model-inputs-outputs.png)

<!-- A model knows training patterns and supplied input; the current repository is not automatically inside that input. Missing information can lead to guesses, or the model can ask for it. Tool requests are structured outputs; the model does not execute functions. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 2:39](https://youtu.be/mQfTdNVCOB0?t=159)' -->

![The runtime repeats observation decision and action](../../carbon-layer/03-ReAct-pattern.png)

<!-- Connect to prior lectures: current context, model response, tool request, execution, observation, another model call. This is a conceptual ReAct loop; visible tool logs are not the model's complete internal reasoning. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 3:30](https://youtu.be/mQfTdNVCOB0?t=210)' -->

![Model runtime and harness are distinct responsibilities](../../carbon-layer/04-ReAct-separation.png)

<!-- The model produces responses and decisions. The runtime drives the loop. The harness supplies context, actions, boundaries, continuity. One Python file can implement several responsibilities. -->

---

## Six responsibilities around the loop

| Primitive | The question it answers |
|---|---|
| Instructions | How should the agent work? |
| Context delivery | How does task information reach the model? |
| Context management | What belongs in the current request? |
| Tool interfaces | How can the model request an operation? |
| Execution environments | Where can that operation act? |
| Durable state | What survives beyond current attention? |

A working vocabulary from The Carbon Layer; responsibilities overlap.

<!-- Explain the lecture's recurring structure: purpose, Claude Code, toy code, limitation, possible extension. Later dimmed primitives in the source images are outside today's scope. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 3:45](https://youtu.be/mQfTdNVCOB0?t=225)' -->

![Instructions establish recurring expectations](../../carbon-layer/05-Instructions.png)

<!-- 8–14 min: instructions, including transition to context delivery. Why needed: a request to fix a bug leaves operating choices open. Standing guidance avoids repeating project conventions and expectations. -->

---

## Instructions: Claude Code and the toy

**Claude Code:** `CLAUDE.md` and applicable project rules.

**Toy, Step 2:** supplied prompt skeleton; you complete the guidance.

```python
SYSTEM = """You are ...

Follow these rules while working.
- Always read a file before you write or edit it.
- ...
"""
```

The starter includes it in every request's conversation:

```python
messages = [{"role": "system", "content": SYSTEM}]
```

<!-- Source: exercise Step 2 and starter. Claude reference: https://code.claude.com/docs/en/memory . The harness loads applicable guidance; it is not enforced configuration. Claude Code does not automatically load AGENTS.md by name without an import or other setup. -->

---

## Instructions change guidance, not authority

Before: a generic assistant prompt.
After: task-specific expectations, such as reading before editing.

An instruction can influence the next tool choice.
It cannot create a tool or enforce a filesystem boundary.

**Toy limit:** no automatic project-instruction loading.
**Possible extension:** read an instruction file at startup.

**Predict:** does a pirate-style system prompt change which files
Python can access?

<!-- Answer: no. The stylistic experiment changes model input. Behavior is probabilistic; a single comparison need not show a difference. The extension is a discussion idea, not added assignment work. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 5:17](https://youtu.be/mQfTdNVCOB0?t=317)' -->

![Instructions cannot discover project facts by themselves](../../carbon-layer/06-context-delivery.png)

<!-- Quick transition. Follow the project's discount policy is guidance; it does not deliver the policy, tests, or implementation. We need context delivery. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 6:15](https://youtu.be/mQfTdNVCOB0?t=375)' -->

![Context delivery brings the actual task into view](../../carbon-layer/07-context-delivery-02.png)

<!-- 14–21 min: context delivery. Access to files does not mean they are already in the model's input. A filename alone is not file contents. -->

---

## A Python function can obtain the file

**Provided in Step 4:**

```python
def read_file(file_name: str) -> str:
    path = resolve_in_sandbox(file_name)
    if not path.is_file():
        return f"ERROR: file not found: {file_name}"
    return path.read_text()
```

Check the path, check that a file exists, return text or an error.

This code obtains information locally.
How does that information reach the next model call?

<!-- The sandbox helper is supplied in Step 3 and explained later in this lecture. Defining this function alone does not make model-directed reading work: declaration and dispatch are still needed. -->

---

## Delivery finishes when the result enters context

**Provided in Step 6** (line-wrapped):

```python
messages.append({
    "role": "tool",
    "tool_call_id": tc["id"],
    "content": str(result),
})
```

File on disk → Python result → message → next model call.

Step 8's `list_files` lets the model discover names before reading.

**Predict:** if the tool reads a file but we omit this append,
does the model receive the contents?

<!-- Answer: no. Both request and response are needed in the next API payload. Merely printing a tool result in the terminal is not delivery to the model. We will return to the call ID under tool interfaces. -->

---

## Context delivery: Claude Code and the toy

**Claude Code:** explicit references such as
`Explain @discount.py alongside @test_checkout.py`,
plus file reads, searches, and command output.

**Toy:** user messages and returned file contents/listings.
Students run `pytest`; its output is not automatically supplied.

**Toy limit:** no special `@file` expansion or repository search.
**Possible extension:** expand checked file references or add search.

More available context creates a new question: **what matters now?**

<!-- Claude source: https://code.claude.com/docs/en/common-workflows#reference-files-and-directories . A directory reference gives a listing, not all contents. Check understanding: a generic fix without project reads points to missing context delivery. A future test tool could deliver failure output, but execution needs additional boundaries. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 7:02](https://youtu.be/mQfTdNVCOB0?t=422)' -->

![Unselected context can become too large or distracting](../../carbon-layer/08-context-management.png)

<!-- 21–29 min: context management. A full log, an obsolete hypothesis, and repeated source snapshots can all enter through the same delivery mechanism. Fitting in the context window does not make them useful. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 8:14](https://youtu.be/mQfTdNVCOB0?t=494)' -->

![Context management selects ranks compresses and assembles](../../carbon-layer/09-context-management-02.png)

<!-- Selection, retrieval/ranking, output limits, summarization, compaction. RAG retrieves external material for input; it is not mandatory for an agent. The source vocabulary includes prompt caching: distinguish processing cost reduction from relevance filtering. -->

---

## The toy keeps accumulating context

**Step 5 request payload fragment:**

```python
json={"model": MODEL, "messages": messages, "tools": tools},
```

Step 6 appends responses and tool results to `messages`.
Every new request sends the growing history and tool schemas.

A useful source read and a huge unrelated log both get appended.
An old file result remains an old snapshot after an edit.

**Step 7's turn cap limits calls, not context size.**

<!-- MAX_TURNS applies within one user interaction. One result can already be huge; history persists across interactions. It is not a complete spend cap either. Ask whether 25 calls solves a huge obsolete log: no. -->

---

## Context management: Claude Code and the toy

**Claude Code:** `/context` shows usage; `/compact` and automatic
compaction make room by reducing conversation detail.

**Tradeoff:** a shorter summary can lose something needed later.

**Toy limit:** no compaction or context budget.
**Possible extension, before `call_zen`:** preserve the task and rules,
bound large outputs, summarize older completed exchanges.

Keep tool requests and their required results together.
Caching can reduce processing costs; it does not filter context.

<!-- Source: https://code.claude.com/docs/en/how-claude-code-works#the-context-window . Explicitly flag the extension as unimplemented. Do not imply deleting arbitrary old messages is safe. Lecture 6 returns to costs and compaction tradeoffs. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 10:46](https://youtu.be/mQfTdNVCOB0?t=646)' -->

![Tools give the model structured ways to request action](../../carbon-layer/11-tool-interface.png)

<!-- 29–39 min: tools. Useful context enables a decision, but writing I fixed it does not edit a file. We need a declared operation, local implementation, dispatch, and feedback. -->

---

<!-- _class: code-dense -->

## Step 5: declare the operation to the model

```python
READ_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Get the full contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string",
                              "description": "The path of the file to read"},
            },
            "required": ["file_name"],
        },
    },
}
```

The description guides selection; the parameters describe arguments.

<!-- Provided schema, reformatted. The model receives metadata, not the Python function. A better description could explain relative paths and when to read; schema metadata does not replace runtime checks. -->

---

## Two registrations, two different jobs

**Provided in Step 5:**

```python
TOOLS_SCHEMA = [READ_FILE_SCHEMA]
TOOLS_DICTIONARY = {"read_file": read_file}
```

| Structure | Where it goes | What it does |
|---|---|---|
| `TOOLS_SCHEMA` | API request | Advertises tools to the model |
| `TOOLS_DICTIONARY` | Stays in Python | Maps a requested name to a function |

Before dispatch exists, the model can request a read,
but the program does not execute it or return its result.

<!-- The model does not see our dictionary of function objects. Adding only one registration is incomplete. Step 5's empty printed reply may actually be a tool request in another field. -->

---

## Step 6: keep going while tools are requested

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

Provided opening, comments omitted. Dispatch follows inside the loop.
**Intermediate stage:** Step 7 adds the required turn cap.

<!-- The inner loop stops on no tool calls; the outer REPL can accept another prompt. Preserve the full assistant message, including requests and provider-required fields. Printed text and tool requests are separate. Stopping is not proof of correctness. -->

---

<!-- _class: code-dense -->

## Step 6: dispatch and return an observation

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

Provided code, comments omitted. Errors become usable results too.

<!-- Trace JSON text to dictionary, then keyword arguments via **, then the function call. This catches malformed arguments and tool exceptions; it is not a catch-all for HTTP errors in call_zen. Each requested call gets a result, even when unknown or rejected. -->

---

## Follow one complete exchange

1. Model requests `read_file`, ID `call_1`, with arguments
   `{"file_name":"discount.py"}` encoded as a string.
2. Harness parses the arguments and finds the Python function.
3. Function checks the path and returns the file contents.
4. Harness appends a tool result with `tool_call_id: "call_1"`.
5. Next model call receives the request **and** the observation.

Match by ID. Answer every call. Preserve the assistant message.

Step 9's verbose mode shows tool names, arguments, and results.

<!-- Illustrative trace, not a recorded run. Some providers require extra assistant fields, e.g. reasoning_content, so do not rebuild the assistant dict using content alone. Verbose mode is evidence about interactions, not complete internal cognition. -->

---

## Tool interfaces: Claude Code and the toy

**Claude Code:** file/search tools, Bash, and connected MCP tools.

**Toy:** `read_file`, `list_files`, and `write_file` (or `edit_file`).
Adding the latter tools enables discovery and actual edits.

**Toy limit:** no command runner or MCP connection.
**Possible extension:** add a declaration and implementation,
return useful results, and define the new operation's boundaries.

A valid tool request still leaves a question: **where may it act?**

<!-- Sources: https://code.claude.com/docs/en/how-claude-code-works#tools and https://code.claude.com/docs/en/mcp . MCP is an interface mechanism, not automatic authority. Students run pytest themselves in the base exercise. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 12:20](https://youtu.be/mQfTdNVCOB0?t=739)' -->

![Execution environments bound what actions can affect](../../carbon-layer/13-execution-environment.png)

<!-- 39–47 min: execution environments. A syntactically valid write request could target the wrong file. The execution layer must enforce scope even if instructions are ignored. -->

---

## Step 3: the supplied sandbox setup and helper

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

Anchor next to the script. Resolve. Check containment. Return or reject.

<!-- Complete supplied executable code, comments omitted. __file__ anchors to script location, not shell CWD. Joining alone is insufficient. resolve normalizes .. and existing symlinks; is_relative_to is path containment, not a string prefix. -->

---

## The check works only when tools use it

**Step 4's read and Step 8's write skeleton both start with:**

```python
path = resolve_in_sandbox(file_name)
```

| Requested path | Outcome |
|---|---|
| `discount.py` | Inside sandbox; file operation may proceed |
| `../../secrets.txt` | Outside sandbox; raises before file I/O |

Step 6 catches the exception and delivers an error result.

**Predict:** what is constrained if we define the helper but never call it?

<!-- Answer: nothing about file access. Adding Step 3 creates the directory but the check must be on every tool path. Windows C:/... is generally relative on macOS/Linux; do not use it as a portable absolute-path example. Valid containment does not guarantee file existence or successful I/O. -->

---

## Execution environments: Claude Code and the toy

**Claude Code:** working directory, permission decisions, and a
configured Bash sandbox that restricts filesystem/network access.

**Toy: partial.** The helper checks its filesystem-tool arguments.
It does not isolate Python or constrain arbitrary child processes.

**Possible extension:** a test runner needs process, filesystem,
network, credential, timeout, and approval boundaries.

Even `pytest` executes project code.
A worktree separates files; it is not an OS sandbox.

<!-- Source: https://code.claude.com/docs/en/sandboxing . Distinguish permissions before a tool call from OS restrictions while sandboxed Bash and its children run. The toy helper is not hardened against concurrent path changes. A command allowlist alone does not constrain everything an allowed program can do. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 14:16](https://youtu.be/mQfTdNVCOB0?t=856)' -->

![Durable state preserves progress beyond current attention](../../carbon-layer/15-durable-state.png)

<!-- 47–55 min: durable state. An execution environment is a place to work, but tasks can stop and resume. Distinguish artifacts and progress records from a current prompt. This is the final primitive today. -->

---

## What survives a restart of the toy?

| State | Survives? | Available to the next conversation? |
|---|---|---|
| In-memory `messages` | No | No session loader exists |
| `SYSTEM` in the script | Yes | Inserted again at startup |
| Edited sandbox files | Yes | After the model requests new reads |
| Manually copied logs | Yes | Only if supplied again |
| Next steps only in chat | No | Must first be saved somewhere |

Startup creates a new list:

```python
messages = [{"role": "system", "content": SYSTEM}]
```

<!-- Steps 8 and Part 2 already provide partial durable state: actual files and manually saved logs. Do not say that all state dies with the process. The model does not automatically see saved files. -->

---

## Durable state: Claude Code and the toy

**Claude Code:** saved sessions with `claude --continue` / `--resume`,
persistent instructions and memory notes, plans, and Git changes.

**Toy: partial.** Files survive; conversation save/load is absent.

**Possible extension:** save completed interactions, load a selected
session, and keep a task summary with evidence and next steps.

If a process stops after an edit but before saving the result,
inspect actual files before repeating the operation.

<!-- Sources: https://code.claude.com/docs/en/how-claude-code-works#work-with-sessions and https://code.claude.com/docs/en/memory . A fresh session is different from resuming. Persistence alone is not crash-safe transactional recovery or proof that saved claims are true. -->

---

## Stored, retrieved, and in context are different

A saved plan can participate in three responsibilities:

| Responsibility | What happens to the plan |
|---|---|
| Durable state | Keeps the plan outside the running conversation |
| Context delivery | Reads it into a later request |
| Context management | Selects the parts needed for the current task |

Saving the next step does not schedule or execute that step.
That leads to **orchestration**, beyond today's scope.

<!-- Ask the restart question: a fix remains on disk, but neither the reason nor test status is automatically recovered. Students should name the missing state and the mechanism to deliver it. -->

---

<!-- _class: lead -->

## Claude Code: observe the harness

Which instructions and facts were supplied?
What context was retained or summarized?
Which tool acted, and what came back?
What enforced its boundary?
What progress will survive?

<!-- 55–70 min: 15-minute demo block reserved. Scenario and script are intentionally deferred to the next instructor discussion. These are observation prompts, not an approved live sequence. Later prepare a rehearsal record and static fallback. -->

---

## Diagnose the missing responsibility

| What you observe | Where to investigate |
|---|---|
| Generic fix; no project files read | Context delivery |
| A huge obsolete log in every request | Context management |
| Outside path rejected before a read | Execution boundary and error feedback |
| Files survive, but the task history is gone | Durable state and retrieval |

Ask **which harness responsibility was missing or inadequate**,
alongside questions about model capability.

<!-- 70–75 min: synthesis and exercise handoff. These scenarios are reviewed within the earlier blocks; use this as a quick recap rather than four new discussions. Instructions could encourage reading, but cannot substitute for missing facts. -->

---

## Exercise 4: understand each addition

Use the provided code. Complete the indicated portions manually,
following the exercise's restriction on coding-agent assistance.

**Predict → add → observe → explain**

Complete both micro-tasks; save verbose logs and manual test results.
Reflect on two Claude Code capabilities the toy lacks,
and point to where each could be added.

Extensions from this lecture are discussion ideas, not extra work.
**Due: start of week 4.**

<!-- Launch the unchanged exercise. The required turn cap and path boundary remain graded. Refer to current starter/setup for model access; no shared Anthropic key or price promise. -->

---

## Before Lecture 6

[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

[Agentic Development Principles](../student-repo/handouts/handout-agentic-principles.md)

[NautilusTRX pass retrospectives](../student-repo/handouts/handout-nautilustrx-retrospectives.md)

Project 0 kickoff: end of this week.

Next: context costs, compaction tradeoffs, memory, and verification.

<!-- Reading reminder; finish within the 70–75 minute close. -->

---

<!-- _class: references -->

## Sources and companion material

The Carbon Layer, [Harness Engineering Masterclass](https://www.youtube.com/watch?v=mQfTdNVCOB0),
opening through Durable state (approximately 0:00–16:00).
The eleven source images retain their third-party provenance.

[Local primitive summary](../../carbon-layer/harness-architecture-primitives.md) ·
[Transcript](../../carbon-layer/harness-engineering-masterclass-transcript.md) ·
[Lecture notes](../lecture-notes/lecture-05-anatomy-of-a-coding-agent.md) ·
[Exercise 4](../exercises/exercise-04-toy-agent.md)

Claude Code: [instructions/memory](https://code.claude.com/docs/en/memory),
[file references](https://code.claude.com/docs/en/common-workflows#reference-files-and-directories),
[tools/context/sessions](https://code.claude.com/docs/en/how-claude-code-works),
[sandboxing](https://code.claude.com/docs/en/sandboxing),
[MCP](https://code.claude.com/docs/en/mcp). Checked September 8, 2026.

<!-- Reference slide, not an additional timed teaching block. Local ch-*.md files describe a different implementation from the assigned toy. Code excerpts are from the exercise/starter, with only presentation reformatting and omitted comments. -->
