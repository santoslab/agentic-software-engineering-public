# Verification (VER)

Version: 1.3
Status: normative; maintained. **Always on.**

This document specifies how conformance between a realization and its
specification is checked: by which kinds of verifier, with what scope, which
clauses each kind may decide, when checks run, and what gate a change must pass.
The keywords MUST, MUST NOT, SHOULD, and MAY carry their RFC 2119 meanings.

## In this repository

| Realization | Specification | Verifiers available |
|---|---|---|
| the engine module (board state, rules of play, win and tie detection, rendering) | `SPECS.md` — board and coordinates, rules of play, display format, interface contract | human; agent; algorithmic — the test suite under `pytest` |
| the computer opponent | `SPECS.md` — the strategy interface and its contract | human; agent; algorithmic — the test suite |
| the command-line interface | `SPECS.md` — input grammar, interaction flow, example session | human; agent; algorithmic — the test suite with scripted input |
| the whole program, as played | `CONOPS.md` — policies, modes, scenarios | human (validation: is this the game that was wanted?); agent — a walkthrough of each scenario |
| the test suite itself | `SPECS.md` §9 — the verification obligations | human; agent — that every obligation is claimed by at least one test, and every test cites its clause (VER-6, VER-8) |
| `fixtures/scenarios.json` with its loader | `SPECS.md` — rules of play, interface contract | algorithmic — the loader, on every implementation (VER-7) |

The gate (VER-4) is
`pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100`:
exit 0 when every test passes and branch coverage is 100%; non-zero otherwise.

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

| Clauses | Algorithmic | Human or agent |
|---|---|---|
| `SPECS.md` board and coordinates; rules of play; win and tie | yes — unit tests on the engine | — |
| `SPECS.md` display format | yes — golden-string tests | — |
| `SPECS.md` input grammar; interaction flow | yes — scripted-input tests | — |
| `SPECS.md` interface contract | yes — unit tests; a type checker where used | — |
| `SPECS.md` example session | yes — an end-to-end scripted run | — |
| `SPECS.md` verification obligations | partly — the suite's presence per category | yes — that each obligation is actually claimed by a test |
| `CONOPS.md` policies and scenarios | — | yes — validation by playing each scenario |

The table is completed when `SPECS.md` exists, clause by clause; clauses added by
amendment are classified when they are added.

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

*Example (game):* when the interface contract gains the clause "a move after the
game is over is rejected", the engine is re-verified against it in the same
commit — and a test citing that clause is added, because a clause no test claims
is not verified (VER-2).

### VER-4 — The gate

The gate is the algorithmic verifier run over the whole realization:
`pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100`. It
MUST pass (exit 0) before an operation is complete and before any commit. A red
gate returns the work: the failures are reported (RPT-2) and, per RPT-4, nothing
is repaired until a ruling is given. The gate decides mechanical clauses only
(VER-2); a green gate says nothing about judgment clauses, and the completion note
(RPT-5) MUST say which of those remain for a human or agent verifier.

*Example:* the sabotage run of the note set — one heading level skipped in one
note, exit 1 — and the restore, exit 0.

*Example (game):* a flipped entry in the engine's direction table fails the
diagonal-win tests, exit 1; the gate returns the work.

### VER-5 — Coverage policy

The gate measures **branch** coverage over every source module, and the target
is **100%**. `# pragma: no cover` is permitted on exactly one location: the
`if __name__ == "__main__":` guard of the entry point, which the test runner
cannot reach by importing. No other exclusion is permitted: every other
branch — including the `sys.exit` paths of menu loops — MUST be reached by a
real test (for example, `pytest.raises(SystemExit)`). If a change introduces a
branch that is genuinely unreachable, this document is amended (DEV-3) to record
the exception — naming the branch and saying why it cannot be reached — before
any pragma is added.

*Example (game):* the reference implementation carries exactly one pragma, on
`main.py`'s `__main__` guard.

### VER-6 — Test discipline

Every test MUST cite, in its docstring or an adjacent comment, the specification
clause it verifies (AUD-5), so that clause coverage can be read off the suite. A
test MAY assert tighter than the specification, never looser: the specification
is the floor. Direct assignment to internal state is permitted for *setting up* a
scenario only; a test that verifies an operation — a move, a turn change, the
list of available moves — MUST go through the public operation. A test that
cannot fail when the realization regresses — one that only re-asserts a property
of its own setup — is not a test and MUST NOT be counted. Tests live under
`tests/`, one file per source module.

*Example (game):* placing five marks by direct assignment in order to verify win
detection is setup; verifying that a move switches the player by direct
assignment would be a violation. The 3-by-3 suite's audit found a test that
seeded the random generator and asserted that two calls agreed — tautological,
and removed.

### VER-7 — Fixtures are never edited to pass

A fixture file (`fixtures/scenarios.json`) is an executable specification: a set
of scenarios with expected outcomes that any implementation of the contract — in
any language — must reproduce. It MUST NOT be modified to make a test pass. An
expectation that looks wrong is a finding about the pair (fixture,
specification), raised as a gap (RPT-1) for a ruling (DEV-4). The fixture file
MUST state the rules it assumes and its known blind spots; a blind spot is part
of its contract, not a defect.

*Example (game):* the shared fixtures contain no tie scenario and say so. A port
that wants tie coverage generates one and verifies it against the specification
by hand before trusting it.

### VER-8 — Coverage is not conformance

Branch coverage is a property of the pair (tests, code): it says which code the
suite reaches. Clause coverage is a property of the pair (tests, specification):
it says which clauses at least one test claims. A suite can hold 100% branch
coverage while claiming nothing about a clause — delete the overline test and
the coverage figure does not move. The two MUST be reported separately: the gate
reports branch coverage (VER-4); the completion note (RPT-5) reports clause
coverage against the verification obligations (`SPECS.md` §9, AUD-14) and names
the clauses that remain for a human or agent verifier (VER-2).

*Example (game):* the sabotage run of Lecture 04 — the overline test deleted,
`--cov-fail-under=100` still green — followed by a flipped direction in the
engine, which the remaining tests catch.

## Changelog

- **1.3** (2026-09-19) — Added VER-5 (coverage policy), VER-6 (test discipline),
  VER-7 (fixtures are never edited to pass), VER-8 (coverage is not
  conformance); binding rows for the test suite and the fixtures.
- **1.2** (2026-09-19) — Binding rewritten for a code repository; VER-2 table by
  kind of specification; the `pytest` gate; game examples.
- **1.1** (2026-09-19) — Added VER-3 (when verification runs) and VER-4 (the
  gate); binding extended to `index.md` and to operations; O2's judgment clause
  added to the VER-2 table.
- **1.0** (2026-09-19) — Initial: VER-1, VER-2.
