# The walkthrough helper: `tools/walk.py`

## Goal

Let a person, in the role a story names, give the guard one message and see
what it does, so that a walkthrough is an observation of the running system
and not a reading of the code. In A0 it produced the evidence for rule
CONF-2 (the stories' behavioral walkthroughs); in A1 the behavioral check
has become the scenario tests, and the helper serves rule VAL-2, the
validation walkthrough in which a stakeholder decides whether the story
describes the guard they want.

## Requirements

1. `uv run python tools/walk.py LEVEL PAYLOAD` prints `drop` or
   `pass: LEVEL PAYLOAD`, nothing else.
2. A level or payload that is not a message is reported as such, with exit
   code 2, rather than crashing.
3. Lives outside the package and outside the coverage measurement: it
   realizes no clause.
4. Unchanged from A0 in behavior; its docstring names the record file it
   serves, which audit 05 noticed still said `reports/walkthrough.md` after
   the rename, and now says `reports/validation.md`.

## The prompt

Inherited from A0, dev-log entry 2. Guidance for the prompt that would
produce it:

> Write a tiny command that builds one message from two arguments, passes it
> through the guard, and prints what came out, so that a stakeholder can
> walk a story without reading Python. Keep it outside the package.

## Review points

It prints what the guard returned, not what the story expects (the
comparison is the person's); it is not imported by any test; it is not
counted in coverage.

## Deliberate-failure checks

None of its own, by design: it is a window, not a verifier. A0's sabotage 1
(the condition changed to Restricted) is visible through it, which is how the
validation walkthrough would catch a wrong realization that no test covered.

## Adapting it to your project

Project-specific: everything. Carries over as an idea: a walkthrough needs a
way to exercise the system along a scenario without touching the code, and
that way should be in the repository, because the walkthrough record cites
it.

## Making it shared infrastructure

Not worth sharing as code; worth sharing as a convention: every project has a
`walk` entry point that takes a scenario's inputs and prints the observable
output, in the words of the concept of operations.
