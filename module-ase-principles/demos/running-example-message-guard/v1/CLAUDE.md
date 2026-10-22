# Message guard, version A1

Before acting, read `process/rules.md`, then `specs/glossary.md`,
`specs/conops.md`, `specs/requirements.md`, and `specs/scenarios.json`. The
rules say how each judgment on this repository is established and when it
must hold; the specifications say what the system must do, in the glossary's
terms. To revise the concept of operations with its stakeholders, run
`/elicit` (rule WF-2). Before a specification is committed, run
`/audit-spec` and wait for the rulings (rule SQ-2). Never edit
`specs/scenarios.json` to make a test pass: a scenario that looks wrong is a
gap for the audit. Change nothing else without approval. The gate is
`tools/gate.sh`.
