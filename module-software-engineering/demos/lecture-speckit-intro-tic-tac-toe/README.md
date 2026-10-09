# Spec Kit introduction: five-in-a-row tic-tac-toe

The five-in-a-row tic-tac-toe of [`lecture-03-game-demo/`](../lecture-03-game-demo/),
built a second time with [GitHub Spec Kit](https://github.com/github/spec-kit) and Claude
Code. The game is the same — a 9×9 board, five or more in a line wins, a random computer
opponent or two players at one keyboard — but the route differs: Lecture 03 takes a
concept-of-operations sketch to a family of specifications by hand, while here Spec Kit's
commands drive the work: a project constitution, then `specify` → `clarify` → `plan` →
`tasks` → `analyze` → `implement`.

Everything Spec Kit and the agent produced is in this folder, and the folder's git
history keeps every step as its own commit. Read the commits in order to watch the
pipeline run:

```sh
git log --reverse --stat -- module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe
```

## What is here

- [`tutorial/speckit-walkthrough.md`](tutorial/speckit-walkthrough.md) — a student
  tutorial for readers new to Spec Kit: how the tool is implemented, what `specify init`
  installed, the greenfield workflow, and each step of the session below with its
  prompt, the agent's report, and a walkthrough of the artifacts it produced.
- [`demo-seeds/`](demo-seeds/) — the developer's inputs: the development rules given to
  `/speckit-constitution`, the concept-of-operations sketch given to `/speckit-specify`
  (a shorter variant of the Lecture 03 demo's `starter/CONOPS-sketch.md`), and the
  direction given to `/speckit-plan`.
- [`.specify/memory/constitution.md`](.specify/memory/constitution.md) — the project
  constitution: specification vs. realization, the three kinds of change, who decides
  when they disagree, derived documents, reports.
- [`specs/001-five-in-a-row/`](specs/001-five-in-a-row/) — the feature: `spec.md` and
  its `CHANGELOG.md`, `plan.md` with `research.md`, `data-model.md`, `contracts/` and
  `quickstart.md`, `tasks.md`, the first `/speckit-analyze` result with its proposed
  edits (`analysis-report.md`), and the spec quality checklist.
- [`specs/001-five-in-a-row/transcript/`](specs/001-five-in-a-row/transcript/) — the
  session transcript (Markdown and PDF): every developer request and the report the agent
  gave at the end of each Spec Kit command.
- `src/`, `tests/`, `pyproject.toml`, `uv.lock` — the realization and its evidence.
- `.specify/` and `.claude/skills/` — Spec Kit's templates, scripts, and the
  `/speckit-*` commands as Claude Code skills, as installed by `specify init`.

## The game

Tic-tac-toe on a 9×9 board where five or more marks in a line — across, down, or
diagonal — wins. Play in a terminal against a computer that picks random squares, or with
a friend at the same keyboard. Type a square as row then column, e.g. `4 7`; type `m` to
leave a game.

### Run the game

```sh
uv run five-in-a-row          # or: uv run python -m five_in_a_row
```

Requires Python 3.12 or later and [`uv`](https://docs.astral.sh/uv/). Without `uv`, see
the fallback in [quickstart.md](specs/001-five-in-a-row/quickstart.md#prerequisites).

### Run the tests

```sh
uv run pytest
```

Each test is tagged with the specification IDs it is evidence for. Every run writes
`reports/conformance.md` (not committed), listing each requirement, acceptance scenario,
success criterion and edge case in the spec with its tests and status.

### Documents

- [Specification](specs/001-five-in-a-row/spec.md) — what the game must do
- [Implementation plan](specs/001-five-in-a-row/plan.md) — engine, opponent and CLI
  modules and how they depend on each other
- [Quickstart](specs/001-five-in-a-row/quickstart.md) — how to validate the game
- [Constitution](.specify/memory/constitution.md) — development rules for this project

## Commit hashes in the transcript

The session ran in a private development repository, and the demo was migrated here with
its history; the commits therefore have new hashes. Hashes the agent cites in the
transcript and in `analysis-report.md` are the original ones. This table maps them:

| Original | Public | Commit |
|---|---|---|
| `18b1d5d` | `578f523` | SPECKIT tic tac toe initialization |
| `89a8043` | `fe0a03f` | SPECKIT tic tac toe - initial draft of constitution |
| `d58d650` | `572a959` | docs: amend constitution to v1.0.1 (spec changelog lives at specs/<feature>/CHANGELOG.md) |
| `a978fb2` | `595788a` | docs(spec): add 001-five-in-a-row specification from seed ConOps |
| `db93179` | `13792df` | docs(spec): clarify 001-five-in-a-row (leave-game, computer move, move format) |
| `fac840c` | `ba62775` | SPECKIT tic tac toe - initial result of speckit-plan |
| `6d5fbbe` | `6047d29` | SPECKIT tic tac toe - finalize plan |
| `d7cfec1` | `fcc0c15` | Add project .gitignore for Python bytecode, tool caches, and generated reports |
| `df82f4c` | `932aea7` | SPECKIT tic tac toe - initial result of speckit-tasks |
| `ba48fd3` | `6a014cf` | SPECKIT tic tac toe - updates to specs, plan, tasks after first speckit-analyze |
| `951832b` | `639e20b` | SPECKIT tic tac toe - fixes from second speckit-analyze (I7, I8, I9) |
| `3b9a45d` | `cbc22a8` | Phase 1 (setup): package skeleton, pyproject, uv environment |
| `2ff1e1c` | `4d6a2cd` | Phase 2 (foundational): evidence tooling, engine, CLI shell |
| `5f105bc` | `e260ec0` | Phase 3 (US1): two players at one keyboard |
| `c79996b` | `dc2d491` | Refactor start menu to use parse_menu (T022) |
| `8fcbe1d` | `b3a8f5a` | Phase 4 (US2): play against the computer |
| `ff29322` | `2dd9c89` | Phase 5 (US3): game-over menu, play again, leave a game |
| `ea0decc` | `5e4e610` | Phase 6 (polish): SC-001 timing, SC-002 manual marker, README |
| `57ef48e` | `62bb29d` | SPECKIT tic tac tow - addt seeds for prompts |
| `43a86c2` | `b0fadc5` | SPECKIT tic tac toe - transcript |
| `8e2135e` | — (folded in: the seeds were added at `demo-seeds/` directly) | Move ASE seed documents into TicTacToe/demo-seeds |
| `e512baf` | `19239cf` | Spec input path to moved seed; add classroom session transcript |
