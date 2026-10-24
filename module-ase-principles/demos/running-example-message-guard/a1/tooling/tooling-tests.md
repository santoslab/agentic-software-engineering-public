# The tooling tests: `tests/tooling/`

## Goal

Show the clause reader and the trace tool failing on inputs they must fail
on, before their findings are trusted. A verifier that has never been seen to
fail has not been verified (threat T2); these cases are the two programs'
known-violation set, run with the suite at every commit. They cite no
clause: they are tests of verifiers, not evidence for a product requirement,
and the suite accepts them uncited (Specs-TR-1).

## Requirements

1. `cases/base/` is a minimal, clean family: one story with one scenario,
   two requirements (one derived from the story, one from a glossary term),
   a glossary, an elicitation entry, and a citation file; it must produce no
   finding.
2. Each other directory overlays one or two files on the base and states in
   `expected.json` the finding kinds the tool must report, and why.
3. `test_trace.py` copies the base, overlays the case, reads it with the
   clause reader, calls `tools.trace.build()` with the case's citations,
   and compares the sorted set of finding kinds with the expectation.
4. One case per finding kind; adding a kind to the tools means adding a
   case here.

## The prompt

New in A1, written by the build agent from T7 of the trace tool's
requirements. The prompt a developer would give:

> For each finding kind of the clause reader and the trace tool, make a
> directory that overlays the smallest change on a clean base family and
> states the expected finding kinds; write one parametrized test that runs
> every directory through the tool's pure `build()` function. The base must
> be clean.

## Review points

The cases exercise `build()` directly, so no pytest-in-pytest run is
needed; the overlay keeps every case small enough to read; `expected.json`
says *why*, so that a reader learns what each kind means; the base is itself
a test.

## Deliberate-failure checks

The cases are the checks. Sabotage 10 of the README is the meta-check:
delete one case directory and nothing fails, which is the point: a finding
kind with no case is a finding kind nobody has seen the tool report.

| Case | Finding kinds expected |
|---|---|
| `base` | none |
| `duplicate-identifier` | duplicate identifier |
| `missing-method` | malformed header |
| `unknown-method` | unknown method |
| `unknown-key` | unknown key |
| `unknown-pattern` | unknown pattern |
| `missing-reason` | missing Reason |
| `dangling-derived-from` | dangling reference; story without requirement |
| `dangling-scenario` | dangling reference |
| `scenario-not-listed` | scenario not listed |
| `story-without-requirement` | story without requirement |
| `dangling-marker` | dangling marker |
| `test-clause-without-test` | test clause without a citing test |

## Adapting it to your project

Project-specific: the base family's content and the finding vocabulary.
Carries over as an idea: every program that produces evidence ships with the
inputs it must fail on, and those inputs are checked in beside it.

## Making it shared infrastructure

The cases travel with the tools they test; a shared reader and trace tool
ship their cases as part of the package's own test suite, and a project that
extends the finding vocabulary adds its cases in its own repository.
