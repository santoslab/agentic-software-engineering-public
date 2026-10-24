# Judgments: Message Guard (version A0)

This file defines five claims about the development state of this
repository, the **judgments**, and says how each is evaluated. A judgment is
stated once, for the repository as a whole, and then once for each
**form** of artifact it concerns: the concept of operations (`ConOps`), the
requirements (`Reqs`), the specifications read together (`Specs`), and the
code (`Code`). A statement about one form is a **clause**, named
`Form-JUDGMENT-n`.

Every clause has four fields. The first three depend only on the form and
read the same in any project that uses the form:

- *Holds when* is the claim, a predicate on the development state.
- *Evaluated by* is what produces the evidence: a program, a person, or an
  agent, by a named verification method (*test*, *analysis*, *review*,
  *walkthrough*), or, for validation, the stakeholder's own statement. The
  kind of evaluator named here is the rung of the verifier ladder the clause
  stands on in this version.
- *Evidence* is what the evaluation produces and where it is kept: the
  result of a run, or a **record** of a human activity under `records/`.

The fourth, *In this project*, binds the clause to this repository: which
files are the form's instances here, which tools and commands evaluate it,
the values of the parameters the form leaves open, and, when one is short,
one instance.

Nothing in this file says when a claim must hold, who must run an evaluation,
or what happens when a claim does not hold. The assurance report (last
section) says whether each claim holds now.

## The five judgments

| ID | Claim | Holds when | Evaluated by |
|---|---|---|---|
| **SQ** · specification quality | The specifications can be built from and checked against: each is well-formed, has one reading, is consistent with itself and complete for its level, and the specifications agree with one another. | ConOps-SQ-1, Reqs-SQ-1, and Specs-SQ-1 hold | a person reading; a program for the identifier and method parts |
| **RQ** · realization quality | The realization is in a state in which evidence about it can be produced: it lints, and its suite collects. | Code-RQ-1 holds | programs |
| **CONF** · conformance | For each specification form in scope, the realization conforms to it: every clause of the form has the evidence its verification method calls for, and that evidence is passing. | Reqs-CONF-1 and ConOps-CONF-1 hold | a test run; a person walking the stories |
| **VAL** · validated | The specifications describe what the stakeholders intend. | ConOps-VAL-1 holds | the stakeholders, and nobody else |
| **TR** · traceable | Every link an artifact declares to another resolves. | Specs-TR-1 holds | a program for the citations; a person for the derivations |

CONF relates two artifacts: a specification form and the realization. A CONF
clause is named by the specification form, and the realization is always
its other side; its evidence is produced against a state of both, and the
report's provenance names both. A claim that holds is a supported claim, not
a proof. The evidence has a scope and a producer, and the report states both.

## Concept of operations (`ConOps`)

### ConOps-SQ-1 · The concept of operations is well-formed

| Field | |
|---|---|
| Holds when | The purpose statement says what the system is for, in the stakeholders' words. The scope says what enters, what leaves, and what is outside. Each user category is named with what it observes. Each story carries an identifier, a verification method, a user category, and a concrete example, and reads as one sentence its stakeholder can confirm or deny. No sentence has two readings. |
| Evaluated by | review (human): a person reads the document against this list |
| Evidence | a review record in `records/reviews.md`: who read it, when, against which state of the file, and the finding |
| In this project | `specs/conops.md`: a purpose, a scope with the domain terms, two user categories, three stories. Instance: US-3 carries method *walkthrough (human)*, user category *security officer*, and the example (Critical, 100). |

### ConOps-CONF-1 · Every story has been walked on the realization

| Field | |
|---|---|
| Holds when | Each story whose method is *walkthrough* has been exercised on the running realization with its example, by a person in the story's role, and what they observed matched the story. |
| Evaluated by | walkthrough (human) |
| Evidence | a walkthrough record: who, in which role, when, against which state of the realization, the steps taken, what was observed, and the finding |
| In this project | The three stories of `specs/conops.md`, walked with `uv run python tools/walk.py LEVEL PAYLOAD`; the record is the walkthrough table of `records/walkthrough.md`. Instance: US-3 walked as the security officer: `tools/walk.py Critical 100` printed `drop`. |

### ConOps-VAL-1 · The stakeholders have confirmed the concept of operations

| Field | |
|---|---|
| Holds when | A stakeholder of each user category has stated, naming the version, that the concept of operations describes what they intend. |
| Evaluated by | the stakeholder's own statement, a sign-off. No program and no agent can evaluate this clause. A walkthrough that matches the story (ConOps-CONF-1) is input to the stakeholder's decision, not a substitute for it. |
| Evidence | a sign-off record: the statement, who, in which role, when, which version |
| In this project | The "Sign-off" section of `records/walkthrough.md`; two user categories, so two lines. Instance: the security officer's sign-off on version A0. |

## Requirements (`Reqs`)

### Reqs-SQ-1 · The requirements are well-formed and cover the scope

| Field | |
|---|---|
| Holds when | Every requirement carries a unique identifier, a verification method, and the story or specification section it derives from. Each states one requirement and has one reading. The set covers every case the scope names. |
| Evaluated by | review (human) for the wording and the coverage of the scope; analysis for the header parts: a clause reader lists every clause it finds and reports a header it cannot read |
| Evidence | the review record; the clause table and the findings of the generated conformance report |
| In this project | `specs/requirements.md`, REQ-0 to REQ-3. The cases the scope names are the form of a message and the three security levels. The reader is `tests/conformance.py`; its table is `reports/conformance.md`. Instance: REQ-1 carries method *test* and derives from US-3. |

### Reqs-CONF-1 · Every requirement assigned *test* has passing test evidence, and the realization is exercised

| Field | |
|---|---|
| Holds when | Every requirement whose method is *test* is cited by at least one test; every citing test passes; and the suite meets the project's structural-coverage objective over the realization. |
| Evaluated by | test: the project's test runner, with a plugin that computes requirements coverage from the citations and the outcomes, and a coverage tool for the structural part |
| Evidence | the generated conformance report; the coverage table of the run |
| In this project | The requirements are the REQ clauses of `specs/requirements.md`; the realization is `guard/`; the objective is 100 percent branch coverage; the run is `uv run pytest` with the plugin in `tests/conftest.py` and `pytest-cov`, which writes `reports/conformance.md`. Instance: REQ-1 is cited by `test_filter.py::test_critical_is_dropped`, run for three payloads. |

## The specifications together (`Specs`)

### Specs-SQ-1 · The specifications agree with one another

| Field | |
|---|---|
| Holds when | No requirement contradicts a story. Every story is covered by at least one requirement. Each term means one thing in every document. |
| Evaluated by | review (human), reading the documents together |
| Evidence | the review record |
| In this project | `specs/conops.md` and `specs/requirements.md`, read together. Instance: US-3 (a Critical message never leaves) and REQ-1 (drop a Critical message) agree. |

### Specs-TR-1 · Every reference resolves

| Field | |
|---|---|
| Holds when | Every citation in a test names a clause that exists. Every derivation a requirement declares names a story or specification section that exists. |
| Evaluated by | analysis for the citations: the conformance plugin lists unknown identifiers, and the test runner rejects a marker that is not declared; review (human) for the derivations, done with Specs-SQ-1 |
| Evidence | the "Unknown identifiers" section of the generated conformance report; the review record |
| In this project | The `req` markers of `tests/`, read by the plugin in `tests/conftest.py` under `--strict-markers`; the `Derived from` fields of `specs/requirements.md`. Instance: `@pytest.mark.req("REQ-2")` resolves to REQ-2 in `specs/requirements.md`. |

## The code (`Code`)

### Code-RQ-1 · The realization lints and the suite collects

| Field | |
|---|---|
| Holds when | The realization passes the project's linter, and its test suite collects without error. |
| Evaluated by | analysis: the two commands |
| Evidence | the exit codes, quoted in the assurance report with the state they were run against |
| In this project | `guard/`, `tests/`, and `tools/`; the commands are `uv run ruff check .` and `uv run pytest --collect-only -q --no-cov`. Instance: the run quoted in the latest assurance report. |

## The assurance report

The report states, for each judgment and each clause above, whether it
holds now, on what evidence, with what provenance. Anyone may compile it; in
this version the agent compiles it when asked. The steps:

1. Read this file.
2. For every clause whose method is *test* or *analysis*, run the evaluation
   now, against the current tree, and quote the result. `tools/evaluate.sh`
   runs all of them in one command and prints a header naming the state it
   checked and the tool versions. Do not report a result from memory or from
   an earlier run.
3. For every clause whose method is *review* or *walkthrough*, and for the
   sign-off, read its record under `records/` and report who decided, in
   which role, when, against which state, and what they decided. Do not
   perform the evaluation; if there is no record, say so. If the record names
   a state other than the current tree, say so.
4. State at the head which state of the tree the report is about, and
   whether the tree had uncommitted changes.
5. Write `reports/assurance-report.md` in the form of
   `process/templates/assurance-report.md`. List at the end every command
   run and every record read.

The report is itself a claim, made by whoever compiled it, and its last
section says what was run and read so that a reader can check it. It is a
very small assurance case: the clauses above are its claims, the evidence
column is its evidence, the *Evaluated by* method is the reason the evidence
bears on the claim, and the provenance is what a reader uses to decide how
far to trust each piece. Later versions keep the report between requests
instead of recompiling it, which is the ledger; this version has no ledger.
