# Sidebar: two elicitation skills, read side by side

Companion to [Lecture 02](lecture-02-conops-and-elicitation-concepts.md),
section "How a concept of operations is obtained". It compares the skill
students used earlier in the course, `grill-me`, with the `/elicit` skill of
version A1, by reading the two definitions, and it says what was done in
writing the second one so that a stakeholder can sit through a session with
it. Both skills are in the repository: `grill-me` at
`module-software-engineering/student-materials/pkb-starter/.claude/skills/grill-me/SKILL.md`,
`/elicit` at
`module-ase-principles/demos/running-example-message-guard/a1/.claude/skills/elicit/`.

## The two definitions

`grill-me`, as shipped to students, is this file in full:

```
---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until
we reach a shared understanding. Walk down each branch of the design
tree resolving dependencies between decisions one by one.

If a question can be answered by exploring the codebase, explore
the codebase instead.

For each question, provide your recommended answer.
```

Three sentences of instruction. Everything the agent does in a session comes
from them and from its own judgment.

`/elicit` is a folder: a `SKILL.md` of about a hundred lines with six
numbered steps, and four bundled files it opens when it needs them: `taxonomy.md`
(eight categories a concept of operations must settle, with what "clear"
means for each), `question-format.md` (the exact shape of a question),
`record-template.md` (the shape of a record entry), and `agents/openai.yaml`
(the switch that keeps another harness from starting it on its own). Its
front matter names the trigger and the near misses, takes an optional path,
and sets `disable-model-invocation: true` and `allowed-tools: Read Grep
Glob`. The body's six steps are: read before asking; scan the document;
build the queue; ask one question at a time; record, then apply, after every
accepted answer; report and stop.

The difference in length is not the point. A longer skill is not a better
one, and much of what `/elicit` says is in bundled files so that the body
stays short. The point is what each definition decides and what it leaves
to the agent.

## What the definitions decide

| Decision | `grill-me` | `/elicit` |
|---|---|---|
| Who is being interviewed | the developer, about their own plan ("Interview me") | a named user category of the concept of operations, about what they want from the system |
| When the session ends | "until we reach a shared understanding": the agent decides | after at most five questions, or when the queue is empty, or when the stakeholder says "done" |
| Which questions are asked | "every aspect"; "each branch of the design tree" | the Partial and Missing categories of a fixed taxonomy, ranked by how much the answer changes the document times how uncertain it is |
| What may be asked | anything a design decision depends on | decisions only; implementation, technology, and task order are excluded; a fact the repository answers is looked up |
| How many at once | not stated (one at a time in the version students had; later versions ask several per round) | exactly one |
| The form of a question | not stated, beyond "provide your recommended answer" | a full interrogative, one "why it matters" sentence, the recommended option first with its reason, a table of two to five options, a line saying how to reply |
| How the answer is recorded | not recorded; it stays in the chat transcript | appended verbatim to `reference/elicitation.md` under an identifier, with who answered, in which role, when, and the consequences |
| Where the answer lands | wherever the agent decides to write it, if anywhere | in the one part of the document it affects, replacing contradicted text, with the entry cited |
| What the agent may not do | not stated | touch the requirements, the scenarios, the tests, or the code; write a decision nobody gave; paraphrase an answer |
| How the session ends | it does not; the next thing the agent does is whatever the developer types next | a completion report: questions asked, sections touched, a coverage table, the next steps |
| Who may start it | the model may, when the description matches | only the developer |
| Portability | the wording is harness-neutral; later versions bound it to one harness's tool name | harness-neutral; the Codex switch is a bundled file |

Every row where `grill-me` says "not stated" is a decision the agent makes
on its own, differently each session.

## Why students were overwhelmed, read off the table

The earlier course material had students run `grill-me` on their own
knowledge-base and game projects, and the common report was that the
questions did not stop. The table says why, and it is not that the skill is
badly written for what it was written for.

`grill-me` was written for a developer stress-testing a design they are
about to implement. In that setting the developer is both the interviewer's
subject and the person who will act on the answers, the design tree is
finite, every branch is theirs to decide, and an unbounded interview is what
they asked for: its author describes sessions of about forty-five minutes.
"Explore the codebase instead" is the one bound it has, and it is the right
one for that setting.

Pointed at a concept of operations, four things change. The person
answering is a stakeholder whose attention is the scarce resource, not the
developer. The questions that matter most, whether the guard should trust
the marking it is given, whether the sender needs to be told of a drop, are
few, and they are mixed in with questions about wording that change one
sentence. The answers are evidence: a story will be written from them and
later checked against them, so they have to be kept, in the stakeholder's
words, with their source. And a guess the interviewer writes into the
document is a requirement nobody decided. `grill-me` has no bound, no
ranking, no record, and no rule against filling a gap with a sensible
default, because the setting it was written for needed none of those.

## What was done to write `/elicit`

The skill was not written from scratch. Its shape is Spec Kit's `clarify`
step, a published procedure that asks at most five questions, one at a time,
each with a recommended option, and encodes the answers into the
specification. Three things were changed for the course, and each is a
design decision with a reason that the skill states.

1. **The taxonomy is the document's own sections.** `clarify` scans ten
   categories of a software feature (data model, performance, integration,
   and so on). `/elicit` scans the eight parts of a concept of operations:
   purpose, scope and boundary, assumptions, user categories, stories, terms,
   wants and non-goals, validation. A question is queued only when one of
   those is Partial or Missing, so the questions are about what the document
   must say and not about what a developer would like to know.
2. **Each question is addressed to a user category.** `clarify` addresses
   "the user". `/elicit` opens every question with "To the security
   officer" or "To the message sender", because the answer is that
   stakeholder's to give and the record will say who gave it. This is also
   what makes the `Source` field of a story checkable: a story in the
   sender's words should cite the sender's answer.
3. **The record is reference, in the stakeholders' words.** `clarify` appends
   a one-line `Q: ... → A: ...` to the specification. `/elicit` writes a
   full entry, with the answer quoted verbatim, to `reference/elicitation.md`,
   a file the course classifies as reference material: not audited, no
   judgment about it, cited from the specification. The reason is stated in
   the skill: the record is where the stakeholders' words live, and it is
   never a specification. A hedge such as "I'd like one eventually; not
   needed for this version" is kept as spoken, and it is the specification,
   not the record, that turns it into the status *deferred*.

Two things were left out of `clarify` on purpose: its extension-hook
machinery, which belongs to its toolkit, and its re-validation of a quality
checklist after the session, because in the course method the next step is
the audit skill, which does that job under its own procedure.

Beyond the adaptation of `clarify`, the writing followed the criteria the
course's skills lecture set out for any skill, and each shows up in the
file:

- **A description that says when and when not.** "Use only when the
  developer explicitly asks to elicit or revise a concept of operations. Not
  for writing requirements, not for auditing a specification, not for
  explaining what a concept of operations is." The description is read on
  every turn by something deciding whether to act; naming the near misses
  keeps it from acting on them.
- **Stops where a human decides.** The session stops at five questions and
  ends with a report; the skill never commits; a change the developer
  rejects is reverted and its entry marked withdrawn rather than deleted.
  Only the developer can start the skill, because a wrong start writes to a
  governing document.
- **Reasons with the rules.** Each step says why: "asking a stakeholder what
  the repository already says wastes the one resource this procedure
  spends"; "quote the stakeholder; do not paraphrase"; "a guess written into
  it becomes a requirement nobody decided". A rule with its reason transfers
  to cases the rule did not list.
- **Concrete over adjectival.** Not "ask good questions" but a format: the
  interrogative, the "why it matters" sentence, the recommended option
  first, the table, the reply line. Not "don't ask too much" but a number.
- **Short body, bundled detail.** The taxonomy, the question format, and the
  record template are files the agent opens when it reaches the step that
  needs them; the body is paid for the whole session, a bundled file only
  when read.
- **Deference to the repository.** The skill reads `process/procedures.md`
  first and says that if the repository's own procedure or record form
  differs, that is the authority and the bundled files are the fallback.
- **Facts are looked up, decisions are asked.** This is `grill-me`'s own
  best line, "if a question can be answered by exploring the codebase,
  explore the codebase instead", kept and given its reason.

## What the evaluation showed

A procedure skill has no exit code, so it was checked the way the skills
lecture checks one: three runs on the same document, the A0 concept of
operations, by fresh agents asked to print their whole queue. All three
queued five questions. All three asked about the marking assumption, what a
sender observes on a drop, the deferred wants, and who is a user; the fifth
question varied. No run wrote a decision of its own. No run asked about
terms, even when it rated that category as Partial, treating a missing
definition as the writer's job; and no run asked about the payload's domain,
because all three found that REQ-0 already answers it. The catalog page
`a1/tooling/skill-elicit.md` has the table, and one proposed change to the
taxonomy that the evaluation suggested. The live session of A1
(`a1/reference/elicitation.md`) used the second run's queue.

That is the practical difference between the two skills, stated as a test:
run `/elicit` three times on one document and the queues agree on the
questions that matter; run `grill-me` three times and there is no way to say
in advance how many questions there will be or which.

## What `grill-me` is still for

None of this makes `grill-me` a bad skill. A developer about to implement a
design, with a backlog of their own decisions to settle and an hour to
settle them, is the case it was written for, and the course's project work
still has that case. The lesson is narrower: a skill is a procedure, a
procedure has a setting, and a procedure moved to a setting with a different
scarce resource needs different stops. For a stakeholder-facing document the
scarce resource is the stakeholder's attention, and the stops are a cap, a
ranking, a record, and a rule against guessing.
