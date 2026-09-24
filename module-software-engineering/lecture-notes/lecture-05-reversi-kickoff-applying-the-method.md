# Lecture 05 — Reversi Kickoff: Applying the Method

> Software-engineering module, meeting 5 of 6. Companion reading for the lecture
> and for the Lecture 05 walkthrough
> (`../demos/lecture-05-reversi-audit/demo-script-lecture-05.md`);
> self-contained. Launches Project 1, Phase 1 (`../project-1-reversi-brief.md`).
> The readings for Lecture 06 are at the end.

## Where we are: one method, six steps

Four lectures have built one method and applied it to two examples. Lecture 01
introduced specifications and their realizations, conformance, and the three
kinds of verifier (human, agent, algorithmic). Lecture 02 introduced the
concept of operations, operations with preconditions and postconditions, and
the idea that conformance is an invariant we maintain while the system
changes. Lecture 03 showed that a program needs a family of specifications —
several kinds, each fixing what the others leave open — and that an agent
helps us discover them by audit. Lecture 04 showed that a test suite is a
specification a program can check, and that coverage tells us which code the
suite reaches, not whether its claims are right.

Every move in those lectures is a rule in `process/`, and the rules are the
same for a note set, for tic-tac-toe, and for the game you receive today.
Recall the specification-family table of Lecture 03. With the audit rule that
checks each kind and the verifier that checks its realization, it becomes the
checklist for Project 1:

| Kind | Audited by | Verified by |
|---|---|---|
| concept of operations | AUDCON-1 to AUDCON-8 | a person playing each scenario — validation |
| rules of play | AUD-8 | unit tests; fixtures |
| display format | AUD-9 | golden-string tests |
| input grammar | AUD-10 | scripted-input rejection tests |
| interaction flow | AUD-11 | scripted-input tests |
| interface contract | AUD-12 | unit tests; a type checker where used |
| example session | AUD-13 | an end-to-end scripted run |
| verification obligations | AUD-14 | reading the suite against §9 (VER-8) |

The course's catalog of specification kinds (`../../specification-kinds.md`)
gives these columns for every kind the course uses, including the test suite
and the fixtures that steps 4 and 5 add. The brief's §4 is organized by these
kinds. Two of its names are not kinds: *computer opponent* is a subject that
spans three of them — an actor in the concept of operations, a section of the
interface contract, and a verification obligation — and *initial state*, in
the comparison table below, is a clause of the rules of play (AUD-8).

The brief's §2 is the method as seven steps, in the order the demo
repository's tags follow, and this lecture reads them in that order. At each
step it opens the artifact the reference game produced — the `t5` state,
`../demos/lecture-03-game-demo/reference/` — so that you know what finished
looks like before you start.

| Tag | Step | Produces | Ends with |
|---|---|---|---|
| `t0` | 0 — start | the starter, committed | `phase 1 start: conops sketch and process` |
| `t1` | 1 — the sketch to a concept of operations | `CONOPS.md` 1.0; the elicitation transcript | `conops: 0.1 sketch -> 1.0` |
| `t2` | 2 — the concept of operations to the specification family | `SPECS.md` 1.0.0; the second transcript | `specs: 1.0.0` |
| `t3` | 3 — audit, plan, build | `plans/001-…`; the engine, the opponent, the entry point | `plan: engine, opponent, CLI (DEV-9)`; `engine: …` |
| `t4` | 4 — the suite as a build; the gate | `plans/002-…`; `tests/`; the gate green | `plan: test suite per SPECS 9 (DEV-9)`; `tests: …` |
| `t5` | 5 — fixtures: the file, then the loader | `fixtures/`; `plans/003-…`; the loader | `fixtures: scenarios.json and README (VER-7)`; `plan: fixture loader (DEV-9)`; `fixtures: loader (VER-7)` |
| — | 6 — close | `PHASE-1-REPORT.md`; the `CLAUDE.md` commands | `phase 1: report` |

Step 0 is not a lecture topic. It is a copy of the starter, a `git init`, a
virtual environment, one commit, and a reading of every governing and process
document in full — DEV-1 applies to you as well as to the agent. Do it
tonight. Notice, when you read `process/verification.md`, that it is at
version 1.3 with VER-5 through VER-8 already in it: the amendment Lecture 04
performed before writing any test has been applied for you.

## Step 1 — the sketch to a concept of operations

### Learning Reversi from its concept of operations sketch

We asked you to read the Reversi sketch as a player, and not to read the rules
of Reversi anywhere else. That was not a restriction for its own sake. Reading
a concept of operations to learn what a system does is the activity Lecture 02
called *validation*: a reader asks whether the document describes the system
that was wanted, and finds out where it does not. A reader who already knows
the answers cannot do that, because they fill the gaps without noticing them.

Section 1.2 of the sketch gives the game in a paragraph: an 8-by-8 board;
discs that are dark on one side and light on the other; a move places a disc
so that one or more of the opponent's discs are trapped in a straight line
between the new disc and one already on the board, and the trapped discs
flip; the aim is to have more discs at the end. Section 4.2 gives the rules a
player would see. Here they are, sorted into what the sketch states, what it
implies, and what it leaves out:

| Stated | Implied | Missing |
|---|---|---|
| two colors; players alternate; one disc per turn | an opening position exists — "a few discs already in the middle" | who moves first |
| a move must trap at least one disc, in a straight line, across, down, or diagonally | a move can trap in more than one direction — "everything trapped flips" | what happens after a forfeit: whose turn, whether it is announced, what if both players are stuck |
| a player with no square to play forfeits the turn | the count is shown at the end (§5.1) | equal counts |
| when the board is full the discs are counted, and more wins | | taking a move back — §7 says no, under Limitations, which is the wrong section (AUDCON-8) |

One item in the table is more than a gap. The sketch says the game ends when
the board is full, and it says a player with no move forfeits the turn. Each
statement is true of Reversi. Together they are incomplete: if both players
are stuck with empty squares left, the sketch does not say what happens, and a
program built from it would either loop forever or invent an answer. Our audit
rule AUD-2 (is the document consistent with itself?) finds it by reading the
two bullets side by side. Note that this is the same kind of finding as
Lecture 03's post-game options, which were stated two different ways in two
sections, and it is the reason our development rule DEV-8 requires the audit
before anything is planned.

**Important**: students who already know Reversi will supply the missing rule
and call it obvious. In this method, a rule the sketch does not state is a
finding, whatever the reader happens to know. The convergence rule (below)
says how such findings are resolved; it does not say they can be skipped.

### The audit, watched

Step 1 of the brief begins with the audit of the sketch, and the demonstration
shows that audit performed on the starter you have — from captures taken at
rehearsal — and then stops. The prompt is the one Lecture 03 typed on its own
sketch, and the one the brief prints for step 1:

> Read `CONOPS-sketch.md` and the process documents. I want a `CONOPS.md` 1.0
> that realizes this sketch as a full-skeleton concept of operations. Before
> proposing anything, run the audits in `process/conops-audit.md` and
> `process/spec-audit.md` on the sketch (DEV-8) and report the gap list per
> RPT-1 — numbered, each with your recommended resolution. Then stop and wait
> for my rulings.

The list comes back longer than the one you wrote in three minutes, in a
different order, with some items you found and it did not. We rule on four in
class, and the rulings are standard Reversi:

- **The end of the game.** The game ends when neither player has a legal move;
  a full board is one case of that. Ruled into §4.2, replacing the last
  bullet. This is the item the tension pointed at.
- **The opening.** Four discs: d4 and e5 light, d5 and e4 dark. The sketch
  implied a position and never gave it (AUD-4, completeness); the rules of
  play will have to state the initial state exactly (AUD-8).
- **The pass.** A player with no legal move passes; the pass is forced, never
  chosen; it is announced; the opponent moves; two consecutive passes end the
  game — which is the end condition again, seen from the side of the pass
  rule. The sketch said "forfeit" and stopped (AUD-4). Also, our audit rule
  AUDCON-3 requires every mode and policy to appear in a scenario, and there
  is no scenario with a pass.
- **The flips.** Every flanked run in every direction flips, in all eight
  directions, when a single move flanks in several. The sketch's "everything
  trapped flips" is ambiguous between one line and all of them (AUD-1).

All four are things a player observes, so all four go into the concept of
operations (AUDCON-2). One item is deferred on purpose: whether the program
shows the legal moves. The client flagged it as undecided; the concept of
operations does not need it settled in order to describe the game; the display
format will settle it when `SPECS.md` is derived. Following our development
rule DEV-6, it is written to `BACKLOG.md` with the question, where it arose,
and the options. Note that a deferral is a decision not to decide yet,
recorded where the next reader will find it — it is not a guess.

One ruling is then carried to the amendment form: the end condition, proposed
per our reporting rule RPT-3 — the document, the clause, the old text, the new
text, the rationale citing the gap-list item, the version bump, the changelog
entry — and marked *awaiting approval*. Nothing further is approved. From that
point to `CONOPS.md` 1.0 — the remaining rulings, the amendments, the rewrite
in the third person, five scenarios, the glossary, the audit run again — is
the rest of step 1, and the brief's step 1 lists what the audit must find in
this sketch and what the rewrite must fix. You have now seen the exact first
move of step 1 performed on your own starter.

### What the reference's concept of operations shows

The brief names `reference/CONOPS.md` as the model for step 1, and three
things in it are worth reading before you write yours. Its §4.2 is the rules
of tic-tac-toe as a player observes them — a policy is a sentence about what
the player sees happen, never about how the program does it (AUDCON-1,
AUDCON-2). Its §5 has one scenario per mode and per policy: solo play to a
win, a two-player game, a tie, and recovery from an invalid entry. AUDCON-3
requires that every mode and every policy appear in a scenario, and for
Reversi that means five scenarios at least, because a pass and a game that
ends before the board is full are policies tic-tac-toe did not have. And the
document carries a version, a status, and a changelog (AUDCON-6); the sketch
carries none, which is itself a finding. Step 1 ends with
`conops: 0.1 sketch -> 1.0` and the export of the session to
`transcripts/01-conops-elicitation.md`. The gap list, your rulings, and the
amendments are the evidence that the document was elicited, not typed.

### The convergence rule: where the sketch is silent

The brief states the rule in one paragraph, and it decides how every gap in
your list is resolved. **Where the sketch is silent, the client's intent is
standard Reversi**: 8-by-8; the standard opening; dark moves first; a move
must flip at least one disc; a player with no legal move passes; the game ends
when neither player can move; more discs wins; equal counts tie.

This does not let you skip a question. A specification that leaves a standard
rule implicit fails the completeness check (AUD-4); the job is to find every
place the sketch leaves a decision open, record the ruling, and state it in
the right document. The rule exists so that engines built by different
students converge — the port stage later in the course runs one shared fixture
file against every engine — while the elicitation stays real.

The rulings that are genuinely yours are listed in the brief's §4: the glyphs
for the two colors and for an empty square; whether and how legal-move hints
are shown; whether the count is shown during play; the notation's edge cases
(case, whitespace, `d9`, `i3`); the post-game options; in solo play, which
color you have and whether it alternates on a rematch; the error wording; the
shape of the interface; the module split. These are graded on three things:
the ruling is recorded, it is applied consistently, and it is stated in the
right document — the concept of operations for what a player observes,
`SPECS.md` for the rest. Which way you decided is not graded.

## Step 2 — the concept of operations to the specification family

Step 2 is the same moves with a new target, and its prompt is Lecture 03's
round-2 prompt, which names no game:

> Read `CONOPS.md` and the process documents. Derive `SPECS.md` 1.0.0 from it:
> one section per kind — board and coordinates; rules of play; display format,
> byte-exact; input grammar; interaction flow; interface contract with
> preconditions and postconditions; an example session; verification
> obligations. Before writing, run the audit (DEV-8) and list every decision
> the concept of operations leaves open, grouped by the kind of specification
> that must settle it, per RPT-1 with a recommendation each. Wait for my
> rulings.

The kinds and their order are pre-picked, as they were in the demo, so that
every submission has the same shape; the course catalog is the menu they were
picked from. The list the agent returns will be long — the brief's §4 is the
floor for what it must contain — and every item gets a ruling. One item that
is not a decision: the coverage policy. It is already in
`process/verification.md`, and §9 of your `SPECS.md` lists obligations — what
the tests must claim, traced to the clauses they verify (AUD-14) — not policy.

### What Reversi demands that tic-tac-toe did not

The game has the same shape as tic-tac-toe — a grid, two players, an ASCII
board, moves, a terminal condition — and every kind of specification gets
harder in a way that shows what that kind is for:

| Kind | Tic-tac-toe had | Reversi forces |
|---|---|---|
| rules of play | one cell written; a win is a line that exists | a legal move flanks at least one disc in at least one of eight directions; a move changes many cells; a pass when there is no legal move; the game ends when neither side can move; the winner by count; ties are realistic |
| initial state | an empty board | the four-disc opening — a completeness trap |
| display format | the grid, `.` for empty | the same grid, plus a real decision: hints, and when |
| input grammar | `[1-9][1-9]` | `[a-h][1-8]` — a letter-to-index mapping; is `A3` accepted? |
| interface contract | `make_move → bool` | a legality query at the center; a move's postcondition names the flipped set; game-over and the count exposed; a disc-count invariant — dark plus light plus empty is 64 |
| verification obligations | §9 | the same categories, on a harder engine; the policy in `process/verification.md` unchanged |
| computer opponent | a random legal move | the same; "most flips" is the natural next strategy |
| fixtures | moves to an expected winner | moves to expected flips and a count; a scenario with a pass; a game that ends before the board is full |

The pass is the seeded gap: the sketch says "forfeits the turn" and the
elicitation must find its consequences. The interface contract is where the
difference is largest. In tic-tac-toe a move's postcondition was one cell; in
Reversi it is a set of cells, and a test of a move has to claim the set.

### What the reference's specification shows

Four sections of `reference/SPECS.md`, one point each:

- **§4, the win condition.** Rules of play as numbered clauses — §4.1, §4.2,
  §4.3 — so that a test can cite one (AUD-5). Your rules of play will have
  more clauses: the opening, the legal move, the flips in every direction, the
  pass, the end, the count.
- **§5.1, `make_move`.** An operation with a precondition, a postcondition,
  and behavior outside the precondition — including, since version 1.2.0,
  after the game is over (AUD-12). Its postcondition changes one cell. Yours
  names the set of discs that flip, and a test of a move claims that set.
- **§7.2, the board format.** Byte-exact, with an empty board and a mid-game
  board as examples (AUD-9). "Looks like the example" is a finding. Yours adds
  the decision the audit deferred: whether hints are shown, and how.
- **§9.5, the required coverage categories.** Obligations, not policy. The
  policy — the target, the pragma, citation discipline, fixtures — is in
  `process/verification.md` and is not yours to weaken. Read §9.5 against the
  Reversi rules and notice how much carries over; that is the point.

Step 2 ends with `specs: 1.0.0` and a second transcript,
`transcripts/02-specs-elicitation.md`.

## Step 3 — audit, plan, build

### A silence through five artifacts

The brief's step 3 has three moves in a fixed order: audit `SPECS.md` itself,
then plan, then build. The reason for the order is in the reference's
history, and Lecture 04 read it. The reference's `SPECS.md` 1.1.0 was silent
on what happens when a move arrives after the game is over: it listed two
reasons `make_move` returns `False` and stopped there. The engine plan came
next, and its `make_move` step says it realizes "each rejection case §5.1
lists" — which it does, faithfully, and there were two. The plan did not
introduce the gap, and no amount of care in writing the plan could have
closed it, because the plan's job is to realize the specification and the
specification did not say. The engine accepted the move, exactly as the plan
described. The suite could not catch it either: §9.5, the section that says
what the tests must claim, listed three failure cases for `make_move` at
1.1.0, and the test plan lists the same three, because it realizes §9.5. So no
test claimed the missing clause.

Five artifacts in a row — specification, engine plan, engine, verification
obligations, test plan — and not one of them at fault. Each faithfully
realizes the one before it, and that is exactly the problem: downstream
fidelity cannot recover information that was never in the specification.
That is why the audit (DEV-8) runs against the specification before any plan
is written, and not after the code exists. Then 1.2.0 records the ruling, and
the engine change and the test citing the new clause follow it in the
history — amendment first, realization after, which is DEV-2 (c). In the demo
you will see the six commands that read this history off the reference; your
report will contain one trace of the same shape through your own artifacts.

The first move of step 3, then, is the audit that would have caught the
silence: `process/spec-audit.md` run on `SPECS.md` itself — AUD-1 to AUD-7,
and AUD-8 to AUD-14 section by section — before any plan exists. If it finds
gaps, you rule, the amendment is committed, and the audit runs again.

### The two prompts, and the plan as an artifact

Lecture 03 showed that the build is asked for in two prompts. The first asks
for the plan and nothing else:

> Read `SPECS.md` and the process documents. Propose a plan for the engine, the
> computer opponent, and the command-line interface — the modules `SPECS.md` §2
> names — citing for each step the clauses it realizes, and wait for my
> approval.

You read the plan and rule on it. Only then does the second prompt ask for the
build:

> Approve the plan. Commit it under `plans/` as
> `plan: engine, opponent, CLI (DEV-9)`. Then build the modules per the approved
> plan, report per RPT-5 with the clauses each module realizes, and commit as
> `engine: game, opponent, and CLI per SPECS 1.0.0`.

Two things about the second prompt. The plan is committed before the first
implementing commit, which is what DEV-9 requires: an approved plan is an
artifact of the repository, readable later by anyone asking why the code has
the shape it has, not an exchange that disappears with the session. And the
prompt says nothing about how to build anything — no module structure, no
algorithm, no naming. The plan says that, and the plan cites the contract
clause by clause; anything added here would be a fourth source of truth
competing with three that are already written down.

The model is `reference/plans/001-engine-opponent-cli.md`. Its step 1 cites a
clause per bullet; its preface says that where the contract does not say, the
plan does not say either, and a question it cannot settle from the contract
goes to `BACKLOG.md`; and its closing section, *Verification at the end of
this build*, names the only verifier available before a suite exists — a
person playing one game in each mode against §8 — and the RPT-5 note says so
(VER-1). The module split is yours if your `SPECS.md` §2 says so; the
reference's — a pure engine with no input or output, the strategies as static
methods, all input and output in the entry point — is the default.

## Step 4 — the test suite as a build, and the gate

The process set in your starter is already the Lecture 04 set. VER-5 through
VER-8 are in `process/verification.md` 1.3, and RPT-5 at 1.3 reports clause
coverage: the amendment Lecture 04 performed before writing any test — for
the same reason a specification precedes its realization — has been applied
for you, and its changelog entry says so.

The suite is a build, so DEV-9 applies to it. The prompt is the one Lecture 04
used, and it names no game:

> Read `SPECS.md` and the process documents. Propose a plan for the test suite
> under `tests/`, one file per source module, that claims every obligation in
> `SPECS.md` §9: for each step, the obligations it claims and the clauses each
> test will cite (VER-6). Wait for my approval. Then commit the plan under
> `plans/` as `plan: test suite per SPECS 9 (DEV-9)`, write the suite, run the
> gate (VER-4), and report per RPT-5, including which obligations are claimed
> by at least one test and which are not (VER-8). Commit the suite as
> `tests: suite per SPECS 9 (VER-4 green)`.

The model plan is `reference/plans/002-test-suite.md`. Its step 0 is the
harness — `tests/__init__.py` and a `tests/conftest.py` that puts the
repository root on `sys.path`; yours is smaller only in that `pytest.ini` and
`requirements-dev.txt` are shipped in the starter — and its step 1 reads beside
`SPECS.md` §9.5: the
obligations can be checked off against the plan's bullets before a single
test exists, which is what "every obligation claimed by at least one test"
looks like in advance.

Two tests of the reference are worth reading for their form. In
`tests/test_game.py`, `test_make_move_rejected_after_game_over` carries the
docstring "SPECS §5.1: a move after the game is over returns False and changes
nothing." The board is set up by direct assignment, and the behavior under
test goes through `make_move`; that is VER-6's discipline — setup by
assignment, behavior through the public operation. It is also the test that
follows the 1.2.0 amendment in the history. In `tests/test_main.py`,
`test_prompt_human_rejects_invalid_forms` carries "SPECS §6.2: every invalid
move form is rejected and re-prompted" and is parametrized over the eight
forms §6.2 lists: one clause, many realizations, one test. Yours enumerates
the forms your grammar rejects — `D3`, ` d3 `, `d9`, `i3`, `d`, `dd3`, an
occupied square, a square that flips nothing — in the order your grammar lists
them.

The gate is the command in your `CLAUDE.md`:

```sh
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100
```

It must exit 0 (VER-4), and the only `# pragma: no cover` in the repository is
on the entry point's `if __name__ == "__main__":` guard (VER-5). The starter
ships the gate's configuration — `.coveragerc` measures every module in the
repository root, whatever your module split, and excludes the tests and the
virtual environment — and neither it nor `pytest.ini` is edited to weaken the
gate. The completion note carries two coverage lines, and they answer
different questions: the gate's line reports branch coverage, a property of
the pair (tests, code); the clause-coverage line reports which of §9's
obligations are claimed by at least one test, a property of the pair (tests,
specification). That is VER-8, and Lecture 04's three sabotage steps showed a
case where each line was informative and the other was not. The brief
recommends, without requiring, that you perform the first of those steps on
your own suite — delete one test that is the only claimant of a clause, run
the gate, watch it stay green, restore the test — and write the verdict in
the lecture's form. It is the shortest route to the second item of your
report.

### Three kinds of change, and the amendment first

From step 3 on, every commit touches a realization, and every such commit is
one of the three kinds DEV-2 names; the history has to show which. A
**repair** (a) follows a report and a ruling, and the specification does not
change. A **conformance-preserving change** (b) changes nothing specified, and
the commit message says so. A **change of specified behavior** (c) commits its
amendment first. Implementation will find something your specification did not
settle — what a move returns after the game is over, what happens when both
players pass, whether an entry with trailing whitespace is accepted — and at
least one such amendment is expected in Phase 1. The amendment (RPT-3;
approved, DEV-3; version bump and changelog entry) is committed before the
code that depends on the ruling, and the audit runs again on the amended
document (DEV-8). A question you cannot settle goes to `BACKLOG.md` (DEV-6).

## Step 5 — fixtures: the file first, then its loader

The fixture shape is fixed by the brief's §3.1 so that the same file can later
run against an engine in another language: squares in the notation your
grammar defines; the literal `"pass"` for a forced pass; colors named `dark`
and `light` regardless of the glyphs your display uses; and, for each move,
the set of squares it flips.

```json
{
  "name": "dark-opens-d3",
  "moves": ["d3"],
  "flips": [["d4"]],
  "expected": {"to_move": "light", "dark": 4, "light": 1, "over": false}
}
```

Step 5 has two halves, and the order is the point. The **file** comes first:
`fixtures/scenarios.json` with at least the eight kinds of scenario the
brief's §3.3 lists — an opening move with its flips; a move that flips in more
than one direction; a rejected move that flips nothing; a rejected entry that
is not a square; a scenario containing a pass; a game that ends before the
board is full; a full-board game with its final count; a tie — and
`fixtures/README.md` with the three sections the reference's has: the rules
the fixtures assume, citing your clauses; the loader contract; the known blind
spots. Every expectation is checked against your `SPECS.md` by hand. The pass
and early-end scenarios are hard to construct by hand. You may generate them
with your engine, but you must verify them against your specification on
paper before trusting them, and say how in the report. Recall from Lecture 04
why: an engine cannot be the oracle for its own fixtures. The file is
committed before any loader exists.

The **loader** comes second, and it is a build: a plan under `plans/`, your
approval, `tests/test_fixtures.py`, the gate, the RPT-5 note, the commit. In
the reference, `tests/test_fixtures.py` is two parametrized functions —
`test_game_scenario` and `test_rejection_scenario` — holding no expectations of
their own; the expectations live in the file. A scenario that fails is a
finding about the pair (fixture, specification): an RPT-1 gap and a DEV-4
ruling, never an edit to make it pass (VER-7). A ruling may change the file;
if it does, the README says why.

Read three things in the reference. A scenario's name cites the clause it
exercises — `x-wins-row-overline` is §4.1 as moves. `fixtures/README.md`'s
*Known blind spots* declares what the file does not cover, and a blind spot
declared is part of the contract, not a defect. `plans/003-fixture-loader.md`
separates the file, installed as given, from the loader built for it, and its
*What this plan does not cover* says so. Your step 5 ends in three commits:
`fixtures: scenarios.json and README (VER-7)`, then
`plan: fixture loader (DEV-9)`, then `fixtures: loader (VER-7)`.

## Step 6 — the report, and what the checklist asks

`PHASE-1-REPORT.md` is one page with four items. First, the amendment or
amendments implementation forced, and for one of them the trace in the form
of the five artifacts above: the clause as it stood, the plan step that
realized it, the code, the §9 obligation, the test plan or the test — and, at
each artifact, whether the silence was still there — with the step of the
brief, and the rule, under which your process caught it. Second, one thing
100% branch coverage did not tell you about conformance (VER-8). Third, how
the pass and early-end fixtures were constructed and checked by hand. Fourth,
what remains for a human or an agent verifier: the judgment clauses of your
specification (VER-2), and anything you could not verify by reading. The
report's ancestor is RPT-5; the reference has no report, and this one is
yours. Then `CLAUDE.md`'s Commands section is updated — "once it exists" goes;
your entry point is named if it is not `main.py` — and `BACKLOG.md` is brought
current.

Nothing in the brief's checklist is new. Each required element is a rule you
have watched applied, and the table says where.

| Required element | Step | Rule | Where it was shown |
|---|---|---|---|
| the starter as shipped in the initial commit; `CLAUDE.md` and `process/` unchanged except the Commands section and recorded amendments | 0 | DEV-1, DEV-3 | Lecture 04 |
| `CONOPS.md` 1.0 — version, status, changelog; third person; implementation-free; kept sections filled; five scenarios; glossary | 1 | AUDCON-1 to AUDCON-8 | Lectures 02 and 03 |
| `SPECS.md` 1.0.0 or later — eight sections, every clause numbered, examples byte-exact, §9 as obligations traced to clauses; changelog | 2 | AUD-5, AUD-8 to AUD-14 | Lecture 03 |
| every decision in the brief's §4 stated in one of the two documents | 1–2 | AUD-4 | Lecture 03 |
| `transcripts/01-conops-elicitation.md` and `transcripts/02-specs-elicitation.md` — two RPT-1 lists, the rulings, the RPT-3 amendments | 1–2 | RPT-1, RPT-3, DEV-4 | Lectures 01 to 03 |
| history: `conops:` before any `SPECS.md` work; `specs: 1.0.0` before any plan; every plan before its build | 1–3 | DEV-2, DEV-7, DEV-9 | Lecture 03 |
| `plans/001-…` approved; engine, opponent, and CLI per `SPECS.md`; the game runs | 3 | DEV-9 | Lecture 03 |
| `plans/002-…` approved; every test cites its clause; every §9 obligation claimed; the gate green at 100% branch with the single pragma; RPT-5's two coverage lines | 4 | VER-4, VER-5, VER-6, VER-8 | Lecture 04 |
| `fixtures/scenarios.json` in the §3.1 shape with the eight kinds, and `fixtures/README.md`, committed before `plans/003-…` and the loader | 5 | VER-7 | Lecture 04 |
| at least one amendment committed before the code that depends on it; every realization commit identifiable as (a), (b), or (c); `BACKLOG.md` current | 3–5 | DEV-2, DEV-3, DEV-6 | Lecture 04 |
| `PHASE-1-REPORT.md` — the four items, one five-artifact trace | 6 | VER-8, VER-2, RPT-5 | Lecture 04 |
| `CLAUDE.md` Commands say how to run the game and the tests | 6 | — | — |

## Logistics

- **The process set is adopted, not authored.** `process/` in your starter is
  the Lecture 04 set, identical to the reference's. A rule changes only by an
  amendment with a changelog entry (DEV-3). A change that weakens a rule —
  the coverage target, the pragma policy, the fixture rule — is returned. The
  gate's configuration — `.coveragerc`, `pytest.ini`, `requirements-dev.txt` —
  is adopted the same way; it measures every module in the repository root,
  so your module split needs no change to it.
- **Notation.** The sketch names squares "like `d3` on a chessboard." Whether
  `D3` and ` d3 ` are accepted, and what `d9` produces, are yours to decide and
  must be stated as a grammar (AUD-10). Where the letter becomes an index is an
  interface decision (AUD-12); the demo's lesson is that the translation lives
  inside the engine and never escapes it.
- **Effort and dates** are in the brief. Phase 1 is due one week from today.
  Lecture 06 is about MCP and launches nothing new; it previews Stage E, an
  MCP server over the engine you are building.
- **Where to ask.** A question the repository can answer is answered by
  reading it (our development rule DEV-10). A question it cannot answer goes
  to `BACKLOG.md` or to the course channel — and a question about the rules of
  Reversi is answered by the convergence rule.

## Questions to think about

1. The sketch says the game ends when the board is full, and that a player
   with no move forfeits the turn. Neither statement is wrong. One is
   incomplete. Which, and how do you know from the document alone?
2. Which rulings in your gap list are yours to make, and which are the
   client's? Where does the brief draw that line, and why there rather than
   somewhere else?
3. Step 5 requires a scenario containing a pass. Before you trust a scenario
   your own engine generated, what do you check it against, and how — and what
   does VER-7 say about the fixture file afterwards?
4. The after-game-over silence passed through five artifacts of the reference.
   At which step of the brief, and under which rule, would your Phase 1 have
   caught it?

## Before next meeting

- Project 1, Phase 1 is launched today: `../project-1-reversi-brief.md`, §2.
  Start with step 0 tonight, and then step 1 — the audit you watched — in your
  own copy of `../student-materials/reversi-starter/`.
- Read the Model Context Protocol documentation's core concepts and the
  FastMCP quickstart, and the dice-server README in the project unit
  (`../../weeks-04-07/student-materials/mcp-example/README.md`). Lecture 06 asks
  what changes when the reader of a specification is a machine.
