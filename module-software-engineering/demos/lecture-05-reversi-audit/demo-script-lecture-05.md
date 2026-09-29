# Reversi walkthrough (Lecture 05) — the Project 1 brief, step by step

The demonstration for Lecture 05 is the Project 1 brief
(`../../project-1-reversi-brief.md`) read in order. Step 1 is shown on Reversi
only as far as reading the sketch: the room sorts §4.2 into stated, implied,
and missing, and finds the tension. The rest of step 1 — the prompt, the gap
list, rulings, a deferral, and an amendment proposal — is shown in its form,
on tic-tac-toe, from *Specifying a Game*. The Reversi gap list and its rulings
are the students' work, and nothing from one is shown. Steps 2 to 5 are shown
by opening, at each step, the artifact the finished tic-tac-toe game — the
reference — produced (`../lecture-03-game-demo/reference/`, the `t5` state) at the section the brief
names as the model. Step 6 and the logistics close the hour.

**What is not shown.** No agent output on the Reversi sketch — no gap list, no
ruling, no amendment. You may run the step-1 prompt on a private copy of the
starter to know what students will get back, but it stays on your machine.
`expected-gaps.md` is for your eyes: for answering questions and for feedback.

## What is live and what is from files

| Segment | Step | Live | From files |
|---|---|---|---|
| 1 | — | the recap; a minute of the Reversi demo; the Project 1 summary; the checklist table; the brief's §2 on screen | the demo page, https://ase.santoslab.org/reversi/ |
| 2 | 1 | the sketch; the sorting of §4.2; the tension; the room's own gap list | the step-1 prompt; the tic-tac-toe rulings and deferral (from *Specifying a Game*); the amendment form |
| 3 | 2 | — | `reference/SPECS.md` §4, §5.1, §7.2, §9.5 opened |
| 4 | 3 | the six commands of the five-artifact history | `plans/001` opened |
| 5 | 4 | the gate in `reference/`; the pragma grep | `plans/002` and two tests opened |
| 6 | 5 | — | `fixtures/scenarios.json`, `fixtures/README.md`, `tests/test_fixtures.py`, `plans/003` opened |
| 7 | 6 | — | the brief's checklist on a slide |

## What the starter contains, and what is known about it

The starter (`../../student-materials/reversi-starter/`) has five things:
`CONOPS-sketch.md` — the client's general idea in the concept-of-operations skeleton with
sections 2, 3, and 6 omitted, because there is no existing system; the loader
`CLAUDE.md`; `process/`, the set *Verifying a Game* ended with, identical to the
reference's;
`BACKLOG.md`; and the gate's configuration — `.coveragerc`, `pytest.ini`,
`requirements-dev.txt`, `.gitignore`. No `CONOPS.md`, no `SPECS.md`, no code,
no tests.

The sketch is incomplete on purpose and contains one internal tension. The key,
`expected-gaps.md`, lists 18 decisions the sketch leaves open and 8 more that
surface when `SPECS.md` is derived, with the standard ruling for each and a
mark on the ones that are genuinely the student's. None is ruled in class; the
students find and rule on them. This script is linked from the student notes, so
the standard rulings are kept only in `expected-gaps.md`, which is for your eyes;
have it open for questions. The rows most worth knowing are 1 (the end of the
game), 2 (the opening), 5 (the pass), 6 (the flips), and 7 (legal-move hints).

Item 1 is the one to spend time on, and the only Reversi finding shown in
class. The sketch's two statements — "if you have
no square you can play, you forfeit your turn" and "when the board is full, the
discs are counted" — are each true of Reversi, and together they are incomplete:
if both players are stuck with empty squares left, the sketch says nothing about
what happens. It can happen early: the shortest game that reaches it is a
nine-move wipeout, `d3 c3 b3 d2 e1 d6 d7 e3 f4`, after which every disc is
black and neither player can move with 51 squares empty (the slide shows the
boards). AUD-2 finds it by reading the two bullets side by side. Students who
know Reversi will supply the answer and call it obvious. The reply, once, is:
if the sketch does not say it, it is a gap — record it and rule on it, even
when you know the answer. The brief's convergence rule says how such gaps are
resolved, not that they are skipped.

## Before class — setup checklist

1. A fresh copy of the starter, outside the course repository, with the initial
   commit of the brief's step 0:

   ```sh
   rm -rf ~/reversi-demo
   cp -R <path-to-module>/student-materials/reversi-starter ~/reversi-demo
   cd ~/reversi-demo && git init && git add -A
   git commit -m "project 1 start: conops sketch and process"
   ```

2. Optional, private: run the step-1 prompt in that copy to know what the
   students' lists will look like. Nothing from it is shown in class.
3. `reference/` (`../lecture-03-game-demo/reference/`) open in an editor with
   these bookmarked, in the order they are opened: `CONOPS.md` §4.2 and §5.4;
   `SPECS.md` §4, §5.1, §7.2, §9.5, and the Changelog;
   `plans/001-engine-opponent-cli.md` step 1 and *Verification at the end of
   this build*; `plans/002-test-suite.md` step 1; `tests/test_game.py` at
   `test_make_move_rejected_after_game_over`; `tests/test_main.py` at
   `test_prompt_human_rejects_invalid_forms`; `fixtures/scenarios.json`;
   `fixtures/README.md` *Known blind spots*; `tests/test_fixtures.py`;
   `plans/003-fixture-loader.md` *What this plan does not cover*;
   `.coveragerc`.
4. A virtual environment with `pytest-cov`, and the gate confirmed green in
   `reference/` that day (99 collected). `PYTHONDONTWRITEBYTECODE=1` exported
   in the terminal, so that no `__pycache__` appears in the reference. The six
   commands of Segment 4 in a text file.
5. Two terminals, large font; `expected-gaps.md` printed, for your eyes; the
   brief open at §2 and at §3.1; its required-elements checklist on a slide;
   the Reversi demo page open in a browser — https://ase.santoslab.org/reversi/.
   Confirm before class that it is live (the course site must be published);
   if it is not, show slide 3's screenshot instead.

## Segment 1 — Where we are (about 6 minutes)

No agent. Slides 2–6:

- **The recap** (slide 2): the chain from an idea to a verified program — idea,
  sketch, `CONOPS.md`, `SPECS.md`, plans, code, verified — naming the lecture
  that showed each part.
- **The Reversi demo** (slide 3): a minute of play on the demo page, so that
  the room has seen the game. Say that it has more than Project 1 asks for — a
  clock, hover previews, a browser page; it plays at four strengths (Random,
  Easy, Medium, Hard) or human against human. Students build a text-based game.
- **Project 1** (slide 4): what you get, what you build, that the decisions are
  yours, that the evidence is the history, and the due date.
- **The checklist** (slide 5): each kind, what its audit demands, and how its
  realization is checked. Point at input grammar versus interaction flow: one
  entry versus the sequence.
- **The seven steps** (slide 6): each of steps 1 to 3 opens with an audit of
  the document the step before produced.

**Say:** today reads the brief in order. At each step we open the artifact the
tic-tac-toe reference produced, so that you know what finished looks like before you
start. Nothing in the brief is new; what is new is the game.

## Segment 2 — Step 1: reading the sketch, and the form of the rest (about 12 minutes)

**Do (shell, live):** `cat CONOPS-sketch.md`, or show slide 8's excerpts. Read
§1.2 and §4.2 aloud. **Say:** it comes in our skeleton only so the audit can
point at "§4.2, second bullet"; what makes it a sketch is its state — first
person, unreviewed, TBDs, one tension. Then sort §4.2's policies with the room
(slide 9):

| # | States | Implies | Leaves out |
|---|---|---|---|
| 1 | two colors; players alternate; one disc per turn, on an empty square | an opening position exists — "a few discs already in the middle" (§1.2) | who moves first? which discs, where? |
| 2 | a move must trap at least one disc, in a straight line — across, down, or diagonally | a move can trap in more than one direction — "everything trapped flips" | does every trapped line flip, or one? |
| 3 | a player with no square to play forfeits the turn | the other player moves next | is the forfeit announced? what if both players are stuck? |
| 4 | when the board is full, the discs are counted; more wins | the count is shown at the end (§5.1) | what if the counts are equal? can the game end before the board is full? |

One row per §4.2 bullet.

**Say:** you know the game, so you will fill gaps from memory without
noticing. If the sketch does not say it, it is a gap — record it and rule on
it, even when you know the answer.

Then the tension (slide 10). **Ask:** "Can both players be stuck with squares
still empty? What does the program do?" Let the room find that §4.2's last
bullet and its third bullet do not, together, say. Then show the nine-move
wipeout on the slide: every disc black, 51 squares empty, neither can move.
That is the finding the audit makes first — and the only Reversi finding shown.

**Do:** give the room three minutes to write its own gap list, on paper, from
the sketch alone. Then the prompt (slide 11). **Say:** it is word for word the
prompt *Specifying a Game* typed on tic-tac-toe; it names no game; you type it
on your own starter tonight, and the list you get back will be longer than
yours and ordered differently.

**Show** slide 12 — what rulings and a deferral look like, on tic-tac-toe, from
*Specifying a Game*'s round 1: six in a row (ambiguous, AUD-1), a win on the
last empty square (incomplete, AUD-4), the post-game options stated two ways in
§4.3 and §5.1 (inconsistent, AUD-2), and quitting mid-game deferred to
`BACKLOG.md` (DEV-6). **Say:** each ruling says what was decided and which
document it goes in; a deferral is a decision not to decide yet, recorded where
the next reader finds it — not a guess. On Reversi, the rulings are yours.

**Show** slide 13 — the amendment form: the agent proposes, marks it *awaiting
approval*, and waits; nothing in a governing document changes until you approve
(DEV-3). From there to `CONOPS.md` 1.0 is the rest of step 1.

**Open:** `reference/CONOPS.md` §4.2, then §5.4. **Say:** a policy as a player
observes it; and a scenario for the policy of rejecting an entry — every policy
appears in a scenario (AUDCON-3). **Reversi:** five scenarios at least, because
a pass and an early end are policies tic-tac-toe did not have; and a version, a
status, and a changelog, which the sketch lacks (AUDCON-6). The step ends with
`conops: 0.1 sketch -> 1.0` and the transcript.

**If a student asks for the Reversi answers:** point to the convergence rule —
where the sketch is silent, the client's intent is standard Reversi — and to
the brief's §4 list of decisions. Finding each gap, ruling on it, and stating it
in the right document is the work.

## Segment 3 — Step 2, the reference's `SPECS.md` (about 10 minutes)

**Say:** step 2's prompt is the round-2 prompt *Specifying a Game* typed on
tic-tac-toe, which names no game;
the kinds are pre-picked; the brief's §4 is the floor for the list the agent
returns, and every item gets a ruling. Then, on the slide, what Reversi demands
that tic-tac-toe did not, kind by kind.

**Open:** `SPECS.md` §4. **Say:** rules of play as numbered clauses, so that a
test can cite one (AUD-5). **Reversi:** more clauses, one per rule the
student's rulings settle — which ones is theirs to find.

**Open:** §5.1, `make_move`. **Say:** a precondition, a postcondition, and
behavior outside the precondition, including after the game is over (AUD-12);
the Changelog shows that clause arriving at 1.2.0. **Reversi:** one move
changes many cells — what the postcondition says about them, and what a test of
a move can check, is the student's to decide.

**Open:** §7.2. **Say:** byte-exact, two examples (AUD-9); "looks like the
example" is a finding. **Reversi:** the same, plus the decision whether hints
are shown — the item deferred in Segment 2 lands here.

**Open:** §9.5. **Say:** obligations, not policy; the policy is VER-4 to VER-8
and is not the student's to weaken. **Reversi:** read this list against the
Reversi rules and see how much carries over. The step ends with `specs: 1.0.0`
and the second transcript.

`[fallback capture]` — stills of the four sections.

## Segment 4 — Step 3, a silence through five artifacts (about 12 minutes)

**Say:** the brief's step 3 has three moves in a fixed order — audit `SPECS.md`
itself, plan, build — and the reason for the order is in the reference's
history.

**Do (shell, live), in `reference/`:**

```sh
grep -n 'game is over' SPECS.md
sed -n '/^## Changelog/,$p' SPECS.md | head -5
grep -A2 'make_move(row, col)' plans/001-engine-opponent-cli.md
grep -n 'winner is not None' game.py
grep -A3 'on failure' plans/002-test-suite.md
grep -n 'after_game_over' tests/test_game.py
```

The top changelog entry is `1.2.1`, a §2 housekeeping patch; the two entries
that matter are `1.2.0` and `1.1.0` below it.

**Say:** take the five artifacts in the order they were written. `SPECS.md`
1.1.0 was silent on a move after the game is over: it listed two reasons
`make_move` returns `False` and stopped. The plan's `make_move` step realizes
"each rejection case §5.1 lists" — faithfully, and there were two. The engine
accepted the move, exactly as the plan described. §9.5 at 1.1.0 listed three
failure cases for `make_move`, and plan 002 lists the same three, because it
realizes §9.5 — so no test claimed the missing clause either. Five artifacts,
none at fault, each faithful to the one before it: downstream fidelity cannot
recover information that was never in the specification. Then 1.2.0 records
the ruling, and the engine change and the test citing the new clause follow it
in the history — amendment first, realization after, DEV-2 (c).

**Open:** `plans/001-engine-opponent-cli.md` step 1. **Say:** a clause per
bullet; find the `make_move` bullet. Then *Verification at the end of this
build*: a human plays one game per mode against §8, and the RPT-5 note says so —
there is no suite yet (VER-1).

**Say:** step 3's three prompts, on slide 22. The first audits `SPECS.md`
itself before any plan (DEV-8) — the move that would have caught the silence.
The second asks for the plan and nothing else (DEV-9). The third approves,
commits the plan under `plans/`, builds, reports per RPT-5, commits — and says
nothing about how to build anything, because the plan says that and the plan
cites the contract clause by clause. **Reversi:** the same three prompts, over
the modules the student's `SPECS.md` §2 names.

`[fallback capture]` — the six commands' output.

## Segment 5 — Step 4, the suite as a build, and the gate (about 12 minutes)

**Say:** the process set in the starter is already the set *Verifying a Game* ended with — VER-5 to
VER-8 are in `verification.md` 1.3, and the amendment *Verifying a Game*
performed before writing any test is done for the students; its changelog entry says
why. The suite is a build, so DEV-9 applies: the prompt (on the slide) asks
for a plan that names, per step, the §9 obligations it claims and the clauses
each test cites, and only then the suite.

**Open:** `plans/002-test-suite.md` step 1 beside `SPECS.md` §9.5. **Say:**
check the obligations off against the plan's bullets; this is what "every
obligation claimed" looks like before a test exists.

**Open:** `tests/test_game.py` at `test_make_move_rejected_after_game_over`.
**Say:** the docstring cites the clause; the board is set up by direct
assignment and the behavior goes through `make_move` (VER-6). This is the test
that follows the 1.2.0 amendment in the history.

**Open:** `tests/test_main.py` at `test_prompt_human_rejects_invalid_forms`.
**Say:** one clause, eight rejected forms, parametrized. **Reversi:** one case for
each form the student's grammar rejects — `d9`, `i3`, and whatever else it
rules out (whether `D3` or ` d3 ` is accepted is the student's decision) — in
the order the grammar lists them. An occupied square or one that flips nothing
is well-formed: the rules of play reject it, and its test cites that clause.

**Do (shell, live), in `reference/`:**

```sh
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100
grep -n 'pragma' *.py
```

**Expected:** 99 passed, 100% branch, exit 0; one pragma, on `main.py`'s
`__main__` guard (VER-5).

**Say:** RPT-5 carries two coverage lines — the gate's branch figure, and
which §9 obligations are claimed by at least one test (VER-8). They answer
different questions, and *Verifying a Game*'s three sabotage steps showed a case where
each was informative and the other was not. Then DEV-2's three kinds of
change, and the standing rule from step 3 on: a change of specified behavior
commits its amendment first.

**Open:** `.coveragerc`. **Say:** this one names its modules; the starter's
follows the same policy with `source = .`, so it measures every module in the
root whatever the split;
neither it nor `pytest.ini` is edited to weaken the gate.

`[fallback capture]` — the gate's output.

## Segment 6 — Step 5, the file first, then the loader (about 10 minutes)

**Open:** `fixtures/scenarios.json` beside the brief's §3.1. **Say:** a
scenario's name cites the clause it exercises — `x-wins-row-overline` is §4.1
as moves. **Reversi:** §3.3's eight kinds; the pass and early-end scenarios are
hard to construct by hand — generated with the engine if need be, verified
against the specification on paper, and the report says how. An engine is not
the oracle for its own fixtures.

**Open:** `fixtures/README.md` *Known blind spots*. **Say:** a blind spot
declared is part of the contract (VER-7); the file states what it assumes and
what it does not cover.

**Open:** `tests/test_fixtures.py`. **Say:** two parametrized functions and no
expectations of their own; the expectations live in the file, and the file is
never edited to make a test pass.

**Open:** `plans/003-fixture-loader.md` *What this plan does not cover*.
**Say:** the file was installed as given and the loader was built for it — two
halves, and the file's commit comes first. **Reversi:** three commits — the
file and its README, the loader's plan, the loader.

`[fallback capture]` — stills.

## Segment 7 — Step 6, the checklist, and logistics (about 10 minutes)

No agent. `PROJECT-1-REPORT.md`'s four items: the amendment implementation
forced, one of them traced through five artifacts in the form of Segment 4;
what 100% branch coverage did not tell you; how the pass and early-end fixtures
were constructed and checked; what remains for a human or agent verifier. Then
the brief's required-elements checklist on the slide, each item tagged with its
step.

- The `process/` set is adopted, not authored. It is the set *Verifying a Game* ended with; a rule
  changes only by an amendment with a changelog entry (DEV-3), and a change
  that weakens a rule is returned. The gate's configuration is adopted the same
  way.
- `d3` notation: the sketch says squares are named "like `d3` on a
  chessboard"; whether `D3` and ` d3 ` are accepted, and where the letter
  becomes an index, are the student's decisions — stated as a grammar
  (AUD-10) and placed inside the engine (AUD-12).
- Due Thursday, October 8, 11:55 pm; Project 0 is still due Thursday, October 1. Start with step 0 tonight.
  Where to ask.

## End

Nothing from a Reversi gap list was shown. If you ran the step-1 prompt on a
private copy, it stays there; students start from the starter.

## Recreating this yourself (students)

This is the brief. Run it in order in your own copy of the starter, beginning
tonight with step 0 and then the audit of your own starter. Rule on every item
yourself — the brief's §4 is your checklist; the instructor key is for feedback,
and reading it first defeats step 1.
