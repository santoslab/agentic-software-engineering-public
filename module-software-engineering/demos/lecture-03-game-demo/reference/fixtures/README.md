# Scenario fixtures

`scenarios.json` is an executable specification of the rules of play and the
interface contract (VER-7): a set of scenarios with expected outcomes that any
implementation of `SPECS.md` — in any language — must reproduce. The loader for
this implementation is `tests/test_fixtures.py`; it runs under the gate (VER-4)
with the rest of the suite. It is the same file as the shared fixtures of the
project unit, so that a port of this engine answers to the same scenarios.

**The file is never edited to make a test pass.** An expectation that looks
wrong is a finding about the pair (fixture, specification): it is reported as a
gap (RPT-1) and ruled on (DEV-4).

## Rules the fixtures assume

A 9-by-9 board; five or more in a row wins (`SPECS.md` §4.1); X moves first;
players alternate on every *accepted* move (§5.1). The file states these in its
`description`, `board_size`, and `win_length` fields.

## Loader contract

- **Games** (`games`): from a fresh game, play `moves` in order. Every listed
  move must be accepted. After each move, run winner detection; no scenario
  produces a winner before its final move. After the final move the winner
  equals `expected_winner` (`"X"`, `"O"`, or `null` for no winner yet).
- **Rejections** (`rejections`): from a fresh game, play `setup_moves` (all
  accepted), then submit `attempt`. The attempt must be rejected, and after the
  rejection the board is unchanged and it is still the same player's turn.

## Known blind spots

- **No tie scenario.** Filling all 81 cells with no five in a row is hard to
  construct by hand. The tie clause (§4.2) is verified by a unit test with a
  constructed board, not by a fixture. A port that wants a tie fixture generates
  one and verifies it against §4.2 before trusting it.
- **No after-game-over rejection.** The clause that a move after the game is
  over is rejected (§5.1, added in 1.2.0) is verified by a unit test only.

A blind spot is part of the fixture set's contract, not a defect: the file says
what it covers, and what it does not cover is verified another way or named as
unverified (VER-8).
