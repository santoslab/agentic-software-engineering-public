# Verification (VER)

Version: 1.0
Status: normative; maintained. **Always on.**

This document specifies how conformance between a realization and its
specification is checked: by which kinds of verifier, with what scope, and which
clauses each kind may decide. Later versions add when checks must run and what gate
a change must pass. The keywords MUST, MUST NOT, SHOULD, and MAY carry their
RFC 2119 meanings.

## In this repository

| Realization | Specification | Verifiers available |
|---|---|---|
| a note in `notes/` | `note-format-spec.md` | a person reading both; the agent, asked to check; `check_notes.py`, once it exists |

## Rules

### VER-1 — Verifiers and scope

Conformance MAY be verified (a) by a **human verifier** — a person reading the
specification and the realization and manually checking the correspondence between the two 
(b) by an **agent verifier** — an agent asked to
check and report — or (c) by an **algorithmic verifier** — a program written to decide
the specification's clauses. These are the three kinds of verifier. Every result
MUST state which verifier produced it and MUST be reported in the form RPT-2, so that its
scope — which verifier, which version of the specification, which clauses — is
explicit.

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
| R3 H1 placement | yes | — |
| R4 single H1 | yes | — |
| R5 no skipped heading levels | yes | — |
| R6 index consistency | yes (`--all`) | — |

All six clauses of specification 0.1 are mechanical. Judgment clauses arrive with
later versions of the specification; this table is amended with them.

## Changelog

- **1.0** (2026-09-19) — Initial: VER-1, VER-2.
