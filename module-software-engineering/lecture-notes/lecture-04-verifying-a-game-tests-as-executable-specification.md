# Lecture 04 — Verifying a Game: Tests as Executable Specification

> Software-engineering module, meeting 4 of 6. Companion reading for the lecture
> and for part 2 of the game demo
> (`../demos/lecture-03-game-demo/demo-script-lecture-04.md`); self-contained.
> Exercise 2 is due at this meeting; Exercise 3 (optional) continues. The
> readings for Lecture 05 are at the end.

## Where we are: an implementation that has not been verified

Lecture 03 ended with a concept of operations, a family of specifications (the
technical specifications in `SPECS.md`, one section per kind), an approved
plan, and three modules — an engine with no input or output, a computer
opponent, and an entry point that owns every prompt. We verified them by
playing one move each way. That is a human verifier with a scope of two moves,
and nothing in the repository records what was checked.

Recall from Lecture 01 that there are three kinds of verifier, and note that
they apply to code exactly as they applied to notes:

- A **human verifier** reads the code against the specification, clause by
  clause.
- An **agent verifier** is asked to check and report (our reporting rule RPT-2
  gives the form of the report).
- An **algorithmic verifier** is a program that decides clauses. For a program,
  the algorithmic verifier is a test suite run by a test runner, together with
  a coverage tool that measures what the suite reached and, where a language
  has one, a type checker.

The columns of the table in our verification rule VER-1 do not change — cost
per check, whether repeating the check gives the same result, which clauses
each kind can decide, whether the result can stand in front of a commit. A
test suite is the algorithmic verifier we build in this lecture, and the
question we ask about it is the one Lecture 01 asked about the note verifier
`check_notes.py`: what does its result establish, and who verifies the
verifier?

## Extending the process documents before writing any tests

At the start of this lecture the process set is the Lecture 03 set:
`verification.md` has four rules. They say what the kinds of verifier are
(VER-1), which clauses are mechanical and which need judgment (VER-2), when
verification runs (VER-3), and what the gate is (VER-4). They do not say what
coverage the gate demands, how a test must be written, what a fixture is, or
how coverage is to be reported. If we wrote the suite first, it would be
written to no standard, and we would be tempted to fit the standard to the
suite afterwards.

So the lecture's first operation is an amendment to the process documents:
VER-5 through VER-8 are added to `verification.md` (version 1.2 to 1.3); the
completion-note rule RPT-5 is extended in `reporting.md` (1.2 to 1.3); the map
in `process/README.md` is updated (1.1 to 1.2); and the loader `CLAUDE.md` is
updated for a repository that has code and tests. The amendment is proposed in
the form our reporting rule RPT-3 prescribes, approved, applied, and committed
with a changelog entry, as our development rule DEV-3 requires.

**Important**: a process document changes by the same mechanism it prescribes
for a specification — a proposal, an approval, a version, a changelog entry.
And we do it *before* writing the suite for the same reason a specification
precedes its realization: the rules the suite must follow have to be in force
before the suite exists.

## Tests as executable specifications

A test is a claim about a clause of the specification, written in a form a
program can check (the catalog of specification kinds,
`../../specification-kinds.md`, has a *test suite* entry for this). Our
verification rule VER-6 says how such a claim must be written. Here it is line
by line.

**Every test cites the clause it verifies.** In the docstring or an adjacent
comment, for example `SPECS §4.1: overlines (6+) count as a win.` This is the
traceability property of Lecture 01 (audit rule AUD-5) applied to tests. It is
what makes the chain of identifiers from Lecture 03 run through the suite: the
concept of operations says "five or more"; §4.1 says overlines count; §9
requires an overline case; the test names §4.1.

**Tighter, never looser.** The specification is the floor. A test may assert
more than the clause — that `check_winner` returns the winner *and* sets the
`winner` attribute — but never less. A test that accepts something the clause
forbids is a looser realization of the clause, and a suite containing it will
pass an engine that does not conform.

**Direct assignment for setup only.** The overline test places nine marks with
`g.board[3][c] = 'X'` and then calls `check_winner` once. The claim is about
`check_winner`; how the board came to hold nine marks is setup, and setup may
bypass the public operation. The precedence test (§4.3) opens one cell in a
tied board by assignment and then makes the final move through `make_move`,
because the claim is about a move. The question that decides which is which
is: *what does this test claim?*

**A test that cannot fail is not a test.** The 3-by-3 suite this course once
used had a test that seeded the random generator and asserted that two calls
agreed. It re-asserted its own setup, could not fail when the strategy
regressed, and was removed by an audit. A test counts only if some
nonconforming realization would fail it.

**One file per source module, under `tests/`.** This lets us read clause
coverage off the suite file by file.

One clause often has many realizations, and a parametrized test states them in
one place. Section 6.2 of the specification lists the rejected forms of a move
entry — wrong length, a non-digit, a `0`, an occupied cell. The reference's
test `test_prompt_human_rejects_invalid_forms` is one function with eight
inputs. The clause enumerates the forms; the test enumerates the same forms;
reading one against the other is an audit of the test.

Recall that `SPECS.md` §9 is the list of **verification obligations** (audit
rule AUD-14): what the tests must claim about this game, category by
category — every direction of win, at least one overline, the tie, precedence,
every rejected input form, every menu branch, the byte-exact board in three
states, the random opponent's result always among the available moves on a
partly filled board. The suite is the realization of §9, and the completion
note the agent gives when the suite is committed (RPT-5) is its conformance
report. Since version 1.3 of `reporting.md`, that note has two coverage lines:
the gate's figure, and which obligations are claimed by at least one test and
which are not (VER-8).

Note that the prompt that produces the suite is a DEV-9 prompt, because a
suite is a build: a plan under `plans/` that names, for each step, the
obligations it claims and the clauses each test will cite; approval; the
suite; the gate; the completion note; a named commit. The suite takes the agent
longer than a lecture can wait, so in class we read three of its tests from
the tag and read the completion note's clause-coverage line.

## Running the gate, then breaking things on purpose

The gate (VER-4) is one command:

```
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100
```

It exits 0 when every test passes and branch coverage is 100%; anything else
is a non-zero exit, and a non-zero exit returns the work. The report lists,
per module, statements, branches, partial branches, the percentage, and the
lines and branches not reached. Branch coverage is stricter than line coverage
in one way that matters here: an `if` in `make_move` is *executed* whenever
the function runs, but its rejection branch is *covered* only when some test
rejects. A suite that only ever plays legal moves can reach every line of
`make_move` and only half of its branches.

Our verification rule VER-5 fixes the target at 100% branch coverage over
every source module and permits one `# pragma: no cover`, on the entry point's
`if __name__ == "__main__":` guard, which a test runner that imports the module
cannot execute. Any other branch that is genuinely unreachable is recorded by
an amendment to `verification.md`, naming the branch and saying why, before a
pragma is added. The reference implementation carries exactly one pragma.

The demo runs the gate green, and then we break the (tests, code) pair three
ways. After each step we state one sentence: what the gate established, and
what it did not.

**Step 1 — delete a test.** We delete the overline test. The gate is green, one
test fewer, 100%. The gate established that every branch of the engine is
reached by some test. It did not establish that §4.1's overline clause is
claimed by any test — it is not, now. Branch coverage is a property of the
pair (tests, code). It says nothing about the pair (tests, specification).

**Step 2 — flip a direction.** In the engine's up-right diagonal scan, we
change `self.board[r - i][c + i]` to `self.board[r - i][c - i]`. The gate is
red: the up-right diagonal test fails, and so does the tie test, which nobody
expected. The flipped index runs off the left edge, a negative index in Python
wraps to the right edge, and the scan reports a line that is not on the
board — so a tied board reports a winner. The tie test caught it because it
claims §4.2, and §4.2 is now false of this code. We ask the agent for the
report, not the repair (RPT-2, then RPT-4): the verifier, the specification
version, the clauses checked, two findings with the clause text quoted, a
verdict. The ruling is that the specification is right; the restore is the
repair. The gate established that the engine no longer conforms to §4.1 and
§4.2 *as the suite claims them*. It did not establish where the fault was; a
person read the failing assertion and the code and ruled.

**Step 3 — a wrong expectation.** On a scratch branch, the rendered board's
header has five leading spaces instead of four, and the two expected-board
constants in the test file have the same five. The gate is green, 100%. Open
§7.2: "4 leading spaces." The code is wrong; the test that claims §7.2 is wrong
in the same way; the gate cannot tell. The suite is itself a realization of
§7.2, and a realization can be nonconformant (VER-1). The gate established
that the code does what the tests claim. It did not establish that the tests
claim what the specification says.

So who verifies the verifier? A reader of §7.2 — a person, or an agent asked
to audit the suite against §9 and the clauses each test cites. That is the
verification-obligations row of the VER-2 table: partly algorithmic (the
suite's presence per category), and for the rest, judgment.

| Step | Gate | Established | Not established |
|---|---|---|---|
| delete the overline test | green | every branch of the engine is reached | that §4.1's overline clause is claimed by any test |
| flip the up-right scan | red | the engine fails what the suite claims about §4.1 and §4.2 | where the fault is; a person ruled |
| wrong code, wrong expectation | green | the code does what the tests claim | that the tests claim what §7.2 says |

## Why coverage is not conformance

Our verification rule VER-8 states the distinction the three steps showed.
**Branch coverage** is a property of (tests, code): which code the suite
reaches. **Clause coverage** is a property of (tests, specification): which
clauses at least one test claims. The two are reported separately — the gate
reports the first; the completion note reports the second against §9 and names
the clauses that remain for a human or agent verifier.

The VER-2 table of the Lecture 04 process set says, kind by kind, what the
algorithmic verifier decides and what remains for a person or an agent:

| Clauses | Algorithmic | Human or agent |
|---|---|---|
| board and coordinates; rules of play; win and tie | unit tests on the engine | — |
| display format | golden-string tests | — |
| input grammar; interaction flow | scripted-input tests | — |
| interface contract | unit tests; a type checker where used | — |
| example session | an end-to-end scripted run | — |
| verification obligations | partly — the suite's presence per category | that each obligation is actually claimed by a test |
| `CONOPS.md` policies and scenarios | — | validation by playing each scenario |

The last two rows are the ones a green gate says nothing about, and step 3
lives in the second-to-last row.

Recall the three scope lines of a conformance report (RPT-2). They apply to a
test run as they applied to a note check. The verifier is the suite at a named
commit, algorithmic; the specification is `SPECS.md` at a stated version; the
clauses checked are the ones the suite cites, and the clauses not checked are
the rest. A green run reported without those three lines is just a number.
With them, it is evidence within a scope, and it can be trusted for what it
claims and no further.

Lecture 01 listed six ways a verification result can be invalid. Each has a
form for a test suite:

| Lecture 01 | For a test suite |
|---|---|
| a defective specification | a test written from an inconsistent clause verifies the inconsistency; this is why the audit runs first (DEV-8) |
| clauses not decided | obligations no test claims — the overline clause after step 1; the completion note's second line exists to name them |
| the verifier mis-implements a clause | the wrong expected string of step 3 |
| checking from memory | a suite written from the agent's recollection of §7.2 rather than from the file — the same failure as step 3 with a different cause; our development rule DEV-1 exists to prevent it |
| attention | the person who read the two failures of step 2 and ruled; the person who reads a constant against §7.2 |
| the wrong version of the specification | tests citing §4.1 as it stood before an amendment, still green after it; VER-3 re-checks everything an amendment touches |

We also saw, in one lecture, all three kinds of change to a realization that
our development rule DEV-2 distinguishes, and what the history must show for
each:

- **(a) Repair.** The flipped scan restored. No specification change; a report
  (RPT-2) and a ruling (DEV-4) precede the change.
- **(b) Conformance-preserving change.** Replacing the 81-cell scan with a
  check around the last move. Every test stays green; no amendment is needed;
  the commit message must say that no specified behavior changed.
- **(c) Change of specified behavior.** A move after the game is over. The
  reference implementation was built from a specification that was silent on
  this point, and its engine accepted such a move. Its `SPECS.md` 1.2.0 adds
  the clause to §5.1 and records the ruling; the engine change and the test
  citing the clause follow the amendment. The history reads amendment, then
  realization. In the demo's own repository the clause was ruled in Lecture 03
  and is in `SPECS.md` 1.0.0 already, so there the question at `t4` is only
  whether a test claims it — the completion note's clause-coverage line
  answers.

**Important**: these three kinds are a general pattern for keeping a
realization conformant while it changes. Before any change to code, we ask
which kind it is, because the answer says what has to happen first: a report
and a ruling, nothing, or an amendment.

## Fixtures: executable specifications that outlive the code

`fixtures/scenarios.json` is a list of scenarios. A game scenario names a
sequence of moves and the expected winner after the last one — `"X"`, `"O"`,
or `null`. A rejection scenario names setup moves, an attempt, and nothing
else: the attempt must be rejected and must leave the board and the turn
unchanged. The file says nothing about Python. A loader turns each scenario
into a test — in the reference, two parametrized functions, one per kind of
scenario — and a loader in another language is the same two functions in that
language. The catalog's *fixtures* entry gives this kind in general; the file's
shape is itself a data format, which the Project 1 brief fixes in its §3.1.

Our verification rule VER-7 says what the file is and how it is treated. It is
an executable specification, derived from the rules of play and the interface
contract, that any implementation of the specification must reproduce. It is
never edited to make a test pass: an expectation that looks wrong is a finding
about the pair (fixture, specification), reported as a gap (RPT-1) for a
ruling (DEV-4). And it states the rules it assumes and its blind spots. The
reference's fixture README names two blind spots: there is no tie scenario,
because a full board with no five in a row is hard to construct by hand, and
there is no after-game-over rejection. Each is verified another way — a unit
test with a constructed board — and the README says so. Note that a blind spot
is part of the fixture set's contract with its users, not a defect; the defect
would be a blind spot the file does not admit.

The scenarios cite clauses the way tests do. `x-wins-row-overline` is §4.1's
overline clause as eleven moves; `four-in-a-row-is-not-a-win` is the same
clause from the other side; the four rejections are §5.1's `False` cases. The
chain from Lecture 03 now runs end to end: concept of operations, rule,
obligation, test, fixture — one intent, five statements, one identifier.

The course's catalog of specification kinds records, for every kind, whether
it survives a change of programming language — the *survives a port?* column
of its summary table — and this lecture has now met the two kinds that answer
differently. The concept of operations, the rules, the display format, the input grammar, the
example session, and the fixtures survive unchanged; the interface contract
and the tests are re-expressed for each language. A later lecture ports the
engine to a different programming language, and the fixture file is the third
artifact both implementations answer to. When two realizations of one
specification both pass the same fixtures, the plain one becomes the
specification for the clever one — the obvious 81-cell scan is the oracle for
the last-move check — and DEV-2 (b) is the rule the clever one is held to.

## What is new in the process documents

| Rule | Says | Used today |
|---|---|---|
| VER-5 | 100% branch coverage; one pragma, on the `__main__` guard; an unreachable branch is recorded by amendment before any pragma | the gate; the pragma count |
| VER-6 | every test cites its clause; tighter never looser; direct assignment for setup only; no test that cannot fail; one file per module | the three tests read aloud; the parametrized forms |
| VER-7 | a fixture file is never edited to pass; it states its assumptions and blind spots | `fixtures/scenarios.json` and its README |
| VER-8 | branch coverage and clause coverage are reported separately | steps 1 and 3; the completion note's second line |
| RPT-5 (1.3) | the completion note reports clause coverage against §9 when the verifier is a suite | the note read in the demo |
| DEV-2 | three kinds of realization change, and what the history shows for each | the flip, the last-move check, the after-game-over clause |

## Looking ahead: what Reversi will demand of each kind of specification

Lecture 05 hands you a sketch of a different game and asks for the same moves.
The specification-family table, unfilled, is the checklist; here is one line
on what each kind will have to say.

| Kind | Reversi will have to say |
|---|---|
| concept of operations | what a player observes: a move flanks and flips; a player with no move passes; the game ends when neither can move |
| rules of play | the opening position; who moves first; flips in all eight directions; the pass; the end condition; the count |
| display format | whether legal moves are shown — a display decision, not a rule |
| input grammar | how a pass is entered, if it is entered at all |
| interaction flow | a forced pass announced; two passes in a row end the game |
| interface contract | the flips as a postcondition of a move; what a move returns when it flips nothing |
| example session | one game with at least one pass |
| verification obligations | a pass scenario and an early-end scenario among the fixtures |

## Questions to think about

1. After the overline test is deleted the gate is green. What, exactly, is
   still verified about §4.1 — which of its sentences does some remaining test
   claim — and what is not?
2. The fixtures have no tie scenario, on purpose. Is that a defect in the
   specification, in the realization, or in the verifier? What does VER-7 say
   a fixture file owes you instead, and where in the reference is the tie
   clause verified?
3. Classify under DEV-2: replacing the 81-cell scan with a check around the
   last move; fixing tie-versus-win precedence in an engine that declared a
   tie on a full board with a line; adding the after-game-over rejection to an
   engine whose specification was silent. Which needs an amendment first, and
   what does each commit message have to say?

## Before next meeting

- Read the Project 1 brief (`../project-1-reversi-brief.md`) in full, and the
  Reversi concept-of-operations sketch
  (`../student-materials/reversi-starter/CONOPS-sketch.md`) as a player, not an
  implementer — five minutes. Do not read the rules of Reversi elsewhere;
  Lecture 05 learns them from the sketch, and the gaps in it are the point.
- Exercise 3 (optional) continues; its second part is the suite and the gate
  on your own `t3`.
