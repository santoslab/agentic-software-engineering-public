# Lecture 05 — Anatomy of a Coding Agent: Harness Primitives

> **Unit:** weeks-01-03 · **Week 3, meeting 1 of 2** · 75 minutes
>
> **Thesis:** Effective coding agents depend on engineering around the model:
> what it sees, how it acts, the boundaries on those actions, and what survives afterward.

## Learning objectives

After this lecture, students can:

1. Distinguish the model, runtime, and harness, and explain the first six Carbon
   Layer primitives through Durable state.
2. Explain why each primitive is needed and identify a corresponding Claude Code
   feature and its manifestation, limitation, or absence in Exercise 4.
3. Trace supplied exercise code from a model's tool request through dispatch,
   path checking, and a result delivered to the next model call.
4. Predict how adding each provided chunk changes the toy's behavior, and explain
   the difference between instructions and enforcement, developer-pushed context
   and model-requested tool reads, and current context and stored state.
5. Propose where a missing capability could be added without treating those
   extensions as new exercise requirements.

## Teaching approach and sources

Use the sequence **purpose → mechanism → Claude Code → toy code → limitation and
possible extension** for each primitive. The recurring example is the discount bug
in Exercise 4's three-file checkout project. The live demo works the same scenario
in Claude Code; see the [demo script](../demos/lecture-05-claude-code-demo/demo-script.md)
and Demo 1 below.

After each primitive's Carbon Layer graphic, begin the next course slide with a
visible summary of the primitive's purpose before introducing product features or
code. Use the transition graphics to state the problem that motivates the next
primitive. In particular, introduce context delivery as developer-controlled
`@file` inclusion before explaining model-requested file reads under tools.

Students are learning to understand and assemble supplied code incrementally, not
to invent the toy agent without help. Quote and explain any code already provided
in the exercise, including the complete Step 3 sandbox helper. Ask students to
predict the effect of an addition, inspect the lines, then explain the resulting
behavior. Preserve the indicated student-authored work for the exercise.

The architectural sequence comes from The Carbon Layer's
[*Harness Engineering Masterclass*](https://www.youtube.com/watch?v=mQfTdNVCOB0),
[local summary](../../carbon-layer/harness-architecture-primitives.md), and
[transcript](../../carbon-layer/harness-engineering-masterclass-transcript.md).
Teach it as the course's chosen vocabulary in an area without a generally accepted
categorization. The accompanying [Carbon Python implementation](https://github.com/thecarbonlayer/carbon)
builds up a harness in stages and provides a more extensive implementation tour.
It and the local `carbon-layer/ch-*.md` materials are additional reference material;
the assigned implementation remains Exercise 4. Recall Yao et al.'s ReAct paper
from the earlier suggested reading. Stop at Durable state; later primitives shown
dimmed in the source images are outside this lecture.

## Before class

- **Required:** Carbon Layer video from the beginning through the Durable state
  discussion (approximately 0:00–16:00), or the corresponding local transcript.
- **Required:** Skim [Exercise 4](../exercises/exercise-04-toy-agent.md), especially
  Steps 3–6, and its [message-format guide](../exercises/exercise-04-starter/message-format-hints.md).

## Topic outline

| Time | Topic | Teaching content and code anchors |
|---|---|---|
| 0–8 | Model, runtime, harness | Source images 02–04; emphasize that the harness assembles model input and executes requested actions. Recall Yao et al.'s ReAct pattern. Introduce the Carbon implementation, discount micro-task, and predict/add/observe/explain method. The exercise uses Chat Completions through OpenCode Zen. |
| 8–14 | Instructions | Image 05, then purpose: recurring project knowledge and general operating expectations, including architecture, technologies, and test-reporting preferences. Claude: system instructions, `CLAUDE.md`, project rules. Toy: Step 2 `SYSTEM` and initial system message. Extension: load an `AGENTS.md` from the sandbox. Image 06 motivates delivery of task-specific files. |
| 14–21 | Context delivery | Images 06–07 and purpose summaries: deliver files without requiring the developer to paste them or the model to request a tool. Claude's `@file` acts as an include; distinguish developer push from later model pull. Explain reference syntax, labels, placement, and size as delivery-policy decisions. Toy lacks this include mechanism; propose checked expansion before a model call. Defer file-reading code to the tools discussion. |
| 21–29 | Context management | Images 08–09, each followed by a purpose summary: handle a finite window and keep current input useful. Compare clearing with summarizing; ask what a summary must preserve. Claude: `/context`, `/compact`, automatic compaction. Toy: growing `messages` without filtering or a context budget; turn limits do not bound context. Extension: a compact command or automated preparation before `call_zen`. Leave detailed cost analysis to L06. |
| 29–39 | Tool interfaces | Image 11, then purpose: move from prose to operations by closing the request/execute/result loop. A tool pairs a function with a schema. Explain the two registries, JSON arguments, Python dispatch, result delivery, and IDs using Steps 5–6; Step 9 makes calls visible. Introduce guardrails: approval gates that fail closed and bounded execution. Toy lacks Bash, MCP, and interactive approval; Step 7 adds the required turn cap. |
| 39–47 | Execution environments | Image 13, then purpose: enforce what a tool may affect even when the model requests the wrong action. Claude: launch directory, permissions, configured Bash sandbox. Toy: supplied Step 3 helper and its callers in Steps 4/8; explain `__file__`, path resolution, containment, and error feedback. Distinguish a path helper or worktree from process isolation. Motivate durable state through interruption. |
| 47–55 | Durable state | Image 15, then purpose: preserve work for restart, handoff to another agent, or a change of model. Claude: saved sessions/resume, persistent notes, plans and Git changes. Toy: files and manually copied logs survive; `messages` starts over. Extension: session save/load and a task summary with evidence and unfinished work, with an explicit interruption boundary. Connect storage, retrieval, and active context. |
| 55–70 | Claude Code demonstrations | Run Demo 1's segments consecutively here, or interleave each segment at the end of its primitive's block and reclaim this slot for discussion. Use the observation prompts below while students watch. |
| 70–75 | Synthesis and Ex. 4 handoff | Diagnose a harness failure, then explain exercise expectations, manual test execution, logs, and reflection. Future extensions are discussion material, not extra deliverables. |

## Demos

### Demo 1 — Claude Code on the checkout micro-task (segmented)

- **Artifacts:** [`demos/lecture-05-claude-code-demo/`](../demos/lecture-05-claude-code-demo/) —
  `starter/` (the Exercise 4 Micro-task B seed files plus `CLAUDE.md`,
  `testing-guidelines.md`, and an empty `NOTES.md`),
  `outside-the-project/fake-api-keys.txt`, a representative `completed/` state,
  and the full [instructor script](../demos/lecture-05-claude-code-demo/demo-script.md).
- **Setup (before class):** follow the script's checklist — copy the demo folder
  outside the course repository (parent-directory `CLAUDE.md` files would leak
  into context), `git init` the starter, confirm `pytest -q` shows two failures,
  default permission mode, two terminals, and one full rehearsal with screenshots
  captured at the script's marked fallback points.
- **Script:** eight short segments in `demo-script.md`, one per primitive plus
  framing and wrap: instructions (`CLAUDE.md`, `/memory`, the `STATUS:` header,
  a `#` memory note), context delivery (model pull via a Read call vs developer
  push via `@file`), context management (`/context`, `/compact`, `/clear`), tool
  interfaces (the bug-fix task with JSON tool reports checked against the Ctrl+O
  transcript), execution environments (a denied out-of-project read), and durable
  state (exit mid-task, fresh-session handoff from `NOTES.md`, `claude --resume`,
  tests run on resume). Segments interleave at the end of each primitive's
  lecture block, or run consecutively in the 55–70 slot.
- **Expected outcome:** two failing tests become two passing tests over the
  session, and each primitive produces one piece of visible evidence (the
  script's Segment 7 table lists them). No beat depends on a specific model
  mistake or exact tool sequence; each has an "if it goes differently" note.
- **Fallback:** the rehearsal screenshots/recording captured at the script's
  **[fallback capture]** points; the `completed/` folder stands in for the end
  state if the live run must be abandoned.

While students watch, use these observation prompts:

- Which standing instructions and project facts are available for this task?
- What evidence did the developer push into context, what did the model request,
  and what was retained or summarized?
- Which tool request actually performed an action, and what result came back?
- What enforces the execution boundary?
- What persists, and how does a resumed session or another agent obtain it?

## Comprehension checks and instructor answers

Use the context questions within their primitive blocks; return to the restart
question at the end. The student-facing notes collect the core scenarios for review.

| Prompt | Expected reasoning |
|---|---|
| The agent proposes a generic fix without receiving the checkout files. What is missing? | Context delivery: the relevant code and tests have not entered a request. The developer can include them with `@file` in Claude Code. Later, tool reads offer another route. Instructions alone do not supply those contents. |
| Who decides to include `@discount.py`, versus requesting a `read_file` tool call? | The developer selects an explicit reference and the harness injects its contents. In the tool route, the model requests a read and the harness executes it and appends the result. The toy has the tool route but no `@file` expansion. |
| A huge obsolete log is resent every call. Does `MAX_TURNS = 25` solve it? | Context management is needed. The cap limits calls within one interaction, not bytes/tokens in a result or history over multiple interactions. |
| Reading `../../secrets.txt` returns a rejection. Which parts of the harness did this? | `resolve_in_sandbox` rejects the resolved path before file I/O; dispatch catches the exception and appends an error tool result. The next call delivers the error to the model. |
| The toy edits a file, exits, and restarts. What survives? | The file and any manually saved logs survive. Conversation history does not. The initial system prompt is loaded again; the agent needs new reads or a future session loader to recover task context. |
| What would another agent or a different model need to continue the work? | A durable account of the goal, changes, evidence, unresolved questions, and next steps, plus access to current artifacts. Those records still need to be delivered into its context. |

## Instructor accuracy notes

- **Separate instructions from task context.** Use general operating expectations
  and recurring project knowledge for Instructions. Use developer-controlled file
  inclusion for the initial Context delivery example; it does not depend on the
  model deciding to call a tool. Do not reintroduce the removed file-reading code
  walkthrough in that block. Delivery policy includes syntax, labels, placement,
  and size limits; `@` is a harness convention, not model magic.
- **Introduce guardrails without overstating the toy.** A gate requiring approval
  should reject a call when approval is absent; sandboxing bounds execution.
  The base toy rejects out-of-sandbox paths but has no interactive approval gate
  or shell runner. Do not describe every permission denial as overridable, or
  claim a directory check alone isolates Bash from the host.
- **Use the actual exercise protocol.** `tool_calls`, JSON-encoded arguments,
  `role: "tool"`, and `tool_call_id`; no Anthropic `stop_reason` or `tool_use` code
  in the toy walkthrough. Excerpts may omit comments or wrap lines, but retain
  the supplied semantics and names.
- **Distinguish stages.** A schema advertises a tool; a local dictionary dispatches
  it; appending its result informs the next model call. The Step 6 `while True`
  code is an intermediate stage, and Step 7's turn cap is required in the exercise.
- **Describe the logs accurately.** Verbose mode prints tool calls, arguments, and
  results, not every API request or all internal model reasoning. Recovery from a
  readable error is possible, not guaranteed.
- **Explain the path code literally.** The sandbox is anchored next to the script,
  not the shell's current directory. `is_relative_to` tests path containment rather
  than a string prefix. The helper is limited application-level enforcement,
  not an OS sandbox.
- **Keep the distinctions visible.** Instructions versus enforcement; developer
  push versus model pull; delivery versus selecting current context; durable
  storage versus automatic retrieval. Compaction is lossy. Prompt caching reduces repeated processing work
  but is not context filtering. A saved claim is not proof that it is true.
- **Use current Claude documentation.** [Instructions/memory](https://code.claude.com/docs/en/memory),
  [file references](https://code.claude.com/docs/en/common-workflows#reference-files-and-directories),
  [tools/context/sessions](https://code.claude.com/docs/en/how-claude-code-works), and
  [sandboxing](https://code.claude.com/docs/en/sandboxing), checked September 8, 2026.
  Recheck the installed interface when rehearsing the demo.
- **If running long:** shorten discussion of extension designs and compress the
  recap. Preserve the request/result trace, sandbox explanation, and restart
  distinction. The notes provide detail for students to revisit.

## Exercise handoff and next lecture

Assign [Exercise 4](../exercises/exercise-04-toy-agent.md).
Students work manually under its no-coding-agent-assistance instruction, with the
provided code as their starting point. They complete the indicated portions,
exercise the path boundary and turn cap, run both micro-tasks with verbose logs,
run `pytest` themselves, and write the reflection. Refer students to the current
starter/setup instructions for model access; do not promise a shared Anthropic
key, a particular free model, or a fixed total price.

Lecture 6 develops context economics, compaction tradeoffs, memory, and verification
in greater depth. **Project 0 will be given at the end of the next lecture.**

## Companion artifacts and rendering

- [Full lecture notes](../lecture-notes/lecture-05-anatomy-of-a-coding-agent.md).
- [Marp slide source](../slides/lecture-05-anatomy-of-a-coding-agent.md).
- [Demo assets and script](../demos/lecture-05-claude-code-demo/demo-script.md).

The deck uses all eleven supplied PNGs from `carbon-layer/`, with source credits
and timestamped links. They retain their third-party provenance as described in
[LICENSING.md](../../LICENSING.md). Source paths are relative; keep the repository
layout intact when presenting the generated HTML. PDF embeds the images.

Render only this lecture from the repository root:

```sh
npx -y @marp-team/marp-cli@latest --allow-local-files weeks-01-03/slides/lecture-05-anatomy-of-a-coding-agent.md -o weeks-01-03/slides/lecture-05-anatomy-of-a-coding-agent.pdf
npx -y @marp-team/marp-cli@latest --allow-local-files weeks-01-03/slides/lecture-05-anatomy-of-a-coding-agent.md -o weeks-01-03/slides/lecture-05-anatomy-of-a-coding-agent.html
```
