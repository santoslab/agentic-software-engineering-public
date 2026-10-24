# Validation Record and Sign-off: Message Guard (version A1)

## Validation walkthroughs (ConOps-VAL-1)

In A0 the stories' behavioral examples were walked by a person, and that
walkthrough was the evidence for ConOps-CONF-1, since retired. In A1 the behavioral evidence
is the scenario tests (`tests/test_scenarios.py`; the story rows of
`reports/conformance.md`), and the walkthrough has one purpose left: a
stakeholder of each user category exercises the running guard along their
stories, with the scenarios' inputs, and decides whether the stories
describe the guard they want. Seeing the expected output does not by itself
answer that question. The decision is recorded here, and the sign-off
follows it.

Walked by: the build agent playing each role, on the instructor's behalf (as
in A0, one person plays both roles; the instructor can re-play the session
and record a new table) · Date: 2026-10-22 · Realization: the a1 working
tree, in which `guard/` is byte-identical to a0 · Command:
`uv run python tools/walk.py LEVEL PAYLOAD`

### Message sender

| Story | Scenarios | Commands | Observed | Decision |
|---|---|---|---|---|
| US-1 | SC-1, SC-2 | `walk.py Public 42`; `walk.py Public -3` | `pass: Public 42`; `pass: Public -3` | the story says what I want: what I send that may leave comes out as I sent it, whatever the number in it |
| US-2 | SC-3, SC-4 | `walk.py Restricted 7`; `walk.py Restricted 150` | `pass: Restricted 7`; `pass: Restricted 150` | as above; the 150 case shows that nothing is cut down in this version, which is what I was told and what I expect |

### Security officer

| Story | Scenarios | Commands | Observed | Decision |
|---|---|---|---|---|
| US-3 | SC-5, SC-6 | `walk.py Critical 100`; `walk.py Critical 0` | `drop`; `drop` | the story says what I want: nothing marked Critical leaves, whatever its payload |
| Deferred wants D-1 to D-3 | read, not walked | — | — | they are mine, recorded as deferred, and not promised here; I sign for A1 with them deferred |

## Sign-off (ConOps-VAL-1, continued)

"The concept of operations, version A1, describes the guard I intend: the
marking alone decides, a Critical message never leaves, and anything else
leaves as it arrived. The three deferred wants are mine and are not promised
in this version."

- Security officer: role played by the build agent on the instructor's
  behalf, 2026-10-22, on `specs/conops.md` version A1 (the text of commit
  a1-specs, unchanged through a1 except for the stories' method and
  `Scenarios` fields).
- Message sender: role played by the build agent on the instructor's
  behalf, 2026-10-22, on `specs/conops.md` version A1.

In a real project the two lines are signed by two different people, and the
instructor's own re-play of this session supersedes these lines when it is
recorded. The sign-off is kept although tests now exist for the stories: the
question it answers, whether these are the right stories, is one no test can
answer. A stakeholder who, at this walkthrough, had said that a Restricted
message with a payload above 100 must not leave would have withheld the
signature while every scenario passed (README, sabotage 9); the resolution
is a sign-off scoped to the version with the want deferred, as here for
D-2, or, in A3, a change request.

## Earlier records, kept for the assurance reports' citations

This file was `records/walkthrough.md` at a0 and at a1-specs; the assurance
reports compiled at those commits cite it under that name. Its earlier contents
follow unchanged.

### Walkthroughs at a0 (version A0; ConOps-CONF-1)

Walked by: the instructor, playing each role · Date: 2026-10-20 · Realization:
the A0 snapshot (`a0`) · Command: `uv run python tools/walk.py LEVEL PAYLOAD`

| Clause | Role | Command | Observed | Finding |
|---|---|---|---|---|
| US-1 | message sender | `tools/walk.py Public 42` | `pass: Public 42` | as the story expects |
| US-2 | message sender | `tools/walk.py Restricted 7` | `pass: Restricted 7` | as the story expects |
| US-3 | security officer | `tools/walk.py Critical 100`, then `Critical 0` | `drop`, both times | as the story expects |

### Sign-off at a0 (version A0; ConOps-VAL-1)

"The concept of operations, version A0, describes the guard I intend: a
Critical message never leaves, and anything else leaves as it arrived."

- Security officer: role played by the instructor, 2026-10-20, on
  `specs/conops.md` version A0.
- Message sender: role played by the instructor, 2026-10-20, on
  `specs/conops.md` version A0.

### Walkthroughs of the revised stories at a1-specs (version A1; ConOps-CONF-1)

Walked by: the build agent, playing each role on the instructor's behalf ·
Date: 2026-10-22 · Realization: the a1-specs working tree (`guard/`
unchanged from a0) · Command: `uv run python tools/walk.py LEVEL PAYLOAD`

| Clause | Role | Command | Observed | Finding |
|---|---|---|---|---|
| US-1 | message sender | `walk.py Public 42`; `walk.py Public -3` | `pass: Public 42`; `pass: Public -3` | as the story expects |
| US-2 | message sender | `walk.py Restricted 7`; `walk.py Restricted 150` | `pass: Restricted 7`; `pass: Restricted 150` | as the story expects |
| US-3 | security officer | `walk.py Critical 100`; `walk.py Critical 0` | `drop`; `drop` | as the story expects |
