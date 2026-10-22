# Audit 03: the specifications, by the `/audit-spec` skill (version A1)

| Field | |
|---|---|
| Audit | 03 |
| Date | 2026-10-22 |
| Auditor | `/audit-spec` 1.0, run by an agent (Claude, a fresh session). The checklist items are cited as the skill's version 1.0 named them, A-1 to A-14; version 1.1, committed with this audit, renamed them C-1 to C-14 after this audit observed the collision with the assumption identifiers of the concept of operations. |
| Audited | the working tree before commit a1-specs (`reference/drafts/` overlaid onto `specs/`) |
| Checks applied | A-1 to A-14 of `checklist.md` 1.0, plus a check the skill added under rule SQ-1 for references to companion files and rules (now item C-13) |
| Read first | `specs/conops.md`, `specs/glossary.md`, `specs/requirements.md`, `process/rules.md`; `reference/elicitation.md` for what the stakeholders meant; `tools/walk.py` and `guard/` for the by-execution step, and the helper run on the six story examples |

## Checks (the skill's results, verbatim in substance)

| Check | Result |
|---|---|
| A-1 Well-formed header | G-10 (REQ-4 has no `Method`); the other eight headers accepted |
| A-2 EARS form | G-9 (REQ-2: no trigger, no "shall", passive with no subject); G-10 (REQ-4 declares no `Pattern`) |
| A-3 Glossary discipline | G-6 ("sensitive" in US-3) |
| A-4 Unambiguous | G-6, G-9. Not reported, per the item: REQ-2's value equality, and "large" in deferred want D-2 (a want, not a clause) |
| A-5 Judgment clauses state why | G-3: the three stories carry `walkthrough (human)` and no `Reason`; the item's parenthetical ("no clause has such a method at A1") disagreed with the tree |
| A-6 Implementation-independent | G-1 ("a Python function" in the purpose) |
| A-7 Complete for the stated scope | G-11 (REQ-4 specifies an input outside the boundary); each security level has an outcome |
| A-8 Derivation both ways | G-4 (US-2's `Source` is the other category's entry), G-11, G-12; every story has a requirement; REQ-0's glossary terms exist |
| A-9 No contradiction | G-5, G-6, G-8, G-11, G-12 |
| A-10 One term, one sense | G-1, G-5, G-8 |
| A-11 Assumptions are not requirements | G-12; A-1 to A-3 are stated as assumptions |
| A-12 Deferred wants stay deferred | G-8 (REQ-1 promises D-1) |
| A-13 Examples agree with their clauses | G-5; the other five examples agree, and `walk.py` agrees with all five; for the G-5 pair the helper gives `pass: Restricted 7` against the stated `(Public, 7)` |
| A-14 Scenarios agree with their story | pass, no scenario in scope |
| References resolve (added under SQ-1) | G-2 (rule VAL-2 does not exist), G-7 (`reports/validation.md` does not exist) |

## Gaps

| Gap | Location | Check | Quoted | Proposed resolution | Key | Ruling | Amendment |
|---|---|---|---|---|---|---|---|
| G-1 | ConOps §1 | A-6, A-10 | "The message guard is a Python function that sits on that boundary" | delete "is a Python function that" | **G7** | **accepted** | §1 |
| G-2 | ConOps §4 preamble | SQ-1 | "(rules VAL-2 and VAL-1)" | cite VAL-1 alone until VAL-2 exists | not seeded | **accepted**: VAL-2 is added with the validation record, later in this version | §4 preamble |
| G-3 | US-1, US-2, US-3 headers | A-5 | "Method: walkthrough (human) ... Validated by: walkthrough (human)" with no `Reason` | add a `Reason` to each, or correct the checklist's parenthetical | not seeded; a genuine finding against the build's own setup | **accepted, both**: each story gets "Reason: no executable form of the story's example exists yet; the scenario file of the next task supplies one", and the checklist item (C-5 in 1.1) now applies to whatever the tree holds | US-1 to US-3; `checklist.md` |
| G-4 | US-2 header | A-8 | "Source: E-1" on a story in the sender's words | "Source: E-3, E-1" | not seeded; a genuine finding | **accepted** | US-2 |
| G-5 | US-2 example | A-13, A-9, A-10 | "(Restricted, 7); it outputs (Public, 7)" | "(Restricted, 7); it outputs (Restricted, 7)" | **G4** | **accepted** | US-2 example |
| G-6 | US-3 | A-3, A-4, A-9 | "every sensitive message stopped" | "every message whose security level is Critical" | **G1** | **accepted**; "stopped" also became "dropped" (audit 02, item 11) | US-3 |
| G-7 | ConOps preamble, §6; requirements preamble | SQ-1 | "`reports/validation.md`" | cite `reports/walkthrough.md`, the file that exists and that VAL-1 names | not seeded: an inconsistency of this working tree | **accepted** for this commit; the validation record arrives later in this version and the references move with it | preambles, §6 |
| G-8 | REQ-1 | A-12, A-7, A-9, A-10 | "and shall record the drop" | delete the clause | **G2** | **accepted** | REQ-1 |
| G-9 | REQ-2 | A-2, A-4 | "Restricted messages are allowed through." | rewrite in the declared pattern with "unchanged" explicit | **G3** | **ruled otherwise** on wording only: "When the filter is given a message whose security level is Restricted, the filter shall pass the message unchanged.", to match REQ-1 and REQ-3 and the glossary's *pass*; rule SQ-3's example updated | REQ-2; SQ-3 |
| G-10 | REQ-4 header | A-1, A-2 | "**REQ-4** · Derived from: US-3" | complete the header, or delete with G-11 | **G6** (the header) | **accepted** with G-11: deleted | REQ-4 |
| G-11 | REQ-4 | A-7, A-8, A-9 | "The filter shall produce no output when it receives no message." | delete: "receives no message" is not a case inside the boundary | **G6** (the content) | **accepted**; noted for the HAMR mapping (No_Input_No_Output has no counterpart in a one-message library) | REQ-4 |
| G-12 | REQ-5 | A-11, A-8, A-9 | "The guard shall receive every message that leaves the enclave." | delete; assumption A-2 stays an assumption | **G5** | **accepted** | REQ-5 |

Considered and not reported (the skill's words): REQ-2's value equality
leaves object identity open, an implementation choice, not a gap (A-4);
assumptions A-1 to A-3 are stated as assumptions (A-11); §2's description
of the interface is at the glossary's own level (A-6); "large" in D-2 is in
a want, not a clause (A-4); the absence of a scenario file is not required
by anything at this commit.

Observations the skill made outside the gap list, and what was done with
them:

- `tests/conformance.py` as it stood matched only `**ID** · Method:` lines,
  so REQ-4 was silently absent from its clause list although rule SQ-1 says
  the reader reports a malformed header. True of A0's reader, which this
  commit still carries; the extended reader of the next task reports it
  (`tooling/clause-reader.md`, case `missing-method`).
- The assumption identifiers A-1 to A-3 collide with the checklist's item
  identifiers A-1 to A-14. Accepted: skill version 1.1 renames the items
  C-1 to C-14.
- The A-5 parenthetical disagreed with the tree. Accepted: see G-3.

Searched: within each document ✔ · between documents ✔ · by execution ✔.

## What this audit shows, beside its findings

- The skill found all seven seeded gaps (G1 to G7: G-6, G-8, G-9, G-5,
  G-12, G-10 with G-11, G-1), and did not report the one non-gap that the
  checklist names, where the ad-hoc audit did (audit 02, item 10).
- It found four unseeded inconsistencies (G-2, G-3, G-4, G-7). Two of them
  (G-3, G-4) the ad-hoc audit missed; two that the ad-hoc audit found (the
  assumption that described the guard; the deferred want that reopened
  Critical) the skill did not report, because no checklist item asks for
  them. A skill reports what its checklist asks; a free reading reports what
  it happens to notice. The checklist gained one item (C-13) from this
  comparison, not the other two, which are judgments of content rather than
  checks of form.
- It reported every item as pass or as the gaps it produced, so this report
  says what was checked, which audit 02's does not.
- Its first finding against the build's own setup (G-3) and its observation
  about identifier collision are why the skill is at version 1.1 in this
  commit: the known-violation set (`reference/drafts/`) caught the audit
  procedure, not only the specifications.

**Rulings:** given above, on the instructor's behalf, following the A1 plan's
section 6 for the seeded gaps and the build's judgment for the rest.
