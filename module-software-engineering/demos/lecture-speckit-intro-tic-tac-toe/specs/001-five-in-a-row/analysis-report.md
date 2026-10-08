# Analysis Report: 001-five-in-a-row

**Command**: `/speckit-analyze` | **Date**: 2026-10-08 | **Constitution**: v1.0.1

**Artifacts analyzed** (at commit `df82f4c`): [spec.md](spec.md), [plan.md](plan.md),
[tasks.md](tasks.md), with [research.md](research.md), [data-model.md](data-model.md),
[contracts/](contracts/), and [quickstart.md](quickstart.md) as supporting context.

This is a point-in-time report. It records what the analysis found; it does not change any
governing document. Part 2 lists the edits recommended before `/speckit-implement`.

---

## Part 1 — Findings

### Summary

| Severity | Count | IDs |
|----------|------:|-----|
| CRITICAL | 1 | C1 |
| HIGH | 1 | I1 |
| MEDIUM | 5 | C2, U1, I2, A1, I3 |
| LOW | 10 | I4, I5, G1, U2, I6, U3, U4, U5, D1, S1 |

| Metric | Value |
|--------|-------|
| Requirements (FR + SC) | 26 (20 FR, 6 SC) |
| Acceptance scenarios / edge cases | 20 / 8 |
| Tasks | 40 |
| Requirement coverage (≥ 1 task) | 100 % (26 / 26) |
| Scenario and edge-case coverage (≥ 1 tagged test) | 100 % (28 / 28) |
| Ambiguities | 1 |
| Duplications | 1 (three overlapping pairs, grouped) |
| Critical issues | 1 |

### Findings table

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| C1 | Constitution | CRITICAL | tasks.md, Notes, "Commit messages" | Constitution Principle II and *Records of Change*: every commit that changes a realization **MUST** identify II(a)/(b)/(c). tasks.md says the message "should say so". | Change to MUST and cite Records of Change (edit E1). |
| I1 | Inconsistency | HIGH | tasks.md T015, T016, T017 | T015 tests end of input mid-game after `2`, but T016 lets choice `2` raise `NotImplementedError` until US1, and T017 requires all tests to pass. The Phase 2 checkpoint cannot be reached as written. | Move the mid-game case into T020 (edit E2). |
| C2 | Constitution | MEDIUM | tasks.md T022; Notes | T022 includes refactoring T016's start menu to use `parse_menu` — a II(b) change (no behavior change), which Principle II requires to be verified and stated as such. The Notes call every commit II(c). | Name II(b) in the Notes and in T022 (edit E3). |
| U1 | Underspecified | MEDIUM | contracts/cli.md §1; tasks.md T020, T031 | When `run()` calls `opponent_factory` — once per session or once per game — is unstated. The `ScriptedOpponent` fake used across "play again" (T031) behaves differently under each. | State it in the contract (edit E4). |
| I2 | Inconsistency | MEDIUM | plan.md *Project Structure*; tasks.md T003, T004, T005, T008, T020, T036, T037, T039 | tasks.md creates files the plan's source tree does not list, and moves the spec-ID parser out of `tests/conftest.py`, which the plan names as the plugin. The plan (governing for tasks) no longer describes the tree. | Update the plan's tree (edit E5). |
| A1 | Ambiguity | MEDIUM | spec.md FR-020 (L205–206); Edge Cases (L148–149) | "End promptly" and "short goodbye message" have no measure; a test cannot fail them. | Give a measure (edit E6). |
| I3 | Terminology | MEDIUM | spec.md L31, 32, 34, 46, 81, 106, 122, 157, 164, 167, 196, 210 ("grid") vs. Key Entities and all contracts ("board") | Two words for one thing; the glossary in *Assumptions* fixes square, mark, line, draw, but not board/grid. | Use "board" throughout; add it to the glossary (edit E7). |
| I4 | Inconsistency | LOW | spec.md Key Entities (Player; Game "has a mode") vs. data-model.md | The spec's *Player* and *Game.mode* are split between engine `GameState` and CLI `Session`; the mapping is sound but unstated. | Add a mapping note to data-model.md. |
| I5 | Inconsistency | LOW | tasks.md T023 | Between US1 and US3 a finished game returns straight to the start menu — not FR-015. Acknowledged in the task; the conformance report shows FR-015 as *no evidence* until T034. | Accept; note it in T023's commit message. |
| G1 | Coverage | LOW | tasks.md T014, T030 | SC-006 includes "bad menu choice", but the menu-rejection tests are not tagged SC-006. | Add `SC-006` to those tags (edit E8). |
| U2 | Underspecified | LOW | spec.md FR-012; tasks.md T025 | FR-012 "each equally likely" is stronger than T025's evidence (each square chosen ≥ 1 time, per SC-004). Uniformity rests on `rng.choice`, i.e. on code review. | Say so in T025. |
| I6 | Inconsistency | LOW | spec.md L3, L7; plan.md header | Both name branch `001-five-in-a-row`, which does not exist; work is on `main`. Spec *Status* is still "Draft". | Mark the branch "n/a (work on `main`)"; set Status when approved. |
| U3 | Underspecified | LOW | tasks.md T006 | A partial run (`pytest tests/engine`) reports every other ID as *no evidence*. | Header line "partial run" when not all tests were collected. |
| U4 | Underspecified | LOW | spec.md SC-001; tasks.md T036 | SC-001 is a person's time to first move; T036 measures only program start-up — a partial proxy. | Note that the human part is checked in quickstart M4. |
| U5 | Constraint | LOW | plan.md *Constraints* (L47); tasks.md T001 | "Offline" holds at run time only; the first `uv sync` downloads `hatchling` and `pytest`. | Reword to "offline at run time". |
| D1 | Duplication | LOW | spec.md FR-005/SC-006; FR-017/edge "Invalid menu choice"; US2-3/SC-004 | Rule-and-measure pairs; not conflicting. | No change. |
| S1 | Style | LOW | spec.md L139 | Line longer than 100 characters (from the clarify edit). | Re-wrap. |

### Coverage

| Requirement | Has task? | Task IDs | Notes |
|---|---|---|---|
| FR-001 | ✓ | T009, T010, T011 | |
| FR-002 | ✓ | T009, T010, T020 | |
| FR-003 | ✓ | T010, T012, T020 | |
| FR-004 | ✓ | T009, T018, T019, T022 | |
| FR-005 | ✓ | T010, T020, T021 | |
| FR-006 | ✓ | T018, T020, T021 | |
| FR-007 | ✓ | T020, T021, T032 | |
| FR-008 | ✓ | T010, T012 | |
| FR-009 | ✓ | T010, T020, T026 | |
| FR-010 | ✓ | T010, T020 | |
| FR-011 | ✓ | T020, T028 | |
| FR-012 | ✓ | T025, T026, T027 | U2 |
| FR-013 | ✓ | T026, T031, T032, T034 | U1 |
| FR-014 | ✓ | T014, T016 | |
| FR-015 | ✓ | T030, T034 | I5 |
| FR-016 | ✓ | T014, T030 | |
| FR-017 | ✓ | T014, T030 | |
| FR-018 | ✓ | T032, T033, T034 | |
| FR-019 | ✓ | T026, T028 | |
| FR-020 | ✓ | T015, T016 | I1, A1 |
| SC-001 | ✓ | T036 | U4 |
| SC-002 | ✓ (manual) | T037, T040 | |
| SC-003 | ✓ | T010, T020 | |
| SC-004 | ✓ | T025 | |
| SC-005 | ✓ | T026 | |
| SC-006 | ✓ | T010, T020 | G1 |

### Constitution alignment

- **Principle II / Records of Change** — C1 (MUST weakened to "should"), C2 (a II(b) step
  labelled II(c)).
- **Principles I, III, IV, V** — reflected correctly: tests are tagged as evidence; a
  failing test is reported to the developer, not resolved by the agent; spec gaps are
  raised as proposals; a conformance report is generated on every run.

### Tasks with no spec requirement

T001–T003 (setup), T004–T008 (evidence tooling, architecture rule, shared positions — they
trace to the constitution and plan.md R3/R7), T039 (README). All are expected.

---

## Part 2 — Edits recommended before `/speckit-implement`

Apply in this order: **spec** (governs everything) → **plan and contracts** → **tasks**
(constitution, *Document Hierarchy*). E1–E7 are recommended before implementation; E8 is a
small coverage fix worth doing at the same time. Line numbers refer to commit `df82f4c`.

### E1 — tasks.md, Notes: restore the MUST (fixes C1)

Replace:

```markdown
- **Commit messages** (constitution Principle II, Records of Change): every commit made
  while carrying out these tasks is case **II(c)** — the realization is being brought into
  conformance with the current specification — and its message should say so (e.g. end
  with `Change type: II(c) — implements FR-008, US1-6`).
```

with (this also carries E3's Notes change):

```markdown
- **Commit messages** (constitution Principle II, Records of Change): every commit that
  changes the realization MUST identify which of II(a), II(b), or II(c) applies, e.g. by
  ending with a line `Change type: II(c) — implements FR-008, US1-6`.
  - Building a task's behavior for the first time is **II(c)**.
  - Restructuring code already written without changing behavior (e.g. T022's refactor of
    the start menu) is **II(b)**: run the full test suite before committing, and the
    message MUST state that no specified behavior changed.
  - Fixing code that a test showed to be non-conforming is **II(a)** — after the
    developer has decided that the code, not the spec, changes (Principle III).
```

### E2 — tasks.md T015 and T020: move the mid-game end-of-input case (fixes I1)

In **T015**, replace:

```markdown
input that ends (empty `StringIO`, or input ending after `2\n` mid-game) makes `run()` print a goodbye line and return 0 without raising
```

with:

```markdown
input that ends at the start menu (empty `StringIO`, or input ending after an invalid choice such as `7\n`) makes `run()` print a goodbye line and return 0 without raising
```

At the end of **T020**, before "Do not assert what happens after the result line …", add:

```markdown
; input that ends mid-game (`2` and two moves, then nothing) prints the goodbye line and `run()` returns 0 (`FR-020`, `US3-6`, `EDGE-end-of-input-or-interrupt`)
```

### E3 — tasks.md T022: label the refactor (fixes C2)

In **T022**, replace:

```markdown
refactor T016's start menu to use `parse_menu`
```

with:

```markdown
then, as a separate II(b) commit (see Notes), refactor T016's start menu to use `parse_menu` — run `uv run pytest` before committing; T014 must still pass unchanged
```

### E4 — contracts/cli.md §1: say when the opponent is created (fixes U1)

After the *Entry point for tests* paragraph (ending "calls it with the real terminal
streams."), add:

```markdown
`run()` calls `opponent_factory()` once each time "Play the computer" is chosen from the
start menu, and uses that opponent for every game of the series ("play again"), until the
player returns to the start menu. It is never called in two-player games.
```

Then in **tasks.md T020**, extend the `ScriptedOpponent` description with: "one instance
serves a whole vs-computer series, so its move list covers every game the test plays
before returning to the start menu (contracts/cli.md §1)".

*Why this choice*: it matches the CLI's *Session* (data-model.md) — the opponent lives as
long as the series — and lets one scripted list drive T031. The alternative, once per game,
also satisfies the spec; pick it instead if you would rather each game get a fresh opponent.

### E5 — plan.md, Project Structure: list the files tasks.md creates (fixes I2)

In the *Source Code* tree, replace the `pyproject.toml` line and the whole `tests/` block:

```text
pyproject.toml                    # package metadata, console script, pytest dev group
```

```text
tests/
├── conftest.py                   # `req` marker + conformance-report plugin (R7)
├── test_architecture.py          # enforces the dependency rule (R3)
├── engine/                       # evidence for contracts/engine.md
├── opponent/                     # evidence for contracts/opponent.md
└── cli/                          # transcript tests for contracts/cli.md
```

with:

```text
pyproject.toml                    # package metadata, console script, pytest dev group
uv.lock                           # locked dev environment (committed)
README.md                         # how to run the game and the tests
```

```text
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
```

### E6 — spec.md FR-020 and edge case: make it testable (fixes A1)

Replace FR-020 (L205–206):

```markdown
- **FR-020**: If input ends or the player interrupts the program at any prompt, the program
  MUST end promptly with a short goodbye message and without an error trace.
```

with:

```markdown
- **FR-020**: If input ends or the player interrupts the program at any prompt, the program
  MUST print a single goodbye line and end within 1 second, without an error trace.
```

Replace the edge-case bullet (L148–149):

```markdown
- **End of input or interrupt**: the terminal's input ends (e.g. Ctrl-D) or the player
  interrupts the program (e.g. Ctrl-C) at any prompt. The program ends promptly (FR-020).
```

with:

```markdown
- **End of input or interrupt**: the terminal's input ends (e.g. Ctrl-D) or the player
  interrupts the program (e.g. Ctrl-C) at any prompt. The program prints one goodbye line
  and ends (FR-020).
```

Then in **contracts/cli.md C-17** add "within 1 second" after "exits with status 0", and in
**tasks.md T015** add "within 1 second" to the expected result.

### E7 — spec.md: one word for the board (fixes I3)

Replace "grid" with "board" at L31, 32, 34, 46, 81, 106, 122, 164, 167, 196, 210 (e.g.
"draws an empty 9-by-9 board", "an empty board is drawn", "within the board", "draw the
board", "new empty board"). Two lines need rewording rather than a word swap:

- **FR-001** (L157): "The game MUST be played on a board of 9 rows and 9 columns of
  squares, all empty at the start of each game."
- **Key Entities, Board** (L210): "**Board**: the 9-by-9 arrangement of squares; each
  square is empty or holds one mark."

Extend the glossary assumption (L255–256):

```markdown
- The ConOps glossary is TBD. This spec uses: **square** (not cell), **mark**, **line**,
  **draw** (not tie). "Play again" in this spec is what the ConOps calls a rematch.
```

to:

```markdown
- The ConOps glossary is TBD. This spec uses: **board** (not grid), **square** (not cell),
  **mark**, **line**, **draw** (not tie) for the result. "Draw the board" means display it.
  "Play again" in this spec is what the ConOps calls a rematch.
```

While editing, re-wrap L138–139 (S1).

### E8 — tasks.md T014 and T030: tag SC-006 (fixes G1)

In **T014**, change `(`FR-017`, `EDGE-invalid-menu-choice`)` to
`(`FR-017`, `SC-006`, `EDGE-invalid-menu-choice`)`. Make the same change in **T030**.

### Changelog entry for the spec edits (constitution, Records of Change)

E6 and E7 change `spec.md`, so `specs/001-five-in-a-row/CHANGELOG.md` needs an entry. Suggested
text:

```markdown
- `/speckit-analyze` follow-up, decided by the developer:
  - FR-020 and its edge case: "end promptly with a short goodbye message" replaced by
    "print a single goodbye line and end within 1 second". Reason: the original wording had
    no measure a test could fail (analysis A1).
  - "Grid" replaced by "board" throughout; "board" added to the glossary. Reason: one term
    for one concept, matching the contracts (analysis I3). No behavior change.
```

### After the edits

1. Commit the spec and changelog first, then the plan and contract, then tasks.md (or all
   together, with the order noted in the message).
2. Re-run `/speckit-analyze`. Expected result: no CRITICAL, HIGH, or MEDIUM findings; the
   LOW items I4, I5, U2–U5, I6, D1 may remain.
3. Proceed to `/speckit-implement`.

### LOW items — optional, any time before T038

| ID | Edit |
|----|------|
| I4 | data-model.md, top: "The spec's *Game* is split here: rules state in `GameState` (engine); mode and which mark the human holds in `Session` (CLI). The spec's *Player* has no class of its own — a side is a `Mark`, and the CLI knows which side is the human." |
| I5 | No document change; say "interim: returns to start menu until T034" in T023's commit message. |
| U2 | T025, append: "Uniformity (FR-012 'each equally likely') is shown by review of `rng.choice` use; the test shows coverage (SC-004)." |
| I6 | spec.md L3 and plan.md header: "n/a (work on `main`)". Set spec Status to "Approved" when you consider it so. |
| U3 | T006, append: "If fewer tests were collected than exist under `tests/`, the report header says 'partial run'." |
| U4 | T036, append: "The human part of SC-001 is checked in quickstart M4." |
| U5 | plan.md L47: "offline at run time (the first `uv sync` needs the network), …" |
