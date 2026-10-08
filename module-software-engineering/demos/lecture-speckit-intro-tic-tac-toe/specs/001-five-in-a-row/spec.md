# Feature Specification: Five-in-a-Row Tic-Tac-Toe

**Feature Branch**: `001-five-in-a-row`

**Created**: 2026-10-08

**Status**: Draft

**Input**: User description: "@../ASE-seed-conops.md" — Concept of Operations sketch for a
text-based tic-tac-toe variant on a 9-by-9 board, five in a row to win, played at a terminal
against the computer or against a friend at the same keyboard.

## Clarifications

### Session 2026-10-08

- Q: Should a player be able to leave a game partway through and go back to the start menu,
  without closing the terminal? → A: Yes — a command typed at any move prompt abandons the
  game and returns to the start menu (FR-018).
- Q: After the computer moves, should the program also say in words which square it took?
  → A: Yes — it names the square (row and column) and redraws the board (FR-019).
- Q: How should a player type a square: both numbers on one line, or one number at a time?
  → A: Row then column on one line, separated by a space or a comma, e.g. `4 7` or `4,7`
  (FR-004).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Two players at one keyboard (Priority: P1)

Two people sit at one keyboard. One starts the program and chooses "play a friend". The
program draws an empty 9-by-9 grid and says it is X's turn. The players take turns typing
the row and column of the square they want; after each move the program redraws the grid
and says whose turn it is. When one player gets five marks in a row — across, down, or on a
diagonal — the program says who won. If the grid fills with no winner, it says the game is
a draw.

**Why this priority**: This is the whole game — board, turns, legal moves, win and draw —
with nothing else. Every other story is built on it, and it is playable on its own.

**Independent Test**: Choose "play a friend" and play complete games by typing moves for
both sides: one where X wins, one where O wins, and one that ends in a draw.

**Acceptance Scenarios**:

1. **Given** the start menu, **When** the player chooses "play a friend", **Then** an empty
   9-by-9 grid is drawn and the program says it is X's turn.
2. **Given** it is X's turn and the square at row 5, column 5 is empty, **When** the player
   enters row 5, column 5, **Then** an X appears in that square and the program says it is
   O's turn.
3. **Given** X has four marks in a row on row 3 at columns 2–5 and column 6 is empty, and it
   is X's turn, **When** X enters row 3, column 6, **Then** the program announces that X has
   won and the game ends.
4. **Given** X has marks at (1,1), (2,2), (3,3), (4,4) and it is X's turn, **When** X enters
   (5,5), **Then** the program announces that X has won (diagonal win).
5. **Given** X has marks at (1,9), (2,8), (3,7), (4,6) and it is X's turn, **When** X enters
   (5,5), **Then** the program announces that X has won (anti-diagonal win).
6. **Given** X has marks on row 7 at columns 1, 2, 4, 5, 6 and column 3 is empty, and it is
   X's turn, **When** X enters row 7, column 3, **Then** the program announces that X has
   won (six in a row counts).
7. **Given** one empty square remains and placing a mark there gives nobody five in a row,
   **When** the player whose turn it is fills it, **Then** the program announces a draw.

---

### User Story 2 - Play against the computer (Priority: P2)

A player alone starts the program and chooses "play the computer". The player and the
computer alternate moves; on the computer's turn it places its mark on an empty square
chosen at random, with no input from the player. The game ends as in User Story 1.

**Why this priority**: Playing alone is one of the two stated ways to use the program, but
it reuses all of User Story 1 and only adds an automatic opponent.

**Independent Test**: Choose "play the computer" and play a game to completion; check that
the computer moves without input, always onto an empty square, and that a win by either side
or a draw is announced.

**Acceptance Scenarios**:

1. **Given** the start menu, **When** the player chooses "play the computer", **Then** an
   empty grid is drawn, the human plays X, and the program asks the human for the first
   move.
2. **Given** it is the computer's turn, **When** the turn begins, **Then** the computer
   places its mark on an empty square without waiting for input, the program states the row
   and column of that square, the board is redrawn showing it, and the turn passes to the
   player.
3. **Given** many computer moves are observed across games, **When** the positions are
   compared, **Then** every computer move is on a square that was empty, and the computer
   does not always choose the same square from the same position.
4. **Given** the computer completes five in a row, **When** its move is placed, **Then** the
   program announces that the computer has won.
5. **Given** a game against the computer in which the human played X has ended, **When** the
   player chooses "play again", **Then** the human plays O, and the computer, as X, makes
   the first move without input.
6. **Given** a game against the computer in which the human played O has ended, **When** the
   player chooses "play again", **Then** the human plays X and is asked for the first move.
7. **Given** any games against the computer have been played, **When** the player returns to
   the start menu and chooses "play the computer" again, **Then** the human plays X.

---

### User Story 3 - Menu, play again, and quit (Priority: P3)

The program opens on a start menu offering "play the computer", "play a friend", and
"quit". When a game ends, the program shows the result and offers "play again" or "back to
the start menu". "Play again" starts a new game in the same mode with an empty grid.

**Why this priority**: These are the transitions between games; useful, but a single game
already delivers the core value.

**Independent Test**: From the start menu, start a game, finish it, choose "play again",
finish that, choose "back to the start menu", then choose "quit" and confirm the program
exits.

**Acceptance Scenarios**:

1. **Given** the program has just started, **When** it is ready for input, **Then** it shows
   exactly three choices: play the computer, play a friend, quit.
2. **Given** a game has ended, **When** the result is shown, **Then** the player is offered
   "play again" and "back to the start menu".
3. **Given** a game in "play a friend" mode has ended, **When** the player chooses "play
   again", **Then** a new game in the same mode begins with an empty grid and X to move.
4. **Given** the start menu, **When** the player chooses "quit", **Then** the program ends.
5. **Given** a game is in progress and the program is asking for a move, **When** the player
   enters the leave-game command, **Then** the game ends with no result announced and the
   start menu is shown.
6. **Given** the program is waiting for any entry (a menu choice or a move), **When** input
   ends or the player interrupts the program, **Then** the program prints a short goodbye
   and ends, without an error trace.

---

### Edge Cases

- **Occupied square**: the player enters a square that already holds a mark. The move is
  rejected, the program says why, the board is unchanged, and the same player is asked again.
- **Out-of-range square**: the player enters a row or column outside 1–9. Rejected as above.
- **Unreadable input**: the player enters something that is not a row and column in the
  form of FR-004 (letters, one number, three numbers, a blank line) and is not the leave-game command (FR-018). Rejected as above.
- **Invalid menu choice**: the player enters something that is not one of the offered menu
  options. The program says so and shows the same choices again.
- **More than five in a row**: a move completes six or more marks in a line, e.g. by
  filling the gap between a run of two and a run of three. This is a win (FR-008).
- **Win on the last square**: the final empty square completes five in a row. This is a win,
  not a draw.
- **Two lines at once**: a single move completes five in a row in two directions. This is
  one win for the player who moved.
- **End of input or interrupt**: the terminal's input ends (e.g. Ctrl-D) or the player
  interrupts the program (e.g. Ctrl-C) at any prompt. The program ends promptly (FR-020).

## Requirements *(mandatory)*

### Functional Requirements

**Board and moves**

- **FR-001**: The game MUST be played on a square grid of 9 rows and 9 columns, all empty
  at the start of each game.
- **FR-002**: The two marks MUST be X and O, and X MUST move first in every game.
- **FR-003**: Players MUST alternate turns, placing exactly one mark per turn.
- **FR-004**: A player MUST choose a square by entering, on one line, its row and then its
  column, each a number from 1 to 9, separated by a space or a comma (e.g. `4 7` or `4,7`
  is row 4, column 7). Row 1 is the top row and column 1 the leftmost column.
- **FR-005**: The system MUST accept a move only onto an empty square within the grid. Any
  other entry, except the leave-game command (FR-018), MUST be rejected with a message
  saying why, leave the board unchanged, and ask the same player again.
- **FR-006**: The system MUST draw the grid, showing every mark and the row and column
  numbers, at the start of the game and after every accepted move.
- **FR-007**: Before each human move the system MUST say whose turn it is, naming the mark.

**End of game**

- **FR-008**: A player MUST win when their move makes five or more of their marks
  consecutive in one line — a row, a column, or either diagonal direction.
- **FR-009**: When a move wins, the game MUST end immediately and the system MUST announce
  the winner.
- **FR-010**: When a move fills the last empty square and does not win, the game MUST end
  and the system MUST announce a draw.

**Opponents and modes**

- **FR-011**: The system MUST offer two ways to play: against the computer, and two people
  at one keyboard taking turns.
- **FR-012**: On its turn the computer opponent MUST place its mark on an empty square
  chosen at random from all empty squares, each equally likely, without player input.
- **FR-013**: In a game against the computer, the human MUST play X (and so move first) in
  the first game started from the start menu. Each time "play again" is chosen, the human
  and the computer MUST swap marks, so the side that moved second in the previous game
  moves first in the next.

**Menus**

- **FR-014**: At startup the system MUST show a start menu offering: play the computer,
  play a friend, quit.
- **FR-015**: When a game ends, the system MUST show the result and offer: play again (same
  mode, new empty grid) or return to the start menu.
- **FR-016**: Choosing "quit" from the start menu MUST end the program.
- **FR-017**: An entry that is not one of the offered menu choices MUST be rejected with a
  message and the same menu shown again.
- **FR-018**: At every prompt for a move, the system MUST accept a leave-game command, and
  MUST say how to enter it. Entering it MUST end the game without a result (no winner, no
  draw) and show the start menu.
- **FR-019**: After every computer move the system MUST state, in words, the row and column
  of the square the computer took, in addition to redrawing the board (FR-006).
- **FR-020**: If input ends or the player interrupts the program at any prompt, the program
  MUST end promptly with a short goodbye message and without an error trace.

### Key Entities

- **Board**: the 9-by-9 grid of squares; each square is empty or holds one mark.
- **Square**: one position on the board, identified by row (1–9) and column (1–9).
- **Mark**: X or O; the symbol a player places.
- **Player**: a side in a game, holding one mark; either a person at the keyboard or the
  computer.
- **Line**: a run of consecutive squares in one direction — across, down, or diagonal.
- **Game**: one play from an empty board to a result; has a mode (vs computer or two
  players), which mark each player holds, the current turn, and a result (in progress,
  X won, O won, draw).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: From launching the program, a player can be making their first move in under
  15 seconds.
- **SC-002**: A person who has watched one complete game can start and finish a game of
  their own without help or written instructions.
- **SC-003**: In every finished game, the announced result (X won, O won, or draw) matches
  the rules in FR-008 and FR-010 — no missed wins, no false wins, no premature draws.
- **SC-004**: Over at least 1,000 computer moves, 100% are onto empty squares; and when the
  computer is given the same position with 10 empty squares 1,000 times, it chooses each of
  the 10 squares at least once.
- **SC-005**: After a computer move, the board is redrawn and the player is prompted in
  under 1 second.
- **SC-006**: 100% of invalid entries (occupied, out of range, unreadable, bad menu choice)
  are rejected without changing the board or losing the player's turn.

## Assumptions

- The program runs in a text terminal on a single laptop; one keyboard is shared in
  two-player mode. No network play, accounts, or saved games.
- A game left with the leave-game command (FR-018) is not "ended" in the sense of FR-015:
  no result is shown and "play again" is not offered. Because it returns to the start menu,
  the next game against the computer starts with the human as X (FR-013).
- "Games that are actually contested" (ConOps 2.1) is not a requirement on this feature:
  the ConOps deliberately makes the computer random for now, so a contested game against
  the computer is a future capability.
- A draw is kept as a rule even though the ConOps doubts it is realistic on a 9-by-9 board.
- In two-player mode the two people decide between themselves who plays X; the program
  does not track or swap who is who across "play again".
- Returning to the start menu ends the series of games against the computer; the next
  "play the computer" starts again with the human as X (FR-013).
- Out of scope (ConOps §4, future capabilities): a smarter computer opponent; a running
  score across games.
- The ConOps glossary is TBD. This spec uses: **square** (not cell), **mark**, **line**,
  **draw** (not tie). "Play again" in this spec is what the ConOps calls a rematch.
