# Note set — agent orientation

## What this repository is

A set of markdown study notes maintained by an agent that follows written
specifications. The concept of operations says what the set is for, who uses it,
and which operations the agent performs; the format specification says what a
conformant note is. Conformance is kept as an invariant while the set changes.

## Governing documents, in authority order

1. `note-set-conops.md` — purpose, roles, the agent's operations (O1–O3) with
   their preconditions and postconditions, conformance, change management.
2. `note-format-spec.md` — what a conformant note is: the rules R1…, at the
   version its changelog states.
3. `note-set-operations.md` — how the agent carries out each operation. Derived
   from 1 and 2 and never contradicting them (DEV-5); created by this project's
   first operation.

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

- `python3 check_notes.py --all` — the algorithmic verifier in whole-set mode;
  the gate (VER-4), once it exists.
