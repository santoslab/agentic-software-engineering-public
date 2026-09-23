# Reversi — agent orientation

## What this repository is

A command-line Reversi — an 8-by-8 board, discs of two colors, captures by
flanking — developed by an agent that follows written specifications. At the
start there is no code and no behavioral specification: there is a sketch of the
concept of operations (`CONOPS-sketch.md`), and there is a process for working
with the specifications. The first task is to turn the sketch into `CONOPS.md`;
the second is to derive `SPECS.md` from it; only then is anything built, and
what is built is verified by a test suite and held to a coverage gate.

## Governing documents, in authority order

1. `CONOPS.md` — what the game is for, who plays it, the rules a player can
   observe, the modes, and the scenarios; implementation-free. Until it exists,
   `CONOPS-sketch.md` stands in for it.
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

- `python main.py` — run the game, once it exists.
- `pytest` — the test suite, once it exists.
- `pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100` —
  the algorithmic verifier run as the gate (VER-4); the coverage policy it
  enforces is VER-5.
