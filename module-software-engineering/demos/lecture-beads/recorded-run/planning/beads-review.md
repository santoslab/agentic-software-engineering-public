# Review of the filed Beads records (epic ttt-cik and children .1–.4)

Method: read every record in full with `bd show`, compared against `planning/beads-plan.md`,
`specs/001-five-in-a-row/tasks.md` (T018–T024, Notes), `contracts/cli.md`, the spec's US1 text, and
the existing `cli/app.py`, `tests/cli/*`, `tests/conftest.py`. Also ran `uv run --frozen --offline pytest -q`
(44 passed; the command in the records works). Refinements were added with `bd update`
(notes and acceptance); the original descriptions were not rewritten, so the notes headed
"REVIEW 1 REFINEMENTS" are binding where they differ.

## Findings and corrections

| # | Record | Finding | Correction |
|---|--------|---------|------------|
| 1 | .2 | Description said only choice `1` still raises `NotImplementedError`; at refactor time choice `2` does too. | Note + acceptance corrected. |
| 2 | .2 | "Parse_menu per C-1/C-2" invited `int()`, which accepts `01`, `+1`; current menu accepts only exact `1/2/3` after strip, so a naive refactor would change behavior (breaking the II(b) claim). | Required identical behavior; added tests `01`, `+1` → None and the `choices` boundary. |
| 3 | .2 | Ambiguous whether failing tests are committed (a red commit would break "full suite verified"). | Tests and code land together in the II(c) commit; failing-run evidence goes in notes; II(b) is a later commit after a green run on the II(c) commit. Same rule added to .1, .3. |
| 4 | .2 | "Signed integer" in C-7/T022 is silent on `+4 7` and non-ASCII digits. | Recorded as D2; narrowest reading (optional `-`, ASCII digits), report choice; no test pins it. |
| 5 | .1 | T021 builds prompt, rejection and result text, but T018 tests only `render_board`; those texts have no test in .1. | Stated explicitly that their evidence is .3; no extra tests invented. |
| 6 | .1/.3 | Function names for text helpers are unspecified; .3 would guess. | Suggested names given (non-binding), chosen names to be recorded at close; wording constraints .3 tests rely on made explicit (`range`, `occupied`, exact result lines). |
| 7 | .3 | T020 says the transcript "ends with a result line", T023 returns to the start menu afterward. Direct contradiction in `tasks.md`. | Recorded as D1; tests assert order and absence of a later move prompt, not `endswith`. |
| 8 | .3 | C-5 (redraw after each move) and C-12 (final board drawn) may double-draw; unspecified. | Recorded as D3; tests use `>= moves+1` and ordering only. |
| 9 | .3 | C-8 does not say if the board is redrawn after a rejection; "board unchanged" had no testable form. | Tests assert one reason line, no new mark, same mark re-prompted; scripts may end with EOF. |
| 10 | .3 | `session()` returns only a transcript but the EOF test needs the return code; `ScriptedOpponent` could import the not-yet-existing opponent package. | Directions added (call `run()` directly or extend helper; use engine `Square` only). Out-of-range must reach `GameState.play`. |
| 11 | .4 | "Unchanged" diffs had no baseline. | Baseline commit `f803ba7` added to epic and .4; diff paths listed. Added report checks (no FAIL, Unknown IDs none), commit-type check, closing order. |
| 12 | epic | No baseline/closure rule; commit-trailer conflict (session requires a Co-Authored-By trailer vs "ends with Change type"). | Epic note: Change-type line comes immediately before the trailer; epic closes after .4. |

Checked and left as is: dependencies (.3 ← .1, .2; .4 ← .3; .1 and .2 independent; transitive
chain needs no extra edges); no duplicated work between issues; every original ID T018–T024
appears in a title and label; II(c)/II(b) split is inside .2; no US3, `m`, or computer-play
scope; design refs are project-relative paths.

## Open items for a developer ruling (not resolved here; non-blocking)
- **D1** `tasks.md` T020 ("transcript ends with a result line") vs T023 (returns to the start menu).
- **D2** C-7/T022 "signed integer": `+4 7` and non-ASCII digits.
- **D3** Whether the final board after a winning move is drawn once or twice (C-5 vs C-12), and
  whether a rejection redraws the board.
- Known staged gap (already ruled): C-6/FR-018/C-9 `m` hint and handling deferred to US3; FR-018 not claimed.

## Limitations
No separate decision issues were created, to avoid extra scope; the items live in notes and
here. The descriptions of .1–.4 still contain the superseded statements (finding 1) next to
the corrective notes. The records were reviewed by the same agent that wrote them.

## Result
Records refined and consistent with the plan. Graph unchanged: `bd ready` lists the epic,
.1 and .2; .3 and .4 are blocked. Ready to start .1 or .2.

---

# Second pass

Checks performed: re-read T018–T024 sentence by sentence against the four child records
(no requirement lost in the T018+T021, T019+T022, T020+T023 grouping: every listed input,
tag, boundary and test case is still present); compared acceptance criteria with C-1/C-2,
C-5…C-8, C-12/C-13, C-17 and the US1 scenarios; checked dependencies and readiness
(`bd ready`: epic, .1, .2; `bd blocked`: .3, .4; unchanged); inspected the repo's commit
mechanics (`.beads/hooks` via `core.hooksPath`, tracked `.beads` files, git-ignored `reports/`)
and how existing tests import shared positions.

## Deficiencies found and corrected
| # | Record | Finding | Correction |
|---|--------|---------|------------|
| 13 | epic | Working protocol was implicit: claim, per-step evidence fields (command, outcome, remaining criteria, next action, commit ref), staying in progress, which files to stage. | Added "REVIEW 2 WORKING PROTOCOL" note covering all children. |
| 14 | epic | Beads git hooks run on every commit and could add unrelated files; `planning/` is untracked. | Protocol: stage explicit paths, check `git show --stat HEAD` after each commit, keep `planning/` out of milestone commits unless asked; no remote operations. |
| 15 | .3 | T020's `session()` wiring to `opponent_factory` (contracts/cli.md §1) was implicit. | Note: factory is `lambda: ScriptedOpponent(opponent_moves)`, and may be made to fail if called to prove it is unused in two-player games. |
| 16 | .3 | US1-1/US1-2 evidence content, import style for `tests.positions`, and the tag-vs-commit-message ID difference were implicit. | Added to the .3 note. |

## Checked, no change needed
- Acceptance vs contracts: .1 (C-5, C-6 without `m` hint, C-8, C-12/C-13), .2 (C-1/C-2, C-7), .3 (C-4, C-8, C-12/C-13, C-17), .4 (T024 text) match; the C-6/C-9/FR-018 staging gap is already documented in .1, .3, .4 and the epic.
- Dependencies are sufficient; adding edges from .4 to .1/.2 would be redundant.
- No requirement for T017's exports is affected (`cli/__init__.py` unchanged; `render`/`parse` are cli-internal).
- Scope: no extra issues, no US2/US3 work added.

## Unresolved developer decisions
Unchanged from the first pass: D1 (T020 vs T023 on the end of the transcript), D2 ("signed integer":
`+4 7`, non-ASCII digits), D3 (single vs double final-board draw; redraw after rejection). None blocks starting; the
records give a neutral test reading for each.

## Result
Ready for an implementation session. Start with `bd update ttt-cik.1 --claim` or `ttt-cik.2 --claim`.
