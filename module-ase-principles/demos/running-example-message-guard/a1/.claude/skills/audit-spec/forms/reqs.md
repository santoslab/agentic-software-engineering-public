# Audit items for a requirements document (`reqs`)

Applied to `specs/requirements.md` on its own. Report each as *pass* or as
the gaps it produced.

- **C-1 Well-formed header.** Every requirement is one line of the form
  `**REQ-n** · Method: <value> · <Key>: <value> ...`; the identifier is
  unique across all specifications; the method is one of *test*,
  *analysis*, *review (human)*, *review (agent)*, *walkthrough (human)*,
  *walkthrough (agent)*; every key is one the format defines for a
  requirement (`Method`, `Pattern`, `Derived from`, `Reason`). A header with
  an identifier and no method is a gap, not an omission. (Mechanical at
  rung 4: `tests/conformance.py` reports the same findings; the audit still
  lists them.)
- **C-2 EARS form.** Every requirement declares a `Pattern` and has that
  pattern's shape: *ubiquitous* "The <subject> shall <response>";
  *event-driven* "When <trigger>, the <subject> shall <response>";
  *state-driven* "While <state>, the <subject> shall <response>";
  *unwanted-behavior* "If <condition>, then the <subject> shall <response>";
  *optional-feature* "Where <feature>, the <subject> shall <response>";
  *complex* a combination of the above. The subject is the one the
  document's preamble names for that kind of clause; the verb is "shall";
  passive voice with no subject is a gap.
- **C-3 Glossary discipline (use).** Every domain term used in a
  requirement is defined in `specs/glossary.md` and used only in its
  defined sense; the document defines no term of its own.
- **C-4 Unambiguous.** Two careful readers could not disagree whether a
  behavior satisfies the clause. An unquantified adjective where a
  definition or a number is needed is a gap. **Not a gap:** an
  implementation choice the clause deliberately leaves open. REQ-2's
  "unchanged" requires equal values; whether the very same object is
  returned is left open on purpose, and asking for object identity would be
  a new requirement, not a resolution of an ambiguity.
- **C-5 Judgment clauses state why.** Every requirement whose method is
  *review* or *walkthrough* carries a `Reason` saying what a program cannot
  decide about it. Apply the item to whatever the tree holds; if no
  requirement has such a method, report *pass, no clause in scope*.
- **C-7 Complete for the stated scope and level.** Every case inside the
  boundary has a clause (each security level has an outcome); nothing
  outside the boundary is specified; leaving an algorithm open is not
  incompleteness.
