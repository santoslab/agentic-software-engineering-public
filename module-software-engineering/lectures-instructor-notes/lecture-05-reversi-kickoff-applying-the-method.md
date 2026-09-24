# Lecture 05 — Reversi Kickoff: Applying the Method

> **Unit:** module-software-engineering · **Module week 3, meeting 1 of 2** · 75 minutes
>
> **Thesis:** The brief is the method you watched, on a game you were handed.
> This lecture reads its Phase 1 in order and opens, at each step, the artifact
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

Assigned at Lecture 04:

- [required] The Project 1 brief, `../project-1-reversi-brief.md`, in full.
- [required] `../student-materials/reversi-starter/CONOPS-sketch.md`, read as a
  player.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–6 | Where we are: one method, six steps | The specification-family table as a checklist, one row per kind, each with the AUD rule that audits it and the VER row that verifies it. The tag ladder `t0`…`t5` is the brief's steps 0–5; step 6 closes. The brief's §2 headings on screen: today reads them in order and opens the reference artifact at each. |
| 6–18 | Step 1 — the sketch to a concept of operations (Demo 1, from captures) | Read §1.2 and §4.2 of the sketch aloud; stated / implied / missing; the tension — "the board is full" as the end, beside forced forfeits that mean it may never fill (AUD-2). The prompt as printed in the brief; the captured RPT-1 list; four rulings (end condition, opening, pass, flips) and one deferral (hints, DEV-6); one ruling in the RPT-3 form, *awaiting approval*; stop — the rest is step 1. Open `reference/CONOPS.md` §4.2 and §5.4: a policy as a player observes it; every policy in a scenario (AUDCON-3); the version block yours must carry (AUDCON-6). The convergence rule. `conops: 0.1 sketch -> 1.0`. |
| 18–28 | Step 2 — the concept of operations to `SPECS.md` | The round-2 prompt; the kinds are pre-picked. What Reversi demands that tic-tac-toe did not, kind by kind. Open `reference/SPECS.md` §4 (numbered clauses, AUD-5), §5.1 `make_move` (Reversi's postcondition names the flipped set), §7.2 (byte-exact, two examples), §9.5 (obligations, not policy; how much carries over). The transcript export. `specs: 1.0.0`. |
| 28–40 | Step 3 — audit, plan, build (Demo 2 begins) | Why the audit precedes the plan: the silence through five artifacts, read live with the six commands of the L04 script's Segment 4. The two DEV-9 prompts and what the second does not say. Open `plans/001-engine-opponent-cli.md` step 1 (a clause per bullet; the `make_move` bullet) and *Verification at the end of this build* (a human verifier, and RPT-5 says so). `plan: …`, `engine: …`. |
| 40–52 | Step 4 — the suite is a build; the gate | The process set is already the L04 set: the amendment is done for you. The suite prompt; open `plans/002-test-suite.md` step 1 beside §9.5 and check off. Open `test_make_move_rejected_after_game_over` and `test_prompt_human_rejects_invalid_forms`: the docstring cites; setup by assignment, behavior through the operation; one clause, eight forms — Reversi's eight. Run the gate in `reference/`; `grep -n pragma *.py`. RPT-5's two coverage lines (VER-8). DEV-2's three kinds; the amendment first — the standing rule from step 3 on. |
| 52–62 | Step 5 — fixtures: the file, then the loader | The brief's §3.1 beside `reference/fixtures/scenarios.json` (`x-wins-row-overline` is §4.1 as moves); §3.3's eight kinds; the pass and early-end scenarios — engine-generated if need be, hand-verified, and the report says how. Open `fixtures/README.md` *Known blind spots*, `tests/test_fixtures.py` (two functions, no expectations of its own), `plans/003-fixture-loader.md` *What this plan does not cover*. VER-7. Three commits, the file's first. |
| 62–72 | Step 6 — the report; the checklist; logistics; Q&A | `PHASE-1-REPORT.md`'s four items and the five-artifact trace. The required-elements checklist, one slide. The starter's gate configuration: adopted, not authored; it measures every module in the root, so the split is yours. Notation. Due one week from today. Where to ask. Lecture 06 is MCP and launches nothing: finish Phase 1; Stage E is previewed there. |

Blocks sum to 72 minutes; 3 minutes slack.

## Demos

### Demo 1 — Step 1, from captures

- **Artifacts:** `../demos/lecture-05-reversi-audit/demo-script-lecture-05.md`;
  `../student-materials/reversi-starter/` (the sketch, the loader, the L04
  `process/`, `BACKLOG.md`, the gate configuration);
  `../demos/lecture-05-reversi-audit/expected-gaps.md` (the key: 26 decisions,
  standard rulings, *student's choice* marks, nudges).
- **Setup (before class):** a fresh copy of the starter with the initial commit
  of the brief's step 0; the audit rehearsed once with the step-1 prompt exactly
  as the brief prints it; four captures — C1 the RPT-1 list, C2 the rulings on
  gaps 1, 2, 5, and 6, C3 the deferral and `BACKLOG.md` after it, C4 the RPT-3
  proposal marked *awaiting approval*. Nothing beyond C4 is captured: a Reversi
  `CONOPS.md` 1.0 is the homework and is never shown.
- **Script:** (1) three minutes for the room's own gap list; (2) the prompt, on
  screen, as the brief prints it; C1; (3) compare — what the room found and the
  agent did not, and the reverse; (4) C2, each ruling in a sentence, naming the
  document it belongs in; C3, and what a deferral is; (5) C4 — the form every
  ruling takes before a document changes (DEV-3); (6) stop, and say why: the
  rest is step 1.
- **Expected outcome:** students have seen the exact first move of step 1
  performed on their own starter, and have a list of their own to compare with
  the agent's.
- **Fallback:** the key stands in for C1; the rulings are in the demo script.

### Demo 2 — Steps 2 to 5, opening the reference game

- **Artifacts:** `../demos/lecture-03-game-demo/reference/` open in an editor,
  bookmarked: `CONOPS.md` §4.2 and §5.4; `SPECS.md` §4, §5.1, §7.2, §9.5, and
  the Changelog; `plans/001-engine-opponent-cli.md` step 1 and *Verification at
  the end of this build*; `plans/002-test-suite.md` step 1; the after-game-over
  test in `tests/test_game.py`; the parametrized rejection test in
  `tests/test_main.py`; `fixtures/scenarios.json`; `fixtures/README.md` *Known
  blind spots*; `tests/test_fixtures.py`; `plans/003-fixture-loader.md` *What
  this plan does not cover*; `.coveragerc`.
- **Setup (before class):** a venv with `pytest-cov`; the gate confirmed green in
  `reference/` that day (99 collected); `PYTHONDONTWRITEBYTECODE=1`; the six
  commands of the L04 script's Segment 4 in a text file; two terminals, large
  font.
- **Script:** per step, *open* the file at the section, *say* the one point,
  and *say* what the Reversi counterpart must state. The only live commands are
  the six greps of the five-artifact history (step 3) and the gate with the
  pragma grep (step 4).
- **Expected outcome:** students have seen what each step's artifact looks like
  when finished, and can name the clause each one cites.
- **Fallback:** stills of each bookmarked section; the gate's output from
  rehearsal.

## Discussion prompts

1. The sketch says the game ends when the board is full, and that a player with
   no move forfeits the turn. Which statement is wrong? (Neither — one is
   incomplete. Which, and how do you know?)
2. Which rulings in your gap list are yours to make, and which are the client's?
   Where does the brief draw that line, and why does it draw it there?
3. Step 5 requires a scenario containing a pass. Before you trust a scenario your
   own engine generated, what do you check it against, and how — and what does
   VER-7 say about the fixture file afterwards?
4. The after-game-over silence passed through five artifacts of the reference.
   At which step of the brief, and under which rule, would your Phase 1 have
   caught it?

## Assigned after class

- Readings (for L06): [required] MCP documentation, core concepts and the
  FastMCP quickstart; [required] the dice-server README
  (`../../weeks-04-07/student-materials/mcp-example/README.md`).
- Project: **Project 1, Phase 1** launched today; due one week from today (date
  per the brief). Start with step 0 tonight.

## Instructor notes

- **Cut if running long:** step 4's live gate run compresses to RPT-5's two
  coverage lines on a slide, and step 2's §7.2 beat drops. Never cut the
  five-artifact trace (it is the argument for DEV-8) or the checklist slide.
- **Risks:** many files are opened live — bookmark them, and rehearse the order.
  `pytest-cov` must be on the presentation machine, as for L04. The captures
  must be taken with the step-1 prompt exactly as the brief prints it, or
  students will see two prompts for one move. Students who know Reversi supply
  rules the sketch does not state and call them obvious; say once that a rule
  the sketch does not state is a finding, whatever the reader already knows,
  and that the convergence rule says how such findings are resolved.
- **Variants:** pairs rule on two gaps each from C1 and read the rulings aloud;
  the class audits each against AUDCON-2 and AUD-1.
