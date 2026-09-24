# Plan 003 — the scenario fixtures and their loader

Version: 1.0
Status: **approved** (2026-09-22). Proposed in plan mode and approved before the
first implementing commit (DEV-9).
Realizes: `SPECS.md` 1.2.0 §9.5 — the `fixtures/scenarios.json` obligations.
Governed by: `process/verification.md` 1.3, VER-7 in particular.

This is one of two builds that follow the `SPECS.md` 1.2.0 amendment. The other
realizes the new §5.1 clause on a move after the game is over — the engine
change and the unit test citing that clause — and is not part of this plan. This
plan covers the fixture file and the loader that runs it.

A fixture file is a specification, not a test. It states scenarios and their
expected outcomes in a form that names no language and no method: an
implementation of `SPECS.md` in any language must reproduce them. The loader is
the realization that runs those scenarios against *this* implementation. Keeping
the two apart is the point of the build, and VER-7 is what protects it: the file
is never edited to make a test pass.

## Step 1 — the fixture file and its README

- `fixtures/scenarios.json`, installed as given. Ten game scenarios and four
  rejection scenarios, each named, with the assumed rules carried in the file's
  own `description`, `board_size`, and `win_length` fields so that a reader in
  another language knows what the numbers mean.
- `fixtures/README.md`, stating the rules the fixtures assume (§4.1, §5.1), the
  loader contract both kinds of scenario must satisfy, and the set's known blind
  spots.

Neither file is edited by any later step of this plan or by any test (VER-7). An
expectation that looks wrong is a finding about the pair (fixture,
specification) and is raised as a gap (RPT-1) for a ruling (DEV-4), never
corrected in place.

## Step 2 — `tests/test_fixtures.py`, the loader

Claims §9.5's fixtures obligations. Clauses cited: §4.1, §4.2, §5.1.

Two parametrized test functions, one per kind of scenario, each parametrized by
scenario name so that a failure names the scenario rather than an index:

- **Game scenarios.** From a fresh `Game`, play `moves` in order. Every listed
  move must be accepted. Winner detection runs after each move, and no scenario
  reports a winner before its final move — that assertion is what makes a
  scenario a claim about *when* the win occurs and not merely that it eventually
  does. After the final move the winner equals `expected_winner`, which may be
  `null` for a scenario that ends with no winner (§4.1, §4.2, §5.1).
- **Rejection scenarios.** From a fresh `Game`, play `setup_moves`, all of which
  must be accepted, then submit `attempt`. The attempt returns `False`, and the
  board and `current_player` are both unchanged afterwards — the clause says no
  change of state, so both halves are asserted (§5.1).

The loader holds no expected values of its own. Every number it asserts comes
out of the file, which is what allows the same file to be run by a loader in
another language: that loader is these two functions written in that language.

## Step 3 — the gate and the report

Run the gate (VER-4). The fixture tests run under it with the rest of the suite;
they are not a separate command and not an optional stage.

Report per RPT-5 with the two coverage figures separate (VER-8), and note in the
clause-coverage line which obligations the fixtures claim in addition to the
unit suite — several clauses are now claimed twice, by a unit test and by a
scenario, which is not duplication: the unit test claims it of this
implementation, the scenario claims it of any implementation.

Commit as `fixtures: scenarios.json and loader (VER-7)`.

## What this plan does not cover

- **The blind spots, which are declared rather than closed.** There is no tie
  scenario: an 81-cell board with no run of five is hard to construct by hand,
  so §4.2 is claimed by a unit test with a directly constructed board instead.
  There is no after-game-over rejection scenario; that clause, new in 1.2.0, is
  claimed by a unit test only. Both are written into `fixtures/README.md`,
  because a reader who does not know what a fixture set omits will assume it
  omits nothing (VER-7).
- **The other 1.2.0 build.** The engine change for the after-game-over clause
  and the unit test citing it are separate work under the same amendment.
- **Any port.** Running this file against an engine in another language is a
  later build with its own plan. What this plan produces is the file and one
  loader for it.

## Changelog

- **1.0** (2026-09-22) — Initial; approved as proposed.
