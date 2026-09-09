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

<!-- The harness assembles effective input from instructions, history, files, and tool metadata. A model knows training patterns and supplied input; the current repository is not automatically inside that input. Missing information can lead to guesses, or the model can ask for it. Tool requests are structured outputs; the model does not execute functions. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 2:39](https://youtu.be/mQfTdNVCOB0?t=159)' -->

![The runtime repeats observation decision and action](../../carbon-layer/03-ReAct-pattern.png)

<!-- Recall Yao et al.'s ReAct paper from the earlier suggested reading (see ../reading-list.md). The harness assembles input and executes requests. Connect to prior lectures: current context, model response, tool request, execution, observation, another model call. This is a conceptual ReAct loop; visible tool logs are not the model's complete internal reasoning. -->

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

The Carbon Layer vocabulary has a [staged Python implementation](https://github.com/thecarbonlayer/carbon).

<!-- The field has no generally accepted taxonomy; this is the course's chosen vocabulary. The Carbon implementation is additional reference, not the assigned toy. Explain the lecture's recurring structure: purpose, Claude Code, toy code, limitation, possible extension. Later dimmed primitives in the source images are outside today's scope. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 3:45](https://youtu.be/mQfTdNVCOB0?t=225)' -->

![Instructions establish recurring expectations](../../carbon-layer/05-Instructions.png)

<!-- 8–14 min: instructions, including transition to context delivery. Why needed: a request to fix a bug leaves operating choices open. Standing guidance avoids repeating project conventions and expectations. -->

---

## Instructions: establish recurring expectations

**Purpose:** supply standing guidance and project knowledge
so the developer does not repeat them for every task.

Examples: project architecture, technologies and tools,
test-documentation conventions, and how to summarize results.

In Claude Code, system instructions and project guidance
such as `CLAUDE.md` serve this purpose.

Instructions guide choices; permissions and sandboxing enforce limits.

<!-- Begin with why this primitive is needed. Follow the revised notes' general operating guidance rather than describing instructions as the particular bug-fix task. -->

---

## Instructions: Claude Code and the toy

**Claude Code:** system instructions, `CLAUDE.md`, and project rules.

**Toy, Step 2:** supplied skeleton for general operating guidance.

```python
SYSTEM = """You are ...

Follow these rules while working.
- Always read a file before you write or edit it.
- ...
"""
```

The starter includes it in the conversation sent to the model:

```python
messages = [{"role": "system", "content": SYSTEM}]
```

<!-- Source: exercise Step 2 and starter. Claude reference: https://code.claude.com/docs/en/memory . Distinguish the harness's system instructions from user-visible project instructions. Claude Code does not automatically load AGENTS.md by name without an import or other setup. -->

---

## Instructions guide recurring behavior

Before: a generic assistant prompt.
After: general operating guidance, such as reading before editing.

These expectations apply across tasks; the current user prompt
supplies the particular task.

**Toy limit:** no automatic project-instruction loading.
**Possible extension:** load an `AGENTS.md` from the sandbox at startup.

**Predict:** does a pirate-style system prompt change which files
Python can access?

<!-- Answer: no. Instructions influence choices, while permissions and sandboxing enforce authority. One run need not show a behavioral difference. The extension is a discussion idea, not added assignment work. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 5:17](https://youtu.be/mQfTdNVCOB0?t=317)' -->

![Instructions cannot discover project facts by themselves](../../carbon-layer/06-context-delivery.png)

<!-- Quick transition. Follow the project's discount policy is guidance; it does not deliver the policy, tests, or implementation. We need context delivery. -->

---

## Context delivery: bring task material into the input

**Purpose:** assemble relevant input from sources beyond standing
instructions and the text the developer types.

Before tools, how could the model inspect a file?
The developer could paste it—or ask the harness to include it.

**Developer push:** `@file` selects content for the harness to inject.
**Model pull:** later, the model can request a file-reading tool.

<!-- Brief transition into the 14–21 minute context-delivery block. The same information may arrive through either route, but who initiates delivery differs. This is a conceptual build-up, not the order of steps in Exercise 4. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 6:15](https://youtu.be/mQfTdNVCOB0?t=375)' -->

![Context delivery brings the actual task into view](../../carbon-layer/07-context-delivery-02.png)

<!-- 14–21 min: context delivery. Access to files does not mean they are already in the model's input. A filename alone is not file contents. -->

---

## Context delivery: include the file contents

**Purpose:** give the model relevant material without requiring
the developer to paste it or the model to request a tool.

In Claude Code:

```text
Explain @discount.py alongside @test_checkout.py
```

The harness expands the references and inserts the file contents.
This works like an **include**, chosen by the developer.

A plain filename mentions a file; `@filename` requests its inclusion.

<!-- First course slide after Carbon image 07 begins with purpose. Source: https://code.claude.com/docs/en/common-workflows#reference-files-and-directories . File inclusion does not require a model-selected tool call. A directory reference supplies a listing, not every file's contents. -->

---

## Delivery policy belongs to the harness

For an include mechanism, the harness must decide:

- Which marker syntax identifies a reference?
- How are injected contents labeled?
- Where do they appear relative to the question?
- How much content may be included?

**Toy limit:** no special `@file` handling.
**Possible extension:** expand references before calling the model,
check their paths, and label and bound the inserted content.

<!-- This section follows the revised notes: developer-controlled injection is the example before tools are introduced. The toy still receives typed user messages; it simply lacks an include mechanism. Search or test-running tools are further extensions considered later. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 7:02](https://youtu.be/mQfTdNVCOB0?t=422)' -->

![Unselected context can become too large or distracting](../../carbon-layer/08-context-management.png)

<!-- 21–29 min: context management. A full log, an obsolete hypothesis, and repeated source snapshots can all enter through the same delivery mechanism. Fitting in the context window does not make them useful. -->

---

## Context management: handle a finite window

**Purpose:** keep useful context available as the conversation grows,
without filling the model's input with obsolete or irrelevant material.

When the window fills, possible responses include:

- **Clear:** start again and supply the necessary context.
- **Summarize:** retain a shorter account, with possible information loss.

What must the summary preserve?
What should be excluded even before the window is full?

<!-- Purpose first after Carbon image 08. Follow the notes' capacity problem before the selection mechanisms in image 09. Preserve the current goal, constraints, evidence, and unresolved questions. Compaction can lose details; source files may need to be reread. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 8:14](https://youtu.be/mQfTdNVCOB0?t=494)' -->

![Context management selects ranks compresses and assembles](../../carbon-layer/09-context-management-02.png)

<!-- Selection, retrieval/ranking, output limits, summarization, compaction. RAG retrieves external material for input; it is not mandatory for an agent. The source vocabulary includes prompt caching: distinguish processing cost reduction from relevance filtering. -->

---

## Context management: select what matters now

**Purpose:** keep the current request useful by selecting, limiting,
or summarizing context while preserving the task and instructions.

**Toy, Step 5 payload fragment:**

```python
json={"model": MODEL, "messages": messages, "tools": tools},
```

Step 6 appends responses and results; every call resends the history.
Useful source reads and huge unrelated logs accumulate alike.

**Step 7's turn cap limits calls, not context size.**

<!-- First course slide after Carbon image 09 restates purpose before implementation. A prior file result remains an old snapshot after edits. MAX_TURNS applies within one user interaction; neither result size nor accumulated history is bounded. It is not a complete spend cap. -->

---

## Context management: Claude Code and the toy

**Claude Code:** `/context` reports usage; `/compact` and automatic
compaction reduce conversation detail to make room.

**Tradeoff:** a shorter summary can omit information needed later.

**Toy limit:** no compaction or context budget.
**Possible extension:** a compact command or automatic preparation
before `call_zen`, preserving the task, rules, and unresolved questions.

Keep tool requests and required results together.
Caching reduces repeated processing; it does not filter context.

<!-- Source: https://code.claude.com/docs/en/how-claude-code-works#the-context-window . Mark the extension as absent from the toy. Arbitrary message deletion can leave an invalid exchange. Lecture 6 returns to costs and compaction tradeoffs. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 10:46](https://youtu.be/mQfTdNVCOB0?t=646)' -->

![Tools give the model structured ways to request action](../../carbon-layer/11-tool-interface.png)

<!-- 29–39 min: tools. Useful context enables a decision, but writing I fixed it does not edit a file. We need a declared operation, local implementation, dispatch, and feedback. -->

---

## Tool interfaces: turn decisions into operations

**Purpose:** let the model request actions and learn from their results.

Instructions and included files support a conversation.
Saying “change the discount calculation” does not edit the file.

A tool pairs a **function** with a **schema** describing its name,
purpose, and parameters.

Model requests → harness executes → result enters context → repeat.

<!-- Purpose first after Carbon image 11. This closes the loop that makes the system act. The conceptual progression includes @path injection; the assigned toy lacks that mechanism. Its file-reading tools belong in this section. -->

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

The name identifies the function; the schema describes its JSON arguments.

<!-- Provided schema, reformatted. The model receives metadata, not the Python function. The model formats argument JSON from the schema; the harness parses it into Python parameters. Schema metadata does not replace runtime checks. -->

---

## Two registrations, two different jobs

**Provided in Step 5:**

```python
TOOLS_DICTIONARY = {"read_file": read_file}
TOOLS_SCHEMA = [READ_FILE_SCHEMA]
```

| Structure | What it tells its recipient |
|---|---|
| `TOOLS_SCHEMA` → model | Tool names, purposes, and argument format |
| `TOOLS_DICTIONARY` → harness | Which Python function a tool name identifies |

The model returns JSON arguments.
The harness parses them, calls the function, and returns its result.

<!-- Match the revised explanation: the string read_file identifies the callable read_file. Only the metadata travels to the model; function objects stay in the harness. Step 5 alone can advertise a tool but cannot execute the request until dispatch is added. -->

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
Adding these tools enables discovery and actual edits.

**Toy limit:** no Bash runner or MCP connection.
**Possible extension:** add these interfaces with registered
implementations and useful results.

Actions also introduce a new responsibility: **guardrails**.

<!-- Sources: https://code.claude.com/docs/en/how-claude-code-works#tools and https://code.claude.com/docs/en/mcp . Students run pytest themselves; its output does not automatically enter the toy's context. MCP is an interface mechanism, not permission to perform every available action. -->

---

## Tool actions need harness guardrails

An **approval gate** can require confirmation before an action runs.
If required approval is absent, the gate rejects the call: **fail closed**.

A **sandbox** limits the resources an executing tool can affect.
Shell execution needs an environment with enforced boundaries.

**Toy:** path rejection and a turn cap, but no interactive approval
gate, Bash tool, or OS sandbox.

Next: how the execution environment enforces those boundaries.

<!-- Reflect the new guardrail discussion in the notes without attributing an approval gate to the toy. Policies may prohibit an action outright; approval is not a universal override. A path helper or working directory alone does not isolate Bash from the host. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 12:20](https://youtu.be/mQfTdNVCOB0?t=739)' -->

![Execution environments bound what actions can affect](../../carbon-layer/13-execution-environment.png)

<!-- 39–47 min: execution environments. A syntactically valid write request could target the wrong file. The execution layer must enforce scope even if instructions are ignored. -->

---

## Execution environments: enforce action boundaries

**Purpose:** decide where tools run and what they can read, change,
or contact—even when the model requests the wrong action.

A valid `write_file` request could still name an outside file.

Permission controls decide whether a call may proceed.
An execution sandbox constrains what a running operation can affect.

The toy illustrates one part: checked paths under `sandbox/`.

<!-- Purpose first after Carbon image 13, before the supplied helper. Distinguish project working directory, permission gate, and runtime confinement. A directory name by itself does not enforce a boundary. -->

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

<!-- Answer: nothing about file access. Adding Step 3 creates the directory but the check must be on every tool path. Valid containment does not guarantee file existence or successful I/O. -->

---

## Execution environments: Claude Code and the toy

**Claude Code:** the directory where you launch it, permission
decisions, and a configured Bash sandbox for filesystem/network limits.

**Toy: partial.** The helper checks its filesystem-tool arguments.
It does not isolate Python or constrain arbitrary child processes.

**Possible extension:** a test runner needs process, filesystem,
network, credential, timeout, and approval boundaries.

What happens to completed and unfinished work if the agent stops?

<!-- Source: https://code.claude.com/docs/en/sandboxing . Even pytest executes project code. A worktree separates working files without providing OS isolation. The helper is not hardened against concurrent path changes. Use interruption to motivate durable state. -->

---

<!-- _class: source -->
<!-- _paginate: false -->
<!-- _footer: 'Source: The Carbon Layer · [Harness Engineering Masterclass, 14:16](https://youtu.be/mQfTdNVCOB0?t=856)' -->

![Durable state preserves progress beyond current attention](../../carbon-layer/15-durable-state.png)

<!-- 47–55 min: durable state. An execution environment is a place to work, but tasks can stop and resume. Distinguish artifacts and progress records from a current prompt. This is the final primitive today. -->

---

## Durable state: preserve work for continuation

**Purpose:** keep completed work, evidence, and unfinished steps
available outside the model's current context.

An edit may be complete even though testing is still pending.

Durable state supports:

- Restarting the same agent after an interruption.
- Handing work to another agent.
- Continuing with a different model.

<!-- Purpose first after Carbon image 15. Examples include files, plans, diffs, logs, session records, and memory notes. The next worker needs both artifacts and an account of what was done and remains uncertain. Stored claims are not automatically verified facts. -->

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

A plan can support a resumed session or a handoff:

| Responsibility | What happens to the plan |
|---|---|
| Durable state | Keeps the goal, changes, evidence, and next steps |
| Context delivery | Includes it in the next agent's input, e.g. `@plan.md` |
| Context management | Selects the parts relevant to the current task |

Saving the next step does not schedule or execute that step.
That leads to **orchestration**, beyond today's scope.

<!-- Durable state supports the same agent restarting, a handoff to another agent, or continuation with a different model. A saved artifact still has to be delivered; raw provider-specific message histories need not be portable. Do not expand into orchestration or subagent mechanics here. -->

---

<!-- _class: lead -->

## Claude Code: observe the harness

Which instructions and facts were supplied?
What did the developer include, and what did the model request?
What context was retained or summarized?
Which tool acted, and what came back?
What enforced its boundary?
What progress survives for a restart or handoff?

<!-- 55–70 min: 15-minute demo block reserved. Scenario and script are intentionally deferred to the next instructor discussion. These are observation prompts, not an approved live sequence. Later prepare a rehearsal record and static fallback. -->

---

## Diagnose the missing responsibility

| What you observe | Where to investigate |
|---|---|
| Generic fix; no project files in context | Context delivery |
| A huge obsolete log in every request | Context management |
| Outside path rejected before a read | Execution boundary and error feedback |
| Files survive; continuation or handoff lacks task history | Durable state and retrieval |

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

<!-- Launch the unchanged exercise. The required turn cap and path boundary remain graded. Refer to current starter/setup for model access; no shared Anthropic key or price promise. -->

---

## Next lecture

Context costs, compaction tradeoffs, memory, and verification.

**Project 0 will be given at the end of the next lecture.**

<!-- Match the revised lecture notes. No additional pre-class readings or end-of-week Project 0 deadline are assigned here. -->

---

<!-- _class: references -->

## Sources and companion material

The Carbon Layer, [Harness Engineering Masterclass](https://www.youtube.com/watch?v=mQfTdNVCOB0),
opening through Durable state (approximately 0:00–16:00).
The eleven source images retain their third-party provenance.
[Carbon's staged Python implementation](https://github.com/thecarbonlayer/carbon)
offers a more extensive tour of the primitives.

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
