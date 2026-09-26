# Lecture 02 — The Concept of Operations, Operations with Contracts, and the Specification as an Invariant

> **Unit:** module-software-engineering · **Module week 1, meeting 2 of 2** · 75 minutes
>
> **Thesis:** A concept of operations is a specification of purpose — who uses
> the system and which operations they perform, each with a precondition and a
> postcondition. Lower-level specifications are derived from it and kept
> consistent with it, and conformance is an invariant re-established after
> every operation and after every amendment, not a milestone reached once.

## Learning objectives

After this lecture, students can:

1. Distinguish a concept of operations from a format specification: what each
   states, what each leaves open, and the question each answers (validation —
   is this the system that was wanted — against verification).
2. Write an operation's precondition and postcondition from the user's side,
   and audit a concept of operations with AUDCON-1 through AUDCON-6.
3. Derive a lower-level document from the governing ones (DEV-5) and say what
   makes it traceable (AUD-5) and consistent with them (AUD-3).
4. State the invariant in `process/README.md` and explain how DEV-7 maintains it
   across an operation and VER-3 across an amendment.
5. Give the five claims about specifications, with one piece of evidence for
   each from the two lectures.

## Before class

Assigned at Lecture 01:

- [required] Royce (1970), *Managing the Development of Large Software Systems*.
- [required] Meyer (1992), *Applying "Design by Contract"*.
- [required] The Lecture 02 handout,
  `../student-materials/handout-lecture-02-conops-and-operations.md`:
  `note-set-conops.md` 0.1 and the three process documents this lecture adds.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–6 | Where we are: what Lecture 01 left in the repository | Specification 1.0.0, one conformant note, its index entry, a verifier for 1.0.0, three process documents. What nothing yet says: what the set is *for*, and what an agent may do to it. `ls starter-l02/`: a concept of operations, three more process documents, `BACKLOG.md`. |
| 6–16 | The concept of operations | Demo, Segment 1. Purpose and scope, the set, roles, operations, conformance, change management. O1–O3, each with an input, a precondition, and a postcondition, from the user's side — Meyer's contract, applied to an operation rather than a method. The light skeleton used here; the full skeleton (nine sections, of which 2, 3, and 6 apply only when an existing system is being improved) as the template for later lectures. The ConOps answers a validation question; the format specification answers verification questions. `conops-audit.md`: AUDCON-1 through AUDCON-6. |
| 16–28 | Demo, Segment 2 — audit the concept of operations | The prompt: the audit is run because the developer asks for it (Lecture 03 makes this a standing rule before any plan). Five findings; rulings — two amendments, three "no change" with the reason recorded. Amendments per RPT-3; ConOps 1.0; `git diff`. Finding 1 is AUD-3, between two documents: the format specification moved in Lecture 01 and the ConOps had not followed. |
| 28–36 | Demo, Segment 3 — derive the operations document | DEV-5: derived from the governing documents, never contradicting them, corrected rather than improvised. Three specifications, three abstractions: purpose; every conformant note; the agent's behavior. Traceability: the derived document cites the clauses it derives from (AUD-5). Consistency audited on the derived document (AUD-3). |
| 36–48 | Demo, Segment 4 — operations under the development rules, and the invariant | O2, then O1 and O3. DEV-7: every operation ends with the gate, a completion note (RPT-5), and a commit named for it. R6 held through every operation. The commit log is the realization of the process documents; reading it is how the process is audited. The judgment clause in O2, reported in the completion note. |
| 48–60 | Demo, Segment 5 — a new requirement | Specification 2.0.0: R8, the amended R6, the migration. VER-3: after an amendment, everything it touches is re-checked against the new version; a verifier at 1.0.0 would report the old notes conformant. R8 split in the VER-2 table: its MUST clause mechanical, its SHOULD clause judgment. The question the change raises, recorded in `BACKLOG.md` (DEV-6). |
| 60–68 | Five claims, and the invariant | The table, one line of evidence per claim from the two lectures. Diagram 4. `process/README.md`: the invariant in three clauses, and which document maintains each. |
| 68–72 | Exercise 2; Project 0; before next meeting | Exercise 2 in three sentences: audit the ConOps, derive the operations document, perform operations on your own notes under DEV-7, break the invariant by hand and repair it. Project 0 assigned: the same structure at the student's scale; the brief (`../project-0-pkb-brief.md`), the starter and example in `student-materials/`, kickoff due before Lecture 05. Exercise 1 reminder. Lecture 03: a program; a sketch of a ConOps; several kinds of specification. |

Blocks sum to 72 minutes; 3 minutes slack.

## Demos

### Demo 1 — The note-set demo, part 2

- **Artifacts:** `../demos/lecture-01-note-specs-demo/demo-script-lecture-02.md`;
  `starter-l02/`; `sample-inputs/no-silver-bullet-content.md` and
  `lehmans-laws-content.md`; `completed/check_notes.py` as the Segment 5
  fallback; `completed/` as the destination.
- **Setup (before class):** the script's checklist: a fresh repository from
  `starter-l02/` with an initial commit (or Lecture 01's repository with the L02
  files added and committed); `python3 check_notes.py --all` exits 0; the 2.0.0
  verifier copied outside the repository; the sample inputs open in a
  plain-text editor; Claude Code started with the always-on process files
  loaded; one rehearsal with captures.
- **Script:** Segment 1 in the 6–16 block; Segment 2 in 16–28; Segment 3 in
  28–36; Segment 4 in 36–48; Segment 5 in 48–60; Segment 6's table in 60–68.
- **Expected outcome:** the class sees a second kind of specification audited by
  its own rules; a document derived from two others; conformance re-established
  after each of three operations; and one requirement change carried through the
  specification, the verifier, the notes, the index, and a process table in one
  commit.
- **Fallback:** captures; Segment 5's summaries and migration diff from the
  rehearsal if the agent's run exceeds two minutes.

## Discussion prompts

1. Findings 3, 4, and 5 of the audit changed nothing. Was the audit wasted on
   them? What does a recorded "no change, because …" give you a month later?
2. O2's postcondition says "preserving the user's meaning." Which kind of
   verifier can decide it, and what must the completion note say about it?
3. A verifier still at 1.0.0, run on the 2.0.0 notes, reports them conformant.
   Which of Lecture 01's six failure modes is that, and which line of an RPT-2
   report exposes it?

## Assigned after class

- Readings (for L03): [required] the Lecture 03 handout — the game's
  `CONOPS-sketch.md` and the L03 process set, as shipped in the demo starter
  (ten minutes); [recommended] the concept-of-operations template (the full
  skeleton, with sections 2, 3, and 6 marked optional).
- Exercise: `../exercises/exercise-02-operations-under-contract.md`, due before
  Lecture 04. Exercise 1 is due before Lecture 03.
- Project: **Project 0 — the personal knowledge base**
  (`../project-0-pkb-brief.md`; starter `../student-materials/pkb-starter/`,
  example `../student-materials/pkb-example/`), kickoff due before Lecture 05.

## Instructor notes

- **Cut if running long:** Segment 3 compresses to `cat note-set-operations.md`
  and the DEV-5 sentence; Segment 5's optional Lehman note is out. Never cut
  Segment 2 or Segment 5.
- **Risks:** the agent's gap list is longer than the table in the script — rule
  on the five listed, defer the rest to `BACKLOG.md`, which is itself DEV-6 in
  use. The migration in Segment 5 can exceed two minutes: show the summaries
  from captures. Students conflate the ConOps with the format specification all
  week: AUDCON-1's test — would a user of the system encounter this noun? — is
  the quickest way to sort a sentence into one document or the other.
- **Variants:** have students write O2's postcondition before it is shown, then
  compare with the ConOps. With a strong room, students rule on findings 3–5
  and the class audits the rulings against AUDCON-2.
