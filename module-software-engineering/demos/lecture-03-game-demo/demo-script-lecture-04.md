# Game demo, part 2 (Lecture 04) — tests, the gate, and fixtures

## What this demonstration is for

Part 1, in Lecture 03, produced a concept of operations, a behavioral contract
of several kinds, an approved plan, and three working modules. It ended with the
instructor playing one move each way and observing that the program appeared to
work. That observation is a verification — a human verifier, applied once, to
whatever part of the specification the instructor happened to exercise. It left
no record, it named no clause it had checked, and no one else can repeat it and
get the same coverage of the contract.

Part 2 replaces it with an algorithmic verifier and then spends most of its time
asking what that verifier actually establishes. This is the point of the whole
demonstration, and it is worth stating plainly before the first command runs: a
test suite that passes is evidence, but evidence for a specific and limited
claim, and the claim is narrower than the word "passing" suggests. A green gate
establishes that the code does what the tests say. It does not establish that
the tests say what the specification says, and it does not establish that every
clause of the specification is claimed by any test at all. Those are three
different propositions, and a repository can satisfy the first while failing
both of the others with every number on the coverage report at 100%. Segment 3
shows exactly that, twice.

The demonstration makes that distinction concrete rather than asserting it. In
Segment 3 the class watches three edits to a repository whose gate is green at
100% branch coverage. The first edit deletes a test and the gate stays green.
The second breaks the engine and the gate goes red. The third breaks the engine
*and* the test that checks it, in the same way, and the gate stays green. After
each one the verdict is stated in a fixed form — what the gate established, and
what it did not. State the first two yourself; for the third, ask the class to
supply the sentence before you do.

The other half of the demonstration is about the order in which things are
written. The suite is about to be governed by rules that do not exist yet in
this repository: what coverage the gate demands, how a test must be written,
what a fixture file is and what may be done to it. Segment 1 puts those rules in
force before the suite exists, by the same amendment mechanism used on a
specification — a proposal, an approval, a version bump, a changelog entry. The
class has already seen that mechanism applied to a specification in Lecture 03.
Seeing it applied to the process documents themselves establishes that the rules
governing development are artifacts under version control like any other, not
preferences that live in someone's head.

## What the demonstration accomplishes, segment by segment

| Segment | Minutes | What is produced or shown | The point it carries |
|---|---|---|---|
| 1 — The process amendment | 6 | `process/` moves from the L03 set to the L04 set: `verification.md` 1.3 (VER-5 to VER-8), `reporting.md` 1.3, `README.md` 1.2, and a new loader | Rules that will govern an artifact are put in force before the artifact exists, by amendment, with a changelog entry |
| 2 — The suite, from the tag | 12 | A test suite of 85 unit tests under `tests/`, one file per source module, every test citing the clause it claims | `SPECS.md` §9 lists what the tests must claim; the suite is the realization of §9, and the completion note is its conformance report |
| 3 — The gate, then sabotage | 18 | The gate run green, then three edits and three verdicts | A green gate establishes that the code does what the tests claim, and nothing more than that |
| 4 — Reading the history | 8 | Four artifacts of the reference read in sequence: specification, plan, engine, test | A silence in a specification propagates to everything derived from it; the three kinds of change to a realization (DEV-2) are distinguishable from the history alone |
| 5 — Fixtures, from the tag | 10 | `fixtures/scenarios.json`, its README, and a parametrized loader over 14 scenarios | A specification of behavior can be written in a form no particular language owns, and a fixture set's blind spots are part of its contract |

At the end the repository holds a realization, an algorithmic verifier for it,
the rules that govern both, and a history in which every change to the
realization is identifiably one of DEV-2's three kinds. Lecture 06 starts from
that repository at `t4`.

## A caution that governs the whole script

Do not depend on the agent making one specific move. Agent behavior varies from
run to run and from version to version, and the value of the demonstration does
not rest on any particular output. The *Expected* notes describe the shape the
output usually takes, not a transcript to match. Every segment carries an *If it
goes differently* note giving the recovery.

Rehearse the whole of part 2 once before class. The rehearsal, not this script,
is the record of what your setup does — test names, counts, and timings all come
from it. Capture a screenshot at every `[fallback capture]` marker during that
rehearsal, so that a live run that goes differently does not cost a teaching
point.

Two things the agent produces here take longer than a lecture can wait: the test
suite at `t4` and the fixture loader at `t5`, each more than two minutes. Both
are shown from their tags. What the class watches happen live is the process
amendment in Segment 1, the three sabotage steps in Segment 3, and the reading
of the reports throughout. Budget the live time accordingly.

## What part 2 starts from, and what is known in advance

The live repository sits at `t3-engine`, holding `CONOPS.md` 1.0, `SPECS.md`
1.0.0, the approved plan under `plans/`, the three modules `game.py`,
`computer_ai.py`, and `main.py`, `BACKLOG.md`, the `CLAUDE.md` loader, and
`process/` at the **L03** level — `verification.md` 1.2 with VER-1 through
VER-4, `reporting.md` 1.2, and `README.md` 1.1.

Two absences matter for Segment 1. There are no tests. And nothing anywhere in
`process/` yet states what coverage a gate requires, how a test must be written,
or what a fixture file is. Those rules arrive in Segment 1, before the suite
that has to obey them.

`reference/` is the destination state, equivalent to `t5`: `SPECS.md` 1.2.1, the
engine, the suite of 85 unit tests plus a fixture loader over 14 scenarios,
`fixtures/`, `plans/`, and the L04 `process/`. Its commit history is not the live
repository's history; it was built earlier, from an earlier version of the
specification, and the difference is the subject of the note on the
after-game-over clause below.

### The three sabotage steps, and their known outcomes

The Segment 3 steps were run against `reference/` on 2026-09-22 in a virtual
environment with `pytest-cov` installed. The figures below are the reference's.
A suite generated live will have different test counts, and possibly different
test names, but the three outcomes hold.

| Step | Edit | Gate | What it shows |
|---|---|---|---|
| 1 | delete `test_check_winner_overline_counts` | **green**; 100% branch; one test fewer | Branch coverage is a property of the pair (tests, code). The clause §4.1 "overlines count" is now claimed by no test at all, and the coverage figure cannot report that (VER-8) |
| 2 | in `game.py`, in the up-right diagonal scan, `self.board[r - i][c + i]` → `self.board[r - i][c - i]` | **red**; two failures: `test_check_winner_diagonal_up_right` and `test_check_winner_detects_tie`; at `t5` the fixture scenario `x-wins-diagonal-down-left` fails as well | The gate returns the work (VER-4, RPT-4). The tie test fails for an instructive reason: the flipped index runs off the left edge of the board, Python's negative indexing wraps it round to the right edge, and the scan then reports a line that does not exist on the board |
| 3 | on a scratch branch: five leading spaces instead of four in `render`'s header **and** in the two expected-board constants in `tests/test_game.py` | **green**; 100% branch | A test whose expectation is wrong passes code that is wrong in the same way. The suite is itself a realization of §7.2, and a realization can be nonconformant (VER-1). The gate cannot detect this; a person reading §7.2 can |

### The after-game-over clause, and why the two repositories differ

This difference will be visible in Segment 2 and is the subject of Segment 4, so
it is worth understanding before class rather than discovering live.

Lecture 03's round 2 of the audit ruled that a move submitted after the game is
over must be rejected with no change of state. That ruling is in the live
repository's `SPECS.md` 1.0.0 at §5.1, recorded under AUD-12, and the plan at
`t3` realizes it.

The reference implementation was built earlier, from a specification that was
silent on the question. Its `SPECS.md` 1.1.0 gives two reasons `make_move`
returns `False` and says nothing about a move after a win, its plan under
`plans/` faithfully realizes those two reasons and no others, and its engine
accepted a move after the game had been won. Version 1.2.0 of the reference adds
the clause; the engine change and the test citing that clause follow the
amendment in the history. That ordering — amendment first, realization after —
is DEV-2 (c), and Segment 4 reads it out of `reference/`.

In the live repository the question at `t4` is a different one, because the
clause is already in the specification. Ask instead whether the completion
note's clause-coverage line (VER-8) lists §5.1's after-game-over clause among
those claimed by a test. If it does not, that is the clause to add a test for,
live, and Segment 2's *If it goes differently* note gives the prompt.

## Before class — setup checklist

1. Start from the rehearsal repository at `t3-engine` — `git checkout t3-engine`
   in `~/game-demo`, or a fresh copy of it. Rehearse the whole of part 2 once
   and tag as you go: `t4-tests-100` after Segment 2, `t5-fixtures` after
   Segment 5.
2. Have a virtual environment with both `pytest` and `pytest-cov` installed,
   activated in the demo shell, and confirm the gate runs green at `t4` and `t5`
   on the presentation machine on the day. The `pytest` installed globally
   through pipx does not carry `pytest-cov`, and without it the gate fails while
   parsing `--cov` rather than while running tests — an error that looks alarming
   in front of a class and has nothing to do with the demonstration.
3. In the demo shell, `export PYTHONDONTWRITEBYTECODE=1` and delete every
   `__pycache__` directory. Sabotage step 2 changes a single character and leaves
   the file size unchanged; a bytecode cache compiled within the same second as
   the edit is not invalidated, and the flipped scan then passes every test. This
   happened once in rehearsal and cost the segment its point.
4. Create the scratch branch for step 3 during rehearsal, from `t4`:

   ```sh
   git checkout -b sabotage-wrong-expectation t4-tests-100
   # game.py: header = "     " + ...   (five spaces)
   # tests/test_game.py: the first line of EMPTY_BOARD and MID_GAME_BOARD, five spaces
   git commit -am "scratch: wrong expectation, wrong code" && git checkout main
   ```

5. Note down, from rehearsal, the name of the overline test and the line number
   of the up-right diagonal scan. If `t4` is regenerated the names may differ,
   and hunting for them live wastes the segment's time.
6. Put the amendment proposal below into a text file ready to display. Have the
   four L04 files ready to copy from `reference/CLAUDE.md` and
   `reference/process/` (`README.md`, `reporting.md`, `verification.md`). Those
   three documents and the loader are the entire difference between the L03 and
   L04 process sets.
7. Have `fixtures/scenarios.json` and `fixtures/README.md` ready to copy from
   `reference/fixtures/`.
8. Start Claude Code in the live repository. Two terminals at a large font: one
   for the agent, one for `git`, `pytest`, and `cat`. Keep the prompts in a text
   file to paste rather than typing them live. Have every `[fallback capture]`
   screenshot to hand.

## The amendment proposal, pre-written (RPT-3)

Display this; do not type it and do not ask the agent to generate it. It is what
the agent would produce if asked to propose the L04 rules, and having it written
in advance saves about eight minutes of watching text appear. The class is
learning what an amendment proposal contains and what approving one means, not
watching one be composed.

> **Amendment proposal — the verification rules for a repository with tests.**
> *Awaiting approval.*
>
> 1. `process/verification.md`, 1.2 → 1.3 (minor). New clauses VER-5
>    (coverage policy: 100% branch; one permitted pragma, on the entry point's
>    `__main__` guard; an unreachable branch is recorded by amendment before
>    any pragma), VER-6 (test discipline: every test cites its clause; tighter
>    never looser; direct assignment for setup only; no test that cannot
>    fail), VER-7 (a fixture file is never edited to make a test pass; it
>    states its assumptions and its blind spots), VER-8 (branch coverage and
>    clause coverage are reported separately). Two binding rows: the test suite
>    against `SPECS.md` §9; the fixture loader. **Rationale:** the suite is
>    about to be written; the rules it must follow have to be in force before
>    it exists, for the same reason a specification precedes its realization
>    (DEV-2 (c)). **Changelog:** "1.3 — Added VER-5 through VER-8; binding rows
>    for the test suite and the fixtures."
> 2. `process/reporting.md`, 1.2 → 1.3 (minor). RPT-5 also reports which
>    verification obligations are claimed by at least one test and which are
>    not (VER-8). **Changelog:** "1.3 — RPT-5 reports clause coverage when the
>    verifier is a test suite."
> 3. `process/README.md`, 1.1 → 1.2 (patch). The map row for
>    `verification.md` names the coverage policy, test discipline, fixtures,
>    and coverage-versus-conformance. **Changelog:** "1.2 — VER-5 through VER-8
>    reflected in the map."
> 4. `CLAUDE.md` (the loader). Governing document 4, `fixtures/`; the gate's
>    coverage policy named as VER-5; the description of the repository updated
>    for one that has code and tests.

## Segment 1 — The process amendment (about 6 minutes)

**Do (shell):**

```sh
git log --oneline | head -5
grep '^### VER' process/verification.md
```

**Say:** the repository's verification document currently holds four rules,
VER-1 through VER-4, and the headings on screen are all of them. They define
what a verifier is, which clauses each kind of verifier may decide, when
verification runs, and what the gate is. That was enough for a repository whose
only realizations were prose and one small Python program.

It is not enough for what happens next. The suite that is about to be written
needs rules that this repository does not yet contain: what coverage the gate
demands, how an individual test must be written, and what a fixture file is. If
the suite is written first and the rules are written afterwards to describe it,
the rules are no longer rules — they are a description of whatever the agent
happened to do, and they cannot fail to be satisfied.

So the rules go in first, and they go in the same way a change to a
specification goes in: a proposal, an explicit approval, a version bump, and a
changelog entry (DEV-3). Display the proposal on screen for about thirty
seconds. Point out that it names each document, the version before and after,
the size of the change, the new clauses, the rationale, and the exact changelog
text — everything a reader six months from now would need to reconstruct why
these rules exist.

**Do:** approve the proposal aloud, then install the four files and show what
changed:

```sh
cp <reference>/CLAUDE.md CLAUDE.md
cp <reference>/process/README.md <reference>/process/reporting.md <reference>/process/verification.md process/
git diff --stat
git diff process/verification.md | grep '^[+-]' | grep -i 'changelog\|^+- \*\*1.3' 
git add -A && git commit -m "process: verification 1.2 -> 1.3 (VER-5..8); reporting 1.3; README 1.2"
```

`[fallback capture]` — the `git diff --stat` output and the changelog lines.

**Say:** note what did not change. `SPECS.md` is untouched. Nothing about the
game's behavior is different from five minutes ago; a player would see no
difference. What changed is the set of rules under which the next artifact will
be built and judged.

Note also the shape of the change. The documents that govern how development
proceeds were amended by exactly the mechanism they themselves prescribe for
amending a specification. They are artifacts in the repository, under version
control, with versions and changelogs, and they are subject to their own rules.
A rule that lives only in a team's habits cannot be cited, cannot be audited,
and cannot be shown to have been in force at the time a decision was made.

Three of the four new rules — VER-5 on coverage, VER-6 on test discipline, VER-8
on the two kinds of coverage — will be visibly applied in the next forty
minutes. The fourth, VER-7 on fixtures, arrives in Segment 5.

**If it goes differently:** if a file is missed or the wrong one is copied,
`git diff` shows it immediately; fix it and amend the commit. Nothing later in
the demonstration depends on this commit having any particular shape.

## Segment 2 — The suite, from the tag (about 12 minutes)

DEV-9 — a plan, approved, committed under `plans/`, citing for each step the
clauses it realizes — applies to a test suite exactly as it applies to a module.
A test suite is a build like any other, and §9 of the specification is the thing
it realizes. Show the prompt; the run takes too long to watch:

> Read `SPECS.md` and the process documents. Propose a plan for the test suite
> under `tests/`, one file per source module, that claims every obligation in
> `SPECS.md` §9: for each step, the obligations it claims and the clauses each
> test will cite (VER-6). Wait for my approval. Then write the suite, run the
> gate (VER-4), and report per RPT-5, including which obligations are claimed
> by at least one test and which are not (VER-8). Commit as
> `tests: suite per SPECS 9 (VER-4 green)`.

**Say (of the prompt, briefly):** the prompt asks for the obligations and the
clause citations at *planning* time, before any test is written. That is what
makes the plan reviewable: a reader can check the plan against §9 and see
whether anything is missing, without reading a line of test code.

**Do:**

```sh
git checkout t4-tests-100
ls tests/
grep -c '^def test_' tests/*.py
```

**Do:** open `tests/test_game.py` and read three tests aloud, docstring first in
each case. The docstring is the part that matters; the code is ordinary.

1. `test_check_winner_overline_counts` — the docstring cites §4.1. Nine marks
   are placed in a row by direct assignment to the board, which VER-6 permits
   for setup but not for the behavior under test. There is one call to
   `check_winner`, and the assertion is the clause restated in Python: a run
   longer than five still wins.
2. `test_check_winner_winner_over_tie_precedence` — cites §4.3. The board is
   the tie board with a single cell reopened, and the final move goes through
   `make_move` rather than direct assignment, because the claim being made is
   about what happens when a move is played. Setup may be assigned; behavior
   must be exercised. The expected result is `X`, not `tie`.
3. In `tests/test_computer_ai.py`,
   `test_random_move_always_returns_valid_position_over_many_calls` — cites
   §5.2. It runs a hundred partly filled boards, and the claim it checks is
   membership in `available_moves()`. That is precisely the obligation §9
   states: a property that must hold every time, not a distribution that must
   look uniform. The docstring records why the boards are partly filled — on an
   empty board every position is available, so the test would pass against an
   implementation that ignored `available_moves()` entirely.

Then open `tests/test_main.py` and read the parametrized
`test_prompt_human_rejects_invalid_forms`: eight rejected input forms, one
clause (§6.2), one test function. The clause enumerates the forms and the test
enumerates the same forms in the same order. A reader can hold the two side by
side and check them off.

**Do:** display the completion note captured from rehearsal — the RPT-5 text —
and read its clause-coverage line: which obligations of §9 are claimed by at
least one test, and which are not.

`[fallback capture]` — the RPT-5 completion note.

**Say:** the thing that makes this suite different from an ordinary one is that
every test names the clause it claims. Because each test cites a clause, clause
coverage can be computed by reading the suite — it is AUD-5's traceability
requirement applied to tests rather than to a specification.

That is what §9 exists for. §9 does not describe the game; it lists what the
tests must claim about the game. The suite is the realization of §9 in the same
sense that `game.py` is the realization of §4 and §5.1, and the completion note
is the conformance report for that realization. Every relationship in this
repository has the same three parts: a specification, a realization, and a
verifier that relates them.

**If it goes differently:** if the live suite's completion note lists a clause as
unclaimed — the after-game-over clause is the one that usually turns up — say so
and treat it as the segment's teaching point rather than a failure. Ask for the
test live:

> Add a test citing §5.1's clause that a move after the game is over is
> rejected, run the gate, and report.

If that test fails, the engine does not conform and the specification already
says what it must do, so the sequence is report, ruling, then repair —
DEV-2 (a). Say each of those three steps aloud as it happens.

## Segment 3 — The gate, then sabotage (about 18 minutes)

**Do (shell, at `t4`):**

```sh
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
```

**Say:** read the report across rather than looking only at the percentage.
There are statements, branches, partial branches, a "missing" column that is
empty, a line stating the required coverage, and an exit code of 0. The exit
code is the part the gate acts on.

Point at a single `if` in `make_move` and say what branch coverage adds to line
coverage. The line containing the condition executes whenever the function is
called, so line coverage is satisfied by any test that calls the function at
all. The branch is covered only when both outcomes have occurred, so a rejection
path is covered only if some test supplies input that gets rejected. Branch
coverage forces the suite to exercise the cases the specification distinguishes.

Then:

```sh
grep -n 'pragma' *.py
```

One result, on the `__main__` guard of the entry point, which is the single
pragma VER-5 permits. VER-5 requires that any other unreachable branch be
recorded by amendment before a pragma may be written for it, so that a
suppression is a decision with a record rather than a quiet convenience.

`[fallback capture]` — the green report.

### Step 1 — delete a test

Ask the room before running anything: which single test could be deleted from
this suite with the coverage figure staying at 100%, and why? Give them twenty
seconds.

The answer is any test whose branches some other test already reaches, and the
overline test is the clearest case in this suite. `check_winner` scans fixed
five-cell windows; a row of nine marks matches the first such window and returns
immediately, taking exactly the path a row of five takes. The engine has no
branch anywhere that corresponds to the clause "overlines count" — the clause is
satisfied incidentally by the five-window scan. A clause that has no branch of
its own cannot register in a branch-coverage figure at all.

```sh
# delete test_check_winner_overline_counts from tests/test_game.py (editor)
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
git checkout -- tests/test_game.py
```

**Expected:** green, one test fewer, still 100% branch coverage, exit 0.

**Say, in the fixed one-sentence form:** the gate established that every branch
of the engine is reached by some test, and it did not establish that §4.1's
overline clause is claimed by any test — which it now is not.

**Say (the reason):** branch coverage is a property of the pair (tests, code).
It has no access to the specification and therefore cannot have an opinion about
the pair (tests, specification). The clause "overlines count" is a real
commitment the program makes to its users, and after that deletion nothing in
the repository checks it, while every number on the report stays perfect. This
is what VER-8 exists to prevent: it requires branch coverage and clause coverage
to be reported as two separate figures, because they answer two different
questions.

### Step 2 — flip a direction

```sh
# game.py, the up-right diagonal scan: self.board[r - i][c + i]  ->  self.board[r - i][c - i]
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
```

**Expected:** two failures — the up-right diagonal test and the tie test — and
exit 1. At `t5` the fixture scenario `x-wins-diagonal-down-left` fails as well.

`[fallback capture]` — the red report.

**Say:** the gate returned the work, which is what VER-4 requires it to do.

The second failure deserves about ten seconds, because it is not the one anyone
predicts. The flipped index walks left instead of right, runs off the left edge
of the board, and Python's negative indexing silently wraps it around to the
right edge. The scan then reports a run of five that does not exist anywhere on
the board, so a board that is genuinely tied reports a winner. Nobody wrote a
test for wrapped indices. The tie test caught it because that test claims §4.2,
and §4.2 is simply false of this code now. A test that claims a clause catches
every way of violating that clause, including ways nobody anticipated.

**Do:** ask the agent for the report, and explicitly not for the repair:

> The gate is red. Report per RPT-2 — verifier, specification version, clauses
> checked — and the findings. Do not change anything.

**Expected:** an RPT-2 conformance report naming the verifier (the suite at
commit `t4`, algorithmic), the specification version (`SPECS.md` 1.0.0), the
clauses checked (those the suite cites), two findings citing §4.1 and §4.2 with
the clause text quoted, a verdict, and proposed repairs that have not been
applied (RPT-4).

**Say:** the separation between reporting and repairing is deliberate. An agent
that finds a failure and immediately fixes it has made a decision — which of the
specification and the realization was wrong — and made it silently. Here the
report comes first, a person rules, and only then does anything change.

Rule aloud: the specification is right and the engine is wrong. Then restore:

```sh
git checkout -- game.py
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
```

**Say, in the fixed one-sentence form:** the gate established that the engine no
longer conforms to §4.1 and §4.2 as the suite claims them, and it did not
establish where the fault lay.

**Say (the reason):** a failing test names a broken claim, not a broken line.
Locating the fault took a person reading the failing assertion against the code.
Having read it, that person ruled — the specification stands, the code is wrong —
and the restore was a repair in the sense of DEV-2 (a): report, then ruling, then
the change, in that order, with all three visible in the history.

### Step 3 — a wrong expectation

```sh
git checkout sabotage-wrong-expectation
git diff main --stat
git diff main -- game.py | grep '^[+-] '
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
python -c "from game import Game; print(repr(Game().render().splitlines()[0]))"
git checkout main
```

**Expected:** green, 100%, exit 0 — and the header printed with five leading
spaces.

**Say:** open `SPECS.md` §7.2 and read the clause: four leading spaces. The
rendered board on screen has five. The board is wrong, the test that claims §7.2
is wrong in exactly the same way, and the gate is green with perfect coverage.

Nothing here is exotic. This is what happens whenever a test is written by
reading the code instead of reading the specification, which is the normal way
tests get written when a suite is added to a program that already exists.

The suite is itself a realization — of §7.2, among other clauses — and VER-1
says plainly that a realization can be nonconformant. So the question is who
verifies the verifier. The gate cannot: it compares code against tests, and both
sides agree. A person reading §7.2 can, and so can an agent asked to audit the
suite against §9 and the clauses each test cites. That is the verification-
obligations row of the VER-2 table, and it is a judgment clause, not a
mechanical one.

**Say, in the fixed one-sentence form:** the gate established that the code does
what the tests claim, and it did not establish that the tests claim what the
specification says.

**Say (to close the segment):** put the three verdicts side by side. Every
branch is reached, but no test claims the clause. The code violates a clause the
tests claim, but the gate cannot say where. The code does what the tests claim,
but the tests misread the specification. Three green-or-red signals, three
different limits, and none of them is discoverable from the coverage percentage.

**If it goes differently:** if the test names differ from rehearsal,
`grep -n overline tests/test_game.py` and `grep -n 'r - i' game.py` find the two
edit points. If step 2 comes out green, the bytecode cache is stale: delete
`__pycache__`, rerun, and tell the class what happened rather than moving on —
a verifier that checked something other than the current artifact is itself an
instance of VER-1, and an unplanned one is worth more than a planned one.

## Segment 4 — Reading the history (about 8 minutes)

No agent runs in this segment. There are two things to read, and the point of
both is that a repository's history is evidence about how decisions were made,
not just a record of what the files contain now.

### The completion note, read again

Return to the RPT-5 note from Segment 2. It carries two coverage lines, and they
answer different questions: the gate's line reports branch coverage under VER-4,
and the clause-coverage line reports which of §9's obligations are claimed by at
least one test under VER-8.

Each of the three sabotage steps was a case where one of those lines was
informative and the other was not. Step 1 moved the clause-coverage line and left
branch coverage untouched. Step 2 moved neither line but turned the gate red.
Step 3 moved neither line and left the gate green, because the failure was
outside what either line measures. Two numbers are not redundancy; they are two
different questions, and a third question — does the suite read the
specification correctly — has no number at all.

### The reference's history

In `reference/`:

```sh
grep -n 'game is over' SPECS.md
sed -n '/^## Changelog/,$p' SPECS.md | head -5
grep -A2 'make_move(row, col)' plans/001-engine-opponent-cli.md
grep -n 'winner is not None' game.py
grep -n 'after_game_over' tests/test_game.py
```

The top changelog entry is `1.2.1`, a §2 housekeeping patch that is not relevant
here; the two entries that matter are `1.2.0` and `1.1.0` below it.

**Say:** take these four artifacts in the order they were written.

The reference's `SPECS.md` 1.1.0 was silent on what happens when a move arrives
after the game is over. It listed two reasons `make_move` returns `False` and
stopped there.

The plan is next, and it is the interesting one. Its `make_move` step says it
realizes "each rejection case §5.1 lists" — which it does, faithfully, and there
were two. The plan did not introduce the gap, and no amount of care in writing
the plan could have closed it, because the plan's job is to realize the
specification and the specification did not say. A silence in a specification is
inherited by every artifact derived from it: the plan, then the code, then the
tests that cite the clauses the code claims to satisfy. This is the reason the
audit (DEV-8) runs against the specification before any plan is written, and not
after the code exists.

The engine accepted the move, exactly as the plan described. The suite did not
catch it, because no clause said otherwise and every test cites a clause.

Then 1.2.0 records the ruling, and the engine change and the test citing the new
clause follow it in the history. The order is amendment first, realization
after, which is DEV-2 (c): the intent changed, and the code changed because the
intent did.

**Say (the comparison):** set the three kinds beside one another, all three now
visible in this repository's history.

The flip in Segment 3 was repaired with no change to the specification, after a
report and a ruling — DEV-2 (a). Replacing the 81-cell scan with a check around
the last move would keep every test green and need no amendment, because the
specification never said how the scan works — DEV-2 (b), and the commit message
must state that no specified behavior changed. The after-game-over clause
required the specification to move first — DEV-2 (c).

Three kinds of change to a realization, and in each case the history shows which
kind it was without anyone having to remember.

## Segment 5 — Fixtures, from the tag (about 10 minutes)

Show the prompt; as with the suite, the run is too slow to watch:

> Add `fixtures/scenarios.json` and `fixtures/README.md` as given; they are not
> to be edited (VER-7). Write `tests/test_fixtures.py`: a parametrized loader
> that runs every game scenario and every rejection scenario against the engine
> per the README's loader contract, citing the clauses each scenario verifies.
> Run the gate, report per RPT-5, and commit as
> `fixtures: scenarios.json and loader (VER-7)`.

**Do:**

```sh
git checkout t5-fixtures
head -30 fixtures/scenarios.json
cat tests/test_fixtures.py
pytest tests/test_fixtures.py -q -v | head -20
```

**Say:** look at what the scenario file contains and, more importantly, at what
it does not. Each entry is a sequence of moves in and an expected winner out, or
a rejected move in and no change of state out. There is no Python in it, no
reference to a class or a method name, nothing that ties it to this
implementation or this language.

The loader is two parametrized test functions, one for each kind of scenario.
A loader written in another language would be the same two functions in that
language reading the same file. The scenarios cite clauses the way the tests do
— `x-wins-row-overline` is §4.1's overline clause expressed as a fixture — so the
chain that began in Lecture 03 now runs end to end and can be traced in either
direction: the concept of operations said "five or more"; §4.1 pinned that
overlines count; §9 required an overline case among the obligations; a test
cites §4.1; and a fixture names the same clause in a file that no language owns.

**Do:** open `fixtures/README.md` at the section headed "Known blind spots".

**Say:** there is no tie scenario in this file, deliberately, and the file says
so in writing. That is what VER-7 requires: a fixture set states its assumptions
and its blind spots, because a reader who does not know what a fixture set omits
will assume it omits nothing.

What is not covered here is covered another way — the tie case is verified by a
unit test with a directly constructed board — or it is named as unverified. Both
are acceptable; silently leaving a gap is not.

One further use is worth mentioning, because a later lecture depends on it. The
same file will be run against an engine written in another language. When two
independent implementations of one specification both pass the same fixtures,
the simpler implementation becomes a specification for the more elaborate one,
and the fixture file is the interface between them.

**If it goes differently:** if the agent edits the fixture file to make a test
pass, stop there and use it. Name the rule that was broken (VER-7), say why the
rule exists — a fixture file that bends to accommodate the code it is testing has
stopped being a specification of anything — restore the file, and point out that
the loader, not the fixtures, was the deliverable.

## End of part 2

The repository now holds the test suite, the gate green at 100% branch coverage,
the L04 process set, the fixtures and their loader, and a history in which every
change to the realization is identifiably one of DEV-2's three kinds.

More to the point, the class has seen the limits of the green gate stated three
times in the same form, with a concrete failure behind each statement. Lecture 06
starts from this repository at `t4`.

## Recreating this part yourself (students)

Start from your own `t3`, produced in Exercise 3. Install the L04 process set as
Segment 1 does, then run the Segment 2 prompt in your own session and let it
write a suite against your own `SPECS.md`.

Then perform the three sabotage steps by hand. For each one, write the verdict
in the form the demonstration used: what the gate established, and what it did
not. The form matters — writing "the gate passed" or "the gate failed" is not an
answer to either half of the question.

Finally, compare your suite's clause-coverage line against the obligations listed
in `SPECS.md` §9.5, and account for any obligation your suite does not claim.
Project 1, Part 2 asks for the same work on Reversi, against a specification you
wrote yourself.
