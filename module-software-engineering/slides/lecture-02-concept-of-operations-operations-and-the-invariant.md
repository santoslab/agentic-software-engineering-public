---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
  }
  section.lead {
    background: #310066;
    color: #ffffff;
  }
  section.lead h1, section.lead h2 {
    color: #ffffff;
  }
  section.standout {
    background: #beaefc;
    color: #310066;
    text-align: center;
    font-size: 36px;
  }
  h1, h2 {
    color: #310066;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->

# The Concept of Operations, Operations with Contracts, and the Specification as an Invariant

**Agentic Software Engineering — Software-Engineering Module, Lecture 02**
Meeting 2 of 6 · runs part 2 of the note-set demo · Project 0 continues

---

## Where we are: what Lecture 01 left in the repository

- `note-format-spec.md` at 1.0.0, audited and amended
- one conformant note, its index entry, a verifier for 1.0.0
- three process documents: AUD, RPT, VER

Missing: what the set is *for* — who uses it, what they do with it — and what an agent may do to it. There is no operation, only a specification of what a note looks like once it exists.

Added today: a draft **concept of operations**; `process/README.md`; `development-rules.md` (DEV); `conops-audit.md` (AUDCON); `BACKLOG.md`.

<!-- 0–6 min. ls starter-l02/. -->

---

## The concept of operations: a specification of purpose

<style scoped>table { font-size: 20px; } p { font-size: 24px; }</style>

A specification of **purpose**: what the system is for, who uses it, which operations they perform, what they can observe. Not how it is built.

| Section | Says |
|---|---|
| Purpose and scope | one user; the agent performs the structural operations; the user writes content |
| The set | markdown files in `notes/`; an index; the format specification that governs them |
| Roles | one user, one agent |
| Scenarios | S1 a placeholder · S2 notes from reading · S3 a mistake — in the user's words |
| Operations | O1 add blank note · O2 add note with content · O3 remove note |
| Conformance | every note conforms *at all times* — an invariant, not a milestone |
| Change management | every operation ends in a commit; specifications change by versioned, reviewed edits |

Version 0.1, draft.

<!-- 6–16 min. Demo Segment 1: cat note-set-conops.md; cat process/README.md; ls process/. -->

---

## Operations as contracts

| | Input | Precondition | Postcondition |
|---|---|---|---|
| O1 add blank note | a title | no note with that title exists | a note exists with well-formed front-matter and the title as its heading; `index.md` lists it |
| O2 add note with content | a title, initial text | as O1 | a note exists whose content is the text brought into conformance, *preserving the user's meaning*; `index.md` lists it |
| O3 remove note | a title | a note with that title exists | the file is gone; `index.md` no longer lists it |

Meyer's design by contract, applied to an operation performed by an agent. From the user's side: can it start? did it finish? The contract abstracts the agent's behavior — what it requires and guarantees, not how.

---

## Two skeletons; validation and verification

- The note set uses the **light** skeleton: purpose, the system, roles, operations, conformance, change management.
- From Lecture 03: the **full** skeleton, nine sections — three of them (Current Situation; Justification for and Nature of the Changes; Summary of Impacts) only when an existing system is being improved.

The format specification answers questions a verifier decides. The ConOps answers a different question: **is this the system that was wanted?** A person decides that, by reading — validation. The ConOps is the one document checked by reading rather than by a program.

---

## Auditing a concept of operations

AUD-1 to AUD-7 apply, and six more rules in `process/conops-audit.md`:

| Rule | Requirement |
|---|---|
| AUDCON-1 | implementation-independent: names nothing that exists only inside the realization |
| AUDCON-2 | observable: every policy is something a user could observe |
| AUDCON-3 | every operation has input, precondition, postcondition; every mode, policy, and user class appears somewhere |
| AUDCON-4 | terms defined and used consistently, across documents |
| AUDCON-5 | third person, present tense; self-contained; never cites code |
| AUDCON-6 | versioned, with a changelog |

<!-- The AUDCON-1 test: would a user encounter this noun? "notes are markdown files in notes/" — yes, they open them. "`check_notes.py` parses two scalar fields" — no. -->

---

<!-- _class: standout -->

## Audit the concept of operations

The specification moved in Lecture 01. Did the concept of operations follow?

<!-- 16–28 min. Demo Segment 2. Plan mode. -->

---

## The prompt

> Read `note-set-conops.md`, `note-format-spec.md`, and the process documents. Run the audits in `process/conops-audit.md` and `process/spec-audit.md` on the concept of operations. Check it against the format specification (AUD-3) and walk through each of O1, O2, and O3 (AUD-4). Report one gap list per RPT-1 and wait for my rulings.

<!-- Expected: at least the five findings on the next slide. -->

---

## Five findings, five rulings

<style scoped>table { font-size: 19px; } p { font-size: 23px; }</style>

| Finding | Rule | Ruling |
|---|---|---|
| §2: formatting of "markdown files in the note set" is governed by the spec; 1.0.0 says `index.md` is not a note | AUD-3, between documents | amend: the index is not a note; only R6 applies |
| O1 supplies a title; nothing says what file is created; R7 now settles it | AUD-4, AUDCON-3 | amend: filename per R7 |
| O2: "preserving the user's meaning" — a judgment clause, no stated verifier | AUDCON-3 | no change; VER-2 names a human or agent verifier |
| §5: reports cite the format spec's rule identifiers | AUDCON-5 (SHOULD) | no change: it describes what the user sees |
| §6: "every operation ends in a git commit" reads like a process rule | AUDCON-2 | no change: the user observes the commit; DEV-7 enforces it |

Two amendments per RPT-3; ConOps 0.1 → 1.0. Three findings ruled *no change*, with the reason recorded.

<!-- Finding 1: the format spec moved in Lecture 01 and the ConOps had not followed. One intent, two documents, kept consistent by an audit that reads both. -->

---

## Deriving lower-level specifications from the concept of operations

<style scoped>table { font-size: 22px; } p { font-size: 24px; }</style>

`note-set-operations.md`: for O1–O3 and a check-conformance operation O4 — input, precondition, steps, postcondition; conventions (the slug per R7; every operation ends with O4 and a named commit).

Three specifications, three abstractions:

| Document | Abstracts |
|---|---|
| the concept of operations | purpose |
| the format specification | every conformant note, and none in particular |
| the operations document | the agent's behavior — what each operation requires and guarantees |

**DEV-5:** a derived document never contradicts a governing one; corrected, not improvised. **AUD-5:** it cites the clauses it derives from. **AUD-3:** audited against both before it is committed.

<!-- 28–36 min. Demo Segment 3. cat note-set-operations.md. Then the next two slides: one operation at three levels. -->

---

## One operation, three levels: S2 → O2

<style scoped>blockquote, li { font-size: 22px; }</style>

**Scenario S2** (ConOps §4): *"I have just read Brooks's* No Silver Bullet *and typed a page of notes with a few headings. I paste them and ask the agent to add a note. Later I open the index and see the note listed."*

**Operation O2** (ConOps §4):
> **Inputs:** a title and initial markdown text. **Precondition:** no note with that title exists in the set. **Postcondition:** a note exists whose content is the supplied text brought into conformance with `note-format-spec.md`, preserving the user's meaning; `index.md` lists it.

- "paste them" → an input with a type, and a title the scenario only implied
- "add a note" → a precondition the scenario never mentioned
- "see the note listed" → a postcondition clause
- what the scenario could not say → "preserving the user's meaning"

<!-- Still open at this level: the filename; what "brought into conformance" may change; which clauses a program checks. The notes give S1/O1 and S3/O3 the same treatment. -->

---

## One operation, three levels: O2 in the operations document

<style scoped>blockquote, li { font-size: 21px; }</style>

> **Precondition:** as O1 — `notes/slug(title).md` does not exist and no `index.md` entry with that title exists. **Steps:** create `notes/slug(title).md`; bring the supplied text into conformance while preserving the user's meaning (add front-matter and the title H1; adjust heading levels only as conformance requires); write a `## Summary` paragraph if the supplied text does not contain one (judgment: the summary must reflect the content); add the R6-form index entry; run O4 on the new note; commit. **Postcondition:** as O1, with the user's content and meaning preserved — the note conforms to R1–R5, R7, and R8, and is listed in `index.md` exactly once.

- the precondition is now a check: a filename by R7, a search of the index
- the steps are an order; "a few headings" is settled by R5
- the postcondition cites clauses a report can cite; the judgment clause is named
- "run O4; commit" is DEV-7 written into the operation
- the Summary phrases arrived with 2.0.0: the derived document followed the governing one (DEV-5)

Each level is a more effective specification than the one before — not because it says more about how the agent works, but because more of its sentences can be checked.

---

<!-- _class: standout -->

## Operations under the development rules

O2, then O1 and O3 — each governed by the development rules.

<!-- 36–48 min. Demo Segment 4. -->

---

## The development rules

| Rule | Requirement |
|---|---|
| DEV-1 | read the governing and always-on documents before acting — from the files |
| DEV-2 | a realization changes as a *repair*, a *conformance-preserving change*, or a *change of specified behavior*; the history shows which |
| DEV-3 | no governing or process document is edited without approval; version and changelog |
| DEV-4 | in a verification failure, a person decides whether the specification or the realization changes; the decision is recorded |
| DEV-5 | derived documents follow governing ones |
| DEV-6 | a question the operation cannot settle goes to `BACKLOG.md`, never a silent guess |
| DEV-7 | every operation ends the same way: verified; a completion note (RPT-5); a commit named for it |

---

## The invariant, in action

- O2 "No Silver Bullet": pasted text brought into conformance; the gate passes; the completion note names the judgment clause the agent reviewed; `add-note-with-content: No Silver Bullet`
- O1 "Design by Contract", then O3: the file gone, the index entry gone; two commits

`check_notes.py --all` passed after every operation. **R6 held throughout.** The ConOps said conformance is an invariant of the set; DEV-7 is the rule that makes it one.

`git log`: each commit names an operation. The process documents are specifications too; the log is their realization.

---

<!-- _class: standout -->

## A specification is continuously maintained: a new requirement

"I want the index to say what each note *says*, not only that it exists."

<!-- 48–60 min. Demo Segment 5. -->

---

## Specification 2.0.0, in one commit

The prompt asks for amendments per RPT-3 first — R8 (a `## Summary` section, one paragraph, first after the title), an amended R6 (the index entry shows the summary's first sentence), version 2.0.0 — and then the matching changes.

One commit changes: the specification · the verifier and its docstring's version · the operations document · the VER-2 table · both notes (summaries written by re-reading them) · the index.

`check_notes.py --all` passes at 2.0.0.

---

## What the migration shows

- **VER-3.** After an amendment, everything it touches is re-checked against the new version. A verifier still at 1.0.0 would have reported both notes conformant — Lecture 01's first failure mode, demonstrated.
- **A judgment clause arrives.** R8's MUST half (a section exists, one paragraph) is mechanical; its SHOULD half (the summary is *accurate*) is judgment. The VER-2 table shows R8 in both columns.
- **A deferred question.** O1 creates a blank note; to satisfy R8 it writes a placeholder summary. Should R8 exempt notes with no content? Not decided today: recorded in `BACKLOG.md` (DEV-6).

---

## The invariant, and the files that keep it

Conformance is an invariant of the repository, not a milestone. At every commit:

1. every specification passes its audit — AUD; AUDCON for the ConOps
2. every realization conforms to the current version of its specification — VER
3. every change to either side is recorded with the decision that caused it — DEV, RPT

Specifications say what the system is; process documents say how work proceeds with respect to them. Both are versioned, audited, cited by identifier, and changed by the same mechanism. Identifiers are never renumbered.

<!-- 60–68 min. process/README.md. -->

---

## Five claims, five pieces of evidence

<style scoped>table { font-size: 22px; }</style>

| Claim | Evidence from the two lectures |
|---|---|
| a continuously maintained document of intent | 0.1 → 1.0.0 → 2.0.0; the ConOps 0.1 → 1.0; each step a ruling with a changelog entry; a backlog for the undecided |
| an abstraction of the realization | R1–R8 describe every conformant note and none in particular; the operations document describes behavior without being it |
| conformance is an invariant while both sides change | S moved with no R (L01 audit) and with R migrated (2.0.0); R moved with S still (L01 repair); a check after every operation |
| several specifications, mutually consistent | three documents; the first finding today was between two of them |
| information flows both ways | the audit produced R7 and the R3 amendment; the verifier fixed R2's grammar; one requirement changed five artifacts |

---

## Not one-way

![w:900 center](diagrams/information-flow.svg)

---

## Planning from specifications: the moves, and where they live

| Move | In the prompt | Rule |
|---|---|---|
| 1. Read | name the files | DEV-1 |
| 2. State the target | which artifacts, which operations | — |
| 3. Audit before planning | "run the audit" | AUD-1…7; AUDCON; RPT-1 |
| 4. Amend with approval | approve | DEV-3; RPT-3 |
| 5. Plan | approve | (DEV-9, from Lecture 03) |
| 6. Realize with a verification gate | — | VER-3, VER-4; RPT-2, RPT-5; DEV-7 |

The demand did not weaken by moving into a file; it is versioned and cited, and it applies whether or not the prompt repeats it. Handout: `spec-driven-planning-prompt-template.md`.

---

## Exercise 2, and Project 0

**Exercise 2** — run part 2 yourself: audit the concept of operations; derive the operations document; add, change, and remove notes of your own, each operation ending per DEV-7; break the invariant by hand and watch the gate catch it; defer one question to `BACKLOG.md`. Due before Lecture 04.

**Project 0** — the same structure at your scale:

- a concept of operations — who uses your PKB, which operations you perform on it
- a format specification — what a conformant entry is
- an operations document derived from both
- a verifier, as the stretch goal

The Open Knowledge Format keeps conformance light on purpose. How much to tighten it, and which clauses a program decides, is the decision this lecture made about R8.

Assigned today: `project-0-pkb-brief.md`, with its starter and example bundle in `student-materials/`. Kickoff due before Lecture 05.

<!-- 68–72 min. -->

---

## Questions to think about

1. Findings 3, 4, and 5 changed nothing. Was the audit wasted on them? What does a recorded "no change, because …" give you later?
2. O2's postcondition says "preserving the user's meaning." Which kind of verifier can decide it, and what must the completion note say?
3. A verifier at 1.0.0, run on the 2.0.0 notes, reports them conformant. Which failure mode is that, and which RPT-2 line exposes it?

---

## Before next meeting

- Read the Lecture 03 handout: the game's `CONOPS-sketch.md` and the process documents in that demo's starter.
- Exercise 1 is due before Lecture 03; Exercise 2 before Lecture 04. Project 0 is assigned today; its kickoff is due before Lecture 05.

**Next meeting:** a program instead of a note set; a sketch of a concept of operations instead of a draft; several kinds of specification.
