# Assurance report: SYSTEM

Requested by: WHO · Compiled by: WHO (a person by name and role; an agent by
model) · Date: DATE · Tree: STATE (a tag or commit, and "clean" or "N
uncommitted paths")

## Summary

| Judgment | Claim | Holds? | Rests on |
|---|---|---|---|
| SQ | one sentence | holds / does not hold / not evaluated | the clauses below |
| RQ | | | |
| CONF | | | |
| VAL | | | |
| TR | | | |

## SQ · specification quality

| Clause | Holds? | Evidence | Provenance |
|---|---|---|---|
| ConOps-SQ-1 | holds (record) | `records/reviews.md`, entry N | review (human): WHO, DATE, state STATE |
| Reqs-SQ-1 | | | |
| Specs-SQ-1 | | | |

(one section per judgment, in the order of the summary)

## What was run and read

- `COMMAND` → exit CODE (tool versions)
- `records/FILE`, entry N, dated DATE, naming state STATE

## What this report does not say

Fixed text, kept in every report: A row that holds is a supported claim
with the scope its provenance states, not a proof. A row evaluated by a
person reports that a record exists and what it says; the compiler did not
repeat the evaluation. A row whose record names a state other than the
current tree is reported as such, and whether the evidence still applies is
for a person to decide.

### Status words

- **holds (run now)**: the evaluation was run against the current tree while
  compiling this report, and passed.
- **holds (record)**: a record exists, names the current state, and records a
  decision that the clause holds.
- **record names another state**: a record exists but was made against a
  different state of the artifact; the decision is reported, its currency is
  not.
- **does not hold**: a run failed, or a record records a negative decision.
- **not evaluated**: no run was possible or no record exists.
