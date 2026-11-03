# Execution plan outside Beads: two-player milestone (T018–T024)

Status: revised twice (see `plan-review.md`; revision 2 applies the developer's clarifications). Planning input only; Beads
becomes authoritative for live status once issues exist. `tasks.md` and all governing
artifacts stay unchanged.

## Scope
- In: original tasks T018–T024, the two-player game for start-menu choice `2`, and T022's
  start-menu refactor. Win length is five or more on the 9×9 board.
- Out: computer play (choice `1` keeps raising `NotImplementedError`), the leave-game
  command `m`, the game-over menu, and the rest of US3. Out-of-scope ideas become future
  work records only.
- Baseline: `uv run pytest` → 44 passed. Of the US1 IDs, only `US1-1` has no evidence in
  `reports/conformance.md`. `FR-006`, `FR-007` and `FR-011` have no evidence either.

## Fixed constraints
- Tests come before the code they cover, and the intended initial failure is recorded.
- CLI code imports only the public APIs `five_in_a_row.engine` / `.opponent`. Test
  code follows the same rule.
- The parser does no range checking (`0 3`, `10 3`, `-1 3` parse to a `Square`). `4;7` is
  unreadable. `GameState.play` rejects out-of-range squares.
- Every test carries `@pytest.mark.req(...)` with the IDs listed in `tasks.md`.
- Commit messages end with `Change type: II(c) — …`, or `II(b)` for the refactor.
  II(b) says that no specified behavior changed and is committed only after the full
  suite passes.
- Tests assert transcript facts, not spacing (contracts/cli.md, "Normative vs. illustrative").
- One issue at a time. No push or remote.

## Work units (original IDs kept; the T020 and T022 splits are marked *)

| Unit | Original | Kind | Prerequisites | Work and evidence |
|------|----------|------|---------------|-------------------|
| A | T018 | test | none | `tests/cli/test_render.py`. Marks at (1,1), (5,5), (9,9); header 1–9, rows 1–9, `.` for empties. Tags FR-006, FR-004. Expected failure: ImportError on `five_in_a_row.cli.render`. |
| B | T021 | impl II(c) | A | `cli/render.py`: `render_board` (C-5), prompt (C-6), rejection lines (C-8: out of range, occupied, unreadable), result lines (C-12/C-13 two-player: `X wins!`, `O wins!`, `It's a draw.`). Evidence: A passes and the full suite is green. |
| C | T019 | test | none | `tests/cli/test_parse.py` for `parse_move` exactly as listed (accept, out-of-range-as-Square, unreadable incl. `4;7`). Tags FR-004, EDGE-unreadable-input. Expected failure: ImportError on `cli.parse`. |
| D | T022* part 1 | impl II(c) | C | `cli/parse.py`: `parse_move` (C-7) and `parse_menu` (C-1/C-2). Evidence: C passes and the suite is green. See review Q1 for the `parse_menu` tests. |
| E | T022* part 2 | refactor II(b) | D, full suite green | Start menu in `app.py` uses `parse_menu`. Run the full suite first. T014 (`test_start_menu.py`) and T015 (`test_end_of_input.py`) pass unchanged. Separate commit that says no specified behavior changed. |
| F | T020* part 1 | test support | none | `tests/cli/conftest.py`: `ScriptedOpponent` and `session(lines, opponent_moves=())`. Not tagged. |
| G | T020* part 2 | test | B, D, E, F | `tests/cli/test_two_player.py` per T020: X wins, O wins, draw, occupied / `0 3` / `abc`, EOF mid-game. Tags as in `tasks.md`. Expected failure: choice `2` raises `NotImplementedError`. Does not assert behavior after the result line. |
| H | T023 | impl II(c) | G, E, B | Two-player loop in `app.py`. Interim: the result line returns to the start menu, and the commit message says "interim until T034". |
| I | T024 | verify | H | `uv run pytest` is fully green. `reports/conformance.md` shows every `US1-1`…`US1-7` as **pass**. |

## Order and parallelism
Order: A → B → C → D → E → F → G → H → I. Run as one issue at a time.

A/C/F share no files and are independent of each other; B needs A and D needs C. The tasks
list proposes writing T018–T020 first; this plan reorders that (review F1) so that
the full suite is green when E (II(b)) is verified. Only G is expected to fail
while E is pending, so G is written after E.

## T024 final conformance check
1. `uv run pytest` → all pass, no failures or errors.
2. `reports/conformance.md`: `US1-1`…`US1-7` all **pass** (US1-2…7 are already covered by
   engine tests; `US1-1` is new from G). Also note FR-004/006/007/011 and
   SC-003/SC-006 gain evidence.
3. Walk the table of the original T018–T023 text against the delivered tests and code. Confirm
   the architecture tests still pass, the start-menu and EOF tests are unmodified
   (`git diff` on those files is empty), and `tasks.md` and the specs are unmodified.
4. Report any disagreement for a developer ruling; do not alter tests or specs.

## Handoff content (for Beads records)
Actual commands and outcomes, remaining criteria, next action, commit hashes, and
discoveries (review Q1–Q3).

## Revision 2: grouping into Beads issues (developer clarifications applied)
Units A–I are internal steps. They become four issues plus the epic:

| Issue | Original IDs | Units | Independent of |
|-------|--------------|-------|----------------|
| Render | T018, T021 | A, B | Parsing |
| Parsing (one bounded bead) | T019, T022 | C, D, E | Render |
| Two-player loop | T020, T023 | F, G, H | none (needs Render and Parsing) |
| Verify | T024 | I | none (needs Loop) |

- Parsing keeps `parse_move` tests, `parse_menu` tests (C-1/C-2, tests-first, no new
  behavior), the II(c) parser commit, and the separate II(b) menu-caller refactor commit
  (full suite green first) inside one bead. This is the unit the lecture interrupts.
- Loop writes its failing tests after the Parsing refactor (within the approved plan).
- Staged boundary: no leave-game hint and no `m` handling (T021/T023 interim behavior).
  FR-018 conformance is not claimed. The `m` gap vs C-6/C-9 is recorded as a discovery, and
  no governing artifact is amended.
- Blocking order: Loop blocked by Render and Parsing; Verify blocked by Loop. Render and
  Parsing could proceed independently, though one agent works one issue at a time.
- Q1 and Q2 of the review are resolved by the clarifications; Q3 is resolved as above.
