# The elicitation record: form of one entry

The record is `reference/elicitation.md`. It is reference material: the
stakeholders' words and the questions that drew them out, kept so that every
sentence of the concept of operations can be followed back to who said it.
No judgment of the development state is about it, and it is never audited as
a specification. If the file does not exist, create it with the header below;
otherwise append.

```markdown
# Elicitation Record: <system> (version <N>)

Reference material, not a specification (rule WF-2). Each entry is one
question put to a stakeholder and the answer in their words. Stories, terms,
and assumptions cite entries by identifier.

Session <YYYY-MM-DD> · asked by: <the agent, running /elicit <version>> ·
answered by: <name or "role played by <who>">, as <user category>; <...>

### E-<n> · to the <user category>

Question: <the interrogative, as asked>
Why it matters: <the one sentence, as asked>
Options: A. <...> (recommended) · B. <...> · C. <...>
Answer (verbatim): "<the stakeholder's words, unedited>"
Answered by: <who>, as <user category>, <YYYY-MM-DD>
Consequences: <section or clause changed>; <glossary term>; <deferred want>; <assumption>
```

Rules for the entry:

- One entry per accepted answer; a withdrawn answer keeps its entry with
  `Status: withdrawn` and the reason.
- Identifiers are never reused or renumbered.
- The verbatim answer is the record's reason to exist. Edit nothing inside
  the quotation marks.
- The consequences line names every place the answer changed, so that a
  reader of the concept of operations who sees `Source: E-3` can find the
  words behind the sentence.
