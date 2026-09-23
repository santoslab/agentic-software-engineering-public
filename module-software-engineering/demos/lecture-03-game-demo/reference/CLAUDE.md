# Five-in-a-row tic-tac-toe — agent orientation

## What this repository is

A command-line game — tic-tac-toe on a 9-by-9 grid, five in a row to win —
developed by an agent that follows written specifications. The concept of
operations says what the game is for and what a player observes; the behavioral
contract says exactly what the engine, the computer opponent, and the
command-line interface do; a test suite verifies the realization against the
contract, and a coverage gate enforces it on every change.

## Governing documents, in authority order

1. `CONOPS.md` — what the game is for, who plays it, the rules a player can
   observe, the modes, and the scenarios; implementation-free.
2. `SPECS.md` — the behavioral contract, one section per kind: board and
   coordinates; rules of play; display format; input grammar; interaction flow;
   interface contract; example session; and, in §9, the verification
   obligations — what the tests must claim. Derived from 1 and never
   contradicting it (DEV-5).
3. `plans/` — approved plans; derived from 2 and never contradicting it (DEV-9).
4. `fixtures/` — scenario fixtures, once they exist: an executable specification
   derived from 2; never edited to make a test pass (VER-7).

## Process — how work proceeds with respect to the specifications

`process/README.md` states the invariant and maps the files.

The rules in the following documents are always in effect (always on) (loaded with this file):
@process/development-rules.md
@process/reporting.md
@process/verification.md

The rules in the following documents are only invoked when needed (on demand) — run before any plan, after any changes to a specification, or when asked:
`process/spec-audit.md` (AUD) for any specification;
`process/conops-audit.md` (AUDCON) in addition, for the concept of operations.

## Bootstrap rules

1. Read the governing documents and the always-on process documents, in full,
   before any operation.
2. Never modify a governing document or a process document without explicit
   approval; propose changes as an amendment proposal (RPT-3) and wait (DEV-3).

## Commands

- `python main.py` — run the game.
- `pytest` — the test suite.
- `pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100` —
  the algorithmic verifier run as the gate (VER-4); the coverage policy it
  enforces is VER-5.
