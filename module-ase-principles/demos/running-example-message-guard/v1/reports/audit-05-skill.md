# Audit 05: the specifications before commit v1, by the `/audit-spec` skill (version A1)

| Field | |
|---|---|
| Audit | 05 |
| Date | 2026-10-22 |
| Auditor | `/audit-spec` 1.1, run by an agent (Claude, a fresh session) |
| Audited | the working tree before commit v1: `specs/conops.md`, `specs/glossary.md`, `specs/requirements.md`, `specs/scenarios.json` |
| Checks applied | C-1 to C-14 of `checklist.md` 1.1 (rules SQ-3 and SQ-4 cited under C-2, C-3, and C-10) |
| Read first | the four specifications and `process/rules.md`; `reference/elicitation.md`; then `reports/audit-04-skill.md` (the rulings applied), `reports/validation.md`, `reports/trace-matrix.md`, `reports/conformance.md`, and `tools/walk.py`, for C-13 and C-14; the helper run on the six scenario inputs |

Rule SQ-2 puts an audit before any commit that changes a specification.
Since audit 04 the specifications changed only in their references: the
concept of operations and the requirements cite `reports/validation.md`
(present, replacing `reports/walkthrough.md`) and rules VAL-2 and VAL-1
(VAL-2 now in `process/rules.md`); §6 says "is recorded" again because the
A1 sign-off now exists. This audit found no gap.

## Checks

| Check | Result |
|---|---|
| C-1 Well-formed header | pass: seven headers, unique identifiers, method *test*, only defined keys; SC-1 to SC-6 unique and complete; the conformance report lists the same seven clauses with no specification finding |
| C-2 EARS form | pass: REQ-0 ubiquitous with the guard as subject; REQ-1 to REQ-3 event-driven with the filter as subject and "shall" |
| C-3 Glossary discipline | pass: thirteen terms, each defined once; no other specification defines one; every domain term used is a glossary term or a stated value of *security level* |
| C-4 Unambiguous | pass; not reported, per the item: value equality in REQ-2 and REQ-3; "large" in D-2 |
| C-5 Judgment clauses state why | pass, no clause in scope; `Validated by` is a field, not the method, and §4 ties it to rules VAL-2 and VAL-1 |
| C-6 Implementation-independent | pass |
| C-7 Complete for the stated scope | pass: each security level has an outcome; a non-message input is covered by REQ-0 with its signaling left open; nothing outside the boundary is specified |
| C-8 Derivation both ways | pass: US-1 to REQ-3, US-2 to REQ-2, US-3 to REQ-1; REQ-0 from the glossary; every scenario derives from a story that lists it; `Source` entries match the stories' categories; the trace matrix reports no finding |
| C-9 No contradiction | pass; §6 "is recorded" agrees with the A1 sign-off now present |
| C-10 One term, one sense | pass; "stopped" appears only as the synonym the glossary declares |
| C-11 Assumptions are not requirements | pass: A-1 and A-2 stated as obligations of the deploying organization; statelessness stated in the scope as a property of the guard |
| C-12 Deferred wants stay deferred | pass: D-1 to D-3 have no requirement, story clause, or scenario promising them |
| C-13 References resolve | pass: every file, rule, entry, and identifier a specification names exists, including `reports/validation.md` with its "Sign-off" naming version A1 for both user categories, and rules VAL-1 and VAL-2 |
| C-14 Examples and scenarios agree with their clauses | pass: the six expectations follow from REQ-1 to REQ-3; the helper printed `pass: Public 42`, `pass: Public -3`, `pass: Restricted 7`, `pass: Restricted 150`, `drop`, `drop` |

## Gaps

| Gap | Location | Check | Quoted | Proposed resolution | Ruling | Amendment |
|---|---|---|---|---|---|---|
| (none) | | | | | | |

No gap was found: fourteen items applied, fourteen *pass*.

Considered and not reported (the skill's words, condensed): "the same
message" in §2 against *unchanged* (object identity left open, C-4); "the
Terms section of the A0 concept of operations" names a version's document,
not a file in this tree; "clamping" in SC-4's note names what this version
does not do.

Observation outside the gap list: the docstring of `tools/walk.py` still
said "recorded in reports/walkthrough.md", the file this commit renames.
Applied before the commit: the docstring now names `reports/validation.md`
(the helper's page records the change; the helper's behavior is unchanged).
Every other mention of the old name is in a historical record or in the
intentional rename notes.

Searched: within each document ✔ · between documents ✔ · by execution ✔.

**Rulings:** none needed; the gap list is empty. The observation was
applied as a one-line edit outside the specifications.
