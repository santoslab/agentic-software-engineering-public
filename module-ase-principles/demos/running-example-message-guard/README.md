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
| A1 | `v1/` | unchanged (`guard/` is byte-identical to v0) | elicitation through the `/elicit` skill and the revised concept of operations with its elicitation record; the glossary; EARS requirements; acceptance scenarios as data with a loader (the stories' method climbs from walkthrough to test); the audit run three times on a seeded draft and the `/audit-spec` skill; the trace tool and matrix; a ledger with two checkpoints; seven new rules in two new styles; a tool catalog (`v1/tooling/`) that teaches how each assurance tool was specified, prompted for, and checked |
| A2 | planned | `sanitize` stage and the pipeline | architecture, data format, interface contracts, the build plan, analysis and review as methods, the generated ledger |

The in-class demonstration for Lecture 01 is scripted in
`demo-script-lecture-01.md`, with a setup checklist and a segment-by-segment
record of what to run and show.

Each version is a self-contained snapshot. To compare two versions, use
`diff -r v0 v1`. `build-history.sh TARGET_DIR`, run from this directory,
replays the snapshots into a tagged git history: the complete A0 snapshot as
the baseline commit (`v0`), then A1's four commits (`a1-specs`,
`a1-scenarios`, `a1-trace`, `v1`) from the patches in
`v1/reference/history/`. The result is a reconstruction, not the original
build history, and its commit messages say so (`v1/tooling/replay.md`). A0's
development-log entries describe tasks, not individual commits: its
per-commit rules would prohibit a specifications-only first commit, so the
replay does not manufacture a commit per A0 task. A1 is the first version
whose dev-log entries each correspond to a commit that passed the gate. A2
will revisit the rules to permit intermediate commits before acceptance
checkpoints.

The A1 build followed `software-engineering/running-example-a1-plan-fable.md`.
The lecture notes for the two lectures on A1 (the concept of operations;
from the concept of operations to requirements) are not written yet.

Licensing follows the repository boundary (`LICENSING.md`): the specifications,
rules, reports, and READMEs are instructional prose under CC BY 4.0; the code,
tests, tools, and configuration are under MIT.
