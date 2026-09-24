---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
  }
  section.lead {
    background: #310066;
    color: #ffffff;
  }
  section.lead h1, section.lead h2 {
    color: #ffffff;
  }
  section.standout {
    background: #beaefc;
    color: #310066;
    text-align: center;
    font-size: 36px;
  }
  h1, h2 {
    color: #310066;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->

# Reversi Kickoff: Applying the Method

**Agentic Software Engineering — Software-Engineering Module, Lecture 05**
Meeting 5 of 6 · walks the Project 1 brief, step by step · launches Project 1, Phase 1

---

## Where we are: one method, six steps

<style scoped>table { font-size: 22px; }</style>

The specification-family table of Lecture 03, with the audit rule for each kind and the verifier for its realization, is the checklist for Project 1.

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

Every kind the course uses, with these columns: `specification-kinds.md`.

<!-- 0–6 min. -->

---

## The brief's seven steps

<style scoped>table { font-size: 19px; }</style>

| Tag | Step | Produces | Rule | Ends with |
|---|---|---|---|---|
| `t0` | 0 start | the starter, committed | DEV-1 | `phase 1 start: …` |
| `t1` | 1 sketch → ConOps | `CONOPS.md` 1.0; transcript | DEV-8, AUDCON | `conops: 0.1 sketch -> 1.0` |
| `t2` | 2 ConOps → `SPECS.md` | `SPECS.md` 1.0.0; transcript | DEV-8, AUD-8…14 | `specs: 1.0.0` |
| `t3` | 3 audit, plan, build | `plans/001`; engine, opponent, CLI | DEV-8, DEV-9 | `plan: …`; `engine: …` |
| `t4` | 4 the suite as a build; the gate | `plans/002`; `tests/`; gate green | VER-4…8 | `plan: …`; `tests: …` |
| `t5` | 5 fixtures: file, then loader | `fixtures/`; `plans/003`; loader | VER-7, DEV-9 | `fixtures: …` ×2; `plan: …` |
| — | 6 close | `PHASE-1-REPORT.md`; commands | VER-8, VER-2 | `phase 1: report` |

Today reads them in order, and opens the reference game's artifact at each. Nothing here is new; what is new is the game.

<!-- Step 0 tonight: copy, git init, venv, one commit, read everything (DEV-1). -->

---

<!-- _class: standout -->

## Step 1 — the sketch to a concept of operations

You read it as a player. That was validation.

<!-- 6–18 min. Demo Segment 2: read §1.2 and §4.2 aloud; sort with the room; then the captures. -->

---

## §4.2, sorted

<style scoped>table { font-size: 21px; }</style>

| Stated | Implied | Missing |
|---|---|---|
| two colors; players alternate; one disc per turn | an opening position exists — "a few discs already in the middle" | who moves first |
| a move must trap at least one disc, in a straight line — across, down, or diagonally | a move can trap in more than one direction — "everything trapped flips" | what happens after a forfeit: whose turn; announced; both stuck |
| a player with no square to play forfeits the turn | the count is shown at the end (§5.1) | equal counts |
| when the board is full the discs are counted; more wins | | taking a move back — §7 says no, under Limitations (AUDCON-8) |

A reader who already knows Reversi fills the gaps without noticing them. That is why you were asked not to read the rules elsewhere.

**Important**: a rule the sketch does not state is a finding, whatever the reader already knows.

---

## The tension

> "If you have no square you can play, you forfeit your turn."
> "When the board is full, the discs are counted and whoever has more wins."

Each is true of Reversi. Together they are incomplete: both players stuck, twelve empty squares — the sketch does not say what happens.

**AUD-2**, consistency within a document, finds it by reading the two bullets side by side. Same kind of finding as Lecture 03's post-game options; same reason the audit runs before any plan (DEV-8).

<!-- Ask: "Both players are stuck with twelve empty squares left. What does the program do?" Then three minutes for the room's own list. -->

---

## The prompt — step 1, as the brief prints it

> Read `CONOPS-sketch.md` and the process documents. I want a `CONOPS.md` 1.0 that realizes this sketch as a full-skeleton concept of operations. Before proposing anything, run the audits in `process/conops-audit.md` and `process/spec-audit.md` on the sketch (DEV-8) and report the gap list per RPT-1 — numbered, each with your recommended resolution. Then stop and wait for my rulings.

The prompt Lecture 03 typed on its own sketch. The list (capture C1) will be longer than yours, ordered differently, and will miss some of what you found.

<!-- Show C1. Compare with the room's lists. -->

---

## Four rulings, one deferral

<style scoped>table { font-size: 21px; }</style>

| Gap | Ruling | Found by | Goes in |
|---|---|---|---|
| the end of the game — "board is full" | when **neither player has a legal move**; a full board is one case | AUD-2 | the concept of operations (AUDCON-2) |
| the opening — "a few discs in the middle" | d4, e5 light; d5, e4 dark | AUD-4; AUD-8 | the concept of operations; the rules of play state it exactly |
| the pass — "forfeit your turn" | forced, never chosen; announced; the opponent moves; two in a row end the game | AUD-4; AUDCON-3 | the concept of operations, and a scenario |
| the flips — "everything trapped flips" | every flanked run, all eight directions | AUD-1 | the concept of operations |
| legal-move hints — flagged undecided | **deferred** to `BACKLOG.md` (DEV-6); the display format settles it | AUD-4 | — |

A deferral is a decision not to decide yet, recorded where the next reader finds it. Not a guess.

<!-- Show C2, then C3. -->

---

## One ruling to the amendment form, then stop

> Propose the amendment for item 1 per RPT-3 — document, clause, old text, new text, rationale citing the gap-list item, the version bump, the changelog entry — and wait for approval.

*Awaiting approval.* Nothing further is approved.

From here to `CONOPS.md` 1.0 — the remaining rulings, the amendments, the third person, five scenarios, the glossary, the audit run again — is the rest of **step 1**. The brief's step 1 lists what the audit must find in this sketch.

<!-- Show C4. At rehearsal, if the agent starts writing CONOPS.md before approval, stop it: DEV-3 is the rule it skipped. -->

---

## What `CONOPS.md` 1.0 looks like — `reference/CONOPS.md`

- **§4.2** — a policy as a player observes it; never how the program does it (AUDCON-1, AUDCON-2)
- **§5.1–§5.4** — one scenario per mode and per policy (AUDCON-3). Reversi: five at least — a pass and an early end are policies tic-tac-toe did not have
- **Version, status, changelog** (AUDCON-6) — the sketch has none; that is a finding

Ends with `conops: 0.1 sketch -> 1.0`, and the session exported to `transcripts/01-conops-elicitation.md` — the evidence that the document was elicited, not typed.

<!-- Open the reference at §4.2, then §5.4. -->

---

## The convergence rule: where the sketch is silent

**Where the sketch is silent, the client's intent is standard Reversi:** 8-by-8; the standard opening; dark moves first; a move must flip at least one disc; no legal move means a pass; the game ends when neither player can move; more discs wins; equal counts tie.

- It does not let you skip a question. A standard rule left implicit fails completeness (AUD-4). Find every open decision, record the ruling, state it.
- It exists so that engines converge — the port stage runs one shared fixture file against every engine — while the elicitation stays real.

**Yours to decide** (brief §4): glyphs; hints; the count during play; notation edge cases; post-game options; solo-play sides and alternation; error wording; interface shape; module split. Graded on: recorded, consistent, stated in the right document. Not on which way.

---

<!-- _class: standout -->

## Step 2 — the concept of operations to `SPECS.md`

Same moves, new target.

<!-- 18–28 min. Demo Segment 3. -->

---

## The round-2 prompt — names no game

> Read `CONOPS.md` and the process documents. Derive `SPECS.md` 1.0.0 from it: one section per kind — board and coordinates; rules of play; display format, byte-exact; input grammar; interaction flow; interface contract with preconditions and postconditions; an example session; verification obligations. Before writing, run the audit (DEV-8) and list every decision the concept of operations leaves open, grouped by the kind of specification that must settle it, per RPT-1 with a recommendation each. Wait for my rulings.

The kinds are pre-picked; the catalog is the menu. The brief's §4 is the floor for the list. Every item gets a ruling. Then `specs: 1.0.0`, and a second transcript.

---

## What Reversi demands that tic-tac-toe did not

<style scoped>table { font-size: 19px; } p { font-size: 23px; }</style>

| Kind | Tic-tac-toe had | Reversi forces |
|---|---|---|
| rules of play | one cell written; a win is a line | a legal move flanks in ≥1 of 8 directions; a move changes many cells; a pass; the end when neither can move; winner by count; ties realistic |
| initial state | an empty board | the four-disc opening — a completeness trap |
| display format | the grid, `.` for empty | the grid, plus a real decision: hints, and when |
| input grammar | `[1-9][1-9]` | `[a-h][1-8]` — a letter-to-index mapping; is `A3` accepted? |
| interface contract | `make_move → bool` | a legality query at the center; a move's postcondition names the flipped set; the count; dark + light + empty = 64 |
| verification obligations | §9 | the same categories, harder engine; the policy unchanged |
| fixtures | moves → winner | moves → flips and a count; a scenario with a pass; an early end |

The pass is the seeded gap. The largest difference is in the interface contract: a move's postcondition is a set of cells, and a test of a move claims the set.

---

## `SPECS.md` as the model — four sections, one point each

- **§4** — rules of play as numbered clauses, so a test can cite one (AUD-5). Reversi: the opening, the legal move, the flips, the pass, the end, the count
- **§5.1 `make_move`** — precondition, postcondition, behavior outside the precondition, including after the game is over (AUD-12; arrived at 1.2.0). Reversi: the postcondition names the flipped set
- **§7.2** — byte-exact, two examples (AUD-9). Reversi: plus the hints decision
- **§9.5** — obligations, not policy. The policy is VER-4 to VER-8 and is not yours to weaken. Read it against Reversi and see how much carries over

<!-- Open each in reference/SPECS.md; the Changelog for §5.1's history. -->

---

<!-- _class: standout -->

## Step 3 — audit, plan, build

Three moves, in a fixed order. The reason is in the reference's history.

<!-- 28–40 min. Demo Segment 4: the six commands, live. -->

---

## A silence through five artifacts

<style scoped>li { font-size: 24px; }</style>

1. **`SPECS.md` 1.1.0 §5.1** — two reasons `make_move` returns `False`. Nothing about a move after the game is over.
2. **`plans/001`**, the `make_move` step — realizes "each rejection case §5.1 lists". Faithfully. There were two.
3. **`game.py`** — accepted the move, exactly as the plan described.
4. **§9.5** at 1.1.0 — three failure obligations for `make_move`.
5. **`plans/002`** — realizes those three. No test claimed the missing clause.

Not one of them at fault. Each faithful to the one before it — and *downstream fidelity cannot recover information that was never in the specification.*

Which is why the audit precedes the plan (DEV-8). Then 1.2.0 records the ruling; the engine change and the citing test follow — amendment first, realization after (DEV-2 (c)).

<!-- The six greps of the L04 script's Segment 4, in reference/. -->

---

## The two DEV-9 prompts, and the plan as an artifact

**First — the plan and nothing else:**
> Read `SPECS.md` and the process documents. Propose a plan for the engine, the computer opponent, and the command-line interface — the modules `SPECS.md` §2 names — citing for each step the clauses it realizes, and wait for my approval.

**Second — approve, commit, build, report, commit:**
> Approve the plan. Commit it under `plans/` as `plan: engine, opponent, CLI (DEV-9)`. Then build the modules per the approved plan, report per RPT-5 with the clauses each module realizes, and commit as `engine: game, opponent, and CLI per SPECS 1.0.0`.

The second says nothing about *how*. The plan says that, clause by clause.

---

## The plan as an artifact — `reference/plans/001`

- **Step 1** — a clause per bullet; the `make_move` bullet is the one that inherited the silence
- **The preface** — "where the contract does not say, this plan does not say either"; a question the contract cannot settle goes to `BACKLOG.md`
- ***Verification at the end of this build*** — a human, one game per mode against §8, and the RPT-5 note says so (VER-1). There is no suite yet
- **Before both prompts** — the audit of `SPECS.md` itself (DEV-8): the move that would have caught the silence. Amend, commit, re-audit; then plan

The module split is yours if `SPECS.md` §2 says so; the reference's — a pure engine, strategies as static methods, all I/O in the entry point — is the default.

<!-- Open plans/001 step 1; find the make_move bullet; then the Verification section. -->

---

<!-- _class: standout -->

## Step 4 — the suite is a build; the gate

Your `process/` is already the Lecture 04 set. The amendment is done for you.

<!-- 40–52 min. Demo Segment 5. -->

---

## The suite prompt; plan 002 beside §9.5

> Read `SPECS.md` and the process documents. Propose a plan for the test suite under `tests/`, one file per source module, that claims every obligation in `SPECS.md` §9: for each step, the obligations it claims and the clauses each test will cite (VER-6). Wait for my approval. Then commit the plan under `plans/` as `plan: test suite per SPECS 9 (DEV-9)`, write the suite, run the gate (VER-4), and report per RPT-5, including which obligations are claimed by at least one test and which are not (VER-8). Commit the suite as `tests: suite per SPECS 9 (VER-4 green)`.

`reference/plans/002` step 1 reads beside §9.5: every obligation checked off before a test exists. Step 0, the harness, is smaller for you — `pytest.ini` and `requirements-dev.txt` are shipped.

<!-- Open plans/002 step 1 next to SPECS.md §9.5. -->

---

## A test that cites

<style scoped>pre { font-size: 20px; }</style>

```python
def test_make_move_rejected_after_game_over():
    """SPECS §5.1: a move after the game is over returns False and changes nothing."""
```

Setup by direct assignment; behavior through `make_move` (VER-6). The test that follows the 1.2.0 amendment.

```python
def test_prompt_human_rejects_invalid_forms(monkeypatch, capsys, bad_input):
    """SPECS §6.2: every invalid move form is rejected and re-prompted."""
```

One clause, eight forms, parametrized. **Reversi's eight:** `D3`, ` d3 `, `d9`, `i3`, `d`, `dd3`, an occupied square, a square that flips nothing — in the order your grammar lists them.

<!-- Open tests/test_game.py at line 111, tests/test_main.py at line 70. -->

---

## The gate — VER-4, VER-5 — and the two coverage lines

```sh
pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100
grep -n 'pragma' *.py
```

Exit 0; one pragma, on the `__main__` guard. The starter ships `.coveragerc` with `source = .` — every module in the root, whatever your split — and `pytest.ini`; neither is edited to weaken the gate.

**RPT-5 carries two lines (VER-8):** branch coverage — a property of (tests, code); clause coverage — which §9 obligations at least one test claims — a property of (tests, specification). Different questions. Lecture 04's three sabotage steps: each line informative once, uninformative once.

Recommended: delete the only test claiming a clause, run the gate, watch it stay green, restore. Write the verdict in the lecture's form.

<!-- Run the gate in reference/, live: 99 passed, 100%. Then .coveragerc. -->

---

## Three kinds of change — DEV-2 — from step 3 on

<style scoped>table { font-size: 22px; }</style>

| Kind | What comes first | The history shows |
|---|---|---|
| **(a) repair** | a report (RPT-2) and a ruling (DEV-4) | no specification change |
| **(b) conformance-preserving** | nothing | the commit message says no specified behavior changed |
| **(c) change of specified behavior** | the amendment — RPT-3, approved (DEV-3), version bump, changelog | amendment first, realization after; the audit run again (DEV-8) |

Implementation will find a silence — a move after the game is over; a pass after a pass; trailing whitespace. At least one (c) is expected. A question you cannot settle goes to `BACKLOG.md` (DEV-6).

---

<!-- _class: standout -->

## Step 5 — fixtures: the file first, then its loader

<!-- 52–62 min. Demo Segment 6. -->

---

## The fixture shape — brief §3.1 — and the eight kinds — §3.3

```json
{ "name": "dark-opens-d3",
  "moves": ["d3"],
  "flips": [["d4"]],
  "expected": {"to_move": "light", "dark": 4, "light": 1, "over": false} }
{ "name": "flips-nothing", "setup_moves": [], "attempt": "a1" }
```

- squares in your grammar's notation; the literal `"pass"` for a forced pass; colors `dark` and `light` whatever your glyphs; for each move, the set it flips
- **at least:** an opening move with its flips · a multi-direction flip · a rejected move that flips nothing · a rejected non-square · **a pass** · **an early end** · a full board with its count · a tie
- a scenario's name cites its clause — `x-wins-row-overline` is §4.1 as moves

<!-- Open reference/fixtures/scenarios.json beside the brief's §3.1. -->

---

## The file first, the loader second

<style scoped>li, p { font-size: 24px; }</style>

- **The file** — `fixtures/scenarios.json` and `fixtures/README.md`: rules assumed, citing your clauses; the loader contract; **known blind spots**, declared and part of the contract. Every expectation checked against `SPECS.md` by hand. Committed before any loader exists.
- **The loader** — a build: plan, approval, `tests/test_fixtures.py`, gate, RPT-5, commit. Two parametrized functions, no expectations of their own.
- **Never edited to pass** (VER-7). A failing scenario is a finding about (fixture, specification): an RPT-1 gap, a DEV-4 ruling.
- The pass and early-end scenarios: engine-generated if you must; **verified against your specification by hand**, and the report says how. An engine is not the oracle for its own fixtures.

Three commits: `fixtures: scenarios.json and README (VER-7)` · `plan: fixture loader (DEV-9)` · `fixtures: loader (VER-7)`.

<!-- Open fixtures/README.md "Known blind spots", tests/test_fixtures.py, plans/003 "What this plan does not cover". -->

---

## Step 6 — the report

`PHASE-1-REPORT.md`, one page, four items:

1. **The amendment(s) implementation forced** — one of them traced through five artifacts: the clause as it stood → the plan step → the code → the §9 obligation → the test plan or test. At which step, under which rule, your process caught it.
2. **One thing 100% branch coverage did not tell you** (VER-8).
3. **How the pass and early-end fixtures were constructed and checked** by hand.
4. **What remains for a human or agent verifier** — the judgment clauses (VER-2); what you could not verify by reading.

Then `CLAUDE.md`'s Commands — "once it exists" goes — and `BACKLOG.md` current. `phase 1: report`.

<!-- 62–72 min. -->

---

## Required elements — all must be present

<style scoped>table { font-size: 15px; } h2 { margin-bottom: 0.3em; }</style>

| Step | Element | Rule |
|---|---|---|
| 0 | the starter as shipped in the initial commit; `CLAUDE.md`/`process/` unchanged except Commands and recorded amendments | DEV-3 |
| 1 | `CONOPS.md` 1.0 — version, status, changelog; third person; implementation-free; sections filled; five scenarios; glossary | AUDCON-1…8 |
| 2 | `SPECS.md` 1.0.0+ — eight sections; every clause numbered; byte-exact examples; §9 traced; changelog | AUD-5, AUD-8…14 |
| 1–2 | every §4 decision stated in one of the two documents; `transcripts/01-…`, `02-…`: two RPT-1 lists, rulings, RPT-3 amendments | AUD-4; RPT-1, RPT-3 |
| 1–3 | history: `conops:` before `SPECS.md` work; `specs: 1.0.0` before any plan; every plan before its build | DEV-2, DEV-7, DEV-9 |
| 3 | `plans/001-…`; engine, opponent, CLI per `SPECS.md`; the game runs | DEV-9 |
| 4 | `plans/002-…`; every test cites; every §9 obligation claimed; gate green at 100% branch, one pragma; RPT-5's two lines | VER-4…6, VER-8 |
| 5 | `fixtures/scenarios.json` (§3.1 shape, §3.3 kinds) and `fixtures/README.md`, committed before `plans/003-…` and the loader | VER-7 |
| 3–5 | ≥1 amendment committed before the code that depends on it; every realization commit (a)/(b)/(c); `BACKLOG.md` current | DEV-2, DEV-3, DEV-6 |
| 6 | `PHASE-1-REPORT.md` — four items, one five-artifact trace; `CLAUDE.md` Commands | VER-8, VER-2 |

---

## Logistics

- **Adopted, not authored.** `process/` is the L04 set, identical to the reference's; so is the gate's configuration. A rule changes only by amendment with a changelog entry (DEV-3); a change that weakens one is returned.
- **Notation.** `d3` per the sketch. `D3`, ` d3 `, `d9` — yours, stated as a grammar (AUD-10). Where the letter becomes an index — inside the engine (AUD-12).
- **Due one week from today** (date per the brief). Start with step 0 tonight.
- **Lecture 06** is MCP and launches nothing new; it previews Stage E — an MCP server over your engine. Finish Phase 1.
- **Where to ask.** The repository first (DEV-10); then `BACKLOG.md` or the course channel. A question about the rules of Reversi is answered by the convergence rule.

---

## Questions to think about

1. The sketch says the game ends when the board is full, and that a player with no move forfeits the turn. Neither is wrong; one is incomplete. Which, and how do you know from the document alone?
2. Which rulings in your gap list are yours, and which are the client's? Where does the brief draw the line, and why there?
3. Step 5 requires a scenario containing a pass. Before you trust one your own engine generated, what do you check it against, and how — and what does VER-7 say about the file afterwards?
4. The after-game-over silence passed through five artifacts of the reference. At which step of the brief, and under which rule, would your Phase 1 have caught it?

---

## Before next meeting

- **Project 1, Phase 1** — the brief, §2. Step 0 tonight; then step 1, the audit you watched, in your own copy of the starter.
- Read the Model Context Protocol documentation's core concepts and the FastMCP quickstart, and the dice-server README from the project unit. Lecture 06: what changes when the reader of a specification is a machine.
