# Assurance report: Message Guard

Requested by: the developer, before commit a1 · Compiled by: an agent
(Claude, the build session), by the procedure at the end of
`process/judgments.md` · Date: 2026-10-24 · Tree: the working tree committed
as `a1`, the last commit of version A1 (the validation record and the A1
sign-off, the amended ConOps-VAL-1, the README, the tool catalog, the skills
at 1.1 and 1.2; the realization unchanged from `a0`)

## Summary

| Judgment | Claim | Holds? | Rests on |
|---|---|---|---|
| SQ | the specifications can be built from and checked against | holds | ConOps-SQ-1, Reqs-SQ-1, Reqs-SQ-2, Gloss-SQ-1, Specs-SQ-1 (audit 05, no gap, on this tree; the header parts run now) |
| RQ | the realization lints and its suite collects | holds | Code-RQ-1 (run now) |
| CONF | the realization conforms to the requirements and to the scenarios, as far as the evidence shows | holds | Reqs-CONF-1, Scen-CONF-1 (run now) |
| VAL | the specifications describe what the stakeholders intend | holds, by a stand-in for the stakeholders | ConOps-VAL-1 (record) |
| TR | every declared link resolves, in both directions | holds | Specs-TR-1, Specs-TR-2 (run now) |

## SQ · specification quality

Audit 05 (`records/audit-05-skill.md`, `/audit-spec` 1.1) was run on the
specifications as this tree commits them: fourteen items applied, fourteen
*pass*, no gap. Since audit 04 the specifications changed only in their
references (the validation record, the amended ConOps-VAL-1).

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| ConOps-SQ-1 | holds (record; header parts run now) | `records/audit-05-skill.md`: C-1, C-4 to C-7 pass; `reports/conformance.md` lists US-1 to US-3 with method *test*, their `Scenarios`, and no finding | review (agent): `/audit-spec` 1.1, 2026-10-22, on this tree; analysis: the clause reader, run now |
| Reqs-SQ-1 | holds (record; header parts run now) | `records/audit-05-skill.md`: C-1, C-4, C-7, C-8 pass; `reports/conformance.md` lists REQ-0 to REQ-3 with no finding | as above |
| Reqs-SQ-2 | holds (record) | `records/audit-05-skill.md`: C-2 pass (REQ-0 ubiquitous with the guard as subject; REQ-1 to REQ-3 event-driven with the filter as subject and "shall") | review (agent): `/audit-spec` 1.1, 2026-10-22 |
| Gloss-SQ-1 | holds (record) | `records/audit-05-skill.md`: C-3 pass (thirteen terms, each defined once; no other specification defines one; every domain term used is a glossary term or a stated value of *security level*); C-10 pass | as above |
| Specs-SQ-1 | holds (record) | `records/audit-05-skill.md`: C-8 to C-14 pass (US-1 to REQ-3, US-2 to REQ-2, US-3 to REQ-1; REQ-0 from the glossary; every scenario derives from a story that lists it; no contradiction; no assumption or want as a requirement; every named file, clause, entry, and identifier exists; the helper agreed with all six scenario expectations) | review (agent): `/audit-spec` 1.1, 2026-10-22, on this tree; analysis: `tools/trace.py` 1.0, run now, for the link part |

## RQ · realization quality

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| Code-RQ-1 | holds (run now) | `uv run ruff check .` → "All checks passed!", exit 0; `uv run pytest --collect-only -q --no-cov` → "29 tests collected", exit 0 (13 of them the tooling tests, which cite no clause) | analysis: ruff 0.17.1 and pytest 9.1.1 on Python 3.14.7, over `guard/`, `tests/`, and `tools/` at this tree, 2026-10-24 |

## CONF · conformance

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| Reqs-CONF-1 | holds (run now) | `uv run pytest` → 29 passed, exit 0; requirements coverage 7 of 7 test clauses with passing evidence (`reports/conformance.md`, scope: full run, 29 collected, 16 cite a clause); branch coverage of `guard/` 100 percent | test: pytest 9.1.1 with the plugin in `tests/conftest.py` and pytest-cov 7.1.0, 2026-10-24; specifications, tests, and tools at this tree, realization unchanged from `a0`; clauses REQ-0 to REQ-3 |
| Scen-CONF-1 | holds (run now) | the same run: the six scenario tests passed, two per story (`reports/conformance.md`, the US rows) | test: the loader `tests/test_scenarios.py` over `specs/scenarios.json` at this tree, 2026-10-24; realization unchanged from `a0`; clauses US-1 to US-3 |

## VAL · validated

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| ConOps-VAL-1 | holds (record) | `records/validation.md`: the message sender walked US-1 with SC-1, SC-2 and US-2 with SC-3, SC-4, and decided that each story says what they want; the security officer walked US-3 with SC-5, SC-6 and decided the same, and signed with D-1 to D-3 deferred; the sign-off: "The concept of operations, version A1, describes the guard I intend: the marking alone decides, a Critical message never leaves, and anything else leaves as it arrived. The three deferred wants are mine and are not promised in this version." | the stakeholders' walkthrough and sign-off, both roles played by the build agent on the instructor's behalf, 2026-10-22, on `specs/conops.md` version A1 and the realization unchanged from `a0`. A stand-in: the record says so, and the instructor's own session supersedes these lines when it is recorded. The claim is as good as that stand-in |

## TR · traceable

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| Specs-TR-1 | holds (run now) | `reports/conformance.md`, "Unknown identifiers: None", 16 citing tests; `reports/trace-matrix.md`, findings none: every `Derived from`, `Source`, and `Scenarios` reference and every scenario's `derived_from` resolves (3 stories, 4 requirements, 6 scenarios, 3 source references) | analysis: the plugin in `tests/conftest.py` under `--strict-markers` and `tools/trace.py` 1.0, both run now at this tree, 2026-10-24 |
| Specs-TR-2 | holds (run now) | `uv run python tools/trace.py` → exit 0, "every declared link resolves"; `reports/trace-matrix.md` regenerated with an empty findings section; the twelve known-violation cases and the clean base pass in the same suite run | analysis: `tools/trace.py` 1.0, 2026-10-24, at this tree; the tool verified on its cases in the same run |

## What was run and read

- `tools/evaluate.sh` → exit 0. Header: `evaluate: 2026-10-24 12:11 ·
  Python 3.14.7 · pytest 9.1.1 · pytest-cov 7.1.0 · ruff 0.17.1 · trace.py
  1.0`. ruff: all checks passed; pytest: 29 passed, branch coverage 100
  percent, conformance "every test clause has passing evidence"; trace:
  "every declared link resolves"; `reports/conformance.md` and
  `reports/trace-matrix.md` regenerated.
- `uv run pytest --collect-only -q --no-cov` → exit 0, "29 tests collected".
- `records/audit-05-skill.md`, dated 2026-10-22, naming the working tree
  before this commit; no gap.
- `records/validation.md`, the two validation tables and the sign-off, dated
  2026-10-22, naming `specs/conops.md` version A1 and the a1 working tree.

## What this report does not say

A row that holds is a supported claim with the scope its provenance states,
not a proof. A row evaluated by a person reports that a record exists and
what it says; the compiler did not repeat the evaluation. A row whose record
names a state other than the current tree is reported as such, and whether
the evidence still applies is for a person to decide. In this report every
record names this tree. Two things the rows say that a green summary alone
would not: the VAL row's provenance names a stand-in for the stakeholders,
so its claim is only as good as that stand-in until the instructor's own
session replaces it; and the SQ rows rest on a skill whose first run caught
the build's own setup (audit 03), which is the reason to trust its later
passes more, not less.
