# Game demo, part 2 (Lecture 04) — tests, the gate, and fixtures

Part 2 of the demonstration that began in Lecture 03. Part 1 ended at `t3`: a
concept of operations, a behavioral contract of several kinds, an approved plan,
and three modules, verified only by playing one move each way. Part 2 puts the
realization under an algorithmic verifier: a test suite whose every test cites
the clause it claims, a coverage gate that runs before every commit, and a
fixture file that outlives the code. It then shows, three times, what a green
gate does and does not establish.

**A caution that governs the whole script.** Do not depend on the agent making
one specific move. The *Expected* notes describe the usual shape; every segment
has an *If it goes differently* note; rehearse once and capture at every
`[fallback capture]` marker. The test suite (`t4`) and the fixture loader (`t5`)
each take the agent more than two minutes to produce, so in class they are
shown from the tag. The live time goes to the process amendment, the three
sabotage steps, and the reading of reports.

## What part 2 starts from, and what is known in advance

The repository at `t3-engine`: `CONOPS.md` 1.0, `SPECS.md` 1.0.0, the approved
plan under `plans/`, `game.py`, `computer_ai.py`, `main.py`, `BACKLOG.md`, the
loader, and `process/` at the **L03** level — `verification.md` 1.2 (VER-1 to
VER-4), `reporting.md` 1.2, `README.md` 1.1. No tests. Nothing in `process/` yet
says what coverage the gate requires or how a test must be written.

`reference/` is the destination, `t5`: `SPECS.md` 1.2.0, the engine, the suite
(85 unit tests plus a 14-scenario fixture loader), `fixtures/`, and the L04
`process/`. Its history is not the live repository's history — see the
paragraph on the after-game-over clause below.

The three sabotage steps of Segment 3 have known outcomes. They were run
against `reference/` on 2026-09-22 in a venv with `pytest-cov`; the numbers are
the reference's, and a live suite's counts differ.

| Step | Edit | Gate | What it shows |
|---|---|---|---|
| 1 | delete `test_check_winner_overline_counts` | **green**; 100% branch; one test fewer | branch coverage is a property of (tests, code); the clause §4.1 "overlines count" is no longer claimed by any test (VER-8) |
| 2 | in `game.py`, in the up-right diagonal scan, `self.board[r - i][c + i]` → `self.board[r - i][c - i]` | **red**; two failures: `test_check_winner_diagonal_up_right` and `test_check_winner_detects_tie`; the fixture scenario `x-wins-diagonal-down-left` also fails at `t5` | the gate returns the work (VER-4, RPT-4). The tie test fails because the flipped index runs off the left edge and Python's negative index wraps to the right edge: the scan reports a line that is not on the board |
| 3 | on a scratch branch: five leading spaces instead of four in `render`'s header **and** in the two expected-board constants in `tests/test_game.py` | **green**; 100% branch | a test whose expectation is wrong passes code that is wrong. The verifier is a realization of §7.2 and can be nonconformant (VER-1); the gate cannot see it; a reader of §7.2 can |

**The after-game-over clause.** Lecture 03's round 2 ruled that a move after
the game is over is rejected with no change of state (`SPECS.md` 1.0.0, §5.1,
AUD-12), and the plan at `t3` realizes that specification. The reference
implementation was built earlier, from a specification that was silent on the
point: its `SPECS.md` 1.1.0 lists two reasons `make_move` returns `False`, and
its engine accepted a move after a win. Version 1.2.0 of the reference adds the
clause, and the engine change and the test citing the clause follow the
amendment — the history reads amendment, then realization, which is DEV-2 (c).
Segment 4 shows that history from `reference/`. In the live repository the
question to ask at `t4` is different: does the completion note's clause-coverage
line (VER-8) list §5.1's after-game-over clause as claimed by a test? If not,
that is the clause to add a test for, live.

## Before class — setup checklist

1. Start from the rehearsal repository at `t3-engine`
   (`git checkout t3-engine` in `~/game-demo`, or a fresh copy of it). Rehearse
   the whole of part 2 once, and tag: `t4-tests-100` after Segment 2,
   `t5-fixtures` after Segment 5.
2. A venv with `pytest` and `pytest-cov` installed, activated in the demo
   shell, and the gate confirmed green at `t4` and `t5` on the presentation
   machine that day. The pipx-installed `pytest` used in planning does not have
   `pytest-cov`; the gate fails to parse `--cov` without it.
3. In the demo shell, `export PYTHONDONTWRITEBYTECODE=1` and delete every
   `__pycache__` directory. Sabotage step 2 changes one character and leaves the
   file size unchanged; a bytecode cache compiled in the same second as the edit
   is not invalidated, and the flipped scan then passes every test. This
   happened once in rehearsal.
4. The scratch branch for step 3, made at rehearsal from `t4`:

   ```sh
   git checkout -b sabotage-wrong-expectation t4-tests-100
   # game.py: header = "     " + ...   (five spaces)
   # tests/test_game.py: the first line of EMPTY_BOARD and MID_GAME_BOARD, five spaces
   git commit -am "scratch: wrong expectation, wrong code" && git checkout main
   ```

5. The names of the overline test and the up-right scan line noted from
   rehearsal; if `t4` is regenerated the names may differ.
6. The amendment proposal (below) in a text file; the four L04 files ready to
   copy from `reference/CLAUDE.md` and `reference/process/` (`README.md`,
   `reporting.md`, `verification.md`) — these three and the loader are the whole
   difference between the L03 and L04 process sets.
7. `fixtures/scenarios.json` and `fixtures/README.md` ready to copy from
   `reference/fixtures/`.
8. Claude Code started in the live repository; two terminals, large font; the
   prompts in a text file; captures at every `[fallback capture]` marker.

## The amendment proposal, pre-written (RPT-3)

Show this; do not type it. It is what the agent would produce if asked to
propose the L04 rules, and writing it in advance saves eight minutes.

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

**Do (shell):** `git log --oneline | head -5`; `grep '^### VER' process/verification.md`.

**Say:** four rules, VER-1 to VER-4. The suite that is about to be written
needs rules that do not exist yet: what coverage the gate demands, how a test
must be written, what a fixture is. A process document is amended the way a
specification is — a proposal, an approval, a version, a changelog entry
(DEV-3). Show the proposal for thirty seconds.

**Do:** approve it aloud, then install the four files and show the diff:

```sh
cp <reference>/CLAUDE.md CLAUDE.md
cp <reference>/process/README.md <reference>/process/reporting.md <reference>/process/verification.md process/
git diff --stat
git diff process/verification.md | grep '^[+-]' | grep -i 'changelog\|^+- \*\*1.3' 
git add -A && git commit -m "process: verification 1.2 -> 1.3 (VER-5..8); reporting 1.3; README 1.2"
```

`[fallback capture]` — `git diff --stat` and the changelog lines.

**Say:** nothing in `SPECS.md` changed. The rules that govern the rules changed
by the same mechanism the rules govern. Three of the four new rules the class
will watch being applied in the next forty minutes.

**If it goes differently:** if the copy is wrong or a file is missed, `git
diff` shows it; fix it and amend the commit. Nothing later depends on the
commit's exact shape.

## Segment 2 — The suite, from the tag (about 12 minutes)

DEV-9 applies to a test suite as it does to a module. Show the prompt, not the
run:

> Read `SPECS.md` and the process documents. Propose a plan for the test suite
> under `tests/`, one file per source module, that claims every obligation in
> `SPECS.md` §9: for each step, the obligations it claims and the clauses each
> test will cite (VER-6). Wait for my approval. Then write the suite, run the
> gate (VER-4), and report per RPT-5, including which obligations are claimed
> by at least one test and which are not (VER-8). Commit as
> `tests: suite per SPECS 9 (VER-4 green)`.

**Do:** `git checkout t4-tests-100`; `ls tests/`; `grep -c '^def test_' tests/*.py`.

**Do:** open `tests/test_game.py` and read three tests aloud, docstring first:

1. `test_check_winner_overline_counts` — the docstring cites §4.1; nine marks
   in a row placed by direct assignment (setup, VER-6); one call to
   `check_winner`; the assertion is the clause.
2. `test_check_winner_winner_over_tie_precedence` — cites §4.3; the tie board
   with one cell opened; the final move goes through `make_move` because the
   claim is about a move (behavior, not setup); the winner is `X`, not `tie`.
3. In `tests/test_computer_ai.py`,
   `test_random_move_always_returns_valid_position_over_many_calls` — cites
   §5.2; a hundred partly filled boards; the claim is membership in
   `available_moves()`, which is the obligation §9 states — a property, not a
   distribution. The docstring says why an empty board would prove nothing.

Then `tests/test_main.py`, the parametrized `test_prompt_human_rejects_invalid_forms`:
eight rejected forms, one clause (§6.2), one test function. The clause lists
the forms; the test lists the same forms.

**Do:** show the completion note from rehearsal (the RPT-5 text, captured), and
read its clause-coverage line: the obligations of §9 claimed by at least one
test, and the ones not claimed.

`[fallback capture]` — the RPT-5 note.

**Say:** every test names the clause it claims, so clause coverage can be read
off the suite (AUD-5 applied to tests). That is what §9 is for: it lists what
the tests must claim about this game; the suite is the realization of §9, and
the completion note is its conformance report.

**If it goes differently:** if the live suite's completion note lists a clause
as unclaimed — the after-game-over clause is the usual one — say so, and ask
for the test live: "Add a test citing §5.1's clause that a move after the game
is over is rejected, run the gate, and report." If the test fails, the engine
is repaired after the report and the ruling (DEV-2 (a)); the specification
already says what the engine must do.

## Segment 3 — The gate, then sabotage (about 18 minutes)

**Do (shell, at `t4`):**

```sh
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
```

**Say:** read the report: statements, branches, partial branches, the missing
column empty, the required-coverage line, exit 0. Point at one `if` in
`make_move` and say what branch coverage adds to line coverage: the line runs
whenever the function runs; the branch is covered only when both outcomes
occur, so a rejection path needs a test that rejects. Then
`grep -n 'pragma' *.py`: one, on the `__main__` guard, the only one VER-5
permits.

`[fallback capture]` — the green report.

**Step 1 — delete a test.** Ask the room first: which single test could be
deleted with the coverage figure unchanged, and why? Then:

```sh
# delete test_check_winner_overline_counts from tests/test_game.py (editor)
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
git checkout -- tests/test_game.py
```

**Expected:** green; one test fewer; 100%.

**Say, in one sentence:** the gate established that every branch of the engine
is reached by some test, and it did not establish that §4.1's overline clause
is claimed by any test — it is not, now — because branch coverage is a
property of the pair (tests, code) and says nothing about the pair (tests,
specification) (VER-8).

**Step 2 — flip a direction.**

```sh
# game.py, the up-right diagonal scan: self.board[r - i][c + i]  ->  self.board[r - i][c - i]
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
```

**Expected:** two failures — the up-right diagonal test, and the tie test — and
exit 1. (At `t5` the fixture scenario `x-wins-diagonal-down-left` fails too.)

`[fallback capture]` — the red report.

**Say:** the gate returned the work. The second failure is worth ten seconds:
the flipped index runs off the left edge, Python's negative index wraps to the
right edge, and the scan reports a line that is not on the board, so a tied
board reports a winner. Nobody wrote a test for that; the tie test caught it
because it claims §4.2 and §4.2 is now false of this code.

**Do:** ask the agent for the report, not the repair:

> The gate is red. Report per RPT-2 — verifier, specification version, clauses
> checked — and the findings. Do not change anything.

**Expected:** an RPT-2 report: verifier (the suite at commit `t4`, algorithmic),
`SPECS.md` 1.0.0, clauses checked (those the suite cites), two findings citing
§4.1 and §4.2 with the clause text quoted, a verdict, repairs proposed, none
applied (RPT-4).

**Say:** rule aloud — the specification is right; the engine is wrong — and
restore:

```sh
git checkout -- game.py
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
```

**Say, in one sentence:** the gate established that the engine no longer
conforms to §4.1 and §4.2 as the suite claims them, and it did not establish
where the fault was — a person read the failing assertion and the code, ruled,
and the restore was a repair (DEV-2 (a)): report, ruling, then the change.

**Step 3 — a wrong expectation.**

```sh
git checkout sabotage-wrong-expectation
git diff main --stat
git diff main -- game.py | grep '^[+-] '
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100; echo "exit: $?"
python -c "from game import Game; print(repr(Game().render().splitlines()[0]))"
git checkout main
```

**Expected:** green; 100%; the header printed with five leading spaces.

**Say:** open `SPECS.md` §7.2: "4 leading spaces". The rendered board is wrong;
the test that claims §7.2 is wrong in the same way; the gate is green. The suite
is itself a realization of §7.2, and a realization can be nonconformant
(VER-1). Who verifies the verifier? Not the gate. A reader of §7.2 — a person,
or an agent asked to audit the suite against §9 and the clauses it cites — the
verification-obligations row of the VER-2 table.

**Say, in one sentence:** the gate established that the code does what the
tests claim, and it did not establish that the tests claim what the
specification says.

**If it goes differently:** if the test names differ from rehearsal, `grep -n
overline tests/test_game.py` and `grep -n 'r - i' game.py` find the two edit
points. If step 2 passes green, the bytecode cache is stale: delete
`__pycache__`, rerun, and say what happened — it is an instance of a verifier
checking something other than the current artifact (VER-1).

## Segment 4 — Reading the history (about 8 minutes)

No agent in this segment. Two things to read.

**The completion note again.** The RPT-5 note from Segment 2 has two coverage
lines, and they answer different questions: the gate's line (branch coverage,
VER-4) and the clause-coverage line (which obligations are claimed, VER-8). The
three sabotage steps were each a case where one line was informative and the
other was not.

**The reference's history.** In `reference/`:

```sh
grep -n 'game is over' SPECS.md
sed -n '/^## Changelog/,$p' SPECS.md | head -4
grep -n 'winner is not None' game.py
grep -n 'after_game_over' tests/test_game.py
```

**Say:** the reference's 1.1.0 was silent on a move after the game is over, and
its engine accepted one. The 1.2.0 entry records the ruling and says the engine
change follows the amendment. The history reads amendment, then realization:
DEV-2 (c). Set beside it: the flip in Segment 3 was repaired with no change to
the specification — DEV-2 (a); and replacing the 81-cell scan with a check
around the last move would keep every test green and need no amendment —
DEV-2 (b), which the commit message must say. Three kinds of change to a
realization, and the history shows which each was.

## Segment 5 — Fixtures, from the tag (about 10 minutes)

Show the prompt:

> Add `fixtures/scenarios.json` and `fixtures/README.md` as given; they are not
> to be edited (VER-7). Write `tests/test_fixtures.py`: a parametrized loader
> that runs every game scenario and every rejection scenario against the engine
> per the README's loader contract, citing the clauses each scenario verifies.
> Run the gate, report per RPT-5, and commit as
> `fixtures: scenarios.json and loader (VER-7)`.

**Do:** `git checkout t5-fixtures`; `head -30 fixtures/scenarios.json`;
`cat tests/test_fixtures.py`; `pytest tests/test_fixtures.py -q -v | head -20`.

**Say:** the file is a list of scenarios: moves in, expected winner out;
rejections in, no change out. It says nothing about Python. The loader is two
parametrized tests, one per kind of scenario, and a loader in another language
is the same two functions in that language. The scenarios cite
clauses the way the tests do — `x-wins-row-overline` is §4.1's overline clause
as a fixture — so the chain from Lecture 03 now runs end to end: the concept of
operations said "five or more"; §4.1 says overlines count; §9 requires an
overline case; a test cites §4.1; a fixture names it.

**Do:** open `fixtures/README.md` at "Known blind spots".

**Say:** no tie scenario, on purpose, and the file says so. A fixture set's
blind spots are part of its contract (VER-7): what it does not cover is
verified another way — here, a unit test with a constructed board — or named
as unverified. The same file will run against an engine in another language in
a later lecture; when two implementations of one specification both pass the
same fixtures, the plain one becomes the specification for the clever one.

**If it goes differently:** if the agent edits the fixture file, stop and say
which rule that broke (VER-7); restore it; the loader is the deliverable.

## End of part 2

The repository holds the suite, the gate green at 100% branch, the L04 process
set, the fixtures, and a history in which every change to the realization is
one of DEV-2's three kinds. Lecture 06 starts from `t4`.

## Recreating this part yourself (students)

From your own `t3` (Exercise 3), install the L04 process set as Segment 1 does
and run the Segment 2 prompt in your own session. Then do the three sabotage
steps by hand and write the one-sentence verdict for each: what the gate
established, and what it did not. Compare your suite's clause-coverage line
with the reference's obligations in `SPECS.md` §9.5. Project 1, Part 2 asks for
this on Reversi.
