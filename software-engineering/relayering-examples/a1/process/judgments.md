# Judgments: Message Guard (version A1)

Five claims about the development state, each stated once for the
repository and then per form. A1 adds two forms, the glossary and the
scenario file, and the file is now arranged by form: a form's section holds
every clause about it, whichever judgment the clause serves. A clause keeps
its identifier when amended; amendments are listed in the changelog.
Procedures for two activities, the audit and elicitation, are in
`process/procedures.md`. Nothing in this file says when a claim must hold.

## The five judgments

| ID | Claim | Holds when | Evaluated by |
|---|---|---|---|
| **SQ** | The specifications can be built from and checked against: each is well-formed, has one reading, is consistent with itself and complete for its level, uses the glossary's terms in the glossary's sense, and the specifications agree with one another. | ConOps-SQ-1, Reqs-SQ-1, Reqs-SQ-2, Gloss-SQ-1, and Specs-SQ-1 hold | the audit (procedure Specs-Audit), by a person or by an agent running `/audit-spec`, with a person ruling on every gap; the clause reader for the header parts |
| **RQ** | The realization lints and its suite collects. | Code-RQ-1 holds | programs |
| **CONF** | The realization does what the specifications say, to the extent the evidence each clause's method calls for can show. | Reqs-CONF-1 and Scen-CONF-1 hold | the test run |
| **VAL** | The specifications describe what the stakeholders intend. | ConOps-VAL-1 holds | the stakeholders, and nobody else |
| **TR** | Every link an artifact declares to another resolves, in both directions. | Specs-TR-1 and Specs-TR-2 hold | programs |

## Concept of operations (`ConOps`)

### ConOps-SQ-1 · The concept of operations is well-formed

| Field | |
|---|---|
| Holds when | The purpose statement says what the guard is for in the stakeholders' words and is agreed. The scope says what enters, what leaves, and what is outside, and states its assumptions as assumptions (A-n). Each user category is named with what it observes; the developer is not one. Each story carries an identifier, a method, the scenarios that exercise it, its user category, how it is validated, and the elicitation entry it comes from, and reads as one sentence its stakeholder can confirm or deny. Wants that are not promised are listed as deferred (D-n) and nothing derives from them. Every domain term is the glossary's. |
| Evaluated by | review within the audit (Specs-Audit, checklist items C-1, C-5, C-7, C-11, C-12); the header parts by the clause reader |
| Evidence | the audit record `records/audit-NN.md` with no open gap on these items; the findings of `reports/conformance.md` |
| Example | US-3 carries `Method: test · Scenarios: SC-5, SC-6 · User category: security officer · Validated by: walkthrough (human) · Source: E-1` |

### ConOps-VAL-1 · The stakeholders have confirmed the concept of operations

| Field | |
|---|---|
| Holds when | A stakeholder of each user category has walked their stories on the running realization with the scenario inputs, decided whether each story describes what they want, and stated, naming the version, that the concept of operations describes what they intend. |
| Evaluated by | the stakeholders: a walkthrough per user category and a sign-off. No program and no agent can evaluate this clause; passing scenarios (Scen-CONF-1) are input to the decision, not a substitute for it. |
| Evidence | `records/validation.md`: per user category, who walked, in which role, when, against which realization state, which stories with which scenario inputs, what was observed, and the decision to sign or to withhold, with its reason; the sign-off naming the version |
| Example | the security officer's section for A1: US-3 walked with SC-5 and SC-6; decision: sign for A1 with D-1 to D-3 deferred |

## Requirements (`Reqs`)

### Reqs-SQ-1 · The requirements are well-formed and cover the scope

| Field | |
|---|---|
| Holds when | Every requirement carries a unique identifier, a method, and the story or the glossary terms it derives from. Each has one reading. The set covers every case the scope names. |
| Evaluated by | review within the audit (C-1, C-8); the header parts by the clause reader |
| Evidence | the audit record; the findings of `reports/conformance.md` |
| Example | REQ-0 derives from the glossary terms message, security level, and payload |

### Reqs-SQ-2 · The requirements are in EARS form

| Field | |
|---|---|
| Holds when | Every requirement declares its EARS pattern in a `Pattern` field (ubiquitous, event-driven, state-driven, unwanted-behavior, optional-feature, or complex) and has that pattern's shape: a trigger where the pattern has one, the filter or the guard as subject, and "shall". |
| Evaluated by | review within the audit (C-2). Planned for A2: analysis by a script. |
| Evidence | the C-2 row of the audit record |
| Example | "Restricted messages are allowed through." became "When the filter is given a message whose security level is Restricted, the filter shall pass the message unchanged." |

### Reqs-CONF-1 · Every requirement has passing test evidence, and the code is exercised

| Field | |
|---|---|
| Holds when | Every requirement (method *test*) is cited by at least one test; every citing test passes; the suite reaches 100 percent branch coverage of `guard/`. |
| Evaluated by | analysis: `uv run pytest` with the plugin in `tests/conftest.py` and `pytest-cov`. A partial run (tests deselected) is labeled in the report and is not evidence. |
| Evidence | `reports/conformance.md`; the coverage table |
| Example | REQ-1 is cited by `test_filter.py::test_critical_is_dropped` |

## Glossary (`Gloss`)

### Gloss-SQ-1 · Glossary discipline

| Field | |
|---|---|
| Holds when | Every domain term used in a specification is defined exactly once, in `specs/glossary.md`, and is used only in its defined sense. No other specification defines a term. |
| Evaluated by | review within the audit (C-3, C-10): a person in audit 01, an agent in audit 02, the skill from audit 03. Planned for A2: analysis by a script. |
| Evidence | the C-3 and C-10 rows of the audit record |
| Example | "sensitive" in a draft of US-3 was undefined; the ruling rewrote the story as "every message whose security level is Critical" |

## Scenarios (`Scen`)

### Scen-CONF-1 · Every scenario runs as a test that cites its story

| Field | |
|---|---|
| Holds when | The loader `tests/test_scenarios.py` runs every scenario of `specs/scenarios.json` as a test citing the story the scenario derives from, and every such test passes. |
| Evaluated by | analysis: the same `uv run pytest` run as Reqs-CONF-1 |
| Evidence | the US rows of `reports/conformance.md` |
| Example | US-3 is cited by `test_scenarios.py::test_scenario[SC-5]` and `[SC-6]` |

The scenario file is a specification: the stakeholders' examples, bound to
values. It is never edited to make a test pass; a scenario that looks wrong
is a gap for the audit (C-14).

## The specifications together (`Specs`)

### Specs-SQ-1 · The specifications agree with one another

| Field | |
|---|---|
| Holds when | Every story has at least one requirement, and every requirement derives from a story or from glossary terms. No two clauses contradict, in one document or across two. Each term has one sense everywhere. No assumption and no deferred want has become a requirement. Every example and every scenario has the output the clauses give it. Every file, rule, and record entry a specification names exists. |
| Evaluated by | the audit (procedure Specs-Audit, C-6 to C-14) |
| Evidence | the audit record with no open gap |
| Example | audit 03 found that a draft of REQ-1 also required a record of the drop, which the scope excludes; the ruling deleted the clause and kept the want as D-1 |

### Specs-TR-1 · Every reference resolves

| Field | |
|---|---|
| Holds when | Every `req` marker names a clause that exists. Every `Derived from` names an existing story or existing glossary terms. Every `Source` names an entry of `reference/elicitation.md`. Every `Scenarios` entry names a scenario that exists. |
| Evaluated by | analysis: the plugin for the markers; `tools/trace.py` for the other three |
| Evidence | the "Unknown identifiers" section of `reports/conformance.md`; the findings section of `reports/trace-matrix.md` |
| Example | US-3's `Source: E-1` resolves to entry E-1 of the elicitation record |

### Specs-TR-2 · The trace matrix is complete in both directions

| Field | |
|---|---|
| Holds when | `reports/trace-matrix.md`, generated by `tools/trace.py` against the current tree, has an empty findings section: no story without a requirement, no requirement without a derivation, no test clause without a citing test, no scenario not listed by its story, no dangling marker, no reader finding. |
| Evaluated by | analysis: the exit code of `uv run python tools/trace.py` |
| Evidence | `reports/trace-matrix.md`, with its header naming the tool version, the files read, and the state checked |
| Example | with REQ-3 derived from US-2 instead of US-1, every link resolves and the matrix reports "story without requirement at US-1" |

## The code (`Code`)

### Code-RQ-1 · The realization lints and the suite collects

| Field | |
|---|---|
| Holds when | `ruff check .` exits 0 over `guard/`, `tests/`, and `tools/`, and `pytest --collect-only` exits 0. |
| Evaluated by | analysis: the two commands |
| Evidence | the exit codes, quoted in the assurance report with the state they were run against |
| Example | the run quoted in the latest assurance report |

## The assurance report

As in A0, with two additions. For the SQ clauses the record is the latest
audit under `records/`; the report names it and says whether it was made
against the current specifications. The report does not run the audit; the
developer starts it (Specs-Audit). The mechanical evaluations are run with
one command, `tools/gate.sh`, which prints what state it checked and with
which tool versions, then runs `ruff`, the suite, and the trace tool, and
stops at the first failure; the report quotes its header.

## Changelog

- **A1.** Added Reqs-SQ-2, Gloss-SQ-1, Scen-CONF-1, Specs-TR-2, and the
  forms `Gloss` and `Scen`. Amended ConOps-SQ-1 (assumptions, deferred
  wants, the story header fields, the glossary's terms), ConOps-VAL-1 (a
  walkthrough per user category with the scenario inputs; the validation
  record), Reqs-SQ-1 (derivation from glossary terms), Reqs-CONF-1 (a
  partial run is not evidence), Specs-SQ-1 (evaluated by the audit; the
  between-document items), Specs-TR-1 (`Source` and `Scenarios`
  references). Retired ConOps-CONF-1: no clause has method *walkthrough* at
  A1, since the stories' examples became scenarios; the identifier is not
  reused.
