# Lecture 07 — Project 1 Kickoff — Own the Spec: ConOps, Classical and Agentic

> **Unit:** weeks-04-07 · **Week 4, meeting 1 of 2** · 75 minutes
>
> **Thesis:** A spec is not paperwork about the code — it is the one artifact that
> outlives implementations and steers agents; producing it is Project 1's first
> deliverable, and the starter ships without one *on purpose*.

## Learning objectives

After this lecture, students can:

1. Distinguish a ConOps (operational, user's-eye, implementation-free) from a SPEC
   (behavioral contract) and write a one-page version of each.
2. Reverse-engineer a behavioral contract from working code, including surfacing
   edge cases where the code's behavior is an *undocumented decision*.
3. State the spec-before-code rule and describe what its evidence looks like in a
   git history.
4. Bind a project law (the engine coverage gate) in CLAUDE.md and explain why laws
   live there rather than in prompts.

## Before class

Assigned at Lecture 06:

- Ex. 4 (toy agent) due at the start of this week — its loop vocabulary is assumed.
- No new reading was assigned; the Project 1 brief is distributed today.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–8 | The gap you are handed | The starter: working 9x9 game, ~90 green tests, random AI — and **no spec**. Recall L04's tale of two attempts: Attempt2's first act was declaring the inherited SPECS "sub-par" and rebuilding it before any code. Project 1 starts where they ended up: you own the spec from day one. The absence is the assignment. |
| 8–22 | What a spec does for an agent | Three loads it carries: (1) *grounding* — read at session start, it outlives every conversation (context rot recall from L06); (2) *drift prevention* — Attempt1's column-then-row prompt vs its shipped row-then-column SPECS: nobody decided, so the artifact and behavior diverged; (3) *portability* — the 9x9 ConOps produced the Java port; specs move across languages, prompts don't. Authority rule: when code and spec disagree, one of them is wrong *on purpose* — someone must rule, in a commit. |
| 22–36 | ConOps: classical shape, agentic revival | Summarize IEEE 1362's skeleton — scope, operational environment, user classes, and scenarios — and explain why it reads like it was written for agents (it grounds *intent*, not implementation). Students draft the one-page mini-ConOps in class; do not publish a starter-specific model. Contrast with SPEC clauses: testable, exact, edge-case-bearing. |
| 36–54 | Demo 1 — eliciting the spec *from* code | Live: Claude reads the starter and drafts the contract, instructed to list every place behavior is a *choice* rather than a necessity. Ask the room to predict and verify edge cases without publishing a canonical list. The point: elicitation runs in both directions — L04 grilled the human; today the code gets grilled. |
| 54–68 | The brief, stage by stage | Walk `project-1-brief.md`: five stages, one classical practice + one Claude feature each; the required-elements checklists; cross-stage rules (spec-before-code in history, plans committed under `plans/`, coverage law in CLAUDE.md from day one). Stage A in detail: SPEC + mini-ConOps + one spec-driven extension; the recommended extension (configurable board size) and why its ripple is the lesson. |
| 68–75 | Logistics + Q&A | Stage A due end of week 4 (pacing target); hard deadline for everything: start of week 8. Solo work; solution-code prohibition (case-study *documents* fair game). Questions. |

## Demos

### Demo 1 — Eliciting the spec from code

- **Artifacts:** `tictactoe-starter/` (clean clone, venv ready); prepared prompt:
  "Read this codebase and draft its behavioral contract as SPEC.md. Separately list
  every behavior that is a *decision* rather than a necessity — places where a
  reasonable implementer could have chosen otherwise."
- **Setup (before class):** fresh clone; `pytest` confirmed green; Claude Code open
  at repo root; font large.
- **Script:** (1) run the prompt; (2) while it works, ask the room to predict the
  edge cases; (3) walk the draft and verify each claim against code and tests;
  (4) show that the draft is still provisional by selecting one contested clause,
  locating its evidence, and sharpening it live.
- **Expected outcome:** students see a spec emerge from interrogation, and see that
  the human still rules on every contested clause.
- **Fallback:** pre-captured transcript of the same session, walked as slides; the
  edge-case list works static.

### Demo 2 — ConOps lineage (static)

- **Artifacts:** the IEEE-1362-derived ConOps model (structure only, one slide);
  9x9 CONOPS excerpts from the weeks 1–3 handouts; the Java port's CONOPS reuse.
- **Script:** skeleton → the 9x9 one → "same document, new language" → your
  one-page version is this, scaled down.
- **Fallback:** none needed (slides-first).

## Discussion prompts

1. The starter *works* and has 90 green tests. What, concretely, can go wrong in
   Stage B–E if no spec ever exists? (Drift, port impossibility, agent guessing.)
2. Choose one behavior the elicitation found that a reasonable implementation could
   handle differently. Bug, or contract? Who decides, and where is the decision
   recorded?
3. When is reverse-engineering a spec from code *wasted* effort?

## Assigned after class

- Readings (for L08):
  - [required] `project-1-brief.md` — in full; bring questions.
  - [required] Re-read the Spec-Driven Development section of
    `prompt-cheat-sheet.md`.
- Project: **P1 Stage A** launched today.

## Instructor notes

- **Cut if running long:** the ConOps block (22–36) compresses to the skeleton
  slide + the Java-port punchline; the demo must not be cut.
- **Risks:** Demo 1's elicitation may surface different edges from rehearsal —
  embrace whatever it finds and verify each claim against the starter. Students
  may conflate ConOps and SPEC all week; the "never says Python" test is the
  fastest discriminator.
- **Variants:** with a strong room, have students draft the mini-ConOps in pairs at
  minute 30 and read two aloud before synthesizing common strengths and omissions.
