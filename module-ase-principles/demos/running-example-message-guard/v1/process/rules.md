# Development Rules: Message Guard (version A1)

Rules are filed by the development-state judgment they maintain (SQ, RQ, CONF,
VAL, TR) or by the process concern they serve (WF, workflow; RPT, reports).
Every rule has the same fields, so a reader can see when a rule is complete.
Four styles are used from this version: an *obligation* says every X MUST
have property P; a *gate* says WHEN step S would complete, condition C MUST
hold; a *procedure* says to do activity A, follow steps 1 to n and stop at
step k to report; a *form* says record R has fields F, is produced by whom
and when, and is read by whom. Identifiers are never renumbered. An amended
rule keeps its identifier, and the amendment is recorded in the changelog at
the end of this file. An example in a rule comes from this system.

## SQ-1 · The specifications are well-formed and consistent

| Field | |
|---|---|
| Style | obligation |
| Maintains | SQ |
| When | at every commit; applies to the specifications as a whole, every file under `specs/`, including identified clauses and contextual specification text |
| Statement | Every identified verification clause MUST carry a unique identifier and a verification method. Every requirement MUST identify the story or the glossary terms it derives from. The specifications MUST be unambiguous, internally consistent, consistent with their companion specifications, and complete for their stated scope and abstraction level. Scope, terms, assumptions, and deferred wants MUST be reviewed with the identified clauses. |
| Decided by | review (human): a person reads the specifications together, informed by the audit of SQ-2, and records the reading in the ledger. The identifier and method parts are also read by `tests/conformance.py`, which lists the clauses it finds and reports a malformed header. |
| Evidence | the SQ row of `reports/ledger.md` |
| On failure | the clause is amended before any test cites it; the SQ row is not established |
| Example | REQ-1 carries method *test* and derives from US-3; REQ-0 derives from the glossary terms message, security level, and payload |

## SQ-2 · The audit procedure

| Field | |
|---|---|
| Style | procedure |
| Maintains | SQ |
| When | before a commit that changes any specification; applies to every file under `specs/` |
| Statement | To audit the specifications: (1) read every file under `specs/` in full before the first check; (2) within each document, check well-formed headers, EARS form against the declared pattern, glossary discipline, and a reason on every judgment clause; (3) between documents, check that every story has at least one requirement and every requirement derives from a story or glossary terms, that no two clauses contradict, that each term is used in one sense, and that assumptions and deferred wants have not become requirements; (4) by execution, decide from the clauses what every example and scenario must output and compare with its stated expectation; (5) stop and report every gap in the form of RPT-2. A person rules on each gap; an accepted gap is amended and the audit is rerun on the amended text. |
| Decided by | review (agent) running `/audit-spec`, or review (human) by the same checklist; rulings by a person |
| Evidence | `reports/audit-NN.md` |
| On failure | an open gap leaves SQ not established; the amendment is made and the audit rerun before the commit |
| Example | audit 03 found that the draft of REQ-1 also required a record of the drop, which the scope excludes; the ruling deleted that clause and kept the want as D-1 |

## SQ-3 · Requirements are in EARS form

| Field | |
|---|---|
| Style | obligation |
| Maintains | SQ |
| When | at every commit; applies to every clause of `specs/requirements.md` |
| Statement | Every requirement MUST declare its EARS pattern in a `Pattern` field (ubiquitous, event-driven, state-driven, unwanted-behavior, optional-feature, or complex) and MUST have that pattern's shape: a trigger where the pattern has one, the filter or the guard as subject, and "shall". |
| Decided by | review within SQ-2 (checklist item C-2). Planned for A2: analysis by a script. |
| Evidence | the C-2 row of the audit report |
| On failure | the clause is rewritten before any test cites it |
| Example | the draft "Restricted messages are allowed through." became "When the filter is given a message whose security level is Restricted, the filter shall pass the message unchanged." |

## SQ-4 · Glossary discipline

| Field | |
|---|---|
| Style | obligation |
| Maintains | SQ |
| When | at every commit; applies to every file under `specs/` |
| Statement | Every domain term used in a specification MUST be defined exactly once in `specs/glossary.md` and MUST be used only in its defined sense. No specification other than the glossary MUST define a term. |
| Decided by | review within SQ-2 (checklist items C-3 and C-10): a person in audit 01, the agent in audit 02, the skill in audit 03. Planned for A2: analysis by a script. |
| Evidence | the C-3 and C-10 rows of the audit report |
| On failure | the term is defined in the glossary, or the sentence is rewritten with a defined term |
| Example | "sensitive" in the draft of US-3 was undefined; the ruling rewrote the story as "every message whose security level is Critical" |

## RQ-1 · The realization lints and the suite collects

| Field | |
|---|---|
| Style | obligation |
| Maintains | RQ |
| When | at every commit; applies to `guard/`, `tests/`, and `tools/` |
| Statement | The realization MUST pass `ruff check`, and the test suite MUST collect without error. |
| Decided by | analysis: `uv run ruff check .` and `uv run pytest --collect-only -q --no-cov`; a non-zero exit code fails it |
| Evidence | the exit codes, recorded in the dev-log entry of the task |
| On failure | the finding is fixed before the commit (WF-1) |
| Example | the gate run recorded in dev-log entry 2 |

## CONF-1 · Every mechanical clause has passing evidence, and the code is exercised

| Field | |
|---|---|
| Style | obligation |
| Maintains | CONF |
| When | at every commit; applies to every clause whose method is *test* |
| Statement | Every clause with method *test* MUST be cited, by marker, by at least one test; every citing test MUST pass; and the suite MUST reach 100 percent branch coverage of `guard/`. The loader `tests/test_scenarios.py` MUST run every scenario of `specs/scenarios.json` as a test citing the story the scenario derives from. |
| Decided by | analysis: `uv run pytest`. The plugin in `tests/conftest.py` fails the run on a clause with no evidence or with a failing citation (requirements coverage), on a marker that names no clause, and on a finding of the clause reader; `pytest-cov` fails it below 100 percent (structural coverage). A partial run (tests deselected) is labeled in the report and does not count. |
| Evidence | `reports/conformance.md`; the coverage table in the run output, recorded in the dev log |
| On failure | a test is added or fixed, or the code is fixed; a clause is never weakened, and a scenario is never edited, to make the run pass |
| Example | REQ-1 is cited by `test_filter.py::test_critical_is_dropped`; US-3 by `test_scenarios.py::test_scenario[SC-5]` and `[SC-6]` |

## CONF-2 · Every judgment clause has a walkthrough record

| Field | |
|---|---|
| Style | obligation |
| Maintains | CONF |
| When | before the CONF row is established at a commit; applies to every clause whose method is *walkthrough* |
| Statement | Every clause with method *walkthrough* MUST have a record stating who walked it and in which role, when, against which commit, what was observed, and the finding. |
| Decided by | review (human) of the record |
| Evidence | a walkthrough record (`reports/walkthrough.md` at v0 and at a1-specs, kept as the appendix of `reports/validation.md`). From commit a1-scenarios no clause carries method *walkthrough*, so no record is required; the rule stays for the next judgment clause |
| On failure | the walkthrough is performed and recorded before the CONF row is established |
| Example | US-3 walked by the security officer on 2026-10-20 against v0, and again at a1-specs before its method became *test* |

## VAL-1 · The concept of operations carries a sign-off

| Field | |
|---|---|
| Style | obligation |
| Maintains | VAL |
| When | before the VAL row is established at a commit; applies to `specs/conops.md` |
| Statement | The concept of operations MUST carry a sign-off in which a stakeholder of each user category states that it describes what they intend, naming the version signed. |
| Decided by | review (human) of the sign-off |
| Evidence | `reports/validation.md`, section "Sign-off" |
| On failure | VAL is not established; the concept of operations is revised with the stakeholder until it is signed |
| Example | the security officer signed version A0 on 2026-10-20 and version A1 on 2026-10-22 |

## VAL-2 · The validation record

| Field | |
|---|---|
| Style | form |
| Maintains | VAL |
| When | before the sign-off of VAL-1, whenever the concept of operations has changed since the last sign-off; produced by a stakeholder of each user category walking their stories on the running realization; read by whoever reads the VAL row of the ledger |
| Statement | The validation record MUST state, per user category: who walked, in which role, when, against which realization version, which stories, with which scenario inputs, what was observed, and the decision to sign or to withhold the signature, with its reason. Observing the expected output is not the decision; the decision is whether the story describes what the stakeholder wants. |
| Decided by | review (human) of the record |
| Evidence | `reports/validation.md` |
| On failure | VAL is not established |
| Example | the security officer's section at v1: US-3 walked with SC-5 and SC-6; decision: sign for A1 with D-1 to D-3 deferred |

## TR-1 · Every reference resolves

| Field | |
|---|---|
| Style | obligation |
| Maintains | TR |
| When | at every commit; applies to every `req` marker, every `Derived from`, and every `Source` reference |
| Statement | Every supplied `req` marker MUST name a clause identifier defined in the specifications. Every `Derived from` reference MUST identify an existing story or existing glossary terms. Every `Source` reference MUST identify an entry of `reference/elicitation.md`. |
| Decided by | analysis: the plugin in `tests/conftest.py` lists unknown identifiers and fails the run; `--strict-markers` rejects a marker that is not declared; `tools/trace.py` (TR-2) resolves the `Derived from`, `Source`, and `Scenarios` references. |
| Evidence | the "Unknown identifiers" section of `reports/conformance.md`; the findings section of `reports/trace-matrix.md` |
| On failure | the marker or the reference is corrected |
| Example | `@pytest.mark.req("REQ-2")` resolves to REQ-2 in `specs/requirements.md`; US-3's `Source: E-1` resolves to entry E-1 of the elicitation record |

## TR-2 · The trace matrix

| Field | |
|---|---|
| Style | form |
| Maintains | TR |
| When | at every commit; produced by `tools/trace.py` as the last step of the gate; read by whoever asks what a story, a requirement, or a test is connected to, and by the audit for its derivation check |
| Statement | `reports/trace-matrix.md` MUST be regenerated at every commit and MUST carry: a header naming the tool's version, the files read, the number of tests collected and citing, and the repository state checked; the forward table (story to requirements to scenarios to tests); the backward tables (requirement to its derivation and tests; test to the clauses it cites); and a findings section listing every declared link that does not resolve, every story with no requirement, every requirement with no derivation, every test clause with no citing test, and every finding of the clause reader. The findings section MUST be empty. |
| Decided by | analysis: the exit code of `uv run python tools/trace.py`, non-zero on any finding |
| Evidence | `reports/trace-matrix.md` |
| On failure | the gate is red; the reference, the clause, or the test is corrected; a link is never deleted to make the matrix clean |
| Example | REQ-3 derived from US-2 instead of US-1: every link resolves, and the matrix reports "story without requirement at US-1" |

## WF-1 · The gate stands before every commit

| Field | |
|---|---|
| Style | gate |
| Maintains | RQ, the mechanical part of CONF, and TR |
| When | WHEN work would be committed |
| Statement | The gate command `tools/gate.sh` MUST exit 0 before the work is committed. |
| Decided by | analysis: the exit code of `tools/gate.sh`, which prints a provenance header (the date, the repository state, the tool versions), then runs RQ-1's analyses, `uv run pytest` with the conformance plugin and coverage, and `tools/trace.py` |
| Evidence | the dev-log entry of the task records the run and copies the header |
| On failure | the commit is not made; the work is returned to the task |
| Example | the v0 gate run in dev-log entry 3 |

## WF-2 · Elicitation precedes a revision of the concept of operations

| Field | |
|---|---|
| Style | procedure |
| Maintains | VAL and SQ |
| When | before any revision of `specs/conops.md` that is to reflect what a stakeholder wants; applies to that file and to the glossary entries the answers define |
| Statement | To revise the concept of operations with its stakeholders, run `/elicit` or follow its steps by hand: (1) read the concept of operations, the glossary, and the existing elicitation record; (2) ask at most five questions, one at a time, each addressed to a user category, with options and a recommended default; (3) record each question and the verbatim answer, with who answered and when, under an E identifier in `reference/elicitation.md`; (4) apply each accepted answer to the part of the specification it affects, citing the identifier; (5) the person reviews the resulting diff and runs the audit of SQ-2 before the revision is committed. |
| Decided by | review (human) of the record and of the diff; the audit that follows |
| Evidence | `reference/elicitation.md`; the dev-log entry that names the run |
| On failure | the revision is not committed |
| Example | E-2: the security officer's "I'd like one eventually; not needed for this version" became deferred want D-1 and no requirement |

## RPT-1 · The dev log and the ledger are kept

| Field | |
|---|---|
| Style | obligation |
| Maintains | the record of every judgment |
| When | at every task and at every commit |
| Statement | Every dev-log entry MUST name the task, the files touched, the judgments touched, and the gate result. At every commit the ledger MUST state the five judgments in a table named for that checkpoint, each with status, evidence, and provenance: who or what verified it, against which artifact version, over which clauses. |
| Decided by | review (human) |
| Evidence | `reports/dev-log.md`; `reports/ledger.md` |
| On failure | the entry is completed before the next task begins |
| Example | the ledger tables at v0 and at a1-specs |

## RPT-2 · The gap list

| Field | |
|---|---|
| Style | form |
| Maintains | the record of SQ |
| When | at the end of every audit (SQ-2); produced by the auditor, read by the person who rules and by whoever reads the SQ row of the ledger |
| Statement | A gap list MUST carry: the audit identifier; the date; the auditor (a person by name and role, an agent by model and prompt, or a skill by name and version); the specifications and the state audited; the checks applied, each with *pass* or the gaps it produced; and one row per gap with an identifier, the location (clause identifier or section), the check violated, the text quoted exactly, one proposed resolution, the ruling (open, accepted, ruled otherwise, rejected with a reason, or deferred), and the amendment made. |
| Decided by | review (human) that the report has the form |
| Evidence | `reports/audit-NN.md` |
| On failure | the report is completed before rulings are given |
| Example | `reports/audit-03-skill.md` |

## Changelog

- **A1, commit a1-specs.** Added SQ-2, SQ-3, SQ-4, WF-2, RPT-2 (styles added:
  procedure, form). Amended SQ-1 (scope is every file under `specs/`;
  derivation from glossary terms; assumptions and deferred wants reviewed),
  TR-1 (`Source` references; glossary derivation), and RPT-1 (a ledger table
  per named checkpoint).
- **A1, commit a1-scenarios.** The stories' method became *test*, their
  examples the scenarios of `specs/scenarios.json`. Amended CONF-1 (the
  loader runs every scenario; the plugin fails on a reader finding and
  labels a partial run) and CONF-2 (no record required while no clause has
  method *walkthrough*).
- **A1, commit a1-trace.** Added TR-2 (the trace matrix, decided by
  `tools/trace.py`). Amended TR-1 (the reference parts are now decided by
  the tool, not read by a person) and WF-1 (the gate runs the trace tool and
  prints a provenance header).
- **A1, commit v1.** Added VAL-2 (the validation record). Amended VAL-1
  (evidence: `reports/validation.md`) and CONF-2 (the earlier walkthrough
  records are the appendix of `reports/validation.md`);
  `reports/walkthrough.md` renamed to `reports/validation.md`.
