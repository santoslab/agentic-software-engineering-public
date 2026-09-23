# Lecture 05 — Reversi Kickoff: Applying the Method

> Software-engineering module, meeting 5 of 6. Companion reading for the lecture
> and for the Reversi audit walkthrough
> (`../demos/lecture-05-reversi-audit/demo-script-lecture-05.md`);
> self-contained. Launches Project 1, Part 1 (`../project-1-reversi-brief.md`).
> The readings for Lecture 06 are at the end.

## Where we are: one method, applied twice

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
gives these columns for every kind the course uses, including the fixtures and
the test suite that Part 2 adds. The brief's §4 is organized by these kinds.
Two of its names are not kinds: *computer opponent* is a subject that spans
three of them — an actor in the concept of operations, a section of the
interface contract, and a verification obligation — and *initial state*, in
the comparison table below, is a clause of the rules of play (AUD-8).

This lecture is deliberately lighter than the last two. If either of them ran
long, we pick up first whatever was dropped: the chain of identifiers from
"five or more" to the overline fixture; the three kinds of change to a
realization (DEV-2); the fixture loader run.

## Learning Reversi from its concept of operations sketch

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

## Watching the first move of Part 1: the audit of the sketch

The demo performs the first move of Part 1 on the starter you have, and then
stops. The prompt is the one Lecture 03 used, on a different sketch:

> Read `CONOPS-sketch.md` and the process documents. Before proposing anything,
> run the audits in `process/conops-audit.md` and `process/spec-audit.md` on the
> sketch (DEV-8) and report the gap list per RPT-1 — numbered, each with your
> recommended resolution. Then stop and wait for my rulings.

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
Part 1, step 1 of the brief. You have now seen the exact first move of Part 1
performed on your own starter.

## The convergence rule: where the sketch is silent

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

## What Reversi demands that tic-tac-toe did not

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

## The Project 1 deliverables, and the rule behind each

Nothing in the brief's two checklists is new. Each required element is a rule
you have watched applied, and the tables below say where.

**Part 1, assigned today.**

| Required element | Rule | Where it was shown |
|---|---|---|
| `CONOPS.md` 1.0 — third person, implementation-free, kept sections filled, five scenarios, glossary, changelog | AUDCON-1 to AUDCON-8 | Lectures 02 and 03 |
| `SPECS.md` 1.0.0 — eight sections, every clause numbered, examples byte-exact, §9 as obligations | AUD-5, AUD-8 to AUD-14 | Lecture 03 |
| every decision in the brief's §4 stated in one of the two documents | AUD-4 | Lecture 03 |
| `transcripts/part-1-elicitation.md` with two RPT-1 lists, the rulings, the RPT-3 amendments | RPT-1, RPT-3, DEV-4 | Lectures 01 to 03 |
| `CLAUDE.md` and `process/` as shipped, or amended only with a changelog entry | DEV-3 | Lecture 04 |
| the concept of operations committed before the `SPECS.md` work begins | DEV-2, DEV-7 | Lecture 03 |

**Part 2, assigned at Lecture 06.**

| Required element | Rule | Where it was shown |
|---|---|---|
| the approved plan under `plans/` before the implementing commits | DEV-9 | Lecture 03 |
| every test cites its clause; every obligation in §9 claimed by at least one test | VER-6, VER-8 | Lecture 04 |
| the gate green at 100% branch with the single permitted pragma | VER-4, VER-5 | Lecture 04 |
| `fixtures/scenarios.json` with the eight scenario kinds, and a loader | VER-7 | Lecture 04 |
| at least one amendment committed before the code that depends on it | DEV-2 (c), DEV-3 | Lecture 04 |
| `PART-2-REPORT.md`: the amendment, what coverage did not tell you, how the pass and early-end fixtures were checked | VER-8, RPT-5 | Lecture 04 |

The fixture shape is fixed by the brief's §3.1 so that the same file can later
run against an engine in another language: squares in the notation your
grammar defines; the literal `"pass"` for a forced pass; colors named `dark`
and `light` regardless of the glyphs your display uses; and, for each move,
the set of squares it flips. The pass and early-end scenarios are hard to
construct by hand. You may generate them with your engine, but you must verify
them against your specification by hand before trusting them, and say how in
the report. Recall from Lecture 04 why: an engine cannot be the oracle for its
own fixtures.

## Logistics

- **The process set is adopted, not authored.** `process/` in your starter is
  the Lecture 04 set, identical to the demo's. A rule changes only by an
  amendment with a changelog entry (DEV-3). A change that weakens a rule —
  the coverage target, the pragma policy, the fixture rule — is returned.
- **Notation.** The sketch names squares "like `d3` on a chessboard." Whether
  `D3` and ` d3 ` are accepted, and what `d9` produces, are yours to decide and
  must be stated as a grammar (AUD-10). Where the letter becomes an index is an
  interface decision (AUD-12); the demo's lesson is that the translation lives
  inside the engine and never escapes it.
- **Effort and dates** are in the brief. Part 1 is due at the end of this
  week; Part 2 is assigned at Lecture 06.
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
3. Part 2 requires a scenario containing a pass. Before you trust a scenario
   your own engine generated, what do you check it against, and how — and what
   does VER-7 say about the fixture file afterwards?

## Before next meeting

- Project 1, Part 1 is launched today: `../project-1-reversi-brief.md`, §2.
  Start with the audit you watched, in your own copy of
  `../student-materials/reversi-starter/`.
- Read the Model Context Protocol documentation's core concepts and the
  FastMCP quickstart, and the dice-server README in the project unit
  (`../../weeks-04-07/student-materials/mcp-example/README.md`). Lecture 06 asks
  what changes when the reader of a specification is a machine.
