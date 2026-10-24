---
name: elicit
description: >-
  Elicits or revises a stakeholder-facing specification with its stakeholders
  by the clarify method: scan the document for what it does not settle, ask
  the stakeholders at most five questions, one at a time, each with options
  and a recommended answer, record every answer verbatim in the elicitation
  record, and apply each answer to the section it affects. The first argument
  names the form (conops) or a path. Use only when the developer explicitly
  asks to elicit or revise a specification with its stakeholders. Not for
  writing requirements, not for auditing a specification, not for explaining
  what a concept of operations is.
argument-hint: "[form (conops) or path, default conops] [optional focus]"
disable-model-invocation: true
allowed-tools: Read Grep Glob
---

# Elicit: a specification from its stakeholders

Version 1.1. This skill packages procedure `Elicit` of
`process/procedures.md`: the steps are the procedure's, stated once for any
form; what depends on the form is a file under [forms/](forms/).

## 0. Resolve the form

The first word of `$ARGUMENTS` is the form or a path; the rest is the focus
the developer wants covered first. If it is empty, the form is `conops`.

| Form | Document | Taxonomy |
|---|---|---|
| `conops` | `specs/conops.md` | [forms/conops.md](forms/conops.md) |

A path is mapped to its form by its file name (`conops.md` is `conops`). A
form or path that is not in the table stops the skill: say which forms have
a taxonomy and ask the developer to add one under `forms/` before running
the skill on a new form. Do not improvise a taxonomy.

A stakeholder-facing specification is a governing document: what derives
from it is built from it, and it is the document a stakeholder signs. A
guess written into it becomes a requirement nobody decided, and a question
put to a stakeholder costs their attention. So this skill asks few
questions, asks them well, records the answers in the stakeholders' own
words, and changes the document only in the way an answer says.

## 1. Read before asking

Read, in full: the document; `specs/glossary.md` if it exists;
`reference/elicitation.md` if it exists (earlier questions are not asked
again); and `process/procedures.md`, whose procedure `Elicit` this skill
performs. If the repository's procedure or record form differs from this
skill's bundled files, the repository's is the authority and the bundled
files are the fallback.

## 2. Scan the document

Rate each category of the form's taxonomy as Clear, Partial, or Missing for
this document. Keep the map internal; print it only if no question will be
asked. A fact the repository answers (a file, a clause, an earlier answer)
is looked up, never asked: asking a stakeholder what the repository already
says wastes the one resource this procedure spends.

## 3. Build the queue

From the Partial and Missing categories, draft candidate questions and keep
at most five, ranked by impact times uncertainty: an answer that would change
a story, a term, an assumption, or the system boundary outranks one that
would only polish wording. Each question must be answerable with a letter
from two to five options, or with at most five words. Exclude questions about
implementation, technology, or task order; exclude anything already answered.
Never reveal the queue; a stakeholder sees one question at a time.

## 4. Ask one question at a time

Address each question to a named user category of the document ("to the
security officer"), since the answer is theirs to give and the record will
say who gave it. Write the question exactly as [question-format.md](question-format.md)
says: a full interrogative, one "Why it matters" sentence, the recommended
option first with its reason, the options table, the reply line. Wait for the
answer. A reply of "yes" or "recommended" takes the recommendation; an
ambiguous reply gets one short disambiguation that does not count as a new
question. Stop when the queue is empty, when the stakeholder says "done" or
"stop", or after the fifth question.

## 5. Record, then apply, after every accepted answer

Immediately after an answer is accepted:

1. Append an entry to `reference/elicitation.md` in the form of
   [record-template.md](record-template.md), under the next free identifier
   `E-n`: the question as asked, why it mattered, the options and the
   recommended one, the answer **verbatim** (quote the stakeholder; do not
   paraphrase), who answered in which role, when, and the consequences
   (which sections, stories, assumptions, wants, or terms the answer changes).
   The record is reference material: it is where the stakeholders' words
   live, and it is never a specification.
2. Apply the answer to the part of the document it affects, and nowhere
   else: a sentence of the purpose; an assumption in the scope section; a
   user category's "observes" line; a story and its example; a deferred
   want; a glossary entry in `specs/glossary.md`. Replace contradicted text
   rather than adding beside it; leave no sentence that the answer has made
   false. Cite the entry (`E-n`) where the document has a place for a
   source. Save after each integration.
3. Check: exactly one record entry per accepted answer; no contradiction
   left behind; no heading added that the document's skeleton does not have;
   one canonical term for one concept.

Do not touch `specs/requirements.md`, the scenarios, the tests, or the code:
those derive from the document and are revised by their own procedures
after the audit.

## 6. Report and stop

End with a completion report: the number of questions asked and answered;
the sections touched; a coverage table listing every taxonomy category as
Resolved, Deferred (quota reached; name what remains), Clear, or Outstanding
(still Partial or Missing but low impact); and the next steps, which in the
course method are `/audit-spec` on the revised family, then the validation
walkthrough and the sign-off (ConOps-VAL-1). The developer reviews the diff;
a change the developer rejects is reverted and its record entry is marked
withdrawn, not deleted. Do not commit.
