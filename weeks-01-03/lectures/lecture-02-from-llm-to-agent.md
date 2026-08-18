# Lecture 02 — From LLM to Agent: the Loop, System Prompts, Tool Calls

> **Unit:** weeks-01-03 · **Week 1, meeting 2 of 2** · 75 minutes
>
> **Thesis:** An agent is an LLM in a while-loop with tools — nothing more mystical
> than that; the difference between ChatGPT and Claude Code is the harness, not the
> model.

## Learning objectives

After this lecture, students can:

1. Draw the agent loop from memory (prompt → model → tool call → execute → append
   result → repeat until no tool call).
2. Name the message roles (system / user / assistant / tool result) and say where tool
   output goes.
3. Read a raw tool-use API request/response pair and identify the schema, the call, and
   the result.
4. Explain why the same model behaves differently under different system prompts.
5. Place Claude Code on Anthropic's workflow-vs-agent spectrum.

## Before class

- [required] Karpathy, *Intro to Large Language Models* (YouTube)
- [recommended] 3Blue1Brown GPT/attention videos
- [gap-filler (optional)] *Deep Dive into LLMs*; *Attention Is All You Need* §1–2; InstructGPT

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–10 | Chat vs agent | Answer L01's cliffhanger: the "memory" lives in a messages list the *harness* maintains. Taxonomy by capability: ChatGPT answers, Copilot completes, an agent **acts** (reads files, runs commands, iterates). Same model underneath all three. |
| 10–25 | The agent loop | The pseudocode slide — the exact structure students will implement in Ex. 4: `while True: response = model(system, messages); if no tool_use: break; result = execute(tool_call); messages.append(result)`. Message roles and who writes each. Termination: the model stops asking for tools. Errors are just another tool result. |
| 25–40 | Tool calling mechanics | A tool = name + description + JSON schema. The model does not *run* anything — it emits a structured request; the **harness** executes and appends the result. Walk one real Messages-API request/response pair on screen: `tools=[...]`, `stop_reason: "tool_use"`, the `tool_result` block going back. Emphasize: the tool description is prompt text — the model chooses tools by reading English. |
| 40–50 | System prompts | What lives in Claude Code's system prompt, conceptually: identity, tool inventory, conventions, safety rules. "Same model, different soul." Foreshadow L03: CLAUDE.md is *user-space* system-prompt extension. |
| 50–62 | Live demo | Instructor's toy agent (the Ex. 4 artifact) on one tiny task, with raw JSON traffic printed to the terminal. Deliberately shown three weeks before students build it — today it demystifies, in week 3 it becomes the spec. |
| 62–70 | Taxonomy & lineage | Anthropic *Building Effective Agents*: workflows (prompt chains, routing) vs agents (model-directed loops); "use the simplest thing that works." ReAct (Yao et al. 2023) as the academic root of reason-then-act. Where Claude Code sits: an agent with strong harness guardrails. |
| 70–75 | Ex. 1 launch | Show 60 seconds of [Handout A](../student-repo/handouts/handout-A-tictactoe-transcript.md) (Session 1). The exercise: read a real multi-session transcript and *grade the human* — where did steering, vagueness, and correction happen? Point at the handout PDFs. |

## Demos

### Demo 1 — Raw tool-use JSON walkthrough

- **Artifacts:** one prepared request/response pair (from a scripted call with a
  `read_file` tool), pretty-printed in an editor.
- **Setup:** generate and save the JSON beforehand; syntax-highlighted, font large.
- **Script:** (1) request: system + messages + tools; (2) response: `stop_reason:
  "tool_use"` and the structured call; (3) the follow-up request with the `tool_result`
  appended — count the messages growing.
- **Expected outcome:** students see there is no magic channel — everything is text in,
  structured text out.
- **Fallback:** it's static content; no failure mode beyond projector gremlins.

### Demo 2 — Toy agent live run

- **Artifacts:** instructor's ~200-line Python toy agent (same one specified in
  `../exercises/exercise-04-toy-agent.md`); a scratch directory with a trivial task
  ("create hello.py that prints a greeting, then run it" — if `run_command` enabled).
- **Setup:** API key exported; scratch dir reset; terminal font large; `--verbose` flag
  printing each request/response summary.
- **Script:** (1) show the loop function on screen for 30 seconds — "this is the whole
  thing"; (2) run the task; (3) narrate each loop iteration as the JSON scrolls;
  (4) point at the moment the model stops requesting tools.
- **Expected outcome:** the loop diagram and the JSON demo fuse into one concrete
  object.
- **Fallback:** recorded run (record it when rehearsing); static transcript of the
  session as a second-level fallback.

## Discussion prompts

1. What can a tool-calling loop do that fine-tuning a model never could?
2. Where should the harness refuse to do what the model asks? (Sets up L03
   permissions.)
3. The tool description is English the model reads — what happens if it's misleading?

## Assigned after class

- Readings (for L03):
  - [required] The Carbon Layer - YouTube Channel - *[Harness Engineering Masterclass: Technical Deep Dive on how to build Agentic Systems](https://youtu.be/mQfTdNVCOB0?si=zZmykXWn-mVEo3Pk)* — up to timestamp 14:00 is good enough for preparing for L03.  This is Week 1-3 core reference (our toy agent will address the first several "primitives" (building blocks) for a coding agent that are introduced in the video. 
  - [required] Anthropic API docs, [*Tool use* overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) (skim to recognize the shapes;
    depth comes with Ex. 4).
  - [recommended] Yao et al., *ReAct* (skim §1–3).
- Exercise: **Ex. 1 — transcript critique**
  (`../exercises/exercise-01-transcript-critique.md`), due before Lecture 04.
- Logistics: Claude Code installed and authenticated before L03; use the current
  official installation documentation for the student's platform.

## Instructor notes

- **Cut if running long:** Taxonomy & lineage (62–70) compresses to two sentences and a
  reading pointer; never cut the live demo.
- **Risks:** the live demo is the first real-API moment of the course — rehearse it, and
  record the rehearsal as the fallback. Watch for students conflating "the model runs
  commands" with "the harness runs commands"; repeat the division of labor at least
  twice.
- **Variants:** none — this lecture is the same with or without laptops.
