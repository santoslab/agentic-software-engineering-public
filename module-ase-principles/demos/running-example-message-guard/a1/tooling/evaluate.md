# The evaluation command: `tools/evaluate.sh` and the pytest configuration

## Goal

One command that runs every mechanical evaluation of `process/judgments.md`
and exits non-zero at the first failure: realization quality (Code-RQ-1),
the test evidence for the requirements and the scenarios (Reqs-CONF-1 and
Scen-CONF-1, through the plugin and `pytest-cov`), and traceability
(Specs-TR-2 and the reference parts of Specs-TR-1, through the trace tool).
It is what the assurance report's procedure runs in its step 2, and its
header is what the report quotes as provenance. It is **not a gate**:
nothing in A1 runs it unasked, and nothing waits for its exit code. It
evaluates. A program whose exit code decides a transition, a hook or a CI
job, is the control layer, and that arrives with A2; the script is written so
that A2 can put it behind one without changing it.

## Requirements

1. Runs, in order, `ruff check .`, `pytest` (with the coverage threshold and
   the conformance plugin, both configured in `pyproject.toml`), and
   `tools/trace.py`; stops at the first failure; exit 0 means every
   mechanical clause holds for the tree it was run on.
2. Prints a provenance header first: the date; the repository state (HEAD
   and the number of changed or untracked paths, so that a run on a dirty
   tree says so); the versions of Python, pytest, pytest-cov, ruff, and the
   trace tool. The assurance report copies this header (the hand convention
   for CF-07; the tree-hash mechanism is A2's).
3. Runs from the snapshot root wherever it is invoked from.
4. Contains no policy of its own: the coverage threshold, the marker
   declaration, and the test paths live in `pyproject.toml`, where a reader
   looks for them, and the clauses it evaluates are named in its header
   comment, not decided by it.

## The prompt

Inherited from A0 (the evaluation command of A0's dev-log entry 2); the
provenance header and the trace step were added by the build agent in A1
from requirements 2 and 1. Guidance for the prompt that would produce it:

> Write one command that runs every evaluation the judgments file assigns to
> a program: lint, then the suite with its coverage threshold and the
> conformance plugin, then the trace tool, failing at the first red step.
> Print, before anything runs, what state is being checked and by which tool
> versions. Keep thresholds out of the script, and do not make it decide
> anything about commits.

## Review points

The script carries no threshold; the order is lint, suite, trace (a suite
that does not collect should fail before a trace is attempted); the header
reports a dirty tree honestly; the exit code is the last step's only because
every earlier step would have stopped the script; the header comment names
the clauses, so that a reader can see which rows of the report one run
covers.

## Deliberate-failure checks

Each step has its own: a lint error (add an unused import to `guard/`), a
failing test (A0's sabotage 1), a coverage gap (A0's sabotage 4 in the form
`payload < -1000`, since the original `payload < 0` is now caught by
scenario SC-2 before the coverage tool sees it), a dangling reference (A1's
sabotage 8). The command must exit non-zero on each and the header must
show the dirty tree. All four observed on 2026-10-22 in a trial copy of this
snapshot: ruff "F401 imported but unused"; four tests and three clause rows
FAIL; coverage 94 percent with every clause cited; "story without
requirement at US-1".

## Adapting it to your project

Project-specific: every command. Carries over as an idea: one command, one
exit code, a header that says what was checked, no policy in the script, and
a comment that names the clauses it evaluates. For a project with no test
framework, the command is whatever evaluates the mechanical clauses: a
schema validator, a type checker, a build.

## Making it shared infrastructure

Keep the command as a thin script that calls shared tools; the policy lives
in configuration files the organization templates. A git pre-commit hook or
a CI job that runs the same script turns the evaluation into a gate, which is
a decision about process, not about the script; A2's build plan decides when
enforcement is wanted and at which checkpoints.
