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
   the difference between instructions and enforcement, context and stored state.
5. Propose where a missing capability could be added without treating those
   extensions as new exercise requirements.

## Teaching approach and sources

Use the sequence **purpose → mechanism → Claude Code → toy code → limitation and
possible extension** for each primitive. The recurring example is the discount bug
in Exercise 4's three-file checkout project. This is a conceptual example throughout
this lecture; the live-demo scenario has not yet been selected.

Students are learning to understand and assemble supplied code incrementally, not
to invent the toy agent without help. Quote and explain any code already provided
in the exercise, including the complete Step 3 sandbox helper. Ask students to
predict the effect of an addition, inspect the lines, then explain the resulting
behavior. Preserve the indicated student-authored work for the exercise.

The architectural sequence comes from The Carbon Layer's
[*Harness Engineering Masterclass*](https://www.youtube.com/watch?v=mQfTdNVCOB0),
[local summary](../../carbon-layer/harness-architecture-primitives.md), and
[transcript](../../carbon-layer/harness-engineering-masterclass-transcript.md).
Teach it as a useful vocabulary whose responsibilities overlap. Stop at Durable
state; later primitives shown dimmed in the source images are outside this lecture.
The `carbon-layer/ch-*.md` materials describe a different, more extensive agent;
do not attribute those capabilities to the assigned toy.

## Before class

- **Required:** Carbon Layer video from the beginning through the Durable state
  discussion (approximately 0:00–16:00), or the corresponding local transcript.
- **Required:** Skim [Exercise 4](../exercises/exercise-04-toy-agent.md), especially
  Steps 3–6, and its [message-format guide](../exercises/exercise-04-starter/message-format-hints.md).

## Topic outline

| Time | Topic | Teaching content and code anchors |
|---|---|---|
| 0–8 | Model, runtime, harness | Source images 02–04; distinguish model input/output from the repeated tool loop and the supporting harness. Introduce the discount task and the predict/add/observe/explain method. The exercise uses Chat Completions through OpenCode Zen. |
| 8–14 | Instructions | Image 05 and transition image 06. Explain why standing guidance matters. Claude: `CLAUDE.md` and project rules. Toy: Step 2 `SYSTEM` and the starter's initial system message. Changing guidance changes model input, not tool authority. Extension: load an instruction file. |
| 14–21 | Context delivery | Image 07. Claude: explicit file references, reads, search, command output. Toy: Step 4 `read_file`, Step 6 result append, Step 8 discovery. Trace disk → return value → message → next request. Test output must be supplied by the student. Extension: explicit file references or focused search. |
| 21–29 | Context management | Images 08–09. Claude: `/context`, `/compact`, automatic compaction. Toy: growing `messages`, repeated payload. Explain relevance and lossy summaries; distinguish turn limits from context limits. Extension: prepare context before `call_zen`, retaining valid tool exchanges. Leave detailed cost analysis to L06. |
| 29–39 | Tool interfaces | Image 11. Claude: file tools, Bash, brief MCP placement. Toy: Step 5 schema and two registries; Step 6 call/dispatch/result cycle; Step 9 verbose output. Trace the `file_name` argument and matching `tool_call_id`. Explain intermediate unbounded loop versus Step 7's required cap. |
| 39–47 | Execution environments | Image 13. Claude: working directory, permissions, configured Bash sandbox. Toy: supplied Step 3 helper and its callers in Steps 4/8. Explain resolve, containment, rejection, error feedback. A worktree or path helper is not process isolation. Extension: boundaries for a future test-running tool. |
| 47–55 | Durable state | Image 15. Claude: saved sessions/resume, persistent notes, plans and Git changes. Toy: files and manually copied logs survive; `messages` starts over. Extension: session save/load and task summary, with an explicit interruption boundary. Connect storage, retrieval, and active context. |
| 55–70 | Claude Code demonstrations | Reserved for the next demo-design discussion. Use the observation prompts below; no scenario or live script is committed yet. |
| 70–75 | Synthesis and Ex. 4 handoff | Diagnose a harness failure, then explain exercise expectations, manual test execution, logs, and reflection. Future extensions are discussion material, not extra deliverables. |

## Demo block — reserved for separate design

**Status:** the lecture content and a 15-minute slot are ready; demo selection and
scripting are intentionally deferred to the next instructor discussion. Do not
present the former toy-agent end-to-end script as an approved demo.

The eventual Claude Code demonstration should let students connect visible behavior
to the content already introduced. These are observation prompts, not a script:

- Which standing instructions and project facts are available for this task?
- What evidence entered context, and what was retained or summarized?
- Which tool request actually performed an action, and what result came back?
- What enforces the execution boundary?
- What persists, and how does a later interaction obtain it?

Once the scenario is selected, prepare a rehearsal record and static fallback,
check the installed Claude Code commands/settings, and keep the total demo time at
15 minutes. Do not depend on a model making a particular mistake or choosing an
exact tool sequence for a teaching point to work.

## Comprehension checks and instructor answers

Use the first three within their primitive blocks; return to the restart question
at the end. The student-facing notes collect all four for review.

| Prompt | Expected reasoning |
|---|---|
| The agent proposes a generic fix without reading the checkout files. What is missing? | Context delivery: the relevant code and tests have not entered a request. Reading or explicitly supplying them grounds the task. Instructions can encourage this, but do not contain the missing facts. |
| A huge obsolete log is resent every call. Does `MAX_TURNS = 25` solve it? | Context management is needed. The cap limits calls within one interaction, not bytes/tokens in a result or history over multiple interactions. |
| Reading `../../secrets.txt` returns a rejection. Which parts of the harness did this? | `resolve_in_sandbox` rejects the resolved path before file I/O; dispatch catches the exception and appends an error tool result. The next call delivers the error to the model. |
| The toy edits a file, exits, and restarts. What survives? | The file and any manually saved logs survive. Conversation history does not. The initial system prompt is loaded again; the agent needs new reads or a future session loader to recover task context. |

## Instructor accuracy notes

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
  than a string prefix. A Windows-style absolute path is not a portable rejection
  test on macOS/Linux; use traversal or a native absolute path when explaining it.
  The helper is limited application-level enforcement, not an OS sandbox.
- **Keep three distinctions visible.** Instructions versus enforcement; context
  delivery versus selecting current context; durable storage versus automatic
  retrieval. Compaction is lossy. Prompt caching reduces repeated processing work
  but is not context filtering. A saved claim is not proof that it is true.
- **Use current Claude documentation.** [Instructions/memory](https://code.claude.com/docs/en/memory),
  [file references](https://code.claude.com/docs/en/common-workflows#reference-files-and-directories),
  [tools/context/sessions](https://code.claude.com/docs/en/how-claude-code-works), and
  [sandboxing](https://code.claude.com/docs/en/sandboxing), checked September 8, 2026.
  Recheck the installed interface when rehearsing the eventual demo.
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
in greater depth. Before that class:

- **Required:** [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
- **Required:** [Agentic Development Principles](../student-repo/handouts/handout-agentic-principles.md).
- **Required:** [NautilusTRX pass retrospectives](../student-repo/handouts/handout-nautilustrx-retrospectives.md).
- Reminder: Project 0 kickoff is due at the end of week 3.

## Companion artifacts and rendering

- [Full lecture notes](../lecture-notes/lecture-05-anatomy-of-a-coding-agent.md).
- [Marp slide source](../slides/lecture-05-anatomy-of-a-coding-agent.md).

The deck uses all eleven supplied PNGs from `carbon-layer/`, with source credits
and timestamped links. They retain their third-party provenance as described in
[LICENSING.md](../../LICENSING.md). Source paths are relative; keep the repository
layout intact when presenting the generated HTML. PDF embeds the images.

Render only this lecture from the repository root:

```sh
npx -y @marp-team/marp-cli@latest --allow-local-files weeks-01-03/slides/lecture-05-anatomy-of-a-coding-agent.md -o weeks-01-03/slides/lecture-05-anatomy-of-a-coding-agent.pdf
npx -y @marp-team/marp-cli@latest --allow-local-files weeks-01-03/slides/lecture-05-anatomy-of-a-coding-agent.md -o weeks-01-03/slides/lecture-05-anatomy-of-a-coding-agent.html
```
