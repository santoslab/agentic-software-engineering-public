# Audit items for a glossary (`gloss`)

Applied to `specs/glossary.md` on its own. Report each as *pass* or as the
gaps it produced.

- **C-3 Glossary discipline (definition).** Every domain term is defined
  exactly once, as an entry of the form `- **term**: ...`; a term defined
  twice is a gap; a term in **bold** inside a definition is itself an entry;
  a definition that names a synonym a stakeholder uses says so inside the
  entry rather than defining the synonym again. The glossary is the only
  specification that defines a term; a definition found in another document
  is reported against that document under its own C-3.
