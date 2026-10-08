---

description: "Task list for 001-five-in-a-row"
---

# Tasks: Five-in-a-Row Tic-Tac-Toe

**Input**: Design documents from `specs/001-five-in-a-row/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ (engine.md,
opponent.md, cli.md), quickstart.md

**Tests**: Included. The constitution (Principle I) requires evidence that the realization
conforms to the specification, and each contract lists the evidence it expects. Tests are
written first and must fail before the code they cover exists.

**Organization**: Tasks are grouped by user story so each story can be implemented and
checked on its own.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- All paths are relative to the project root `SpecKit/TicTacToe/`

## Conventions every task follows

- **Requirement tags.** Every test function carries `@pytest.mark.req(...)` naming the
  spec IDs it is evidence for. IDs: `FR-nnn`, `SC-nnn` as in `spec.md`; `US<s>-<n>` for
  acceptance scenario *n* of User Story *s*; `EDGE-<slug>` for an edge case, where the
  slug is the edge case's bold name lower-cased with spaces as hyphens (e.g.
  `EDGE-occupied-square`, `EDGE-end-of-input-or-interrupt`). Each task below lists the
  IDs its tests must carry.
- **Public APIs only.** Code outside a subpackage imports only from that subpackage's
  `__init__.py` (`five_in_a_row.engine`, `five_in_a_row.opponent`, `five_in_a_row.cli`).
- **CLI tests** call `five_in_a_row.cli.run(stdin, stdout, opponent_factory)` with
  `io.StringIO` input (one entry per line), a `StringIO` output, and — for vs-computer
  games — the `ScriptedOpponent` fake from T020. They assert on facts in the transcript
  (a square's row and column, a mark, a reason word), not on exact spacing
  (contracts/cli.md, "Normative vs. illustrative").
- **Shared positions** (from `tests/positions.py`, T008):
  - `DRAW_PATTERN` — a full board with no line longer than 2, X on 41 squares and O on
    40. Row *r* (1–9) is `XXOOXXOOX` for odd *r* and `OOXXOOXXO` for even *r*.
  - `DRAW_MOVES` — the 81 squares of `DRAW_PATTERN` in a legal playing order: X's squares
    and O's squares each in row-major order, interleaved X, O, X, O, …, ending with X's
    41st square. Because the final board has no five-in-a-line, no earlier board does.
  - `X_WINS_MOVES` — X: `5 1`, `5 2`, `5 3`, `5 4`, `5 5`; O between them: `1 1`, `1 2`,
    `1 3`, `1 4`. Nine moves; X wins on the ninth.
  - `O_WINS_MOVES` — X: `9 1`, `9 3`, `9 5`, `9 7`, `7 1`; O: `1 1` … `1 5`. Ten moves
    alternating from X; O wins on the tenth.
- **When a test fails after the code is written**, do not change the test or the spec to
  make it pass: stop and report the disagreement to the developer, who decides which side
  changes (constitution Principle III).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: An installable, testable, empty package laid out as in plan.md.

- [X] T001 Create `pyproject.toml` at the project root: `[project]` name `five-in-a-row`, version `0.1.0`, `requires-python = ">=3.12"`, no run-time `dependencies`; `[project.scripts]` `five-in-a-row = "five_in_a_row.cli:main"`; build backend `hatchling` with `[tool.hatch.build.targets.wheel] packages = ["src/five_in_a_row"]`; `[dependency-groups] dev = ["pytest>=8"]`; `[tool.pytest.ini_options]` with `testpaths = ["tests"]`, `addopts = "--strict-markers"`, and `markers = ["req(*ids): spec IDs this test is evidence for"]`
- [X] T002 Create the package skeleton per plan.md: `src/five_in_a_row/__init__.py` (docstring only), `src/five_in_a_row/__main__.py` (calls `five_in_a_row.cli.main()` and exits with its return value), and empty-API `__init__.py` files in `src/five_in_a_row/engine/`, `src/five_in_a_row/opponent/`, `src/five_in_a_row/cli/` (the CLI one defines `main()` returning 0 for now); create `tests/__init__.py`, `tests/engine/__init__.py`, `tests/opponent/__init__.py`, `tests/cli/__init__.py`
- [X] T003 Run `uv sync` and `uv run pytest` from the project root and confirm the environment builds and pytest runs (zero tests collected is expected); `uv.lock` is created — keep it in version control

**Checkpoint**: `uv run pytest` runs; `uv run five-in-a-row` exits with status 0.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Evidence tooling, the architecture rule, the whole engine (every story plays
through it), and the CLI shell — start menu and end-of-input handling — that every
story's sessions start from.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

### Evidence tooling (constitution Principles I and V; research.md R7)

- [X] T004 [P] Create `tests/conformance.py` with `spec_ids(spec_path) -> dict[str, list[str]]` that reads `specs/001-five-in-a-row/spec.md` and returns IDs grouped as `"Functional Requirements"` (every `**FR-nnn**`), `"Success Criteria"` (every `**SC-nnn**`), `"Acceptance Scenarios"` (`US<s>-<n>` for each numbered `**Given**` item under `### User Story <s>`), and `"Edge Cases"` (`EDGE-<slug>` for each `- **Name**:` bullet under `### Edge Cases`), each in document order
- [X] T005 [P] Create `tests/test_conformance.py` asserting that `spec_ids()` on the real spec returns exactly FR-001–FR-020, SC-001–SC-006, US1-1–US1-7, US2-1–US2-7, US3-1–US3-6, and these eight edge IDs: `EDGE-occupied-square`, `EDGE-out-of-range-square`, `EDGE-unreadable-input`, `EDGE-invalid-menu-choice`, `EDGE-more-than-five-in-a-row`, `EDGE-win-on-the-last-square`, `EDGE-two-lines-at-once`, `EDGE-end-of-input-or-interrupt` (this test is expected to need updating, through the spec changelog, whenever the spec gains or loses an ID)
- [X] T006 Create `tests/conftest.py`: a pytest plugin that records, for each test, its `req` IDs and outcome (passed / failed / skipped, with the skip reason), and at session end writes `reports/conformance.md` containing, per group from `spec_ids()`, a table `| ID | Tests | Status |` where Status is **pass** (all tagged tests passed), **FAIL** (any failed), **manual** (only skipped tests, all with a reason starting `manual:`), or **no evidence** (no tagged test); plus a final section "Unknown IDs" listing any tag not found in the spec, with the tests using it; plus a header with the run date, spec path, and pass/fail/no-evidence counts. Create `reports/` if missing (depends on T004)
- [X] T007 [P] Create `tests/test_architecture.py`: parse every `.py` under `src/five_in_a_row/` with `ast`, and assert (a) nothing under `engine/` imports `five_in_a_row.opponent` or `five_in_a_row.cli`; (b) nothing under `opponent/` imports `five_in_a_row.cli`; (c) any import of a sibling subpackage from outside it names only the subpackage itself (e.g. `from five_in_a_row.engine import GameState`), never a submodule such as `five_in_a_row.engine.state`; (d) only modules under `cli/` reference `sys.stdin`, `sys.stdout`, `input(` or `print(`. Leave this test without a `req` tag: it is evidence for the plan's dependency rule (research.md R3), not for a spec ID
- [X] T008 [P] Create `tests/positions.py` defining `DRAW_PATTERN`, `DRAW_MOVES`, `X_WINS_MOVES`, `O_WINS_MOVES` exactly as described under *Conventions*, as tuples of `(row, col)` integer pairs (and `DRAW_PATTERN` as a tuple of 9 strings). No self-check is needed here; T010 plays `DRAW_MOVES` and checks the result

### Engine (contracts/engine.md; data-model.md "Engine entities")

- [X] T009 [P] Write `tests/engine/test_board.py`: `Mark.other()` swaps X and O; `Square` equality by value; a new board has 81 empty squares and `empty_squares()` returns them in row-major order `(1,1), (1,2), …, (9,9)`; `at()` on an off-board square raises `ValueError`; `is_full()` false on an empty board. Tags: `FR-001`, `FR-002`, `FR-004`
- [X] T010 [P] Write `tests/engine/test_state.py` covering every row of the "Evidence expected" table in contracts/engine.md, with tags as listed there: `new()` fields (`FR-001`, `FR-002`); alternation after accepted moves (`FR-003`, `US1-2`); each rejection reason `GAME_OVER`, `OUT_OF_RANGE` (row 0, row 10, col 0, col 10), `OCCUPIED`, with the original state unchanged and the reasons checked in the contract's order (`FR-005`, `SC-006`, `EDGE-occupied-square`, `EDGE-out-of-range-square`); a win in each of the four directions using the exact positions of US1-3, US1-4, US1-5 (`FR-008`, `FR-009`, `US1-3`, `US1-4`, `US1-5`); six-in-a-row by filling the gap at row 7, col 3 per US1-6 (`FR-008`, `US1-6`, `EDGE-more-than-five-in-a-row`); one move completing a row and a column at once gives one win (`EDGE-two-lines-at-once`); a win on the last empty square is a win, not a draw (`FR-010`, `EDGE-win-on-the-last-square`); playing `DRAW_MOVES` ends in `DRAW` and no earlier state is terminal (`FR-010`, `US1-7`, `SC-003`); four in a line, five broken by a gap, and five broken by the other mark are not wins (`SC-003`); `play` after a win raises `GAME_OVER` (`FR-009`); `winner` is X/O/None as appropriate
- [X] T011 Implement `src/five_in_a_row/engine/board.py`: `SIZE = 9`; `Mark` enum (`X = "X"`, `O = "O"`, `other()`); frozen, slotted dataclass `Square(row: int, col: int)` that accepts any integers ("A `Square` with a value outside 1–9 can be *described* … but the engine rejects it in `play`"); immutable `Board` with `at(square) -> Mark | None` ("raises ValueError if off-board"), `empty_squares() -> tuple[Square, ...]` ("in row-major order"), `is_full()`, and an internal `with_mark(square, mark) -> Board` used only by the engine (depends on T009 failing first)
- [X] T012 Implement `src/five_in_a_row/engine/state.py`: `WIN_LENGTH = 5`; `Result` enum (`IN_PROGRESS`, `X_WON`, `O_WON`, `DRAW`); `IllegalMoveReason` enum (`GAME_OVER`, `OUT_OF_RANGE`, `OCCUPIED`); `IllegalMove(Exception)` with `reason` and `square`; immutable `GameState` with fields `board`, `turn`, `result`, `last_move`, `new()`, `play(square)`, and `winner`, exactly as specified in contracts/engine.md §Behavior — rejection reasons checked in the order GAME_OVER, OUT_OF_RANGE, OCCUPIED; win detection per research.md R5 (count both directions through the square just played in each of the four directions; win if count ≥ `WIN_LENGTH`); "A win is checked before fullness, so a win on the last square is a win, not a draw" (depends on T010, T011)
- [X] T013 Export the engine's public API from `src/five_in_a_row/engine/__init__.py`: `SIZE`, `WIN_LENGTH`, `Mark`, `Square`, `Result`, `Board`, `GameState`, `IllegalMove`, `IllegalMoveReason` (with `__all__`); run `uv run pytest tests/engine tests/test_architecture.py` — all pass (depends on T011, T012)

### CLI shell (contracts/cli.md §1, §2, §5)

- [X] T014 [P] Write `tests/cli/test_start_menu.py`: on start the output shows the three choices "Play the computer", "Play a friend", "Quit" numbered 1–3 (`FR-014`, `US3-1`); entering `3` ends the program and `run()` returns 0 (`FR-016`, `US3-4`); entering `7`, `x`, and a blank line each print a not-a-choice message and show the same menu again (`FR-017`, `SC-006`, `EDGE-invalid-menu-choice`); ` 3 ` with surrounding spaces is accepted
- [X] T015 [P] Write `tests/cli/test_end_of_input.py`: input that ends at the start menu (empty `StringIO`, or input ending after an invalid choice such as `7\n`) makes `run()` print a goodbye line and return 0 within 1 second without raising (`FR-020`, `US3-6`, `EDGE-end-of-input-or-interrupt`); a `stdin` whose `readline` raises `KeyboardInterrupt` gives the same result
- [X] T016 Implement `src/five_in_a_row/cli/app.py` with `run(stdin: TextIO, stdout: TextIO, opponent_factory=None) -> int` (T028 gives `opponent_factory` its final type `Callable[[], Opponent]` and default `RandomOpponent` once the opponent module exists) and a private line reader that turns end of input (`readline()` returning `""`) and `KeyboardInterrupt` into a single goodbye line and a return value of 0 (C-17); implement the start menu per C-1–C-3 (choices `1` and `2` may raise `NotImplementedError` until US2 and US1 add them)
- [X] T017 Export `run` and `main` from `src/five_in_a_row/cli/__init__.py`; `main()` calls `run(sys.stdin, sys.stdout)` and returns its result; run `uv run pytest` — all tests so far pass (depends on T016)

**Checkpoint**: Engine complete and verified; `uv run five-in-a-row` shows the start menu,
quits on `3`, and exits cleanly on Ctrl-D/Ctrl-C.

---

## Phase 3: User Story 1 - Two players at one keyboard (Priority: P1) 🎯 MVP

**Goal**: Choosing "Play a friend" plays a complete two-player game to a win or a draw.

**Independent Test**: Choose `2` and play complete games by typing moves for both sides:
one where X wins, one where O wins, one that ends in a draw (spec US1; quickstart M1, M2).

### Tests for User Story 1 ⚠️ write first; they must fail

- [X] T018 [P] [US1] Write `tests/cli/test_render.py` for `render_board(board) -> str` in `five_in_a_row.cli.render`: the output has column numbers 1–9 across the top, row numbers 1–9 down the left with row 1 first, `.` for every empty square, and `X`/`O` at the squares holding them, checked on a board with marks at (1,1), (5,5), (9,9) (`FR-006`, `FR-004`)
- [X] T019 [P] [US1] Write `tests/cli/test_parse.py` for `parse_move(text)` in `five_in_a_row.cli.parse`: `4 7`, `4,7`, ` 4 , 7 `, `4   7` → `Square(4, 7)`; `0 3`, `10 3`, `-1 3` → a `Square` (out-of-range values are left for the engine to reject); `abc`, `5`, `1 2 3`, `` (blank), `4;7` → unreadable (`FR-004`, `EDGE-unreadable-input`)
- [X] T020 [P] [US1] Create `tests/cli/conftest.py` with a `ScriptedOpponent` fake (constructed with a list of `(row, col)` pairs; `choose_move` returns them in order as `Square`s) and a `session(lines, opponent_moves=())` helper that runs `run()` on those input lines and returns the output transcript; one instance serves a whole vs-computer series, so its move list covers every game the test plays before returning to the start menu (contracts/cli.md §1); then write `tests/cli/test_two_player.py` driving `run()` with `2` followed by moves: `X_WINS_MOVES` → the board is drawn before the first move and after every move, each prompt names the mark to move, and the transcript ends with a result line naming X as winner (`FR-002`, `FR-003`, `FR-006`, `FR-007`, `FR-009`, `FR-011`, `US1-1`, `US1-2`, `US1-3`); `O_WINS_MOVES` → result names O (`FR-009`, `SC-003`); `DRAW_MOVES` → result says draw (`FR-010`, `US1-7`, `SC-003`); occupied square, `0 3`, and `abc` each print one line with the reason word "occupied" / "range" / a not-understood message, the board is unchanged, and the same mark is asked again (`FR-005`, `SC-006`, `EDGE-occupied-square`, `EDGE-out-of-range-square`, `EDGE-unreadable-input`); input that ends mid-game (`2` and two moves, then nothing) prints the goodbye line and `run()` returns 0 (`FR-020`, `US3-6`, `EDGE-end-of-input-or-interrupt`). Do not assert what happens after the result line — it changes in US3; end each input script there

### Implementation for User Story 1

- [X] T021 [P] [US1] Implement `src/five_in_a_row/cli/render.py`: `render_board(board)` per C-5 (reads `SIZE` from the engine), the move prompt text per C-6 (names the mark and says how to enter a square, e.g. `X to move — type row and column (e.g. 4 7):`; US3 adds the `m` hint), rejection messages per C-8 for `OUT_OF_RANGE`, `OCCUPIED`, and unreadable entries, and result lines per C-12/C-13 for two-player games (`X wins!`, `O wins!`, `It's a draw.`)
- [X] T022 [P] [US1] Implement `src/five_in_a_row/cli/parse.py`: `parse_move(text) -> Square | None` per C-7 (regex: optional spaces, signed integer, then one or more spaces or a comma with optional spaces, signed integer, optional spaces; `None` means unreadable) and `parse_menu(text, choices: int) -> int | None` per C-1/C-2 (surrounding spaces ignored; `None` for anything not in `1..choices`); then, as a separate II(b) commit (see Notes), refactor T016's start menu to use `parse_menu` — run `uv run pytest` before committing; T014 must still pass unchanged
- [X] T023 [US1] Implement the two-player game loop in `src/five_in_a_row/cli/app.py` for start-menu choice `2`: new `GameState`, draw the board, prompt the mark to move, read and parse a move, call `GameState.play`, on `IllegalMove` print the reason and re-prompt the same mark, on acceptance redraw; on a terminal result draw the final board and print the result line, then return to the start menu (interim — US3 replaces this with the game-over menu) (depends on T021, T022)
- [X] T024 [US1] Run `uv run pytest`; all tests pass; open `reports/conformance.md` and confirm every `US1-*` ID is **pass** (depends on T023)

**Checkpoint**: The MVP — two people can play a full game of five-in-a-row.

---

## Phase 4: User Story 2 - Play against the computer (Priority: P2)

**Goal**: Choosing "Play the computer" plays a full game against a random computer
opponent, which announces each square it takes.

**Independent Test**: Choose `1` and play a game to completion; the computer moves without
input, always onto an empty square, names its square, and a win by either side or a draw
is announced (spec US2; quickstart M4).

### Tests for User Story 2 ⚠️ write first; they must fail

- [ ] T025 [P] [US2] Write `tests/opponent/test_random_opponent.py` per the "Evidence expected" table in contracts/opponent.md: with `random.Random(seed)`, 1,000 `choose_move` calls on random in-progress positions (built by playing random legal moves from `GameState.new()`) all return empty squares (`FR-012`, `SC-004`, `US2-3`); one fixed position with exactly 10 empty squares and no win, 1,000 calls with a seeded generator, each of the 10 squares returned at least once (`FR-012`, `SC-004`, `US2-3`); a terminal state raises `ValueError`; the state passed in equals itself before and after the call
- [ ] T026 [P] [US2] Write `tests/cli/test_vs_computer.py` using `ScriptedOpponent`: choice `1` draws an empty board and prompts X — the human — for the first move (`US2-1`, `FR-013`); after each human move the computer moves without reading input (the input script contains only human moves), a line names the computer's mark and the square's row and column, and the board is redrawn showing it (`FR-012`, `FR-019`, `US2-2`); a computer win prints a result naming the computer and its mark (`US2-4`, `FR-009`); a human win names the human ("you") and the mark; the time from a human move to the next prompt, measured over a whole game with the real `RandomOpponent`, is under 1 second per move (`SC-005`); end each input script at the result line

### Implementation for User Story 2

- [ ] T027 [P] [US2] Implement `src/five_in_a_row/opponent/base.py` (`Opponent` as a `typing.Protocol` with `choose_move(self, state: GameState) -> Square`) and `src/five_in_a_row/opponent/random_opponent.py` (`RandomOpponent(rng: random.Random | None = None)`; `choose_move` raises `ValueError` if `state.result` is not `IN_PROGRESS`, else returns `self._rng.choice(state.board.empty_squares())`); export both from `src/five_in_a_row/opponent/__init__.py`; import only from `five_in_a_row.engine`
- [ ] T028 [US2] Implement the vs-computer game loop in `src/five_in_a_row/cli/app.py` for start-menu choice `1`, sharing the two-player loop: the session's `human_mark` is `Mark.X` (C-4); on the computer's turn read no input, call `opponent.choose_move(state)`, play it, print the computer-move line per C-10 (add its text to `render.py`), and redraw; result lines per C-12 for vs-computer games ("You win! (X)", "The computer wins! (O)", draw); set `run()`'s default `opponent_factory` to `RandomOpponent` (depends on T027)
- [ ] T029 [US2] Run `uv run pytest`; all tests pass; in `reports/conformance.md` `US2-1`–`US2-4` are **pass** (`US2-5`–`US2-7` stay **no evidence** until US3, which adds "play again") (depends on T028)

**Checkpoint**: One person can play the computer; two-player play still works.

---

## Phase 5: User Story 3 - Menu, play again, and quit (Priority: P3)

**Goal**: After a game the player can play again (same mode; sides swap against the
computer) or return to the start menu, and can leave a game partway through.

**Independent Test**: Start a game, finish it, choose play again, finish that, choose back
to the start menu, then quit (spec US3; quickstart M3, M5–M7).

**Note**: this phase also delivers US2 scenarios 5–7, which need "play again".

### Tests for User Story 3 ⚠️ write first; they must fail

- [ ] T030 [P] [US3] Write `tests/cli/test_game_over_menu.py`: after a finished game the output offers "Play again" and "Back to the start menu" as 1 and 2 (`FR-015`, `US3-2`); an invalid entry re-shows that menu (`FR-017`, `SC-006`, `EDGE-invalid-menu-choice`); in two-player mode `1` starts a new game with an empty board and X to move (`US3-3`); `2` shows the start menu, and `3` there ends the program (`US3-4`, `FR-016`); a full session following US3's Independent Test ends with `run()` returning 0
- [ ] T031 [P] [US3] Write `tests/cli/test_series.py` using `ScriptedOpponent`: after a vs-computer game in which the human was X, play again makes the human O and the computer moves first without input (`FR-013`, `US2-5`); after the next game play again makes the human X again and prompts the human first (`FR-013`, `US2-6`); after any games, back to the start menu then `1` makes the human X (`FR-013`, `US2-7`)
- [ ] T032 [P] [US3] Write `tests/cli/test_leave_game.py`: at a move prompt, `m`, `M`, and ` m ` each end the game with no result line and show the start menu (`FR-018`, `US3-5`); every move prompt mentions `m` (`FR-018`, `FR-007`); after leaving a vs-computer game in which the human was O, choosing `1` makes the human X (`FR-013`); add a `parse_move`-level case in this file confirming `m` is not reported as unreadable

### Implementation for User Story 3

- [ ] T033 [US3] Add the leave-game command to `src/five_in_a_row/cli/parse.py` (`m` or `M`, surrounding spaces ignored, recognised before move parsing — C-9) and the `m` hint to the move prompt in `src/five_in_a_row/cli/render.py` (C-6, e.g. `X to move — type row and column (e.g. 4 7), or m for the menu:`)
- [ ] T034 [US3] In `src/five_in_a_row/cli/app.py`: replace the interim "return to start menu after a result" with the game-over menu per C-14; implement play again per C-15 (same mode; vs-computer flips `human_mark`; two-player starts with X) and back to the start menu per C-16 (next `1` sets `human_mark` to X); handle the leave-game command per C-9 (no result line, start menu shown, session ended) (depends on T033)
- [ ] T035 [US3] Run `uv run pytest`; all tests pass; in `reports/conformance.md` every `US3-*` and `US2-5`–`US2-7` ID is **pass** (depends on T034)

**Checkpoint**: All three user stories work; the full session flow in data-model.md
"Session" transitions is in place.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Close evidence gaps, validate end to end, and leave the project easy to run.

- [ ] T036 [P] Write `tests/cli/test_timing.py`: from `run()` starting to the first move prompt after input `2` takes under 15 seconds (`SC-001`)
- [ ] T037 [P] Create `tests/test_manual_checks.py` with one test tagged `req("SC-002")` that calls `pytest.skip("manual: quickstart.md — a person who watched one game plays one unaided")`, so the conformance report shows SC-002 as **manual** rather than **no evidence**
- [ ] T038 Run `uv run pytest`; open `reports/conformance.md` and confirm: no **FAIL**, no **no evidence**, no "Unknown IDs", and SC-002 is the only **manual** row. If any ID lacks evidence, add the missing test in the matching `tests/` subdirectory before continuing
- [ ] T039 [P] Create `README.md` at the project root: one paragraph on the game, how to run it (`uv run five-in-a-row` or `python -m five_in_a_row`), how to run the tests and where the conformance report is written, and links to `specs/001-five-in-a-row/spec.md`, `plan.md`, and `quickstart.md`
- [ ] T040 Walk through quickstart.md §2 (M1–M8) by hand with `uv run five-in-a-row`, and report each walkthrough's outcome to the developer; any mismatch is reported, not fixed silently (constitution Principle III)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: none — start immediately.
- **Foundational (Phase 2)**: depends on Setup. Blocks all user stories.
- **US1 (Phase 3)**: depends on Foundational.
- **US2 (Phase 4)**: depends on Foundational; its CLI work (T028) reuses the game loop from
  US1 (T023), so in practice it follows US1. The opponent module (T025, T027) has no
  dependency on US1 and can be built in parallel with it.
- **US3 (Phase 5)**: depends on US1 (game loop, results). Scenarios US2-5–US2-7 also need
  US2.
- **Polish (Phase 6)**: depends on all stories.

### Within Each Phase

- Tests are written first and must fail before the code they cover is written.
- Engine: board (T011) before state (T012) before exports (T013).
- CLI: render and parse (T021, T022) before the game loop (T023).

### Parallel Opportunities

- Phase 2: T004, T007, T008, T009, T010, T014, T015 touch different files and can run
  together; T006 waits for T004.
- Phase 3: T018, T019, T020 together; then T021 and T022 together.
- Phase 4: T025 and T026 together; T027 can be built alongside Phase 3.
- Phase 5: T030, T031, T032 together.
- Phase 6: T036, T037, T039 together.

---

## Parallel Example: Foundational engine work

```text
Task: "Write tests/engine/test_board.py …"          (T009)
Task: "Write tests/engine/test_state.py …"          (T010)
Task: "Create tests/test_architecture.py …"         (T007)
Task: "Create tests/positions.py …"                 (T008)
```

## Parallel Example: User Story 1

```text
Task: "Write tests/cli/test_render.py …"            (T018)
Task: "Write tests/cli/test_parse.py …"             (T019)
# then
Task: "Implement src/five_in_a_row/cli/render.py …" (T021)
Task: "Implement src/five_in_a_row/cli/parse.py …"  (T022)
```

## Parallel Example: User Story 2 alongside User Story 1

```text
Task: "Write tests/opponent/test_random_opponent.py …"         (T025)
Task: "Implement src/five_in_a_row/opponent/ …"                (T027)
# while US1's CLI tasks proceed — the opponent depends only on the engine
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: Setup.
2. Phase 2: Foundational — engine fully verified, start menu, clean exit.
3. Phase 3: User Story 1.
4. **Stop and validate**: quickstart M1, M2; `US1-*` all **pass** in the conformance
   report.

### Incremental Delivery

1. Setup + Foundational → engine and shell ready.
2. US1 → two-player game (MVP).
3. US2 → play the computer.
4. US3 → game-over menu, play again with side swapping, leave-game.
5. Polish → no evidence gaps; README; manual walkthroughs.

---

## Notes

- **Commit messages** (constitution Principle II, Records of Change): every commit that
  changes the realization MUST identify which of II(a), II(b), or II(c) applies, e.g. by
  ending with a line `Change type: II(c) — implements FR-008, US1-6`.
  - Building a task's behavior for the first time is **II(c)**.
  - Restructuring code already written without changing behavior (e.g. T022's refactor of
    the start menu) is **II(b)**: run the full test suite before committing, and the
    message MUST state that no specified behavior changed.
  - Fixing code that a test showed to be non-conforming is **II(a)** — after the
    developer has decided that the code, not the spec, changes (Principle III).
- **Spec questions**: if a task reveals that the spec, plan, or a contract is wrong or
  incomplete, stop and propose a correction to the developer rather than improvising
  (Principle IV). A spec change also needs an entry in `specs/001-five-in-a-row/CHANGELOG.md`.
- `reports/` is git-ignored; `uv.lock` is committed.
- Commit after each task or logical group; stop at any checkpoint to validate a story on
  its own.
