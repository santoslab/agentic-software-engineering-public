# Reversi audit walkthrough (Lecture 05) — the first move of Part 1, performed live

The demonstration for Lecture 05 is one segment of the method applied to a game
the class has not seen specified: the audit of the Reversi concept-of-operations
sketch, the gap list per RPT-1, rulings on four of its items, one deferral, and
one ruling carried through to an amendment proposal per RPT-3. It stops there,
because everything after that point is Project 1, Part 1.

**A caution that governs the whole script.** Do not depend on the agent making
one specific move. The agent's list will be longer than the key and ordered
differently; rule on the four scripted gaps and defer one, and mark the rest
*ruled* in a sentence or *deferred*. Rehearse once and capture at every
`[fallback capture]` marker; the key stands in for the agent's list if the
session fails.

## What the starter contains, and what is known about it

The starter (`../../student-materials/reversi-starter/`) has four things:
`CONOPS-sketch.md` — the client's general idea in the Lecture 02 skeleton with
sections 2, 3, and 6 omitted, because there is no existing system; the loader
`CLAUDE.md`; `process/`, the L04 set, identical to the game demo's; and
`BACKLOG.md`. No `CONOPS.md`, no `SPECS.md`, no code, no tests.

The sketch is incomplete on purpose and contains one internal tension. The key,
`expected-gaps.md`, lists 18 decisions the sketch leaves open and 8 more that
surface when `SPECS.md` is derived, with the standard ruling for each and a
mark on the ones that are genuinely the student's. Four are ruled live and one
is deferred:

| # | Gap | Scripted ruling | Found by |
|---|---|---|---|
| 1 | The game ends "when the board is full" — **in tension with** the forfeit rule: with forced passes the board may never fill | the game ends when neither player has a legal move; a full board is one case of that | AUD-2 |
| 2 | The opening position: "a few discs already in the middle" | d4 and e5 light, d5 and e4 dark | AUD-4; AUD-8 |
| 5 | Consequences of a pass: forced or chosen; announced; whose turn; two in a row | forced, never chosen; announced; the opponent moves; two consecutive passes end the game | AUD-4; AUDCON-3 |
| 6 | Must *all* flanked runs flip, in all eight directions? | yes — every direction, every run | AUD-1 |
| 7 | Legal-move hints — flagged by the client as undecided | **deferred** to `BACKLOG.md`: a display decision; the concept of operations does not need it settled; the display format will | AUD-4 → DEV-6 |

Item 1 is the one to spend time on. The sketch's two statements — "if you have
no square you can play, you forfeit your turn" and "when the board is full, the
discs are counted" — are each true of Reversi, and together they are incomplete:
if both players are stuck with empty squares left, the sketch says nothing about
what happens. AUD-2 finds it by reading the two bullets side by side. Students
who know Reversi will supply the answer and call it obvious. The reply, once, is
that a rule the sketch does not state is a finding, whatever the reader already
knows — the brief's convergence rule says how such findings are resolved, not
that they are skipped.

## Before class — setup checklist

1. A fresh copy of the starter, outside the course repository, with one
   initial commit:

   ```sh
   rm -rf ~/reversi-demo
   cp -R <path-to-module>/student-materials/reversi-starter ~/reversi-demo
   cd ~/reversi-demo && git init && git add -A
   git commit -m "part 1 start: conops sketch and process"
   ```

2. Rehearse Segment 2 once; keep the rehearsal repository and its captures.
3. Claude Code started in the copy with the always-on process files loaded;
   two terminals, large font; the prompts in a text file; `expected-gaps.md`
   printed, for your eyes.
4. The brief's two required-elements checklists (§2 and §3) on a slide, for
   Segment 3.

## Segment 1 — Learn the game from its sketch (about 14 minutes)

No agent. **Do (shell):** `cat CONOPS-sketch.md`. Read §1.2 and §4.2 aloud.

**Say:** this is the first time most of the room has learned a game's rules
from a concept of operations, and it is the same act as validation: a reader
asks whether the document describes the game that was wanted, and finds out
where it does not. Sort §4.2's policies on the board with the room:

| Stated | Implied | Missing |
|---|---|---|
| two colors; alternate turns; one disc per turn | an opening position exists (§1.2 "a few discs already in the middle") | who moves first |
| a move must trap at least one disc, in a straight line, in any of the three kinds of direction | trapping in more than one direction at once is possible (§4.2 "everything trapped flips") | what happens after a forfeit: whose turn, is it announced, what if both are stuck |
| a player with no square to play forfeits the turn | the count is shown at the end (§5.1) | equal counts |
| when the board is full, the discs are counted and more wins | | whether a move can be taken back (§7 says no — in the wrong section) |

Then the tension. **Ask:** "Both players are stuck with twelve empty squares
left. What does the program do?" Let the room find that §4.2's last bullet and
its third bullet do not, together, say. That is the finding the audit will make
first.

`[fallback capture]` — the sorted table.

## Segment 2 — The audit, watched (about 26 minutes)

**Do:** give the room three minutes to write its own gap list, on paper, from
the sketch alone. Then plan mode, and the prompt:

> Read `CONOPS-sketch.md` and the process documents. Before proposing anything,
> run the audits in `process/conops-audit.md` and `process/spec-audit.md` on the
> sketch (DEV-8) and report the gap list per RPT-1 — numbered, each with your
> recommended resolution. Then stop and wait for my rulings.

**Expected:** an RPT-1 list — where, category, quoted text, recommendation,
status — ending with the three search places covered (AUD-6). It usually
contains most of the key's first 18 rows, in its own order, and things the key
does not list.

`[fallback capture]` — the list.

**Do:** compare, aloud, with the room's lists: what the room found that the
agent did not, and the reverse. Then rule on 1, 2, 5, and 6 per the table
above, each in one or two sentences, saying which document the ruling belongs
in: the end condition, the opening, the pass, and the flips are all things a
player observes, so they go in the concept of operations (AUDCON-2). Defer 7:

> Ruling on the hints item: deferred. Write it to `BACKLOG.md` per DEV-6 — the
> question, where it arose, the options — and do not decide it. The display
> format will settle it when `SPECS.md` is derived.

**Say:** a deferral is a decision not to decide yet, recorded where the next
person can find it. It is not a guess.

For the remaining items, say *ruled* with the standard ruling in a sentence
each, or *the student's choice* — and say what that phrase means: the brief
lists which decisions are the client's and which are yours; yours are graded on
being recorded, consistent, and stated in the right document, not on which way
you decided.

**Do:** one ruling to the amendment form:

> Propose the amendment for item 1 per RPT-3 — document, clause, old text, new
> text, rationale citing the gap-list item, the version bump, the changelog
> entry — and wait for approval.

**Expected:** an RPT-3 proposal, marked *awaiting approval*, for the sketch's
§4.2 last bullet.

`[fallback capture]` — the proposal.

**Say:** this is the form every ruling takes before a document changes (DEV-3).
Approve nothing further. Then stop, and say why: from here to `CONOPS.md` 1.0 —
the remaining rulings, the amendments, the rewrite in the third person, the
scenarios, the glossary, the audit run again — is Part 1, step 1. The class
has now seen its exact first move performed on its own starter.

**If it goes differently:** if the agent misses item 1, nudge: "Both players
are stuck with twelve empty squares left. What does the program do?" Item 2:
"Draw the board before the first move. Which squares hold which color?" Item 5:
"You have no move. What is the very next thing that happens — and the thing
after that?" Item 6: "A square would trap discs both across and diagonally.
What flips?" If the agent starts writing `CONOPS.md` after the rulings, stop it;
the amendment proposal is the last artifact of the hour, and RPT-4 is the rule
it skipped.

## Segment 3 — The deliverables, by rule (about 14 minutes)

No agent. The brief's two checklists on the screen, and for each required
element the rule that governs it and the lecture that taught it.

**Part 1 (assigned today):** `CONOPS.md` 1.0 — AUDCON-1 through AUDCON-8;
`SPECS.md` 1.0.0, one section per kind, every clause numbered, §9 as
obligations — AUD-8 through AUD-14, AUD-5; the elicitation transcript with two
RPT-1 lists and the RPT-3 amendments; `CLAUDE.md` and `process/` as shipped —
DEV-3; the history showing the concept of operations committed before the
contract work begins — DEV-2, DEV-7.

**Part 2 (assigned at Lecture 06):** the plan under `plans/` — DEV-9; tests
that cite — VER-6; the gate — VER-4, VER-5; fixtures with a pass and an
early-end scenario — VER-7; at least one amendment committed before the code
that needs it — DEV-2 (c), DEV-3; the report naming what coverage did not tell
you — VER-8.

**Say:** nothing in either list is new. Every item is a rule the class has
watched applied to the note set or the tic-tac-toe game. What is new is the
game, and the specification-family table is the checklist for what each kind of
specification has to say about it.

## Segment 4 — Logistics and questions (about 10 minutes)

- The `process/` set is adopted, not authored. It is the L04 set; a rule
  changes only by an amendment with a changelog entry (DEV-3), and a change
  that weakens a rule is returned.
- `d3` notation: the sketch says squares are named "like `d3` on a
  chessboard"; whether `D3` and ` d3 ` are accepted, and where the letter
  becomes an index, are the student's decisions — stated as a grammar
  (AUD-10) and placed inside the engine (AUD-12).
- Effort and dates per the brief. Where to ask.

## End

The demo repository holds the sketch, the process set, one deferred question
in `BACKLOG.md`, and an unapproved amendment proposal in the conversation. It
is not committed further; students start from the starter, not from this
repository.

## Recreating this yourself (students)

This segment is Part 1, step 1 of the brief. Run it in your own copy of the
starter, rule on every item yourself — the brief's §4 is your checklist; the
instructor key is for grading, and reading it first defeats the exercise — and
continue to `CONOPS.md` 1.0.
