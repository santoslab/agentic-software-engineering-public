# The scenario loader: `tests/test_scenarios.py`

## Goal

Run every acceptance scenario of `specs/scenarios.json` as a test that cites
the story it derives from, so that a story's behavioral evidence is a passing
test rather than a person's observation. Rule CONF-1 then covers the stories
like any other *test* clause. The scenario file is a specification (values
only, readable by a stakeholder, portable to any realization); the loader is
the one place that binds it to this realization's interface.

## Requirements

1. One parametrized test; one case per scenario; the case id is the
   scenario's identifier, so that a failure names it.
2. Each case carries the marker `req(<derived_from>)`, so that the
   conformance report lists it under the story.
3. Builds the message from the scenario's input through the public
   interface, calls `filter_message`, and compares the output with
   `expected` by value: `null` means no output.
4. Reads the file at collection time; never edits it, and never skips a
   scenario.
5. If the file is malformed, collection fails (rule RQ-1 catches it before
   any evidence is produced).

## The prompt

New in A1; written by the build agent from the A1 plan's section 5.4, which
fixed the file's shape and these five requirements. The prompt a developer
would give:

> Write a pytest module that turns every scenario in `specs/scenarios.json`
> into a parametrized case, cites the story each scenario derives from with
> the `req` marker, builds the message through the package's public
> interface, and compares the output by value. The file is a specification:
> read it, never change it, never skip an entry.

## Review points

Each case is marked with the scenario's `derived_from`, not with a constant;
the comparison is by value (level and payload), not by object identity; a
`null` expectation asserts that nothing came out; the test imports only the
public interface.

## Deliberate-failure checks

A1's sabotage 7: change `filter.py` and the unit test
`test_restricted_passes_unchanged` together so that both read "unchanged"
as "payload normalized to non-negative" (a shared misreading); the unit test
passes and `SC-2`, whose expectation was written from the stakeholder's
words, fails. Observed on 2026-10-22 in the trial run. This is the
independence point (threat T5): the scenario file was authored on the
specification side, so it does not share the realization's mistake.

## Adapting it to your project

Project-specific: the message constructor and the function under test; the
scenario schema. Carries over as an idea: one loader per realization, one
scenario file per system, and the file governed on the specification side
(never edited to make a test pass).

## Making it shared infrastructure

The scenario file's schema is the shareable part: an organization that fixes
one schema can share one loader per language and run every realization of a
system, in every language, against the same file. The HAMR version of this
guard in Rust would read the same file.
