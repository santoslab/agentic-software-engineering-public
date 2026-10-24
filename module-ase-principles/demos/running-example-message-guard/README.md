# Running Example: the Message Guard

The running example of the agentic software engineering principles module: a
small cross-domain message guard in Python, grown through numbered versions so
that each version introduces a few specification forms, judgment clauses, and
process artifacts. The design, the capability pool, the chosen progression
(option A), and the canonical list of specification forms are in
`software-engineering/running-example-design.md` at the repository root; the
layering of the process material (definition, evaluation, reporting, ledger,
control) is in `software-engineering/running-example-relayering.md`.

| Version | Directory | System | What it introduces |
|---|---|---|---|
| A0 | `a0/` | the `filter` stage: drop Critical, pass the rest unchanged | all five judgments on one function: a concept of operations with a sign-off, requirements with identifiers and methods, tests that cite clauses, the conformance evidence, five judgment definitions with eight clauses filed by form, records of the review, the walkthroughs, and the sign-off, and an assurance report compiled on request with provenance per row. No process rules: nothing says when a claim must hold |
| A1 | `a1/` | unchanged (`guard/` is byte-identical to `a0/`) | elicitation through the `/elicit` skill and the revised concept of operations with its elicitation record; the glossary; EARS requirements; acceptance scenarios as data with a loader (the stories' method climbs from walkthrough to test); the audit run three times on a seeded draft and the `/audit-spec` skill, both skills taking the form as their argument; the two procedures, Audit and Elicit; the trace tool and matrix; the judgments file grown to eleven clauses in six forms; an assurance report compiled at each of four commits; a tool catalog (`a1/tooling/`) that teaches how each assurance tool was specified, prompted for, and checked |
| A2 | planned | `sanitize` stage and the pipeline | architecture, data format, interface contracts, the build plan, analysis and review as methods; the ledger as the report kept, and the first process rules: gates, staleness, the hook |

The in-class demonstration for Lecture 01 is scripted in
`demo-script-lecture-01.md`, with a setup checklist and a segment-by-segment
record of what to run and show.

Each version is a self-contained snapshot. To compare two versions, use
`diff -r a0 a1`. `build-history.sh TARGET_DIR`, run from this directory,
replays the snapshots into a tagged git history: the complete A0 snapshot as
the baseline commit (`a0`), then A1's four commits (`a1-specs`,
`a1-scenarios`, `a1-trace`, `a1`) from the patches in
`a1/reference/history/`. The result is a reconstruction, not the original
build history, and its commit messages say so (`a1/tooling/replay.md`).
A0's development-log entries describe tasks, not individual commits, so the
replay does not manufacture a commit per A0 task. A1's entries from the
sixth on each correspond to a commit, and the assurance report compiled for
each commit is in its tree (`git show a1-specs:reports/assurance-report.md`
shows ConOps-VAL-1 not holding after the revision of the concept of
operations).

The A1 build followed `software-engineering/running-example-a1-plan-fable.md`
and was re-layered on 2026-10-24 (`a1/reference/history/README.md` says how
the patches were regenerated). The lecture notes for the two lectures on A1
are `../../lecture-notes/lecture-02-conops-and-elicitation-concepts.md`
(written) and Lecture 03 (planned).

Licensing follows the repository boundary (`LICENSING.md`): the
specifications, judgments, procedures, templates, records, reports, and
READMEs are instructional prose under CC BY 4.0; the code, tests, tools,
skills, and configuration are under MIT.
