# Verification (VER)

Version: 1.1
Status: normative; maintained. **Always on.**

This document specifies how conformance between a realization and its
specification is checked: by which kinds of verifier, with what scope, which
clauses each kind may decide, when checks run, and what gate a change must pass.
The keywords MUST, MUST NOT, SHOULD, and MAY carry their RFC 2119 meanings.

## In this repository

| Realization | Specification | Verifiers available |
|---|---|---|
| a note in `notes/` | `note-format-spec.md`, the per-note rules | human; agent; algorithmic — `python3 check_notes.py <note>` |
| `index.md`, with the set of notes | `note-format-spec.md`, the index rule (R6) | human; agent; algorithmic — `python3 check_notes.py --all` |
| the performance of an operation (O1–O3) | `note-set-conops.md` §4 preconditions and postconditions; `note-set-operations.md` | human; agent — the postcondition is confirmed by the checks above and a reading of the result |

The gate (VER-4) is `python3 check_notes.py --all`: exit 0 conformant; 1
violations found; 2 usage error.

## Rules

### VER-1 — Verifiers and scope

Conformance MAY be verified (a) by a **human verifier** — a person reading the
specification and the realization and manually checking the correspondence between the two 
(b) by an **agent verifier** — an agent asked to
check and report — or (c) by an **algorithmic verifier** — a program written to decide
the specification's clauses. These are the three kinds of verifier. Every result
MUST state which verifier produced it and MUST be reported in the form RPT-2,
so that its scope — which verifier, which version of the specification, which
clauses — is explicit.

| | Human | Agent | Algorithmic |
|---|---|---|---|
| Cost per check | minutes of attention | tokens | milliseconds |
| Same result on repeat | not guaranteed | not guaranteed | yes |
| Decides mechanical clauses | yes | yes | yes |
| Decides judgment clauses | yes | yes | no |
| Composable into a gate | no | with effort | yes, via the exit code |

When verification is performed, this doesn't give us a "proof" that the realization
meets the specification.  It only provides some "evidence within a given scope" 
that the verification holds.  Unless we formally prove the verifier correct, 
any verifier can be wrong: it may implement or apply a clause incorrectly, 
run against a stale version of a specification, judge from memory instead of 
from the document, or decide fewer clauses than its output implies. 
The reporting instructions of RPT-2 include reporting on the scope so that
we can see possible gaps.

### VER-2 — Mechanical clauses and judgment clauses

Every clause of a specification MUST be classified as **mechanical** — decidable
by a program from the artifact alone — or **judgment** — requiring a reader's
assessment ("accurately summarizes", "preserving the user's meaning"). The
classification is kept in the table below and MUST be amended whenever the
specification changes. An algorithmic verifier decides mechanical clauses only;
judgment clauses are named as remaining for a human or an agent verifier, never
silently assumed to be covered.

| Clause | Algorithmic | Human or agent |
|---|---|---|
| R1 front-matter block | yes | — |
| R2 fields, including date validity | yes | — |
| R3 H1 placement, and H1 = `title` once amended | yes | — |
| R4 single H1 | yes | — |
| R5 no skipped heading levels | yes | — |
| R6 index consistency | yes (`--all`) | — |
| O2 "preserving the user's meaning" | no | yes |

Clauses added by amendment are classified when they are added (a filename rule
is mechanical; a "SHOULD accurately summarize" clause is judgment).

### VER-3 — When verification runs

A realization MUST be verified: after every operation that creates, changes, or
removes it, before the operation is declared complete (DEV-7); before every
commit that touches it; after any amendment to its specification — everything the
amendment touches is re-checked against the new version, because a pass against
the old version is not a result; and whenever the developer asks.

*Example:* when the format specification moves to a version that adds a required
section, every existing note is re-checked against the new version and migrated
in the same commit. A verifier still implementing the old version would report
them conformant.

### VER-4 — The gate

The gate is the algorithmic verifier run in whole-set mode:
`python3 check_notes.py --all`. It MUST pass (exit 0) before an operation is
complete and before any commit. A red gate returns the work: the violations are
reported (RPT-2) and, per RPT-4, nothing is repaired until a ruling is given. The
gate decides mechanical clauses only (VER-2); a green gate says nothing about
judgment clauses, and the completion note (RPT-5) MUST say which of those remain
for a human or agent verifier.

*Example:* the sabotage run — one heading level skipped in one note, exit 1 —
and the restore, exit 0.

## Changelog

- **1.1** (2026-09-19) — Added VER-3 (when verification runs) and VER-4 (the
  gate); binding extended to `index.md` and to operations; O2's judgment clause
  added to the VER-2 table.
- **1.0** (2026-09-19) — Initial: VER-1, VER-2.
