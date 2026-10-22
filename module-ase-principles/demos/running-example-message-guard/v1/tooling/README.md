# Tool Catalog: the assurance tooling of version A1

With agentic development, the effort of a developer shifts from writing the
code to building the environment and tooling that directs agents to build the
code and reports on whether the code and the development process meet the
goals. None of the reports, gates, or procedures in this snapshot appeared by
themselves when the requirements were written. Each was specified, built or
adapted, reviewed, and checked on inputs it must fail on, and each is
maintained like any other engineered artifact. This catalog is where that
work is recorded, so that a reader can set up the same tooling in their own
project, or build infrastructure shared across several. The companion sidebar
beside the module's Lecture 02 notes, *Tooling as engineering*, states the
philosophy and the organization model at more length; this file is the
inventory.

**How to read a page.** Every page has the same seven headings: the tool's
*goal* (the question it answers and the rule that names it); its
*requirements*, numbered; *the prompt*, verbatim for a tool new in A1 and as
guidance for a tool inherited from A0; the *review points* to check in an
agent's proposed design before accepting it; the *deliberate-failure checks*
the tool must fail or report on, and where they live; what to change when
*adapting it to your project*; and how to turn it into *shared
infrastructure*. A tool whose page has an empty deliberate-failure section is
a tool nobody has seen fail, and its findings are trusted only to that
extent.

## The tools

| Tool | Kind | Goal | Decides or supports | Reads | Writes | A0 or A1 | Page |
|---|---|---|---|---|---|---|---|
| `tests/conformance.py` | program | read the identified clauses and their fields from the specifications, so that no report depends on a hand-kept list | SQ-1 (well-formedness), TR-1 | `specs/*.md`, `specs/scenarios.json`, `reference/elicitation.md` | clause records; findings | A0, extended in A1 | [clause-reader.md](clause-reader.md) |
| `tests/conftest.py` | program (pytest plugin) | turn test citations and outcomes into requirements coverage, and fail the run on missing or failing evidence | CONF-1, TR-1 | citations, outcomes, the clause records | `reports/conformance.md` | A0, extended in A1 | [conformance-plugin.md](conformance-plugin.md) |
| `tools/gate.sh`, with the pytest and coverage settings in `pyproject.toml` | configuration | one command that decides RQ and the mechanical part of CONF and TR with an exit code | WF-1, RQ-1, CONF-1, TR-2 | the repository | an exit code; a provenance header | A0, extended in A1 | [gate.md](gate.md) |
| `tools/walk.py` | program | let a person exercise one message in a role and see what the guard does | VAL-2 (in A0, CONF-2) | one message | one line | A0 | [walkthrough-helper.md](walkthrough-helper.md) |
| `tests/test_scenarios.py` | program | run every scenario of the fixture file as a test that cites its story | CONF-1 | `specs/scenarios.json` | outcomes | A1 | [scenario-loader.md](scenario-loader.md) |
| `tools/trace.py` | program | resolve every declared link in both directions and report the ones that do not resolve | TR-2 | the specifications, the suite's citations | `reports/trace-matrix.md`; an exit code | A1 | [trace.md](trace.md) |
| `tests/tooling/` | program (tests of the tools) | show the clause reader and the trace tool failing on inputs they must fail on, before their findings are trusted | the trustworthiness of CONF and TR evidence | case directories | outcomes | A1 | [tooling-tests.md](tooling-tests.md) |
| `.claude/skills/elicit/` | agent procedure | obtain a concept of operations from its stakeholders in at most five questions and record their words | WF-2 | `specs/conops.md`, the glossary, the record | the record, the concept of operations, the glossary | A1 | [skill-elicit.md](skill-elicit.md) |
| `.claude/skills/audit-spec/` | agent procedure | audit the specifications by a fixed procedure and report gaps in a fixed form, under a version | SQ-2, RPT-2 | `specs/`, `process/rules.md` | `reports/audit-NN.md` | A1 | [skill-audit-spec.md](skill-audit-spec.md) |
| `build-history.sh` | program | replay the snapshots into a tagged git history, labeled as a reconstruction | none | `v0/`, `v1/reference/history/` | a git repository | A1 | [replay.md](replay.md) |

## Reused and new

Reused from A0: the clause reader and the conformance plugin, which A0 had
adapted from the Spec Kit tic-tac-toe demo; the gate; the walkthrough helper.
New in A1: the scenario loader, the trace tool, the tooling tests, and the two
skills. Unchanged tools from the ecosystem: `pytest`, `pytest-cov`, `ruff`,
`uv`. Every page says which of these its tool is.

## Licensing

The pages of this catalog are instructional prose (CC BY 4.0). The tools
themselves, their tests, and the skills are code and configuration (MIT).
