# Review of planning/beads-plan.md

Reviewed against: `tasks.md` T018–T024 and Notes, `contracts/cli.md` (C-1…C-17),
`contracts/engine.md`, `spec.md` US1 / FR-004…FR-011 / edge cases, `analysis-report.md`,
the constitution, CLAUDE.md/AGENTS.md, the existing `cli/app.py`, engine, tests and
`reports/conformance.md`. Baseline: 44 tests pass.

## Draft 1
A single chain following the order in `tasks.md`: T018/T019/T020 tests together, then T021,
T022 (parse and refactor as one), T023, T024.

## Findings and changes

**F1 — The II(b) "full suite verified first" condition conflicts with writing all tests
first.** The T020 tests fail until T023 exists. If they are written before T022's
refactor, the full suite cannot be green when E is verified. *Change:* the tests that
exercise the new loop (G) are written after the refactor (E). A/C still fail first against
B/D, so each piece of code keeps its own test-first record. `tasks.md` marks the tasks
[P] and its only ordering rule is tests before the code they cover, so this reorder
doesn't contradict it. See Q2 for confirmation.

**F2 — T022 mixes two change types.** Parse functions are II(c). The menu refactor is
II(b). *Change:* split into D and E with separate commits and messages. The original ID
T022 is kept on both.

**F3 — T020 mixes test support with the behavior tests.** *Change:* split into F
(`conftest.py`, untagged, no behavior of its own) and G. Both keep ID T020.

**F4 — `parse_menu` has no listed test.** T019 covers `parse_move` only; T022 requires
`parse_menu`. Test-first would be violated if it is only exercised via T014. *Change:* D
lists `parse_menu` unit tests in `test_parse.py` (spaces ignored, `None` outside `1..choices`).
See Q1.

**F5 — `app.py` is touched by both E and H.** *Change:* E before H, as a strict order,
so there are no conflicting edits. This is also what T023 "depends on T022" means.

**F6 — Tags and T024.** Only `US1-1` lacks evidence now; G supplies it. US1-2…7 are
already **pass** from engine tests. *Change:* T024 checks all seven are **pass**
after the full run, and that G's tags don't reintroduce unknown IDs.

**F7 — Scope guards added.** Choice `1` must still raise `NotImplementedError` (no
test may enter it); no `m` handling; no range checks in the parser; `4;7` unreadable;
no post-result assertions in G. Unchanged: `test_start_menu.py`, `test_end_of_input.py`.

**F8 — Commit/trace hygiene.** Each commit message names II(b) or II(c) and its spec IDs. H
says "interim until T034" (analysis I5). Failing-test evidence (command and first error)
is recorded in Beads, not only in commit text.

## Unresolved questions (not guessed)

**Q1 — parse_menu tests.** `tasks.md` T019 does not list them. I plan to add them to
`test_parse.py`, tagged FR-014/FR-017, as they follow from C-1/C-2. If the developer
reads T019 as exhaustive, they can be dropped and coverage left to T014.

**Q2 — Reordering (F1).** Is writing G after E acceptable? The alternative is committing
failing tests before the refactor and running only the previously passing tests for E,
which does not match "full suite verified first".

**Q3 — Leave-game hint.** C-6 and FR-007/FR-018 say the prompt explains how to leave the
game, but T021 says US3 adds the `m` hint and C-9 is US3 scope. Until then the prompt
cannot honestly advertise `m`, and `m` is rejected as unreadable. I will implement
the T021 wording (no hint, no `m`) and record this as a discovery for the developer. I
will not edit the contract or tasks.

## Result
Plan revised once; the summary of changes is F1–F8. Only Q1–Q3 stay open.

## Revision 2 (after developer clarifications)
- **Q1 resolved:** `parse_menu` unit tests are added, tests-first, under C-1/C-2. No new behavior.
- **Q2 resolved:** writing the two-player tests after the green-suite II(b) refactor is within the approved plan.
- **Q3 resolved:** follow T021/T023 interim behavior (no `m` hint, no `m` handling). FR-018 is not claimed.
  The C-6/C-9 staging gap is still recorded as a discovery in Beads; no artifact is amended.
- **Grouping change:** the nine units become four issues (Render, Parsing, Loop, Verify). T019 and T022 (parse_move,
  parse_menu, menu-caller refactor) stay in ONE bead, with the II(c) and II(b) commits separate inside it.
- **Correction to my earlier report:** I said no `bd` command had been run. That was wrong:
  the planning turn ran `bd list` (it returned "No issues found") and the session hook injected `bd prime` output.
  No issues were created then.
