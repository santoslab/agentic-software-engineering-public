# Audit items for a scenario file (`scen`)

Applied to `specs/scenarios.json` on its own, with the stories it derives
from at hand. Report each as *pass* or as the gaps it produced.

- **C-1 Well-formed header.** Every scenario has an identifier of the form
  `SC-n`, unique in the file; `id`, `derived_from`, `input`, and `expected`
  are present; `expected` is a message or `null`. (Mechanical at rung 4:
  `tests/conformance.py` reports a malformed or duplicate scenario; the
  audit still lists it.)
- **C-3 Glossary discipline (use).** The prose fields of the file (the
  `specification`, `assumes`, `governance`, `loader`, `blind_spots`, and
  `note` fields) use the glossary's terms in the glossary's sense and
  define none.
- **C-14 Examples and scenarios agree with their clauses.** For every
  scenario, the expected output follows from the clauses; a disagreement is
  a gap about the pair (scenario, clause), reported without deciding which
  side is wrong. Each scenario's input and expectation are the story's
  example, or a further instance the story's wording covers. The file is
  never edited to make a test pass; a scenario that looks wrong is a gap
  here.
