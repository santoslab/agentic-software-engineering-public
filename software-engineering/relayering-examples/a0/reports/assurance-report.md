# Assurance report: Message Guard

Requested by: the developer · Compiled by: an agent (Claude, one session) ·
Date: 2026-10-20 · Tree: tag v0, clean

## Summary

| Judgment | Claim | Holds? | Rests on |
|---|---|---|---|
| SQ | the specifications can be built from and checked against | holds | ConOps-SQ-1, Reqs-SQ-1, Specs-SQ-1 (records; the header parts run now) |
| RQ | the realization lints and its suite collects | holds | Code-RQ-1 (run now) |
| CONF | the realization does what the specifications say, as far as the evidence shows | holds | Reqs-CONF-1 (run now), ConOps-CONF-1 (record) |
| VAL | the specifications describe what the stakeholders intend | holds | ConOps-VAL-1 (record) |
| TR | every declared link resolves | holds | Specs-TR-1 (run now; derivations by record) |

## SQ · specification quality

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| ConOps-SQ-1 | holds (record) | `records/reviews.md`, entry 1: purpose, scope, two user categories, three stories each with identifier, method, category, and example; no sentence with two readings | review (human): the instructor, 2026-10-20, `specs/conops.md` at v0 |
| Reqs-SQ-1 | holds (record; header parts run now) | `records/reviews.md`, entry 1: four requirements, one sentence each, the three levels and the message form covered; `reports/conformance.md` lists REQ-0 to REQ-3 with no finding | review (human): the instructor, 2026-10-20, `specs/requirements.md` at v0; analysis: the clause reader in `tests/conformance.py`, run now at v0 |
| Specs-SQ-1 | holds (record) | `records/reviews.md`, entry 1: US-1 to REQ-3, US-2 to REQ-2, US-3 to REQ-1; no contradiction; one sense per term | review (human): the instructor, 2026-10-20, both files at v0 |

## RQ · realization quality

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| Code-RQ-1 | holds (run now) | `ruff check .` exit 0; `pytest --collect-only -q --no-cov` exit 0, 10 tests collected | analysis: ruff 0.17.1, pytest 9.1.1, Python 3.14.7, at v0 |

## CONF · conformance

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| Reqs-CONF-1 | holds (run now) | 10 passed; requirements coverage 4 of 4 test clauses with passing evidence (`reports/conformance.md`); branch coverage of `guard/` 100 percent | analysis: pytest 9.1.1 with the plugin in `tests/conftest.py` and pytest-cov 7.1.0, at v0, clauses REQ-0 to REQ-3 |
| ConOps-CONF-1 | holds (record) | `records/validation.md`, walkthrough table: US-1 `Public 42` passed unchanged; US-2 `Restricted 7` passed unchanged; US-3 `Critical 100` and `Critical 0` dropped; each "as the story expects" | walkthrough (human): the instructor as message sender (US-1, US-2) and as security officer (US-3), 2026-10-20, realization at v0 |

## VAL · validated

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| ConOps-VAL-1 | holds (record) | `records/validation.md`, sign-off: "The concept of operations, version A0, describes the guard I intend: a Critical message never leaves, and anything else leaves as it arrived." | sign-off: security officer and message sender, both roles played by the instructor, 2026-10-20, on `specs/conops.md` version A0 |

## TR · traceable

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| Specs-TR-1 | holds (run now; derivations by record) | `reports/conformance.md`, "Unknown identifiers: none", 10 markers; `records/reviews.md`, entry 1: every "Derived from" names an existing story | analysis: the plugin at v0 over 10 markers; review (human): the instructor, 2026-10-20 |

## What was run and read

- `uv run ruff check .` → exit 0 (ruff 0.17.1)
- `uv run pytest --collect-only -q --no-cov` → exit 0, 10 collected (pytest 9.1.1)
- `uv run pytest` → exit 0, 10 passed, branch coverage 100 percent; regenerated `reports/conformance.md` (pytest-cov 7.1.0; plugin `tests/conftest.py`)
- `records/reviews.md`, entry 1, dated 2026-10-20, naming state v0
- `records/validation.md`, walkthrough table and sign-off, dated 2026-10-20, naming realization v0 and `specs/conops.md` version A0

## What this report does not say

A row that holds is a supported claim with the scope its provenance states,
not a proof. A row evaluated by a person reports that a record exists and
what it says; the compiler did not repeat the evaluation. A row whose record
names a state other than the current tree is reported as such, and whether
the evidence still applies is for a person to decide. In this report every
record names v0, which is the current tree.
