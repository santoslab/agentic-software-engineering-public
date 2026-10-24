# Walkthrough Record and Sign-off: Message Guard (version A0)

## Walkthroughs (ConOps-CONF-1)

Each user story is a judgment clause with method *walkthrough (human)*. A
person, in the role the story names, gives the guard the story's example with
the helper `tools/walk.py` and judges what they observe.

Walked by: the instructor, playing each role · Date: 2026-10-20 · Realization:
the A0 snapshot (`a0`) · Command: `uv run python tools/walk.py LEVEL PAYLOAD`

| Clause | Role | Command | Observed | Finding |
|---|---|---|---|---|
| US-1 | message sender | `tools/walk.py Public 42` | `pass: Public 42` | as the story expects |
| US-2 | message sender | `tools/walk.py Restricted 7` | `pass: Restricted 7` | as the story expects |
| US-3 | security officer | `tools/walk.py Critical 100`, then `Critical 0` | `drop`, both times | as the story expects |

## Sign-off (ConOps-VAL-1)

"The concept of operations, version A0, describes the guard I intend: a
Critical message never leaves, and anything else leaves as it arrived."

- Security officer: role played by the instructor, 2026-10-20, on
  `specs/conops.md` version A0.
- Message sender: role played by the instructor, 2026-10-20, on
  `specs/conops.md` version A0.

In a real project the two lines are signed by two different people. The
sign-off is kept even after tests exist for the stories (later versions),
because the question it answers, whether these are the right stories, is one
no test can answer.
