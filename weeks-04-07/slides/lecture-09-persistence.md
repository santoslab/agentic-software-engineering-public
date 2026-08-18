---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
  }
  section.lead {
    background: #310066;
    color: #ffffff;
  }
  section.lead h1, section.lead h2 {
    color: #ffffff;
  }
  section.standout {
    background: #beaefc;
    color: #310066;
    text-align: center;
    font-size: 36px;
  }
  h1, h2 {
    color: #310066;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->

# Persistence: Data Modeling, Migrations, Integration Testing

**Agentic Software Engineering — Lecture 9**
Week 5 · Meeting 1 of 2 · launches **Stage B**

---

## The one idea

A migration is **a spec that executes** — and the fresh-clone gate is the only honest proof a data layer exists.

---

## State changes everything

Until today: the repo *is* the program. Every clone identical; every checkout a time machine.

A database is the first artifact your repo doesn't carry:

- exists only on your machine
- accumulates history your commits know nothing about
- **diverges**

*"Works on my machine" = "my machine has state your clone can't reproduce."*

<!-- 0-8 min. -->

---

## Model backwards from the queries

Stage B must answer: **the leaderboard** (W/L/T per player, ranked) and **a player's recent games** (Stage E serves exactly this via MCP).

```sql
CREATE TABLE players (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);
CREATE TABLE games (
    id        INTEGER PRIMARY KEY,
    x_player  INTEGER NOT NULL REFERENCES players(id),
    o_player  INTEGER NOT NULL REFERENCES players(id),
    winner    INTEGER REFERENCES players(id),   -- NULL = tie
    played_at TEXT NOT NULL
);
```

Two tables. W/L/T are **derived** by query.

---

## Why no `wins` column?

The moment a game row and a counter *can* disagree, one day they **will** — a crash between writes, a hand edit, an agent updating one and not the other.

Then your database holds two answers to one question, and no way to know which is the lie.

**Derive, don't duplicate.** The spec states the truth once:
*"a player's win count is the number of games whose winner is that player."*

(The day deriving is too slow, add the cache — as a decision, in a commit, with a clause.)

<!-- 8-24 min. The update anomaly, textbook version. -->

---

## Migrations: the schema's history, executable

```python
MIGRATIONS = [migration_1_initial, migration_2_played_at_index]

def migrate(db):
    current = get_version(db)      # 0 on a fresh database
    for number, step in enumerate(MIGRATIONS, start=1):
        if number > current:
            step(db)
            set_version(db, number)
```

- **Idempotent** — running twice is safe; any older version catches up
- **Append-only** — committed migrations are never edited; changes are *new* functions

The file reads top to bottom as the schema's entire history. That's a replayable spec.

---

<!-- _class: standout -->

## The fresh-clone gate

`git clone` → `python migrate.py` → `python seed.py` → `python main.py`

**Empty checkout to working, populated system, in documented commands.**

A warm working tree proves nothing.

---

## Gates drive tooling

The case study's M2 gate — *fresh clone boots populated* — forced an amendment worth reading:

> *"M2's gate requires proving that each M-N association round-trips, and there is **no honest way to prove that without a test runner**. So the harness was pulled forward into M2, and `npm test` has guarded main from M2 onward."*

The test harness arrived a milestone **early** because the gate demanded proof.

**Gates drive tooling; tooling does not excuse gates.**

<!-- 24-38 min. -->

---

<!-- _class: standout -->

## Demo: a migration lifecycle in miniature

v1 from nothing → rerun (no-op) → v2 adds a column → seed → leaderboard query → `rm` the DB and replay everything in one line

<!-- 38-52 min. The one-line replay IS the fresh-clone gate. -->

---

## The testing split

| | Unit | Integration |
|---|---|---|
| What | The engine suite — **untouched** | Everything touching the DB |
| I/O | None | Real sqlite3, real files, real migrations |
| Speed | Fast | Slower, and that's fine |

```python
@pytest.fixture
def db(tmp_path):
    conn = sqlite3.connect(tmp_path / "test.db")
    migrate(conn)          # the REAL migrations build every test DB
    yield conn
    conn.close()
```

**Fresh database per test** — and your migration chain gets exercised dozens of times a day, free.

---

## The layering rule

**`game.py` never imports `sqlite3`.**

Persistence is a *caller's* concern: `main.py` records results; the engine plays tic-tac-toe.

The proof is mechanical and you already own it: the engine's 100% branch gate runs **without any database at all**.

<!-- 52-64 min. If an engine test wants a DB, the change is on the wrong side of the line. -->

---

## Stage B checklist (from the brief)

- [ ] Data model spec'd **before** the schema commit
- [ ] `migrate.py` + `seed.py`; fresh-clone gate demonstrated (paste the transcript)
- [ ] Unit / integration split visible in `tests/`
- [ ] CLI wiring: names, results recorded, leaderboard menu
- [ ] **`BACKLOG.md` goes live** — every stage now starts by reading it
- [ ] Custom skill — assigned Thursday

---

## Questions to think about

1. When does "delete the DB and re-run migrate + seed" stop being a valid recovery strategy — and what must exist by then?
2. Run the L08 ripple hunt on "store the full move list of every game." Stage B or backlog? Write the entry.
3. What bug class does fresh-DB-per-test catch that a shared test database hides?

---

## Before Thursday

- [required] Claude Code docs: Skills / slash commands
- [recommended] Re-read grill-me — as a *program* this time

**Thursday: the prompts you keep retyping become assets.**
