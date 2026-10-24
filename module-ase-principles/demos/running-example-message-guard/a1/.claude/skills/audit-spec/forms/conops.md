# Audit items for a concept of operations (`conops`)

Applied to `specs/conops.md` on its own. Report each as *pass* or as the
gaps it produced.

- **C-1 Well-formed header.** Every story is one line of the form
  `**US-n** · Method: <value> · <Key>: <value> ...`; the identifier is unique
  across all specifications; the method is one of *test*, *analysis*,
  *review (human)*, *review (agent)*, *walkthrough (human)*, *walkthrough
  (agent)*; every key is one the format defines for a story (`Method`,
  `Scenarios`, `User category`, `Validated by`, `Source`, `Reason`). A
  header with an identifier and no method is a gap, not an omission.
  (Mechanical at rung 4: `tests/conformance.py` reports the same findings;
  the audit still lists them.)
- **C-3 Glossary discipline (use).** Every domain term used in the document
  is defined in `specs/glossary.md` and used only in its defined sense; the
  document defines no term of its own. A term used in a story and absent
  from the glossary is a gap.
- **C-4 Unambiguous.** Two careful readers could not disagree whether a
  behavior satisfies a story or whether a sentence of the scope holds. An
  unquantified adjective ("sensitive", "large", "promptly") where a
  definition or a number is needed is a gap. **Not a gap:** an
  implementation choice the document deliberately leaves open, and an
  adjective inside a deferred want, which is a want, not a clause.
- **C-5 Judgment clauses state why.** Every story whose method is *review*
  or *walkthrough* carries a `Reason` saying what a program cannot decide
  about it, or why it is not decided by a program at this commit. Apply the
  item to whatever the tree holds; if no story has such a method, report
  *pass, no clause in scope*.
- **C-6 Implementation-independent purpose and stories.** Nothing in the
  purpose statement, the scope, the user categories, or the stories names a
  language, a library, a data structure, or anything only a builder would
  see. This check has a ceiling: a reader decides it, and a program cannot;
  the repository records that at rung 3.
- **C-7 Complete for the stated scope and level.** Every case inside the
  boundary has a story or is covered by a requirement derived from one;
  nothing outside the boundary is specified; each user category has at
  least one story; leaving an algorithm open is not incompleteness.
