# Project 1 — Reversi, Specification-First

> **Assigned:** Lecture 05 · **Due:** one week after Lecture 05 *(date:
> instructor to fix)* · **Effort:** ≈ 9–12 h *(unvalidated until the reference
> solution exists)*
>
> **Requires:** Claude Code, Python 3.11+, git, `pytest` with `pytest-cov`.
>
> **Status:** draft; instructor review required before assigning (date, effort
> estimate).

## 0. What this project is

Someone wants a text-based Reversi and has written down their general idea as a
sketch of a concept of operations. That sketch, a `CLAUDE.md`, a `process/`
folder, and the configuration of a coverage gate are everything you receive.
There is no specification, no code, no tests.

You will do to Reversi what Lectures 03 and 04 did to five-in-a-row
tic-tac-toe, in the order the demo repository's tags follow: `t0` the sketch,
`t1` the concept of operations, `t2` the family of specifications, `t3` the
plan and the engine, `t4` the tests and the gate, `t5` the fixtures. §2 is that
sequence as seven steps. Each step names what you do, the prompt you type, the
process rules that govern it, where the lectures performed it, and the artifact
of the reference game that shows what the result looks like. Lecture 05 walks
through the steps in this order and opens the reference artifact at each one,
so that you know what finished looks like before you start. The method is the
same; the game is harder in ways that make each kind of specification earn its
place (§4).

Phase 1 is the whole of this brief. Later stages of Project 1 — persistence, a
web layer, a port to another language proven equivalent by shared fixtures, an
MCP server — build on what you produce here. Read Stages B–E of the project
unit's brief (`../weeks-04-07/project-1-brief.md`) with "Reversi" in place of
"tic-tac-toe"; they are otherwise unchanged. Lecture 06 launches nothing new;
it previews Stage E, an MCP server over the engine you produce here.

## 1. What you get

| File | What it is |
|---|---|
| `student-materials/reversi-starter/CONOPS-sketch.md` | The client's general idea, in the Lecture 02 skeleton with sections 2, 3, and 6 omitted (no existing system). Incomplete on purpose; it contains at least one internal tension. |
| `student-materials/reversi-starter/CLAUDE.md` | The loader: the governing documents in authority order, the process files, two bootstrap rules, the commands. |
| `student-materials/reversi-starter/process/`, `…/BACKLOG.md` | How development proceeds with respect to the specifications — `development-rules.md` (DEV), `spec-audit.md` (AUD), `conops-audit.md` (AUDCON), `verification.md` (VER), `reporting.md` (RPT), and the invariant in `process/README.md` — identical to the reference game's. DEV-8 makes the audit a standing law; DEV-9 makes the plan one; `BACKLOG.md` is where deferred questions go (DEV-6). |
| `…/.coveragerc`, `…/pytest.ini`, `…/requirements-dev.txt`, `…/.gitignore` | The gate's configuration, the same as the reference's: branch coverage over every module in the repository root, whatever your module split; tests and the virtual environment excluded; the `__main__` guard excluded by pattern (VER-5). Adopted, not authored, like `process/`. |

**The worked example.** The in-class demo repository is a tic-tac-toe built by
the same method, and its tags name the states this brief's steps reach:

| Tag | Step | What exists at that state |
|---|---|---|
| `t0-conops-sketch` | 0 | the sketch, the loader, `process/`, `BACKLOG.md` — `demos/lecture-03-game-demo/starter/` |
| `t1-conops` | 1 | `CONOPS.md` 1.0 |
| `t2-spec-family` | 2 | `SPECS.md` 1.0.0 |
| `t3-engine` | 3 | `plans/001-engine-opponent-cli.md`; the engine, the opponent, the entry point |
| `t4-tests-100` | 4 | `plans/002-test-suite.md`; `tests/`; the gate green |
| `t5-fixtures` | 5 | `plans/003-fixture-loader.md`; `fixtures/`; the loader — `demos/lecture-03-game-demo/reference/` |

`demos/lecture-03-game-demo/reference/` is the `t5` state. The tags themselves
live in the instructor's rehearsal repository; they are named here so that this
brief and the lectures can refer to states. The two demo scripts,
`demos/lecture-03-game-demo/demo-script-lecture-03.md` and
`demos/lecture-03-game-demo/demo-script-lecture-04.md`, each end with a section
*Recreating this part yourself (students)*. Read the reference's
specifications, plans, and tests as **patterns**. Do not start from its code;
your engine is derived from your `SPECS.md`, and your git history has to show
that.

**Where the sketch is silent, the client's intent is standard Reversi** (8×8; the
standard four-disc opening; dark moves first; a move must flip at least one disc; a
player with no legal move passes; the game ends when neither player can move; more
discs wins; equal counts tie). This does not let you skip the questions. Your job
is to *find* every place the sketch leaves a decision open, record the ruling, and
state it in the specification — a specification that leaves a standard rule
implicit fails the completeness check. Rulings that are genuinely yours (display
glyphs, hints, post-game options, side alternation, error wording, interface
shapes, module split) are yours to make and record.

## 2. Phase 1, step by step

**How to read a step.** Each step has the same six parts. *Do* is the operation.
*Prompt* is the shape of what you type, taken from the demo scripts; adapt the
names, not the structure. *Rules* are the process rules that govern the step;
the agent has them loaded, and you are expected to know which apply. *Shown in*
is where Lectures 03 to 05 performed it — the lecture notes are
`lecture-notes/lecture-03-specifying-a-game-one-system-several-specifications.md`
and `lecture-notes/lecture-04-verifying-a-game-tests-as-executable-specification.md`,
the demo scripts are the two named above, and "Lecture 05, step N" is the block
of that lecture that walks this step. *Model* is the reference artifact that
shows what the result looks like, under `demos/lecture-03-game-demo/reference/`.
*Ends with* is the commit that closes the step (DEV-7). Rulings are yours, typed
in one or two sentences each; a question you cannot settle is deferred to
`BACKLOG.md`, not guessed (DEV-6). Nothing in the steps is new: every move is
one you watched applied to the note set or to tic-tac-toe.

### Step 0 — Start (`t0`)

**Do.** Copy the starter outside the course repository, initialize a
repository and a virtual environment, install the development requirements,
and make one initial commit:

```sh
cp -R <path-to-module>/student-materials/reversi-starter ~/reversi
cd ~/reversi && git init
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
git add -A && git commit -m "phase 1 start: conops sketch and process"
```

Then read, in full, `CLAUDE.md`, `CONOPS-sketch.md`, and the six documents
under `process/`. DEV-1 applies to you as well as to the agent. Notice that
`process/verification.md` is at version 1.3 with VER-5 through VER-8 already in
it: the amendment Lecture 04 performed before writing any test has been applied
for you, and its changelog entry says why.

**Prompt.** None.

**Rules.** DEV-1 (read before acting); DEV-3 (nothing under `process/` or in
`CLAUDE.md` changes without a proposal and a changelog entry).

**Shown in.** The L03 demo script, *Before class — setup checklist*, step 1;
Lecture 05, opening block.

**Model.** `demos/lecture-03-game-demo/starter/` is the same state for the other
game.

**Ends with.** `phase 1 start: conops sketch and process`.

### Step 1 — The sketch to `CONOPS.md` 1.0 (`t1`)

**Do.** In plan mode: the round-1 audit of the sketch, before anything is
proposed; the gap list per RPT-1; your rulings, one or two sentences each,
saying which document each ruling belongs in (AUDCON-2 — what a player observes
goes in the concept of operations); at least one deferral to `BACKLOG.md`; the
amendments proposed and approved; the rewrite; the audit run again on the
result; the commit.

What the audit must find in this sketch, and the rewrite must fix: sections 2,
3, and 6 stay omitted, with the reason stated (AUDCON-7 — there is no existing
system); every kept section is filled, and no "TBD" survives (AUDCON-7); the
document is in the third person, in the present tense, and names no
implementation (AUDCON-1, AUDCON-5); every mode and every policy appears in a
scenario (AUDCON-3), which for Reversi means at least five scenarios — solo
play, two-player play, a pass, a game that ends before the board is full, and
recovery from an entry the program rejects; a version, a status, and a changelog
(AUDCON-6); the glossary filled (AUDCON-4); each fact in the section whose
purpose it serves (AUDCON-8 — the sketch's "no taking a move back" sits under
Limitations and belongs in §4.2).

**Prompt.** Four, in order. The first is the one Lecture 03 typed on its own
sketch and the one Lecture 05's captures show on yours:

> Read `CONOPS-sketch.md` and the process documents. I want a `CONOPS.md` 1.0
> that realizes this sketch as a full-skeleton concept of operations. Before
> proposing anything, run the audits in `process/conops-audit.md` and
> `process/spec-audit.md` on the sketch (DEV-8) and report the gap list per
> RPT-1 — numbered, each with your recommended resolution. Then stop and wait
> for my rulings.

Rule on every item. For an item you defer:

> Ruling on item N: deferred. Write it to `BACKLOG.md` per DEV-6 — the
> question, where it arose, the options — and do not decide it.

Then:

> Propose the amendments per RPT-3 and wait for my approval.

Read the proposals; approve them, or rule again. Then:

> Write `CONOPS.md` 1.0, run the audits on it again, report per RPT-1, and
> commit as `conops: 0.1 sketch -> 1.0`.

**Rules.** DEV-8, RPT-1, AUD-1 to AUD-7, AUDCON-1 to AUDCON-8, DEV-6, RPT-3,
DEV-3, DEV-7.

**Shown in.** Lecture 03 notes, *A concept of operations for a program* and
*Round 1: turning the sketch to a concept of operations*; the L03 demo script,
Segment 2 and *Recreating this part yourself*; Lecture 05, step 1 — the same
audit, on this sketch.

**Model.** `reference/CONOPS.md` — §4.2 for how a policy reads when it is
something a player observes; §5.1 to §5.4 for one scenario per mode and per
policy; the version, status, and changelog that yours must also carry.

**Ends with.** `conops: 0.1 sketch -> 1.0`. Then export the session to
`transcripts/01-conops-elicitation.md` and commit it as
`transcripts: conops elicitation`. The RPT-1 list, your rulings, and the RPT-3
amendments are the evidence that the document was *elicited*, not typed.

### Step 2 — `CONOPS.md` to `SPECS.md` 1.0.0 (`t2`)

**Do.** The same moves, with a new target. One file, one section per kind, in
this order: board and coordinates; rules of play; display format (byte-exact,
with an empty-board and a mid-game example); input grammar; interaction flow
(menus, the per-game loop, pass handling, post-game); interface contract (each
public operation with its pre- and postconditions — a move's postcondition
names the discs that flip); an example session, with at least one pass in it;
verification obligations. Number every clause so that tests can cite it
(AUD-5). The kinds and their order are pre-picked for this assignment, as they
were for the in-class demo, so that every submission has the same shape; in
general, choosing the kinds of specification is a decision the developer or the
organization makes, and the course catalog (`../specification-kinds.md`) is
the menu.

**Verification obligations, not a testing contract.** The policy — 100% branch
coverage, the single permitted pragma, citation discipline, fixtures never
edited — is already in your `process/verification.md` (VER-4 through VER-8) and
is not yours to weaken. Your `SPECS.md` §9 lists the *obligations*: what the
tests must claim about Reversi, category by category, each traced to the
clauses it verifies (AUD-14). The reference's `SPECS.md` §9.5 is the model;
notice how much of it carries over — that is the point.

**Prompt.** The round-2 prompt of Lecture 03, which names no game:

> Read `CONOPS.md` and the process documents. Derive `SPECS.md` 1.0.0 from it:
> one section per kind — board and coordinates; rules of play; display format,
> byte-exact; input grammar; interaction flow; interface contract with
> preconditions and postconditions; an example session; verification
> obligations. Before writing, run the audit (DEV-8) and list every decision
> the concept of operations leaves open, grouped by the kind of specification
> that must settle it, per RPT-1 with a recommendation each. Wait for my
> rulings.

The list will be long; §4 of this brief is the floor for what it must contain.
Rule on every item. Then:

> Write `SPECS.md` 1.0.0 and commit as `specs: 1.0.0`.

**Rules.** DEV-8, AUD-5, AUD-8 to AUD-14 (one per kind), AUD-3 and DEV-5 (the
contract never contradicts the concept of operations), RPT-1, DEV-7.

**Shown in.** Lecture 03 notes, *Several kinds of specification*, *Round 2:
deriving specifications from the concept of operations*, and *Quality across
the family of specifications*; the L03 demo script, Segment 3; Lecture 05,
step 2.

**Model.** `reference/SPECS.md` — §4 for rules of play as numbered clauses;
§5.1 for an operation's pre- and postconditions (`make_move` there changes one
cell; yours names the set of discs that flip); §7.2 for a byte-exact display
format with two examples; §9.5 for the obligations.

**Ends with.** `specs: 1.0.0`. Export the session to
`transcripts/02-specs-elicitation.md` and commit it.

### From step 3 on: three kinds of change, and the amendment first

From here every commit touches a realization, and every such commit is one of
the three kinds DEV-2 names. The history has to show which:

- **(a) A repair.** The realization did not conform. A report (RPT-2) and a
  ruling come first (RPT-4, DEV-4); the specification does not change.
- **(b) A conformance-preserving change.** Nothing specified changes, and the
  commit message says so.
- **(c) A change of specified behavior.** Implementation will find something the
  specification did not settle — what a move returns after the game is over,
  what happens when both players pass, whether an entry with trailing
  whitespace is accepted. The amendment (RPT-3; approved, DEV-3; version bump
  and changelog entry) is committed **before** the code that depends on the
  ruling, and the audit runs again on the amended document (DEV-8). At least
  one such amendment is expected in Phase 1. A question you cannot settle goes
  to `BACKLOG.md` (DEV-6).

A process document changes only by the same mechanism, and a change that
weakens a rule is returned. Lecture 04 read the reference's history to show why
the order matters: a silence in `SPECS.md` 1.1.0 — nothing said about a move
after the game is over — passed, unaltered, through the engine plan, the
engine, the verification obligations, and the test plan. Five artifacts, none
at fault, each faithful to the one before it, because downstream fidelity
cannot recover information that was never in the specification. That is why
the audit precedes the plan (step 3), and it is the shape of the trace your
report will contain (step 6).

### Step 3 — Audit, plan, build: the engine, the opponent, the CLI (`t3`)

**Do.** Three moves, and the order is the point. (a) Audit `SPECS.md` itself
before any plan exists. This is the audit that, had the reference run it
against its 1.1.0, would have found the after-game-over silence before it
reached the plan. If it finds gaps, rule, amend (RPT-3), commit the amendment,
and run the audit again. (b) Ask for a plan and nothing else; read it; check
that every step cites the clauses it realizes; rule. (c) Approve, commit the
plan, build, report, commit. The module split is yours if your `SPECS.md` §2
says so; the reference's split — a pure engine with no input or output, the
computer strategies as static methods, all input and output in the entry
point — is the default.

**Prompt.** Three, in order:

> Read `SPECS.md` and the process documents. Before any plan, run the audit in
> `process/spec-audit.md` on `SPECS.md` (DEV-8) — AUD-1 through AUD-7, and
> AUD-8 through AUD-14 section by section — and report the gap list per RPT-1.
> Then stop and wait for my rulings.

Then, once the specification is audited and stands:

> Read `SPECS.md` and the process documents. Propose a plan for the engine, the
> computer opponent, and the command-line interface — the modules `SPECS.md` §2
> names — citing for each step the clauses it realizes, and wait for my
> approval.

Then, once you have read and approved the plan:

> Approve the plan. Commit it under `plans/` as
> `plan: engine, opponent, CLI (DEV-9)`. Then build the modules per the approved
> plan, report per RPT-5 with the clauses each module realizes, and commit as
> `engine: game, opponent, and CLI per SPECS 1.0.0`.

Notice what the third prompt does not say: nothing about how to build
anything — no module structure, no algorithm, no naming. The plan says that,
and the plan cites the contract clause by clause; anything added here would be
a fourth source of truth competing with three that are already written down.

**Rules.** DEV-8, DEV-9, DEV-5, RPT-5, DEV-7. VER-1 too: the only verifier at
this point is a person playing one game in each mode against §8 of your
specification, and the RPT-5 note has to say so.

**Shown in.** Lecture 03 notes, *Implementation as a consequence of the
specifications*; the L03 demo script, Segment 4; Lecture 04 notes, *Why
coverage is not conformance*, the DEV-2 (c) paragraph; the L04 demo script,
Segment 4, *The reference's history*; Lecture 05, step 3.

**Model.** `reference/plans/001-engine-opponent-cli.md` — step 1 cites a clause
per bullet, and its `make_move` bullet is the one that inherited the silence;
*What this plan does not cover*; *Verification at the end of this build*. The
three modules, as shape only.

**Ends with.** `plan: engine, opponent, CLI (DEV-9)`, then
`engine: game, opponent, and CLI per SPECS 1.0.0` (or the version the audit
left you with).

### Step 4 — Plan, build, gate: the test suite (`t4`)

**Do.** The suite is a build, so DEV-9 applies to it: a plan under `plans/`
naming, for each step, the obligations of `SPECS.md` §9 it claims and the
clauses each test will cite; then the suite. One test file per source module;
every test's docstring cites the clause it verifies; tighter never looser;
direct board assignment for *setup* only — behavior goes through the public
operation; no test that cannot fail (VER-6). The gate —
`pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100` —
exits 0, and the only `# pragma: no cover` in the repository is on the entry
point's `if __name__ == "__main__":` guard (VER-4, VER-5). The completion note
carries two coverage lines: the gate's branch figure, and which obligations of
§9 are claimed by at least one test and which are not (VER-8). Every
obligation must be claimed.

Recommended, not required: perform Lecture 04's first sabotage step on your
own suite. Delete one test that is the only claimant of a clause, run the
gate, watch it stay green, restore the test. Write the verdict in the lecture's
form — what the gate established, and what it did not. It is the shortest route
to the second item of your report.

**Prompt.** The one Lecture 04 used, which names no game:

> Read `SPECS.md` and the process documents. Propose a plan for the test suite
> under `tests/`, one file per source module, that claims every obligation in
> `SPECS.md` §9: for each step, the obligations it claims and the clauses each
> test will cite (VER-6). Wait for my approval. Then commit the plan under
> `plans/` as `plan: test suite per SPECS 9 (DEV-9)`, write the suite, run the
> gate (VER-4), and report per RPT-5, including which obligations are claimed
> by at least one test and which are not (VER-8). Commit the suite as
> `tests: suite per SPECS 9 (VER-4 green)`.

If the completion note names an obligation no test claims:

> Add a test citing §n.m, run the gate, and report.

If that test fails, the sequence is report (RPT-2), ruling (DEV-4), and only
then a repair — DEV-2 (a) — or an amendment — DEV-2 (c).

**Rules.** DEV-9, VER-4, VER-5, VER-6, VER-8, RPT-5, AUD-14, DEV-2.

**Shown in.** Lecture 04 notes, *Extending the process documents before writing
any tests* (why the rules are already in force), *Tests as executable
specifications*, *Running the gate, then breaking things on purpose*, and *Why
coverage is not conformance*; the L04 demo script, Segments 1 to 4 and
*Recreating this part yourself*; Lecture 05, step 4.

**Model.** `reference/plans/002-test-suite.md` — step 0 is the harness:
`tests/__init__.py` and a `tests/conftest.py` that puts the repository root on
`sys.path` (yours is smaller only in that `pytest.ini` and
`requirements-dev.txt` are shipped), and step 1 reads beside `SPECS.md` §9.5. In `reference/tests/`:
`test_game.py::test_make_move_rejected_after_game_over` (the test that cites
the amended clause) and `::test_render_mid_game_byte_exact` (a golden string);
`test_main.py::test_prompt_human_rejects_invalid_forms` (one clause, eight
rejected forms, parametrized — yours enumerates the forms your grammar rejects,
such as `D3`, ` d3 `, `d9`, `i3`, `d`, `dd3`, an occupied square, a square that
flips nothing, in the order your grammar lists them);
`test_computer_ai.py::test_random_move_always_returns_valid_position_over_many_calls`
(a property, not a distribution). `reference/.coveragerc`, beside your own.

**Ends with.** `plan: test suite per SPECS 9 (DEV-9)`, then
`tests: suite per SPECS 9 (VER-4 green)`.

### Step 5 — Fixtures: the file first, then its loader (`t5`)

**Do.** Two halves, and the order is the point.

(a) **The file.** Write `fixtures/scenarios.json` in the shape of §3.1,
containing at least the eight kinds of scenario §3.3 lists, and
`fixtures/README.md` with the three sections the reference's has: the rules the
fixtures assume, citing your clauses; the loader contract (§3.2); the known
blind spots. Every expectation is checked against your `SPECS.md` by hand. The
pass and early-end scenarios are hard to construct by hand — generate them with
your engine if you must, but verify them against your specification on paper
before trusting them, and say how you did it in the report. An engine is not
the oracle for its own fixtures. Commit the file before any loader exists.

(b) **The loader.** The loader is a build: a plan, your approval,
`tests/test_fixtures.py`, the gate, the RPT-5 note, the commit. A scenario that
fails is a finding about the pair (fixture, specification) — an RPT-1 gap and a
DEV-4 ruling — and never an edit to make it pass (VER-7). A ruling may change
the file; if it does, the README says why.

**Prompt.** The one Lecture 04 used for its loader, with the file already
committed:

> `fixtures/scenarios.json` and `fixtures/README.md` are committed and are not
> to be edited (VER-7). Propose a plan for `tests/test_fixtures.py`: a
> parametrized loader that runs every game scenario and every rejection
> scenario against the engine per the README's loader contract, citing for each
> step the clauses the scenarios verify. Wait for my approval. Then commit the
> plan under `plans/` as `plan: fixture loader (DEV-9)`, write the loader, run
> the gate, report per RPT-5, and commit as `fixtures: loader (VER-7)`.

**Rules.** VER-7, DEV-9, VER-4, VER-8, RPT-1 and DEV-4 for a wrong-looking
expectation, DEV-7.

**Shown in.** Lecture 04 notes, *Fixtures: executable specifications that
outlive the code*; the L04 demo script, Segment 5; Lecture 05, step 5.

**Model.** `reference/fixtures/scenarios.json` — a scenario's name cites the
clause it exercises (`x-wins-row-overline` is §4.1 as moves);
`reference/fixtures/README.md`, three sections; `reference/tests/test_fixtures.py`,
two parametrized functions holding no expectations of their own;
`reference/plans/003-fixture-loader.md`, *What this plan does not cover* — the
blind spots declared, not hidden.

**Ends with.** `fixtures: scenarios.json and README (VER-7)`, then
`plan: fixture loader (DEV-9)`, then `fixtures: loader (VER-7)`.

### Step 6 — Close: the report and the loader's commands

**Do.** Write `PHASE-1-REPORT.md`, one page, four items:

1. **The amendment(s) implementation forced.** For one of them, the trace in
   the form Lecture 04 used for the reference: the clause as it stood; the plan
   step that realized it; the code; the §9 obligation; the test plan or the
   test — and, at each artifact, whether the silence was still there. Say at
   which step of this brief, and under which rule, your process caught it.
2. **One thing 100% branch coverage did not tell you** about conformance
   (VER-8).
3. **How the pass and early-end fixtures were constructed and checked** by
   hand.
4. **What remains for a human or an agent verifier**: the judgment clauses of
   your specification (VER-2), and anything you could not verify by reading.

Then update `CLAUDE.md`'s Commands section — drop "once it exists"; name your
entry point if it is not `main.py` — and make sure `BACKLOG.md` is current:
every deferral open, or closed with a pointer to the ruling that closed it.

**Prompt.** None. The report is yours to write.

**Rules.** VER-8, VER-2, RPT-2 (its scope lines are the report's form), RPT-5,
DEV-6.

**Shown in.** Lecture 04 notes, *Why coverage is not conformance*; the L04 demo
script, Segment 4, *The completion note, read again*; Lecture 05, step 6.

**Model.** `process/reporting.md`, RPT-5 — the report's ancestor. The reference
has no report; this one is yours.

**Ends with.** `phase 1: report`.

### Required elements (all must be present)

Each item names the step it belongs to.

- [ ] **[0]** The initial commit holds the starter as shipped. `CLAUDE.md` and
      `process/` are unchanged except for the Commands section and any
      amendment with a changelog entry (DEV-3).
- [ ] **[1]** `CONOPS.md` 1.0 — version, status, changelog; third person;
      implementation-free; every kept section filled; five scenarios as above;
      glossary.
- [ ] **[2]** `SPECS.md` 1.0.0 or later — the eight sections above; every
      clause numbered; examples byte-exact; §9 as obligations traced to
      clauses; changelog.
- [ ] **[1–2]** Every decision in §4 of this brief is stated explicitly in one
      of the two documents (the concept of operations for what a player
      observes, `SPECS.md` for the rest).
- [ ] **[1–2]** `transcripts/01-conops-elicitation.md` and
      `transcripts/02-specs-elicitation.md` — two RPT-1 gap lists, your
      rulings, the RPT-3 amendments.
- [ ] **[1–3]** Git history: `conops:` before any `SPECS.md` work;
      `specs: 1.0.0` before any plan; every plan committed before the build it
      governs (DEV-9); spec before code (DEV-2).
- [ ] **[3]** `plans/001-…` approved; engine, computer strategy, and CLI per
      `SPECS.md`; the game runs.
- [ ] **[4]** `plans/002-…` approved; `tests/`, one file per source module;
      every test cites a `SPECS.md` clause (VER-6); every obligation in §9
      claimed by at least one test; the gate passes at 100% branch with the
      single permitted pragma; the RPT-5 note's two coverage lines in the
      transcript or the commit.
- [ ] **[5]** `fixtures/scenarios.json` in the shape of §3.1 with the eight
      scenario kinds of §3.3, and `fixtures/README.md`, committed before
      `plans/003-…` and the loader; the loader in `tests/`.
- [ ] **[3–5]** At least one `SPECS.md` amendment committed **before** the
      code that depends on it (DEV-2 (c)); every realization commit
      identifiable as (a), (b), or (c); `BACKLOG.md` lists every deferral.
- [ ] **[6]** `PHASE-1-REPORT.md` with the four items, including one
      five-artifact trace.
- [ ] **[6]** `CLAUDE.md`'s Commands say how to run the game and the tests.

## 3. The fixture file

### 3.1 Fixture shape

Moves are squares in the notation your input grammar defines (`d3`); the literal
`"pass"` means the player to move has no legal move and the engine must report
that before play continues. Colors are named `dark` and `light` regardless of the
glyphs your display uses, so the same file can later run against an engine in
another language.

```json
{
  "description": "Reversi engine fixtures. Standard rules: 8x8, standard opening, dark moves first.",
  "games": [
    {
      "name": "dark-opens-d3",
      "moves": ["d3"],
      "flips": [["d4"]],
      "expected": {"to_move": "light", "dark": 4, "light": 1, "over": false}
    }
  ],
  "rejections": [
    {"name": "flips-nothing", "setup_moves": [], "attempt": "a1"},
    {"name": "occupied",      "setup_moves": [], "attempt": "d4"}
  ]
}
```

### 3.2 Loader contract

Loader contract: from a fresh game, play `moves` in order; every listed move is
accepted; `flips[i]`, if present, is exactly the set of squares flipped by move
`i`; after the last move the engine's state matches `expected`. A `rejections`
entry plays `setup_moves`, submits `attempt`, and requires rejection with the board
and the player to move unchanged. The file is never edited to make a test pass — a
wrong expectation is a specification conversation (VER-7).

### 3.3 Required scenarios

At least: an opening move with its flips; a move that flips in more than one
direction; a rejected move that flips nothing; a rejected entry that is not a
square; **a scenario containing a pass**; **a game that ends before the board is
full**; a full-board game with its final count; a tie. The pass and early-end
scenarios are hard to construct by hand — generate them with your engine if you
must, but *verify them against your specification by hand* before trusting
them, and say how you did it in the report. Name each scenario for the clause
it exercises, as the reference's are named.

## 4. Decisions your specification must record

By kind — the kinds of the course catalog, `../specification-kinds.md`; *computer
opponent* below is a subject that spans three of them. Each is either observable by a player (state it in the ConOps and pin it
in `SPECS.md`) or internal (`SPECS.md` only). Finding them is the exercise; this
list is the floor, not the ceiling.

- **Rules of play.** The exact opening position and which color it gives the first
  move. Who moves first. That a move must flip at least one disc, and that *all*
  flanked runs in *all* directions flip. Whether a pass is forced or chosen. What
  happens after a pass (whose turn; is it announced). When the game ends — and
  that this is not "when the board is full." Who wins on equal counts. Whether a
  move can be taken back.
- **Display.** The glyphs for dark, light, and empty. Row and column labels.
  Whether legal-move hints are shown, when, and how. Whether the count is shown
  during play. Byte-exact format.
- **Input grammar.** The square notation; case; whitespace; length; what is
  rejected and with what effect on the turn. Whether a pass is typed or automatic.
- **Interaction flow.** Menus and their options; the per-game loop; how a pass is
  presented; post-game options; in solo play, which color the human has and
  whether it alternates on a rematch; in two-player play, whether anything
  alternates.
- **Interface contract.** How a square is named to the engine; what a move
  operation returns and what it changes (including the flipped set); how legality
  is queried; how "no legal move" is exposed; how game-over and the count are
  exposed; what an operation does after the game is over.
- **Computer opponent.** "Random among legal moves" — and how that is tested.
- **Verification obligations (`SPECS.md` §9).** The categories of behavior the
  tests must claim, each traced to clauses (AUD-14). The policy — target,
  pragma, citation discipline, fixtures — is fixed by VER-4 through VER-8 and is
  not a decision.

## 5. Process rules

1. **Spec before code (DEV-2).** A change of specified behavior trails a committed
   amendment; a repair follows a report and a ruling; a conformance-preserving
   change says so in its commit. Checked by reading your git history.
2. **Audit before plan; plan before build (DEV-8, DEV-9).** At least three
   approved plans under `plans/` — the engine, the suite, the loader — as in
   the reference; each committed before the build it governs.
3. **The process stands.** `CLAUDE.md` and `process/` are not edited to weaken a
   rule; a process document changes only by an amendment proposal (RPT-3) with
   a changelog entry (DEV-3).
4. **`CONOPS.md` never names an implementation (AUDCON-1).** A ConOps that says
   "Python," "class," or "list" is returned.
5. **Every operation ends the same way (DEV-7):** verified, reported (RPT-5),
   and committed under a message that names it — `conops: 0.1 sketch -> 1.0`,
   `specs: 1.0.0`, `plan: engine, opponent, CLI (DEV-9)`,
   `engine: game, opponent, and CLI per SPECS 1.0.0`,
   `specs: 1.1.0 pass handling (DEV-2 (c))`,
   `tests: suite per SPECS 9 (VER-4 green)`,
   `fixtures: scenarios.json and README (VER-7)`, `fixtures: loader (VER-7)`.

## 6. Grading

Completion-based. Phase 1 is **satisfactory** when every required element is
present and honest — a documented failure or a well-argued deviation counts, a
missing element does not. One resubmission pass.

## 7. What comes next

Stages B–E of the project unit's brief (`../weeks-04-07/project-1-brief.md`),
with Reversi as the subject. Your `fixtures/scenarios.json` and the
instructor's shared fixture set are what the port stage will run against your
engine and its counterpart in another language. Your Phase 1 engine — obvious,
spec-traceable, tested — is the executable specification a later stage will
hold a faster implementation to. Lecture 06 shows the shape of Stage E's MCP
server over the tic-tac-toe engine; over yours, `legal_moves` becomes a
necessary tool, because flanking cannot be read off an ASCII board.

## 8. Do / don't

- **Do** rule on gaps yourself and record the ruling; **don't** let the agent
  decide by default and discover the decision in the code later.
- **Do** reuse the reference's `SPECS.md` §9.5 as the model for your
  obligations — the `process/` set is already yours; **don't** start from its
  code.
- **Do** read the reference's three plans as the pattern for yours; **don't**
  copy its tests, which cite clauses your specification does not have.
- **Do** write the fixture file before its loader and treat it as given from
  then on; **don't** let the engine be the oracle for its own fixtures.
- **Do** commit transcripts and plans; **don't** summarize them from memory.
- **Don't** edit a fixture to make a test pass.
