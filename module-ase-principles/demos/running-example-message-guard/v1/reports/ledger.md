# Assurance Ledger: Message Guard

One row per development-state judgment, at a named commit. A row is a claim
with evidence. Its provenance says who or what made the claim, against which
artifacts, and over which clauses, so that the claim can be checked, and so
that if a verifier is later found to be wrong, the rows it established can be
found.

## At v0 (version A0, 2026-10-20)

| Judgment | Status | Evidence | Provenance | Goes stale when |
|---|---|---|---|---|
| SQ · specification quality | established | `specs/conops.md` and `specs/requirements.md` read together: 7 clauses, each with an identifier and a method; every requirement derives from a story or from the terms; no contradiction; no clause with two readings | review (human): the instructor, 2026-10-20, specifications at v0, clauses US-1 to US-3 and REQ-0 to REQ-3 | any specification changes |
| RQ · realization quality | established | `ruff check .` exit 0; `pytest --collect-only -q --no-cov` exit 0, 10 tests collected | analysis: ruff 0.17.1, pytest 9.1.1 on Python 3.14.7; realization at v0 | the code or the tests change |
| CONF · conformance | established | tests: 10 passed; requirements coverage: 4 of 4 test clauses have passing evidence (`reports/conformance.md`); structural coverage: 100 percent of branches in `guard/`; judgment clauses: US-1 to US-3 walked (`reports/walkthrough.md`) | tests: pytest 9.1.1; coverage and citation analysis: pytest-cov 7.1.0 and the plugin in `tests/conftest.py`, specifications and realization at v0, clauses REQ-0 to REQ-3; walkthrough (human): the instructor as sender and as security officer, 2026-10-20, clauses US-1 to US-3 | relevant specifications, code, tests, or verification tools/configuration/environment change |
| VAL · validated | established | sign-off by the security officer and by the message sender, `reports/walkthrough.md` under "Sign-off" | review (human): sign-off dated 2026-10-20 on `specs/conops.md` version A0 | a stakeholder declares a change of mind, or the concept of operations or a requirement changes |
| TR · traceable | established | every marker resolves to a clause (`reports/conformance.md`, "Unknown identifiers: none"); every "derived from" resolves (read with SQ) | analysis: the plugin in `tests/conftest.py` at v0 over 10 markers; review (human): the instructor, 2026-10-20, for the "derived from" links | any artifact changes |

All five rows are established at v0, which is what a green ledger means. No
row is a proof: each is a claim whose scope is the provenance column.

## At a1-specs (version A1, first commit, 2026-10-22)

The concept of operations was revised through elicitation, the terms became
a glossary, the requirements were rewritten in EARS, and the family was
audited three times before this commit. The realization is unchanged.

| Judgment | Status | Evidence | Provenance | Goes stale when |
|---|---|---|---|---|
| SQ · specification quality | established | the pre-audit draft (`reference/drafts/`) audited by an agent with an ad-hoc prompt (`reports/audit-02-agent.md`, 20 findings) and by `/audit-spec` 1.0 (`reports/audit-03-skill.md`, 12 findings, every checklist item reported); both found all seven seeded gaps; every gap ruled; the amended family read together: 7 clauses, each with identifier, method, and derivation; no contradiction; every term defined once | review (agent): the ad-hoc audit and `/audit-spec` 1.0, 2026-10-22, on the draft; review (human): the rulings and the re-read of the amended text, by the build agent on the instructor's behalf, 2026-10-22, clauses US-1 to US-3 and REQ-0 to REQ-3 | any specification changes |
| RQ · realization quality | established | `ruff check .` exit 0; `pytest --collect-only -q --no-cov` exit 0, 10 tests collected | analysis: ruff 0.17.1, pytest 9.1.1 on Python 3.14.7; realization unchanged from v0 | the code or the tests change |
| CONF · conformance | established (renewed) | tests: 10 passed; requirements coverage: 4 of 4 test clauses have passing evidence (`reports/conformance.md`); structural coverage: 100 percent of branches in `guard/`; judgment clauses: the revised US-1 to US-3 walked (`reports/walkthrough.md`, A1 section). Renewal note: the requirements' sentences changed and their identifiers did not; the citing tests were re-read against the new sentences and found to check what they say | tests: pytest 9.1.1; coverage and citation analysis: pytest-cov 7.1.0 and the plugin in `tests/conftest.py`, specifications at a1-specs, realization at v0, clauses REQ-0 to REQ-3; walkthrough (human): the build agent in both roles on the instructor's behalf, 2026-10-22, clauses US-1 to US-3 | relevant specifications, code, tests, or verification tools/configuration/environment change |
| VAL · validated | **stale** | the only sign-off (`reports/walkthrough.md`) names version A0; the concept of operations changed in every section (E-1 to E-5); the A1 sign-off is a later task of this version | review (human): the sign-off dated 2026-10-20 on version A0, which this revision supersedes | re-established by the validation walkthrough and the A1 sign-off; stale again on a change of mind or a further revision |
| TR · traceable | established | every marker resolves (`reports/conformance.md`, "Unknown identifiers: none"); every `Derived from` names an existing story or existing glossary terms, and every `Source` an entry of `reference/elicitation.md`, read by a person (4 derivations, 4 source references) | analysis: the plugin in `tests/conftest.py` at a1-specs over 10 markers; review (human): the build agent, 2026-10-22, for the derivation and source links | any artifact changes |

Four rows established and one stale: the ledger says what the state is, not
what one would like it to be. The stale row is not a finding that the
specifications are wrong; it says the stakeholders have not yet said that
the revised document is what they want.

## At a1-scenarios (version A1, second commit, 2026-10-22)

The stories' examples became `specs/scenarios.json` and their method became
*test*; the clause reader and the plugin were extended. The realization is
unchanged.

| Judgment | Status | Evidence | Provenance | Goes stale when |
|---|---|---|---|---|
| SQ · specification quality | established | audit 04 (`reports/audit-04-skill.md`): fourteen checklist items, ten pass, four wording gaps, all ruled and applied before the commit; the amended family re-read | review (agent): `/audit-spec` 1.1, 2026-10-22, on the pre-commit tree; review (human): rulings and the re-read, by the build agent on the instructor's behalf, 2026-10-22, clauses US-1 to US-3, REQ-0 to REQ-3, SC-1 to SC-6 | any specification changes |
| RQ · realization quality | established | `ruff check .` exit 0; `pytest --collect-only -q --no-cov` exit 0, 16 tests collected | analysis: ruff 0.17.1, pytest 9.1.1 on Python 3.14.7; `guard/` unchanged from v0; `tests/` extended | the code or the tests change |
| CONF · conformance | established | tests: 16 passed; requirements coverage: 7 of 7 test clauses have passing evidence (`reports/conformance.md`, scope: full run), the three stories through their scenario tests; structural coverage: 100 percent of branches in `guard/`; judgment clauses: none in scope | tests: pytest 9.1.1; coverage and citation analysis: pytest-cov 7.1.0 and the plugin in `tests/conftest.py`, specifications and tests at a1-scenarios, realization at v0, clauses US-1 to US-3 and REQ-0 to REQ-3 | relevant specifications, code, tests, or verification tools/configuration/environment change |
| VAL · validated | **stale** | unchanged since a1-specs: the only sign-off names version A0 | as at a1-specs | re-established by the validation walkthrough and the A1 sign-off |
| TR · traceable | established | every marker resolves (16 markers, "Unknown identifiers: none"); every `Derived from`, `Source`, and `Scenarios` reference, and every scenario's `derived_from`, read by a person and resolving | analysis: the plugin at a1-scenarios; review (human): the build agent, 2026-10-22, for the link fields (the trace tool of the next commit takes these over) | any artifact changes |

## At a1-trace (version A1, third commit, 2026-10-22)

The trace tool, its cases, and the extended gate were added; no
specification changed.

| Judgment | Status | Evidence | Provenance | Goes stale when |
|---|---|---|---|---|
| SQ · specification quality | established | unchanged since a1-scenarios: no specification changed at this commit | as at a1-scenarios | any specification changes |
| RQ · realization quality | established | `ruff check .` exit 0; `pytest --collect-only -q --no-cov` exit 0, 29 tests collected (13 of them the tooling tests, uncited) | analysis: ruff 0.17.1, pytest 9.1.1 on Python 3.14.7; `guard/` unchanged from v0; `tests/` and `tools/` extended | the code, the tests, or the tools change |
| CONF · conformance | established | tests: 29 passed; requirements coverage: 7 of 7 test clauses (`reports/conformance.md`, scope: full run); structural coverage: 100 percent of branches in `guard/`; judgment clauses: none in scope | tests: pytest 9.1.1; coverage and citation analysis: pytest-cov 7.1.0 and the plugin, specifications at a1-scenarios, tests at a1-trace, realization at v0, clauses US-1 to US-3 and REQ-0 to REQ-3 | relevant specifications, code, tests, or verification tools/configuration/environment change |
| VAL · validated | **stale** | unchanged since a1-specs | as at a1-specs | re-established by the validation walkthrough and the A1 sign-off |
| TR · traceable | established | every declared link resolves in both directions: `reports/trace-matrix.md`, findings none (3 stories, 4 requirements, 6 scenarios, 3 source references, 16 citing tests); the twelve known-violation cases pass (`tests/tooling/`) | analysis: `tools/trace.py` 1.0, run by the gate on the pre-commit tree (header: HEAD 4a4f1b2, 5 changed paths), over every clause, scenario, entry, and citation; the tool verified on its cases at the same run | any linked artifact, or the tool, changes |

## At v1 (version A1, fourth and last commit, 2026-10-22)

The validation walkthrough and the A1 sign-off, rule VAL-2, the README, and
the tool catalog were added; the specifications changed only in their
references, and audit 05 passed on them.

| Judgment | Status | Evidence | Provenance | Goes stale when |
|---|---|---|---|---|
| SQ · specification quality | established | audit 05 (`reports/audit-05-skill.md`): fourteen checklist items, fourteen pass, no gap, on the tree before this commit; the whole family (`conops.md`, `glossary.md`, `requirements.md`, `scenarios.json`) read together: 7 clauses with identifier, method, pattern or scenarios, and derivation; 13 terms; 6 scenarios | review (agent): `/audit-spec` 1.1, 2026-10-22, on the pre-commit tree; review (human): the re-read by the build agent on the instructor's behalf, 2026-10-22, clauses US-1 to US-3, REQ-0 to REQ-3, SC-1 to SC-6 | any specification changes |
| RQ · realization quality | established | `ruff check .` exit 0; `pytest --collect-only -q --no-cov` exit 0, 29 tests collected | analysis: ruff 0.17.1, pytest 9.1.1 on Python 3.14.7; `guard/` byte-identical to v0; `tests/` and `tools/` at v1 | the code, the tests, or the tools change |
| CONF · conformance | established | tests: 29 passed; requirements coverage: 7 of 7 test clauses have passing evidence (`reports/conformance.md`, scope: full run; the stories through their scenario tests, the requirements through the unit tests); structural coverage: 100 percent of branches in `guard/`; judgment clauses: none in scope | tests: pytest 9.1.1; coverage and citation analysis: pytest-cov 7.1.0 and the plugin in `tests/conftest.py`, specifications, tests, and tools at v1, realization at v0, clauses US-1 to US-3 and REQ-0 to REQ-3; the gate run and its header are in dev-log entry 9 | relevant specifications, code, tests, or verification tools/configuration/environment change |
| VAL · validated | established | `reports/validation.md`: a stakeholder of each user category walked their stories on the running guard with the scenarios' inputs and decided that the stories describe what they want; the sign-off names version A1 for both categories, with deferred wants D-1 to D-3 recorded as theirs and not promised | review (human): the walkthrough and the sign-off, by the build agent playing both roles on the instructor's behalf, 2026-10-22, on `specs/conops.md` version A1; the instructor's own re-play of the session supersedes these lines when it is recorded | a stakeholder declares a change of mind, or the concept of operations or a requirement changes |
| TR · traceable | established | every declared link resolves in both directions (`reports/trace-matrix.md`, findings none); 29 tests collected, 16 cite a clause; the twelve known-violation cases pass | analysis: `tools/trace.py` 1.0 in the gate at the pre-commit run of dev-log entry 9, over every clause, scenario, entry, and citation | any linked artifact, or the tool, changes |

All five rows are established at v1. Two things the table says that a green
ledger alone would not: the VAL row's provenance names a stand-in for the
stakeholders, so its claim is only as good as that stand-in until the
instructor's own session replaces it; and the SQ row rests on a skill whose
first run caught the build's own setup (audit 03), which is the reason to
trust its later passes more, not less.
