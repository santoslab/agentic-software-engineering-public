# Contract: Command-line interface

**Module**: `five_in_a_row.cli` | **Depends on**: `engine` and `opponent` public APIs

The CLI is the only module that talks to the player. It owns menus, prompts, input
parsing, board drawing, and the session (mode, and which mark the human holds against the
computer). It holds no game rules: every move goes through `GameState.play`, and every
computer move comes from an `Opponent`.

**Normative vs. illustrative.** The numbered rules (**C-n**) are binding and are what the
tests check. The sample screens are illustrative: tests match the facts a rule requires
(e.g. "names the square"), not exact spacing or wording.

## 1. Launch

```text
five-in-a-row            # console script installed by the package
python -m five_in_a_row  # equivalent
```

No arguments, no configuration, no files read or written. Exit status 0 on every normal
exit, including quit, end of input, and interrupt.

**Entry point for tests**: `five_in_a_row.cli.run(stdin: TextIO, stdout: TextIO,
opponent_factory: Callable[[], Opponent] = RandomOpponent) -> int`. The console script
calls it with the real terminal streams.

## 2. Start menu (FR-014, FR-016, FR-017)

```text
Five-in-a-Row — 9×9, five or more in a line wins.

  1  Play the computer
  2  Play a friend
  3  Quit

Choose 1, 2 or 3:
```

- **C-1** The start menu offers exactly these three choices, selected by typing `1`, `2`
  or `3` (surrounding spaces ignored).
- **C-2** Any other entry prints a one-line message saying the entry was not a choice and
  shows the same menu again.
- **C-3** `3` ends the program.
- **C-4** `1` sets the session to vs-computer with the human as X; `2` sets two-player.
  Either starts a new game.

## 3. Playing a game

```text
    1 2 3 4 5 6 7 8 9
 1  . . . . . . . . .
 2  . . . . . . . . .
 3  . . . . . . . . .
 4  . . . . . . O . .
 5  . . . . X . . . .
 6  . . . . . . . . .
 7  . . . . . . . . .
 8  . . . . . . . . .
 9  . . . . . . . . .

Computer (O) plays row 4, column 7.
X to move — type row and column (e.g. 4 7), or m for the menu:
```

- **C-5** The board is drawn at the start of every game and after every accepted move,
  human or computer. The drawing shows every mark, row numbers 1–9 down the left and
  column numbers 1–9 across the top, row 1 at the top (FR-006, FR-004).
- **C-6** Before each human move the prompt names the mark to move (FR-007) and says how to
  enter a square and how to leave the game (FR-018). In vs-computer games the prompt may
  also say "you"; it must still name the mark.
- **C-7** Move entry: two integers, row then column, separated by one or more spaces, or by
  a comma with optional spaces around it; leading/trailing spaces ignored (FR-004). E.g.
  `4 7`, `4,7`, ` 4 , 7 ` all mean row 4, column 7.
- **C-8** Rejected entries print one line naming the reason, leave the board unchanged,
  and ask the same mark again (FR-005, SC-006). Reasons:
  - **out of range** — two integers, not both 1–9;
  - **occupied** — the square already holds a mark;
  - **unreadable** — anything else that is not the leave-game command.
- **C-9** Leave-game command: `m` or `M` (surrounding spaces ignored) at any move prompt.
  The game is abandoned with no result line, and the start menu is shown (FR-018).
- **C-10** On the computer's turn no input is read. The CLI asks the opponent for a
  square, plays it, prints one line naming the computer's mark and the square's row and
  column, and redraws the board (FR-012, FR-019). The board and next prompt appear within
  1 second (SC-005).
- **C-11** Vs-computer: the human holds the session's `human_mark`; X always moves first,
  so when the human is O the computer moves first without input (FR-002, FR-013).

## 4. Game over (FR-009, FR-010, FR-013, FR-015)

```text
X wins!          (two-player)           You win! (X)       (vs computer, human won)
It's a draw.                            The computer wins! (O)

  1  Play again
  2  Back to the start menu

Choose 1 or 2:
```

- **C-12** When a move wins, the final board is drawn and then one result line naming the
  winner: the mark in two-player games; "you" or "the computer", with the mark, in
  vs-computer games (FR-009). No further move is requested.
- **C-13** When a move fills the board without a win, the final board is drawn and then a
  result line saying the game is a draw (FR-010).
- **C-14** Then the game-over menu offers `1` play again and `2` back to the start menu;
  other entries are handled as in C-2 (FR-015, FR-017).
- **C-15** Play again starts a new game in the same mode. Vs-computer: the human's mark
  flips (X → O or O → X) on every play again (FR-013). Two-player: the game starts with X
  as always; no swapping is tracked (spec Assumptions).
- **C-16** Back to the start menu ends the session; choosing `1` there again starts with
  the human as X (FR-013).

## 5. End of input and interrupt — *pending proposal P1*

- **C-17** If input ends (EOF) or the player interrupts (Ctrl-C) at any prompt, the
  program prints a one-line goodbye and exits with status 0, without a traceback.

This rule implements proposed specification correction P1
([research.md](../research.md#proposed-specification-corrections)). It is not yet in the
spec and is not to be implemented until the developer accepts it.

## Evidence expected (tests in `tests/cli/`)

Tests call `run()` with a scripted input stream, a capturing output stream, and a seeded
or scripted opponent, and assert on the transcript.

| Rules | Spec IDs |
|-------|----------|
| C-1 – C-4 | FR-014, FR-016, FR-017, US3-1, US3-4, US1-1, US2-1 |
| C-5, C-6 | FR-006, FR-007, FR-018 |
| C-7, C-8 | FR-004, FR-005, SC-006, Edge Cases |
| C-9 | FR-018, US3-5 |
| C-10, C-11 | FR-012, FR-019, FR-013, US2-2, US2-5, US2-6 |
| C-12 – C-16 | FR-009, FR-010, FR-013, FR-015, US2-4, US2-7, US3-2, US3-3 |
| full scripted sessions (X wins, O wins, draw) | US1 independent test, SC-003 |
| C-17 | proposal P1 |
