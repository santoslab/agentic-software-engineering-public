# The trace tool: `tools/trace.py`

## Goal

Resolve every declared link between the specifications and the suite, in
both directions, and report the ones that do not resolve: story to
requirements to scenarios to tests, and back. Rule TR-2 names it; it climbs
the "derived from" check from a person (A0's TR-1, "read by a person with
SQ-1") to a program. It decides links only. Whether a requirement says what
its story says, or a test's assertions check its clause, still needs a
reader (rule SQ-2's audit and A2's test-discipline review).

## Requirements

Written before the tool was built (the A1 plan's section 9.3).

- **T1 Inputs.** The clause headers of `specs/conops.md` and
  `specs/requirements.md` through `tests/conformance.py`; the scenarios of
  `specs/scenarios.json`; the glossary terms of `specs/glossary.md`; the
  `E-n` entries of `reference/elicitation.md`; the suite's citations,
  obtained by collecting the suite in-process with a small plugin that
  gathers the `req` markers (no second marker parser).
- **T2 Output.** `reports/trace-matrix.md` with a header (tool version, files
  read, number of tests collected and citing, the repository state: HEAD
  and whether the working tree was clean), the forward table, the two
  backward tables, a findings section, and a scope line.
- **T3 Findings**, each with the identifier and the location: dangling
  `Derived from`, `Scenarios`, `Source`, or marker; a scenario not listed by
  its story; a story with no requirement; a requirement with no story or
  glossary derivation; a *test* clause with no citing test (reported here as
  a link, while the plugin reports its outcome); and every finding of the
  clause reader (duplicate identifier, malformed header, unknown method,
  key, or pattern, missing Reason).
- **T4 Exit code** non-zero if the findings section is not empty; zero
  otherwise.
- **T5 No judgment.** The tool never decides whether a link is semantically
  right.
- **T6 Determinism.** Same inputs, same report, except the date line and
  the repository state.
- **T7 Verified** on `tests/tooling/cases/`: one directory per finding kind
  with the expected findings, and a clean base that must produce none.
- **T8 Runs** as `uv run python tools/trace.py` from the snapshot root and
  is the last step of `tools/gate.sh`.

## The prompt

New in A1. The tool was written by the build agent working from T1 to T8
and the plan's layout decisions; no separate prompt-to-agent exchange took
place in this build, so the prompt below is the one a developer would hand
to an agent to reproduce the work, and the "approved layout" is the layout
actually built and reviewed against the points in the next section.

> Here are the requirements T1 to T8 for a trace tool and the clause reader
> `tests/conformance.py` it must use. Before writing code, propose: what is
> read and from where; what is computed; the report's sections; the finding
> kinds as a fixed vocabulary; and the list of cases under
> `tests/tooling/cases/` that the tool must report a finding on, one per
> kind. Wait for my approval of that layout, then implement, then run the
> cases.

Approved layout: `read()` in the clause reader returns clauses, scenarios,
glossary terms, elicitation entries, and syntactic findings; `trace.py`
adds `link_findings()` (the link checks of T3), `build()` (pure: specs and
citations in, report text and findings out, so that the cases can call it
without running pytest), `collect_citations()` (an in-process
`pytest.main(["--collect-only", ...], plugins=[collector])` with the
terminal reporter disabled), and `main()`. The finding vocabulary is the
set of kind strings in both modules; the cases are the twelve directories
listed on [tooling-tests.md](tooling-tests.md).

## Review points

Citations come from pytest's own collection, so the tool and the plugin can
never disagree about what a test cites; every finding carries a file and
line or an identifier; the forward and backward tables are built from the
same records; a story with no requirement is a finding even though every
link resolves; `build()` has no side effects, which is what makes T7
possible; the tool never reads the ledger or the dev log.

## Deliberate-failure checks

`uv run pytest tests/tooling` runs the base and the twelve cases. Two
sabotages on the real specifications, both observed on 2026-10-22: changing
REQ-3's derivation to `US-2` (every link resolves; the finding is "story
without requirement at US-1"), and to `US-9` (two findings: the dangling
reference and the story it left behind).

## Adapting it to your project

Project-specific: the clause reader it uses; the citation mechanism (another
framework's markers, or a comment convention read by the tool); the link
kinds (allocation to a component arrives in A2). Carries over as an idea: a
link vocabulary declared on the clauses, a tool that resolves it both ways,
findings as a fixed vocabulary with cases, and a report that says its scope.

## Making it shared infrastructure

Share it together with the clause reader and the header format they both
read (see [clause-reader.md](clause-reader.md)); the link vocabulary is the
part an organization fixes once. Version the finding vocabulary: a project's
dev log cites finding kinds, and renaming one silently changes what old
entries mean.
