# Plan 002 — the test suite

Version: 1.0
Status: **approved** (2026-09-20). Proposed in plan mode and approved before the
first implementing commit (DEV-9).
Realizes: `SPECS.md` 1.1.0 §9 — the verification obligations.
Governed by: `process/verification.md` 1.3. VER-5 through VER-8 were added by
amendment on 2026-09-19, before this plan was written, because a suite cannot be
judged against rules that are settled after it exists.

A test suite is a build, so it gets a plan like any other (DEV-9). What it
realizes is §9: that section does not describe the game, it lists what the tests
must claim about the game. Each step below names the obligations of §9.5 it
takes on and the clauses its tests will cite (VER-6), so that the plan can be
checked against §9.5 before a line of test code is written.

Four files, one per source module plus the loader for the suite itself, per
VER-6's organization rule. The gate (VER-4) runs at the end of the last step,
not once per step.

## Step 0 — the test harness

- `pytest.ini` with `testpaths = tests`.
- `tests/__init__.py`, and `tests/conftest.py` placing the repository root on
  `sys.path` so that `game`, `computer_ai`, and `main` import without
  installation.
- `requirements-dev.txt`: `pytest`, `pytest-cov`. The gate's `--cov` flags do
  not parse without `pytest-cov`, so it is a dependency of the gate and not an
  optional extra.

No obligations are claimed by this step. It exists so that the three that follow
can be run.

## Step 1 — `tests/test_game.py`

Claims every obligation §9.5 lists under `game.py`. Clauses cited: §3.1, §3.2,
§3.3, §4.1, §4.2, §4.3, §5.1, §7.2.

- Construction with the default `starting_player` and with an explicit one
  (§5.1).
- `make_move` on success: the mark is written at the cell §3.1's coordinates
  name, `current_player` switches, the return is `True` (§3.1, §5.1).
- `make_move` on failure, a test for each case §5.1 lists — a coordinate that
  is not an `int`, a coordinate outside 1–9, and an already-occupied cell. The
  first two are parametrized over a range of bad values rather than written out
  one per function. Each asserts `False`, and each also asserts that the board
  and `current_player` are unchanged, because "no state change" is half of what
  the clause says (§5.1).
- `available_moves` on an empty board, a partly filled board, and a full board
  (§5.1).
- `check_winner` finding a run in each direction §4.1 names: horizontal,
  vertical, diagonal down-right, diagonal up-right. At least one of these uses
  a line that does not pass through the centre, so that an implementation
  scanning only the main diagonals fails (§4.1).
- `check_winner` on an overline: a run longer than five still wins (§4.1). This
  is the obligation §9.5 calls out explicitly, and it is worth noting that the
  engine will have no branch of its own for it — the clause is satisfied
  incidentally by the five-window scan, so only a test that claims §4.1 records
  that the program makes this promise.
- `check_winner` returning `None` on an empty board and on a board holding runs
  shorter than five (§4.1).
- `check_winner` returning `'tie'` on a full board with no run (§4.2), and
  returning the winner rather than `'tie'` on a full board that holds one
  (§4.3).
- `is_over` false on a new game, true after a win, true after a tie (§5.1).
- `render` byte-exact against §7.2 on an empty board, a mid-game board, and a
  full board. The expected strings are written from §7.2 and not from the
  output of `render` (§7.2, VER-6).

Direct assignment to `board` is used to reach a position, which VER-6 permits
for setup. Every assertion about an operation — a move, a turn change, the
available list — goes through the public method, because the claim is about
behavior.

## Step 2 — `tests/test_computer_ai.py`

Claims §9.5's obligation for `ComputerAI.random_move`. Clause cited: §5.2.

- The returned pair is a member of `game.available_moves()`, checked on a partly
  filled board, on a board with a single cell remaining, and across a hundred
  partly filled boards.

The obligation is membership, which is a property that must hold on every call.
It is not a claim about the distribution, and no test asserts one; §5.2 says
uniformly at random, but a test that checks uniformity would fail at random and
is out of scope for this suite. The many-calls test uses partly filled boards
because on an empty board every position is available, so the test would pass
against an implementation that ignored `available_moves()` altogether. Each
test's docstring records that reasoning.

## Step 3 — `tests/test_main.py`

Claims every obligation §9.5 lists under `main.py`. Clauses cited: §5.3, §6.1,
§6.2, §6.3, §7.3.

- Each main-menu branch: 1-player, 2-player, Quit (§5.3).
- Each post-game-menu branch — Play Again, Main Menu, Quit — in both modes
  (§5.3).
- The 1-player human-symbol alternation across consecutive Play Again
  selections, and its reset after a return to the main menu (§5.3).
- Invalid move input rejected and re-prompted, one parametrized test carrying
  every form §6.2 lists — wrong length, non-digit, containing `0`, occupied
  cell — in the order §6.2 lists them, so a reader can check the test against
  the clause item by item (§6.1, §6.2).
- Invalid menu input rejected and re-prompted (§6.3).
- The board rendered on every turn of the per-game loop, asserted through
  `capsys` (§5.3).
- The three result announcements, each matched as an exact string in the
  captured output: `"X wins!"`, `"O wins!"`, `"It's a tie!"` (§5.3, §7.3).
- The quit branches raising `SystemExit`, asserted with `pytest.raises` (§5.3).
  VER-5 permits no pragma here: `sys.exit` paths are reachable by a real test
  and must be reached by one.

Input is supplied by monkeypatching `input`; output is captured with `capsys`.
Neither is a change to `main.py`, which keeps every prompt and every message.

## Step 4 — the gate and the report

Run the gate (VER-4):

```sh
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100
```

VER-5 requires 100% branch coverage with exactly one pragma, on the entry
point's `__main__` guard. If any other branch proves unreachable, it is recorded
by amendment before a pragma is written for it — the plan does not authorize a
pragma in advance.

Report per RPT-5, with the two coverage figures reported separately as VER-8
requires: branch coverage from the gate, and clause coverage — which obligations
of §9.5 are claimed by at least one test and which are not — read off the
citations in the suite.

Commit as `tests: suite per SPECS 9 (VER-4 green)`.

## What this plan does not cover

- **The fixture loader.** §9.5 at this version has no fixtures subsection and
  `fixtures/` does not exist. Both arrive with `SPECS.md` 1.2.0 and are planned
  separately.
- **Auditing the suite against the specification.** The gate compares code
  against tests. Whether the tests read the clauses correctly is a judgment
  clause under VER-2, settled by a human or agent verifier reading §9 beside the
  suite, not by this build.

## Changelog

- **1.0** (2026-09-20) — Initial; approved as proposed.
