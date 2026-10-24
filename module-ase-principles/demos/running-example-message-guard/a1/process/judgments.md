# Judgments: Message Guard (version A1)

This file defines five claims about the development state of this
repository, the **judgments**, and says how each is evaluated. A judgment is
stated once, for the repository as a whole, and then once for each **form**
of artifact it concerns: the concept of operations (`ConOps`), the requirements (`Reqs`), the glossary (`Gloss`), the scenarios (`Scen`), the specifications read together (`Specs`), the code (`Code`). A statement about one form is a
**clause**, named `Form-JUDGMENT-n`; the file is arranged by form, so that a
form's section holds every clause about it, whichever judgment the clause
serves. A clause keeps its identifier when amended; amendments are listed in
the changelog at the end.

Every clause has four fields. The first three depend only on the form and
read the same in any project that uses the form: *Holds when* is the claim;
*Evaluated by* is what produces the evidence, a program, a person, or an
agent by a named verification method, which is also the rung of the verifier
ladder the clause stands on in this version; *Evidence* is what the
evaluation produces and where it is kept. The fourth, *In this project*,
binds the clause to this repository: the files, the tools and commands, the
parameters, and, when one is short, one instance. Where an *Evaluated by*
field says "within the audit", the items it cites (C-1 to C-14) are the
audit's checklist, `.claude/skills/audit-spec/forms/`; the procedure itself is `Audit` in
`process/procedures.md`.

Nothing in this file says when a claim must hold, who must run an
evaluation, or what happens when a claim does not hold. The assurance report
(last section) says whether each claim holds now.

## The five judgments

| ID | Claim | Holds when | Evaluated by |
|---|---|---|---|
| **SQ** · specification quality | The specifications can be built from and checked against: each is well-formed, has one reading, is consistent with itself and complete for its level, uses the glossary's terms in the glossary's sense, and the specifications agree with one another. | ConOps-SQ-1, Reqs-SQ-1, Reqs-SQ-2, Gloss-SQ-1, and Specs-SQ-1 hold | the audit (procedure Audit), by a person or by an agent running `/audit-spec`, with a person ruling on every gap; the clause reader for the header parts |
| **RQ** · realization quality | The realization is in a state in which evidence about it can be produced: it lints, and its suite collects. | Code-RQ-1 holds | programs |
| **CONF** · conformance | For each specification form in scope, the realization conforms to it: every clause of the form has the evidence its verification method calls for, and that evidence is passing. | Reqs-CONF-1 and Scen-CONF-1 hold | the test run |
| **VAL** · validated | The specifications describe what the stakeholders intend. | ConOps-VAL-1 holds | the stakeholders, and nobody else |
| **TR** · traceable | Every link an artifact declares to another resolves, in both directions. | Specs-TR-1 and Specs-TR-2 hold | programs |

CONF relates two artifacts: a specification form and the realization. A CONF
clause is named by the specification form, and the realization is always
its other side; its evidence is produced against a state of both, and the
report's provenance names both. A claim that holds is a supported claim, not
a proof. The evidence has a scope and a producer, and the report states both.

## Concept of operations (`ConOps`)

### ConOps-SQ-1 · The concept of operations is well-formed

| Field | |
|---|---|
| Holds when | The purpose statement says what the system is for, in the stakeholders' words, and says who agreed to it and when. The scope says what enters, what leaves, and what is outside, and states its assumptions as assumptions, each an obligation of the deploying organization rather than a requirement on the system. Each user category is named with what it observes, and whoever is not a user is said not to be. Each story carries an identifier, a verification method, the scenarios that exercise it where its method is *test*, its user category, how it is validated, and the elicitation entry it comes from; has a concrete example; and reads as one sentence its stakeholder can confirm or deny. Wants that are not promised are listed as deferred, with their source, and nothing derives from them. Every domain term is the glossary's. |
| Evaluated by | review within the audit (procedure Audit; the within-document items for this form, C-1 and C-4 to C-7, with C-11 and C-12 between documents); the header parts by the clause reader |
| Evidence | the latest audit record under `records/` with no open gap on these items; the clause table and the findings of the generated conformance report |
| In this project | `specs/conops.md`: a purpose agreed on 2026-10-22 (E-1, E-3); assumptions A-1 and A-2; two user categories; stories US-1 to US-3, each with a `Source`; deferred wants D-1 to D-3. Instance: US-3 carries `Method: test · Scenarios: SC-5, SC-6 · User category: security officer · Validated by: walkthrough (human) · Source: E-1`. |

### ConOps-VAL-1 · The stakeholders have confirmed the concept of operations

| Field | |
|---|---|
| Holds when | A stakeholder of each user category has walked their stories on the running realization with the scenario inputs, decided whether each story describes what they want, and stated, naming the version, that the concept of operations describes what they intend. |
| Evaluated by | the stakeholders: a walkthrough per user category and a sign-off. No program and no agent can evaluate this clause; passing scenarios (Scen-CONF-1) are input to the decision, not a substitute for it. Observing the expected output is not the decision; the decision is whether the story describes what the stakeholder wants. |
| Evidence | a validation record: per user category, who walked, in which role, when, against which realization state, which stories with which scenario inputs, what was observed, and the decision to sign or to withhold, with its reason; and the sign-off naming the version |
| In this project | `records/validation.md`: one table per user category, the sign-off below them, and the earlier walkthrough records kept as an appendix. The walkthrough uses `uv run python tools/walk.py LEVEL PAYLOAD` with the inputs of `specs/scenarios.json`. Instance: the security officer's section for A1: US-3 walked with SC-5 and SC-6; decision: sign for A1 with D-1 to D-3 deferred. |

## Requirements (`Reqs`)

### Reqs-SQ-1 · The requirements are well-formed and cover the scope

| Field | |
|---|---|
| Holds when | Every requirement carries a unique identifier, a verification method, and the story or the glossary terms it derives from. Each states one requirement and has one reading. The set covers every case the scope names. |
| Evaluated by | review within the audit (C-1, C-4, C-7, C-8); the header parts by the clause reader |
| Evidence | the latest audit record with no open gap on these items; the clause table and the findings of the generated conformance report |
| In this project | `specs/requirements.md`, REQ-0 to REQ-3. The cases the scope names are the form of a message and the three security levels. The reader is `tests/conformance.py`. Instance: REQ-0 derives from the glossary terms *message*, *security level*, and *payload*; REQ-1 from US-3. |

### Reqs-SQ-2 · The requirements are in EARS form

| Field | |
|---|---|
| Holds when | Every requirement declares its EARS pattern in a `Pattern` field (ubiquitous, event-driven, state-driven, unwanted-behavior, optional-feature, or complex) and has that pattern's shape: a trigger where the pattern has one, a stated subject, and "shall". |
| Evaluated by | review within the audit (C-2). Planned for A2: analysis by a script, at which point the method flips from review to analysis. |
| Evidence | the C-2 row of the latest audit record |
| In this project | The subject of a clause about the input is the guard; the subject of a pass-or-drop clause is the filter; the trigger of an event-driven clause is "When the filter is given a message ..." (the preamble of `specs/requirements.md` states the convention). Instance: the draft "Restricted messages are allowed through." became "When the filter is given a message whose security level is Restricted, the filter shall pass the message unchanged." |

### Reqs-CONF-1 · Every requirement assigned *test* has passing test evidence, and the realization is exercised

| Field | |
|---|---|
| Holds when | Every requirement whose method is *test* is cited by at least one test; every citing test passes; and the suite meets the project's structural-coverage objective over the realization. |
| Evaluated by | test: the project's test runner, with a plugin that computes requirements coverage from the citations and the outcomes, and a coverage tool for the structural part. A partial run (tests deselected) is labeled in the report and is not evidence; a finding of the clause reader fails the run. |
| Evidence | the generated conformance report, with its scope line; the coverage table of the run |
| In this project | The requirements are the REQ clauses of `specs/requirements.md`; the realization is `guard/`; the objective is 100 percent branch coverage; the run is `uv run pytest` with the plugin in `tests/conftest.py` and `pytest-cov`, which writes `reports/conformance.md`. Instance: REQ-1 is cited by `test_filter.py::test_critical_is_dropped`, run for three payloads. |

## Glossary (`Gloss`)

### Gloss-SQ-1 · Glossary discipline

| Field | |
|---|---|
| Holds when | Every domain term used in a specification is defined exactly once, in the glossary, and is used only in its defined sense. No other specification defines a term. |
| Evaluated by | review within the audit (C-3, C-10): a person in audit 01, an agent in audit 02, the skill from audit 03. Planned for A2: analysis by a script. |
| Evidence | the C-3 and C-10 rows of the latest audit record |
| In this project | `specs/glossary.md`, read against `specs/conops.md` and `specs/requirements.md` and `specs/scenarios.json`. Instance: "sensitive" in a draft of US-3 was undefined; the ruling rewrote the story as "every message whose security level is Critical". |

## Scenarios (`Scen`)

### Scen-CONF-1 · Every scenario runs as a test that cites its story

| Field | |
|---|---|
| Holds when | A loader runs every scenario of the scenario file as a test citing the story the scenario derives from, and every such test passes. |
| Evaluated by | test: the same run as Reqs-CONF-1 |
| Evidence | the story rows of the generated conformance report |
| In this project | `specs/scenarios.json`, SC-1 to SC-6, run by `tests/test_scenarios.py`, which builds each message through the public interface and compares the output by value. The file is a specification and is never edited to make a test pass; a scenario that looks wrong is a gap for the audit (C-14). Instance: US-3 is cited by `test_scenarios.py::test_scenario[SC-5]` and `[SC-6]`. |

The scenario file is a specification: the stakeholders' examples, bound to
values. It is never edited to make a test pass; a scenario that looks wrong
is a gap for the audit (C-14).

## The specifications together (`Specs`)

### Specs-SQ-1 · The specifications agree with one another

| Field | |
|---|---|
| Holds when | Every story has at least one requirement, and every requirement derives from a story or from glossary terms. No two clauses contradict, in one document or across two. Each term has one sense everywhere. No assumption and no deferred want has become a requirement. Every example and every scenario has the output the clauses give it. Every file, clause, procedure, and record entry a specification names exists. |
| Evaluated by | the audit (procedure Audit; the between-document items C-8 to C-13 and the by-execution item C-14), by a person or by an agent running `/audit-spec`, with a person ruling on every gap |
| Evidence | the latest audit record under `records/` with no open gap |
| In this project | Every file under `specs/`, read together; the helper `tools/walk.py` for the by-execution item. Instance: audit 03 found that a draft of REQ-1 also required a record of the drop, which the scope excludes; the ruling deleted the clause and kept the want as D-1. |

### Specs-TR-1 · Every reference resolves

| Field | |
|---|---|
| Holds when | Every citation in a test names a clause that exists. Every derivation names an existing story or existing glossary terms. Every source reference names an entry of the elicitation record. Every scenario reference names a scenario that exists, and every scenario is listed by the story it derives from. |
| Evaluated by | analysis: the conformance plugin for the citations (unknown identifiers; `--strict-markers`); the trace tool for the derivation, source, and scenario references |
| Evidence | the "Unknown identifiers" section of the generated conformance report; the findings section of the generated trace matrix |
| In this project | The `req` markers of `tests/`; the `Derived from`, `Source`, and `Scenarios` fields of the specifications and each scenario's `derived_from`, resolved by `uv run python tools/trace.py` against `specs/` and `reference/elicitation.md`. Instance: US-3's `Source: E-1` resolves to entry E-1 of the elicitation record. |

### Specs-TR-2 · The trace matrix is complete in both directions

| Field | |
|---|---|
| Holds when | A trace matrix generated against the current tree has an empty findings section: no story without a requirement, no requirement without a derivation, no test clause without a citing test, no scenario not listed by its story, no dangling reference or citation, and no finding of the clause reader. |
| Evaluated by | analysis: the exit code of the trace tool |
| Evidence | the generated trace matrix, whose header names the tool version, the files read, the number of tests collected and citing, and the state checked |
| In this project | `uv run python tools/trace.py`, the last step of `tools/evaluate.sh`, writes `reports/trace-matrix.md`; its known-violation cases are `tests/tooling/`. Instance: with REQ-3 derived from US-2 instead of US-1, every link resolves and the matrix reports "story without requirement at US-1". |

## The code (`Code`)

### Code-RQ-1 · The realization lints and the suite collects

| Field | |
|---|---|
| Holds when | The realization passes the project's linter, and its test suite collects without error. |
| Evaluated by | analysis: the two commands |
| Evidence | the exit codes, quoted in the assurance report with the state they were run against |
| In this project | `guard/`, `tests/` (including the tools' own tests under `tests/tooling/`), and `tools/`; the commands are `uv run ruff check .` and `uv run pytest --collect-only -q --no-cov`. Instance: the run quoted in the latest assurance report. |

## The assurance report

As in A0: the report states, for each judgment and each clause above,
whether it holds now, on what evidence, with what provenance, and anyone may
compile it; in this version the agent compiles it when asked, by the steps
in `CLAUDE.md`. Two things are new. For the SQ clauses the record is the
latest audit under `records/`; the report names it and says whether it was
made against the current specifications. The report does not run the audit;
the developer starts it (procedure Audit). The mechanical evaluations are run with one command, `tools/evaluate.sh`,
which prints a header naming the state it checked and the tool versions,
then runs `ruff`, the suite, and the trace tool, and stops at the first
failure; the report quotes its header.

The report is a very small assurance case: the clauses above are its claims,
the evidence column is its evidence, the *Evaluated by* method is the reason
the evidence bears on the claim, and the provenance is what a reader uses to
decide how far to trust each piece. Later versions keep the report between
requests instead of recompiling it, which is the ledger; this version has no
ledger.

## Changelog

- **A1, commit a1-specs.** Added Reqs-SQ-2, Gloss-SQ-1, and the form
  `Gloss`. Amended ConOps-SQ-1 (the agreed purpose; assumptions and deferred
  wants; the `Validated by` and `Source` fields; the glossary's terms),
  Reqs-SQ-1 (derivation from glossary terms), Specs-SQ-1 (evaluated by the
  audit; the between-document and by-execution items), and Specs-TR-1 (the
  `Source` references; derivations from glossary terms). The procedures
  `Audit` and `Elicit` entered `process/procedures.md`.
- **A1, commit a1-scenarios.** Added Scen-CONF-1 and the form `Scen`. The
  stories' method became *test*, their examples the scenarios of
  `specs/scenarios.json`. Amended ConOps-SQ-1 (the `Scenarios` field),
  Reqs-CONF-1 (a partial run is labeled and is not evidence; a reader
  finding fails the run), Specs-SQ-1 (scenarios in the by-execution item),
  and Specs-TR-1 (the scenario references). Retired ConOps-CONF-1: no clause
  has method *walkthrough* at this commit; the identifier is not reused.
- **A1, commit a1-trace.** Added Specs-TR-2 (the trace matrix, evaluated by
  `tools/trace.py`). Amended Specs-TR-1 (the reference parts are now
  evaluated by the tool, not read by a person) and Code-RQ-1 (the tools'
  own tests collect with the suite); `tools/evaluate.sh` runs the trace tool
  as its last step.
- **A1, commit a1.** Amended ConOps-VAL-1 (a walkthrough per user category
  with the scenario inputs, and a validation record with a decision per
  story); `records/walkthrough.md` became `records/validation.md`, with the
  earlier walkthrough records kept as its appendix.
