# Note set — agent orientation

## What this repository is

A set of markdown study notes maintained by an agent that follows a written
specification. At the start there are no notes: there is a specification, and
there is a process for working with the specification.

## Governing documents, in authority order

1. `note-format-spec.md` — what a conformant note is: rules R1–R6.

## Process — how work proceeds with respect to the specification

The rules in the following documents are always in effect (always on) (loaded with this file):
@process/reporting.md
@process/verification.md

The rules in the following document are only invoked when needed (On demand) — run before any plan, after any changes to the specification, or when asked:
`process/spec-audit.md` (AUD).

## Bootstrap rules

1. Read the governing documents and the always-on process documents, in full,
   before any operation.
2. Never modify a governing document or a process document without explicit
   approval; propose changes as an amendment proposal (RPT-3) and wait.

## Commands

- `python3 check_notes.py --all` — the algorithmic verifier (VER-1), once it exists.
