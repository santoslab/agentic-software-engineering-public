# Audit 04: the specifications before commit a1-scenarios, by the `/audit-spec` skill (version A1)

| Field | |
|---|---|
| Audit | 04 |
| Date | 2026-10-22 |
| Auditor | `/audit-spec` 1.1, run by an agent (Claude, a fresh session) |
| Audited | the working tree before commit a1-scenarios: `specs/conops.md`, `specs/glossary.md`, `specs/requirements.md`, `specs/scenarios.json` |
| Checks applied | C-1 to C-14 of `checklist.md` 1.1 |
| Read first | the four specifications and `process/rules.md`; `reference/elicitation.md`; then every file the specifications name, for C-13; `tools/walk.py` run on the six scenario inputs, for C-14 |

Rule SQ-2 puts an audit before any commit that changes a specification. The
task of this commit changed the stories' headers (method *test*, a
`Scenarios` field), two sentences of the concept of operations, and added
the scenario file; this is the audit of that state, and the first audit of
this version to find no seeded gap, since the drafts were amended at
a1-specs.

## Checks

| Check | Result |
|---|---|
| C-1 Well-formed header | pass: seven headers, unique identifiers, method *test*, only defined keys; SC-1 to SC-6 unique and complete |
| C-2 EARS form | pass: REQ-0 ubiquitous; REQ-1 to REQ-3 event-driven, each with its pattern's shape |
| C-3 Glossary discipline | pass: thirteen terms, each defined once; no other specification defines one; every domain term used is a glossary term or a stated value of *security level* |
| C-4 Unambiguous | G-1. Not reported, per the item: value equality in REQ-2 and REQ-3; "large" in D-2 |
| C-5 Judgment clauses state why | pass, no clause in scope: all seven clauses carry method *test* |
| C-6 Implementation-independent | pass |
| C-7 Complete for the stated scope | pass: each security level has an outcome; nothing outside the boundary is specified |
| C-8 Derivation both ways | G-2. Every story has a requirement; every scenario derives from a story and is listed by it |
| C-9 No contradiction | G-1 (read as a second reading of §2 against REQ-0); otherwise pass |
| C-10 One term, one sense | pass; "stopped" appears only as the synonym the glossary declares |
| C-11 Assumptions are not requirements | pass |
| C-12 Deferred wants stay deferred | pass |
| C-13 References resolve | G-3, G-4; every other file, rule, entry, and identifier resolves |
| C-14 Examples and scenarios agree with their clauses | pass: the helper agrees with all six expectations |

## Gaps

| Gap | Location | Check | Quoted | Proposed resolution | Ruling | Amendment |
|---|---|---|---|---|---|---|
| G-1 | ConOps §2, read with REQ-0 | C-9, C-4 | "what the realization does with such an input is not specified in this version" | say what REQ-0 says: the guard does not accept it; how a realization signals that is not specified | **accepted** | §2 |
| G-2 | US-2 header | C-8 | "Source: E-3, E-1" | keep `Source: E-3`; cite E-1 inside the reason clause of the story | **accepted**: this corrects audit 03's ruling on its G-4, which the 1.1 checklist's C-8 does not admit; the story is in the sender's words and cites the officer's answer where it relies on it | US-2 |
| G-3 | ConOps §6 | C-13 | "is recorded in `reports/walkthrough.md` under \"Sign-off\"" | "is to be recorded": the only sign-off there names version A0 | **accepted** for this commit; the sentence says "is recorded" again once the A1 sign-off exists | §6 |
| G-4 | `scenarios.json`, `assumes` | C-13 | "(A1)" | "(glossary: filter)", so the citation cannot be read as assumption A-1 | **accepted** | `scenarios.json` |

Considered and not reported (the skill's words, condensed): value equality
versus object identity (C-4); "large" in a want (C-4); the statelessness
sentence has no clause of its own but follows from REQ-1 to REQ-3 (C-7);
"clamping" in SC-4's note names what this version does not do (C-3); the
`Validated by` field is governed by no rule at this commit; "the Terms
section of the A0 concept of operations" names a version, not a file.

Observations outside the gap list: checklist item C-8 names `tools/trace.py`,
which the next commit adds; the plugin's legend and the clause reader's
docstring name `reports/validation.md` and `tooling/`, which later commits
add. Noted; not specifications.

Searched: within each document ✔ · between documents ✔ · by execution ✔.

## What this audit shows

A pass report: fourteen items, ten of them *pass* with the evidence stated,
and four wording gaps that a reader fixes in a minute. This is what the
procedure costs once the family is clean, and why rule SQ-2 can afford to
run before every commit that touches a specification. The skill's checklist
also caught its own earlier ruling (G-2), which is the value of writing the
check down: a rule applied by a checklist is applied the same way to the
author's decisions as to anyone else's.

**Rulings:** given above, on the instructor's behalf.
