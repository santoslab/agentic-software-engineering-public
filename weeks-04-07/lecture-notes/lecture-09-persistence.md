# Lecture 09 — Persistence: Data Modeling, Migrations, Integration Testing

> Week 5, meeting 1 of 2. Companion reading for the lecture; self-contained.
> Launches **Stage B**.

## State changes everything

Until today, your repository *is* your program. Anyone who clones it has exactly
what you have; every `git checkout` is a time machine; two clones can never
disagree. The moment Stage B adds a database, that stops being true. A database is
the first artifact your repo does not carry: it exists only on your machine, it
accumulates history your commits know nothing about, and it diverges — between
your laptop and your grader's, between this week and last week, between "works"
and "works on my machine."

Almost every "works on my machine" is really "my machine has state your clone
cannot reproduce." The entire lecture is one idea with three mechanisms: **make
the state reproducible from the repo.** The mechanisms are a data model someone
decided on purpose, migrations that replay that decision anywhere, and a gate that
proves it.

## Data modeling: start from the queries

The wrong way to start is "what tables should a tic-tac-toe game have?" — that
question has infinitely many defensible answers. The right way is to start from
what Stage B must *answer*:

1. The leaderboard: every player's wins, losses, and ties, ranked.
2. A player's record and recent games (Stage E will serve exactly this via MCP).

Work backwards from those two queries and the model nearly writes itself:

```sql
CREATE TABLE players (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE games (
    id        INTEGER PRIMARY KEY,
    x_player  INTEGER NOT NULL REFERENCES players(id),
    o_player  INTEGER NOT NULL REFERENCES players(id),
    winner    INTEGER REFERENCES players(id),   -- NULL means a tie
    played_at TEXT NOT NULL                     -- ISO 8601, UTC
);
```

Two tables. Wins, losses, and ties are *derived* — a query groups `games` and
counts. Now the decision worth dwelling on, because it is the classic one:

**Why is there no `wins` column on `players`?** It would make the leaderboard
query trivial. It would also create the textbook *update anomaly*: the moment a
game row and a counter can disagree, one day they will — a crash between the two
writes, a hand-edited row, an agent "helpfully" updating one and not the other.
Then your database contains two answers to the same question, and no way to know
which is the lie. Derive, don't duplicate: at this scale the counting query is
instant, and the spec states the truth exactly once ("a player's win count is the
number of games whose winner is that player"). If the day comes when deriving is
too slow, *that* day you introduce a cache — as a decision, in a commit, with a
clause. (Write the counter-column's failure into your integration tests' heads:
the test you would need is "counter equals count(games)", and the need for that
test is the model critiquing itself.)

And per the standing rule: the model above goes into your spec (a data section of
SPEC.md is fine) *before* the commit that creates the schema. Spec, then code —
the rule did not change when the artifact became a database.

## Migrations: the schema's history, executable

A migration script answers one question, executably: **how does an empty directory
become the current schema?** Yours can be plain Python on `sqlite3` — a
`schema_version` table, numbered migration functions, apply-the-missing-ones:

```python
MIGRATIONS = [migration_1_initial, migration_2_played_at_index]

def migrate(db):
    current = get_version(db)          # 0 on a fresh database
    for number, step in enumerate(MIGRATIONS, start=1):
        if number > current:
            step(db)
            set_version(db, number)
```

Two properties turn this from "a script" into "a spec that executes":

- **Idempotent.** Running it twice is safe; running it on any older version
  produces the same result as running it on empty. It does not matter *when* you
  clone — the migration chain catches you up.
- **Append-only.** Migration 1 is never edited once committed. Schema changes are
  *new* numbered functions. The file reads top to bottom as the schema's entire
  history — which is exactly what a replayable spec is.

Seeds are the same idea for data: `seed.py` loads sample players and games so a
fresh clone boots into something usable and demonstrable. Seeds are executable
documentation — "here is what this system's data looks like" — and they are what
your integration tests and your in-class demos stand on.

## The fresh-clone gate

Here is Stage B's gate, and it is the only honest proof a data layer exists:

```
git clone <your-repo> && cd <repo>
python migrate.py && python seed.py
python main.py        # leaderboard menu shows seeded players
```

Empty checkout to working, populated system, in documented commands. Not "works
in my working tree" — a warm tree proves nothing, because your working tree has
the state (Lecture 11 makes the same point about smoke tests, and it is the same
point).

This gate has a distinguished history in the course's case-study corpus. The
lost-communities project's plan defines milestone gates mechanically — "a red
gate returns the work to in-progress; it does not advance" — and its M2 gate was
exactly this one: *fresh clone boots populated*. The instructive part is what
that gate forced. The plan's own amendment note, quoted:

> M2's gate requires proving that each M-N association round-trips, and there is
> no honest way to prove that without a test runner. So the Mocha + Chai harness
> was pulled forward into M2, and `npm test` has guarded main from M2 onward.

The test harness arrived a milestone *early* because the gate demanded proof the
tooling couldn't yet give. **Gates drive tooling; tooling does not excuse gates.**
When your fresh-clone run needs something your repo doesn't have yet — that is
the gate telling you what to build next.

## Integration tests, and where they live

Stage B splits your test suite in two, and the split must be visible:

- **Unit tests** — the existing engine suite. Pure, fast, no I/O. *Untouched.*
- **Integration tests** — everything that touches the database. Real `sqlite3`,
  real files, real migrations.

The non-negotiable pattern for the second kind: **a fresh database per test.**
With pytest this is a fixture and a temp directory:

```python
@pytest.fixture
def db(tmp_path):
    conn = sqlite3.connect(tmp_path / "test.db")
    migrate(conn)          # the real migrations, not a parallel schema
    yield conn
    conn.close()
```

Note what that fixture quietly buys you: every test runs against a database built
by *your actual migration chain* — so the migrations themselves are exercised
dozens of times a day, for free. A test database built by any other means (a
checked-in `.db` file, a hand-written `CREATE TABLE` in the test) is a second
schema that will drift from the first.

And the layering rule, stated once and enforced forever: **`game.py` never
imports `sqlite3`.** Persistence is a caller's concern — `main.py` records
results; the engine plays tic-tac-toe. The proof is mechanical and you already
own it: the engine's 100% branch coverage gate runs without any database at all.
If a Stage B change makes an engine test want a database, the change is on the
wrong side of the line.

## Stage B, concretely

From the brief: model spec'd first; `migrate.py` + `seed.py` with the fresh-clone
gate demonstrated (paste the transcript); CLI wiring (name capture, results
recorded, leaderboard menu); `BACKLOG.md` goes live — from now on every stage
starts by reading it; and Thursday's lecture adds the custom skill requirement.
Pacing: schema and migrations by mid-week, wiring and seeds by the weekend, so
the skill lands on a working data layer.

## Questions to think about

1. "Delete the database and re-run migrate + seed" is a perfectly good recovery
   strategy for Stage B. Name the exact moment in this project's future (think
   Project 2, or one real user) when it stops being one, and what has to exist by
   then.
2. Someone proposes storing the full move list of every game (for replays,
   someday). Run the ripple hunt from Lecture 08 on that change: which artifacts
   move? Then argue whether it belongs in Stage B or in BACKLOG.md — and write
   the backlog entry, why-it-matters line included.
3. Your integration fixture migrates a fresh database per test. What specific
   class of bug does this catch that a shared, session-scoped test database
   would hide? (Hint: what does test A's data do to test B's assertions?)
