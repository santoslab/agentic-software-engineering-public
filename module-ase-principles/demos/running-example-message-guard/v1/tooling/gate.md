# The gate: `tools/gate.sh` and the pytest configuration

## Goal

One command whose exit code decides, before any commit, realization quality
(rule RQ-1), the mechanical part of conformance (CONF-1, through the plugin
and `pytest-cov`), and traceability (TR-2, through the trace tool). Rule
WF-1 names it. It is an *algorithmic gate*: a program decides, and the
decision is an exit code that a hook or a CI job could enforce. In A1 it is
prescribed, not enforced: nothing stops a commit made without running it,
and the dev log is where the run is recorded.

## Requirements

1. Runs, in order, `ruff check .`, `pytest` (with the coverage threshold and
   the conformance plugin, both configured in `pyproject.toml`), and
   `tools/trace.py`; stops at the first failure; exit 0 is green.
2. Prints a provenance header first: the date; the repository state (HEAD
   and the number of changed or untracked paths, so that a run on a dirty
   tree says so); the versions of Python, pytest, pytest-cov, ruff, and the
   trace tool. The dev-log entry for a commit copies this header (the hand
   convention for CF-07; the tree-hash mechanism is A2's).
3. Runs from the snapshot root wherever it is invoked from.
4. Contains no policy of its own: the coverage threshold, the marker
   declaration, and the test paths live in `pyproject.toml`, where a reader
   looks for them.

## The prompt

Inherited from A0 (the gate command of A0's dev-log entry 2); the provenance
header and the trace step were added by the build agent in A1 from
requirements 2 and 1. Guidance for the prompt that would produce it:

> Write the one command rule WF-1 names: lint, then the suite with its
> coverage threshold and the conformance plugin, then the trace tool, failing
> at the first red step. Print, before anything runs, what state is being
> checked and by which tool versions. Keep thresholds out of the script.

## Review points

The script carries no threshold; the order is lint, suite, trace (a suite
that does not collect should fail before a trace is attempted); the header
reports a dirty tree honestly; the exit code is the last step's only because
every earlier step would have stopped the script.

## Deliberate-failure checks

Each step has its own: a lint error (add an unused import to `guard/`), a
failing test (A0's sabotage 1), a coverage gap (A0's sabotage 4 in the form
`payload < -1000`, since the original `payload < 0` is now caught by
scenario SC-2 before the coverage tool sees it), a dangling reference (A1's
sabotage 8). The gate must go red on each and the header must show the
dirty tree. All four observed on 2026-10-22 in a trial copy of this
snapshot: ruff "F401 imported but unused"; four tests and three clause rows
FAIL; coverage 94 percent with every clause cited; "story without
requirement at US-1".

## Adapting it to your project

Project-specific: every command. Carries over as an idea: one command, one
exit code, a header that says what was checked, and no policy in the script.
For a project with no test framework, the gate is whatever decides the
mechanical clauses: a schema validator, a type checker, a build.

## Making it shared infrastructure

Keep the gate as a thin script that calls shared tools; the policy lives in
configuration files the organization templates. A git pre-commit hook or a
CI job that runs the same script turns the prescribed gate into an enforced
one; A2's build plan decides when enforcement is wanted and at which
checkpoints.
