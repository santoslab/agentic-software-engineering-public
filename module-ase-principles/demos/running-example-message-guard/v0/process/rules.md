# Development Rules: Message Guard (version A0)

Rules are filed by the development-state judgment they maintain (SQ, RQ, CONF,
VAL, TR) or by the process concern they serve (WF, workflow; RPT, reports).
Every rule has the same fields, so a reader can see when a rule is complete.
Two styles are used in this version: an *obligation* says every X MUST have
property P; a *gate* says WHEN step S would complete, condition C MUST hold.
Identifiers are never renumbered; an example in a rule comes from this system.

## SQ-1 · The specifications are well-formed and consistent

| Field | |
|---|---|
| Style | obligation |
| Maintains | SQ |
| When | at every commit; applies to the specifications as a whole, including identified clauses and contextual specification text |
| Statement | Every identified verification clause MUST carry a unique identifier and a verification method. Every requirement MUST identify the story or specification section it derives from. The specifications MUST be unambiguous, internally consistent, consistent with their companion specifications, and complete for their stated scope and abstraction level. Scope, terms, and environmental assumptions MUST be reviewed with the identified clauses. |
| Decided by | review (human): a person reads the specifications together and records the reading in the ledger. The identifier and method parts are also read by `tests/conformance.py`, which lists the clauses it finds. |
| Evidence | the SQ row of `reports/ledger.md` |
| On failure | the clause is amended before any test cites it; the SQ row is not established |
| Example | REQ-1 carries method *test* and derives from US-3 |

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
| Statement | Every clause with method *test* MUST be cited, by marker, by at least one test; every citing test MUST pass; and the suite MUST reach 100 percent branch coverage of `guard/`. |
| Decided by | analysis: `uv run pytest`. The plugin in `tests/conftest.py` fails the run on a clause with no evidence or with a failing citation (requirements coverage); `pytest-cov` fails it below 100 percent (structural coverage). |
| Evidence | `reports/conformance.md`; the coverage table in the run output, recorded in the dev log |
| On failure | a test is added or fixed, or the code is fixed; a clause is never weakened to make the run pass |
| Example | REQ-1 is cited by `test_filter.py::test_critical_is_dropped` |

## CONF-2 · Every judgment clause has a walkthrough record

| Field | |
|---|---|
| Style | obligation |
| Maintains | CONF |
| When | before the CONF row is established at a commit; applies to every clause whose method is *walkthrough* |
| Statement | Every clause with method *walkthrough* MUST have a record stating who walked it and in which role, when, against which commit, what was observed, and the finding. |
| Decided by | review (human) of the record |
| Evidence | `reports/walkthrough.md` |
| On failure | the walkthrough is performed and recorded before the CONF row is established |
| Example | US-3 walked by the security officer on 2026-10-20 against v0 |

## VAL-1 · The concept of operations carries a sign-off

| Field | |
|---|---|
| Style | obligation |
| Maintains | VAL |
| When | before the VAL row is established at a commit; applies to `specs/conops.md` |
| Statement | The concept of operations MUST carry a sign-off in which a stakeholder of each user category states that it describes what they intend, naming the version signed. |
| Decided by | review (human) of the sign-off |
| Evidence | `reports/walkthrough.md`, section "Sign-off" |
| On failure | VAL is not established; the concept of operations is revised with the stakeholder until it is signed |
| Example | the security officer signed version A0 on 2026-10-20 |

## TR-1 · Every reference resolves

| Field | |
|---|---|
| Style | obligation |
| Maintains | TR |
| When | at every commit; applies to every `req` marker and every "derived from" |
| Statement | Every supplied `req` marker MUST name a clause identifier defined in the specifications. Every "derived from" reference MUST identify an existing story or specification section; A0 permits REQ-0's reference to the ConOps Terms section. |
| Decided by | analysis: the plugin in `tests/conftest.py` lists unknown identifiers and fails the run; `--strict-markers` rejects a marker that is not declared. The "derived from" part is read by a person with SQ-1. |
| Evidence | the "Unknown identifiers" section of `reports/conformance.md` |
| On failure | the marker or the reference is corrected |
| Example | `@pytest.mark.req("REQ-2")` resolves to REQ-2 in `specs/requirements.md` |

## WF-1 · The gate stands before every commit

| Field | |
|---|---|
| Style | gate |
| Maintains | RQ and the mechanical part of CONF (and, through the plugin, TR) |
| When | WHEN work would be committed |
| Statement | The gate command `tools/gate.sh` MUST exit 0 before the work is committed. |
| Decided by | analysis: the exit code of `tools/gate.sh`, which runs RQ-1's analyses and then `uv run pytest` with the conformance plugin and coverage |
| Evidence | the dev-log entry of the task records the run |
| On failure | the commit is not made; the work is returned to the task |
| Example | the v0 gate run in dev-log entry 3 |

## RPT-1 · The dev log and the ledger are kept

| Field | |
|---|---|
| Style | obligation |
| Maintains | the record of every judgment |
| When | at every task and at every commit |
| Statement | Every dev-log entry MUST name the task, the files touched, the judgments touched, and the gate result. At every commit the ledger MUST state the five judgments, each with status, evidence, and provenance: who or what verified it, against which artifact version, over which clauses. |
| Decided by | review (human) |
| Evidence | `reports/dev-log.md`; `reports/ledger.md` |
| On failure | the entry is completed before the next task begins |
| Example | the ledger at v0 |
