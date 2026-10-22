# Running Example: the Message Guard

The running example of the agentic software engineering principles module: a
small cross-domain message guard in Python, grown through numbered versions so
that each version introduces a few specification forms, judgments, and process
rules. The design, the capability pool, the chosen progression (option A), and
the canonical list of specification forms are in
`software-engineering/running-example-design.md` at the repository root.

| Version | Directory | System | What it introduces |
|---|---|---|---|
| A0 | `v0/` | the `filter` stage: drop Critical, pass the rest unchanged | all five judgments on one function: a concept of operations with a sign-off, requirements with identifiers and methods, tests that cite clauses, the conformance aggregate, eight rules, a hand-written ledger with provenance |
| A1 | planned | unchanged | elicitation and the revised concept of operations, the glossary, EARS, fixtures, the audit and its skill, the trace matrix |
| A2 | planned | `sanitize` stage and the pipeline | architecture, data format, interface contracts, the build plan, analysis and review as methods, the generated ledger |

The in-class demonstration for Lecture 01 is scripted in
`demo-script-lecture-01.md`, with a setup checklist and a segment-by-segment
record of what to run and show.

Each version is a self-contained snapshot. To compare two versions, use
`diff -r v0 v1`. A replay script that turns the snapshots into a tagged git
history is planned with A1. A0's development-log entries describe tasks, not
individual commits: its per-commit rules would prohibit a specifications-only
first commit. Replay must start with the completed A0 snapshot as a baseline,
not manufacture a separate compliant commit for each task. The resulting
history would be a reconstruction from snapshots, not the original build
history. A2 will revisit the rules to permit intermediate commits before
acceptance checkpoints.

Licensing follows the repository boundary (`LICENSING.md`): the specifications,
rules, reports, and READMEs are instructional prose under CC BY 4.0; the code,
tests, tools, and configuration are under MIT.
