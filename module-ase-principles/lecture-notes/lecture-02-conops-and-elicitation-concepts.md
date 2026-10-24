# Lecture 02 — ConOps and Elicitation Concepts

> Agentic software engineering principles module, meeting 2. Companion reading
> for the lecture; self-contained. The example is version A1 of the message
> guard, in `../demos/running-example-message-guard/a1/`, with version A0
> (`a0/`) used for contrast; file paths below are relative to `a1/` unless
> they say otherwise. Vocabulary follows the course glossary,
> `../../glossary.md`. Launches **Exercise 2**.

## Purpose of this lecture

Lecture 01 introduced the concept of operations as one of the two
specifications of version A0: the document that says what the system is for,
who uses it, and what they observe, and the one document a stakeholder signs.
That was a view from a distance. This lecture takes the document apart.

Four questions organize it. **Why** do we write a concept of operations, and
what does it do for validation that no other artifact can? **What** is in
one, section by section, and why does version A1's differ from A0's in
format? **How** is it obtained from the people whose intent it records,
which is the activity called *elicitation*, and what does a disciplined
version of that activity look like when an agent conducts it? And **what do
we do with it** once it exists: in this lecture, two things, validating it
with the stakeholders, and deriving from its stories a set of system tests
that any realization of the system must pass, through the artifact the
course calls a *fixture* or *scenario file*.

The third use of a concept of operations, deriving requirements from its
stories, is the subject of the next lecture. This one stops where that
derivation begins, and says so at the point where it stops.

The running example is version A1 of the message guard. Its product behavior
is exactly A0's: one stage, `filter`, drops a Critical message and passes
anything else unchanged, and the code in `guard/` is byte-identical between
the two versions. Everything that changed between A0 and A1 is in how the
system is specified, checked, and recorded, which is why A1 is the version
for a lecture about a specification.

### Learning objectives

By the end of this lecture, students should be able to:

- State what a concept of operations fixes and what it deliberately leaves
  open, and explain why it is the specification on which validation is
  performed rather than one of the specifications that are verified.
- Name the sections of A1's concept of operations, say what each is for,
  and identify, for each difference from A0's format, the problem it
  answers.
- Distinguish an assumption (an obligation of the deploying organization)
  from a requirement (an obligation of the system), and a deferred want
  (heard and recorded) from a promise.
- Describe elicitation as a procedure with a stopping condition: what is
  asked, of whom, in what form, how the answer is recorded, and where the
  answer lands in the document.
- Explain why the elicitation record is reference material and not a
  specification, and what follows from that for the audit and for the
  assurance report.
- Read a scenario file and its loader, and trace one scenario from the
  stakeholder's example to a row of the conformance report and a row of the
  trace matrix.
- State what a passing scenario set establishes and what it does not, and
  explain why the file is governed on the specification side.
- Construct a case in which every scenario passes and validation fails, and
  say which clause of the assurance report moves and which verifier
  catches it.

## Where we are: A0's concept of operations, and what it did not say

A0's `specs/conops.md` had five sections: a purpose statement, a scope with a
list of terms, two user categories, three user stories each with an example
message, and a pointer to the sign-off. Lecture 01 presented it as an
artifact "already agreed on by the stakeholders", because the lecture was
about the entities and the judgments, not about how the document came to be.

Read it again with the questions of this lecture in mind, and several things
are missing or in the wrong place.

- The purpose statement ended with a promise: "Later versions will sanitize
  what leaves, record what was stopped, and let the security officer change
  the policy." Nobody is named as wanting any of that, and nothing in the
  document says whether these are commitments or ideas.
- The deployment assumption, that messages leaving the enclave are routed
  through the guard, sat inside the purpose statement, and the assumption on
  which the whole decision rests, that a message's marking is correct when it
  arrives, was nowhere stated.
- The terms were a subsection of the concept of operations, although the
  requirements used them too. A term shared by two documents belongs to
  neither.
- Each story's example was checked by a person walking it (`tools/walk.py
  Restricted 7`, observe `pass: Restricted 7`), which produced evidence for
  conformance and, in the same sitting, for validation. The two questions
  were answered by one activity, and Lecture 01 had to spend a paragraph
  keeping them apart.
- Nothing recorded where the stories came from. If the security officer had
  disputed US-2, there was no record of what they had said.

None of these is a defect of the product; A0's guard does what A0's stories
say. They are defects of the document as a record of intent, and they are the
kind a concept of operations exists to prevent. A1 fixes each, and the fixes
are the format changes this lecture explains.

## What a concept of operations is for

A **concept of operations** is a specification of purpose. It says what the
system is for, who uses it, what those users can observe of its behavior, and
the scenarios of its use, written so that a person who is not a programmer
can read it and say whether this is the system they want. It does not say how
the system is built, and it does not say anything a user could not observe:
not the language, not the modules, not what a function returns.

That restriction is what makes the document useful, for two reasons that
pull in the same direction.

The first is validation. Lecture 01 said that intent has no artifact: what
the stakeholders want lives in their minds, and the only way to consult it is
to ask them. The concept of operations is the document we ask them about. A
stakeholder cannot say whether `filter_message` should return `None`; they
can say whether "a message marked Critical never leaves" is what they want.
Validation, the judgment VAL, is therefore *performed on* the
concept of operations, by a stakeholder reading its scenarios or walking
them on the running system, and every other specification is validated
*through* it: a requirement is right if it says what a validated story says.
The glossary entry for validation puts it this way: the judgment covers every
specification derived from the concept of operations, but only one document
is the one a person signs.

The second is governance of the family. Every other specification is derived
from the concept of operations or must agree with it. The requirements of
A1 derive from its stories; the scenario file is its examples as data; the
glossary defines the terms its stories use. When two documents disagree, the
concept of operations wins, because it is the one the stakeholders agreed
to. That is why Lecture 03's audit has a check for the agreement of each
requirement with its story, and why the first thing an agent is told to read
in this repository, after the judgments and the procedures, is the glossary
and then the concept of operations.

What the document leaves open is as important as what it fixes. It leaves
open everything a user cannot observe, which is where the realization is
free. A0's scope section said that transport, authentication, and the
assignment of security levels are outside the boundary; that sentence is a
decision about what the document will not say, and it is as much a part of
the specification as the stories are.

Two practical consequences for writing one. The document is written in the
stakeholders' words wherever it can be, because the stakeholders are the
ones who will be asked whether it is right, and a sentence they recognize is
one they can judge. And it is kept implementation-independent not as a
stylistic preference but because a sentence that names the implementation
is a sentence a stakeholder cannot validate and a sentence that constrains
the realization without anyone having decided to.

**Contextual text and identified clauses.** As in A0, only some of the
document is made of identified clauses: the user stories, each with an
identifier and a verification method, are the clauses that the conformance
report and the trace matrix have rows for. The purpose, the scope, the
assumptions, the user-category descriptions, and the deferred wants are
contextual specification text: they are part of the specification, they are
audited with the clauses (ConOps-SQ-1 says so), and they have no row of
their own. The distinction matters for the tooling, which reads clause headers and
nothing else, and for the audit, which must read everything.

## The format, section by section

A1's `specs/conops.md` has six sections, and two companion files carry what
A0 kept inside the document: the glossary (`specs/glossary.md`) and the
scenario file (`specs/scenarios.json`). Here is each section, what it is for,
and what changed from A0.

### 1. Purpose

> An organization keeps a protected enclave whose systems produce messages
> of differing sensitivity, and it needs some of those messages to reach a
> less trusted network outside the enclave. The message guard sits on that
> boundary and decides, one message at a time, whether a message may leave.
>
> In this version the decision rests on one thing, the security level marked
> on the message: a message marked Critical never leaves, and every other
> message leaves exactly as it arrived. The guard does not inspect the
> payload (E-1). This version establishes the guard itself, and the way its
> behavior is specified and shown to hold; what later versions may add is
> recorded in section 5 as deferred wants, not promised here.
>
> Agreed by the security officer and a message sender on 2026-10-22; their
> words are in `reference/elicitation.md` (E-1, E-3).

Three changes from A0. The sentence that the guard does not inspect the
payload is new, and it carries a citation, `(E-1)`, to the entry of the
elicitation record where the security officer said so. The promise about
later versions is gone, replaced by a pointer to the deferred wants. And the
statement ends with a line saying who agreed to it and when. That line is
not decoration. The purpose statement is the closest written thing to intent
that the repository holds, and a reader who wants to know whether it is the
stakeholders' purpose or the author's guess needs to be told.

### 2. Scope and system boundary, with assumptions

The boundary paragraph is A0's, with two sentences added: that each call is
independent and the guard keeps no state between messages, and that an input
which is not a message as the glossary defines it is outside the boundary,
with how a realization signals that it did not accept it left unspecified.

New in A1 is a subsection of **assumptions**:

> Each assumption is an obligation of the organization that deploys the
> guard, not a requirement on this library. Establishing that an assumption
> holds needs evidence about the deployment, not tests of the guard.
>
> - **A-1** A message's security level is assigned before the message
>   reaches the guard, and the guard trusts the marking (E-5).
> - **A-2** Every message that leaves the enclave is routed through the
>   guard; the guard cannot prevent a bypass.

Lecture 01 introduced environmental assumptions in a paragraph and said it
would not pursue them. A1 gives them a section, because elicitation produced
one (A-1 is the security officer's answer to the question of who is
responsible for the marking) and because the audit of the draft found what
happens when an assumption is not labeled: the agent that rewrote the
requirements had turned A-2 into a requirement, "The guard shall receive
every message that leaves the enclave," with a verification method of
*test*. No test of the guard can establish that. The section exists so that
an obligation of the deploying organization has a place to be written down
that is not the requirements, and so that the audit has a sentence to point
at when one leaks.

Note what the section does not contain. A first draft had a third
assumption, that the guard handles one message at a time and keeps nothing
between messages. The ad-hoc agent audit observed that this is a property of
the guard, not of the deployment: it can only be established by examining
the guard. The ruling moved the sentence into the boundary paragraph, where
it now sits. An assumption is defined by who is obliged to make it true, and
a sentence about the guard's own behavior is not one.

### 3. User categories

The two categories of A0, each with a line saying what the user of that
category observes. The lines are sharper than A0's, and each cites the
elicitation entry that sharpened it: the message sender "observes nothing
when a message is dropped (E-3)"; the security officer "in this version has
no record of what was dropped (E-2; deferred want D-1)". And a sentence that
was not in A0:

> The developer who builds the guard is not a user category (E-4); the
> developer's roles are in `CLAUDE.md`, and the judgments the developer's
> work is held to are in `process/judgments.md`.

The sentence answers a question the first version left open. A user
category is a role whose holder can be asked whether the system is the one
they want, and whose stories therefore need a sign-off. The developer is not
such a role. Saying so keeps the sign-off list from growing a signature that
answers no validation question.

### 4. User stories

Each story is a clause. Its header has more fields than A0's, and each field
has a reader:

```
**US-2** · Method: test · Scenarios: SC-3, SC-4 · User category: message sender · Validated by: walkthrough (human) · Source: E-3
```

The identifier is what reports cite. `Method: test` says how the story's
behavior is verified: in A1, by the scenario tests, which is a change from
A0's `walkthrough (human)` that the fixtures section below explains.
`Scenarios` names the entries of the scenario file that are this story's
examples as data. `User category` says whose story it is. `Validated by`
says how the question whether the story is *right* is decided: a walkthrough
with a stakeholder of that category, under ConOps-VAL-1, followed by the
sign-off. `Source` names the elicitation entry whose words the story is
written from.

Two of those fields answer questions that Lecture 01 could only gesture at.
`Method` and `Validated by` are two fields because they answer two
questions, whether the realization does what the story says and whether the
story says what the stakeholder wants; in A0 both were answered by the same
walkthrough, and the lecture had to explain that one sitting produced two
kinds of evidence. `Source` is the field that makes a story checkable
against something other than itself.

The story's text is in the stakeholder's words, followed by its example:

> As a message sender, when I send a Restricted message, I expect it to
> arrive unchanged, because in this version a Restricted message is allowed
> to leave and its payload is neither inspected nor altered (E-1).
>
> Example: the guard is given (Restricted, 7); it outputs (Restricted, 7).
> Given (Restricted, 150), it outputs (Restricted, 150).

The second example is new in A1. It exists because the security officer, in
answering E-1, mentioned that they might later want "large Restricted
payloads cut down before they go out." That is a deferred want, D-2. The
example with payload 150 pins down that in *this* version nothing is cut
down, so that when D-2 is eventually built, the story, the example, and the
scenario derived from it will all have to change together, visibly.

A note on the reason clause, "its payload is neither inspected nor altered
(E-1)". The story is the sender's, and its `Source` is E-3, the sender's
answer. But the fact it relies on, that the payload is not inspected, was the
security officer's answer. The citation inside the sentence says so. The
audit before the second commit of A1 found that an earlier draft had listed
both entries in the `Source` field, and ruled that a story's source is the
stakeholder whose story it is, with other stakeholders' answers cited where
the story uses them. Small, but it is the kind of thing a format decides
once so that nobody has to decide it again.

### 5. Deferred wants

> Heard during elicitation and recorded here so that they are neither
> forgotten nor promised. No requirement, story, or scenario of this version
> derives from any of them.
>
> - **D-1** A record of every dropped message, observable by the security
>   officer (E-2).
> - **D-2** Changing the payload of a Restricted message before it leaves,
>   for instance cutting a large payload down (E-1).
> - **D-3** A change to whether Restricted or Public messages are dropped;
>   that a Critical message is dropped does not change (E-1).

This section replaces A0's "Later versions will" sentence. The difference is
not the list, which is nearly the same; it is the status of the items. Each
want names who wants it, through its citation, and the section's preamble
says what the status *deferred* means: nothing in this version derives from
it. The audit checks that (procedure Audit, item C-12), and the check has
teeth. The
draft that the audits examined contained the sentence "the filter shall drop
the message and shall record the drop" in REQ-1, which is D-1 leaking into a
requirement one version early. Both audits found it; the ruling deleted the
clause and left D-1 where it was.

D-3's wording also changed under audit. A draft said "a change to which
security levels are stopped", which includes Critical; the security officer
had said, in E-1, "Critical never leaves, full stop." A deferred want is
still a sentence the stakeholders have to recognize.

### 6. Sign-off

A pointer to `reports/validation.md`, where the walkthrough decisions and
the signatures are. The section is one sentence; the validation section
below says what the file holds.

### The glossary, promoted to a document

A0 defined its six terms in a subsection of the concept of operations. A1
moves them to `specs/glossary.md`, adds the terms elicitation produced, and
makes the glossary a specification of its own, the kind the course's catalog
now lists as entry 16. The reason is Gloss-SQ-1, glossary discipline: every
domain term used in any specification is defined exactly once, in the
glossary, and used only in that sense, and no other specification defines a
term. With four specifications sharing the vocabulary, a term defined inside
one of them is a term the others cannot be audited against.

Two entries show what the glossary is for. The entry for *drop* says that
nothing else happens when a message is dropped: no record is kept, and the
sender is not told, with citations to the entries where each stakeholder
said so, and it notes that "a stakeholder may say *stopped*", which is the
word the security officer actually used. The entry for *payload* says that
the specification does not constrain how a programming language represents
integers, and points at the elicitation record's list of questions that were
not asked, where the reason is given. A glossary entry is where a decision
about a word is recorded so that the next reader does not reopen it.

### A table of the changes

| A0 | A1 | The problem the change answers |
|---|---|---|
| terms inside the concept of operations | `specs/glossary.md`, a specification of its own; Gloss-SQ-1 | a term shared by several documents was owned by one of them |
| "Later versions will sanitize, record, change the policy" | section 5, deferred wants D-1 to D-3, each with its source | a promise with no owner; a want that could leak into a requirement |
| the deployment assumption inside the purpose | section 2.1, assumptions A-1 and A-2, labeled as the deploying organization's obligations | an obligation on the environment could be mistaken for one on the system |
| a story's example checked by a person | `specs/scenarios.json`, run by `tests/test_scenarios.py`; the story's method is *test* | behavioral evidence that cost a person's attention every time |
| no record of where a story came from | a `Source` field; `reference/elicitation.md` | a disputed story had nothing to be checked against |
| one walkthrough for conformance and validation | `Method` and `Validated by` as separate fields; `reports/validation.md` for the decision | two questions answered by one activity |
| the purpose statement, unattributed | "Agreed by ... on ...; their words are in ..." | no way to tell the stakeholders' purpose from the author's |
| no statement of who is not a user | "The developer ... is not a user category" | a signature list that could grow for no reason |

## How a concept of operations is obtained: elicitation

Everything above describes a document. This section is about where its
sentences come from.

**Elicitation** is the activity of asking the stakeholders what they want
and turning the answers into an engineering document. The word is older than
agentic development and the activity is unchanged by it: someone who knows
the domain is asked questions by someone who is writing the specification,
and the answers are recorded. What agentic development changes is who asks.
An agent can read the whole repository, notice what the current document
does not settle, and put questions to a stakeholder faster and more
systematically than a person can, which is useful, and it can also put far
too many of them, which is the failure mode that shaped A1's procedure.

### What goes wrong

The course's earlier material used a skill called `grill-me`, whose
instruction to the agent begins "Interview me relentlessly about every
aspect of this plan until we reach a shared understanding." Students who
used it on their projects reported being overwhelmed: the questions did not
stop, they were not ranked, many of them could have been answered by reading
the repository, and the answers vanished into the chat transcript. That
skill was written for a developer stress-testing their own design, where an
unbounded interview is what the developer asked for. Pointed at a
stakeholder-facing document it has three defects, and each is a defect of
the procedure, not of the agent.

First, no bound. A stakeholder's attention is the scarce resource, and a
procedure that spends it without limit will be abandoned. Second, no
ranking. A question about whether the guard should check the marking changes
the system boundary; a question about the wording of a definition changes a
sentence. Asked in arbitrary order, the second kind crowds out the first.
Third, no record. An answer that lives in a chat transcript cannot be cited
by the story it produced, cannot be audited against the story, and cannot be
shown to a stakeholder who later asks "did I say that?"

There is a fourth failure, subtler than the others: the interviewer writes a
decision into the document that nobody gave. An agent that notices a gap and
fills it with a sensible default has done exactly what the document exists
to prevent. A guess written into a governing document becomes a requirement
nobody decided.

The sidebar [Two elicitation skills, read side by
side](sidebar-elicitation-grill-me-vs-elicit.md) sets the two skill
definitions next to each other, row by row, and says what was done in
writing `/elicit` so that a stakeholder can sit through a session with it.

### The procedure

A1's elicitation is a procedure, `Elicit` in `process/procedures.md`,
packaged as the skill `/elicit` (`.claude/skills/elicit/`), which the
developer starts with the form to elicit as its argument (`/elicit conops`). It is modeled on the `clarify` step of Spec Kit,
a specification-driven development toolkit the course meets later, which
asks at most five questions and encodes the answers into the specification.
The course's version keeps that shape and changes three things: the
categories it scans are the parts of a concept of operations; each question
is addressed to a named user category; and the answers go to a record under
`reference/`, in the stakeholders' words, rather than into the
specification.

The steps, as the skill performs them:

1. **Read before asking.** The current concept of operations, the glossary,
   the existing elicitation record, and the procedures file. A question the repository
   answers is answered by reading it, not by asking. The record of A1's
   session has a closing section, "Not asked", listing the questions the
   skill considered and excluded, with the reason for each: whether
   Restricted messages should also be stopped (answered by US-2 and the A0
   sign-off); what the guard does with a marking outside the three (answered
   by REQ-0); who agreed to the purpose (the A0 sign-off); and so on.
2. **Scan the document** against the form's fixed list of eight categories
   (`forms/conops.md` in the skill): purpose, scope and boundary,
   assumptions, user categories, stories, terms, wants and non-goals,
   validation. Each is rated Clear, Partial, or Missing. For
   A0's document, three runs of the skill agreed that assumptions, user
   categories, and wants were Partial and the rest Clear.
3. **Build a queue** of at most five questions from the Partial and Missing
   categories, ranked by how much the answer would change the document and
   how uncertain the answer is. Each must be answerable with a letter or a
   few words. Questions about implementation, technology, or task order are
   excluded; a stakeholder is not the person to ask them.
4. **Ask one question at a time**, addressed to a user category, in a fixed
   form: a full question, one sentence saying why it matters, the
   recommended option first with its reason, a table of options, and a line
   saying how to reply. The stakeholder answers with a letter, or "yes" to
   take the recommendation, or a short answer.
5. **Record, then apply, after each accepted answer.** An entry is appended
   to `reference/elicitation.md` under the next identifier `E-n`, with the
   question, the options, the recommended one, the answer *verbatim*, who
   gave it in which role, and the consequences. Then the answer is applied to
   the part of the document it affects, a sentence of the purpose, an
   assumption, a story, a deferred want, a glossary entry, replacing
   contradicted text rather than adding beside it.
6. **Report and stop.** The number of questions, the sections touched, a
   coverage table of the eight categories, and the next steps: the audit,
   then the validation walkthrough and the sign-off.

The procedure's cap is five questions. That number is not derived from
anything; it is a budget, chosen because a session of five well-chosen
questions is one a stakeholder will sit through, and because the ranking
step means the five are the ones whose answers change the most. A sixth
question, if one is needed, is a second session.

### The session that produced A1

The record of A1's elicitation, `reference/elicitation.md`, has five entries.
Here is one in full:

```
### E-3 · to the message sender

Question: When a message you send is stopped at the guard, do you want to be
told that it was stopped?
Why it matters: "yes, in this version" adds a story and changes what the
guard gives back for a stopped message, "later" is recorded as a deferred
want, and "no" is recorded so that no notification is ever required of the
guard on the sender's behalf.
Options: A. no; a stopped message simply does not arrive (recommended) · B.
not in this version, but eventually · C. yes, in this version · Short.
Answer (verbatim): "A. No. It just doesn't arrive, and I may not even know.
What I care about is that anything I send that is allowed out comes out
exactly as I sent it, whatever the number in it, Public or Restricted."
Answered by: a message sender (role played by the build agent), 2026-10-22
Consequences: the message sender's "observes" line (observes nothing when a
message is dropped); glossary entry *drop* (the sender is not told); US-1
and US-2 reworded in the sender's words, with "whatever its payload" and the
second example of each.
```

Read the consequences line against the document. The sender's "observes"
line in section 3 now ends "observes nothing when a message is dropped
(E-3)". US-1 now says "whatever its payload", which is the sender's
"whatever the number in it". The glossary's *drop* entry says the sender is
not told. Every one of those sentences can be followed back to this entry,
and the entry quotes the sender rather than paraphrasing them, so that a
reader who doubts a sentence can see what was actually said.

The five questions, condensed:

| Entry | To | Asked | Answered | What it changed |
|---|---|---|---|---|
| E-1 | security officer | whether "Critical never leaves" is permanent or a changeable policy setting | permanent; the marking alone decides; the payload is not inspected; a later wish to cut large Restricted payloads down | the purpose statement; US-2 and US-3; deferred wants D-2 and D-3 |
| E-2 | security officer | which of the three "later versions will" items are things the officer wants | all three, deferred; "don't build any of it now" | the promise removed; section 5; the officer's "observes" line |
| E-3 | message sender | whether the sender wants to be told of a drop | no; a dropped message does not arrive | the sender's "observes" line; *drop*; US-1 and US-2 |
| E-4 | security officer | whether anyone else is a user of the guard | no one else; the developer is not a user | the sentence in section 3 |
| E-5 | security officer | whether the guard should trust the marking it is given | yes; marking before arrival is the organization's responsibility | assumption A-1; *security level* |

Two things about this session are worth stating plainly, because the
record states them. The questions were generated by the skill, and the
answers were given by the person who built A1, playing both stakeholder
roles according to a script, as the instructor played both roles for A0's
sign-off. The record says so in its header, and says that a live session
with the instructor, or with two different people, supersedes it. A record
that says who answered is a record that can be replaced by a better one; a
document that absorbed the answers silently could not be.

### The record is reference, not specification

`reference/elicitation.md` lives under `reference/`, not `specs/`. The
glossary's definition of *reference* is "material that informs
specifications but is not one: sketches, research notes, the elicitation
record. Not audited; no judgment is about it." The distinction has
consequences.

The record is not audited, because it is not supposed to be consistent,
complete, or unambiguous: it is what people said. A stakeholder's "I'd like
one eventually; not needed for this version" is not a clause, and trying to
make it one would destroy the information it carries, which is exactly its
hedge. The specification is where that hedge becomes a status (*deferred*)
that the audit can check.

The record is cited, not copied. A story's `Source` field names an entry;
the audit's derivation check (item C-8 of the checklist) reads the entry to
see whether the story is in the words of a stakeholder of its own category.
When the two disagree, the story is wrong, not the record.

And no judgment clause is about it. Changing the record changes nothing in
the assurance report; changing the concept of operations does. That is the
operational meaning of "reference": the development state does not depend
on it.

### Evaluating a procedure that has no exit code

The `/audit-spec` skill of the next lecture is a verifier, and a verifier is
checked by giving it inputs it must fail on. `/elicit` is a procedure, not a
verifier; it produces a document rather than a verdict, so the question of
whether it works is answered differently: run it several times on the same
document and compare what it asks. A1 did that, three times on A0's concept
of operations, before the real session. All three runs queued five
questions; all three asked about the marking assumption, the drop, the
deferred wants, and the user categories; the fifth question varied (the
transport's obligation, the permanence of the Critical rule, who assigns the
marking). No run asked about terms, even when it rated the Terms category as
Partial: all three treated a missing definition as the writer's job rather
than a stakeholder's. And no run asked about the payload's domain, because
all three excluded the question as answered by REQ-0, with the residue (how
a programming language represents an integer) an implementation matter. The
catalog page for the skill, `tooling/skill-elicit.md`, records the
evaluation and one proposed change to the skill that the evaluation
suggested. The lesson transfers: a procedure packaged as a skill is checked
by running it and reading what it does, and the runs are kept beside it.

### The procedure, written down

`Elicit` is one of the two procedures in `process/procedures.md`, the file
A1 adds beside the judgments. Condensed:

| Field | |
|---|---|
| Purpose | obtain or revise a stakeholder-facing specification from its stakeholders, so that it says what they intend and its VAL clause can be evaluated against it; an authoring procedure, not an evaluation |
| Serves | ConOps-VAL-1 (the document it produces is what the stakeholders sign); the SQ clauses (its answers settle terms, assumptions, and wants) |
| Run by | an agent running `/elicit [form]`, which the developer starts; the stakeholders answer; the developer reviews the resulting change |
| Steps | read; scan by the form's taxonomy and queue at most five questions by impact times uncertainty; ask one at a time, addressed to a user category, with options and a recommended answer; record each answer verbatim under an E identifier, then apply it to the one part it affects, citing the identifier; report |
| Per-form parts | the taxonomy, `forms/conops.md` in the skill |
| Stops | after five questions, when the queue is empty, or when the stakeholder says "done"; never writes a decision nobody gave; never touches the requirements, the scenarios, the tests, or the code; the next step is the audit |
| Record | `reference/elicitation.md`: reference material in the stakeholders' words |

A procedure is new in A1: it says how an activity is done and where it
stops, once, for any form it applies to, with the parts that depend on the
form kept with the skill that packages it. Lecture 01's judgments file said
what each claim is and how it is evaluated; a procedure says how an activity
that produces or evaluates an artifact is carried out. Neither says *when*
the activity must run: nothing in A1 does. The build ran the audit before
every commit that changed a specification as a practice, and A2 turns such
practices into rules, with a trigger and a failure clause, which is the
layer this version deliberately leaves out.

## What we do with it, first: validation

The concept of operations is validated by its stakeholders, and in A1 the
clause that says so, ConOps-VAL-1, was amended to say what its record holds.

Its *Evidence* field now names a validation record: per user category, who
walked, in which role, when, against which realization state, which stories,
with which scenario inputs, what was observed, and the decision to sign or
to withhold the signature, with its reason; and, as in A0, the sign-off
naming the version, from a stakeholder of each user category. The record is
`records/validation.md`. Its security officer's section:

| Story | Scenarios | Commands | Observed | Decision |
|---|---|---|---|---|
| US-3 | SC-5, SC-6 | `walk.py Critical 100`; `walk.py Critical 0` | `drop`; `drop` | the story says what I want: nothing marked Critical leaves, whatever its payload |
| Deferred wants D-1 to D-3 | read, not walked | — | — | they are mine, recorded as deferred, and not promised here; I sign for A1 with them deferred |

The sign-off below the tables names version A1 and states the scope: "The
three deferred wants are mine and are not promised in this version."

Compare this with A0's walkthrough record. A0's table had the same
commands and the same observed outputs, and its last column was headed
*Finding*, with the value "as the story expects". That column answered a
conformance question: does the running guard do what the story says? A1's
last column is headed *Decision*, and it answers a validation question: is
this the story I want? The behavioral question is still answered, but not
here; it is answered by the scenario tests, which the next section
describes. The walkthrough in A1 has one job, and the clause's *Evaluated by* field
says it in a sentence: observing the expected output is not the decision;
the decision is whether the story describes what the stakeholder wants.

Two things follow that the assurance report shows. At A1's first commit,
after the concept of operations had been revised but before the stakeholders
had walked it, the report compiled for that commit says ConOps-VAL-1 **does
not hold**: the only sign-off named version A0, and the document had changed
in every section (`git show a1-specs:reports/assurance-report.md` in the
replayed history). The four other judgments hold in the same report. Three
commits later, at `a1`, the row holds, and its provenance says what the
evidence is: a walkthrough and a sign-off by a stand-in for the
stakeholders, which the instructor's own session supersedes. A row that
names a stand-in is weaker than one that names the stakeholder, and the
report is where that is written down.

The second thing is the case Lecture 01 constructed for A0, now with more
machinery around it. Suppose the security officer, walking US-2 at this
validation, says that a Restricted message with a payload above 100 must not
leave. Every scenario passes, including SC-4, which encodes a Restricted
message with payload 150 leaving unchanged. The audit found nothing; the
trace matrix has no findings; coverage is complete. The officer declines to
sign. ConOps-VAL-1 does not hold, and nothing else in the report moves,
because nothing else is wrong: the repository is a consistent realization of a story
the stakeholder does not want. In A1 the resolution is a sign-off scoped to
the version, with the want recorded as deferred, which is what D-2 is. The
unscoped resolution, where the requirement actually changes, is the change
request of version A3.

## What we do with it, second: system tests from the stories

A story carries an example: the guard is given (Restricted, 7); it outputs
(Restricted, 7). In A0 a person checked the example by hand. In A1 the
examples are data, the data is run by a test, and the test cites the story.
This section follows one example all the way from the stakeholder's sentence
to the rows of two reports, and then says what the arrangement establishes
and what it does not.

### The scenario file

`specs/scenarios.json` holds the six examples of the three stories:

```json
{
  "specification": "Acceptance scenarios for the message guard, derived from the user stories in specs/conops.md. Any realization, in any language, must reproduce them. ...",
  "version": "A1",
  "assumes": "A message is a security level and an integer payload (REQ-0). The guard is the filter stage alone (glossary: filter); the payload is not inspected (E-1).",
  "governance": "Never edited to make a test pass. A scenario that looks wrong is a gap about the pair (scenario, story): report it to the audit (procedure Audit) and rule on it there.",
  "loader": "tests/test_scenarios.py runs every scenario and cites the story it derives from (Scen-CONF-1).",
  "scenarios": [
    {
      "id": "SC-1",
      "derived_from": "US-1",
      "role": "message sender",
      "input": {"level": "Public", "payload": 42},
      "expected": {"level": "Public", "payload": 42}
    },
    {
      "id": "SC-2",
      "derived_from": "US-1",
      "role": "message sender",
      "input": {"level": "Public", "payload": -3},
      "expected": {"level": "Public", "payload": -3},
      "note": "E-1: the payload is not inspected; a negative payload leaves like any other."
    },
    ...
    {
      "id": "SC-5",
      "derived_from": "US-3",
      "role": "security officer",
      "input": {"level": "Critical", "payload": 100},
      "expected": null
    }
  ],
  "blind_spots": [
    "Only the listed payload values are checked; the requirements are universal over integers.",
    "No scenario sends a malformed message; REQ-0 is verified by unit tests, not by scenarios."
  ]
}
```

Each scenario has an identifier, the story it derives from, the role of the
stakeholder whose story it is, one input message, and the expected output,
where `null` means that nothing comes out. The file also says what it
assumes, how it is governed, which program runs it, and what it does not
cover. A stakeholder can read every line of it: "Restricted 150 in,
Restricted 150 out" is the officer's own answer to E-1, written as data.

The course calls this kind of file a **fixture**, or a **scenario file**: a
set of scenarios with expected outcomes that any realization of the
specification, in any language, must reproduce. The catalog of
specification kinds has an entry for it. Three properties define it.

It is **values only**. A scenario says which message goes in and which
comes out. It does not say which function is called, how the message is
constructed, or what "nothing" looks like in a programming language. Those
bindings belong to the loader, below, and to each realization. The file
survives a change of language unchanged; the loader is rewritten.

It is **derived from the stories**, and each scenario says from which. The
scenarios are the stories' examples, and nothing else: a scenario that the
story's wording does not cover is a gap, not an extra test.

It is **governed on the specification side**. The `governance` field says it:
never edited to make a test pass. When a scenario fails, there are three
candidates for what is wrong: the realization, the story, or the scenario's
expectation. The first is fixed by changing the code. The second and third
are gaps about the pair (scenario, story), and they go to the audit for a
ruling, not to whoever is editing tests that afternoon. This is the
difference between a fixture and a test suite: a test suite is a
realization, edited under the test discipline; a fixture is a specification,
edited by amendment.

### Why two examples per story

US-1 has SC-1 (Public, 42) and SC-2 (Public, -3). US-2 has SC-3 (Restricted,
7) and SC-4 (Restricted, 150). The second scenario of each pair is new in A1
and exists because of something a stakeholder said. SC-2 pins down that a
negative payload leaves like any other, because the officer said the payload
is not inspected and the sender said "whatever the number in it". SC-4 pins
down that a large payload is not cut down in this version, against the
officer's deferred want.

Behind that choice is a general point about what a scenario can establish. A
story is universal: *every* Public message arrives unchanged. A scenario is
one instance. A set of scenarios therefore under-approximates the story:
every behavior the set checks is one the story demands, and the story
demands behaviors the set never checks. The `blind_spots` field says so for
this file. Choosing which instances to include is the work of thinking about
which inputs the story treats alike (every Public message, whatever its
payload) and which boundaries matter (a negative payload; a large one), and
of writing one scenario per class and per boundary that a stakeholder has
mentioned. The classical name for this is equivalence partitioning, and the
next lecture's requirements will give the same idea a sharper form.

### The loader: how the file is processed at the testing level

A scenario file does nothing by itself. `tests/test_scenarios.py` is the
program that turns it into tests in this realization's language and test
framework:

```python
"""Evidence for the user stories: every acceptance scenario of specs/scenarios.json, run as a test.
...
"""

import json
from pathlib import Path

import pytest

from guard import Message, SecurityLevel, filter_message

SCENARIOS = Path(__file__).resolve().parent.parent / "specs" / "scenarios.json"


def _cases():
    data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    for scenario in data["scenarios"]:
        yield pytest.param(scenario, id=scenario["id"], marks=pytest.mark.req(scenario["derived_from"]))


@pytest.mark.parametrize("scenario", list(_cases()))
def test_scenario(scenario):
    given = scenario["input"]
    out = filter_message(Message(SecurityLevel(given["level"]), given["payload"]))
    expected = scenario["expected"]
    if expected is None:
        assert out is None
    else:
        assert out is not None
        assert (out.level.value, out.payload) == (expected["level"], expected["payload"])
```

Walk through what happens when pytest runs.

**At collection.** Before any test runs, pytest imports the module and
evaluates `list(_cases())`. The function reads the file and yields one
parameter set per scenario. Two things are attached to each: an *id*, the
scenario's identifier, so that the test case is named
`test_scenario[SC-2]` and a failure names the scenario; and a *marker*,
`req("US-1")` for SC-1 and SC-2, which is the same `@pytest.mark.req`
citation that Lecture 01's unit tests carry, attached per case through
`pytest.param` because the clause cited differs from case to case. The
conformance plugin collects these markers exactly as it collects the unit
tests' markers; it does not know or care that they came from a file. One
test function has become six test cases, each citing its story.

**At execution.** For each case, the test builds the input message through
the package's public interface, `Message(SecurityLevel(...), payload)`, which
is the binding the scenario file deliberately left open; calls
`filter_message`; and compares. A `null` expectation asserts that nothing
came out. Any other expectation asserts that something came out and that
its level and payload equal the expected values. The comparison is by value,
not by object identity, because the glossary's *unchanged* is defined as
"the same security level and the same payload"; the question Lecture 01
raised about identity is settled here by not asking it.

**What the loader must not do.** It must not skip a scenario it cannot
parse (collection fails instead, which Code-RQ-1 catches before any
evidence is produced), must not edit the file, and must not add a scenario
of its own. A loader is the thinnest possible layer between a data file and
a test framework, and its catalog page, `tooling/scenario-loader.md`, lists
the five requirements it meets. The loader is one of ten tools the catalog
documents this way, with the goal, the requirements, the prompt, the review
points, and the cases each must fail on; the sidebar [Tooling as
engineering](sidebar-tooling-as-engineering.md) says why those pages exist
and how to read them, since no lecture time is given to building the tools.

### What the reports say

Run `tools/evaluate.sh`, and two generated reports now carry the stories. The
conformance report, `reports/conformance.md`, has a row per clause; the
story rows, which in A0 pointed at the walkthrough file, now list the citing
scenario tests:

| Clause | Specification | Method | Tests citing it | Status |
|---|---|---|---|---|
| US-1 | `conops.md` | test | `test_scenarios.py::test_scenario[SC-1]`<br>`test_scenarios.py::test_scenario[SC-2]` | pass |
| US-2 | `conops.md` | test | `test_scenarios.py::test_scenario[SC-3]`<br>`test_scenarios.py::test_scenario[SC-4]` | pass |
| US-3 | `conops.md` | test | `test_scenarios.py::test_scenario[SC-5]`<br>`test_scenarios.py::test_scenario[SC-6]` | pass |

The requirements-coverage line reads "7 of 7 test clauses have passing
evidence": the four requirements and the three stories. A1 adds a clause
for the new form, Scen-CONF-1, which says in so many words that a loader
runs every scenario of the file as a test citing the story it derives from,
so that a story with no scenario would show as **no evidence** and fail the
run, like a requirement with no test.

The trace matrix, `reports/trace-matrix.md`, which the next lecture
introduces properly, has a forward table whose first row is:

| Story | Source | Requirements | Scenarios | Tests citing the story | Tests citing its requirements |
|---|---|---|---|---|---|
| US-1 | E-3 | REQ-3 | SC-1, SC-2 | `test_scenarios.py::test_scenario[SC-1]`<br>`test_scenarios.py::test_scenario[SC-2]` | `test_filter.py::test_public_passes_unchanged` |

Read the row left to right and the whole chain of this lecture is in it: a
stakeholder's words (E-3), the story written from them (US-1), the scenarios
derived from the story's examples (SC-1, SC-2), the tests that run them, and,
in the last two columns, the two kinds of evidence the story now has: its
own scenarios and the unit tests of the requirement derived from it. The
tool that builds this table also checks that every scenario is listed by the
story it derives from, and that every story lists only scenarios that exist.

### The climb, and what it leaves behind

In A0 the three stories carried the method *walkthrough (human)*, and their
evidence was a person's observation. In A1 they carry *test*, and their
evidence is the loader's cases. Lecture 01 named this movement the verifier
ladder: a check that begins with a person can, when the procedure turns out
to be decidable, end as a program, and then the clause is mechanical and can
be evaluated at every request, and at A2 behind a gate. The stories' examples were always decidable; what A1
adds is the artifact that makes them so, the scenario file, and the loader
that runs it.

Two things do not climb. The validation of the story stays with a person,
which is why the `Validated by` field still says *walkthrough (human)* and
why the sign-off is kept after the tests exist. And the question whether the
scenarios are the *right* instances of the story, whether the file's blind
spots are acceptable, is a judgment that the audit makes and no test can.

ConOps-CONF-1, which in A0 required a walkthrough record for every story
with method *walkthrough*, now has no story in scope, and A1 retires it: the
judgments file's changelog says so, and the identifier is not reused. A
clause that applies to nothing is retired rather than kept, because a
reader of the file should find only clauses that say something about the
tree in front of them; when A2 brings review clauses, they bring a clause of
their own.

### Independence: what a person-authored file catches

The scenario file was written from the stakeholders' words, on the
specification side, before anyone looked at the realization. That gives it a
property the unit tests do not have: it does not share the realization's
reading of the specification.

Here is the demonstration from the README (sabotage 7). Suppose the agent
that wrote `filter.py` read "unchanged" as "with the payload normalized to a
non-negative number", and wrote its unit test with the same reading. The
code's last line becomes

```python
    return Message(message.level, abs(message.payload))  # REQ-2, REQ-3 (misread)
```

and the assertion of `test_restricted_passes_unchanged` becomes

```python
    assert filter_message(message) == Message(message.level, abs(message.payload))
```

The unit test passes: the test and the code agree, because the same mind
wrote both. Run the evaluations:

```
FAILED tests/test_scenarios.py::test_scenario[SC-2] - AssertionError
conformance: US-1: FAIL
conformance: FAIL, see reports/conformance.md
1 failed, 28 passed
```

SC-2 sends (Public, -3) and expects (Public, -3), because the sender said
"whatever the number in it". The scenario was not written by the mind that
misread the word, so it does not share the misreading. This is the simplest
form of what the course calls **independence**: the verifier of a clause is
not the author of the realization it verifies. In A1 it is a property of
where the file came from. Later versions make it a rule.

### What the scenarios do not do

A passing scenario set establishes that the realization reproduces the
listed instances of the stories. It does not establish anything about
inputs no scenario sends, which is what the `blind_spots` field is for, and
it does not establish that the listed instances are the right ones. Two
consequences are visible in A1.

The first concerns Lecture 01's coverage sabotage. In A0, adding the branch
`elif message.payload < 0: return None` before the final return left every
test passing and dropped branch coverage below 100 percent; the
structural-coverage conjunct caught it. In A1 the same edit is caught
earlier and differently: SC-2 sends a negative payload, the scenario fails,
and coverage stays at 100 percent because the new branch was exercised. To
see the coverage conjunct alone one has to write a branch no scenario
reaches, such as `payload < -1000`: every clause is still cited, every test
passes, and coverage drops to 94 percent. The point is not that one check
has replaced the other; it is that the stakeholder's example reached a bug
before the coverage tool did, and the coverage tool still catches what no
example reaches.

The second concerns the file's future. When version A2 adds the `sanitize`
stage, a Restricted message with payload 150 will no longer leave unchanged,
and SC-4 will be wrong. The right sequence is then: the story changes, with
the stakeholders; the scenario changes, as an amendment that cites the
story's change; the loader does not change at all. If instead a developer
edits SC-4 to make the new code pass, the file has stopped being a
specification. The `governance` field, and from version A3 a rule of the
change-control style, exist to keep that from happening quietly.

## What this lecture leaves to the next

A concept of operations has a third use, and it is the one this lecture has
only pointed at: the requirements are derived from its stories. Every
requirement in `specs/requirements.md` carries a `Derived from` field naming
a story or glossary terms, and the trace matrix's backward table shows the
links; the audit checks that every story has at least one requirement and
that each requirement says what its story says. How a requirement is written
so that it can be checked for form, which is the EARS notation A1 adopted,
how the specifications are audited for quality, what the audit found in A1's
draft and who found it, and how the trace matrix is built are the subjects
of Lecture 03.

## Applying this to your own project

Most of this lecture carries over to a project of any kind, and the parts
that need adapting are small.

**What carries over directly.**

- *The sections.* A purpose statement that says who agreed to it; a scope
  with the boundary and the assumptions labeled as someone else's
  obligations; the user categories with what each observes, and who is not
  a user; stories in the users' words with concrete examples; deferred
  wants with their sources; a pointer to the sign-off. A glossary beside it.
  None of this depends on the domain.
- *Elicitation with a cap.* Five questions, ranked, one at a time, each with
  a recommended answer, each recorded verbatim with who gave it. The
  `/elicit` skill works on any concept of operations that has the sections
  above; its taxonomy, `forms/conops.md`, is the section list stated as
  questions, and a document of another form gets a file of its own under
  `forms/` and becomes the skill's argument.
- *The record under reference.* Keep the stakeholders' words in a file no
  judgment depends on, and cite it from the specification. The habit costs
  a `Source` field per story.
- *A scenario file and a loader.* Any system with observable input and
  output can have its stories' examples written as data: one input, one
  expected output, the story it derives from, and a statement of what the
  file does not cover. The loader is twenty lines in whatever test framework
  the project uses, and it is the only part that changes when the language
  does.
- *A validation record with a decision column.* Separate the question "did
  it do what the story says?" from "is that what I want?"; the first is a
  test, the second is a column headed *Decision* and a signature.

**What you will need to adapt.**

- *The shape of a scenario.* The guard's is a message in and a message or
  nothing out. A system with state needs a setup, a sequence of steps, and an
  expected state; a system with a display needs an expected rendering. The
  course's earlier game example has scenarios of both kinds, and the shape
  of the file is itself a data format that the project fixes.
- *The elicitation taxonomy.* The eight categories are a concept of
  operations' sections. A different governing document has different
  sections, and a new file under the skill's `forms/` is where they go.
- *The people.* In A1 one person played both stakeholder roles, and the
  record says so. In a project the roles are held by different people, the
  record names them, and finding them before the first session is part of
  the work.
- *The cap.* Five questions suits a document the size of the guard's. A
  larger system has more Partial categories; the answer is more sessions,
  each capped, not a longer one.

## Exercise 2

Take a system of your own, or a copy of A1 with the security officer's
deferred want D-1 (a record of every dropped message) as the thing to be
elicited. Run `/elicit` with the stakeholders, or with yourself playing them
and saying so in the record. Produce: the elicitation record with at most
five entries; the revised concept of operations, with every changed sentence
citing its entry; the glossary entries the answers define; a scenario file
derived from the stories, with its assumptions and blind spots stated; a
loader in your language that runs every scenario citing its story; and a
validation record with a decision per user category and a sign-off naming
the version.

Then evaluate the skill the way A1 did: run it three times on the same
starting document, record the three queues, and write half a page on which
questions every run asked, which varied, and which category the skill never
asked about. Propose one change to its taxonomy and say what it would have
changed in your runs.

Deliverable: the record, the revised document, the glossary, the scenario
file and loader with the generated conformance report showing the stories'
rows, the validation record, and the evaluation note.

## Questions to think about

1. The elicitation record is reference material: not audited, and no
   judgment clause is about it. Suppose it were made a specification instead. Which
   audit checks would it fail by design, and what would a stakeholder lose?
2. When version A2 adds the `sanitize` stage, scenario SC-4 (Restricted 150
   in, Restricted 150 out) becomes wrong. List, in order, the artifacts that
   change and the people or rules that authorize each change. Which file
   must not be the first one edited, and why?
3. Construct the case from the validation section: the security officer
   says a Restricted message with payload above 100 must not leave, and every
   scenario passes. Which rows of the assurance report change, in what
   order, and what is the evidence for each change? What is the first artifact that would have to
   change for the scenarios to catch the officer's intent, and who may
   change it?
4. A1's loader compares outputs by value. Write the one-line change that
   would make it compare by object identity, and say which specification
   would have to change first for that test to be legitimate.
5. The three evaluation runs of `/elicit` never asked a question about terms,
   even when they rated the Terms category as Partial. Is that a defect of
   the skill, of its taxonomy, or of neither? What would the question have
   had to look like to be worth one of the five slots?

## Before next meeting

- Run A1 yourself: `uv sync`, then `tools/evaluate.sh`; read
  `reports/conformance.md` and find the three story rows; run sabotage 7
  from the README and restore the file.
- In a scratch copy, start a Claude Code session in `a1/`, run `/elicit
  conops` on the A0 concept of operations (copy `../a0/specs/conops.md` over
  `specs/conops.md` first), answer its questions yourself, and compare its
  queue with the five entries of `reference/elicitation.md`.
- Read the glossary entries for: concept of operations, purpose statement,
  elicitation record, reference, validation, executable specification,
  independence, verifier ladder.
- Read `specs/requirements.md` and the backward tables of
  `reports/trace-matrix.md`, and ask of each requirement how it was derived
  from its story and what a check of that derivation would look like. The
  next lecture is about that.
