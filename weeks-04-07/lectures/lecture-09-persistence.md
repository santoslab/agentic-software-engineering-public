# Lecture 09 — Persistence: Data Modeling, Migrations, Integration Testing

> **Unit:** weeks-04-07 · **Week 5, meeting 1 of 2** · 75 minutes
>
> **Thesis:** A migration is a spec that executes — and the fresh-clone gate
> ("empty checkout to working, populated system in N documented commands") is the
> only honest proof a data layer exists.

## Learning objectives

After this lecture, students can:

1. Design a minimal relational model by working *backwards from the queries* the
   feature needs.
2. Write an idempotent migration script and a seed script, and explain why each is
   a spec rather than a convenience.
3. State the fresh-clone gate and demonstrate it on their own repo.
4. Split unit from integration tests and place database tests correctly (fresh
   database per test, engine tests untouched).

## Before class

- [recommended] Python `sqlite3` module docs — the tutorial section.
- [recommended] A migration folder from your Ex. 2 target repo, revisited.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–8 | Cold open: state changes everything | Until today the repo *is* the program — clone it, run it, identical. A database is the first artifact your repo doesn't carry: it exists only on your machine, accumulates history, and diverges. "Works on my machine" is almost always "my machine has state your clone can't reproduce." The whole lecture is one idea: make the state reproducible from the repo. |
| 8–24 | Data modeling, backwards from queries | Don't start with tables; start with what Stage B must answer: the leaderboard (W/L/T per player, ranked) and a player's recent games. Worked example on the board: derive `players(id, name UNIQUE)` and `games(id, x_player, o_player, winner NULLable for tie, played_at)`; stats *derived* by query, not stored. Discuss the rejected alternative — a `wins` counter column — and why derived beats materialized at this scale (no update anomaly; the spec states truth once). Spec the model in SPEC.md *before* the schema commit — same rule as ever. |
| 24–38 | Migrations and seeds as replayable specs | A migration answers "how does an empty directory become the current schema" — *executably*. Idempotency (running twice is safe) is what makes it a spec rather than a one-shot script. Seeds are executable documentation: the sample data a fresh clone boots with. The case-study anchor: lost-communities' M2 gate — "fresh clone boots populated" — and its instructive amendment: the test harness got pulled *forward* a milestone because the gate ("prove each association round-trips") could not be met honestly without a runner. Gates drive tooling, not vice versa. |
| 38–52 | Demo 1 — a migration lifecycle in miniature | Live: scratch directory → `migrate.py` creates v1 schema → rerun (no-op, idempotent) → v2 adds a column → seed → the leaderboard `SELECT` works. Then the punchline command sequence students must own: `git clone … && python migrate.py && python seed.py && python main.py` → leaderboard has data. |
| 52–64 | The testing split | Unit tests: pure, fast, no I/O — the engine suite stays exactly as it is. Integration tests: touch the DB, need setup/teardown — **fresh temp database per test** via a pytest fixture (show the `tmp_path` conftest pattern). Layering consequence: `game.py` never imports `sqlite3`; persistence is a *caller's* concern, and the test folders should make the split visible (`tests/unit/`, `tests/integration/` or markers). |
| 64–75 | Stage B walkthrough + Q&A | The brief's checklist: model spec'd first; migrate + seed + fresh-clone gate demonstrated; CLI wiring; BACKLOG.md goes live; the custom skill is assigned Thursday (L10). Pacing: schema by mid-week, wiring by the weekend. |

## Demos

### Demo 1 — A migration lifecycle in miniature

- **Artifacts:** a prepared `migrate.py` (~30 lines: `schema_version` table,
  numbered migration functions, applies the missing ones) and `seed.py` (~15
  lines); scratch directory.
- **Setup (before class):** scripts tested; terminal font large; delete any
  leftover `*.db` from rehearsal.
- **Script:** (1) run `migrate.py` on nothing — schema appears; (2) run it again —
  "already at v2", nothing breaks; (3) show adding migration 3 as a function —
  *this file is the schema's history*; (4) seed; (5) run the leaderboard query;
  (6) `rm` the DB and replay the whole chain in one line — the fresh-clone gate,
  live.
- **Expected outcome:** migrations demystified — a numbered list of idempotent
  steps — and the gate seen working end to end in under a minute.
- **Fallback:** the same sequence as a recorded terminal cast; the scripts as
  static listings (they're short enough to read on slides).

## Discussion prompts

1. When is "delete the database and recreate it" a perfectly good migration
   strategy — and what changes the moment it isn't? (Dev vs anything shared;
   the moment one row exists you can't regenerate.)
2. The `wins`-counter column we rejected: name the exact bug it invites, and the
   test that would catch it.
3. What is the toy-scale equivalent of a data-loss incident in Stage B, and which
   artifact prevents it?

## Assigned after class

- Readings (for L10):
  - [required] Claude Code docs: Skills / slash commands (how skills are defined
    and discovered).
  - [recommended] Re-read the grill-me skill file — this time as a *program* you
    are about to write more of.
- Project: **Stage B** launched today.

## Instructor notes

- **Cut if running long:** the testing split (52–64) compresses to the conftest
  slide + the layering rule; it is re-taught by doing in Stage B anyway.
- **Risks:** students with database coursework will find the modeling trivial —
  aim the depth at *migrations as specs* and the gate, which are new to almost
  everyone. Keep the demo's v2 migration truly one column, or the idempotency
  story muddies. SQLite ships with Python — resist any ORM discussion today
  (raw `sqlite3` is the point at this scale; note P2 revisits the question).
- **Variants:** strong room — ask *them* to derive the schema from the leaderboard
  query before showing yours; the counter-column trap usually surfaces on its own.
