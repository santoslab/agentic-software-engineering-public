# Lecture 03 — Specifying a Game: One System, Several Specifications

> Software-engineering module, meeting 3 of 6. Companion reading for the lecture
> and for part 1 of the game demo
> (`../demos/lecture-03-game-demo/demo-script-lecture-03.md`); self-contained.
> Launches Exercise 3 (optional); Exercise 2 is due before Lecture 04.

## Illustrating spec-based development with a program

The first two lectures introduced basic concepts of specifications and realizations
using a set of markdown notes. The specification described markdown format rules for 
each note, the realizations were markdown files; the operations were three things an agent
helps a human do with the set of notes. Everything else — the audit, the reports, the three kinds of
verifier, the development rules, the invariant — was about the relationship
between a specification and what realizes it.

The important thing about all the above is that none of the above concepts and patterns
depend on the realizations being non-executable markdown files.  The same 
concepts apply broadly to developing programs as well.

This lecture applies the same process to a simple program: a command-line game,
tic-tac-toe on a 9-by-9 grid where five in a row wins.  As we move from the 
note set example to the game example, three things are going to be different.

- The specification starts as a **sketch** (a collection of informal ideas), not a fully written 
  draft: the sketch contains a client's general idea,
  written in the first person in one sitting. Lecture 01's specification had
  six numbered rules (i.e., we tried to be specific from the start); 
  this one only says things like "I want a bigger board", and we also leave two sections
  marked TBD.
- The realization is code (not markdown files), and what the code must satisfy is not one
  specification but **several kinds** — rules of play, a display format, an
  input grammar, an interaction flow, an interface contract, an example session,
  verification obligations — each fixing something the others leave open.
- The process documents gain three rules and one appendix, all about building:
  audit before planning (DEV-8), plan before build (DEV-9), read the repository
  before asking (DEV-10); two rules for the full concept-of-operations skeleton
  (AUDCON-7, AUDCON-8); and checks by kind of specification (AUD-8 to AUD-14).

The repository at the start holds a `CLAUDE.md` (which loads other files), `CONOPS-sketch.md`, `process/`,
and `BACKLOG.md`. No concept of operations, no technical specifications, no code.

Why did we use a game as the example in this lecture?
It has a grid (some visual elements), two players (multiple people interacting with the system), 
rules (some natural "behavior requirements" for the system), and a terminal condition (we can
recognize that a "playing mode" is done, and consider re-starting).  The example is
small enough to specify completely in a lecture and large enough to 
have several kinds of specifications. Project 1 (the Reversi project) 
is a game with the same shape.

## A concept of operations for a program

Lecture 02's concept of operations used the light skeleton. The game uses the
full one - nine numbered sections:
 - scope;
 - current situation; 
 - justification for and nature of the changes; 
 - the concept for the proposed system (objectives, operational policies, modes, user classes, environment); 
 - operational scenarios (user stories about the system);
 - summary of impacts; 
 - analysis; 
 - future capabilities; 
 - glossary. 
 
Sections 2, 3, and 6 (dealing with the current state and proposed changes) 
apply only when an existing system is being improved. The sketch keeps 2 and
3 short, because ordinary 3-by-3 tic-tac-toe is the baseline, and skips 6 (summary of impacts).

Our audit rule AUDCON-7 audits exactly this: are the optional sections present when there is a
baseline and absent when there is not, and is every needed section filled?

What the concept of operations does for a program is what it did for the note
set. It states the purpose of the system and how it is used from an external
point of view (i.e., how the system interacts with external entities).

For the game, the ConOps states what the game is for and what a player observes — the
operational policies of §4.2: two marks, X moves first, turns alternate, five in
a row wins — and it answers a validation question: is this the game that was
wanted? A player can read it and say. What it does not do is decide any system internals a
player cannot observe (AUDCON-1, AUDCON-2), e.g., how the board is stored, what a
method returns. Those belong to the technical specifications.

Two correspondences with Lecture 02 are worth remembering because they are instances
of important general concepts.  The game's first operation is a
move: its precondition is that the cell is empty and the game is not over; its
postcondition is that the cell holds the current player's mark and the turn has
passed.   This corresponds to the general notion of an initial system state where
one or more operations on the system are available to be executed.

Second, we have requirements or rules that the system obeys as it evolves.  That is, 
we have "invariants" that the system must maintain as execution unfolds.  In our case, 
the rules of game play are the invariant, in the sense the format
specification was: every state the game can reach must satisfy them, and a
check after every move is what keeps that true.  This is a general pattern that must
be followed when working with invariants.

## Round 1: turning the sketch to a concept of operations

The demo's second segment runs the audits on the sketch.  Recall that our development 
rule DEV-8 requires an audit of ConOps and Specifications before doing any planning:

> Read `CONOPS-sketch.md` and the process documents. I want a `CONOPS.md` 1.0
> that realizes this sketch as a full-skeleton concept of operations. Before
> proposing anything, run the audits in `process/conops-audit.md` and
> `process/spec-audit.md` on the sketch (DEV-8) and report the gap list per
> RPT-1 — numbered, each with your recommended resolution. Then stop and wait
> for my rulings.

The sketch leaves fourteen things open, and the list usually contains most of
them. Some are the kind Lecture 01 found — an ambiguity, an omission, an
inconsistency:

- "Five in a row wins." Does six? (AUD-1.) Ruling: five or more.
- The last empty square completes five in a row. A win, or a draw? The sketch's
  draw rule is silent. (AUD-4.) Ruling: a win takes precedence.
- The sketch says the post-game choices are "play again or the start menu" in
  §4.3 and "play again or quit" in §5.1. (AUD-2 — inconsistent within the
  document.) Ruling: three options.
- "You pick a square by typing its row and column." In what form? (AUD-1.)
  Ruling: a two-digit entry, row then column, no separator.

Others are the kind only a concept of operations can have, and the AUDCON rules
find them:

- "Nothing is saved between games" appears under §7, Limitations. It is a fact
  about the operational environment and belongs in §4.5 (AUDCON-8).
- One scenario, and it assumes a win. Every mode and policy must appear in a
  scenario (AUDCON-3): two-player play, a tie, recovery from a bad entry.
- The glossary says TBD (AUDCON-7).
- The whole document is in the first person (AUDCON-5).

We want to illustrate that some aspects of developing the specifications can be
explicitly deferred.

So one item is deferred on purpose: whether a player can quit in the middle of a
game. The original ConOps sketch is silent on this point, nothing depends on it 
for what we do in this lecture.  Note that in explicitly constructing the backlog list, 
we are following our development rule DEV-6 that says such a question goes to `BACKLOG.md` 
rather than being guessed. Watching it go there is part of the lecture.

So to summarize what happens in this phase, the developer evaluates the 
feedback from the agents; the agent proposes amendments per our rules for 
reporting audit results in RPT-3; the developer approves the amendments; 
the agent then writes `CONOPS.md` 1.0, audits it again (the DEV-8 rule requires
that we re-audit after an amendment too), and commits. 
The rewrite takes the agent more than two minutes, so the class sees it from the tag. 
What survives the rewrite is the original concepts that we introduced in the sketch (but with 
the details filled out); what does not survive is the informal "sketchy" writing and
the first-person writing (the agent switches that to third-person).

## Several kinds of specification

For the note set, one document — the format specification — said what a
conformant realization was. For a program, we typically need multiple types of specifications. 
Consider:  our game has rules; it has a screen; it takes input; it has menus; it has an interface that
code calls; and the tests that will verify it need to know what to claim. Each
of these is a specification of a different kind, fixing different things and
verified by different means.   Here is a summary of the different types of specifications.

| Kind | Fixes | Leaves open | Form | Verified by |
|---|---|---|---|---|
| Concept of operations | what the game is for; what a player observes; modes; scenarios | everything a player cannot see | prose, the full skeleton | a person reading (validation) |
| Rules of play | the win condition, the tie, their precedence, the initial state, the turn | how a rule is implemented | numbered clauses | tests; fixtures |
| Display format | exactly what the screen shows | nothing — byte-exact | example plus measurements | golden-string tests |
| Input grammar | every accepted and rejected form; the effect of a rejection | the wording of an error message | a grammar | rejection tests |
| Interaction flow | menus, options, the per-game loop, every exit | — | numbered steps | scripted-input tests |
| Interface contract | each public operation: parameters, precondition, postcondition, behavior outside the precondition | the algorithm | signatures with contracts | unit tests |
| Example session | one whole transcript | — | specification by example | an end-to-end run |
| Verification obligations | what the tests must claim, traced to clauses | how the tests are written | a list of categories | reading the suite |

Every row of this table is an instance of a kind in the course's catalog of
specification kinds (`../../specification-kinds.md`), which gives each kind's
purpose, its audit rules, how it is used in verification, and examples inside
and outside the course. One row carries a game-specific name: the *rules of
play* are the game's instance of the catalog's *behavioral requirements*. The
other seven rows use the catalog's own names, and any interactive program has
them. The catalog also lists kinds this game has that the table leaves out
because they are not derived from the concept of operations — the module split
(architecture, `SPECS.md` §2 and §5), the platform (Python, `pytest`), and the
process documents themselves — and the kinds Lecture 04 adds (the test suite,
the fixtures) and Lecture 06 adds (the tool contract).

Here are two important concepts.  

All the different forms of specifications (the specification "kinds") 
must agree with one another — the same fact stated
in the concept of operations, in the rules, and in the obligations.
The AUD-3 rule now applies across a family of specifications rather than just a pair
of specifications.  Also, each kind has checks of its own,
which the audit's appendix gives as AUD-8 through AUD-14: the rules of play
state every terminal condition and the precedence between them; the display
format is byte-exact with examples for the initial, a mid-play, and a terminal
state; the input grammar enumerates every rejected form and its effect; the
interaction flow names every option and exit; the interface contract says what
each operation does outside its precondition, including after the game is over;
the example session agrees with the three kinds it exercises, character for
character; and every clause maps to at least one obligation.

**Important**: What we are learning here is that, in the context of agentic 
development, we are less focused on writing code (the agent does that), and more
focused on setting up the *development framework* - choosing which types of specifications 
to use, writing the quality/audit rules for specifications so that they can be 
kept in a good state as development proceeds, designing what it means for a realization
to be conformant to a specification.  

**Important**: choosing which kinds of specification to use is itself a
decision, and in practice it is the developer's or the organization's. A
company often has a fixed collection of specification kinds that every project
must produce, with a prescribed format for each; a certification standard
prescribes its own. Without that guidance, someone has to decide the kinds and
their formats — and if nobody does, the agent decides by default, and the
decision surfaces later in the shape of the code. To keep the demo simple and
more deterministic, we pre-pick the kinds here: the loader `CLAUDE.md` names
the eight sections of `SPECS.md`, the round-2 prompt repeats them, and our
audit rules AUD-8 to AUD-14 check one kind each, so an omitted kind is a
finding. The Reversi assignment pre-picks the same kinds in the same order (the
brief's Phase 1, step 2). What the agent decides is everything inside that
frame: which open decisions each kind must settle, and what it proposes for
each.

Some kinds survive a change of programming language unchanged — the concept of
operations, the rules, the display format, the grammar, the example session,
and (from Lecture 04) the fixtures — and some are re-expressed for each
language: the interface contract and the tests. The catalog's summary table
records this for every kind in its *survives a port?* column, and a later
lecture uses that column when the game is ported to a different programming
language.

## Round 2: deriving specifications from the concept of operations

The demo's third segment derives `SPECS.md` from `CONOPS.md`.  Recall that
the specifications serve as a *contract* that our realization must adhere to.

> Read `CONOPS.md` and the process documents. Derive `SPECS.md` 1.0.0 from it:
> one section per kind — board and coordinates; rules of play; display format,
> byte-exact; input grammar; interaction flow; interface contract with
> preconditions and postconditions; an example session; verification
> obligations. Before writing, run the audit (DEV-8) and list every decision
> the concept of operations leaves open, grouped by the kind of specification
> that must settle it, per RPT-1 with a recommendation each. Wait for my
> rulings.

The list comes back grouped by kind, and the groups are the rows of the table
above — not because the agent invented the grouping (the prompt and the loader
hand it the kinds) but because the open decisions do fall into those kinds,
with one exception discussed below. Four rulings are made live.

- **Display.** The concept of operations never says what the board looks like;
  a display specification is a kind the concept of operations does not contain
  (AUD-4), and it must be byte-exact (AUD-9). Ruling: labels always visible,
  `.` for an empty cell, four leading spaces on the column header, nineteen
  dashes in each border — and two examples, one empty, one mid-game.
- **Input grammar.** The concept of operations settled "two digits." It did not
  say whether `0` is a digit, whether spaces are tolerated, or what happens to
  `123` (AUD-10). Ruling: strip whitespace; exactly two characters; each in
  `1`–`9`; anything else is rejected and the turn does not pass.
- **A move after the game is over.** The interface contract must say what every
  operation does outside its precondition (AUD-12). Ruling: rejected, with no
  change of state. The reference implementation the course keeps was built
  from a specification that never said this; today's specification is stricter than
  that code, and Lecture 04 will show what a test suite does with the
  difference.
- **"The computer picks at random."** How is that verified? A test cannot check
  randomness by running the game once. Ruling: the obligation is that the
  result is always among the available moves, on a board that is partly full —
  a property, not a distribution.

One item in the list is not a decision the technical specifications make at all, and it is
worth saying so: the coverage policy — 100% branch coverage, the single
permitted pragma, the discipline that every test cites its clause — is already
in `process/verification.md`.  This is really a quality constraint on the 
implementation.   What `SPECS.md` §9 holds is the obligations: what
the tests must claim about *this* game, category by category. The policy is the
same for every project; the obligations are not.

`SPECS.md` 1.0.0 has eight sections and every clause has a number. The
reference's numbering is a good model: §3 board and coordinates, §4 win
condition (4.1 the winning line, 4.2 the tie, 4.3 their precedence), §5 the
modules and their interfaces, §6 input handling, §7 display conventions, §8 an
example session, §9 verification obligations.

## Quality across the family of specifications

The properties of Lecture 01 apply to each specification document, and across 
the family of specifications.

**Unambiguous (AUD-1).** "The board looks like this" with a picture is not a
display specification; "four leading spaces, then the digits 1 to 9 separated by
single spaces" is.  We need this level of detail in our specification to ensure
that we can test appropriately.  Byte-exact means a test can compare strings.

**Externally consistent (AUD-3).** Follow one fact across the family of specifications. The
concept of operations: a player wins with "five or more" marks in a line. The
rules of play, §4.1: overlines count. The verification obligations, §9: at least
one overline case. Lecture 04 adds a test citing §4.1 and a fixture named
`x-wins-row-overline`. One intent, five statements, one chain of identifiers.
If the rules said "exactly five," the audit would find it (and the reference's
early drafts did say it).

**Complete for its level (AUD-4).** What does the display format say about a
full board? What does the interface contract say about `make_move` when the
game is over? The walkthrough — play one game on paper, from the menu to the
post-game menu — finds the gaps.

**Traceable (AUD-5).** Every clause has a section number, so that a test can
say `SPECS §4.1` in its docstring, a fixture can cite a rule, and an amendment
can be located. When a clause is added, it gets a new number; nothing is
renumbered.

## Implementation as a consequence of the specifications

Nothing in this lecture has been built, and the specification is complete for
its level. DEV-8 is satisfied: every specification the plan would realize has
been audited. We are now ready to enforce DEV-9: 
any build is preceded by a plan, proposed in
plan mode, approved, and committed under `plans/`, and the plan cites, for each
step, the clauses it realizes. The first prompt asks for the plan and nothing
else:

> Read `SPECS.md` and the process documents. Propose a plan for the engine
> module, the computer opponent, and the command-line interface, citing for
> each step the clauses it realizes, and wait for my approval.

The plan is read and ruled on. Only then does the second prompt ask for the
build:

> Approve the plan. Commit it under `plans/` as
> `plan: engine, opponent, CLI (DEV-9)`. Then build the three modules per the
> approved plan, report per RPT-5 with the clauses each module realizes, and
> commit as `engine: game, opponent, and CLI per SPECS 1.0.0`.

Two things about that second prompt. The plan is committed before the first
implementing commit, which is what DEV-9 requires: an approved plan is an
artifact of the repository, readable later by anyone asking why the code has the
shape it has, not an exchange that disappears with the session. And the prompt
says nothing about how to build anything — no module structure, no algorithm, no
naming. It does not need to. The plan says that, and the plan cites the contract
clause by clause; anything the prompt added here would be a fourth source of
truth competing with three that are already written down.

The plan and the build are shown from the tag; both take the agent longer than
a lecture can wait. What the class sees is the result: three modules — an
engine with no input or output, a computer opponent as a set of strategies, an
entry point that owns every prompt — and a history that reads specification,
plan, realization. `CLAUDE.md` is still two rules. The laws are in `process/`.

Nothing has been verified yet except by playing one move each way. That is
Lecture 04.

## What is new in the process documents

| Rule | Says | Used today |
|---|---|---|
| DEV-8 | audit before any plan, and again after any amendment | rounds 1 and 2; the re-audit of `CONOPS.md` 1.0 |
| DEV-9 | plan, then build; the plan cites clauses; committed under `plans/` | the implementation |
| DEV-10 | a question the repository can answer is answered by reading it | throughout |
| AUDCON-7 | the full skeleton: kept sections filled; sections 2, 3, 6 present only with a baseline | the TBD glossary; sections 2 and 3 kept, 6 skipped |
| AUDCON-8 | a fact in the section whose purpose it serves | "nothing is saved" moved to §4.5 |
| AUD-8 to AUD-14 | checks by kind of specification | round 2 |

## Exercise 3, and what comes next

Exercise 3 is optional: from your own copy of the starter, run round 1 and
compare your gap list with the script's table; then, if you continue, run
round 2 and submit the grouped list with your rulings. It is the same work as
Exercise 2 on a different kind of system, and it is the first move of
Project 1.

Lecture 04 takes the implementation and verifies it: a test suite that cites
clauses, a coverage gate, and what coverage does not tell you. Lecture 05 hands
you a sketch of a different game and asks for these moves in your own session.

## Questions to think about

1. The question "how is the random opponent tested?" ended up in the verification
   obligations, not in the rules of play. Why is *how it is tested* not a
   property of the game? What would it mean for the concept of operations to
   say it?
2. The sketch said "five in a row." The concept of operations says "five or
   more." Which side moved, who decided, and where is the decision recorded —
   and what does the rules-of-play clause add that the concept of operations
   does not?
3. Of the fourteen round-1 gaps, which would a player have noticed first, and
   which only an implementer? Use AUDCON-2 to sort them, and say what that
   sorting tells you about which document each ruling belongs in.

## Before next meeting

- Read `process/verification.md` at its Lecture 04 level — VER-5 through VER-8 —
  before the lecture that teaches them, and the shared-fixtures README from the
  project materials.
- Exercise 2 is due before Lecture 04. Exercise 3 is optional.
