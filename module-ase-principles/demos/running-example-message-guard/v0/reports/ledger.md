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
