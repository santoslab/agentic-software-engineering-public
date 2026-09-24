# Reversi walkthrough (Lecture 05) — the brief's Phase 1, step by step

The demonstration for Lecture 05 is the Project 1 brief
(`../../project-1-reversi-brief.md`) read in order. Step 1 — the audit of the
Reversi concept-of-operations sketch, the gap list per RPT-1, rulings on four
of its items, one deferral, and one ruling carried through to an amendment
proposal per RPT-3 — is shown from captures taken at rehearsal, on the starter
the students have, and stops before `CONOPS.md` is written. Steps 2 to 5 are
shown by opening, at each step, the artifact the reference game produced
(`../lecture-03-game-demo/reference/`, the `t5` state) at the section the brief
names as the model. Step 6 and the logistics close the hour.

**A caution that governs the step-1 captures.** Do not depend on the agent
making one specific move. The agent's list will be longer than the key and
ordered differently; rule on the four scripted gaps and defer one, and mark the
rest *ruled* in a sentence or *deferred*. Take the captures at rehearsal with
the step-1 prompt exactly as the brief prints it, so that students see one
prompt for one move; the key stands in for the list if a capture is missing.

## What is live and what is from captures

| Segment | Step | Live | From captures or files |
|---|---|---|---|
| 1 | — | the checklist table; the brief's §2 on screen | — |
| 2 | 1 | the room's own gap list; the sorting of §4.2 | C1 the RPT-1 list; C2 the four rulings; C3 the deferral and `BACKLOG.md`; C4 the RPT-3 proposal |
| 3 | 2 | — | `reference/SPECS.md` §4, §5.1, §7.2, §9.5 opened |
| 4 | 3 | the six commands of the five-artifact history | `plans/001` opened |
| 5 | 4 | the gate in `reference/`; the pragma grep | `plans/002` and two tests opened |
| 6 | 5 | — | `fixtures/scenarios.json`, `fixtures/README.md`, `tests/test_fixtures.py`, `plans/003` opened |
| 7 | 6 | — | the brief's checklist on a slide |

## What the starter contains, and what is known about it

The starter (`../../student-materials/reversi-starter/`) has five things:
`CONOPS-sketch.md` — the client's general idea in the Lecture 02 skeleton with
sections 2, 3, and 6 omitted, because there is no existing system; the loader
`CLAUDE.md`; `process/`, the L04 set, identical to the game demo's;
`BACKLOG.md`; and the gate's configuration — `.coveragerc`, `pytest.ini`,
`requirements-dev.txt`, `.gitignore`. No `CONOPS.md`, no `SPECS.md`, no code,
no tests.

The sketch is incomplete on purpose and contains one internal tension. The key,
`expected-gaps.md`, lists 18 decisions the sketch leaves open and 8 more that
surface when `SPECS.md` is derived, with the standard ruling for each and a
mark on the ones that are genuinely the student's. Four are ruled in the
captures and one is deferred:

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

1. A fresh copy of the starter, outside the course repository, with the initial
   commit of the brief's step 0:

   ```sh
   rm -rf ~/reversi-demo
   cp -R <path-to-module>/student-materials/reversi-starter ~/reversi-demo
   cd ~/reversi-demo && git init && git add -A
   git commit -m "phase 1 start: conops sketch and process"
   ```

2. Rehearse Segment 2 once in that copy with the step-1 prompt exactly as the
   brief prints it, and capture C1 to C4 at the markers below. Keep the
   rehearsal repository. Nothing beyond C4 is captured — a Reversi `CONOPS.md`
   1.0 is the homework and is never shown.
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
   brief open at §2 and at §3.1; its required-elements checklist on a slide.

## Segment 1 — Where we are (about 6 minutes)

No agent. The specification-family table with its audit and verifier columns,
as the checklist for Project 1. Then the brief's §2 headings on screen: seven
steps, with the demo's tags `t0` to `t5` beside steps 0 to 5.

**Say:** today reads the brief in order. At each step we open the artifact the
reference game produced, so that you know what finished looks like before you
start. Nothing in the brief is new; what is new is the game.

## Segment 2 — Step 1, from captures (about 12 minutes)

**Do (shell, live):** `cat CONOPS-sketch.md`. Read §1.2 and §4.2 aloud, and
sort §4.2's policies on the board with the room:

| Stated | Implied | Missing |
|---|---|---|
| two colors; alternate turns; one disc per turn | an opening position exists (§1.2 "a few discs already in the middle") | who moves first |
| a move must trap at least one disc, in a straight line, in any of the three kinds of direction | trapping in more than one direction at once is possible (§4.2 "everything trapped flips") | what happens after a forfeit: whose turn, is it announced, what if both are stuck |
| a player with no square to play forfeits the turn | the count is shown at the end (§5.1) | equal counts |
| when the board is full, the discs are counted and more wins | | whether a move can be taken back (§7 says no — in the wrong section) |

Then the tension. **Ask:** "Both players are stuck with twelve empty squares
left. What does the program do?" Let the room find that §4.2's last bullet and
its third bullet do not, together, say. That is the finding the audit makes
first.

**Do:** give the room three minutes to write its own gap list, on paper, from
the sketch alone. Then the prompt, on screen, as the brief prints it for
step 1:

> Read `CONOPS-sketch.md` and the process documents. I want a `CONOPS.md` 1.0
> that realizes this sketch as a full-skeleton concept of operations. Before
> proposing anything, run the audits in `process/conops-audit.md` and
> `process/spec-audit.md` on the sketch (DEV-8) and report the gap list per
> RPT-1 — numbered, each with your recommended resolution. Then stop and wait
> for my rulings.

**Show C1** — the RPT-1 list from rehearsal. `[capture C1]`

**Expected:** an RPT-1 list — where, category, quoted text, recommendation,
status — ending with the three search places covered (AUD-6). It usually
contains most of the key's first 18 rows, in its own order, and things the key
does not list.

**Do:** compare, aloud, with the room's lists: what the room found that the
agent did not, and the reverse. **Show C2** — the rulings on 1, 2, 5, and 6
per the table above, each in one or two sentences, saying which document the
ruling belongs in: the end condition, the opening, the pass, and the flips are
all things a player observes, so they go in the concept of operations
(AUDCON-2). `[capture C2]`

**Show C3** — the deferral of 7, and `BACKLOG.md` after it. The ruling, as
typed at rehearsal:

> Ruling on the hints item: deferred. Write it to `BACKLOG.md` per DEV-6 — the
> question, where it arose, the options — and do not decide it. The display
> format will settle it when `SPECS.md` is derived.

`[capture C3]`

**Say:** a deferral is a decision not to decide yet, recorded where the next
person can find it. It is not a guess. For the remaining items, say *ruled*
with the standard ruling in a sentence each, or *the student's choice* — and
say what that phrase means: the brief lists which decisions are the client's
and which are yours; yours are graded on being recorded, consistent, and
stated in the right document, not on which way you decided.

**Show C4** — one ruling carried to the amendment form. The prompt, as typed at
rehearsal:

> Propose the amendment for item 1 per RPT-3 — document, clause, old text, new
> text, rationale citing the gap-list item, the version bump, the changelog
> entry — and wait for approval.

`[capture C4]` — an RPT-3 proposal, marked *awaiting approval*, for the
sketch's §4.2 last bullet.

**Say:** this is the form every ruling takes before a document changes (DEV-3).
Approve nothing further. Then stop, and say why: from here to `CONOPS.md`
1.0 — the remaining rulings, the amendments, the rewrite in the third person,
the five scenarios, the glossary, the audit run again — is step 1, and the
brief's step 1 lists what the audit must find in this sketch. The class has
now seen its exact first move performed on its own starter.

**Open:** `reference/CONOPS.md` §4.2, then §5.4. **Say:** a policy as a player
observes it; and a scenario for the policy of rejecting an entry — every policy
appears in a scenario (AUDCON-3). **Reversi:** five scenarios at least, because
a pass and an early end are policies tic-tac-toe did not have; and a version, a
status, and a changelog, which the sketch lacks (AUDCON-6). The step ends with
`conops: 0.1 sketch -> 1.0` and the transcript.

**If it goes differently at rehearsal:** if the agent misses item 1, nudge:
"Both players are stuck with twelve empty squares left. What does the program
do?" Item 2: "Draw the board before the first move. Which squares hold which
color?" Item 5: "You have no move. What is the very next thing that happens —
and the thing after that?" Item 6: "A square would trap discs both across and
diagonally. What flips?" If the agent starts writing `CONOPS.md` after the
rulings, stop it; the amendment proposal is the last artifact of the step's
first move, and DEV-3 — nothing in a governing document changes until an
amendment is approved — is the rule it skipped.

## Segment 3 — Step 2, the reference's `SPECS.md` (about 10 minutes)

**Say:** step 2's prompt is Lecture 03's round-2 prompt, which names no game;
the kinds are pre-picked; the brief's §4 is the floor for the list the agent
returns, and every item gets a ruling. Then, on the slide, what Reversi demands
that tic-tac-toe did not, kind by kind.

**Open:** `SPECS.md` §4. **Say:** rules of play as numbered clauses, so that a
test can cite one (AUD-5). **Reversi:** more clauses — the opening, the legal
move, the flips in every direction, the pass, the end, the count.

**Open:** §5.1, `make_move`. **Say:** a precondition, a postcondition, and
behavior outside the precondition, including after the game is over (AUD-12);
the Changelog shows that clause arriving at 1.2.0. **Reversi:** the
postcondition names the set of discs that flip; a test of a move claims the
set.

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

**Say:** the two DEV-9 prompts, on the slide. The first asks for the plan and
nothing else. The second approves, commits the plan under `plans/`, builds,
reports per RPT-5, commits — and says nothing about how to build anything,
because the plan says that and the plan cites the contract clause by clause.
**Reversi:** the same two prompts, over the modules `SPECS.md` §2 names; and
before them, the audit of `SPECS.md` itself — the move that would have caught
the silence.

`[fallback capture]` — the six commands' output.

## Segment 5 — Step 4, the suite as a build, and the gate (about 12 minutes)

**Say:** the process set in the starter is already the L04 set — VER-5 to
VER-8 are in `verification.md` 1.3, and the amendment Lecture 04 performed
before writing any test is done for the students; its changelog entry says
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
**Say:** one clause, eight rejected forms, parametrized. **Reversi:** the forms
the student's grammar rejects — `D3`, ` d3 `, `d9`, `i3`, `d`, `dd3`, an
occupied square, a square that flips nothing — in the order the grammar lists
them.

**Do (shell, live), in `reference/`:**

```sh
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100
grep -n 'pragma' *.py
```

**Expected:** 99 passed, 100% branch, exit 0; one pragma, on `main.py`'s
`__main__` guard (VER-5).

**Say:** RPT-5 carries two coverage lines — the gate's branch figure, and
which §9 obligations are claimed by at least one test (VER-8). They answer
different questions, and Lecture 04's three sabotage steps showed a case where
each was informative and the other was not. Then DEV-2's three kinds of
change, and the standing rule from step 3 on: a change of specified behavior
commits its amendment first.

**Open:** `.coveragerc`. **Say:** the starter ships the same file with
`source = .`, so it measures every module in the root whatever the split;
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

No agent. `PHASE-1-REPORT.md`'s four items: the amendment implementation
forced, one of them traced through five artifacts in the form of Segment 4;
what 100% branch coverage did not tell you; how the pass and early-end fixtures
were constructed and checked; what remains for a human or agent verifier. Then
the brief's required-elements checklist on the slide, each item tagged with its
step.

- The `process/` set is adopted, not authored. It is the L04 set; a rule
  changes only by an amendment with a changelog entry (DEV-3), and a change
  that weakens a rule is returned. The gate's configuration is adopted the same
  way.
- `d3` notation: the sketch says squares are named "like `d3` on a
  chessboard"; whether `D3` and ` d3 ` are accepted, and where the letter
  becomes an index, are the student's decisions — stated as a grammar
  (AUD-10) and placed inside the engine (AUD-12).
- Due one week from today (date per the brief); start with step 0 tonight.
  Lecture 06 is MCP and launches nothing — finish Phase 1. Where to ask.

## End

The rehearsal repository holds the sketch, the process set, the gate
configuration, one deferred question in `BACKLOG.md`, and an unapproved
amendment proposal in its transcript. It is not committed further; students
start from the starter, not from this repository.

## Recreating this yourself (students)

This is the brief. Run it in order in your own copy of the starter, beginning
tonight with step 0 and then the audit you watched. Rule on every item
yourself — the brief's §4 is your checklist; the instructor key is for grading,
and reading it first defeats step 1.
