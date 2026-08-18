# Project 1 — The Growing Tic-Tac-Toe

> **Solo project - Weeks 4-7 - due at the start of week 8 (Lecture 15)** - 30% of the
> course grade - target effort 6-8 hours/week.
>
> **The one rule that governs everything: the spec changes before the code does.**
> Every stage below is graded partly on *process evidence in your git history* — a
> commit that changes behavior without a preceding (or included) spec change is the
> main way to lose credit in this project.

## 0. What this project is

You receive a working program — a 9x9 tic-tac-toe variant (five in a row wins) with a
CLI, a random-move computer opponent, and a green test suite — and **no specification
of any kind. That gap is deliberate, and closing it is Stage A.**

Over four weeks the program grows through five stages: own the spec (A), persistence
(B), a web interface (C), a TypeScript port of the engine (D), and an MCP server (E).
Each stage pairs one classical software-engineering practice with one Claude Code
capability, and each lands the same week as the lecture that teaches it. By the end
you will have practiced every one of the five agentic principles on a codebase that
you grew deliberately, with the evidence to prove it.

This is the same shape as the course's own experiments: the 9x9 game you studied in
Lecture 4 grew from a 3x3 game, gained a real ConOps and SPECS only when an attempt
without them went sideways, and was later ported to Java on the strength of those
documents alone. You are going to do that arc on purpose, instead of discovering it
the hard way.

## 1. What you get

The starter (`tictactoe-starter/`, from the course student repo):

| File | What it is |
|---|---|
| `game.py` | The engine: `Game` class — board state, move validation, win/tie detection, rendering |
| `computer_ai.py` | `ComputerAI.random_move` — the entire "AI" |
| `main.py` | CLI: menus, 1-player and 2-player modes, the two-step row-then-column input flow |
| `tests/` | ~90 pytest tests, all green |
| `.coveragerc`, `pytest.ini`, `requirements-dev.txt` | pytest + coverage configuration |

Also shipped with this brief (in `student-materials/`, distributed per stage):

- `fixtures/` — shared game-scenario fixtures for Stage D's differential testing
- `stage-d-scaffold/` — `package.json` + `tsconfig.json` for the TypeScript port
- `hooks/` — the original PowerShell cost hook that Stage C asks you to port
- `mcp-example/` — a minimal FastMCP server in a neutral domain, for Stage E's shape

Set up: fork/copy the starter into your own repo, create a venv, `pip install -r
requirements-dev.txt`, confirm `pytest` is green and `pytest --cov` runs. Commit that
as your baseline before touching anything.

## 2. The five stages

Stage checkpoints are pacing targets; the hard deadline for everything is the start
of week 8. Falling a few days behind a checkpoint is survivable. Attempting D and E
in the last weekend is not — they depend on B's database and A's spec being solid.

### Stage A — Own the spec *(week 4; taught by Lectures 07-08)*

**Reverse-engineer the specification, then make your first spec-driven change.**

1. **Elicit a SPEC.md from the code.** Use Claude to interrogate the starter — but
   *you* own every sentence. The spec must state the actual behavioral contract:
   board geometry, win/tie rules, move-validation rules (what exactly is rejected,
   and what happens to the turn when it is), the two-step input flow, menu flows,
   and AI behavior. At least two behaviors in this codebase are *decisions the spec
   must take a position on* — for example, what the engine does if `make_move` is
   called after the game is over. Finding these edges is the exercise.
2. **Write a one-page mini-ConOps** — user's-eye view, implementation-free (it never
   says "Python"). Lecture 07 shows the IEEE-1362-derived model from the course
   repo; yours is one page, not forty.
3. **One spec-driven extension.** Default (recommended): make board size and win
   length configurable from the main menu (e.g., 3x3/3, 9x9/5, 19x19/5). Note the
   ripple: `main.py`'s prompt strings hard-code "1-9" — your spec amendment has to
   catch what the constants alone won't. Alternatives (equal credit): a heuristic AI
   (win-if-possible, block-if-needed) or an undo command. Whichever you pick: **amend
   SPEC.md and get the amendment committed before the implementing commit.**
4. **Bind the gate in CLAUDE.md.** Write your project CLAUDE.md; it must state the
   coverage law: *engine (`game.py`) at 100% branch coverage, enforced, always.*

**Required elements (all must be present):**

- [ ] `SPEC.md` — behavioral contract covering engine, CLI flow, and AI; takes an
      explicit position on at least two edge-case behaviors you found in the code
- [ ] `CONOPS.md` — one page, implementation-free
- [ ] `CLAUDE.md` — includes the engine coverage law and how to run tests
- [ ] The extension, implemented and tested; `pytest` green
- [ ] `pytest --cov` shows **100% branch coverage on `game.py`**
- [ ] Git history shows the spec amendment committed **before or with** — never
      after — the extension's implementation
- [ ] Plan mode used for the extension; the approved plan committed under `plans/`

### Stage B — Persistence *(week 5; taught by Lectures 09-10)*

**Add SQLite users, scores, and a leaderboard — with migrations, seeds, and a
backlog.**

1. **Data model.** Players and completed games (who played, who won, when; enough to
   derive a leaderboard: wins/losses/ties per player). Spec the model in SPEC.md (or
   a `SPEC-data.md` section) *first*.
2. **Migrations as replayable specs.** A `migrate.py` (or equivalent) that takes an
   empty directory to a current schema, idempotently. A `seed.py` that loads sample
   players and games. **The gate: a fresh clone plus two documented commands yields
   a migrated, seeded database.** (This is the lost-communities M2 gate at toy
   scale; the same gate returns in Project 2.)
3. **Wire the CLI.** Name capture, results recorded, a leaderboard menu entry.
   The engine (`game.py`) does not change — persistence is a caller's concern.
4. **Start `BACKLOG.md`.** From now on, every loose end, deferred decision, and
   known imperfection lands there — and stays until resolved or explicitly closed.
5. **Build a custom skill** (this stage's Claude feature; Lecture 10). Pick one type:
   *scaffolding* (e.g., generate a migration file pair from a description), *review*
   (e.g., check a diff against your SPEC), or *documentation* (e.g., update the
   leaderboard section of your docs from the schema). It must be a real skill in
   `.claude/skills/`, and **you must use it at least once in Stage C or D and cite
   where.**

**Required elements:**

- [ ] Data-model spec committed before the schema-implementing commit
- [ ] `migrate.py` + `seed.py` (or equivalent); fresh-clone gate documented in
      README and demonstrated (paste the transcript of the two commands in the
      stage's commit message or README)
- [ ] Unit vs integration split visible in `tests/` (engine tests untouched;
      new DB tests are integration tests and marked/foldered as such)
- [ ] Leaderboard reachable from the CLI; recorded games persist across runs
- [ ] `BACKLOG.md` exists and has real entries (an empty backlog after a stage this
      size is not credible)
- [ ] Custom skill committed under `.claude/skills/` with a line in its README
      saying what type it is and when it's meant to run

### Stage C — The web layer *(week 6; taught by Lectures 11-12)*

**Play in the browser; leaderboard page; and your environment starts automating
itself.**

1. **Flask + Jinja + light JS.** Server-rendered: a play page (click a cell to move
   against the computer) and a leaderboard page over the Stage B database. The
   engine still does not change — the web layer is another caller, like the CLI.
2. **A written gate checklist.** Lecture 11's lesson made mechanical: a
   `GATES.md` listing your lint, test, and smoke gates — the exact commands and
   what "green" means. **Run it before every commit from here on.** Smoke means: a
   fresh clone, documented setup, server boots, both pages render.
3. **Flask test-client integration tests.** Both paths per route where it matters
   (a good move and a rejected move; a leaderboard with data and one without).
4. **Port the cost hook** (this stage's Claude feature; Lecture 12). The original
   PowerShell SessionEnd hook ships in `student-materials/hooks/` — **the .ps1 is
   your spec**. Port it to cross-platform Python: same CSV columns, same
   never-block-exit guarantee, works on macOS/Linux/Windows. Register it in
   `.claude/settings.json` and commit a `session-costs.csv` with real rows from
   your own sessions. (Notice what this is: a behavior-preserving port from a
   language you may not know, against an artifact-as-spec. Stage D does it again,
   bigger.)
5. **Per-directory CLAUDE.md.** At minimum `web/` (or wherever Flask lives) gets
   its own CLAUDE.md stating the layering rule and the test commands for that
   layer.

**Required elements:**

- [ ] Play + leaderboard pages, server-rendered, working from a fresh clone with
      documented setup
- [ ] `game.py` diff across Stage C is empty (layering held)
- [ ] `GATES.md` committed; gate runs visible in the history (e.g., a "gates green"
      line in commit messages, or committed gate output)
- [ ] Flask test-client tests, both-paths where applicable
- [ ] `.claude/hooks/log_cost_on_end.py` + registration; 5 or more real rows in
      `session-costs.csv`
- [ ] Per-directory CLAUDE.md for the web layer

### Stage D — The port *(week 7 first half; taught by Lecture 13)*

**The engine and AI in TypeScript, proven equivalent by shared fixtures.**

1. **Scope: engine + AI + tests only.** No web, no DB, no CLI beyond what tests
   need. Start from `student-materials/stage-d-scaffold/`.
2. **Your SPEC.md is the source, not `game.py`.** Work in a session where the agent
   reads the spec and the shared fixtures — resist pasting the Python in. Where the
   spec turns out to be ambiguous (it will), that's a spec bug: **fix SPEC.md**, in
   its own commit, then continue. Log each one in BACKLOG.md.
3. **Differential testing.** `student-materials/fixtures/scenarios.json` holds
   move-by-move scenarios with expected outcomes. Write a loader on each side
   (pytest, and the TS test runner) so **the same fixture file passes against both
   implementations.**
4. **The compiler is a gate.** `tsc --noEmit` clean, strict mode on (the scaffold
   sets it). This is your first non-test mechanical gate; notice how it changes
   what the agent gets away with.
5. **Honest reporting.** You are working in a language most of you don't know.
   Your stage report (a `STAGE-D-REPORT.md`, half a page) must include a section:
   *what I could not verify by reading* — named, not hand-waved.

**Required elements:**

- [ ] TS engine + AI under `ts/` (or scaffold layout); `npm test` green;
      `tsc --noEmit` clean in strict mode
- [ ] Fixture loader on both sides; **all shared scenarios green in both
      implementations** — same fixture file, unmodified
- [ ] At least one committed SPEC.md clarification found by the port (if you
      genuinely found none, say so in the report — and expect skepticism)
- [ ] `STAGE-D-REPORT.md` with the could-not-verify section

### Stage E — The MCP server *(week 7 second half; taught by Lecture 14)*

**Give Claude a tool of your own making.**

1. **FastMCP server** exposing exactly two tools over the Stage B database:
   `get_leaderboard()` (ranked players with W/L/T) and `get_player_stats(name)`
   (one player's record and recent games). The neutral-domain example in
   `student-materials/mcp-example/` shows the shape; yours queries your real DB.
2. **Tool contracts are docs.** Each tool's docstring states what it returns and
   what happens on unknown players — the docstring *is* the contract the agent
   sees. Write it like you mean it.
3. **Register and demo.** Register the server in Claude Code, then capture a short
   transcript of Claude answering "who's on top of the leaderboard and what's
   their record?" *using your tools* — that transcript is a required element.
4. **Fresh-clone install.** A `README-mcp.md` documenting install (pip or uvx) and
   registration such that a fresh clone works on a machine that isn't yours.

**Required elements:**

- [ ] `mcp_server.py` with the two tools, contract-quality docstrings
- [ ] Registration documented; works from a fresh clone per your README-mcp.md
- [ ] Committed transcript showing Claude calling both tools successfully
- [ ] One BACKLOG.md entry: what you'd add to this server next, and why you didn't

**Optional stretch (documented, zero credit, real bragging rights):** a second MCP
server exposing search over your Project 0 knowledge base (`search_pkb(query)`).
If you build it, note it in your final report.

## 3. Cross-stage process requirements

These hold from Stage A's first commit to the end:

1. **Spec before code** — behavior changes trail a committed spec change. This is
   checked by reading your git history.
2. **Plan mode for every stage's main build** — approved plans are committed under
   `plans/` (plain markdown export is fine). Five stages, at least five plans.
3. **BACKLOG.md is live** from Stage B on — the Lecture 08 discipline: loose ends
   are written down, not remembered.
4. **Gates run before commits** from Stage C on, per your GATES.md.
5. **The engine coverage law** — `game.py` at 100% branch, from Stage A on, stated
   in CLAUDE.md and true at every stage boundary.

## 4. Grading

Completion-based, like everything in this course. Each stage has its
required-elements checklist above; a stage is **satisfactory** when every element is
present and honest — a documented failure or a well-argued deviation counts, a
missing element doesn't. Unsatisfactory stages get one resubmission pass (a red
gate returns work; it doesn't end it).

At project end, one **light holistic pass** against the five agentic principles
(Spec-Driven Development, Cycle of Development, Project Context Management,
Requirement Elicitation, Verification), using your repo's process evidence: the
spec-before-code history, the backlog, the gate runs, the plans, the cost CSV.
Lecture 15 runs the project retrospective; your last deliverable is a half-page
retrospective against those five principles — where each one saved you, or what
happened where you skipped it.

**Weight:** 30% of the course grade — stages roughly equal, holistic pass counted
as one stage-equivalent.

## 5. Do / don't

- **Do** let Claude write most of the code — that's the course. **Own** the spec,
  the plans, the gates, and every commit message.
- **Do** use your Stage B skill, your hooks, and plan mode as *daily tools*, not
  as compliance artifacts produced the night before.
- **Don't** consult the course repo's finished solutions (`9by9_Java`, the
  experiment transcripts' code). Case-study documents cited in lectures are fair
  game; solution *code* defeats the point and is easy to spot.
- **Don't** hide failures. "The migration gate was red for two days; here's what
  it was" is exactly what retrospectives are for — and it's graded as evidence of
  process, not as a defect.
