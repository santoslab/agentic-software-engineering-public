# Research: Five-in-a-Row Tic-Tac-Toe

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Date**: 2026-10-08

Each entry records a decision the plan makes in the space the specification deliberately
leaves open. None of them changes specified behavior. Where planning found something the
specification does not settle and that is not merely a design choice, it is listed under
[Proposed specification corrections](#proposed-specification-corrections) instead of being
decided here (constitution, Principle IV).

## R1. Language and runtime

- **Decision**: Python 3.12 or later, standard library only at run time.
- **Rationale**: The program is a small text game on one laptop (spec, Assumptions); it
  needs no third-party run-time libraries. Python 3.14 is already installed, `uv` is
  available for environments, and the sibling experiments in `tic-tac-toe-project/` use
  Python + pytest, so results stay comparable across experiments. 3.12 is the floor
  because it is the oldest release still receiving security fixes and has every language
  feature the contracts use (dataclasses with `slots`, `enum`, `typing.Protocol`).
- **Alternatives considered**: Java (the `9by9_Java` sibling) — more ceremony for a
  single-process console program; Rust/Go — no benefit at this scale and less familiar
  for a teaching example.

## R2. Test framework and environment

- **Decision**: pytest (development-only dependency), environment and runs managed with
  `uv` (`uv run pytest`).
- **Rationale**: pytest's plain `assert` style keeps tests readable as evidence
  (Principle I); markers give a cheap way to tag each test with the requirement it
  provides evidence for (R7). `uv` creates the environment from `pyproject.toml` with one
  command and needs nothing installed globally.
- **Alternatives considered**: `unittest` (no install, but no markers and noisier tests);
  plain `venv` + `pip` (works; `uv` is faster and already present — `venv` remains a
  documented fallback in quickstart).

## R3. Separating engine, opponent, and CLI so each can evolve independently

- **Decision**: Three subpackages of one distribution package, with a one-way dependency
  rule:

  ```text
  cli  ──▶  opponent  ──▶  engine
   └──────────────────────▶  engine
  ```

  - `engine` imports nothing from the other two and does no I/O.
  - `opponent` imports only `engine`'s public API.
  - `cli` imports both public APIs and is the only place with terminal I/O.
  - Each subpackage exposes its public API from its `__init__.py`; other subpackages
    import only from there. The rule is checked by a test (`tests/test_architecture.py`)
    that inspects imports.
- **Rationale**: The three foreseeable evolutions (spec §Assumptions, ConOps §4) land in
  different places: a smarter computer replaces the opponent only; a running score or a
  different front end changes the CLI only; rule variants (board size, run length) change
  the engine only. A one-way rule means a change in one never forces a change in a module
  that sits "below" it, and the contracts in `contracts/` are the only coupling.
- **Alternatives considered**: three separately versioned distributions (overkill for one
  program; can be split later because the boundaries already exist); a single module
  (fastest to write, but the opponent and CLI would reach into board internals).

## R4. Engine state: immutable values

- **Decision**: The game state is an immutable value. `GameState.play(square)` returns a
  new state; it never mutates the old one.
- **Rationale**: (a) A future smarter opponent will search ahead — trying moves on copies
  — and immutable states make that safe and free of undo logic. (b) The CLI and the
  opponent can be handed the same state with no risk of one changing what the other sees.
  (c) Tests can build any position directly and compare states by value. With at most 81
  moves per game, copying a 9×9 board per move costs nothing measurable (SC-005).
- **Alternatives considered**: a mutable `Game` object with `play`/`undo` — smaller
  allocations, but couples a future search opponent to undo correctness.

## R5. Win detection

- **Decision**: After each move, count consecutive same-mark squares through the square
  just played in each of the four directions (row, column, diagonal, anti-diagonal),
  adding both sides; the move wins if any count is ≥ 5 (FR-008, "five or more").
- **Rationale**: Only lines through the last move can have changed, so this is exact and
  cheap. Counting both sides through the new square handles "fills a gap" six-in-a-row
  (spec US1 scenario 6) and "two lines at once" (one win) without special cases. The run
  length (5) and board size (9) are named constants in the engine so a variant is a
  one-line change.
- **Alternatives considered**: scanning the whole board after every move — correct but
  needlessly repeats work and obscures *which* move won.

## R6. Randomness in the computer opponent

- **Decision**: `RandomOpponent` takes an optional `random.Random` instance; by default it
  creates its own unseeded one. It chooses with `rng.choice(state.board.empty_squares())`.
- **Rationale**: `choice` over the list of empty squares is uniform, which is exactly
  FR-012 ("each equally likely"). Injecting the generator lets tests use a fixed seed so
  SC-004 (1,000 trials, every one of 10 empty squares chosen) is deterministic and never
  flaky, while real play stays unpredictable.
- **Alternatives considered**: module-level `random` with `random.seed` in tests —
  global state, leaks between tests; picking random (row, col) and retrying until empty —
  slower near the end of a game and harder to argue uniform.

## R7. Conformance evidence and reports (constitution Principles I and V)

- **Decision**: Each test that provides evidence for a requirement is tagged with a pytest
  marker naming it, e.g. `@pytest.mark.req("FR-008", "US1-6")`. A small pytest plugin in
  `tests/conftest.py` writes `reports/conformance.md` after each run: one row per
  requirement / acceptance scenario / success criterion in the spec, listing the tests
  tagged with it and whether they passed. Requirement IDs with no tagged test are listed
  as **no evidence**. IDs are `FR-nnn` and `SC-nnn` as written in the spec, and
  `US<story>-<n>` for acceptance scenario *n* of User Story *story* (the spec numbers them
  but does not label them). Edge cases are unnumbered in the spec; their tests are tagged
  `EDGE-<short-name>` and listed in a separate section of the report.
- **Rationale**: Principle V asks for reports that let the developer see at a glance where
  conformance stands. Reading the IDs from `spec.md` (the governing document), not from a
  hand-kept list, means a new requirement shows up as "no evidence" automatically.
  `reports/` is generated output and is git-ignored.
- **Alternatives considered**: a hand-maintained traceability table (goes stale);
  third-party plugins such as pytest-html (adds a dependency, and still needs the ID
  mapping).

## R8. CLI design choices left open by the specification

These are presentation details the spec leaves to planning; the binding text is in
[contracts/cli.md](contracts/cli.md).

- **Menu entry**: menus are numbered; the player types the number (`1`, `2`, `3`).
  Rationale: one keystroke, no spelling to get wrong (FR-017 handles anything else).
- **Leave-game command** (FR-018 leaves the command to planning): `m` (for "menu"),
  case-insensitive, surrounding spaces ignored. Every move prompt names it.
  `q` was rejected because "quit" at the start menu means *end the program*, and the
  leave-game command must not.
- **Move entry** (FR-004): two integers, separated by one or more spaces, or by a comma
  with optional spaces around it; leading/trailing spaces ignored. Two integers that are
  not both 1–9 are reported as *out of range*; anything else that is not `m` is
  *unreadable*.
- **Board rendering** (FR-006): column numbers across the top, row numbers down the left,
  `.` for an empty square, `X`/`O` for marks.
- **I/O seam**: the CLI reads from and writes to text streams passed in at start-up (the
  real terminal by default). Tests drive whole sessions by feeding a script of input lines
  and checking the output transcript.

## Proposed specification corrections

Planning found one behavior the specification does not settle and that a design choice
should not settle on its own:

- **P1 — End of input / interrupt.** If the terminal's input ends (Ctrl-D) or the player
  presses Ctrl-C, at any prompt, the spec says nothing (it was listed as *Outstanding, low
  impact* at the end of `/speckit-clarify`). **Proposed addition** to the spec: "If input
  ends or the player interrupts the program at any prompt, the program MUST end promptly
  with a short goodbye message and without an error trace." The plan and contracts are
  written assuming this proposal is accepted; if the developer rejects or changes it, only
  `contracts/cli.md` §5 and its tests change.
