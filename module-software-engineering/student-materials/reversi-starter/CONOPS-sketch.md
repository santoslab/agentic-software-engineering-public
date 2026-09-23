# Concept of Operations — Reversi (sketch)

Version: 0.1 (sketch)
Status: my general idea, written down in one sitting; not reviewed; nothing built.

*I am using the ConOps skeleton from Lecture 02. There is no existing system here —
this is a new game, not an improvement to one — so sections 2, 3, and 6 do not
apply and I have left them out. Where I have not decided something I have written a
question or "TBD" rather than guessing.*

## 1. Scope

### 1.1 Identification

A text-based version of Reversi (some people know it as Othello) that you can play
alone against the computer or with a friend at one keyboard.

### 1.2 System Overview

Reversi is played on an 8-by-8 board with discs that are black on one side and
white on the other. One player is black, the other is white. The board starts with
a few discs already in the middle, the way the real game does. On your turn you put
down a disc of your color so that one or more of the other player's discs are
trapped in a straight line between your new disc and one you already have; the
trapped discs flip over to your color. The game is about ending up with more discs
of your color than the other player.

The program draws the board in the terminal, tells you whose turn it is, checks
that a move is allowed, does the flipping for you, and counts up at the end. You
say where you want to play by typing the square, like `d3` on a chessboard.

### 1.3 Document Overview

TBD — fill in last.

## 2. Current Situation

*(omitted — no existing system)*

## 3. Justification for and Nature of the Changes

*(omitted — no existing system)*

## 4. Concept for the Proposed System

### 4.1 Objectives

- Quick to start. The rules are simple, but I always get the flipping wrong by
  hand, so the program should do it — and should not let me make a move that is
  not allowed.
- Playable alone.
- Keep score.

### 4.2 Operational Policies and Constraints

Rules a player would see:

- Two colors, black and white. Players take turns placing one disc of their color
  on an empty square.
- A move has to trap at least one of the other player's discs: in a straight line
  — across, down, or diagonally — with your new disc at one end, one of your discs
  at the other, and only their discs in between. Everything trapped flips. If a
  square would trap nothing, you cannot play there.
- If you have no square you can play, you forfeit your turn.
- When the board is full, the discs are counted and whoever has more wins.

Not decided yet: should the program show me where I am allowed to play, or make me
work it out?

### 4.3 Modes of Operation

- A start menu: play the computer, play a friend, or quit.
- Playing: the board is drawn, someone moves, the flips happen, repeat.
- When the game ends: show the count, then let you play again or go back to the
  start menu.

### 4.4 User Classes and Actors

- Me, playing alone against the computer.
- Me and a friend at one keyboard.
- The computer opponent. For now it just picks one of its allowed moves at
  random. Later I would like it to be at least a bit greedy.

### 4.5 Operational Environment

A terminal window and a keyboard. It runs on my laptop.

## 5. Operational Scenarios

### 5.1 Playing the computer

I start the program and pick "play the computer." The board comes up with the
starting discs. I type a square; the program flips the discs I trapped and shows
the board; then the computer plays and I see its flips. At one point I type a
square that traps nothing and the program tells me I cannot play there, so I try
another. Later in the game I have no move at all, the program says so, and the
computer goes again. When the board fills up the program counts — 40 to 24, I win —
and asks whether I want to play again.

(Probably need a two-player walkthrough too.)

## 6. Summary of Impacts

*(omitted — not applicable)*

## 7. Analysis of the Proposed System

- Benefits: TBD.
- Limitations: the computer plays randomly. No taking a move back.
- Alternatives considered: a 6-by-6 board for faster games; I decided to start
  with the real size.

## 8. Future Operational Capabilities

- A computer opponent that takes the move that flips the most discs.
- Choosing the board size.

## 9. Glossary

TBD. Words I keep using and should pin down: disc, flip, trap, forfeit, allowed
move, black / white.
