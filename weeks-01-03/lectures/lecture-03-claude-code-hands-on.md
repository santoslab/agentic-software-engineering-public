# Lecture 03 — Claude Code Hands-On: Permissions, CLAUDE.md, Plan Mode

> **Unit:** weeks-01-03 · **Week 2, meeting 1 of 2** · 75 minutes
>
> **Thesis:** Claude Code is Lecture 02's loop productionized; today you learn to drive
> it deliberately instead of vibing.

## Learning objectives

After this lecture, students can:

1. Start a Claude Code session and reason about each permission prompt (what the
   harness is protecting and why).
2. Generate a CLAUDE.md with `/init` and critique it against a human-authored intent
   checklist.
3. Use plan mode for a nontrivial change: explore → plan → approve → execute → steer.
4. Use @-mentions and slash commands, and explain what each does to the context.
5. Name the advanced features (hooks, subagents, skills, MCP, sandbox) and say when in
   the semester each is taught.

## Before class

- [required] Anthropic, *Building Effective Agents*
- [required] Anthropic API docs, *Tool use* (skim)
- [recommended] Yao et al., *ReAct* §1–3
- Logistics: Claude Code installed and authenticated (Claude Pro).

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–5 | Recap & mapping | Map the Claude Code UI onto the L02 loop diagram: the spinner is the model call; the diff view is a tool call awaiting your permission; the transcript is the messages list. |
| 5–15 | First session & permissions | REPL basics. Permission prompts are the harness's refusal point from L02's discussion — the safety layer *is* the harness. Permission modes and their tradeoffs; why auto-accept is a loaded gun on day one; where settings live (`.claude/settings.json`). |
| 15–30 | Demo 1: workspace context | On a clean copy of the [bundled starter](../student-repo/tictactoe-starter/), run `/init` and compare its output with the human-intent examples in the companion notes (coordinate conventions, rendering rules, architecture boundaries). What did `/init` miss? Because it derives from code, it cannot know intent. @-mentions force a file into context; slash commands are prompt files — show the short elicitation-skill excerpt in the notes and the bundled [skill skeleton](../../.claude-template/skills/skill-template/SKILL.md). |
| 30–45 | Demo 2: plan mode | A real change to the starter: add a `blocking_move` strategy beside `random_move` in `computer_ai.py`. Explore → plan → approve → watch execution → interrupt once to steer. Why plan-first beats prompt-and-pray: cheap words before expensive edits. |
| 45–52 | Cost/context survival kit | Just enough for Ex. 2: `/context` (what's in the window), `/cost` (what you've spent), `/compact` (summarize to reclaim space), `/clear` (fresh start). Rule of thumb for now: watch `/context` when sessions feel sluggish or dumb; the economics deep-dive is L06. |
| 52–63 | Vague-prompt failure OR micro-lab | Default: demo a deliberately vague prompt ("fix the AI, it plays bad") producing a plausible-but-wrong change — cold open for L04. Variant if laptops: students run one exploration prompt on their own clone (needs install instructions published with L02). |
| 63–70 | Deferred-features map | One slide: sandbox, hooks, subagents, skills-at-depth, MCP, plugins — each mapped to its `../../technical-concepts.md` entry and the semester unit where it's taught (hooks/subagents ~W9, MCP ~W12). Message: "you don't need these yet; you'll meet each one when a project demands it." |
| 70–75 | Ex. 2 launch | Walk the comprehension exercise: unfamiliar OSS repo, `/init` then *improve* the CLAUDE.md, answer the question set, and catch Claude being wrong at least once. |

## Demos

### Demo 1 — `/init` vs the curated CLAUDE.md

- **Artifacts:** clean copy of the [bundled starter](../student-repo/tictactoe-starter/),
  the human-intent examples in the companion notes, and the bundled
  [skill skeleton](../../.claude-template/skills/skill-template/SKILL.md).
- **Setup:** copy the starter to a scratch directory; start a fresh Claude Code session.
- **Script:** (1) `/init`, read the output aloud; (2) compare it with the intent
  examples; (3) ask the room: "which lines could `/init` never have written?"; (4)
  open the skill skeleton — a slash command is just a versioned prompt file.
- **Expected outcome:** CLAUDE.md is understood as *user-maintained memory carrying
  intent*, not generated boilerplate.
- **Fallback:** pre-captured `/init` output as a text file; do the diff statically.

### Demo 2 — Plan mode feature add

- **Artifacts:** same starter scratch copy; target: `computer_ai.py` (add
  `blocking_move`: block the opponent's immediate win if one exists, else random).
- **Setup:** tests passing before class (`pytest`); prompt written on a card in advance.
- **Script:** (1) enter plan mode with a spec-flavored prompt referencing
  `random_move`'s pattern; (2) read the plan aloud — what would you push back on?;
  (3) approve; (4) interrupt once mid-execution to steer (e.g., naming); (5) run tests.
- **Expected outcome:** plan mode as a review gate: read, push back, then let it run.
- **Fallback:** recorded run from rehearsal.

### Demo 3 — Vague-prompt failure

- **Artifacts:** same scratch copy, fresh session.
- **Script:** "fix the AI, it plays bad" → watch it guess at what "bad" means; contrast
  with one sentence of specificity. Keep to 5 minutes; the point lands fast.
- **Fallback:** narrate from a saved transcript.

## Discussion prompts

1. What belongs in CLAUDE.md vs in the prompt vs in a spec file? (L04 answers this
   properly.)
2. Which permission would you *never* auto-accept, even in week 15?
3. `/init` read all the code and still missed things — what category of knowledge did
   it miss?

## Assigned after class

- Readings (for L04):
  - [required] [`prompt-cheat-sheet.md`](../../prompt-cheat-sheet.md) — L04's handout; read before
    class.
  - [required] Anthropic, *Claude Code Best Practices* (engineering blog).
  - [recommended] Claude Code docs: permission modes; CLAUDE.md/memory; plan mode
    (links curated in `../../technical-concepts.md` §1–5).
- Exercise: **Ex. 2 — codebase comprehension**
  (`../exercises/exercise-02-codebase-comprehension.md`), due before Lecture 05.
- Reminder: Ex. 1 due before Lecture 04.

## Instructor notes

- **Cut if running long:** the deferred-features map (63–70) collapses to "it's all in
  technical-concepts.md, each taught when a project needs it" — one sentence.
- **Risks:** live Claude Code demos are nondeterministic — rehearse both demos the
  morning of, and keep the rehearsal recordings as fallbacks. `/init` output quality
  varies; if it comes back unusually good, the diff against the curated file still
  carries the point (intent vs derivation).
- **Variants:** the 52–63 block is the designated flex point — failure demo (no
  laptops) or micro-lab (laptops; requires install instructions published with L02 and
  a TA in the room).
