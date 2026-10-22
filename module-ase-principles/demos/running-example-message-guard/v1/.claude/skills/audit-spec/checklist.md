# Audit checklist (rule SQ-2; skill version 1.1)

Every item is applied and reported, as *pass* or as the gaps it produced.
Cite items as C-1 to C-14. (Version 1.0 cited them as A-1 to A-14, which
collided with the assumption identifiers A-1, A-2 of the concept of
operations; audit 03 noticed, and 1.1 renamed them.) The judgment each item
maintains is SQ unless the item says otherwise.

## Within a document

- **C-1 Well-formed header.** Every identified clause is one line of the form
  `**ID** · Method: <value> · <Key>: <value> ...`; the identifier is unique
  across all specifications; the method is one of *test*, *analysis*,
  *review (human)*, *review (agent)*, *walkthrough (human)*, *walkthrough
  (agent)*; every key is one the format defines (`Method`, `Pattern`,
  `Derived from`, `Scenarios`, `Validated by`, `Source`, `User category`,
  `Reason`). A header with an identifier and no method is a gap, not an
  omission. (Mechanical at rung 4: `tests/conformance.py` reports the same
  findings; the audit still lists them.)
- **C-2 EARS form.** Every requirement declares a `Pattern` and has that
  pattern's shape: *ubiquitous* "The <subject> shall <response>";
  *event-driven* "When <trigger>, the <subject> shall <response>";
  *state-driven* "While <state>, the <subject> shall <response>";
  *unwanted-behavior* "If <condition>, then the <subject> shall <response>";
  *optional-feature* "Where <feature>, the <subject> shall <response>";
  *complex* a combination of the above. The subject is the stage or the
  guard; the verb is "shall"; passive voice with no subject is a gap.
- **C-3 Glossary discipline.** Every domain term used in a specification is
  defined exactly once in `specs/glossary.md` and used only in its defined
  sense; no other specification defines a term. A term used in a story and
  absent from the glossary is a gap; a term defined twice is a gap.
- **C-4 Unambiguous.** Two careful readers could not disagree whether a
  behavior satisfies the clause. An unquantified adjective ("sensitive",
  "large", "promptly") where a definition or a number is needed is a gap.
  **Not a gap:** an implementation choice the clause deliberately leaves
  open. REQ-2's "unchanged" requires equal values; whether the very same
  object is returned is left open on purpose, and asking for object
  identity would be a new requirement, not a resolution of an ambiguity.
- **C-5 Judgment clauses state why.** Every clause whose method is *review*
  or *walkthrough* carries a `Reason` saying what a program cannot decide
  about it, or why it is not decided by a program at this commit. Apply the
  item to whatever the tree holds; if no clause has such a method, report
  *pass, no clause in scope*.
- **C-6 Implementation-independent purpose and stories.** Nothing in the
  purpose statement, the scope, the user categories, or the stories names a
  language, a library, a data structure, or anything only a builder would
  see. This check has a ceiling: a reader decides it, and a program cannot;
  the repository records that at rung 3.
- **C-7 Complete for the stated scope and level.** Every case inside the
  boundary has a clause (each security level has an outcome); nothing
  outside the boundary is specified; leaving an algorithm open is not
  incompleteness.

## Between documents

- **C-8 Derivation both ways.** Every story has at least one requirement
  deriving from it; every requirement derives from a story or from glossary
  terms; every scenario derives from a story and is listed in that story's
  `Scenarios` field; a story's `Source` entries are answers given by a
  stakeholder of the story's own user category. (Mechanical at rung 4 for
  the link part: `tools/trace.py`.)
- **C-9 No contradiction.** No two clauses, in one document or across two,
  assign the same input different outcomes or promise what another
  forbids. Read clauses that touch the same property side by side, word for
  word.
- **C-10 One term, one sense.** The same word means the same thing in every
  document; a definition that differs between the glossary and a document
  is a gap in the document.
- **C-11 Assumptions are not requirements.** Anything the deploying
  organization must ensure (routing, assignment of markings, authentication)
  is stated as an assumption in the scope section, never as a requirement
  with a verification method. **Not a gap:** an assumption stated as an
  assumption.
- **C-12 Deferred wants stay deferred.** A want the concept of operations
  records as deferred has no requirement, story clause, or scenario that
  promises it.
- **C-13 References resolve.** Every file, rule, and record entry a
  specification names exists in the tree at this commit. (Added in 1.1:
  audit 03 found two forward references under rule SQ-1 with no item to
  cite.)

## By execution

- **C-14 Examples and scenarios agree with their clauses.** For every story
  example and every scenario, the expected output follows from the clauses;
  a disagreement is a gap about the pair (example, clause), reported without
  deciding which side is wrong. Each scenario's input and expectation are
  the story's example, or a further instance the story's wording covers.
