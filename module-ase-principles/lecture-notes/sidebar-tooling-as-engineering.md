# Sidebar: tooling as engineering

Companion to [Lecture 02](lecture-02-conops-and-elicitation-concepts.md)
and to the tool catalog of version A1,
`../demos/running-example-message-guard/v1/tooling/`. Lecture 01 ended its
section on process, reporting, and assurance tooling by saying that later
lectures would give the subject substantial attention. They do not, by
decision: there is no lecture time for building tools. This sidebar states
the idea in two pages, and the catalog, one page per tool, is the reading
that takes the place of the lecture.

## The shift of effort

With agentic development, a developer's effort moves from writing the code
to building the environment and the tooling that directs agents to build the
code, and that reports on whether the code and the development process meet
the developer's goals.

The reason is the one Lecture 01 gave for the whole method. An agent writes
code quickly and in volume, and the person directing it does not read all of
it; for a system of any size they cannot. What the person reads instead is
the specifications, the evidence that the code conforms to them, and the
record of whether that evidence is current. None of those three exists
unless something produces it. A conformance report is written by a program
that reads clause identifiers from the specifications and citations from the
tests. A trace matrix is written by a program that resolves links. A gate is
a program whose exit code decides whether a commit may be made. An
elicitation session or an audit is run by an agent following a procedure
that someone wrote down. Every one of these is an engineered artifact: it
has goals, it has requirements, its design is reviewed before it is trusted,
it is checked on inputs it must fail on, and it is maintained when the things
it reads change.

Version A1 of the message guard makes the proportion visible. The product,
`guard/`, is 29 lines of code, unchanged since A0. The tooling that
specifies, checks, and reports on it is about 600 lines of code (the clause
reader, the conformance plugin, the trace tool, the scenario loader, the
gate, and the tools' own tests), about 500 lines of procedure in the two
skills, and 31 small files of cases the tools must fail on. The prose that
governs and records the work, the specifications, the rules, the ledger, the
dev log, the audits, and the validation record, is about 1,150 lines more.
For a system this small the proportion is absurd, and Lecture 01 said so;
the point is that the proportion does not reverse as the system grows. It is
where the person's effort goes when the agent writes the code.

## What counts as assurance tooling

Five kinds of thing in A1 are tooling in this sense, and each has a page in
the catalog.

- **Readers**, which take the specifications apart so that no report depends
  on a hand-kept list: the clause reader, `tests/conformance.py`.
- **Checkers**, which decide something and say what they could not accept:
  the trace tool, `tools/trace.py`, and the gap logic inside the plugin.
- **Report writers**, which produce the files a person reads instead of the
  code: the plugin's conformance report, the trace matrix.
- **Gates**, which turn checks into an exit code a commit can be conditioned
  on: `tools/gate.sh`, with the thresholds in `pyproject.toml`.
- **Agent procedures**, which package an activity so that it is done the
  same way every time and reported under a version: `/elicit` and
  `/audit-spec`.

And one thing that is tooling about tooling: the tools' own tests,
`tests/tooling/`, which show the reader and the trace tool failing on inputs
they must fail on. A verifier that has never been seen to fail has not been
verified, and its findings are trusted only to that extent.

Two things are not tooling. The product is not. And the specifications are
not, although the tools read them: a specification is what the tools check
against, and a tool that could change it would not be a verifier.

## The tools of A1

| Tool | Goal | Decides or supports |
|---|---|---|
| `tests/conformance.py`, the clause reader | read the identified clauses and their fields from the specifications; report a header it cannot accept rather than dropping it | SQ-1, TR-1 |
| `tests/conftest.py`, the conformance plugin | turn test citations and outcomes into requirements coverage; fail the run on missing or failing evidence; label a partial run | CONF-1, TR-1 |
| `tools/gate.sh`, with the settings in `pyproject.toml` | one command that decides RQ, the mechanical part of CONF, and TR, with an exit code and a header saying what was checked | WF-1 |
| `tools/walk.py`, the walkthrough helper | let a person exercise one message in a role and see what the guard does | VAL-2 |
| `tests/test_scenarios.py`, the scenario loader | run every scenario of the fixture file as a test that cites its story | CONF-1 |
| `tools/trace.py`, the trace tool | resolve every declared link in both directions and report the ones that do not resolve | TR-2 |
| `tests/tooling/`, the tooling tests | show the reader and the trace tool failing on inputs they must fail on | the trustworthiness of CONF and TR evidence |
| `.claude/skills/elicit/` | obtain a concept of operations from its stakeholders in at most five questions and record their words | WF-2 |
| `.claude/skills/audit-spec/` | audit the specifications by a fixed procedure and report gaps in a fixed form, under a version | SQ-2, RPT-2 |
| `build-history.sh` | replay the snapshots into a tagged git history, labeled as a reconstruction | none; a teaching artifact |

Four of these were inherited from A0, where they had been adapted from the
course's earlier Spec Kit demonstration; six are new in A1. The catalog's
front page, `tooling/README.md`, has the fuller table, with what each reads
and writes.

## How to read a catalog page

Every page has the same seven headings, and the order is the order in which
the tool was built.

1. **Goal.** The question the tool answers, for whom, and the rule that names
   it as decider or evidence. A tool with no rule naming it is a tool nobody
   is obliged to run.
2. **Requirements.** Numbered: what it reads, what it writes, which findings
   it reports, its exit code, whether it is deterministic, and what it does
   not decide. The last item is the one most often missing from a first
   draft, and the one that keeps a green result from being read as more than
   it is.
3. **The prompt.** For a tool new in A1, the prompt that produced it,
   verbatim, with the layout the agent proposed and the developer approved.
   For a tool inherited from A0, the prompt that would produce it, labeled as
   guidance, with the chain of decisions that actually produced it. The
   prompt is on the page because asking for a tool is different from asking
   for a report: the trace tool's prompt hands the agent eight requirements
   and asks for a layout before any code, and the layout is what was
   reviewed.
4. **Review points.** What to check in the agent's proposed design before
   accepting it. For the plugin: the clause list comes from the reader and
   never from a constant; a clause with no citing test fails the run rather
   than being omitted; a partial run cannot be mistaken for a full one when
   the saved file is read alone.
5. **Deliberate-failure checks.** The inputs the tool must fail on or report,
   where they live, and how to run them. For the trace tool, a directory per
   finding kind under `tests/tooling/cases/`; for the plugin, four scripted
   demonstrations in the README, one of which is the uncited failing test
   that fails the suite while every clause row stays green.
6. **Adapting it to your project.** What is project-specific (the header
   format, the marker name, the coverage threshold, the test framework) and
   what carries over as an idea.
7. **Making it shared infrastructure.** How to package it, what to version,
   and why a shared defect matters.

The page for the trace tool, `tooling/trace.md`, is the worked example: its
requirements were written before the tool, its prompt asks for a layout
first, and its cases were listed before its code.

## Sharing across projects

Nothing on the list above is specific to the message guard except the
header format the reader parses and the names of the files it reads. An
organization that fixes one clause-header format, one citation convention,
and one report form for all its projects can share one reader, one plugin,
one trace tool, and one pair of skills, and each product repository then
carries only its specifications, its tests with their citations, and its
configuration.

The model, stated once: a development-infrastructure or
engineering-productivity team maintains the common foundation as versioned
packages (a pytest plugin with an entry point; a skill folder; a trace tool
that takes the reader as configuration), with the cases each tool must fail
on shipped inside the package and run on every release. Product teams supply
specifications, tests, and configuration, and they pin the version of the
foundation they use. Updates are controlled, because a defect in a shared
report gives every project the same misleading picture at once: a plugin
that silently drops a malformed header, which is what A0's did, would do so
in every repository that used it. The header format is the contract between
the two sides, and it is versioned with the tools that read it.

This is an organizational model to understand, not a platform to build for
the course. The course's version is the catalog: enough of the foundation,
written down, that a reader can set it up alone or recognize it when an
organization provides it.

## In your own project

- Start with the gate and one report. A single command whose exit code says
  whether the mechanical checks pass, and one generated file a person can
  read, are the two tools every project needs on its first day. The
  catalog's pages for the gate and the plugin say what each must do.
- Add a tool the second time you do a check by hand. The first time is a
  habit; the second time, write the goal down, and the goal is most of the
  requirements.
- Write the requirements before the prompt, and ask for a layout before
  code. The review of the layout is where a tool that would silently omit
  something gets caught, and it is cheaper than the review of the code.
- Keep the inputs it must fail on beside it, and run them with the suite. A
  finding kind with no case is a finding kind nobody has seen the tool
  report.
- Say, on the tool's page, what it does not decide. The trace tool decides
  whether a link resolves, not whether the linked texts agree; the plugin
  decides whether a clause is cited, not whether the citing test's
  assertions check it. Those sentences are what keep a green report from
  being read as proof.
- Keep the prompt. Six months later, the prompt and the approved layout are
  how the next person learns why the tool is shaped as it is.

The catalog is at `v1/tooling/README.md`.
