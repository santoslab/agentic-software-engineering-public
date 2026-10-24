# Review Records: Message Guard

One entry per review. A review is a person reading an artifact against a
clause of `process/judgments.md` and recording the finding; the entry says
who read, when, against which state, which clauses, and what they found. An
entry is appended, never edited.

## Entry 1 · 2026-10-20 · the instructor

- Clauses: ConOps-SQ-1, Reqs-SQ-1 (the wording and the coverage of the
  scope), Specs-SQ-1, and the derivation part of Specs-TR-1
- Read: `specs/conops.md` and `specs/requirements.md`, together, at the
  state of the A0 snapshot (`a0`)
- Finding, ConOps-SQ-1: the purpose statement is in the stakeholders' words;
  the scope names what enters, what leaves, and what is outside, and lists
  the domain terms; two user categories, each with what it observes; three
  stories, each with an identifier, a method, a user category, and an
  example, each one sentence its stakeholder can confirm or deny; no
  sentence with two readings. Holds.
- Finding, Reqs-SQ-1: four requirements, each with a unique identifier, a
  method, and a derivation; each states one requirement with one reading;
  the form of a message (REQ-0) and each of the three security levels
  (REQ-1 to REQ-3) have a clause. Holds. (The header parts were also read by
  `tests/conformance.py`, whose table in `reports/conformance.md` lists the
  same four clauses with no finding.)
- Finding, Specs-SQ-1: US-1 is covered by REQ-3, US-2 by REQ-2, US-3 by
  REQ-1; no requirement contradicts a story; *message*, *security level*,
  *payload*, *pass*, and *drop* mean one thing in both documents. Holds.
- Finding, Specs-TR-1 (derivations): REQ-1 derives from US-3, REQ-2 from
  US-2, REQ-3 from US-1, and REQ-0 from the Terms section of the concept of
  operations; every one names a story or section that exists. Holds.
