# Tic-Tac-Toe (9x9, 5-in-a-row) — Project Specification

Version: 1.2.1
Status: normative; maintained.

## 1. Overview

A command-line Tic-Tac-Toe variant written in Python. The board is **9×9** and the win condition is **5 or more consecutive same-symbol cells** in any row, column, or diagonal direction. Two modes are supported:

- **1-player** — human vs. computer.
- **2-player** — human vs. human at the same keyboard.

The computer player exposes strategies through a pluggable static-method interface so additional AIs can be added later. Only a uniform random strategy is implemented in this version.

This document is the behavioral contract for the program. All behavior, contracts, and verification obligations live here; how development proceeds with respect to this document — audits, verification, the coverage gate, test discipline, reporting — is specified in `process/`. Implementation and tests must match the spec; tests may assert tighter than the spec but must never assert looser (VER-6).

## 2. File Structure

```
tic-tac-toe/
├── main.py            # Entry point; menus and game flow control
├── game.py            # Game class: board state and game logic
├── computer_ai.py     # Computer player strategies (static class)
├── tests/             # pytest suite (one file per source module)
│   ├── test_game.py
│   ├── test_computer_ai.py
│   ├── test_main.py
│   └── test_fixtures.py   # loader for fixtures/scenarios.json (VER-7)
├── fixtures/
│   └── scenarios.json     # scenario fixtures — an executable specification (VER-7)
├── plans/             # Approved plans, each citing the clauses its steps realize (DEV-9)
├── CONOPS.md          # What the game is for and what a player observes; this document derives from it (DEV-5)
├── SPECS.md           # This document — canonical contract
├── CLAUDE.md          # Agent orientation: the governing documents and the process
├── BACKLOG.md         # Deferred questions (DEV-6)
└── process/           # How development proceeds with respect to this document (DEV, AUD, AUDCON, VER, RPT)
```

## 3. Board Representation

### 3.1 Layout and Coordinates

The board is a 9×9 grid. Players address cells by a **`(row, col)` pair** where:

- **Row** is `1`–`9`, numbered **top to bottom**. Row 1 is the topmost row.
- **Column** is `1`–`9`, numbered **left to right**. Column 1 is the leftmost column.

Coordinates are always written and entered as a single 2-character string with the **row digit first** and no separator. For example, the input `35` means row 3, column 5.

### 3.2 Internal Storage

The board is stored as a **2D list**: a list of 9 row lists, each containing 9 cells. Rows are ordered top to bottom (`self.board[0]` is row 1; `self.board[8]` is row 9). Within a row, columns are ordered left to right (`self.board[0][0]` is row 1 col 1; `self.board[0][8]` is row 1 col 9).

The cell at `(row, col)` lives at `self.board[row - 1][col - 1]`.

This shape is part of the contract: the initial board is `[[None] * 9 for _ in range(9)]`, and tests are permitted to construct board states by direct assignment to `self.board` for setup purposes (see §9.3). The public `Game` API still speaks exclusively in `(row, col)` pairs for normal gameplay.

### 3.3 Cell Values

Each cell holds one of:

- `None` — empty.
- `'X'` — claimed by player X.
- `'O'` — claimed by player O.

## 4. Win Condition

### 4.1 Winning Line

A player wins as soon as they have **5 or more same-symbol cells consecutive** in any of these four directions:

1. **Horizontal** — within a single row.
2. **Vertical** — within a single column.
3. **Diagonal ↘** — increasing row and increasing column.
4. **Diagonal ↗** — decreasing row and increasing column.

Overlines (6, 7, 8, or 9 in a row) **count as a win**. Only the existence of a 5+ consecutive run is required, regardless of cells beyond the line.

### 4.2 Tie

A tie is declared if and only if **the board is completely full AND no winning line exists**. A tie is a terminal state.

### 4.3 Winner-over-Tie Precedence

If a move simultaneously fills the final empty cell AND completes a 5-in-a-row, the **winner wins**. A tie is declared only when no winning line exists on a full board.

## 5. Module Specifications

### 5.1 `game.py`

Defines the `Game` class, encapsulating one game's state and rules. Pure logic; no I/O.

**Attributes**

| Name | Type | Meaning |
|---|---|---|
| `board` | 2D `list` (9 row lists × 9 cells) | Current board state. Each cell is `None`, `'X'`, or `'O'`. Accessed as `self.board[row - 1][col - 1]`. |
| `current_player` | `'X'` or `'O'` | Whose turn it is. |
| `starting_player` | `'X'` or `'O'` | Who started this game. |
| `winner` | `'X'`, `'O'`, `'tie'`, or `None` | Game result; `None` means ongoing. |

**Methods**

- `__init__(self, starting_player='X')` — initialize an empty board (`[[None] * 9 for _ in range(9)]`); set `current_player = starting_player`; set `winner = None`.
- `make_move(self, row, col) -> bool` — apply `current_player`'s mark at `(row, col)`. Returns `True` on success and switches `current_player`. Returns `False` (no state change) if:
  - `row` or `col` is not an `int` in `1`–`9`, OR
  - the target cell is already occupied, OR
  - the game is over (`winner` is not `None`). A move after the game is over is rejected.
- `available_moves(self) -> list[tuple[int, int]]` — returns a list of `(row, col)` pairs for cells that are still empty. Order is row-major (row 1 first, then row 2, etc.).
- `check_winner(self) -> 'X' | 'O' | 'tie' | None` — scans the board for a 5+ run (per §4.1). Sets `self.winner` accordingly and returns it. If no winner is found and the board is full, sets `self.winner = 'tie'`. Otherwise sets `self.winner = None`.
- `is_over(self) -> bool` — returns `self.winner is not None`. A tie is terminal.
- `render(self) -> str` — returns the string representation of the board per §7. The same format applies whether the board is empty, mid-game, or full.

`Game` does **not** expose a `reset()` method. To start a new game, construct a fresh `Game(starting_player=...)`.

### 5.2 `computer_ai.py`

Defines `ComputerAI` as a class with **only static methods**. Each strategy is a separate static method that takes a `Game` instance and returns the chosen move as a `(row, col)` tuple.

**Methods**

- `random_move(game) -> tuple[int, int]` — picks uniformly at random from `game.available_moves()` and returns the chosen pair. Uses Python's `random` module. Assumes at least one move is available; behavior on an empty `available_moves()` list is undefined (the per-game loop in `main.py` exits via `is_over()` before this state is reachable).

**Extensibility**

Future strategies (e.g. `block_threats`, `prefer_adjacent`, `minimax`) follow the same signature: a static method taking a `Game` and returning a `(row, col)` tuple. `main.py` selects a strategy by name; adding a new method requires registering it in the strategy dispatch in `main.py`.

### 5.3 `main.py`

The executable entry point. Owns all I/O: menus, prompts, input validation, and the per-game loop.

**Top-Level Flow**

1. Show the **main menu**.
2. Based on selection, start a 1-player game, a 2-player game, or quit.
3. After a game ends, show the **post-game menu**.

**Main Menu**

```
==== TIC-TAC-TOE ====
1) 1 Player (vs. Computer)
2) 2 Players
3) Quit
```

**1-Player Mode**

- Every game is created with `Game(starting_player='X')`. `X` always moves first.
- In the very first 1-player game of a session, the **human is `X`** and the computer is `O`.
- After each completed game, if the player chooses **Play Again**, the **human's symbol alternates**: game 1 human is `X`; game 2 human is `O` (computer moves first as `X`); game 3 human is `X` again; etc. The starting symbol itself stays `X` — what flips is which side the human plays.
- On the computer's turn, `main.py` calls the selected strategy (default: `random_move`) and applies the returned move.

**2-Player Mode**

- Player 1 is `X`; Player 2 is `O`.
- `X` starts **every** game. The CLI cannot distinguish two humans at one keyboard, so no alternation is attempted; choosing Play Again starts a fresh game with `X` to move.

**Per-Game Loop**

1. Render the board (always; including the empty board at the start of a game).
2. Announce whose turn it is.
3. Prompt for input (or call the computer strategy in 1-player mode).
4. Validate input. On invalid input, print a short error and re-prompt **without** advancing the turn.
5. Apply the move via `Game.make_move`.
6. Call `Game.check_winner`. If `is_over()`, exit the loop.
7. Otherwise, repeat from step 1.

**Post-Game Menu**

After a win or tie is detected:

1. Render the final board.
2. Announce the result (`"X wins!"`, `"O wins!"`, or `"It's a tie!"`).
3. Show:

```
1) Play Again
2) Main Menu
3) Quit
```

- **Play Again** — start a new game in the **same mode**. In 1-player mode the human's symbol flips (so the computer moves first when the human is `O`). In 2-player mode the new game simply starts again with `X`.
- **Main Menu** — return to the main menu. Any 1-player human-symbol alternation **resets**; the next 1-player session starts with the human as `X` again.
- **Quit** — exit the program with `sys.exit(0)`.

## 6. Input Handling

### 6.1 Common Rules

- All user input is read with `input()` and immediately `.strip()`-ed.
- Invalid input prints a short error message and re-prompts in the same context. Invalid input never advances a turn or changes menus.

### 6.2 Move Input

A move input is valid if and only if, **after stripping**, the input is:

- Exactly **2 characters long**, AND
- Both characters are digits in `'1'`–`'9'` (digit `0` is not allowed in either position).

A valid input is parsed as `row = int(s[0])`, `col = int(s[1])`. The cell must then be unoccupied; an already-occupied cell is invalid and re-prompts.

Invalid move forms (each rejected with a re-prompt):

- Length ≠ 2 (e.g. `""`, `"5"`, `"123"`).
- Contains a non-digit (e.g. `"a5"`, `"5x"`).
- Contains a `0` (e.g. `"05"`, `"50"`).
- Points at an occupied cell.

The exact error message wording is not part of the spec; only the behavior (print a brief error and re-prompt) is.

### 6.3 Menu Input

Menu input is valid if and only if, after stripping, the input is a single digit corresponding to one of the listed options. Any other input re-prompts.

## 7. Display Conventions

### 7.1 Screen Spacing

Each new screen (menu render, board render, post-game summary) is preceded by a blank line for readability. Terminal clearing is not performed.

### 7.2 Board Format

The board renders with always-visible row and column labels. Empty cells render as `.`. Occupied cells render as `X` or `O`. The format is **byte-exact** — tests assert against the rendered string verbatim.

**Empty board:**

```
    1 2 3 4 5 6 7 8 9
  +-------------------+
1 | . . . . . . . . . |
2 | . . . . . . . . . |
3 | . . . . . . . . . |
4 | . . . . . . . . . |
5 | . . . . . . . . . |
6 | . . . . . . . . . |
7 | . . . . . . . . . |
8 | . . . . . . . . . |
9 | . . . . . . . . . |
  +-------------------+
```

**Mid-game example** (X at row 3 col 3, O at row 4 col 4):

```
    1 2 3 4 5 6 7 8 9
  +-------------------+
1 | . . . . . . . . . |
2 | . . . . . . . . . |
3 | . . X . . . . . . |
4 | . . . O . . . . . |
5 | . . . . . . . . . |
6 | . . . . . . . . . |
7 | . . . . . . . . . |
8 | . . . . . . . . . |
9 | . . . . . . . . . |
  +-------------------+
```

Format details:

- The column-header line is `    1 2 3 4 5 6 7 8 9` (4 leading spaces; digits 1–9 separated by a single space).
- The top and bottom borders are `  +-------------------+` (2 leading spaces; `+`; 19 dashes; `+`).
- Each body row is `R | C C C C C C C C C |` where `R` is the row digit and each `C` is one of `.`, `X`, or `O`. Cells are separated by single spaces, with one space of padding inside each `|`.
- Lines are joined by `\n`. There is no trailing newline after the final border line.

### 7.3 Prompts

User prompts end with `> ` on the same line so input appears immediately after. For example:

```
Your turn (X). Enter a position (e.g. 35 for row 3 col 5):
> 35
```

## 8. Example Session (1-Player)

```
==== TIC-TAC-TOE ====
1) 1 Player (vs. Computer)
2) 2 Players
3) Quit
> 1

    1 2 3 4 5 6 7 8 9
  +-------------------+
1 | . . . . . . . . . |
2 | . . . . . . . . . |
3 | . . . . . . . . . |
4 | . . . . . . . . . |
5 | . . . . . . . . . |
6 | . . . . . . . . . |
7 | . . . . . . . . . |
8 | . . . . . . . . . |
9 | . . . . . . . . . |
  +-------------------+

Your turn (X). Enter a position (e.g. 35 for row 3 col 5):
> 55

    1 2 3 4 5 6 7 8 9
  +-------------------+
1 | . . . . . . . . . |
2 | . . . . . . . . . |
3 | . . . . . . . . . |
4 | . . . . . . . . . |
5 | . . . . X . . . . |
6 | . . . . . . . . . |
7 | . . . . . . . . . |
8 | . . . . . . . . . |
9 | . . . . . . . . . |
  +-------------------+

Computer (O) plays 27.

    1 2 3 4 5 6 7 8 9
  +-------------------+
1 | . . . . . . . . . |
2 | . . . . . . O . . |
3 | . . . . . . . . . |
4 | . . . . . . . . . |
5 | . . . . X . . . . |
6 | . . . . . . . . . |
7 | . . . . . . . . . |
8 | . . . . . . . . . |
9 | . . . . . . . . . |
  +-------------------+

Your turn (X). Enter a position (e.g. 35 for row 3 col 5):
> ...
```

## 9. Verification Obligations

The test suite is part of the contract: this section states what it must claim. How the suite is run and written — the gate command (VER-4), the coverage policy (VER-5), test discipline and organization (VER-6), fixtures (VER-7), and the separate reporting of clause coverage (VER-8) — is specified in `process/verification.md`. Subsections 9.1–9.4 held that policy in version 1.0.0; they keep their numbers so that existing citations remain valid, and each now points to the rule that replaced it.

### 9.1 Framework and Invocation

Relocated in 1.1.0 to `process/verification.md`, VER-4 (the gate command).

### 9.2 Coverage Policy

Relocated in 1.1.0 to `process/verification.md`, VER-5 (100% branch; the single permitted pragma; unreachable branches recorded by amendment before any pragma).

### 9.3 Test Discipline

Relocated in 1.1.0 to `process/verification.md`, VER-6 (spec-as-floor; every test cites its clause; no tautological tests; direct board setup for setup only).

### 9.4 Test Organization

Relocated in 1.1.0 to `process/verification.md`, VER-6 (tests under `tests/`, one file per source module).

### 9.5 Required Coverage Categories

The following behavior areas must be exercised by the test suite. This is a list of **categories**, not specific test names; structuring within each category is at the implementer's discretion.

**`game.py` — `Game` class:**

- Construction with default and explicit `starting_player`.
- `make_move` success: writes correct cell, switches `current_player`, returns `True`.
- `make_move` failure: out-of-range coordinates, non-`int` coordinates, occupied cell, a move after the game is over. Each case returns `False` and leaves state unchanged.
- `available_moves` on empty, partially-filled, and full boards.
- `check_winner` detects 5-in-a-row in every direction:
  - Horizontal (at least one row).
  - Vertical (at least one column).
  - Diagonal ↘ and ↗ (both directions, including lines that don't pass through the center).
  - At least one **overline (6+)** case to verify §4.1 (overlines count).
- `check_winner` returns `None` for ongoing games.
- `check_winner` detects ties (full board, no 5-line) per §4.2.
- `check_winner` honors winner-over-tie precedence per §4.3.
- `is_over` is `False` initially and `True` for both wins and ties.
- `render` matches the byte-exact format from §7.2 on:
  - An empty board.
  - A mid-game board.
  - A full board (tied or won).

**`computer_ai.py` — `ComputerAI.random_move`:**

- Always returns a `(row, col)` tuple that is currently in `game.available_moves()`. Exercise with partially-filled boards, not just empty ones (a test on an empty board does not verify the "must be available" contract).

**`main.py` — flow and I/O:**

- Each main-menu choice branch (1-player, 2-player, Quit).
- Each post-game-menu choice branch (Play Again, Main Menu, Quit) in both 1-player and 2-player modes.
- 1-player human-symbol alternation across consecutive Play Again selections (§5.3).
- 1-player human-symbol alternation **reset** after Main Menu (§5.3).
- Invalid move input is rejected and re-prompted for each invalid form listed in §6.2 (length ≠ 2, non-digit, contains `0`, occupied cell).
- Invalid menu input is rejected and re-prompted (§6.3).
- Board is rendered each turn during the per-game loop (§5.3 step 1) — assertable via `capsys`.
- Result announcement strings: `"X wins!"`, `"O wins!"`, and `"It's a tie!"` (§5.3 post-game menu).
- Quit branches raise `SystemExit` (testable with `pytest.raises(SystemExit)`).

**`fixtures/scenarios.json` — the loader (`tests/test_fixtures.py`):**

- Every game scenario: each listed move is accepted, no winner is reported before the final move, and the winner after the final move equals `expected_winner` (§4.1, §4.2, §5.1).
- Every rejection scenario: after the setup moves, the attempt returns `False` and leaves the board and `current_player` unchanged (§5.1).
- The fixture file is never edited to make a test pass (VER-7); its stated blind spots are part of its contract.

## 10. Future Extensions (Out of Scope for Initial Build)

- Smarter AI strategies in `computer_ai.py` — examples: `block_threats` (detect opponent's 3/4-in-a-row and block), `prefer_adjacent` (cluster near existing stones), or a depth-bounded `minimax`. On a 9×9 board with 5-in-a-row, `random_move` is essentially unbeatable for the computer, so smarter strategies are the natural next addition.
- Difficulty selection in the main menu (choose which strategy the computer uses).
- Persistent score tracking across games in a session.
- Configurable board sizes and win lengths.

## Changelog

- **1.2.1** (2026-09-24) — §2: `plans/` and `CONOPS.md` listed. Both existed in the repository and are named in `CLAUDE.md` as governing documents; the file structure had not caught up. No behavior specified or unspecified by this change.
- **1.2.0** (2026-09-22) — §5.1: `make_move` returns `False` with no state change once the game is over. Version 1.1.0 was silent on a move after the game is over; the ruling (DEV-4) is that such a move is rejected. This is a change of specified behavior (DEV-2 (c)): the clause is added here first, and the engine change and the test citing this clause follow it. §9.5: the obligation added; the loader for `fixtures/scenarios.json` added. §2: `fixtures/` and `tests/test_fixtures.py` listed.
- **1.1.0** (2026-09-19) — §9 retitled *Verification Obligations*; §9.1–§9.4 relocated to `process/verification.md` (VER-4 through VER-6) with pointers left in place so that citations such as "SPECS §9.3" still resolve; §1 and §2 updated for `process/` and `BACKLOG.md`. Behavior unchanged.
- **1.0.0** — The specification as received (Attempt2, 2026-05-27).
