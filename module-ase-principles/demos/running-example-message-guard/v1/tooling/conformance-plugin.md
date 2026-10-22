# The conformance plugin: `tests/conftest.py`

## Goal

Turn the suite's citations and outcomes into **requirements coverage**: one
row per identified clause saying which tests cite it and whether they passed,
written to `reports/conformance.md` after every run, and fail the run when a
clause assigned method *test* has no passing evidence or a marker names a
clause that does not exist. Rule CONF-1 names it for requirements coverage;
rule TR-1 for the resolution of markers. It is the mechanism behind "a green
suite is not conformance": the suite can pass while a clause has no test.

## Requirements

1. Reads clauses through the clause reader; never from a list of its own.
2. Collects, from every test, the identifiers in its `req` markers;
   `--strict-markers` in `pyproject.toml` rejects an undeclared marker before
   any test runs.
3. Records each cited test's outcome (passed, failed, skipped).
4. After the session, writes the report: a header naming the files read, the
   number of tests collected and the number that cite a clause; a **scope
   line** saying full run or partial run; the requirements-coverage count;
   one row per clause; the legend; unknown identifiers; the reader's
   findings.
5. A *test* clause's status is pass, FAIL, partial, or no evidence; a
   walkthrough or review clause is not decided by the run and its row points
   at the record file.
6. Fails the run (exit as if a test failed) on any no-evidence or FAIL
   clause, any unknown identifier, or any reader finding, unless tests were
   deselected, in which case the report is written, labeled partial, and the
   gate is not applied.
7. Tests may omit citations; they still run, still count toward structural
   coverage, and still fail the suite if they fail.
8. The terminal summary names each gap, so that a red run says why.

## The prompt

Inherited from A0, adapted from the Spec Kit demo (the provenance chain is
on [clause-reader.md](clause-reader.md)). The A1 extensions, the scope line,
the findings section, and story rows backed by scenario tests, were written
by the build agent from the A1 plan's N11.

Guidance for the prompt that would produce it from nothing (it is the one
Lecture 01 gives as the example of asking for a tool rather than a report):

> Read the identified clauses from these specification files, show the tests
> citing each test clause and their outcomes, identify missing evidence and
> invalid citations, distinguish a partial run from a full run, and fail the
> run on a missing or failing citation. Propose the report's layout and the
> status vocabulary first, and say what the plugin will not decide.

## Review points

The clause list comes from the reader; a clause with no citing test fails
the run rather than being omitted; a partial run cannot be mistaken for a
full one when the saved file is read alone; the report says how many tests
were collected and how many cite a clause, so that an uncited test is
visible; the legend says what a citation does not establish (assertion
adequacy).

## Deliberate-failure checks

Four scripted demonstrations, run from a scratch copy of the snapshot (also
listed in the README under "Breaking the verifiers"):

1. **An uncited passing test is accepted.** Add `def test_extra(): pass` to
   any test file; the gate stays green and the report's "cite a clause" count
   is unchanged.
2. **An invalid citation is rejected.** Change a marker to `"REQ-9"`; the
   report lists it under "Unknown identifiers" and the run fails.
3. **A test clause with no citing test is a coverage gap.** Delete
   `test_public_passes_unchanged`; every remaining test passes, branch
   coverage stays at 100 percent, and the run fails with "REQ-3: no
   evidence".
4. **An uncited failing test fails the suite while every clause row stays
   green.** Add `def test_uncited_failure(): assert False`; pytest reports one
   failure and the plugin still prints "every test clause has passing
   evidence". The clause table and the suite result are two different
   claims, and the gate's exit code is the one that counts; A2's generated
   ledger must read the suite result, not the table (CF-08).

Observed on 2026-10-22 in the trial run of this snapshot: 1 and 4 as
described; 2 and 3 are A0's sabotages 5 and 3, unchanged.

## Adapting it to your project

Project-specific: the marker name and the test framework's hook API (this is
pytest's `pytest_collection_modifyitems`, `pytest_runtest_logreport`,
`pytest_sessionfinish`); the report path; the status vocabulary if the
organization has one. Carries over as an idea: citations in tests, a
generated report over the specification's identifiers, and a run that fails
on absence, not only on failure. Another language needs its own way to cite
a clause from a test and its own coverage tool.

## Making it shared infrastructure

This is the tool most worth sharing: package it as a pytest plugin
(`pyproject.toml` entry point `pytest11`) that takes the clause reader and
the report path as configuration, so that product repositories carry only
their specifications and markers. Version it; a plugin defect gives every
project the same misleading green, which is why the deliberate-failure
demonstrations ship with it and run on every release.
