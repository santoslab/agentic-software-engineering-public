# Implementation Plan: Five-in-a-Row Tic-Tac-Toe

**Branch**: `001-five-in-a-row` | **Date**: 2026-10-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-five-in-a-row/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

A terminal game of tic-tac-toe on a 9×9 board where five or more in a line wins, played
against a random computer opponent or by two people at one keyboard (spec FR-001 –
FR-020). The design splits the program into three modules with a one-way dependency rule
so each can evolve on its own:

- **engine** — rules only: an immutable `GameState` whose `play(square)` validates the
  move, places the mark, and determines win/draw. No I/O.
- **opponent** — an `Opponent` protocol (`choose_move(state) -> Square`) with one
  strategy, `RandomOpponent`, choosing uniformly among empty squares.
- **cli** — menus, prompts, input parsing, board drawing, and the session (mode, and the
  human's mark against the computer). The only module that does I/O.

Evidence of conformance is a pytest suite whose tests are tagged with spec IDs, plus a
generated conformance report listing every spec ID and its evidence (constitution
Principles I and V).

## Technical Context

**Language/Version**: Python ≥ 3.12 (developed on 3.14) — research.md R1

**Primary Dependencies**: none at run time (standard library only); pytest for tests

**Storage**: N/A — nothing is saved between runs (spec Assumptions)

**Testing**: pytest, run through `uv` — research.md R2; requirement tagging and report — R7

**Target Platform**: a text terminal on macOS (the developer's laptop); nothing
platform-specific is used, so Linux/Windows terminals are expected to work too

**Project Type**: CLI application structured as an installable Python package with three
internal modules

**Performance Goals**: board and next prompt within 1 s of a computer move (SC-005);
first move possible within 15 s of launch (SC-001). Both are far above what the design
needs.

**Constraints**: offline, single process, one keyboard; no third-party run-time
dependencies; terminal I/O confined to `cli`

**Scale/Scope**: one board of 81 squares, at most 81 moves per game, one player session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution v1.0.1.

| Principle | How this plan complies | Pre-research | Post-design |
|-----------|------------------------|:---:|:---:|
| **I. Specification and Realization** | Spec (`spec.md`) and realization (`src/`) are kept separate. Each contract lists the evidence it expects; tests are tagged with the spec IDs they evidence (R7). | PASS | PASS |
| **II. Specification Before Realization** | All realization work in this feature is case (c): it follows the spec. Design choices the spec leaves open are recorded as such (research.md R3–R8), so later changes to them are case (b) and need no spec change. | PASS | PASS |
| **III. A Person Decides Which Side Changes** | When a test fails, the plan does not say whether spec or code moves; tasks must stop and ask. Spec changes go in `specs/001-five-in-a-row/CHANGELOG.md`; code changes record the decision in the commit message. | PASS | PASS |
| **IV. Derived Documents Follow Governing Ones** | This plan and its artifacts are derived from `spec.md` and do not contradict it. One gap found during design (end of input / interrupt) was raised as **proposal P1** in research.md rather than decided by the plan; the developer accepted it and it is now spec FR-020, implemented by `contracts/cli.md` C-17. | PASS | PASS |
| **V. Reports** | `reports/conformance.md` is generated on every test run, mapping each spec ID to its tests and their status and flagging IDs with no evidence (R7). The spec's acceptance scenarios serve as the explanatory examples; the CLI contract adds sample screens. | PASS | PASS |
| **Document Hierarchy** | Contracts cite the spec IDs they implement; where a contract says more than the spec (menu numbers, `m` command, separators), it is a choice inside what the spec leaves open (FR-004, FR-018) — see research.md R8. | PASS | PASS |
| **Records of Change** | Applies from implementation on; nothing here changes the spec. | PASS | PASS |

No violations; Complexity Tracking is not needed.

## Project Structure

### Documentation (this feature)

```text
specs/001-five-in-a-row/
├── spec.md              # governing specification
├── CHANGELOG.md         # specification changelog (constitution, Records of Change)
├── plan.md              # this file
├── research.md          # Phase 0: decisions R1–R8, proposal P1
├── data-model.md        # Phase 1: entities, validation, state transitions
├── quickstart.md        # Phase 1: how to validate the feature
├── contracts/
│   ├── engine.md        # engine public API
│   ├── opponent.md      # Opponent protocol and RandomOpponent
│   └── cli.md           # screens, input rules C-1 – C-17
├── checklists/
│   └── requirements.md  # spec quality checklist
└── tasks.md             # Phase 2 (/speckit-tasks; not created here)
```

### Source Code (project root `SpecKit/TicTacToe/`)

```text
pyproject.toml                    # package metadata, console script, pytest dev group
uv.lock                           # locked dev environment (committed)
README.md                         # how to run the game and the tests
src/five_in_a_row/
├── __init__.py
├── __main__.py                   # python -m five_in_a_row → cli.main()
├── engine/
│   ├── __init__.py               # public API: SIZE, WIN_LENGTH, Mark, Square, Result,
│   │                             #   Board, GameState, IllegalMove, IllegalMoveReason
│   ├── board.py                  # Mark, Square, Board
│   └── state.py                  # Result, GameState, IllegalMove, win detection
├── opponent/
│   ├── __init__.py               # public API: Opponent, RandomOpponent
│   ├── base.py                   # Opponent protocol
│   └── random_opponent.py
└── cli/
    ├── __init__.py               # public API: run, main
    ├── app.py                    # session loop: start menu, game, game-over menu
    ├── parse.py                  # move and menu entry parsing (C-1, C-7 – C-9)
    └── render.py                 # board drawing and message text (C-5, C-10, C-12)

tests/
├── conftest.py                   # conformance-report plugin: records `req` tags, writes report (R7)
├── conformance.py                # reads spec IDs from spec.md (used by conftest.py)
├── positions.py                  # shared board positions and move sequences
├── test_conformance.py           # checks the spec-ID reader against spec.md
├── test_architecture.py          # enforces the dependency rule (R3)
├── test_manual_checks.py         # placeholders for manually checked criteria (SC-002)
├── engine/                       # evidence for contracts/engine.md
├── opponent/                     # evidence for contracts/opponent.md
└── cli/                          # transcript tests for contracts/cli.md
    └── conftest.py               # ScriptedOpponent fake and session helper

reports/                          # generated; git-ignored
└── conformance.md
```

**Structure Decision**: a single installable package with three subpackages, one per
module the feature names. The dependency rule `cli → opponent → engine` (and
`cli → engine`) is enforced by `tests/test_architecture.py`, and each subpackage's
`__init__.py` is its public API. Each subpackage has its own test directory and contract,
so a future change to one module — a smarter opponent, a different front end, a rule
variant — is made and verified against that module's contract alone.

### How each module can evolve independently

| Future change (ConOps §4, spec Assumptions) | Module that changes | Untouched |
|---------------------------------------------|---------------------|-----------|
| Smarter computer opponent | `opponent`: add a class satisfying `Opponent`; CLI picks it via `opponent_factory` | engine; CLI apart from one line choosing the strategy |
| Running score across games | `cli`: session gains a tally | engine, opponent |
| A different front end (e.g. curses, GUI) | new front-end package beside `cli` | engine, opponent |
| Rule variant (board size, run length) | `engine`: `SIZE` / `WIN_LENGTH` | opponent (uses `empty_squares()`); CLI drawing reads `SIZE` |

## Open Items for the Developer

None. Proposal P1 (end of input / interrupt) was accepted on 2026-10-08 and is now spec
FR-020.

## Complexity Tracking

Not needed — the Constitution Check found no violations.
