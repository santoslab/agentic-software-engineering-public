# Lecture 02 — The Concept of Operations, Operations with Contracts, and the Specification as an Invariant

> Software-engineering module, meeting 2 of 6. Companion reading for the lecture
> and for part 2 of the note-set demo
> (`../demos/lecture-01-note-specs-demo/demo-script-lecture-02.md`);
> self-contained. Project 0 continues; Exercise 1 is due before Lecture 03.

## Where we are: what Lecture 01 left in the repository

At the end of the first lecture the repository holds the format specification
at version 1.0.0, one conformant note with its index entry, a program
(`check_notes.py`) that verifies notes against 1.0.0, and three process
documents: how a specification is audited (AUD), how findings are reported
(RPT), and how verification is done (VER).

Two things are missing, and their absence is the subject of this lecture.
Nothing says what the note set is *for* — who uses it, and what they do with
it. And nothing says what an agent may do to the set: there is no notion of an
operation, only a specification of what a note looks like once it exists.

The repository at the start of part 2 adds four files:

- `note-set-conops.md`, a draft concept of operations (the document that says
  what the note set is for);
- `process/README.md`, which states an invariant and maps the process files;
- `development-rules.md` (DEV), the rules for how an operation begins and
  ends and who may change what;
- `conops-audit.md` (AUDCON), audit rules that apply only to a concept of
  operations;

together with `BACKLOG.md`, a file for questions that are deferred rather than
guessed.

## The concept of operations: a specification of purpose

A **concept of operations** (ConOps) is a specification of purpose. It says
what the system is for, who uses it, which operations they perform, and what
they can observe. It does not say how the system is built. In this lecture we
introduce it on the note set; from Lecture 03 on, every example starts from
one.

The note set's ConOps is short. Its sections: purpose and scope (one user; an
agent performs the structural operations; the user writes the content); the
set (markdown files in `notes/`, an index file, the format specification that
governs them); roles (one user, one agent); three scenarios in the user's
words and the agent's operations; conformance; change management. Version
0.1, draft.

The operations are the center of the document, and each is written as a
contract (a precondition and a postcondition):

- **O1 — Add blank note.** Input: a title. Precondition: no note with that title
  exists. Postcondition: a new note exists with well-formed front-matter and the
  title as its heading, and `index.md` lists it.
- **O2 — Add note with initial content.** Inputs: a title and initial text.
  Precondition: as O1. Postcondition: a note exists whose content is the supplied
  text brought into conformance with the format specification, preserving the
  user's meaning; `index.md` lists it.
- **O3 — Remove note.** Input: a title. Precondition: a note with that title
  exists. Postcondition: the file no longer exists, and `index.md` no longer
  lists it.

A precondition says what must hold before the operation may start; a
postcondition says what holds when it is done. Note that both are stated from
the user's side: a user can tell whether O3 may start (is there such a note?)
and whether it finished (is the file gone, and the index entry with it?). This
is Meyer's *design by contract*, applied to an operation performed by an agent
rather than to a method in a program. The contract is an abstraction of the
agent's behavior: it says what the operation requires and guarantees, not how
the agent carries it out.

**Important**: this is a general pattern we will see again with the game. A
system has states; in a given state some operations are available (their
preconditions hold); performing an operation moves the system to a new state
that satisfies the postcondition. Writing operations this way lets a person
check, from the outside, whether the system did what it promised.

**User stories and scenarios.** Agile development states intent in *user
stories* — "as a <role>, I want <capability>, so that <benefit>" — each with
acceptance criteria that say when the story is done. A user story and a ConOps
scenario come from the same place: the user's point of view, in the user's
words, with nothing about how the system is built. They serve the same first
purpose, to state what the system is for in a form a non-programmer can
confirm. Each of the note set's operations could be written as a story: as the
user, I want to add a note from text I paste, so that my reading is captured
without my formatting it.

The differences are in what happens next. A story is a unit of planning: it
sits in a backlog, is estimated, and is closed when its acceptance criteria
pass. A scenario — or, in the light skeleton, an operation — is part of a
governing document: it is audited (our audit rule AUDCON-3 requires every
mode, policy, and user class to appear in one), versioned, and cited by the
documents derived from it. Acceptance criteria correspond to the precondition
and postcondition, what must hold before and what holds after; but a story's
criteria are written for one feature and checked when the feature is
delivered, while a contract is verified again after every operation (our
development rule DEV-7). And a scenario narrates a session that exercises
several operations and policies together, which is what the audit's
walkthrough (AUD-4) needs; a story names one capability. A story is a good way
to begin. The audit is what turns it into a contract.

Two other sections of the ConOps matter later. Conformance (§5) says that
every note is expected to conform to the format specification *at all
times* — conformance is an invariant of the set, not a milestone — and that a
report cites the rule identifiers. Change management (§6) says every operation
ends in a git commit and that the specifications themselves change by
versioned, reviewed edits.

**Two skeletons.** The note set's ConOps uses a light skeleton: purpose, the
system, roles, operations, conformance, change management. The full skeleton,
used from Lecture 03 on, has nine numbered sections; three of them — Current
Situation, Justification for and Nature of the Changes, Summary of Impacts —
apply only when an existing system is being improved, and are omitted for a
new system. The template resource in the student materials gives the full
skeleton with those sections marked.

**Validation and verification.** The format specification answers questions a
verifier can decide: does this note satisfy R3? The ConOps answers a different
question: is this the system that was wanted? A non-programmer could read the
note set's ConOps and say yes or no. That question is *validation*, and a
person decides it, usually by reading scenarios or walking through operations.
The ConOps is the one specification in the repository that is checked by
reading rather than by a program. Keep this distinction in mind: verification
asks whether a realization satisfies its specification; validation asks
whether the specification describes the system that was wanted.

## Auditing a concept of operations

A ConOps is audited like any specification (our audit rules AUD-1 through
AUD-7), and by six further rules in `process/conops-audit.md` that apply only
to this kind of document:

- **AUDCON-1 — Implementation-independent.** The ConOps names nothing that
  exists only inside the realization: no language, module, class, method, data
  structure, or internal file. What the user sees, types, opens, or is told
  belongs — a markdown file in `notes/` is something the user opens; how a
  program parses its front-matter is not.
- **AUDCON-2 — Observable.** Every policy the ConOps states is something a user
  could observe or an operation could show. "Conformance is an invariant of the
  set" is observable: a check requested at any moment passes. "The agent reads
  the specifications before every operation" is not a policy of the system but a
  rule of the process, and belongs in `development-rules.md`.
- **AUDCON-3 — Operations and scenarios cover.** Every operation states its
  input, precondition, and postcondition; every mode, policy, and user class
  appears in at least one operation or scenario.
- **AUDCON-4 — Terms.** Every recurring term is defined, in a glossary or where
  it first appears, and used with one meaning throughout — consistently with the
  other specifications.
- **AUDCON-5 — Voice and self-containment.** Third person, present tense;
  understandable without any other document; never cites code; should not
  depend on clauses of lower-level specifications, though naming a lower-level
  document as the place where a detail is fixed is acceptable.
- **AUDCON-6 — Versioned,** with a changelog.

The demo's second segment runs both audits on the draft ConOps, checking it
against the format specification as well. The developer types:

> Read `note-set-conops.md`, `note-format-spec.md`, and the process documents.
> Run the audits in `process/conops-audit.md` and `process/spec-audit.md` on the
> concept of operations. Check it against the format specification (AUD-3) and
> walk through each of O1, O2, and O3 (AUD-4). Report one gap list per RPT-1 and
> wait for my rulings.

Here are five findings the list should contain, and the rulings we make:

1. The ConOps says the formatting of "markdown files in the note set" is
   governed by the format specification. Specification 1.0.0 says `index.md` is
   not a note. The two documents disagree — AUD-3, an inconsistency *between*
   documents. The format specification moved in Lecture 01; the ConOps had not
   followed. **Ruling:** amend the ConOps: the index is not a note, and only R6
   applies to it.
2. O1 supplies a title, and nothing in the ConOps says what file is created.
   Since Lecture 01, R7 settles it. **Ruling:** amend the ConOps to say that a
   note's filename is derived from its title as R7 specifies.
3. O2's postcondition contains "preserving the user's meaning" — a clause no
   program can decide, and the ConOps does not say who does. **Ruling:** no
   amendment. It is a judgment clause; the VER-2 table names a human or agent
   verifier for it.
4. The ConOps says a conformance report cites the rule identifiers of the format
   specification — a dependence on a lower-level document (AUDCON-5, a SHOULD).
   **Ruling:** no change; the sentence describes what the user sees.
5. "Every operation ends in a git commit" reads like a process rule. **Ruling:**
   no change; the user observes the commit, so it is a policy of the system, and
   the rule that enforces it is DEV-7.

Note that rulings 3, 4, and 5 change nothing, and the gap list records them as
*ruled: no change*, with the reason. A finding is not always a change; a
recorded decision not to change is still a decision, and a month later it
answers the question "did anyone notice this?"

The agent then proposes the two amendments in the form our reporting rule
RPT-3 prescribes; the developer approves; the ConOps goes to 1.0 with a
changelog entry that says the clarifications surfaced during the audit; the
agent commits.

## Deriving lower-level specifications from the concept of operations

The ConOps promises operations; the format specification says what a
conformant note is. Neither says how the agent carries an operation out — which
file it creates, in what order it checks, what it commits. That is a third
document, `note-set-operations.md`, and it is *derived* from the other two.

**From a scenario to an operation.** The concept of operations gives each
operation twice: first as a scenario, in the user's words, then as a contract.
The operations document gives it a third time. Reading the three versions of
one operation side by side shows what each level adds and what it settles. We
take O2 first, in full; then O1 and O3.

*Scenario S2, from the concept of operations, §4:*

> "I have just read Brooks's *No Silver Bullet* and typed a page of notes with
> a few headings. I paste them and ask the agent to add a note. Later I open
> the index and see the note listed."

The scenario fixes an actor, an intent, and the two things the user will
notice afterwards: the note exists, and the index lists it. It leaves open
what the agent does with the headings, whether a second note with the same
title is allowed, what "listed" looks like, and whether the user's wording
survives.

*Operation O2, from the concept of operations, §4:*

> - **Inputs:** a title and initial markdown text.
> - **Precondition:** no note with that title exists in the set.
> - **Postcondition:** a note exists whose content is the supplied text brought
>   into conformance with `note-format-spec.md`, preserving the user's meaning;
>   `index.md` lists it.

"Paste them" has become an input with a type — markdown text — and a second
input the scenario only implied, a title. "Add a note" has acquired a
precondition the scenario never mentioned: no note with that title already
exists. "See the note listed" has become a clause of the postcondition. And the
one thing the scenario cared about but could not say — that the notes stay the
user's — has become "preserving the user's meaning." Still open: the filename;
what "brought into conformance" is allowed to change; which of these clauses a
program can check.

*Operation O2, from `note-set-operations.md` (the derived document, quoted as
it stands after specification 2.0.0; "as O1" refers to the O1 text quoted
below):*

> - **Inputs:** a title and initial markdown text.
> - **Precondition:** as O1.
> - **Steps:** create `notes/slug(title).md`; bring the supplied text into
>   conformance while preserving the user's meaning (add front-matter and the
>   title H1; adjust heading levels only as conformance requires); write a
>   `## Summary` paragraph if the supplied text does not contain one
>   (judgment: the summary must reflect the content); add the R6-form index
>   entry; run O4 on the new note; commit.
> - **Postcondition:** as O1, with the user's content and meaning preserved.

The precondition is now something a program can check — a filename computed
by R7, and a search of the index for the title. The steps are an order, and the
scenario's "a few headings" is settled: heading levels change only where R5
requires it. "Listed" is "the R6-form index entry," and the postcondition (via
O1's) says *exactly once* and names the clauses the note must satisfy, so that
the verification report can cite them. The judgment clause is named as such.
Two phrases — the `## Summary` paragraph, and R8 in O1's postcondition — were
not in the 1.0 version; they were added when the specification moved to 2.0.0,
which is the derived document following the governing one (our development
rule DEV-5). And the last two steps, "run O4; commit," are DEV-7 written into
the operation itself.

*Scenario S1 and operation O1:*

> "I want a note for a paper I have not read yet, so that it is in the index
> and I remember to come back to it. I give the agent the title and nothing
> else."

> - **Input:** a title.
> - **Precondition:** no note with that title exists in the set.
> - **Postcondition:** a new note exists containing well-formed front-matter
>   and the title as its heading, with no other content; `index.md` lists it.

> - **Input:** a title.
> - **Precondition:** `notes/slug(title).md` does not exist and no `index.md`
>   entry with that title exists.
> - **Steps:** create `notes/slug(title).md` containing front-matter (`title`,
>   `created` set to today's date in ISO-8601 form), the H1 equal to the
>   title, and a `## Summary` section holding a one-sentence placeholder that
>   names the note's intended topic; add the R6-form index entry; run O4 on
>   the new note; commit.
> - **Postcondition:** the note exists, conforms to R1–R5, R7, and R8, and is
>   listed in `index.md` exactly once.

"The title and nothing else" became the single input. "Well-formed
front-matter" became two named fields with the date in ISO form. "No other
content" was exact at 1.0; at 2.0.0 it conflicts with R8, and the operation
now writes a placeholder — the deferred question in `BACKLOG.md`. "So that it
is in the index" became "listed in `index.md` exactly once."

*Scenario S3 and operation O3:*

> "That note was a mistake. I tell the agent the title and ask it to get rid
> of it; afterwards the index should not mention it."

> - **Input:** a title.
> - **Precondition:** a note with that title exists in the set.
> - **Postcondition:** the note file no longer exists; `index.md` no longer
>   lists it.

> - **Input:** a title.
> - **Precondition:** `notes/slug(title).md` exists.
> - **Steps:** delete the file; remove its `index.md` entry; run O4 in whole-set
>   mode to confirm R6 still holds; commit.
> - **Postcondition:** the file no longer exists and `index.md` no longer
>   lists it.

The scenario's "get rid of it" became two steps and a whole-set check, because
removing a file can break R6 for the index, not only for the note. What the
scenario never says — what happens when there is no such note — is settled by
the precondition: it is false, the operation does not start, and the agent
reports that instead of guessing which note was meant.

So to summarize, the pattern is the same each time. The scenario gives the
actors, the intent, and one path through the system, in prose. The contract in
the concept of operations fixes the inputs and states, from the user's side,
what must hold before and what holds after. The operations document makes the
precondition something a program or a reader can check, orders the steps,
states the postcondition in terms of the clauses it must satisfy so that a
verification report can cite them (AUD-5), says what happens when the
precondition does not hold — which a scenario never mentions — and names the
clauses that remain judgment.

**Important**: each level is a more effective specification than the one
before, not because it says more about how the agent works, but because more
of its sentences can be checked. That is the general direction in which
specifications are refined: from intent in the user's words toward clauses a
verifier can decide.

The demo's third segment has the agent write the operations document: for O1,
O2, O3, and a fourth operation, check conformance (O4), the input, the
precondition, the steps, and the postcondition; the conventions (the filename
slug per R7; every operation ends with O4 and a commit named for it); and an
audit of the new document against both governing documents before it is
committed.

Three specifications now govern the repository, and each abstracts something
different. The ConOps abstracts purpose. The format specification abstracts
every conformant note — it describes all of them and none in particular. The
operations document abstracts the agent's behavior: what each operation
requires and guarantees, not how the agent performs it step by step. A reader
can understand the system from the three documents without reading a single
note. In the course's catalog of specification kinds
(`../../specification-kinds.md`) these are three entries: the *concept of
operations*; a *data format*; and, for the operations document, the *interface
contract* — an operation's precondition and postcondition are the same form
Lecture 03 gives to a program's public operations. The operations document's
*Steps* go beyond a contract, and the catalog's notes on naming say how.

Two rules govern a derived document. Our development rule **DEV-5** says that
a derived document never contradicts the governing documents; when it is wrong
or incomplete, the agent proposes a correction rather than improvising; when
it and a governing document disagree, the governing document wins and the
derived one is corrected. The operations document says this about itself in
its first paragraph. And our audit rule **AUD-5, traceability**, says that a
derived document cites the clauses it derives from — the operations document
names R7 for the slug and R6 for the index entry — so that when a governing
clause changes, the places that depend on it can be found.

Consistency between the three documents is not assumed. The derived document
is audited against the other two (AUD-3) before it is committed, the way the
ConOps was audited against the format specification.

## Performing operations under the development rules, and the invariant

The demo's fourth segment performs three operations: O2, adding "No Silver
Bullet" from pasted text; O1, adding a blank note; O3, removing it. Each is
governed by the development rules in `process/development-rules.md`, which we
introduce in this lecture:

- **DEV-1** — the agent reads the governing documents and the always-on process
  documents before acting, from the files, not from memory.
- **DEV-2** — a realization changes for one of three reasons, and the history
  shows which: a *repair* (it did not conform; a report and a ruling precede
  the change); a *conformance-preserving change* (it conformed before and
  after; what changed is in what the specification leaves open, and the commit
  says so); or a *change of specified behavior*, which follows a committed
  amendment. An operation creates or changes a realization; the check at the
  end of the operation (DEV-7) is what establishes its conformance.
- **DEV-3** — no governing or process document is edited without approval;
  changes are proposed per RPT-3, with a version bump and a changelog entry.
- **DEV-4** — in a verification failure, when a specification and a realization
  disagree, a person decides whether the specification or the realization
  changes, and the decision is recorded: the changelog when the specification
  moves, the commit message when the realization moves.
- **DEV-5** — derived documents follow governing ones.
- **DEV-6** — a question the operation cannot settle is written to
  `BACKLOG.md`, never settled by a silent guess.
- **DEV-7** — every operation ends the same way: the affected realizations are
  verified, a completion note is given (RPT-5: what changed, which checks ran
  and their result, which judgment clauses remain for a human or agent
  verifier, anything deferred, the commit), and a commit is made whose message
  names the operation.

After each of the three operations, the algorithmic verifier runs over the
whole set and passes; R6 — every note linked exactly once, every link
resolving — held throughout, including across the add-then-remove pair. Recall
that the ConOps said conformance is an invariant of the set, not a milestone.
DEV-7 is the rule that makes it one, by ending every operation with a check.

**Important**: this is the general pattern for working with an invariant. An
invariant is a property every reachable state must satisfy. We do not
establish it once; we re-establish it at the end of every operation that could
have disturbed it, and we record that we did. The game in Lecture 03 has the
same pattern: the rules of play are its invariant, and a check after every
move keeps them true.

The completion note for O2 names the judgment clause. The program checked
R1–R7; whether the agent "preserved the user's meaning" when it wrapped the
pasted sections in front-matter and adjusted a heading level is not something
a program decides, and the note says the agent reviewed it and what it changed.

One more thing is visible in `git log`. Each commit names an operation:
`add-note-with-content: No Silver Bullet`, `remove-note: Design by Contract`.
Note that the process documents are specifications too — of how work
proceeds — and the commit log is their realization. Auditing the process means
reading the log. (The catalog's *development process* entry describes this
kind.)

## A specification is continuously maintained: a new requirement

The demo's fifth segment changes a requirement. The developer wants the index
to say what each note *says*, not only that it exists:

> New requirement: every note begins with a `## Summary` section — one
> paragraph, the first section after the title — and each index entry shows the
> first sentence of that summary. This is a specification change. Propose per
> RPT-3: a new rule R8, an amended R6, version 2.0.0 with a changelog entry; the
> matching changes to `note-set-operations.md`, to `check_notes.py` and its
> docstring's version, to the VER-2 table in `process/verification.md`, to the
> two existing notes, and to `index.md`. Show me the amendments first and wait.

After approval, one commit changes the specification, the verifier, the
operations document, a process table, both notes, and the index, and the
program passes at 2.0.0. There are three things to see in it.

**VER-3: when verification runs.** Our verification rule VER-3 says that after
an amendment, everything the amendment touches is re-checked against the new
version, because a pass against the old version is not a result. A verifier
still at 1.0.0 would have reported both notes conformant — the "wrong version
of the specification" failure mode from Lecture 01, now demonstrated. That is
why the prompt bundled the verifier's update with the specification's, and why
the verifier's docstring states which version it implements.

**A judgment clause arrives.** R8 has two halves. That a `## Summary` section
exists, first, with exactly one paragraph, is mechanical, and the program now
decides it. That the summary *accurately* summarizes the note (a SHOULD) is
judgment, and only a person or an agent can decide it. The VER-2 table now
shows R8 in both columns. The agent wrote the two summaries by re-reading each
note; that is the judgment work, and the completion note says so.

**A deferred question.** O1 creates a blank note. To satisfy R8 it now writes a
placeholder summary sentence. Should R8 instead exempt notes that have no
content yet? The developer does not decide this in the lecture. Following our
development rule DEV-6, it is written to `BACKLOG.md` with the current
practice stated, and it stays there until a ruling closes it.

## The invariant, and the files that maintain it

`process/README.md` states what the whole set of process documents exists to
keep true. Conformance is an invariant of the repository, not a milestone. At
every commit:

1. every specification passes its audit — AUD for any specification, AUDCON in
   addition for the concept of operations;
2. every realization conforms to the current version of its specification — VER;
3. every change to either side is recorded with the decision that caused it —
   DEV, RPT.

The specifications say what the system is. The process documents say how work
proceeds with respect to them. Note that both are specifications: versioned,
audited, cited by identifier, changed by the same mechanism (a proposal, an
approval, a version bump, a changelog entry). Rule identifiers are never
renumbered; new rules are appended, so that a citation made today is still
right after the next change.

## Five claims about specifications

Specification-driven development is sometimes described as a one-way process:
write the specification, hand it to an agent, receive the implementation. The
two lectures so far give evidence against that description, one piece per
claim.

1. **A specification is a continuously maintained document of intent.** The
   format specification moved from 0.1 to 1.0.0 during the audit and to 2.0.0
   when a requirement changed; the ConOps moved from 0.1 to 1.0. Each step is a
   ruling with a changelog entry, and `BACKLOG.md` holds what is not yet
   decided.
2. **A specification is an abstraction of the realization.** R1–R8 describe
   every conformant note and none in particular. The operations document
   describes the agent's behavior without being it.
3. **Conformance is an invariant maintained while both sides change.** The
   specification moved with no realization present (Lecture 01, the audit) and
   with realizations present, which were migrated (this lecture, 2.0.0); the
   realization moved with the specification still (Lecture 01, the repair). A
   check ends every operation.
4. **There are typically several specifications, and they must be consistent
   with each other.** Three govern this repository. The first finding of this
   lecture's audit was between two of them, and both now agree.
5. **Information flows in both directions.** The audit produced R7 and the R3
   amendment before any note existed. Writing the verifier fixed the
   front-matter grammar at two scalar fields, so that a short parser could be
   complete. A new requirement changed five artifacts in one commit. None of
   this is a failure of the specification; it is how a specification is
   maintained.

Diagram 4 in the slides contrasts the one-way description with the flows the
demo showed.

## Planning from specifications: the moves, and where they live

Across the two lectures the developer made the same moves several times, and
they generalize to any project that starts from specifications. As a prompt:

1. **Read.** Name the specification files and require that they be read in full.
2. **State the target.** Which artifacts, which operations, documented where.
3. **Audit before planning.** Run the audit (AUD; AUDCON for a ConOps) and
   deliver the gap list (RPT-1); stop for rulings.
4. **Amend with approval.** Propose amendments (RPT-3); wait; then apply them
   with a version bump and a changelog entry (DEV-3).
5. **Plan.** Once the specifications are audited, ask for a plan; review and
   approve it.
6. **Realize with a verification gate.** After each change, verify the affected
   artifacts (VER), report (RPT-2), and end the operation the standard way
   (DEV-7).

These demands could be written into every prompt. Instead, most of them are
rules in `process/`, loaded every session or invoked by name, and the prompt
says which specifications, which target, and "run the audit." The demand is
not weaker for being in a file; it is versioned and cited like everything else,
and it applies whether or not the prompt repeats it. The handout
`../student-materials/spec-driven-planning-prompt-template.md` gives the full
form and a filled example.

## Exercise 2

Exercise 2 asks you to run part 2 of the demo in your own session: audit the
concept of operations and compare your findings with the five in the script;
derive the operations document; then add, change, and remove notes of your own,
with every operation ending as DEV-7 requires — the gate, a completion note, a
commit named for the operation. One step breaks the invariant by hand (a note
renamed outside the process) so that you can watch the gate catch it, rule, and
repair. One step defers a question to `BACKLOG.md` instead of deciding it. The
deliverable is your repository's history and a short account of which rule each
commit obeyed. The full specification is
`../exercises/exercise-02-operations-under-contract.md`; it is due before
Lecture 04.

## Project 0 - The Personal Knowledge Base

Project 0 follows the same structure that we have introduced in the last two lectures, 
but at a larger scale (in fact, you get to determine the scale as you evolve it 
during the semester).  Your PKB has a concept of
operations (who uses it, what operations you perform on it), a format
specification (what a conformant entry is), an operations document derived from
both, and — as the stretch goal — a verifier. The Open Knowledge Format keeps
conformance deliberately light; deciding how much to tighten it, and which
clauses a program decides, is the decision this lecture made about R8.

## Questions to think about

1. Findings 3, 4, and 5 of the audit changed nothing. Was the audit wasted on
   them? What does a recorded "no change, because …" give you later?
2. O2's postcondition says "preserving the user's meaning." Which kind of
   verifier can decide it, and what must the completion note say about it?
3. A verifier still at 1.0.0, run on the 2.0.0 notes, reports them conformant.
   Which of Lecture 01's six failure modes is that, and which line of an RPT-2
   report exposes it?

## Before next meeting

- Read the Lecture 03 handout: the game's `CONOPS-sketch.md` and the process
  documents as shipped in that demo's starter. Lecture 03 applies this method to
  a program, starting from a sketch rather than a draft.
- Exercise 1 is due before Lecture 03; Exercise 2, assigned today, before
  Lecture 04. Project 0 continues.
