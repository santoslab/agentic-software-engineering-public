# Concept of Operations (ConOps) — Five-in-a-Row Tic-Tac-Toe

*Operational view of the game system. This document describes who uses the
system, why it exists, and how it is operated. It is written from the user's
perspective and is independent of how the system is built. It is self-contained:
all terms it relies on are defined within it.*

Version: 1.0
Status: normative; maintained.

---

## 1. Scope

### 1.1 Identification

This Concept of Operations describes a two-player strategy game: a larger,
deeper variant of the classic game of tic-tac-toe. It is intended to convey, in
plain language, what the game is for, who plays it, and how a session unfolds —
not how it is implemented.

### 1.2 System Overview

The system is a text-based game played at a keyboard. Players take turns placing
their mark on a **9-by-9 grid** of cells. A player wins by forming a line of
**five or more of their own marks in a row** — horizontally, vertically, or
diagonally. The system supports two ways to play:

- **Solo play** — one person plays against a built-in computer opponent.
- **Two-player play** — two people play against each other, taking turns at the
  same keyboard.

The system presents on-screen menus, draws the grid after every move, prompts
the player whose turn it is, checks for a winner automatically, and announces
the result. A player chooses a cell by typing a short **two-digit entry**: the
row first, then the column (for example, `35` means row 3, column 5).

### 1.3 Document Overview

Section 2 describes the familiar game this system grows out of, and its
shortcomings. Section 3 explains the changes this system makes and why. Section 4
presents the operational concept: objectives, the rules players observe, the
modes the system runs in, the people and parties who use it, and the environment
it runs in. Section 5 walks through representative play sessions. Sections 6 and
7 summarize the impact on players and weigh the benefits and limitations.
Section 8 sketches envisioned future capabilities. Section 9 is a glossary.

---

## 2. Current Situation

The everyday version of this game is **standard 3-by-3 tic-tac-toe**: two
players alternately mark cells of a tiny nine-cell grid, each trying to claim
three cells in a row. It is universally known, learned in minutes, and playable
with nothing more than paper and a pencil.

That very simplicity is its limitation:

- **The board is tiny.** With only nine cells, games are over in moments and
  offer little room for planning ahead.
- **Skilled play is a forced draw.** Once both players understand the game,
  almost every match ends in a tie. The game is, in practice, "solved" — there
  is no real contest left.
- **It always needs a present opponent.** A person who wants to play must find
  another person willing to play; there is no way to practice alone.
- **Everything is manual.** Players must draw the grid themselves, keep track of
  whose turn it is, and notice for themselves when someone has won — which is
  easy to overlook or dispute.

The result is a game that is charming but shallow, and that cannot be enjoyed
solo.

---

## 3. Justification For and Nature of the Changes

This system keeps the familiar feel of tic-tac-toe — place a mark, take turns,
make a line — while removing the limitations above. Three changes define it:

1. **A much larger grid and a longer winning line.** The board grows from 9
   cells to 81 (a 9-by-9 grid), and the goal grows from three in a row to
   **five or more in a row**. This opens far more room to maneuver, build
   threats, and block. Forced draws become rare, so games stay a genuine
   contest between players of similar skill.
2. **A built-in computer opponent.** A person can now play alone, against the
   system itself, without needing to find a partner. This makes the game
   available any time, to a single player.
3. **Automated officiating.** The system draws the grid after every move, tracks
   whose turn it is, rejects illegal entries, and detects a win or a tie the
   moment it happens — announcing the outcome. Players never have to track the
   board state or adjudicate a win by hand.

The intent is a game that is as easy to start as the original, but with enough
depth to stay interesting and the convenience of solo play and automatic
refereeing.

---

## 4. Concept for the Proposed System

### 4.1 Objectives

- Let two people, or one person and the computer, play a deeper variant of
  tic-tac-toe at a single keyboard.
- Make a match easy to start, easy to understand, and hard to draw by accident.
- Remove all manual bookkeeping: the system owns drawing the board, enforcing
  the rules, and declaring the result.
- Keep the rules few and observable, so a new player can learn by watching one
  game.

### 4.2 Operational Policies and Constraints

These are the rules a player can directly observe during play:

- **Two marks.** One side plays `X`, the other plays `O`.
- **X always moves first** in every game.
- **Turns strictly alternate.** A player places exactly one mark per turn, in an
  empty cell of their choice.
- **Winning line.** A player wins the instant they have **five or more of their
  own marks in an unbroken line** — along a row, a column, or either diagonal
  direction. A line longer than five (six, seven, and so on) also wins; only the
  existence of an unbroken run of at least five matters.
- **Immediate win.** The game ends the moment a winning line appears, even if
  that same move fills the last empty cell of the grid. A win always takes
  precedence over a tie.
- **Tie.** If the grid becomes completely full and no winning line exists, the
  game ends in a tie. A tie is final.
- **Solo side-alternation.** In solo play, the human plays `X` in the first game.
  If the human chooses a rematch, the side the human plays alternates: `O` in the
  next game (so the computer, as `X`, moves first), then `X` again, and so on.
  Because `X` always moves first, this alternation changes *which side the human
  plays*, not which mark opens the game.
- **Alternation resets at the main menu.** Returning to the main menu clears the
  solo side-alternation; the next solo game again starts with the human as `X`.
- **Two-player play does not alternate sides.** Because the system cannot tell
  the two people apart at one keyboard, the first player is always `X` and the
  second is always `O`; a rematch simply starts again with `X` to move.
- **Invalid entries never cost a turn.** If a player enters something that is not
  a legal move — the wrong length, a non-digit, a position off the grid, or a
  cell that is already taken — the system shows a brief error and asks again. The
  turn does not pass and the board does not change until a legal move is made.

### 4.3 Modes of Operation

The system runs in a small number of clearly separated modes:

- **Main menu.** The entry point. The player chooses solo play, two-player play,
  or to quit.
- **Solo play (vs. computer).** One human against the computer opponent.
- **Two-player play (hot-seat).** Two humans alternating at the same keyboard.
- **In-game turn loop.** Within either play mode: the system draws the grid,
  announces whose turn it is, takes a move (a typed entry from a human, or a
  choice from the computer), validates it, applies it, and then checks for a win
  or tie. This repeats until the game ends.
- **Post-game.** After a win or tie, the system shows the final grid, announces
  the result, and offers three choices: play again (same mode), return to the
  main menu, or quit.

### 4.4 User Classes and Actors

- **Solo player.** A single person who wants to play without a partner. Plays
  against the computer; in the first game holds `X`, and alternates sides on
  each rematch as described in §4.2.
- **Hot-seat pair.** Two people sharing one keyboard, playing against each other.
  One is always `X` (and moves first), the other always `O`. They cooperate to
  pass the keyboard at each turn.
- **Computer opponent.** An automated participant in solo play. In the current
  system it plays a **uniformly random legal move** — it picks, at random, any
  empty cell. It does not plan, threaten, or block. It serves to give the solo
  player a live opponent rather than a strong one.


### 4.5 Operational Environment

- **A single text terminal.** All interaction is through on-screen text and
  keyboard entry. The grid, menus, prompts, and results are all displayed as
  text; the player responds by typing.
- **One session at a time.** The game is played in a single sitting. Nothing is
  saved between sessions: there is no stored history, no saved scores, and no
  account.
- **Local and shared.** The game runs in one place. Two-player play means two
  people at the *same* keyboard; the system does not connect players across
  separate machines or over a network.

---

## 5. Operational Scenarios

The following walkthroughs illustrate typical use from the player's point of
view.

### 5.1 Solo Play to a Win

A player opens the game and is shown the main menu. They choose solo play. The
system draws an empty 9-by-9 grid and announces that it is the player's turn as
`X`. The player types a two-digit entry — say `55` — to place an `X` near the
center. The system redraws the grid showing the new mark, then announces the
computer's move and shows where the computer (playing `O`) placed its mark. Play
continues back and forth, the grid redrawn after every move. The player steadily
builds a line, and on the move that completes five `X` marks in a row, the system
immediately stops the game, shows the final grid, and announces that `X` wins.
The player is then offered to play again, return to the main menu, or quit.

### 5.2 Two-Player Hot-Seat Game

Two friends choose two-player play from the main menu. The system announces the
first player's turn as `X` and draws the empty grid. The first player types their
entry; the system redraws the grid and announces the second player's turn as `O`.
The two pass the keyboard back and forth, each placing a mark on their turn,
reading the redrawn grid to plan their next move. Eventually one player forms an
unbroken line of five of their mark. The system ends the game at once, shows the
final grid, and announces that player as the winner. The pair may start a
rematch — again with `X` to move — return to the menu, or quit.

### 5.3 A Tie Game

In either mode, play can continue until every cell of the grid is filled without
either side ever forming five in a row. When the final empty cell is filled and
no winning line exists, the system declares the game a tie, shows the completely
filled grid, and announces the tie as the result. As with any finished game, the
players are offered to play again, return to the menu, or quit. (On a grid this
large with a five-mark goal, ties are uncommon — they require careful or unlucky
play that blocks every long line.)

### 5.4 Recovering From an Invalid Entry

It is the player's turn. Instead of a valid position they type something the
system cannot accept — for example an empty entry, a single digit, three digits,
a letter, a position that falls outside the grid, or the coordinates of a cell
that is already occupied. The system responds with a short error message and
prompts the player again for the same turn. The board is unchanged and the turn
has not passed. The player then types a valid, empty position, and play proceeds
normally. No invalid entry ever advances the game or alters the grid.

---

## 6. Summary of Impacts

For players, the system changes the experience of tic-tac-toe in several ways:

- **Deeper games.** The larger grid and longer winning line make matches last
  longer and reward planning, blocking, and building multiple threats.
- **Solo play becomes possible.** A person no longer needs a partner present to
  play a game.
- **No manual bookkeeping.** The system draws the board, enforces legal moves,
  and detects wins and ties, so players focus entirely on strategy.
- **A gentle learning curve preserved.** The rules remain few and observable, so
  the deeper game is still easy to pick up.

There are no organizational impacts: the game is used casually by individuals or
pairs, in a single sitting, with no setup, accounts, or saved data.

---

## 7. Analysis of the Proposed System

### 7.1 Benefits

- **Renewed contest.** Moving to a 9-by-9 grid with a five-mark goal makes the
  near-guaranteed draw of classic tic-tac-toe rare, restoring real competition.
- **Always available.** The computer opponent means a single player can always
  start a game.
- **Trustworthy refereeing.** Automatic win and tie detection removes disputes
  and overlooked victories.
- **Low barrier.** Text display and a simple two-digit entry keep the game quick
  to start and easy to learn.

### 7.2 Limitations

- **A weak computer opponent.** The computer currently plays random legal moves;
  it does not plan or block. Against an attentive human it is easy to beat. It
  provides a live opponent, not a challenging one.
- **No saved progress or scores.** Nothing carries over between games or
  sessions; results are not recorded.
- **Single session, single place.** The game is played in one sitting at one
  keyboard. There is no save-and-resume.
- **Two-player means same keyboard.** Two people must share one keyboard; the
  system does not connect separate players or machines.
- **No undo.** Once a legal move is made, it stands; there is no take-back.

### 7.3 Alternatives Considered

- **Keep the classic 3-by-3 board.** Rejected: it is enjoyable but shallow and
  almost always drawn between competent players, which is exactly the limitation
  this system set out to remove.
- **An even larger board or a longer winning line.** A bigger grid or a
  six-or-more goal would add still more depth but also make games longer and
  harder to learn at a glance. The 9-by-9 grid with a five-mark line was chosen
  as a balance between depth and approachability.
- **A strong, planning computer opponent from the start.** Desirable, but a
  simple random opponent is enough to make solo play possible immediately;
  stronger opponents are a natural future addition (see §8) rather than a
  prerequisite.

---

## 8. Future Operational Capabilities

The following capabilities are envisioned but not part of the current system:

- **A smarter computer opponent.** An opponent that blocks the human's emerging
  lines, builds its own threats, or looks several moves ahead — turning solo
  play into a real challenge.
- **Difficulty selection.** Letting the solo player choose how strong the
  computer opponent should be before a game.
- **Score tracking within a session.** Keeping a running tally of wins, losses,
  and ties across the games played in a single sitting.
- **Configurable grid size and winning length.** Letting players choose a
  different board size or a different number-in-a-row to win, so the same system
  can offer easier or harder variants.

---

## 9. Glossary

- **Cell** — one of the squares of the grid, identified by its row and column.
- **Mark / symbol** — the token a side places in a cell; one side uses `X`, the
  other `O`.
- **Grid / board** — the 9-by-9 arrangement of 81 cells on which the game is
  played.
- **Two-digit entry** — how a player names a cell: the row digit followed by the
  column digit, with no space (for example, `35` is row 3, column 5).
- **Five-in-a-row** — the winning condition: five or more of one side's marks in
  an unbroken line along a row, column, or diagonal.
- **Overline** — a winning line longer than five (six or more in a row); it still
  counts as a win.
- **Win** — the state reached when a side forms a five-in-a-row; it ends the game
  immediately and takes precedence over a tie.
- **Tie** — the state reached when the grid is completely full and no side has a
  five-in-a-row; the game ends with no winner.
- **Solo play** — one human playing against the computer opponent.
- **Hot-seat (two-player) play** — two humans playing against each other at the
  same keyboard.
- **Rematch** — starting a new game in the same mode immediately after one ends.
- **Computer opponent** — the automated participant in solo play; currently
  plays a random legal move.

---

## Changelog

- **1.0** (2026-09-19) — Rewritten from the 0.1 sketch after the round-1 audit
  (Lecture 03): third person, all nine sections of the skeleton filled, four
  scenarios, glossary. A version, a status, and this changelog are required of a
  concept of operations by AUDCON-6.
