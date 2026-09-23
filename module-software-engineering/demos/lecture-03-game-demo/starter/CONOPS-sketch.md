# Concept of Operations — Five-in-a-Row Tic-Tac-Toe (sketch)

Version: 0.1 (sketch)
Status: my general idea, written down in one sitting; not reviewed; nothing built.

*I am using the ConOps skeleton from Lecture 02. Sections 2, 3, and 6 only apply
when you are improving a system that already exists. Here the existing system is
ordinary 3-by-3 tic-tac-toe, so I have kept 2 and 3 but short, and skipped 6 for
now. Where I have not decided something I have written a question or "TBD" rather
than guessing.*

## 1. Scope

### 1.1 Identification

A text-based tic-tac-toe variant on a bigger board, playable alone or with a
friend.

### 1.2 System Overview

The general idea: tic-tac-toe, but on a 9-by-9 grid, and you need five in a row to
win instead of three. You play at a keyboard in a terminal. You can play against
the computer, or two people can play at the same keyboard, taking turns. The
program draws the grid, asks whose turn it is, and tells you when someone has won.

You pick a square by typing where you want to go — its row and column.

### 1.3 Document Overview

TBD — fill in last.

## 2. Current Situation *(optional section — kept because a baseline exists)*

Ordinary 3-by-3 tic-tac-toe. Once you know the trick, every game is a draw, and
you need another person present to play at all.

## 3. Justification for and Nature of the Changes *(optional section)*

Two changes: a much bigger board with a longer winning line, so games stop being
automatic draws; and a built-in computer opponent, so one person can play alone.

## 4. Concept for the Proposed System

### 4.1 Objectives

- Quick to start; easy to learn by watching one game.
- Games that are actually contested.
- The program does the bookkeeping: draws the board, keeps track of turns, spots
  the winner.

### 4.2 Operational Policies and Constraints

Rules a player would see:

- Two marks, X and O. X goes first.
- Players take turns, one mark per turn, on an empty square.
- Five in a row wins — across, down, or on a diagonal.
- If the board fills up and nobody has five in a row, it is a draw.

Not decided yet: against the computer, who goes first — always me? And does that
change if we play again?

### 4.3 Modes of Operation

- A start menu: play the computer, play a friend, or quit.
- Playing: the board is drawn, someone moves, repeat until the game ends.
- When the game ends: show the result, then let you play again or go back to the
  start menu.

### 4.4 User Classes and Actors

- Me, playing alone against the computer.
- Me and a friend at one keyboard.
- The computer opponent. For now it just picks a random empty square — I want to
  play the game before I make it clever.

### 4.5 Operational Environment

A terminal window and a keyboard. It runs on my laptop.

## 5. Operational Scenarios

### 5.1 Playing the computer

I start the program and pick "play the computer." I get an empty grid. I type a
square, my X appears, the computer puts an O somewhere, and we go back and forth
until one of us gets five in a row. The program tells me I won and asks whether I
want to play again or quit.

(Probably need a two-player walkthrough too. And a draw? Not sure a draw is even
realistic on a board this big.)

## 6. Summary of Impacts

*(skipped — optional section; it is a game, there is nothing organizational to
say)*

## 7. Analysis of the Proposed System

- Benefits: TBD.
- Limitations: the computer is not smart. Nothing is saved between games.
- Alternatives considered: I thought about 15-by-15 (like gomoku) but that seemed
  like too much to look at in a terminal.

## 8. Future Operational Capabilities

- A smarter computer opponent.
- Maybe a running score if you play several games in a row.

## 9. Glossary

TBD. Words I keep using and should pin down: square / cell, mark, line, draw /
tie, rematch.
