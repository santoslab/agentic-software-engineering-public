# The game demo

One demonstration, run across Lectures 03 and 04, on a command-line
five-in-a-row tic-tac-toe (a 9-by-9 grid). Lecture 03 takes a sketch of a
concept of operations to a full concept of operations and then to a behavioral
contract of several kinds, and builds the game from it; Lecture 04 verifies
the build with a test suite, a coverage gate, and fixtures.

| Lecture | Script | Starts from | Ends at |
|---|---|---|---|
| 03 | `demo-script-lecture-03.md` | `starter/` (`t0`) | the implementation (`t3`) |
| 04 | `demo-script-lecture-04.md` | `t3` | the L04 process set, tests, the gate, fixtures (`t5`) |

## Folders

- `starter/` — the state at the start of Lecture 03, tag `t0`: `CONOPS-sketch.md`
  (the client's general idea; incomplete on purpose), `CLAUDE.md` (the loader),
  `process/` (the L03 set), `BACKLOG.md`. No `CONOPS.md`, no `SPECS.md`, no code.
- `reference/` — the destination, `t5`: `CONOPS.md` 1.0, `SPECS.md` 1.2.1 (§9
  holds the verification obligations; the policy is in
  `process/verification.md`), the three approved plans under `plans/`, the three
  modules, 85 unit tests and a fixture loader over the 14 scenarios of
  `fixtures/scenarios.json`, the L04 `process/`, `BACKLOG.md`. The gate is green at 100% branch coverage
  (confirmed 2026-09-22 in a venv with `pytest-cov`). A live run does not
  reproduce this folder; it shows the shape of `t2` through `t5`. The
  implementation was produced from an earlier version of the specification
  that was silent on a move after the game is over — the clause Lecture 03's
  round 2 puts into the demo's `SPECS.md` 1.0.0. `plans/` holds the three DEV-9
  plans from that history: `001-engine-opponent-cli.md` and `002-test-suite.md`
  written against `SPECS.md` 1.1.0, and `003-fixture-loader.md` against 1.2.0.
  The first two inherit the same silence — 001's `make_move` step realizes the
  rejection cases §5.1 listed at 1.1.0 and no others, and 002's matching step
  realizes the three failure obligations §9.5 listed at 1.1.0 and no others —
  which is what lets Lecture 04's Segment 4 follow one omission through five
  artifacts. They are also the fallback artifacts for Lecture 03's Segment 4 and
  Lecture 04's Segment 2 when the rehearsal repository's tags are not to hand.
  The reference's 1.2.0 adds
  that clause, and the engine change and the test citing it follow the
  amendment; Lecture 04 reads that history as its DEV-2 (c) example.

## Tags

The demo repository is built once at rehearsal and tagged at every state a
lecture may stop at or start from: `t0-conops-sketch`, `t1-conops`,
`t2-spec-family`, `t3-engine`, `t4-tests-100`, `t5-fixtures`. Anything the agent
takes longer than about two minutes to produce is shown from its tag, never
waited for. Lecture 04 starts from `t3` whatever Lecture 03 reached.

`process/` in `starter/` is installed from the L03 template set and is not
edited here; at the start of Lecture 04 it is upgraded to the L04 set by an
amendment commit, which the lecture shows. `reference/CLAUDE.md` and
`reference/process/` are that L04 set; `reference/fixtures/` is the file
`scenarios.json` shared with the project unit, with a README stating its
assumptions and blind spots (VER-7).
