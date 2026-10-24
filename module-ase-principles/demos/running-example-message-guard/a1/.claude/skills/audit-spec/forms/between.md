# Audit items between documents

Applied when the scope has more than one form, to the documents read
together. Report each as *pass*, *not in scope*, or the gaps it produced.

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
- **C-13 References resolve.** Every file, judgment clause, procedure, and
  record entry a specification names exists in the tree at this commit.
  (Added in 1.1: audit 03 found two forward references, under Specs-SQ-1,
  with no item to cite.)
- **C-14 Examples agree with their clauses.** For every story example, the
  expected output follows from the clauses; a disagreement is a gap about
  the pair (example, clause), reported without deciding which side is
  wrong. The scenario file's own C-14 is in `scen.md`.
