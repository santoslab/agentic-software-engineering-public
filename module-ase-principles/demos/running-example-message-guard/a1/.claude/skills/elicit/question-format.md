# How to write a question

These rules follow the `speckit-clarify` skill's question-writing rules, with
one addition: the question names who is being asked.

- Open with the addressee: `**To the security officer**` (a user category of
  the document, never "the user").
- Lead with `**Question:**` followed by a full interrogative that ends with
  `?`. The text before the `?` must make sense on its own. A topic label, a
  section heading, or an identifier is not a question: `Payload domain (REQ-0)`
  is invalid; `What values can a payload take?` is valid. An identifier may
  follow the `?` in parentheses, never precede it.
- Next, one plain-language sentence beginning `Why it matters:` that states
  what changes in the document depending on the answer.
- Everyday wording. Introduce a technical term only if the same sentence
  defines it. A reader who has never seen this repository must be able to
  answer from the question line alone.

For a multiple-choice question:

- Work out the most suitable option from the document, the domain, and the
  risk of getting it wrong, and put it first:
  `**Recommended:** Option A - <one or two sentences of reasoning>`.
- Then the options as a table, two to five of them, mutually exclusive, plus
  a `Short` row when a free-form answer is reasonable:

  | Option | Description |
  |---|---|
  | A | ... |
  | B | ... |
  | Short | A different short answer (at most five words) |

- Then the reply line: `Reply with a letter, say "yes" to take the
  recommendation, or give a short answer.`

For a short-answer question (no meaningful discrete options):

- `**Suggested:** <answer> - <reasoning>`, then
  `Format: at most five words. Say "yes" to take the suggestion, or answer
  in your own words.`

After the answer:

- "yes", "recommended", or "suggested" means the recommendation.
- Otherwise check that the answer names one option or fits five words; if it
  does not, ask one short disambiguation, which does not count as a question.
- Quote the answer verbatim in the record, including hedges and asides: a
  stakeholder's "I'd like one eventually; not needed for this version" is
  the sentence that makes a want *deferred* rather than *rejected*.
