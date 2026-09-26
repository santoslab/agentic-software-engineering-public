# Project 0 — A Personal Knowledge Base, Specification-First

> **Assigned:** Lecture 02 · **Kickoff due:** before Lecture 05 *(date: instructor
> to fix)* · **Then:** semester-long, about thirty minutes a week ·
> **Checkpoints:** weeks 6, 10, and 15 · **Effort (kickoff):** about 6–8 h
> without the optional verifier, which adds 2–4 h *(unvalidated)*
>
> **Requires:** Claude Code; git; Obsidian (free) or any Markdown viewer; Python
> 3.11 or newer for the optional verifier (step 7).
>
> **Status:** draft; instructor review required before assigning (due date,
> effort estimate).

## 0. What this project is

You will design, build, and then maintain for the rest of the semester a
personal knowledge base (PKB): a set of Markdown notes on agentic software
engineering, organized around your own interests, kept in a git repository, and
maintained by a coding agent that follows written specifications. The notes are
the product. What the project teaches is the method for producing them.

Lectures 01 and 02 introduced that method on a small note set: a specification
and its realizations, conformance between them, verification by three kinds of
verifier, a concept of operations that says what the set is for and which
operations an agent may perform on it, an operations document derived from
both, and a process under which conformance is re-established after every
operation. The note set was designed as a reduced version of this project.
Project 0 is the same structure at your scale: you write the same three
governing documents for your PKB, install the same process documents, and
perform the same kinds of operation. The scale — how many notes, how many
kinds of note, how strict the rules — is yours to set, and to change as the
semester goes on.

Three things differ from the note set, and each is a learning outcome:

- **You are the client.** The note set's concept of operations arrived as a
  draft. Yours does not exist until you write a sketch of it, and the agent's
  first job is to turn that sketch into a concept of operations by asking you
  questions. A concept of operations answers a validation question (Lecture
  02): is this the system that was wanted? Only its user can answer, and here
  the user is you.
- **The format is given, and you restrict it.** Notes follow Google's Open
  Knowledge Format (OKF), a short specification for Markdown files with YAML
  frontmatter. OKF was designed for catalogs of datasets as well as for
  personal notes, and most of its fields serve the former. §3 fixes the
  profile of OKF this course uses. Deciding how much further to tighten it,
  and which of your rules a program can decide, is the decision Lecture 02
  made about rule R8, made for every rule of yours.
- **The realization is knowledge, not code.** There is no compiler and no test
  suite between you and the artifacts. Every concept from the two lectures
  applies unchanged, and the artifacts are small enough that you can read all
  of them.

Why a knowledge base at all. Over the semester you will read papers, watch
talks, and learn things from your own project sessions. Anything you find
yourself explaining to the agent twice belongs in a note the agent can read.
Later units connect tooling to the PKB (§7). By the end of the course it should
be the artifact from this course that you keep using.

Grading is completion-based (§6). There is no correct taxonomy and no correct
set of rules. There is a correct way of arriving at them and recording them,
and that is what the required elements check.

## 1. What you get

| File or folder | What it is |
|---|---|
| `student-materials/pkb-starter/CLAUDE.md` | The loader: the governing documents in authority order, the process files, two bootstrap rules, the commands. Until your concept of operations exists, your sketch stands in for it. |
| `student-materials/pkb-starter/process/`, `…/BACKLOG.md` | The Lecture 02 process set — `development-rules.md` (DEV-1 to DEV-7), `spec-audit.md` (AUD-1 to AUD-7), `conops-audit.md` (AUDCON-1 to AUDCON-6), `verification.md` (VER-1 to VER-4), `reporting.md` (RPT-1 to RPT-5), and the invariant in `process/README.md`. Identical to the note set's except for the *In this repository* block of each document, which names your PKB's documents instead of the note set's. `BACKLOG.md` is where deferred questions go (DEV-6). |
| `student-materials/pkb-starter/.claude/skills/grill-me/SKILL.md` | The elicitation skill that step 2 uses. |
| `student-materials/pkb-starter/.gitignore` | Ignores the `.obsidian/` folder wholesale (Obsidian's per-vault settings and workspace), Python caches, and virtual environments. Amend it if you want to commit your vault settings. |
| `student-materials/pkb-example/` | Three notes in the profile of §3, with an `index.md` and a `log.md`. It shows what a conformant bundle looks like, not what yours should contain. It has no governing documents, on purpose. |
| `demos/lecture-01-note-specs-demo/completed/` | The note set at the end of Lecture 02: the model for your three governing documents and for the verifier. |
| The OKF specification, v0.2 | <https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md>. Read §3 of this brief first; it says which parts apply. |

**Repository layout.** At the end of the kickoff your repository looks like
this. The bundle is the folder `kb/` and nothing above it: OKF requires every
non-reserved Markdown file inside a bundle to carry note frontmatter, so the
governing documents, the process documents, and the report cannot live inside
it.

```
CLAUDE.md                the loader (from the starter)
pkb-conops-sketch.md     step 1, written by you
pkb-conops.md            step 2
pkb-format-spec.md       step 3
pkb-operations.md        step 4
process/                 from the starter
BACKLOG.md               from the starter
kb/                      the OKF bundle: index.md, log.md, your notes
check_pkb.py             step 7, optional
transcripts/             step 2
KICKOFF-REPORT.md        step 8
```

**The worked example.** The model for each step is the note set at the end of
Lecture 02, `demos/lecture-01-note-specs-demo/completed/`, together with the
two demo scripts, each of which ends with a section *Recreating this part
yourself (students)*. Read those files as patterns: the shape of a document,
the form of a rule, the form of a commit message. Do not copy their content.
Your PKB's purpose, vocabulary, and rules are decisions you make and record.

## 2. The kickoff, step by step

**How to read a step.** Each step has the same seven parts. *Do* is the
operation. *Why* names the learning outcome the step serves and the concept
from Lectures 01 and 02 that it applies; read it before the prompt, because the
prompt makes more sense once you know what it is for. *Prompt* is the shape of
what you type; adapt the names, not the structure. *Rules* are the process
rules that govern the step; the agent has them loaded, and you are expected to
know which apply. *Shown in* is where the lectures performed the same move on
the note set — the lecture notes are
`lecture-notes/lecture-01-specifications-realizations-and-conformance.md` and
`lecture-notes/lecture-02-concept-of-operations-operations-and-the-invariant.md`;
the demo scripts are `demos/lecture-01-note-specs-demo/demo-script-lecture-01.md`
and `demo-script-lecture-02.md`. *Model* is the note-set artifact that shows
what the result looks like, under `demos/lecture-01-note-specs-demo/completed/`.
*Ends with* is the commit that closes the step (DEV-7). Rulings are yours,
typed in one or two sentences each; a question you cannot settle is deferred
to `BACKLOG.md`, not guessed (DEV-6).

### Step 0 — Start

**Do.** Copy the starter outside the course repository, initialize a
repository, and make one initial commit:

```sh
cp -R <path-to-module>/student-materials/pkb-starter ~/pkb
cd ~/pkb && git init
git add -A && git commit -m "kickoff start: process and loader"
```

Then read, in full, `CLAUDE.md` and the six documents under `process/`. DEV-1
(read before acting) applies to you as well as to the agent: the rulings you
give in steps 2 to 4 cite these rules, and the report in step 8 maps every
commit to one of them.

**Why.** The process documents are the part of the method that does not change
from one system to the next. Lecture 02 closed on the invariant they maintain:
every specification passes its audit, every realization conforms to the
current version of its specification, and every change to either side is
recorded with the decision that caused it. Installing them before anything
else exists is what makes the rest of the kickoff auditable afterwards. The
history of your repository is the realization of these documents, and reading
it against them is how the process is audited.

**Prompt.** None.

**Rules.** DEV-1; DEV-3 (nothing under `process/` or in `CLAUDE.md` changes
without a proposal and a changelog entry).

**Shown in.** Lecture 01 notes, *What the process documents did today*;
Lecture 02 notes, *The invariant, and the files that maintain it*; the L02
demo script, *Before class — setup checklist*.

**Model.** `completed/process/README.md` for the invariant and the map of the
files; `completed/CLAUDE.md` for what a loader contains.

**Ends with.** `kickoff start: process and loader`.

### Step 1 — Your sketch of the concept of operations

**Do.** Write `pkb-conops-sketch.md` yourself, without the agent, under the
six headings of the light skeleton from Lecture 02: purpose and scope; the
system; roles; scenarios and operations; conformance; change management. Mark
it `Version: 0.1` and `Status: draft`. Under *scenarios*, write at least three
sessions as you would describe them — for example, capturing a concept from a
lecture in your own words; asking for a summary of an article you give the
agent a link to; discovering that two notes overlap and wanting one of them
gone. Under *operations*, name what the agent does in each scenario: a title
and one sentence each. It is a sketch. Incomplete sentences, open questions
written as questions, and a TBD or two are expected. Commit it.

The sketch should say, in your own words:

- what the PKB is for and who reads it — you during the course; you in a
  year; anyone else;
- what topic areas it starts with, and what is out of scope;
- what kinds of note you expect — a concept in your own words; a summary of a
  source you cite; a lesson from a project session — because this becomes the
  `type` vocabulary in step 3;
- what the agent may do to the PKB and what only you do: who writes note
  bodies, who decides that a note is finished;
- what "conformant" should mean, as far as you can say before the format
  specification exists.

**Why.** A concept of operations is a specification of purpose (Lecture 02):
it says what the system is for, who uses it, which operations they perform,
and what they observe. It is validated rather than verified — a person decides
whether it describes the system that was wanted. For the note set that person
was the instructor, and the sketch arrived written. For your PKB the person is
you, and no one else can supply the first draft. Writing it yourself, before
any agent is involved, is also what makes step 2 an elicitation: the agent has
something of yours to question. Sorting a sentence into this document or into
the format specification is a skill in itself. The test in AUDCON-1 — would a
user of the system encounter this noun? — is the quickest way to decide.

**Prompt.** None.

**Rules.** AUDCON-1 (implementation-independent); AUDCON-5 (third person,
present tense).

**Shown in.** Lecture 02 notes, *The concept of operations: a specification of
purpose*; the L02 demo script, Segment 1.

**Model.** `completed/note-set-conops.md` — its six sections and its three
scenarios S1 to S3; `demos/lecture-01-note-specs-demo/starter-l02/note-set-conops.md`
for what version 0.1 of one looks like.

**Ends with.** `conops: 0.1 sketch`.

### Step 2 — Elicitation: the sketch to `pkb-conops.md` 1.0

**Do.** In plan mode: the audit of the sketch, before anything is proposed;
the gap list per RPT-1; an interview about every decision the sketch leaves
open, using the grill-me skill; your rulings, one or two sentences each; at
least one deferral to `BACKLOG.md`; the amendments proposed and approved; the
rewrite as `pkb-conops.md` 1.0; the audit run again on the result; the commit.
Then export the session.

What the audit and the interview must settle: every kept section filled and no
TBD surviving; the document in the third person and the present tense, naming
no tool or implementation as a decision (AUDCON-1, AUDCON-5 — "notes are
Markdown files with frontmatter" is a fact about the system a user observes;
"the agent parses frontmatter with a YAML library" is not); every scenario
covered by an operation and every operation by a scenario (AUDCON-3); each
operation with an input, a precondition, and a postcondition stated from the
user's side, which is Lecture 02's contract form; the terms you will keep
using defined once (AUDCON-4); a version, a status, and a changelog
(AUDCON-6). At minimum the operations include adding a note with content you
supply, adding a note that summarizes a source you name, removing a note, and
checking conformance; an update operation if any scenario needs one.

**Why.** This step is the course's first full elicitation, and its evidence
is the transcript. The agent can only be as right as your requirements. An
interview converts the questions you did not know were open into rulings
recorded in a document, before they become rework in the notes. Two lecture
concepts are exercised at once: the audit of a concept of operations by its
own rules (AUDCON-1 to AUDCON-6, Lecture 02), and the rule that a gap is
reported and ruled on before anything is changed (RPT-4). Watch for the
confusion the Lecture 02 instructor notes warn about: sentences that belong
in the format specification — what a conformant note looks like — keep
appearing in the concept of operations, and the audit should move them.

**Prompt.** Four, in order.

> Read `pkb-conops-sketch.md`, `CLAUDE.md`, and the documents under
> `process/`. I want `pkb-conops.md` 1.0, a light-skeleton concept of
> operations that realizes this sketch. Before proposing anything, run the
> audits in `process/conops-audit.md` and `process/spec-audit.md` on the
> sketch and report the gap list per RPT-1 — numbered, each with your
> recommended resolution. Then /grill-me: interview me about every decision
> the sketch leaves open, one question at a time, with your recommended
> answer for each. Stop after the gap list and wait for my rulings.

Rule on every item. For an item you defer:

> Ruling on item N: deferred. Write it to `BACKLOG.md` per DEV-6 — the
> question, where it arose, the options — and do not decide it.

Then:

> Propose the amendments per RPT-3 and wait for my approval.

Read the proposals; approve them, or rule again. Then:

> Write `pkb-conops.md` 1.0, run both audits on it again, report per RPT-1,
> and commit as `conops: 0.1 sketch -> 1.0`.

**Rules.** RPT-1, AUD-1 to AUD-7, AUDCON-1 to AUDCON-6, DEV-6, RPT-3, RPT-4,
DEV-3, DEV-7.

**Shown in.** Lecture 02 notes, *Auditing a concept of operations*; the L02
demo script, Segment 2 and *Recreating this part yourself*. For elicitation
as such, the foundations unit's Lecture 04: the grill-me skill and the
concept-of-operations interview in the 9×9 excerpts.

**Model.** `completed/note-set-conops.md` — the operations O1 to O3 in
input / precondition / postcondition form; the changelog entry that records
what the audit changed and why.

**Ends with.** `conops: 0.1 sketch -> 1.0`. Then export the session with
`/export transcripts/01-conops-elicitation.md` and commit it as
`transcripts: conops elicitation`. The export is plain text; the `.md`
extension is kept for consistency with the Project 1 brief. The RPT-1 list, your rulings, and the
RPT-3 amendments in that transcript are the evidence that the document was
elicited, not typed.

### Step 3 — Derive `pkb-format-spec.md` 1.0.0

**Do.** The same moves, with a new target: the format specification, which
says what a conformant entry in the bundle is. Its base is OKF v0.2 restricted
to the profile in §3. On top of the profile you decide the type vocabulary,
the folder layout under `kb/`, the filename rule, the index-entry form, what
`log.md` records, and how strict each rule is (§4). Every rule is numbered R1,
R2, …, written so that a verifier can answer yes or no to it, and never
renumbered. The document declares the RFC 2119 keywords, carries a version and
a changelog, and states in its section on OKF which fields the profile
excludes and why. Then the audit. Then an amendment to
`process/verification.md`, proposed per RPT-3, that replaces the VER-2 table's
by-kind rows with one row per rule: whether a program can decide it or a reader
must, with a rule that has a judgment half split across both columns, as the
note set's R8 was.

**Why.** Lecture 01's five quality properties are the point of this step, and
the first of them — unambiguous — decides whether step 7 is possible: a rule
that a verifier cannot answer yes or no to cannot be checked by anyone, human
or program. The VER-2 split is Lecture 02's decision about R8 made for every
rule of yours. "The `description` is one sentence" is mechanical; "the
`description` accurately summarizes the note" is judgment; a specification
that does not say which is which lets the algorithmic verifier's green result
claim more than it decided. The profile in §3 exists for a reason worth
understanding: OKF is a format for data catalogs as well as for personal
notes, and its trust, staleness, and computation fields serve catalogs. A
specification that carries fields no operation ever sets misleads the next
reader about what the system does, and is incomplete at its own level (AUD-4)
because it does not say what those fields mean here.

**Prompt.** Two, in order. The first pastes the profile paragraph from §3, so
that the exclusion is in the agent's context and not only in yours:

> Read `pkb-conops.md`, `CLAUDE.md`, and the documents under `process/`.
> Derive `pkb-format-spec.md` 1.0.0 from the concept of operations: the
> format of a conformant entry in the bundle `kb/`. The base is Google's Open
> Knowledge Format v0.2
> (https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md),
> restricted to this profile:
>
> [paste the paragraph *What to tell the agent* from §3 of the brief]
>
> The specification states numbered rules R1, R2, … each decidable as yes or
> no; the closed `type` vocabulary with a one-line definition of each value;
> the filename rule; the folder layout under `kb/`; the entry form of
> `kb/index.md` and which field it displays; what `kb/log.md` records and the
> form of an entry; the link form; the RFC 2119 keywords; a version and a
> changelog. Before writing, run the audit in `process/spec-audit.md` on the
> concept of operations, list every decision it leaves open that this
> specification must settle, report per RPT-1, and wait for my rulings.

Rule on every item; defer what you cannot settle. Then:

> Write `pkb-format-spec.md` 1.0.0, run the audit on it, and report per
> RPT-1. Then propose per RPT-3 the amendment to `process/verification.md`
> that replaces the VER-2 table's rows by kind with one row per rule,
> mechanical or judgment, and wait for my approval.

Approve, or rule again; then have the agent commit.

**Rules.** AUD-1 to AUD-7, RPT-1, RPT-3, DEV-3, DEV-5 (the format
specification must not contradict the concept of operations), VER-2, DEV-7.

**Shown in.** Lecture 01 notes, *Evaluating a specification: the quality
properties, as an audit* and *The audit, in the demo*; Lecture 02 notes, *A
specification is continuously maintained: a new requirement* (R8 and the
VER-2 split); the L01 demo script, Segment 2.

**Model.** `completed/note-format-spec.md` — the form of a rule, the scope
sentence, the changelog; `completed/process/verification.md` — the VER-2
table at specification 2.0.0.

**Ends with.** `format-spec: 1.0.0`, with the amendment to
`process/verification.md` in the same commit or the one before it, with its
changelog entry.

### Step 4 — Derive `pkb-operations.md` 1.0

**Do.** Derive the operations document from the two governing documents: one
section per operation the concept of operations promises, each with its
input, precondition, steps, and postcondition; a short section for the
one-time scaffold of the empty bundle (step 5), which the concept of
operations need not list; a conventions section — the slug function, the rule
that every operation touching the bundle ends with the conformance check, the
commit-message form; and the statement that the specifications win where the
documents disagree. Audit the new document for consistency with both governing
documents (AUD-3) and for traceability (AUD-5: each step cites the rule or
clause it realizes). If the audit finds a gap, where it is decides what moves:
a finding against a governing document is an RPT-3 amendment to that document
(DEV-5); a finding against the operations document is a correction to it.
Commit.

**Why.** The concept of operations says what an operation achieves, from the
user's side; the format specification says what a conformant note is; neither
says how the agent gets from one to the other. The operations document is
that third abstraction (Lecture 02: three specifications, three abstractions),
and DEV-5 governs it: derived from the governing documents, never
contradicting them, corrected rather than improvised when it is wrong. Its
steps are the instructions the agent follows in step 6 and every week after,
so an execution gap here — a step that cannot be performed without inventing
something — shows up later as an inconsistent bundle.

**Prompt.**

> Read `pkb-conops.md`, `pkb-format-spec.md`, and the process documents.
> Derive `pkb-operations.md` 1.0 from them per DEV-5: for each operation the
> concept of operations promises, its input, precondition, steps, and
> postcondition; a section for the one-time scaffold of the empty bundle; the
> conventions; and the statement that the specifications win where this
> document disagrees with them. Each step cites the rule or
> clause it realizes. Then audit the document against both governing
> documents (AUD-3, AUD-5), report per RPT-1, and wait.

Rule; then have the agent commit.

**Rules.** DEV-5, AUD-3, AUD-5, RPT-1, DEV-7.

**Shown in.** Lecture 02 notes, *Deriving lower-level specifications from the
concept of operations*; the L02 demo script, Segment 3.

**Model.** `completed/note-set-operations.md`.

**Ends with.** `operations: 1.0`.

### Step 5 — Clear the context; scaffold the empty bundle

**Do.** Run `/clear`. Then ask, before anything else:

> What is your understanding of the purpose and state of this repository, and
> which documents govern the next operation?

If the answer is wrong or incomplete, the fix is to the loader or to the
documents, not to the conversation: correct the file, commit it (`loader: …`
with a changelog entry, since `CLAUDE.md` is under DEV-3), clear again, and
ask again. Save the final question and answer; they open the report (step 8).
When the answer is right, have the agent scaffold the bundle: `kb/index.md`, `kb/log.md`, and
the folders `pkb-format-spec.md` names, with nothing else in them.

**Why.** Everything the agent knows after `/clear` comes from the files the
loader names. This is the test of whether your three documents and the loader
carry the whole state of the project across a context boundary — the property
that lets a later session, a colleague, or a later you pick the work up.
A loader that needs the conversation to make sense is a specification that is
incomplete at its own level. The scaffold itself is small. It is the first
realization of the format specification's rules on the reserved files, and it
is performed as an operation so that it ends the way every operation ends
(DEV-7).

**Prompt.**

> Scaffold the empty bundle as `pkb-format-spec.md` specifies: `kb/index.md`,
> `kb/log.md`, and the folders the specification names. Verify the result
> against the specification, give the completion note per RPT-5, and commit
> as `scaffold: empty bundle`.

**Rules.** DEV-1, DEV-3 (the loader), VER-3, RPT-5, DEV-7.

**Shown in.** Lecture 01 notes, the closing section on where a developer's
time goes; the L01 demo script, Segment 1 (what the loader does); the
foundations unit's Lecture 06 on memory across `/clear`.

**Model.** `completed/index.md` for an index with entries; `completed/CLAUDE.md`
for what a loader must carry.

**Ends with.** `scaffold: empty bundle`.

### Step 6 — Seed the bundle: five or more notes, as operations

**Do.** Add at least five notes, in your own words, from the foundations unit
and from Lectures 01 and 02 — for example: the agent loop; context windows and
caching; specification, realization, and conformance; the three kinds of
verifier; the concept of operations and validation; a lesson from Exercise 1
or 2. Each note is added by an operation from `pkb-operations.md`, and each
operation ends as DEV-7 requires: the affected files verified against the
format specification, a completion note per RPT-5 that names which judgment
clauses remain for you to check, and a commit named for the operation. Among
the five: at least one note that cites an external source — a `sources` entry
and a per-claim footnote — and at least one note of your Reference type,
produced by the operation that summarizes a source you name. Add the notes in
an order such that every link points to a note that already exists, or list
the target under a "not yet written" heading in `kb/index.md` and remove that
entry when the note arrives; otherwise the link rule fails at the earlier
commit, and the gate with it. Then open `kb/` in Obsidian (or your viewer) as
a vault and confirm that every link resolves except the ones you meant to
leave open.

**Why.** Lecture 02's claim is that conformance is an invariant re-established
after every operation, not a milestone reached once. Five operations in a row
are where you see what that costs and what it buys. The completion note is the
part students skip and should not: a green check decides mechanical clauses
only (VER-4), and the note is where the judgment clauses — "in the student's
own words", "the description summarizes the note" — are named as remaining
for you, rather than silently assumed covered. The notes' content is the
other half of the outcome. Written in your own words, they are the first
entries of the artifact you keep.

**Prompt.** For a note you wrote (adapt the operation number to your
operations document):

> Perform O1 — add a note with content. Title: "The agent loop". Content
> follows. End the operation as DEV-7 requires.
>
> [your paragraphs]

For a Reference note from a source:

> Perform O2 — add a Reference note. Source: <URL>. Summarize it in two
> paragraphs, record the source in `resource` and `sources`, and end the
> operation as DEV-7 requires.

**Rules.** DEV-1; DEV-2 (every change to the bundle is a repair, a
conformance-preserving change, or a change of specified behavior, and the
history shows which); VER-3; VER-4 once the verifier exists, and before that
an agent verifier reporting per RPT-2; RPT-5; DEV-7; DEV-6.

**Shown in.** Lecture 02 notes, *Performing operations under the development
rules, and the invariant*; the L02 demo script, Segment 4 and *Recreating
this part yourself*.

**Model.** `completed/notes/no-silver-bullet.md` for a note; the RPT-5 example
in `completed/process/reporting.md` for a completion note; the commit
messages in the L02 demo script.

**Ends with.** Five or more commits, each named for its operation — the
operation's name as your operations document gives it, not its O-number — for
example `add-note: The agent loop`.

### Step 7 — Stretch: the algorithmic verifier

**Do.** Have the agent write `check_pkb.py`. Given note paths, it decides the
per-note rules of `pkb-format-spec.md` that the VER-2 table marks mechanical;
given `--all`, every note under `kb/` plus the index and log rules; one line
per violation citing the rule; exit 0 for conformant, 1 for violations, 2 for
a usage error. Then the two amendments per RPT-3: the VER-2 table names the
script as the algorithmic verifier for each mechanical rule, and the loader's
Commands section names `python3 check_pkb.py --all` as the gate (VER-4). Run
the sabotage test from Lecture 01: break one note by hand, commit `careless
edit (before)`, watch the gate exit 1, ask for the report per RPT-2, rule,
repair, commit `careless edit (after)`. The first of those commits breaks
VER-4 on purpose, so that the history shows the gate catching a nonconformant
state; its message says so.

**Why.** Lecture 01 compared the three kinds of verifier on cost,
repeatability, and what each can decide. This step is where the comparison
becomes concrete for a specification you wrote. Two things to notice while it
is built. The script is itself a realization of the format specification and
can be wrong in the six ways the lecture listed — in particular, it can
implement a rule as its author remembered it rather than as written, which is
why the VER-2 amendment and the sabotage test are part of the step. And a
program that returns an exit code can stand in front of a commit; that is what
makes it a gate, and from now on every operation on the PKB ends with it.

**Prompt.**

> Write `check_pkb.py`, an algorithmic verifier for `pkb-format-spec.md`
> 1.0.0. It decides every rule the VER-2 table marks mechanical: given note
> paths, the per-note rules; given `--all`, every note under `kb/` plus the
> index and log rules. One line per violation, citing the rule identifier and
> quoting the rule; exit 0 conformant, 1 violations found, 2 usage error.
> Judgment clauses are out of scope and are named in the docstring. Then
> propose per RPT-3 the amendments to the VER-2 table and to the Commands
> section of `CLAUDE.md`, and wait.

**Rules.** VER-1, VER-2, VER-4, RPT-2, RPT-3, RPT-4, DEV-3, DEV-4, DEV-7.

**Shown in.** Lecture 01 notes, *The verification gate*, *Verification and the
three kinds of verifier*, and *How a verification result can be invalid*; the
L01 demo script, Segments 3 and 4.

**Model.** `completed/check_notes.py`; `completed/process/verification.md`, the
VER-2 table and VER-4.

**Ends with.** `verifier: check_pkb.py for format-spec 1.0.0`, then `careless
edit (before)` and `careless edit (after)`.

### Step 8 — Close: the kickoff report

**Do.** Write `KICKOFF-REPORT.md`. It opens with the memory check of step 5 —
the question you asked after `/clear` and the answer you accepted — and then
has four sections, in this order.

1. **The elicitation as an agent loop.** From
   `transcripts/01-conops-elicitation.md`, two examples each of a user input,
   an agent response, a tool call, and a tool result feeding back into the
   context — quoted, or cited by line — with one sentence each on what the
   element did for the session.
2. **Commits and rules.** For each commit in your history, the DEV rule or
   rules it obeyed; for each change to a realization, which of DEV-2's three
   kinds it was.
3. **Verification scope.** In the form of RPT-2's three scope lines, what the
   bundle was checked against at the end of the kickoff: which verifier,
   which version of the format specification, which rules; and which judgment
   clauses you checked yourself, and which you did not.
4. **Reflection.** Two or three paragraphs: what went as you expected and what
   did not; whether the agent's behavior under the process documents matched
   what the lectures led you to expect; and what the kickoff shows about
   where a developer's time goes under agentic development — the claim
   Lecture 01 closed on — measured against your own hours.

**Why.** The first section connects this project to the foundations unit: an
elicitation is the agent loop of that unit's Lecture 02 running with you as
the source of the inputs, and seeing the loop in a transcript is the skill
Exercise 1 started. The second is the audit of the process: the commit log is
the realization of the process documents, and reading it against the rules is
how a process is audited (Lecture 02). The third is the habit of stating
scope, which is the only defense against a true-looking result that misleads
(Lecture 01). The fourth is the reflection every completion-based deliverable
in this course carries.

**Prompt.** None; this is yours to write.

**Rules.** RPT-2 (the scope lines); DEV-2.

**Shown in.** Lecture 01 notes, *How a verification result can be invalid*;
Exercise 2, step 6.

**Model.** The RPT-2 example in `completed/process/reporting.md`.

**Ends with.** `kickoff report`.

### Required elements (all must be present)

- [ ] **[0]** The starter's `process/` and `CLAUDE.md` in the first commit,
      unmodified afterwards except by RPT-3 amendments with changelog entries.
- [ ] **[1]** `pkb-conops-sketch.md` 0.1, written by you, with at least three
      scenarios.
- [ ] **[2]** `pkb-conops.md` 1.0 with a changelog entry;
      `transcripts/01-conops-elicitation.md` showing the RPT-1 gap list, your
      rulings, and the RPT-3 amendments; at least one entry in `BACKLOG.md`
      written instead of decided.
- [ ] **[3]** `pkb-format-spec.md` 1.0.0: numbered rules, a closed type
      vocabulary, an OKF section stating the profile and the excluded fields;
      `process/verification.md` amended so that the VER-2 table classifies
      every rule.
- [ ] **[4]** `pkb-operations.md` 1.0, each step citing what it realizes.
- [ ] **[5]** `kb/index.md` and `kb/log.md` in the forms the specification
      gives; the memory-check question and answer at the top of the report.
- [ ] **[6]** Five or more notes, each added by a commit named for its
      operation and reported in an RPT-5 completion note (saved in the report,
      or as the body of the commit message); at least one with `sources` and a
      per-claim footnote; at least one Reference note with `resource`; the
      bundle opens as a vault with every intended link resolving.
- [ ] **[7]** *(optional)* `check_pkb.py`; the VER-2 table and the loader
      amended; the `careless edit (before)` / `(after)` pair.
- [ ] **[8]** `KICKOFF-REPORT.md`: the memory check, then its four sections.

## 3. The OKF profile this course uses

OKF v0.2 defines a bundle as a directory tree of Markdown files with YAML
frontmatter, two reserved files, and bundle-relative links. Its conformance
rule is short: every non-reserved `.md` file in the tree has parseable
frontmatter with a non-empty `type`; `index.md` and `log.md`, where present,
have the forms the specification gives. Everything else in OKF is optional,
and most of it was designed for catalogs of datasets and computations rather
than for a set of notes. The instructor's own PKB, kept in this format, used
the fields below on every note and never used the rest. Your format
specification adopts the profile as its base and may tighten it — make an
optional field required, restrict a value — but does not extend it during
Project 0.

**Fields you use.**

| Field | When | What it is for |
|---|---|---|
| `type` | required (by OKF) | The kind of note, from your closed vocabulary (§4). |
| `title` | required | The note's name; a noun phrase. |
| `description` | required | One sentence; the text `index.md` displays beside the link. |
| `generated` | required | `by`: the actor that wrote the current content, as `claude-code/<model>` or `human:<your name>`; `at`: the date, `YYYY-MM-DD`. This is OKF's authorship stamp, and it is how a reader tells agent-written content from human-written content. |
| `sources` | when the note derives from external material | A list. Each entry has `id` (a short key that the body's footnotes cite) and `resource` (a URL or a path), and may have `author` and `last_modified` (`YYYY-MM-DD`). Whether a note derives from external material is a judgment; a program checks only the form of the list and that every `id` is cited. |
| `resource` | on a Reference note | The URL of the source the note summarizes. A Reference note also carries a `sources` entry for the same URL, so that its footnotes have an `id` to cite. |
| `status` | optional | `draft` or `stable`. Your specification says who may set `stable`; the sensible rule is that the agent never does. |
| `okf_version` | optional, on `kb/index.md` only | `"0.2"`. |

**Fields you do not use.** Your specification does not define them, the agent
does not generate or propose them, and a note carrying one is nonconformant.

| Field | Why it is excluded |
|---|---|
| `tags` | A second classification axis beside `type` and the folder layout. It went unused in practice; if you need cross-cutting classification later, add it by amendment, with a rule that says what a tag means. |
| `sources[].title`, `sources[].usage_count`, `usage_window` | Catalog signals: how often a dataset was used, and over what period. A note cites a source; it does not meter it. |
| `verified` | A list of confirmation events by actor, from which OKF derives trust tiers. The bookkeeping outweighed its value; `status` and `generated.by` say what a reader needs. |
| `stale_after` | A staleness horizon per note. Freshness is a judgment a reader makes while reading; a date that expires by itself was never acted on. |
| `status: deprecated` | Notes are removed by an operation, not marked; a removed note's history is in git and in `log.md`. |
| `runtime`, `parameters`, `computation`, `executor`, `attester`; the type `Attested Computation` | OKF's machinery for documents that run and attest a computation. Nothing in a PKB executes. |

Two OKF rules to keep as written. Links are bundle-relative and begin with `/`
(`/concepts/agent-loop.md`). A link to a file that does not exist is legal: it
marks knowledge not yet written, and Obsidian shows it as an unresolved link.
Your specification may restrict the second rule — for example, to links listed
under a "not yet written" heading in `index.md` — but it should say what it
does about the case, because the verifier has to decide it.

**What to tell the agent.** Paste this paragraph into the step 3 prompt, and
into any later prompt that adds or changes a frontmatter field, so that the
exclusion is in the agent's context and in the specification it writes:

> Frontmatter fields: every note MUST carry `type`, `title`, `description`,
> and `generated` (`by`, an actor string; `at`, a date `YYYY-MM-DD`). A note
> derived from external material MUST carry `sources`, a list whose entries
> have `id` and `resource` and MAY have `author` and `last_modified`. A note
> of the Reference type MUST carry `resource`. A note MAY carry `status` with
> the value `draft` or `stable`. `kb/index.md` MAY carry `okf_version: "0.2"`
> and no other frontmatter. No other frontmatter field is permitted. In
> particular, do not use, generate, or propose `tags`, `sources[].title`,
> `sources[].usage_count`, `usage_window`, `verified`, `stale_after`, the
> status value `deprecated`, or any field of OKF's Attested Computation family
> (`runtime`, `parameters`, `computation`, `executor`, `attester`), and do not
> define a type named `Attested Computation`. State this exclusion in the
> specification's section on OKF, with the reason: those fields serve data
> catalogs and the trust or staleness tracking that a personal knowledge base
> does not use.

## 4. Decisions your specification must record

The concept of operations and the format specification must settle the
following. Finding them is part of the exercise; this list is the floor.

**Concept of operations**

- Who reads the PKB and who writes to it; which operations the agent performs
  and which only you perform (for example, setting `status: stable`).
- The scenarios, and an operation for each: at least adding a note with your
  content, adding a Reference note from a source, removing a note, and
  checking conformance.
- What conformance means for the bundle as a whole, and who may ask for a
  check.

**Format specification**

- The `type` vocabulary: closed, two to four values, one line each; one value
  is a Reference type for summaries of sources you cite. (The example uses
  `Concept` and `Reference`.)
- The layout under `kb/`: notes in folders by type, by topic area, or flat;
  where the reserved files sit. Recorded with the reason, because the layout
  is what a reorganization later has to change by amendment.
- The filename rule (the slug of the title, as the note set's R7), and what
  happens when a title already exists.
- The index-entry form and which field it displays; whether `index.md` lists
  every note (a bijection, as the note set's R6) or only some.
- What `log.md` records — every operation, or only additions and removals —
  and the form of an entry (in OKF: a date heading `YYYY-MM-DD`, newest first,
  prose beneath).
- The body form: one H1 equal to `title`; whether a summary section is
  required; whether every footnote label must match a `sources[].id`.
- The link form, and the broken-link policy.
- Whether `status` is used, and the rule for who sets it.
- What `generated.by` records when the agent files text you wrote; the sensible
  rule is `human:<you>`, with the agent's actor string only when the agent
  wrote the content.
- For each rule, mechanical or judgment (the VER-2 table). A rule such as
  "`sources` is present when the note derives from external material" splits:
  the form of the list is mechanical, the condition is judgment.

Two things to expect. The index and log rules are the ones most likely to be
under-specified; write the entry form to the character, as the note set's R6
does, because that is what the verifier has to match. And eight to twelve
rules is enough for the kickoff; a longer list costs specification and
verifier time that the notes need more.

## 5. Process rules

1. **Read before acting (DEV-1).** Every session starts from the files. A
   ruling given from memory of a document is a verification failure waiting
   to happen (VER-1).
2. **The specifications move first (DEV-2, DEV-3).** A note that would
   violate the format specification is not written. If the rule is wrong, the
   rule is amended by RPT-3 with a version bump and a changelog entry, and
   then the note is written. The history has to show the order.
3. **Nothing under `process/` or in `CLAUDE.md` changes without a proposal
   and a changelog entry (DEV-3).** The two amendments the kickoff expects —
   the VER-2 table in step 3 and the gate in step 7 — go through RPT-3 like
   any other.
4. **Report before repair (RPT-4).** When a check fails, the report comes
   first, and you rule on which side moves (DEV-4). The ruling goes in the
   changelog when a specification moves and in the commit message when a note
   moves.
5. **Defer explicitly (DEV-6).** A question you cannot settle goes to
   `BACKLOG.md` with its options; it is closed by a ruling recorded where
   DEV-4 says.
6. **Every operation ends the same way (DEV-7).** Verification of what changed
   (VER-3, and the gate once it exists, VER-4), a completion note (RPT-5), a
   commit named for the operation.
7. **The bundle boundary.** `kb/` is the OKF bundle, and nothing above it is.
   The governing documents, the process documents, the transcripts, and the
   report live outside it; the verifier checks `kb/` only.
8. **Commit vocabulary.** `kickoff start: …`; `conops: …`; `format-spec: …`;
   `operations: …`; `scaffold: …`; `<operation>: <title>` for every operation
   on the bundle, where `<operation>` is the name your operations document
   gives it (`add-note`, `add-reference`, `remove-note`), not its O-number; `verifier: …`; `careless edit (before)` / `(after)`;
   `transcripts: …`; `kickoff report`; and `<document>: <old> -> <new>` for
   every amendment.

## 6. Grading

Completion-based. The kickoff is satisfactory when every required element of
§2 is present and honest. A documented failure counts: a gap list with items
you could not resolve and deferred; a verifier that decides fewer rules than
you hoped, with the VER-2 table saying so. A missing element does not.
Project 0 counts toward the individual-exercises share of the grade (30%, per
the foundations unit's Lecture 01). The checkpoints in §7 are graded the same
way.

## 7. Maintaining the PKB through the semester

The kickoff leaves you a bundle with five notes and a process for adding more.
The rest of Project 0 is that process, run weekly.

- **Weekly, about thirty minutes.** Add or improve notes by operations from
  `pkb-operations.md`: a concept from the week's lectures in your own words; a
  summary of a paper, post, or talk you read; a lesson from a project session.
  Each ends per DEV-7. Anything you find yourself explaining to the agent
  twice is a note.
- **`kb/log.md` is the record.** It is what a checkpoint reads for evidence
  that the bundle grew by operations rather than by a batch of files.
- **Amend when the rules get in the way.** A rule you keep working around is
  a specification that has fallen behind its realization. The fix is RPT-3, a
  version bump, and re-verification of everything the amendment touches
  (VER-3), not a note that quietly breaks the rule. Expect at least one such
  amendment before week 10.

**Checkpoints (completion-based).** At each, tag the commit (`cp1`, `cp2`,
`cp3`) and add a half-page `CHECKPOINT-n.md` at the repository root that
addresses the items:

- **Checkpoint 1, week 6** (the project unit's Lecture 11): twelve or more
  notes; `kb/log.md` showing steady accretion; one note capturing a lesson
  from Project 1, Phase 1; every note since the kickoff added by a named
  operation commit.
- **Checkpoint 2, week 10:** twenty-five or more notes; at least one amendment
  to a governing document carried through RPT-3, a version bump, and
  re-verification — or a paragraph saying why none was needed; the verifier in
  use as the gate, if it exists; evidence of the reorganization, if the layout
  changed.
- **Checkpoint 3, week 15:** the final state, and a half-page retrospective:
  what the kickoff specification got wrong, what the amendments were, and
  what you would tell a student designing theirs.

**What later units connect.** The project unit's Lecture 10 (skills) has you
package a note-capture procedure as a Claude Code skill; Lecture 12 (hooks and
memory) places the PKB in the memory taxonomy beside `CLAUDE.md` and
auto-memory; Lecture 14 (MCP) and the Project 1 brief offer an optional
stretch, an MCP server exposing search over your bundle.

**Extensions that are not part of Project 0.** A PKB kept for longer tends to
grow classification links between notes (a field naming the topics a note
belongs to), a store for full-text captures of sources, transcript ingestion
for videos, and views over `status`. Each of these is a change of specified
behavior (DEV-2, kind c): an amendment to the governing documents first, then
the realization. None is expected this semester, and none belongs in the
kickoff.

## 8. Do / don't

- **Do** write the sketch yourself, before the agent sees anything. **Don't**
  paste the OKF specification and ask for "a personal knowledge base"; the
  result will conform to OKF and to nothing you decided.
- **Do** paste the profile paragraph from §3 into every prompt that touches
  frontmatter. **Don't** accept a field from the excluded list because "OKF
  allows it"; your specification does not.
- **Do** keep the governing documents outside `kb/`. **Don't** let the agent
  set `status: stable`; that is your judgment.
- **Do** rule in one or two sentences and move on. **Don't** re-open a ruling
  in conversation without recording the new one where DEV-4 says.
- **Do** defer what you cannot settle. **Don't** let the agent guess, and
  don't guess yourself: a `BACKLOG.md` entry costs a minute; a silent guess
  costs a reorganization.
- **Do** read the completion notes. **Don't** treat a green gate as
  conformance; it decides mechanical clauses only.
