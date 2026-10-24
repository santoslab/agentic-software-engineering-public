# Judgments: Message Guard (version A0)

This file defines five claims about the development state of this
repository and says how each is evaluated. A claim is stated once for the
repository and then, below, once for each form it concerns: the concept of
operations, the requirements, the specifications read together, and the
code. Each per-form clause has four fields. *Holds when* is the claim.
*Evaluated by* is what produces the evidence: a program, or a person, by a
named verification method. *Evidence* is what the evaluation produces and
where it is kept. *Example* is one instance from this system.

Nothing in this file says when a claim must hold. The assurance report
(last section) says whether each holds now.

## The five judgments

| ID | Claim | Holds when | Evaluated by |
|---|---|---|---|
| **SQ** · specification quality | The specifications can be built from and checked against: each is well-formed, has one reading, is consistent with itself and complete for its level, and the specifications agree with one another. | ConOps-SQ-1, Reqs-SQ-1, and Specs-SQ-1 hold | a person reading; a program for the identifier and method parts |
| **RQ** · realization quality | The realization is in a state in which evidence about it can be produced: it lints, and its suite collects. | Code-RQ-1 holds | programs |
| **CONF** · conformance | The realization does what the specifications say, to the extent the evidence each clause's method calls for can show. | Reqs-CONF-1 and ConOps-CONF-1 hold | a test run; a person walking the stories |
| **VAL** · validated | The specifications describe what the stakeholders intend. | ConOps-VAL-1 holds | the stakeholders, and nobody else |
| **TR** · traceable | Every link an artifact declares to another resolves. | Specs-TR-1 holds | a program for the markers; a person for the derivations |

A claim that holds is a supported claim, not a proof. The evidence has a
scope and a producer, and the report states both.

## Concept of operations (`ConOps`)

### ConOps-SQ-1 · The concept of operations is well-formed

| Field | |
|---|---|
| Holds when | The purpose statement says what the guard is for, in the stakeholders' words. The scope says what enters, what leaves, and what is outside. Each user category is named with what it observes. Each story carries an identifier, a method, a user category, and an example message, and reads as one sentence its stakeholder can confirm or deny. No sentence has two readings. |
| Evaluated by | review (human): a person reads the document against this list |
| Evidence | a review record in `records/reviews.md`: who read it, when, against which state of the file, and the finding |
| Example | US-3 carries method *walkthrough (human)*, user category *security officer*, and the example (Critical, 100) |

### ConOps-CONF-1 · Every story has been walked on the realization

| Field | |
|---|---|
| Holds when | Each story (method *walkthrough (human)*) has been exercised on the running guard with its example message, by a person in the story's role, and what they observed matched the story. |
| Evaluated by | walkthrough (human), with `tools/walk.py` |
| Evidence | the walkthrough table of `records/validation.md`: who, in which role, when, against which state of the realization, the command, what was observed, the finding |
| Example | US-3 walked as the security officer: `tools/walk.py Critical 100` printed `drop` |

### ConOps-VAL-1 · The stakeholders have confirmed the concept of operations

| Field | |
|---|---|
| Holds when | A stakeholder of each user category has stated, naming the version, that the concept of operations describes what they intend. |
| Evaluated by | the stakeholder's own statement, a sign-off. No program and no agent can evaluate this clause. A walkthrough that matches the story (ConOps-CONF-1) is input to the stakeholder's decision, not a substitute for it. |
| Evidence | the sign-off in `records/validation.md`: the statement, who, in which role, when, which version |
| Example | the security officer's sign-off on version A0 |

## Requirements (`Reqs`)

### Reqs-SQ-1 · The requirements are well-formed and cover the scope

| Field | |
|---|---|
| Holds when | Every requirement carries a unique identifier, a method, and the story it derives from. Each is one sentence with "shall" and one reading. The set covers every case the scope names: the form of a message, and each of the three security levels. |
| Evaluated by | review (human) for the wording and the coverage of the scope; analysis for the header parts: the clause reader in `tests/conformance.py` lists every clause it finds and reports a header it cannot read |
| Evidence | the review record; the clause table and the findings of `reports/conformance.md` |
| Example | REQ-1 carries method *test* and derives from US-3 |

### Reqs-CONF-1 · Every requirement has passing test evidence, and the code is exercised

| Field | |
|---|---|
| Holds when | Every requirement (method *test*) is cited by at least one test; every citing test passes; and the suite reaches 100 percent branch coverage of `guard/`. |
| Evaluated by | analysis: `uv run pytest`. The plugin in `tests/conftest.py` computes requirements coverage from the markers and the outcomes; `pytest-cov` computes the structural coverage. |
| Evidence | `reports/conformance.md`; the coverage table of the run |
| Example | REQ-1 is cited by `test_filter.py::test_critical_is_dropped`, run for three payloads |

## The specifications together (`Specs`)

### Specs-SQ-1 · The specifications agree with one another

| Field | |
|---|---|
| Holds when | No requirement contradicts a story. Every story is covered by at least one requirement. Each term means one thing in both documents. |
| Evaluated by | review (human), reading both documents together |
| Evidence | the review record |
| Example | US-3 (a Critical message never leaves) and REQ-1 (drop a Critical message) agree |

### Specs-TR-1 · Every reference resolves

| Field | |
|---|---|
| Holds when | Every `req` marker names a requirement that exists. Every "Derived from" names a story that exists. |
| Evaluated by | analysis for the markers: the plugin lists unknown identifiers, and `--strict-markers` rejects a marker that is not declared; review (human) for the derivations, done with Specs-SQ-1 |
| Evidence | the "Unknown identifiers" section of `reports/conformance.md`; the review record |
| Example | `@pytest.mark.req("REQ-2")` resolves to REQ-2 in `specs/requirements.md` |

## The code (`Code`)

### Code-RQ-1 · The realization lints and the suite collects

| Field | |
|---|---|
| Holds when | `ruff check .` exits 0, and `pytest --collect-only` exits 0. |
| Evaluated by | analysis: the two commands |
| Evidence | the exit codes, quoted in the assurance report with the state they were run against |
| Example | the run quoted in the report of 2026-10-20 |

## The assurance report

The report states, for each judgment and each clause above, whether it
holds now, on what evidence, with what provenance. Anyone may compile it; in
this version the agent compiles it when asked. The steps:

1. Read this file.
2. For every clause whose method is *test* or *analysis*, run the evaluation
   now, against the current tree, and quote the result. Do not report a
   result from memory or from an earlier run.
3. For every clause whose method is *review*, *walkthrough*, or a sign-off,
   read its record under `records/` and report who decided, in which role,
   when, against which state, and what they decided. Do not perform the
   evaluation; if there is no record, say so. If the record names a state
   other than the current tree, say so.
4. State at the head which state of the tree the report is about, and
   whether the tree had uncommitted changes.
5. Write `reports/assurance-report.md` in the form of
   `process/templates/assurance-report.md`. List at the end every command
   run and every record read.

The report is itself a claim, made by whoever compiled it. Its last section
says what was run and read, so that a reader can check it. Later versions
keep the report between requests instead of recompiling it, which is the
ledger; this version has no ledger.
