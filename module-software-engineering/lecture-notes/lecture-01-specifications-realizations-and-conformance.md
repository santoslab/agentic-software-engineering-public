# Lecture 01 — Specifications, Realizations, and Conformance

> Software-engineering module, meeting 1 of 6. Companion reading for the lecture
> and for part 1 of the note-set demo
> (`../demos/lecture-01-note-specs-demo/demo-script-lecture-01.md`);
> self-contained. Launches **Exercise 1**.

## The example: a set of study notes

This lecture uses a running example to illustrate the concepts of specification, 
realization, and conformance. 

The example is a folder of notes, similar to what 
you might write as you are studying about a particular topic.  For instance, 
for each research article you read, you write a markdown file to summarize the key 
points of the article.

Two questions come up at once. How should a note be formatted, so that every note looks the
same and a tool can read them all? And who checks that a note is formatted that
way?

To answer the first question, we will use a document that is not a note -- it is a 
**specification** of the note format, `note-format-spec.md`.  It provides the 
formatting rules that notes in our note set must follow.

In this lecture, we will study..
  - the rules that appear in `note-format-spec.md`
  - general principles for judging whether a specification is "good" (this will take 
  the form of "auditing" a specification), 
  - approaches for determining if a note is formatted according to the `note-format-spec.md`
    (i.e., for verifying if the note conforms to the specification).
We will also come to understand that the way that we work with the specification above 
(e.g., write the spec, have an approach for checking the quality of the specification, 
having an approach for judging if the realization satisfies a specification) should be documented as part of a *development process* that both humans and agents follow.

The repository at the start of the demo holds three things and no notes:

- `note-format-spec.md`, version 0.1, marked draft — six numbered rules that
  every note must satisfy;
- `CLAUDE.md`, a short file that names the specification, names the process
  documents, and states two rules for the agent: read everything before acting,
  and change nothing without approval;
- `process/`, three documents that say how work proceeds with respect to the
  specification: `spec-audit.md` (how a specification's quality is assessed),
  `reporting.md` (the forms in which findings are reported), and
  `verification.md` (how conformance is checked, and by what).

The format specification, condensed:

| Rule | Requirement |
|---|---|
| R1 | A note begins with a YAML front-matter block delimited by `---` lines; the opening `---` is the first line of the file. |
| R2 | The front-matter contains exactly two fields: `title` (a non-empty string) and `created` (an ISO-8601 date, `YYYY-MM-DD`). |
| R3 | The body begins with a level-1 heading, which is the first non-blank line after the front-matter. |
| R4 | A note contains exactly one level-1 heading. |
| R5 | A heading is at most one level deeper than the nearest heading above it. |
| R6 | Every note file is linked from `index.md` exactly once, and every note link in `index.md` resolves to an existing file. |

The rules use the RFC 2119 keywords (MUST, MUST NOT, SHOULD, MAY) and are
numbered so that a report — written by a person, an agent, or a program — can
cite them.

The example was chosen for size. Six rules fit on one screen; a conformant note
is a dozen lines; every concept in this lecture can be pointed at in a file
rather than described in the abstract. Project 0 asks you to build a larger
version of the same thing.

## Four terms

**Specification (S).** A document that states, at a higher level than the
artifact it governs, what the developer intends. It fixes some properties and
deliberately omits others. `note-format-spec.md` fixes the front-matter fields
and the heading structure of a note. It says nothing about the note's subject,
length, or prose. The omissions are deliberate: the specification constrains
what matters to the developer and leaves the rest free. In the vocabulary of
the course's catalog of specification kinds (`../../specification-kinds.md`),
`note-format-spec.md` is a *data format* specification; the catalog lists the
other kinds the course uses, and Lecture 03 introduces several of them at once.

**Realization (R).** An artifact built to satisfy S. When R is code, the usual
word is *implementation*; *realization* is the general term, because a note, a
script, or another document can each be built to satisfy a specification. In the
example, every file in `notes/` is a realization of the format specification.

**Conformance.** The relationship between S and R that holds when R satisfies
every property stated in S. It is a yes-or-no question about the pair: given
this specification and this note, does the note satisfy R1 through R6?
Properties that S does not state are not part of the question. Two notes with
different content, different lengths, and different headings below the title
can both conform.

**Verification.** The activity of trying to confirm that R conforms to S. The
word *trying* is deliberate. Verification produces a result, and the result can
be wrong: the program that checks can have a bug; the reader can miss a line;
the check can be run against an old copy of S. A later section lists the ways
this happens. The point for now is that a verification result is evidence, and
we need to know what it is evidence of.

Taken together, the four terms above name the two participants (S and R), the relationship the
developer wants between them (conformance), and the act of finding out whether
the relationship holds (verification). Diagram 1 in the slides shows the
arrangement in the abstract and for the demo's files.

One specification has many realizations. Every conformant note is a distinct
realization of the same S.

## Evaluating a specification: the quality properties, as an audit

A specification can be poorly written or even incorrect. 
It can say something two readers would decide
differently; two of its rules can conflict; it can leave out something the
developer meant; and it can be impossible to cite. 

Even though specifications vary widely in their character, 
there are some general "quality properties" that specifications should possess...

**Unambiguous**: We want to be able to check if a realization conforms to a specification.
We need a "yes" or "no" answer.  This implies that every property in our specification 
is stated in such a way that we can determine if a realization satisfies or fails the property.

**Internally consistent**:  The specification does have any rules that conflict with each other.
In very bad cases, we can situations that, due to conflicting rules, there are no realizations
that can conform to the specifications.

**Externally consistent and aligned**:  We may have multiple types of specifications for a
system.  Even when the specification forms are different, the vocabulary and terminology used across
the specifications should be consistent.  To help with this, we often have a glossary to define 
terms that appear through our specifications, documentation, and implementations.  Building on 
"internal consistency" above, there should not be situations where two different specifications
have confliciting properties or implications about the system.

**Completeness**:  Specifications are meant to be abstractions -- they are intended to 
omit some details.  So "complete" does not mean "we have addressed everything".  Rather, 
the intuition is that, for the chosen level of abstraction, we have not omitted addressing things.
For example, if our system has three forms of output, and our specifications only give contraints 
for two forms of output, and our specifications are likely incomplete.

**Tracebility**:  As we develope our system and produce reports, we will want to refer back to 
specific clauses or properties stated in the specification.  For this reason, it is important to 
uniquely identify specification properties so that we can associate (trace) system implementation 
features that address the properties or error reports that report on property violations.

Before the world of agents, we would just list these principles somewhere in our
developer guidelines as things to be considered when writing and reviewing specifications.

But now in with agents available that can read and follow natural language instructions, 
we can turn these into instructions that agents apply.  

Specifically, we write the rules down in `process/spec-audit.md` to enable an agent to audit
our specifications (identifying gaps, and providing suggestions for improvement).
The rules are numbered AUD-1 through AUD-5, each with a test and an
example; AUD-6 says where to look (within each document; between documents;
between a document and the act of executing it); AUD-7 says what the audit
produces (a numbered gap list, in the form the reporting document calls RPT-1,
with a recommended resolution for each item) and that the auditor then stops
and waits for rulings.   

The concept of a specification audit should become part of a 
disciplined development process.  The agents can help enforce that process.
Specifically, the audit is run when the developer asks for it, before
any plan that would realize the specification, and after any amendment to the specification. 
A person, an agent, or a program can run it; the output has the same form whoever
produces it.

That is the first sense in which this lecture differs from a lecture that only
states the properties: the properties are a procedure, the procedure is a file
in the repository, and the file is cited by number.

## The audit, in the demo

The demo's second segment runs the audit. The developer types, in plan mode:

> Read `note-format-spec.md` and the process documents. Run the audit in
> `process/spec-audit.md` on the specification and report per RPT-1: number
> every finding, place it, quote the text, categorize it, and give a recommended
> resolution. Include the walkthrough that AUD-4 asks for: write one conformant
> note on paper, step by step, and say what you had to invent. State which of the
> three places in AUD-6 you searched. Then stop and wait for my rulings.

The agent reads the specification and the process files and returns a gap list.
Three findings are in the specification on purpose, and the list should contain
at least these:

1. **Inconsistent within the document (AUD-2).** The scope sentence says that
   every markdown file in the note set must satisfy the rules, and R6 names
   `index.md` — a file with no front-matter, which cannot satisfy R1. The
   document requires something of a file it also describes as unable to comply.
2. **Two clauses, one property, no stated relationship (AUD-2).** R2 requires a
   `title` field and R3 requires a level-1 heading. Nothing says they agree. A
   note whose heading differs from its title conforms to 0.1.
3. **An execution gap (AUD-4).** R6 requires links to note files, so a note has a
   filename; nothing says what it is. The walkthrough — write one conformant
   note — cannot finish without inventing one.

The developer rules on each. `index.md` is not a note: R1–R5 govern the files
in `notes/`, and `index.md` is governed only by R6. The H1 must equal the
`title` field, and the field is authoritative — a repair adjusts the heading,
never the field. A new rule R7 derives the filename from the title. The agent
proposes the amendments in the form RPT-3 — old text, new text, the finding
that motivates each, the version bump, the changelog entry — and waits. The
developer approves; the agent edits the file, sets the version to 1.0.0, and
commits. `git diff` shows the three changes and the changelog entry that
records why.

Notice what has happened: the specification changed, and there is not yet a
single realization of it (i.e., we are identifying potential errors 
early in our development process, before we potentially waste time or tokens
when we find them later).  Having this concept of an audit in place
only costs a few hundred tokens.

## When conformance fails: change S or change R

It is tempting to treat the specification as the truth, because the developer
wrote it. The audit has just shown otherwise. A specification can be missing a
rule, or two of its rules can conflict, or a clause can fail to say what the
developer meant.

So a conformance check that fails reports a fact about the pair (S, R). It does
not say which side is wrong. R may break a rule; or R may be what the developer
wants, and S may state the rule badly. Re-establishing conformance means
changing one side, and the choice is an engineering decision, made by a person
and recorded. When the specification moves, the decision is recorded in its
changelog entry; when the realization moves, in the commit message.

Two ways to look for defects in S: build realistic examples that exercise every
rule, and analyze S for the properties above. Both can be done by a person, an
agent, or a tool. Neither is easy, because in most cases only the developer
knows the intent, and people tire. In practice it is a systematic search over
scenarios and possible realizations, which is what the audit rules organize.

The demo shows both sides move. In the second segment the specification moved
and there was nothing to repair. In the third segment, which follows, the
realization moves and the specification holds still.

Diagram 2 in the slides shows the loop: verify; if conformance holds, record the
result; if not, decide which side is wrong, repair R or amend S, and verify
again.

## The verification gate

The demo's third segment. The developer creates `notes/`, pastes in a note
written carelessly the night before — in another editor, with nothing checking
it — as `notes/royce-1970-waterfall-paper.md` (the filename follows the R7 just
approved), and writes a one-line `index.md` by hand. Then:

> I wrote `notes/royce-1970-waterfall-paper.md` myself and added its index entry
> by hand. Check the note and `index.md` for conformance to
> `note-format-spec.md` 1.0.0 and report per RPT-2. Do not change anything.

RPT-2 is the form of a conformance report. Before any finding, it states three
things: which verifier produced the result, and its version; which
specification, at which version; which clauses were checked and which were not.
Then each finding: the clause, its text quoted, the location in the
realization, what was observed. Then a verdict. Repairs may be proposed; none
are applied.

The report finds four violations:

| In the file | Rule | Repair |
|---|---|---|
| `created: Sept 11, 2026` | R2 (in the specification since 0.1) | `2026-09-11` |
| H1 `The Waterfall Paper`; `title: Royce 1970 Waterfall Paper` | R3 (as amended an hour earlier) | the heading is rewritten; the field is authoritative |
| a second H1, `# My take` | R4 | demoted to `##` |
| a `####` heading directly after a `##` | R5 | demoted to `###` |

The R3 finding exists only because of the audit. Against 0.1 the heading was
allowed to differ from the field, and a report would have said so and been
correct — for 0.1. That is why a report says which version it was checked
against.

The report has been delivered and nothing has changed. That is RPT-4: report
before repair. The developer now rules — the specification is right and the note
is wrong — and asks for the repair, the re-check, and a commit. The agent makes
the four changes, runs the check again, reports that it passes, and commits.
The passing re-check is what "done" means: the task was not to edit the file
but to make the check pass.

One of the four repairs carried a decision. The heading and the field
disagreed; either could have been changed. The amended R3 says the field is
authoritative. That sentence is in the specification so that neither the agent
nor a program has to choose, and so that the choice is made once.

## Verification and the three kinds of verifier

There are three ways to check a note against the format specification.

1. **A human verifier** reads the specification and the note and works through
   the rules. This can decide every clause, including the ones that require
   judgment. It is slow, and its reliability depends on attention: the careless
   note went into the repository because nothing was checking.
2. **An agent verifier** is asked to check and report. It reads the specification
   (the loader's first rule requires this), reads the note, and reports findings
   that cite rule identifiers and quote rule text. It can apply judgment
   clauses. Each check costs tokens, and two runs can differ.
3. **An algorithmic verifier** is a program written to decide the
   specification's clauses. In the demo's fourth segment the agent writes one,
   `check_notes.py`: given note paths, it decides R1–R5 and R7; given `--all`,
   it decides every note and R6 over the index. It prints one line per
   violation citing the rule, and exits 0 for conformant, 1 for violations,
   2 for a usage error. It is deterministic, immediate, and free to run. It
   decides only the mechanical clauses.

| | Human | Agent | Algorithmic |
|---|---|---|---|
| Cost per check | minutes of attention | tokens | milliseconds |
| Same result on repeat | not guaranteed | not guaranteed | yes |
| Decides mechanical clauses | yes | yes | yes |
| Decides judgment clauses | yes | yes | no |
| Composable into a gate | no | with effort | yes, via the exit code |

This is VER-1 in `process/verification.md`. Because every rule has an
identifier, the three kinds of verifier are comparable: all three cite R2, R3,
R4, and R5 on the same note.

**Mechanical clauses and judgment clauses (VER-2).** A clause is *mechanical*
when a program can decide it from the file alone, and *judgment* when it needs a
reader's assessment. Every clause of specification 1.0.0 is mechanical. The
next lecture adds one that is not — "the summary accurately summarizes the
note" — and the table in `process/verification.md` that records the
classification is amended with it. A program decides what it can; the rest is
named as remaining for a human or agent verifier, never assumed to be covered.

The demo then sabotages the note — the `created` date changed to `Sept 2026` —
runs the program (one R2 line, exit 1), restores the file, and runs it again
(exit 0). A program that can return an exit code can stand in front of a
commit or a build; that is what makes it a gate.

One more thing about the program: it is itself a realization of the
specification. It was written to embody R1–R7, and if it implements a rule
wrongly, its results are wrong in a way the results do not show. The question
"who verifies the verifier" has to be answered separately — by reading the
script against the rules, by testing it on inputs with known violations, or by
comparing it with another verifier.

## How a verification result can be invalid

A verification result is a claim made by a verifier, and the verifier (or the specification
it is working with) can be wrong (whether it is a human, agent, or algorithmic verifier). 
Here are six ways that an "improper" verification result as produced in the the demo:

- **A defective S.** Before the amendments to the specification, 
  the specification required every
  markdown file to satisfy R1.  But `index.md` could not satisfy the specification. A
  verification result against an inconsistent specification cannot be valid,
  regardless of the verifier that produces it. This is why the specification is audited
  before anything is checked against it.
- **Clauses not decided.** A pass from the program (the algorithmic verifier) 
  says nothing about clauses the program does not decide (i.e., clauses that require
  judgement). A verification report has to say which clauses are actually checked.
- **The verifier misinterprets or mis-implements a clause.** `check_notes.py` is
  built to embody the rules. If it mis-parses a heading inside a code block, it
  is a nonconformant realization of the specification, and its results are wrong
  silently.
- **Checking from memory instead of from the document.** An agent that read the
  specification earlier in a session may judge from recollection. The loader's
  first rule — read before any operation — exists so that the check is driven
  by the current file.
- **Attention.** The human is the verifier for judgment clauses, and for
  everything else whenever no process is running. The careless note written
  by the developer (`royce-1970-waterfall-paper.md`) is an example where a human
  did not put in enough effort or didn't pay attention, and so a note
  that did not conform to the specification entered the note set.
- **Wrong version of S.** A verifier written for 1.0.0, run after the
  specification moves to 2.0.0, reports the old notes conformant. A pass against
  an old specification is a false result, and nothing in the output says so
  unless the verifier states which version it implements.

Verification does not give a proof that the realization meets the
specification. It gives evidence within a scope: which verifier, which version
of S, which clauses. The three scope lines of RPT-2 exist so that the scope is
always stated, and a report that states them can be trusted for what it claims
and no further.

## What the process documents did today

Three documents in `process/` were in use, and it is worth naming what each did.

- `spec-audit.md` (AUD) was run once, when the developer asked, before anything
  was built. It is not loaded every session; it is invoked.
- `reporting.md` (RPT) gave every report its form: the gap list (RPT-1), two
  conformance reports (RPT-2), an amendment proposal (RPT-3), and the rule that
  nothing changes until a report has been read and a ruling given (RPT-4). It
  is always loaded.
- `verification.md` (VER) named the three kinds of verifier and their scope
  (VER-1) and classified the clauses (VER-2). It is always loaded.

`CLAUDE.md` itself says little: which document governs, which process documents
apply, and two rules — read everything first; change nothing without approval.
Everything else the agent needs to know is in a file whose name is the concept.

Not yet present: any operation the agent performs on the set, any statement of
what the set is *for*, and the rule that conformance is maintained as an
invariant while the set changes. Those are Lecture 02.

We are starting to see something important: as we embrace agentic development, 
more time is spent by humans writing specifications and setting up the development 
process, as opposed to the conventional developer practice of writing code.

## Exercise 1 and Project 0

Exercise 1 asks you to run the demo's audit and verification segments in your
own session, write one note carelessly, and check it with all three kinds of
verifier. The deliverable is a table of findings by verifier, one explained
disagreement or coverage gap, and a half page on which side should have moved
and how each verifier could have been wrong.

It is deliberately small. Project 0, assigned at Lecture 02, has the same
structure at a larger scale: your PKB specification is this specification grown
up, its conformance checklist is R1–R7 grown up, and the stretch-goal validator
is `check_notes.py` grown up.

## Questions to think about

1. Name one property of a note that `note-format-spec.md` 1.0.0 leaves
   unconstrained. Should it stay unconstrained? If not, write the rule and say
   which kind of verifier would decide it.
2. For the R3 finding on the careless note, defend moving the specification
   instead of the note: what would the amendment say, and what would it cost the
   rest of the system?
3. A compiler's type checker is an algorithmic verifier. Which of the six
   failure modes apply to it, and what stands in for "who verifies the
   verifier" in that setting?

## Before next meeting

- Read Royce (1970), "Managing the Development of Large Software Systems," and
  Meyer (1992), "Applying Design by Contract"; see `../reading-list.md`. Meyer's
  precondition and postcondition are the form the next lecture gives to an
  operation.
- Read the Lecture 02 handout: the draft concept of operations and the three
  process documents Lecture 02 adds.
- Exercise 1 is due before Lecture 03.
