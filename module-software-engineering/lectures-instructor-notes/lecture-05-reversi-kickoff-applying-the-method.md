# Lecture 05 — Reversi Kickoff: Applying the Method

> **Unit:** module-software-engineering · **Module week 3, meeting 1 of 2** · 75 minutes
>
> **Thesis:** The brief is the method you watched, on a game you were handed.
> This lecture reads Project 1 in order and opens, at each step, the artifact
> the reference game produced — so that you know what finished looks like before
> you start.

## Learning objectives

After this lecture, students can:

1. List the brief's steps 0 to 6 in order and name, for each, the artifact it
   produces, the commit that ends it, and the rule that governs it (DEV-8,
   DEV-9, DEV-2, VER-4 to VER-8, RPT-1, RPT-3, RPT-5).
2. Sort the Reversi sketch's observable policies into stated, implied, and
   missing (AUDCON-2, AUD-4), and state the convergence rule and what it does
   not permit.
3. Given a reference artifact — a numbered clause, a plan step, a test
   docstring, a §9.5 obligation, a fixture scenario — say which clause it cites
   and what its Reversi counterpart must state.
4. Trace the after-game-over silence through the reference's five artifacts and
   explain why the audit precedes the plan (DEV-8) and what the report's trace
   must show.
5. State what a green gate establishes and does not (VER-8) and what a fixture
   file owes its readers (VER-7), including how a pass scenario is verified
   before it is trusted.

## Before class

Assigned at *Verifying a Game*:

- [required] The Project 1 brief, `../project-1-reversi-brief.md`, in full.
- [required] `../student-materials/reversi-starter/CONOPS-sketch.md`, read as a
  player.

## Topic outline

The slide deck (35 slides) is the source of truth for the structure.

| Time | Slides | Topic | Content |
|------|--------|-------|---------|
| 0–6 | 1–6 | Where we are; Project 1 | The recap diagram: the method as one chain, naming the lecture that showed each part (*Specifying a Game*, *Verifying a Game*). A minute on the Reversi demo (https://ase.santoslab.org/reversi/, or slide 3's screenshot). Project 1 in one slide: what you get, what you build, the decisions are yours, the evidence is the history, the due date. The checklist table — each kind, what its audit demands, how it is verified. The brief's seven steps, each with its artifact, rule, and closing commit. |
| 6–18 | 7–15 | Step 1 — the sketch to a concept of operations (Demo 1) | "Read what the sketch says, not what the game does." The sketch's excerpts; §4.2 sorted with the room into stated / implied / missing; "if the sketch does not say it, it is a gap — record it and rule on it, even when you know the answer." The tension: the forfeit bullet beside "when the board is full", and the nine-move wipeout (13 black, 0 white, 51 empty) — the only Reversi finding shown. Three minutes for the room's own gap list. The step-1 prompt, word for word the one *Specifying a Game* typed on tic-tac-toe. The form of rulings and a deferral, on tic-tac-toe; from a ruling to an amendment (RPT-3, DEV-3). Tic-tac-toe's finished `CONOPS.md` (§4.2, §5.1–§5.4, version block). The convergence rule and what is yours to decide. `conops: 0.1 sketch -> 1.0`. |
| 18–28 | 16–19 | Step 2 — the concept of operations to `SPECS.md` | The step-2 prompt; the kinds are pre-picked. What Reversi demands that tic-tac-toe did not — as questions, kind by kind, not answers. Tic-tac-toe's `SPECS.md` §4 (numbered clauses, AUD-5), §5.1 `make_move` (AUD-12), §7.2 (byte-exact, two examples), §9.5 (obligations, not policy). `specs: 1.0.0`. |
| 28–40 | 20–23 | Step 3 — audit, plan, build (Demo 2 begins) | A silence in an earlier step propagates down: the after-game-over silence through five artifacts, read live with the six commands of the demo script's Segment 4. Step 3 in three prompts — audit, plan, build — and what the third does not say. The plan as an artifact: `plans/001-engine-opponent-cli.md` step 1 and *Verification at the end of this build*. `plan: …`, `engine: …`. |
| 40–52 | 24–28 | Step 4 — the suite is a build; the gate | The starter's `process/` already has the test rules *Verifying a Game* added. The test-suite prompt; `plans/002-test-suite.md` step 1 beside §9.5. A test that cites its clause: `test_make_move_rejected_after_game_over` and `test_prompt_human_rejects_invalid_forms`. The gate and the two coverage lines (VER-4, VER-5, VER-8); `grep -n pragma *.py`. Three kinds of change (DEV-2); the amendment first. |
| 52–62 | 29–31 | Step 5 — fixtures: the file, then the loader | The fixture shape (brief §3.1) and the eight kinds (§3.3); a scenario's name cites its clause. The file first, the loader second: `fixtures/README.md` *Known blind spots*, `tests/test_fixtures.py`, `plans/003-fixture-loader.md`. The pass and early-end scenarios verified by hand. VER-7. Three commits, the file's first. |
| 62–72 | 32–35 | Step 6 — the report; required elements; logistics; questions | `PROJECT-1-REPORT.md`'s four items and the five-artifact trace. The required-elements table. Logistics: `process/` and the gate's configuration are adopted, not authored (the same policy as tic-tac-toe's; the starter's `.coveragerc` has `source = .`); due Thursday, October 8, 11:55 pm, and Project 0 still due Thursday, October 1; where to ask. Three questions to think about. |

Blocks sum to 72 minutes; 3 minutes slack.

## Demos

### Demo 1 — Step 1: reading the sketch; the form, on tic-tac-toe

- **Artifacts:** `../demos/lecture-05-reversi-audit/demo-script-lecture-05.md`;
  `../student-materials/reversi-starter/CONOPS-sketch.md` (open in an editor as
  a backup to slide 8's excerpts); `../demos/lecture-05-reversi-audit/expected-gaps.md`
  (the key, for your eyes only: for answering questions and for feedback).
- **Setup (before class):** a fresh copy of the starter with the initial commit
  of the brief's step 0. Optionally, run the step-1 prompt on a private copy to
  know what students will get back; nothing from it is shown. Confirm that
  https://ase.santoslab.org/reversi/ is live; if not, use slide 3's screenshot.
- **Script:** (1) read §1.2 and §4.2 aloud; sort §4.2 with the room into
  stated / implied / missing; (2) the tension, then the nine-move wipeout
  `d3 c3 b3 d2 e1 d6 d7 e3 f4` — 13 black, 0 white, 51 empty, neither can move;
  (3) three minutes for the room's own gap list, on paper; (4) the step-1
  prompt, the same words *Specifying a Game* typed on tic-tac-toe; (5) the form
  of rulings and a deferral on tic-tac-toe (six in a row → five or more wins,
  AUD-1; a win on the last empty square → the win takes precedence, AUD-4; the
  post-game options in §4.3 and §5.1 → three options, AUD-2; quitting mid-game
  → deferred to `BACKLOG.md`, DEV-6); (6) from a ruling to an amendment (RPT-3,
  DEV-3); stop — the Reversi gap list and its rulings are the students' work.
- **Expected outcome:** students can sort a sketch's statements into stated,
  implied, and missing, have a gap list of their own, and have seen the form
  their rulings, deferrals, and amendments take.
- **Fallback:** slide 8's excerpts stand in for the live file; slide 3's
  screenshot for the demo page.

### Demo 2 — Steps 2 to 5, opening the reference game

- **Artifacts:** `../demos/lecture-03-game-demo/reference/` — the finished
  tic-tac-toe game — open in an editor, bookmarked: `CONOPS.md` §4.2 and §5.4;
  `SPECS.md` §4, §5.1, §7.2, §9.5, and the Changelog;
  `plans/001-engine-opponent-cli.md` step 1 and *Verification at the end of
  this build*; `plans/002-test-suite.md` step 1; the after-game-over test in
  `tests/test_game.py`; the parametrized rejection test in `tests/test_main.py`;
  `fixtures/scenarios.json`; `fixtures/README.md` *Known blind spots*;
  `tests/test_fixtures.py`; `plans/003-fixture-loader.md` *What this plan does
  not cover*; `.coveragerc`.
- **Setup (before class):** a venv with `pytest-cov`; the gate confirmed green in
  `reference/` that day (99 collected); `PYTHONDONTWRITEBYTECODE=1`; the six
  commands of the demo script's Segment 4 in a text file; two terminals, large
  font.
- **Script:** per step, *open* the file at the section, *say* the one point,
  and *say* what question the Reversi counterpart must answer. The only live
  commands are the six greps of the five-artifact history (step 3) and the gate
  with the pragma grep (step 4).
- **Expected outcome:** students have seen what each step's artifact looks like
  when finished, and can name the clause each one cites.
- **Fallback:** stills of each bookmarked section; the gate's output from
  rehearsal.

## Discussion prompts

The three questions on slide 35:

1. Which rulings in your gap list are yours, and which are the client's? Where
   does the brief draw the line, and why there?
2. Step 5 requires a scenario containing a pass. Before you trust one your own
   engine generated, what do you check it against, and how — and what does the
   fixture rule (VER-7) say about the file afterwards?
3. The after-game-over silence passed through five artifacts of tic-tac-toe's
   reference. At which step of the brief, and under which rule, would your
   Project 1 have caught it?

## Assigned after class

- Readings (for the next lecture): [required] MCP documentation, core concepts
  and the FastMCP quickstart; [required] the dice-server README
  (`../../weeks-04-07/student-materials/mcp-example/README.md`).
- Project: **Project 1** launched today; due Thursday, October 8, 11:55 pm
  (Project 0 is still due Thursday, October 1). Start with step 0 tonight.

## Instructor notes

- **Dense slides are for reference, not reading aloud:** slide 5 (the checklist),
  slide 8 (the sketch excerpts — show the sketch in an editor if the room is
  large), and slide 33 (required elements). Point at one row each and move on.
- **Cut if running long:** step 4's live gate run compresses to RPT-5's two
  coverage lines on a slide, and step 2's §7.2 beat drops. Never cut the
  five-artifact trace (it is the argument for DEV-8) or the checklist slide.
- **Risks:** many files are opened live — bookmark them, and rehearse the order.
  `pytest-cov` must be on the presentation machine, as for *Verifying a Game*.
  The demo page must be live (the course site published) or slide 3's
  screenshot is used. Nothing from a Reversi gap list, ruling, or design is
  shown: if you ran the step-1 prompt privately, it stays on your machine; the
  only Reversi finding shown is the end-of-game tension. Students who know
  Reversi supply rules the sketch does not state and call them obvious; say
  once: if the sketch does not say it, it is a gap — record it and rule on it,
  even when you know the answer. The convergence rule says how such gaps are
  resolved, not that they are skipped.
- **Variants:** pairs sort a second section of the sketch (§4.3 or §5.1) into
  stated / implied / missing and read out their gaps — no rulings; the class
  checks each against AUDCON-2 and AUD-1.
