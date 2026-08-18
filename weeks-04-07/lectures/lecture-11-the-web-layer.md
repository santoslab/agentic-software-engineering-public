# Lecture 11 — The Web Layer: Testing Types Become Mechanical Gates

> **Unit:** weeks-04-07 · **Week 6, meeting 1 of 2** · 75 minutes
>
> **Thesis:** The classical testing-types taxonomy stops being exam trivia the day
> each type becomes a gate an agent must turn green before work advances — and a
> green unit suite and a working application are different claims.

## Learning objectives

After this lecture, students can:

1. Map the testing pyramid onto a layered application and say which layer each
   test type guards.
2. Design a gate table: check, exact command, definition of green, and when the
   gate activates.
3. Write Flask test-client integration tests with both paths (success and
   rejection) per route.
4. Keep layering intact under feature pressure — the engine diff stays empty while
   the app grows a whole interface.

## Before class

- [required] Flask docs: Quickstart + Testing.
- [recommended] The lost-communities gate-table excerpt (in today's notes).
- **PKB checkpoint 1 due today.**

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–10 | Cold open: green suite, broken app | The lost-communities smoke-gate rationale, quoted: unit tests never start the real server, so *nothing* catches a broken boot — and a clean clone has no `.env`, so smoke-testing from a warm working tree proves the wrong thing. The claim hierarchy: "the functions work" (unit) < "the pieces work together" (integration) < "the application starts and serves" (smoke) < "a user can do the thing" (end-to-end). Each is a *different sentence*; a gate table is deciding which sentences you require, and when. |
| 10–26 | Testing types, mapped onto Stage C | The pyramid on the tictactoe stack: unit = the engine suite (untouched, pure, fast); integration = Flask test-client hitting routes that call engine + DB; smoke = fresh clone, documented setup, server boots, both pages render; e2e = clicking through a real browser (P2 territory — named, deferred). Worked example: both paths for the move route — a legal move (200, board advances) and an occupied-cell move (rejection status, board unchanged, error surfaced). One route, two sentences, both required. |
| 26–40 | The gate table | Read the real one: lost-communities' Lint / Tests / Smoke / Both-paths / Contract / Coverage / Review / Live-app rows, each with a command, a definition of green, and an *active-from* milestone. Two design ideas to steal: gates **activate progressively** (the both-paths gate would be silly before routes exist), and **"verification fails" is mechanical** — a red gate returns work to in-progress, no judgment call. Stage C's version is three rows (lint, tests, smoke); it grows in P2. |
| 40–54 | Demo 1 — running the gates, and one red | Live on the instructor's Stage C repo: `GATES.md` on screen; run lint, pytest, smoke (fresh-clone boot + both pages) — green. Then break the move route's rejection path deliberately, run gates, watch the both-paths test go red, and *stop* — the red gate returns the work; no "I'll fix it after commit." Revert, green, commit with the gates-green line. |
| 54–64 | Flask in twenty lines | For students who've never seen it: route → handler → `render_template`; the app factory pattern (needed for test-client isolation); where the engine gets called (the handler is a *caller*, like `main.py` — the layering rule stated in `web/CLAUDE.md`). What "light JS" means here: a click posts a move; no framework, no build step. |
| 64–75 | Stage C walkthrough + Q&A | The checklist: pages from a fresh clone, empty engine diff, GATES.md with visible runs, both-paths tests, the hook (assigned Thursday), per-directory CLAUDE.md. PKB checkpoint 1 collected today. |

## Demos

### Demo 1 — Running the gates, and one red

- **Artifacts:** instructor's Stage-C-complete repo: play + leaderboard pages,
  `GATES.md`, both-paths tests; a prepared one-line breakage of the rejection
  path (e.g., return 200 on occupied cell).
- **Setup (before class):** rehearse the full gate run under 4 minutes; have the
  breakage as a stashed patch; fresh scratch directory for the smoke clone.
- **Script:** (1) read GATES.md aloud — commands and greens; (2) run all three
  gates green, including the fresh-clone smoke; (3) apply the breakage patch as if
  an agent "simplified" the handler; (4) gates — both-paths red; (5) narrate the
  discipline: red returns work, the todo goes back to in-progress; (6) revert,
  green, commit "gates green".
- **Expected outcome:** the gate table experienced as a *procedure with teeth*,
  not documentation; the red-gate moment is the memory students keep.
- **Fallback:** recorded terminal run; the red-gate beat survives on video, and
  GATES.md reads fine as a slide.

## Discussion prompts

1. Which claim does each of your Stage C tests actually make — and do you have any
   test making the "it boots" claim, or are you smoke-testing from a warm tree?
2. Why does the both-paths rule say *per route where it matters* instead of
   *per route*? Find a route where the failure path is genuinely not worth a test.
3. The gate table has an "active from" column. What goes wrong with gates that
   activate too early? Too late?

## Assigned after class

- Readings (for L12):
  - [required] Claude Code docs: Hooks; Memory (CLAUDE.md hierarchy).
  - [recommended] `student-materials/hooks/log-cost-on-end.ps1` — read it as a
    spec; Thursday you port it.
- Project: **Stage C** launched today. **PKB checkpoint 1** collected.

## Instructor notes

- **Cut if running long:** the Flask-in-twenty-lines block (54–64) compresses to
  the app-factory slide + "the handler is a caller"; students with the Quickstart
  read survive, and the notes carry the rest.
- **Risks:** the fresh-clone smoke in the demo needs network for `pip install` —
  pre-warm a wheel cache or use `--no-index --find-links` against a local cache;
  the red-gate beat must not be improvised (a wrong breakage can cascade into
  debugging on stage). Students will want to add JS frameworks; hold the
  server-rendered line — the testing story is the point, and P2 stays
  server-rendered too.
- **Variants:** if several students finished Stage B early, run one student's repo
  through *their* gates cold as the opening instead of the instructor's.
