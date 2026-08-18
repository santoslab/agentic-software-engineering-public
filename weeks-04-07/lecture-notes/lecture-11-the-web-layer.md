# Lecture 11 — The Web Layer: Testing Types Become Mechanical Gates

> Week 6, meeting 1 of 2. Companion reading for the lecture; self-contained.
> Launches **Stage C**. PKB checkpoint 1 is due today.

## Green suite, broken app

The course's large-scale case study keeps a table of verification gates, and its
"smoke" row carries a rationale worth reading twice:

> Server boots and /docs renders — supertest never starts bin/www, so unit tests
> cannot catch a broken boot. A clean clone has no .env (it is gitignored), and
> without one /docs 404s — so smoke-test from a fresh checkout, not from a warm
> working tree.

Two separate lessons are compressed in there. First: the HTTP-level test suite
*never starts the real server* — it drives handlers through a test harness. Every
test can be green while the actual application fails to boot. Second: even
running the real server proves the wrong thing if you run it from your warm
working tree, because your tree has state (a `.env`, an installed dependency, a
migrated database) that a fresh clone does not. You met this exact argument in
Lecture 09 as the fresh-clone gate. It is the same argument. It is always the
same argument.

The general principle: **a test type is a claim type.** "The functions are
correct" (unit), "the pieces cooperate" (integration), "the application starts
and serves" (smoke), "a user can do the thing" (end-to-end) are different
*sentences* — no quantity of one substitutes for another. The classical
testing-types taxonomy you learned in earlier courses stops being exam trivia
the day each type becomes a gate: a named check, with a command, that must be
green before work advances.

## The taxonomy, mapped onto Stage C

Stage C adds Flask, Jinja templates, and light JavaScript to your project. Here
is the pyramid, made concrete on your own stack:

| Type | In your project | The claim | Gate command (yours will vary) |
|---|---|---|---|
| Unit | The engine suite — untouched since Stage A | The rules of the game are correctly implemented | `pytest tests/unit` |
| Integration | Flask test-client tests: routes that call engine + database | The web layer correctly drives the engine and DB | `pytest tests/integration` |
| Smoke | Fresh clone, documented setup, server boots, both pages render | The application actually starts, from nothing | scripted clone + boot + curl |
| End-to-end | A browser clicking through a real game | A user can do the thing | *deferred to Project 2* — named so you know what you are not claiming |

**Worked example — both paths for one route.** The move route is Stage C's
center, and it needs *two* tests because it makes two promises:

```python
def test_legal_move_advances_board(client):
    resp = client.post("/move", data={"row": 3, "col": 4})
    assert resp.status_code == 200
    assert "3,4" in get_board_state(resp)     # the move landed

def test_occupied_cell_rejected(client):
    client.post("/move", data={"row": 3, "col": 4})
    resp = client.post("/move", data={"row": 3, "col": 4})   # same cell
    assert resp.status_code == 400
    assert "occupied" in resp.get_data(as_text=True).lower()
    # and the board did NOT change, and it is still the same player's turn
```

The second test is the one that finds real bugs, because the failure path is
where agent-written code quietly "simplifies." Recall SPEC clause S-3.3 from
Lecture 07 — *a rejected move changes nothing, including whose turn it is*. That
clause now has a web-layer test enforcing it through a second interface. One
spec, two implementations of its enforcement: this is your first taste of what
Stage D does across languages.

The rule from the case study is "both paths per endpoint" and the honest version
at your scale is *both paths where the failure path carries a promise*. The
leaderboard page's failure path (empty database renders an empty table, not a
crash) carries one. A static "about" page's does not.

## The gate table

Stage C's second deliverable is a file: `GATES.md`. Three rows now — lint,
tests, smoke — each with the exact command and the definition of green. The
full-scale version you are imitating (lost-communities' table) has eight rows —
lint, tests, smoke, both-paths, contract conformance, coverage, review,
live-app — and two design ideas to steal:

**Gates activate progressively.** Each row of the big table has an "active from"
milestone: the both-paths gate switches on when endpoints exist; the live-app
gate when there is an app to drive. A gate that activates too early is noise
(red for structural reasons, teaching everyone to ignore red); too late and the
work it guards is already built wrong. Your version: three gates now, coverage
gate already active since Stage A, more in Project 2.

**Red is mechanical.** The case study's phrasing: *"Verification fails" means
one of these is red, and a red gate returns the work to in-progress — it does
not advance.* No judgment call, no "it's basically fine." This is the pass-4
lesson from Lecture 06 in institutional form: the checks that depend on
remembering to care get skipped, so the checks are named in a file and run as a
unit. In class you will watch a deliberately broken failure path turn a gate
red, and watch the work go *back* — the demo's point is the discipline, not the
bug.

From Stage C on, the brief requires the gate run before every commit, visible in
your history ("gates green" in the message, or committed gate output). It costs
about ninety seconds. Notice, as you pay it, what it buys: every commit on your
main branch now carries the same three claims, mechanically checked — which is
what lets *future you* (and later, teammates and autonomous agents) trust the
branch without re-deriving that trust by hand. That is where this course is
going; Project 2's whole autonomy story stands on gates you are learning to
run this week.

## Flask, sized for this project

For those meeting Flask cold, the whole Stage C shape fits in one paragraph. A
Flask app maps routes to handler functions; handlers call your engine and your
Stage B persistence code, then hand data to a Jinja template that renders HTML.
Use the app-factory pattern (`create_app()`) — it is what makes the test client
clean (each test builds a fresh app against a fresh temp database, exactly like
Lecture 09's fixture). "Light JS" means: clicking a cell posts a move; the
server re-renders. No framework, no build step, no API layer — the testing
story above is the point, and every piece of it runs in pytest.

And the layering rule gets its third enforcement: **the web layer is a caller,
like the CLI.** The handler translates HTTP to engine calls; it contains no
game rules. The mechanical check is brutal and satisfying: at stage end,
`git diff stage-b..HEAD -- game.py` prints *nothing*. An entire user interface
appeared and the engine never noticed. If you find yourself editing `game.py`
to make a page work, stop — you are about to move game logic to the wrong side
of a boundary your spec, your ConOps, and now two interfaces all depend on.

Write the rule down where the sessions that build pages will see it: a
`web/CLAUDE.md` stating the layering rule and this layer's test commands. That
is the per-directory memory layer from the hierarchy — Thursday's lecture
completes that picture.

## Stage C, concretely

From the brief: play + leaderboard pages working from a fresh clone; empty
`game.py` diff; `GATES.md` with visible runs; both-paths test-client tests; the
per-directory CLAUDE.md; and Thursday assigns the cost-hook port. Also due
today: **PKB checkpoint 1** — the mechanics are in the Project 0 spec; the
short version is your bundle, your log, and evidence of weekly tending.

## Questions to think about

1. For each of your Stage C tests, complete the sentence "this test claims
   that..." — then find the claim none of your tests makes. (There is always
   one. The smoke gate exists because "it boots" is usually it.)
2. The demo shows a red gate returning work. What is the *cheapest* moment in
   your week to discover the rejection-path bug: gate-before-commit, grader,
   or week 7's port? Price each one in your own hours.
3. Your `web/CLAUDE.md` will say "no game logic in handlers." Write the one
   sentence that tells a future session how to *check* whether it is about to
   violate that — a rule an agent can apply is worth ten it can admire.
