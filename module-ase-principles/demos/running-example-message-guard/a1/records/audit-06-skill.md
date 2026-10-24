# Audit 06: the audit skill at version 1.2, rerun on its known-violation set

**Why this record exists.** The catalog page of `/audit-spec` says that any
change to the skill is rerun on `reference/drafts/`, the pre-audit
specifications with the seven seeded gaps, and must still find the seven
and report nothing for the one non-gap. Version 1.2 (2026-10-24) moved the
checklist into one file per form and made the form the skill's argument,
with the items unchanged. This is that rerun. It is a check of the skill,
not an audit of the live specifications: the gaps below are the drafts'
known violations, ruled on in audit 03, and no ruling is given here.

**Setup.** A scratch copy of this snapshot with `reference/drafts/conops.md`,
`glossary.md`, and `requirements.md` overlaid onto `specs/` and
`specs/scenarios.json` removed (the drafts predate the scenario file),
committed in the scratch repository as `ce2e589`; a fresh agent session
started with `/audit-spec` and no other instruction, allowed to read and
not to write. The record below is the skill's output, verbatim, from its
title to its gap table; the two observations it made outside the gap list
are kept because both are artifacts of this setup.

---

# Audit 06: the specifications at commit ce2e589 (version A1)

| Field | |
|---|---|
| Audit | 06 |
| Date | 2026-10-24 |
| Auditor | `/audit-spec` 1.2, run by an agent (Claude Opus 5.5, `claude-opus-5-5`) |
| Audited | commit ce2e589, working tree clean: `specs/conops.md`, `specs/glossary.md`, `specs/requirements.md`. Each is byte-identical to its copy under `reference/drafts/`. **`specs/scenarios.json` does not exist**, so `scen` is not in scope |
| Checks applied | C-1 to C-14 of `checklist.md` 1.2. Reqs-SQ-1's "Each states one requirement" was applied under C-4 |
| Read first | the three specs, `judgments.md`, `procedures.md`, `elicitation.md`, the skill's files and the gap-list template. Then `records/validation.md`, `reference/drafts/README.md` and audits 04 and 05 (for numbering and form). **Audits 01–03 were not read**, because they hold this set's answer key. `tools/walk.py` was not run because it needs your permission; C-14 was decided from the clauses |

## Checks

| Check | Result |
|---|---|
| C-1 Well-formed header | G-15; otherwise pass |
| C-2 EARS form | G-10, G-13, G-16 |
| C-3 Glossary discipline | G-7, G-8, G-14. The glossary's own definitions pass: 13 terms, each defined once |
| C-4 Unambiguous | G-2, G-7, G-11, G-14. Not reported, as the item says: value equality in REQ-3, and "large" in D-2 |
| C-5 Judgment clauses state why | conops: G-4. reqs: pass, no clause in scope |
| C-6 Implementation-independent | G-1 |
| C-7 Complete for scope | conops: pass. reqs: G-12, G-17 |
| C-8 Derivation both ways | G-5, G-17, G-18. The scenario part is not in scope |
| C-9 No contradiction | G-6, G-12, G-18 |
| C-10 One term, one sense | G-8 |
| C-11 Assumptions are not requirements | G-2, G-18 |
| C-12 Deferred wants stay deferred | G-12 |
| C-13 References resolve | G-3, G-9 |
| C-14 Examples agree with clauses | G-6. The scenario part is not in scope |

## Gaps

| Gap | Location | Check | Quoted | Proposed resolution | Ruling |
|---|---|---|---|---|---|
| G-1 | ConOps §1 | C-6 | "The message guard is a Python function that sits on that boundary" | "The message guard sits on that boundary and decides, one message at a time, whether a message may leave." | open |
| G-2 | ConOps §2.1, A-3 | C-11, C-4 | "The guard handles one message at a time and keeps nothing between messages." | Move it to §2 as a statement about the guard, because it describes the guard and is not something the deploying organization must do. §2.1 keeps A-1 and A-2 | open |
| G-3 | ConOps §4 preamble | C-13 | "(ConOps-VAL-2 and ConOps-VAL-1)" | "(ConOps-VAL-1)". There is no ConOps-VAL-2 | open |
| G-4 | US-1, US-2, US-3 headers | C-5 | "Method: walkthrough (human) · …" with no `Reason` | Add a `Reason` to each. The reason is yours to state | open |
| G-5 | US-2 header | C-8 | "Source: E-1" | "Source: E-3". E-1 is the security officer's answer, but US-2 is the message sender's story | open |
| G-6 | US-2 example | C-14, C-9 | "the guard is given (Restricted, 7); it outputs (Public, 7)." | "…it outputs (Restricted, 7)." This is a gap about the pair; you may rule that the story changes instead | open |
| G-7 | US-3 | C-3, C-4 | "every sensitive message stopped at the guard" | "every message whose security level is Critical stopped at the guard". One reading of "sensitive" includes Restricted, which contradicts US-2 | open |
| G-8 | US-3; §3 | C-3, C-10 | "stopped at the guard"; "has no record of what was stopped" | Declare "stopped" as the stakeholders' word inside the glossary's *drop* entry | open |
| G-9 | ConOps §6 | C-13 | "Validation of this document … is recorded in `records/validation.md` under "Sign-off"." | "…is to be recorded…". The recorded sign-off is for "the text of commit a1-specs", and this draft was never committed | open |
| G-10 | Reqs preamble | C-2 | "Each requirement carries an identifier, a verification method, the EARS pattern it uses…" | Add the subject and trigger convention that Reqs-SQ-2 says the preamble states | open |
| G-11 | REQ-0 | C-4 (Reqs-SQ-1) | "The guard shall not change a message after it is created." | Move it to its own requirement (REQ-6, ubiquitous, derived from Glossary: message) | open |
| G-12 | REQ-1 | C-12, C-9, C-7 | "shall drop the message and shall record the drop." | "shall drop the message." The record is deferred want D-1, the glossary's *drop* says "no record is kept", and §2 puts records outside the boundary | open |
| G-13 | REQ-2 | C-2 | "Restricted messages are allowed through." | "When the filter is given a message whose security level is Restricted, the filter shall pass the message unchanged." | open |
| G-14 | REQ-2 | C-3, C-4 | "allowed through" | Use the glossary's *pass*, as G-13's text does. "Allowed through" doesn't say the message leaves unchanged | open |
| G-15 | REQ-4 header | C-1 | "**REQ-4** · Derived from: US-3" | If REQ-4 stays, add "Method: test" | open |
| G-16 | REQ-4 header | C-2 | (same) | If REQ-4 stays, declare a `Pattern` and match the sentence to it | open |
| G-17 | REQ-4 | C-7, C-8 | "The filter shall produce no output when it receives no message." | Delete it. §2 gives the input as one message, and US-3 says nothing about receiving no message | open |
| G-18 | REQ-5 | C-11, C-8, C-9 | "Derived from: ConOps §2.1"; "The guard shall receive every message that leaves the enclave." | Delete it. This is assumption A-2 restated as a requirement, and A-2 itself says "the guard cannot prevent a bypass" | open |

**Two things outside the gap list.** Neither is in a specification:
1. `specs/scenarios.json` is missing, yet `CLAUDE.md` and the *In this project* fields of `judgments.md` still name it and describe the a1 text: US-3 "Method: test · Scenarios: SC-5, SC-6", "REQ-0 to REQ-3", and "SC-1 to SC-6".
2. ConOps-CONF-1 was retired because no clause used the *walkthrough* method, but US-1 to US-3 now use it. So no judgment clause checks the stories' behavior, which matters for your ruling on G-4.

Searched: within each document ✔ · between documents ✔ · by execution ✔ (decided from the clauses; helper not run).


## Key to the seeded gaps, and what the run shows

| Seeded gap (A1 plan) | Found as | Audit 03 found it as |
|---|---|---|
| G1 "sensitive" in US-3 | G-7 | G-6 |
| G2 REQ-1 records the drop | G-12 | G-8 |
| G3 REQ-2 not in EARS form | G-13 (and G-14, the wording) | G-9 |
| G4 US-2's example outputs (Public, 7) | G-6 | G-5 |
| G5 REQ-5 promotes assumption A-2 | G-18 | G-12 |
| G6 REQ-4: no method; no input event | G-15, G-16 (header), G-17 (content) | G-10, G-11 |
| G7 "a Python function" in the purpose | G-1 | G-1 |

- **Seven of seven seeded gaps found.** The non-gap, value equality versus
  object identity in REQ-2 and REQ-3, was not reported and is listed under
  C-4 as not reported, per the item.
- **The unseeded findings of audit 03 are found again** (G-2 the assumption
  that describes the guard, G-3 the forward reference to a second VAL
  clause, G-4 the missing `Reason`, G-5 US-2's `Source`, G-9 the sign-off
  sentence), and three more are reported that audit 03 did not: G-8
  ("stopped" against the glossary's *drop*, which audit 02 had found as
  its item 11), G-10 (the requirements preamble does not state the subject
  and trigger convention, an item that exists only because Reqs-SQ-2's *In
  this project* field now says the preamble states it), and G-11 (REQ-0's
  two sentences, audit 02's item 15). Eighteen gaps against audit 03's
  twelve: the per-form files split REQ-4 into three gaps where 1.0 reported
  two, and the items are now read against a judgments file that says more.
- **The skill kept to its procedure.** It refused to read audits 01 to 03,
  naming them as this set's answer key; it reported the between-document
  items with the scenario parts as not in scope; it did not run the helper
  without permission and said so; it wrote nothing.
- **The two observations outside the gap list** are consequences of the
  setup, not findings about the snapshot: the scenario file was removed on
  purpose, and the stories carry *walkthrough* because the drafts predate
  Scen-CONF-1. Both are the kind of thing a reader of the record should be
  told, which is why the skill reports them.

**Rulings:** none; this is a rerun on the known-violation set, whose gaps
were ruled in audit 03. The skill at 1.2 is trusted on the same grounds as
1.1 was, plus this run.
