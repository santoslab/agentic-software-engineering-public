# Personal knowledge base — agent orientation

## What this repository is

A personal knowledge base (PKB): a bundle of markdown notes on agentic software
engineering in Google's Open Knowledge Format, as restricted by the format
specification, maintained by an agent that follows written specifications. The
concept of operations says what the PKB is for, who uses it, and which
operations the agent performs; the format specification says what a conformant
note is; the operations document says how each operation is carried out.
Conformance is kept as an invariant while the bundle changes.

At the start there is no bundle and no governing document: there is a sketch of
the concept of operations, written by the user, a process for working with the
specifications, and this loader. The first task is to turn the sketch into
`pkb-conops.md`; the second is to derive `pkb-format-spec.md` from it; the third
is to derive `pkb-operations.md` from both; only then is the bundle scaffolded
under `kb/`, and every note after that is added by an operation.

## Governing documents, in authority order

1. `pkb-conops.md` — purpose, readers, roles, the agent's operations with their
   preconditions and postconditions, conformance, change management;
   implementation-free. Until it exists, `pkb-conops-sketch.md` stands in for it.
2. `pkb-format-spec.md` — what a conformant entry in the bundle is: the rules
   R1…, at the version its changelog states; the OKF profile it adopts and the
   fields it excludes.
3. `pkb-operations.md` — how the agent carries out each operation. Derived from
   1 and 2 and never contradicting them (DEV-5).

The bundle is `kb/` and nothing above it. The governing documents, the process
documents, and everything else at the repository root are outside the bundle.

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

- `python3 check_pkb.py --all` — the algorithmic verifier in whole-bundle mode;
  the gate (VER-4), once it exists.
