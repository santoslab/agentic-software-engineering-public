# Lecture 05 — Anatomy of a Coding Agent: Building the Toy Agent

> **Unit:** weeks-01-03 · **Week 3, meeting 1 of 2** · 75 minutes
>
> **Thesis:** In ~200 lines of Python against the raw API you can build a working
> coding agent — after today, no part of Claude Code is magic.

## Learning objectives

After this lecture, students can:

1. Write the agent loop against the Anthropic Messages API (the Ex. 4 deliverable).
2. Author a system prompt and JSON tool schemas for file-editing tools.
3. Identify the security decisions a harness must make (path jailing, command
   allowlists, spend caps) and where each lives in the code.
4. Enumerate what Claude Code adds beyond the bare loop.

## Before class

- [required] Anthropic API docs: Messages API + Tool use (in depth)
- [required] Thorsten Ball, *How to Build an Agent*
- [recommended] *Building Effective Agents*, "agents" section (re-read)
- Ex. 2 due today.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–5 | Motivation | Ball's subtitle says it: "the emperor has no clothes." Everything from weeks 1–2 — loop, roles, tools, system prompt — in one file you can read in a sitting. Today: walk it; this week: build it. |
| 5–20 | Walkthrough 1: the conversation | Anatomy of a call: `model`, `system`, `messages`, `max_tokens`. The messages list is the **only** state (L01's statelessness, now in code — point at the line where it's re-sent whole). System prompt authoring for the toy: identity, working-directory rule, "prefer reading before editing," output discipline. |
| 20–40 | Walkthrough 2: tools & dispatch | Schemas for `read_file`, `list_dir`, `write_file`/`edit_file`; optional `run_command` with a hard allowlist. The dispatch loop: `stop_reason == "tool_use"` → execute → append `tool_result` → re-call. Tool errors go back as results — feedback, not crashes. Security beat: **you are now the permission system from L03** — path jailing (resolve + prefix-check against the scratch dir), allowlist rationale, why `max_tokens` and model choice are your spend cap. |
| 40–57 | Live run | The toy agent on a seeded task: "fix the failing test in this 3-file mini-project" (same mini-project that ships with Ex. 4). Verbose mode prints each request/response. Narrate the iterations; savor the moment it hits a tool error and recovers. If time: second run with a deliberately worse system prompt — behavior visibly degrades (L02's "same model, different soul," now reproducible). |
| 57–67 | Toy vs Claude Code | What the toy lacks: permission UI, context compaction, CLAUDE.md injection, plan mode, subagents, a battle-tested system prompt, sandboxing. Each maps to something students have already used in Ex. 2 — the harness reframed as legible engineering, not secret sauce. |
| 67–75 | Ex. 4 launch | Spec walkthrough; the pseudocode skeleton (structure, not solution); shared API-key logistics and spend rules (Haiku for iteration, `max_tokens` cap, expected total < a few dollars); safety rules are graded elements, not suggestions. What "done" looks like: both micro-tasks completed with session logs. |

## Demos

### Demo 1 — Toy agent end-to-end (the lecture's spine)

- **Artifacts:** instructor's toy agent (~200 lines, same structure as the Ex. 4
  skeleton); seeded 3-file mini-project with one failing test (the same one shipped in
  the exercise); verbose flag on.
- **Setup:** API key exported; scratch dir reset to the seeded state; rehearsed the
  morning of; terminal font large; the agent source open in a second pane.
- **Script:** (1) 60 seconds on the source: point at the loop, the dispatch, the
  jail check; (2) run the fix-the-test task; (3) narrate each iteration against the
  L02 diagram; (4) show the passing test; (5) optional degraded-system-prompt rerun.
- **Expected outcome:** the class watches ~200 lines do recognizably Claude-Code-like
  work.
- **Fallback (mandatory to prepare):** full recorded run from rehearsal, plus the
  printed session log as a static walkthrough.

## Discussion prompts

1. Which single tool would you add next, and what's the worst thing it could do?
2. Where in the loop would you insert a human checkpoint, and what would it cost you?
3. Your toy re-sends the whole conversation every call — what does that predict about
   long sessions? (Sets up L06.)

## Assigned after class

- Readings (for L06):
  - [required] Anthropic engineering blog, *Effective context engineering for AI
    agents*.
  - [required] [Agentic Development Principles](../student-repo/handouts/handout-agentic-principles.md).
  - [required] [NautilusTRX pass retrospectives](../student-repo/handouts/handout-nautilustrx-retrospectives.md)
    (~10 min).
- Exercise: **Ex. 4 — toy agent**
  (`../exercises/exercise-04-toy-agent.md`), due start of week 4.
- Reminder: Project 0 kickoff due end of week 3.

## Instructor notes

- **Cut if running long:** the degraded-system-prompt rerun inside Demo 1, then
  compress "Toy vs Claude Code" (57–67) — the exercise reflection asks the same
  question, so it self-heals.
- **Risks:** highest-stakes live demo of the unit. Rehearse same-day; record the
  rehearsal. Have the seeded mini-project under version control so reset is one
  command. If the model one-shots the fix without exploring, rerun with the harder
  seeded variant (keep two seeds prepared).
- **Variants:** with laptops and time, minutes 40–57 can become "predict the next tool
  call" — pause before each iteration and poll the room.
