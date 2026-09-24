# Plan 001 — the engine, the computer opponent, and the command-line interface

Version: 1.0
Status: **approved** (2026-09-19). Proposed in plan mode and approved before the
first implementing commit (DEV-9).
Realizes: `SPECS.md` 1.1.0.

Three steps, one per module of §5, in dependency order: the engine owes nothing
to the other two, the opponent owes the engine its move list, and the entry
point owes both. Each step names the clauses it realizes. Nothing here decides
what the contract already decides; where the contract does not say, this plan
does not say either, and a question it cannot settle from the contract goes to
`BACKLOG.md` (DEV-6).

## Step 1 — `game.py`, the engine

Realizes §3.1 (layout and coordinates), §3.2 (internal storage), §3.3 (cell
values), §4.1 (the winning line, overlines counting), §4.2 (tie), §4.3
(winner-over-tie precedence), §5.1 (the `Game` interface), and §7.2 (the
byte-exact board format, through `render`).

- `Game.__init__(starting_player='X')` — the board as
  `[[None] * 9 for _ in range(9)]`; `current_player`, `starting_player`,
  `winner = None` (§5.1 attributes, §3.2, §3.3).
- `make_move(row, col) -> bool` — each rejection case §5.1 lists returns `False`
  with no change of state; on success the mark is written at
  `self.board[row - 1][col - 1]` and `current_player` switches (§3.1, §5.1).
- `available_moves() -> list[tuple[int, int]]` — the empty cells, row-major
  (§5.1).
- `check_winner()` — the scan for a run of five or more in each of the four
  directions, setting and returning `winner`; a full board with no run is
  `'tie'`; a run wins over a full board (§4.1, §4.2, §4.3).
- `is_over()` — `winner is not None`; a tie is terminal (§5.1).
- `render() -> str` — the format of §7.2, the same whether the board is empty,
  mid-game, or full (§7.2, §5.1).

No input and no output: every method returns a value (§5.1, "pure logic; no
I/O"). No `reset()` — §5.1 says a new game is a new `Game`.

## Step 2 — `computer_ai.py`, the computer opponent

Realizes §5.2.

- `ComputerAI` as a class of static methods only, one per strategy, each taking
  a `Game` and returning a `(row, col)` pair (§5.2).
- `random_move(game)` — uniform over `game.available_moves()`, using `random`
  (§5.2). The empty-list case is not handled: §5.2 states that it is undefined
  and that the per-game loop exits through `is_over()` before it is reachable.

## Step 3 — `main.py`, the command-line interface

Realizes §5.3 (top-level flow, the two modes, the per-game loop, the post-game
menu), §6.1 through §6.3 (the input grammar), §7.1 and §7.3 (screen spacing and
prompt text), and §8 (the example session, as the walkthrough the build is
checked against).

- The main menu and the post-game menu, verbatim as §5.3 gives them (§5.3, §7.3).
- Move entry and menu entry validated per §6.2 and §6.3; an invalid entry prints
  a short error and re-prompts without advancing the turn (§5.3 per-game loop
  step 4, §6.1).
- The per-game loop in the seven steps §5.3 lists, in that order (§5.3).
- 1-player mode: `Game(starting_player='X')` every game; the human is `X` in the
  first game of a session, and the side the human plays alternates on Play Again
  while `X` still moves first (§5.3). 2-player mode: no alternation (§5.3).
- Strategy selection by name, defaulting to `random_move` (§5.2 extensibility,
  §5.3).
- Every prompt and every message lives here; neither other module prints (§5.1,
  §5.2, §5.3).

## What this plan does not cover

- **The test suite.** §9 states the verification obligations, but the suite that
  claims them is a separate build with its own plan (DEV-9), and the rules it
  must follow — coverage policy, test discipline, fixtures — are not in
  `process/` at this version.
- **`fixtures/`.** Same reason.

## Verification at the end of this build

The algorithmic verifier does not exist yet. The realization is checked by a
human verifier (VER-1) playing one game in each mode against §8's example
session. The completion note says so, and says that no clause of §4 or §7.2 has
been verified by anything but that walkthrough (RPT-5).

## Changelog

- **1.0** (2026-09-19) — Initial; approved as proposed.
