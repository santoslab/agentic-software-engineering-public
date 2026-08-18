# Exercise 2 — Codebase Comprehension with Claude Code

> **Assigned:** Lecture 03 · **Due:** before Lecture 05 · **Effort:** 2–3 hours
>
> **Requires:** Claude Code installed and authenticated (Claude Pro).

## Goal

Your first real Claude Code sessions — on a codebase you've never seen, in
*comprehension* mode. You will use the agent to build an accurate mental model of an
unfamiliar project, improve its machine-generated documentation with human intent, and
— critically — **catch the agent being wrong at least once**. You don't modify the
code in this exercise; the first agentic build is Project 1.

## Target codebase

<!-- INSTRUCTOR PLACEHOLDER — pick before publishing.
Selection criteria:
  - ~2–10 KLOC: big enough that nobody reads it linearly, small enough for 2–3 hours
  - unfamiliar to the class (not covered in prior courses, not famous)
  - builds and runs tests cleanly with documented steps (students verify claims)
  - has at least one non-obvious design decision (something /init will miss)
  - permissive license
Record the pinned commit hash here so all students explore identical code. -->

**Repo:** `<URL>` at commit `<hash>`

Clone it read-only. Do not read third-party write-ups about it; the point is what *you*
and the agent can establish from the source.

## Task

1. **Explore.** Start a Claude Code session in the repo. Use exploration prompts,
   @-mentions, and (if useful) plan mode's read-only analysis to answer the instructor
   question set below. Watch `/context` as you go — notice what exploring costs.
2. **Generate, then improve.** Run `/init`. Read the generated CLAUDE.md critically,
   then produce an improved version: correct what's wrong, cut what's noise, and add
   at least three things `/init` could not have known from the code alone (intent,
   conventions, gotchas you established by asking).
3. **Question set.** Answer in your own words (the agent may help you find evidence,
   but every claim must cite a file path you actually opened):
   - What does this system do, in one paragraph for a new teammate?
   - Trace the main data flow: from entry point to the core computation/state change
     to output/persistence.
   - Where are the tests, what do they actually cover, and what's conspicuously
     untested?
   - Find one design decision you'd question, and steelman why the authors did it.
4. **Catch it being wrong.** Document at least one instance where Claude's claim about
   the codebase was inaccurate, incomplete, or confidently overstated — and how you
   caught it (reading the source, running the code, running tests). If everything it
   said checked out, document the claim you *verified hardest* and how.

## Deliverable

A folder (zip or repo link) containing:

- `CLAUDE.md` — your improved version (mark your three-plus additions with `<!-- added -->`)
- `architecture.md` — 1–2 pages answering the question set, with file-path citations
- `gotcha.md` — the caught-being-wrong writeup (claim, evidence, how you checked)
- `reflection.md` — half a page: which exploration prompts earned their keep, which
  wasted context, and what you'd ask first next time

## Completion checklist (all required for satisfactory)

- [ ] Improved CLAUDE.md with ≥3 marked additions the generator couldn't know
- [ ] Question set answered with file-path citations throughout
- [ ] One verified inaccuracy (or hardest-verified claim) documented with evidence
- [ ] Reflection names specific prompts, not generalities
- [ ] No code modifications (comprehension only)

## Troubleshooting

- **Permission prompts on every file read:** normal on first contact — consider
  accepting reads for the session; keep write/execute prompts on.
- **Session feels sluggish or answers degrade:** check `/context`; a fresh session plus
  your improved CLAUDE.md re-gathers cheaper than compacting a bloated one (this is
  Lecture 06's topic — you're living it early).
- **Claude asserts something about the code you can't find:** that may be your
  `gotcha.md` — make it show you the file and line.
