# Quickstart: validating Five-in-a-Row

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

How to check, once the feature is built, that it conforms to its specification. Paths
are relative to the project root (`SpecKit/TicTacToe/`).

## Prerequisites

- Python 3.12 or later (`python3 --version`).
- `uv` (`uv --version`). Without `uv`: `python3 -m venv .venv && .venv/bin/pip install -e
  . pytest`, then use `.venv/bin/pytest` and `.venv/bin/five-in-a-row` below.

## 1. Automated evidence

```sh
uv run pytest
```

Expected: all tests pass, and `reports/conformance.md` is written
([research.md R7](research.md#r7-conformance-evidence-and-reports-constitution-principles-i-and-v)).
Open it and confirm every FR, SC, and acceptance-scenario ID from `spec.md` has at least
one passing test. Any row marked **no evidence** is a gap to close before the feature is
called done.

Run one module's evidence on its own:

```sh
uv run pytest tests/engine      # rules — contracts/engine.md
uv run pytest tests/opponent    # computer opponent — contracts/opponent.md
uv run pytest tests/cli         # menus, prompts, transcripts — contracts/cli.md
uv run pytest tests/test_architecture.py   # dependency rule (research.md R3)
```

## 2. Manual walkthroughs

Start the game with `uv run five-in-a-row`. Each walkthrough follows a user story's
*Independent Test* in the spec; tick it off when the observed behavior matches.

| # | Walkthrough | Expected | Spec |
|---|-------------|----------|------|
| M1 | Choose `2`. Play X at `5 1`,`5 2`,`5 3`,`5 4`,`5 5`, and O anywhere not on row 5 between them. | Board redrawn after each move; prompt names the mark; after X's fifth: "X wins!" and the play-again menu. | US1 |
| M2 | At the play-again menu choose `1`, then type `0 3`, `abc`, `5`, then a used square. | Each rejected with the right reason; board unchanged; same mark asked again. | FR-005, Edge Cases |
| M3 | In the same game type `m`. | No result shown; start menu appears. | FR-018, US3-5 |
| M4 | Choose `1`. Play until the game ends. | You are X and move first; after each computer move a line names its row and column and the board is redrawn; result names you or the computer. | US2 |
| M5 | Choose `1` (play again). | You are now O; the computer moves first without input. Play again once more: you are X. | FR-013, US2-5, US2-6 |
| M6 | Choose `2` (back to start menu), then `1`. | You are X again. | US2-7 |
| M7 | From the start menu type `7`, then `3`. | `7` rejected and the menu redrawn; `3` ends the program. | FR-016, FR-017 |
| M8 | Start the game and press Ctrl-D at the menu; start again and press Ctrl-C mid-game. | One-line goodbye, no traceback. | FR-020, US3-6 |

A draw is impractical to reach by hand on a 9×9 board; it is covered by a scripted
session in `tests/cli` and by engine tests.

## 3. Timing

SC-001 (first move within 15 s of launch) and SC-005 (board and prompt within 1 s of a
computer move) are checked during M4 by eye; the program does no work that could approach
either limit.
