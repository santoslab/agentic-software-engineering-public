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
Meeting 5 of 6 · runs the Reversi audit walkthrough · launches Project 1, Part 1

---

## Where we are: one method, applied twice

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

<!-- 0–8 min. Buffer: anything L03/L04 dropped — the overline chain, DEV-2's three kinds, the fixture loader run. -->

---

<!-- _class: standout -->

## Learning Reversi from its sketch

You read it as a player. That was validation.

<!-- 8–22 min. Demo Segment 1: read §1.2 and §4.2 aloud; sort with the room. -->

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

<!-- Ask: "Both players are stuck with twelve empty squares left. What does the program do?" -->

---

<!-- _class: standout -->

## The audit of the sketch, watched

The first move of Part 1, on the starter you have.

<!-- 22–48 min. Demo Segment 2. Three minutes for the room's list first. -->

---

## The prompt

> Read `CONOPS-sketch.md` and the process documents. Before proposing anything, run the audits in `process/conops-audit.md` and `process/spec-audit.md` on the sketch (DEV-8) and report the gap list per RPT-1 — numbered, each with your recommended resolution. Then stop and wait for my rulings.

The same prompt Lecture 03 used, on a different sketch. The list will be longer than yours, ordered differently, and will miss some of what you found.

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

---

## One ruling to the amendment form, then stop

> Propose the amendment for item 1 per RPT-3 — document, clause, old text, new text, rationale citing the gap-list item, the version bump, the changelog entry — and wait for approval.

*Awaiting approval.* Nothing further is approved.

From here to `CONOPS.md` 1.0 — the remaining rulings, the amendments, the third person, five scenarios, the glossary, the audit run again — is **Part 1, step 1**.

<!-- If the agent starts writing CONOPS.md, stop it: RPT-4 is the rule it skipped. -->

---

## The convergence rule: where the sketch is silent

**Where the sketch is silent, the client's intent is standard Reversi:** 8-by-8; the standard opening; dark moves first; a move must flip at least one disc; no legal move means a pass; the game ends when neither player can move; more discs wins; equal counts tie.

- It does not let you skip a question. A standard rule left implicit fails completeness (AUD-4). Find every open decision, record the ruling, state it.
- It exists so that engines converge — the port stage runs one shared fixture file against every engine — while the elicitation stays real.

**Yours to decide** (brief §4): glyphs; hints; the count during play; notation edge cases; post-game options; solo-play sides and alternation; error wording; interface shape; module split. Graded on: recorded, consistent, stated in the right document. Not on which way.

<!-- 48–62 min. -->

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

<!-- 48–62 min, with the two deliverables slides. -->

---

## The Project 1 deliverables and the rule behind each — Part 1

<style scoped>table { font-size: 21px; }</style>

| Required element | Rule | Shown in |
|---|---|---|
| `CONOPS.md` 1.0 — third person, implementation-free, kept sections filled, five scenarios, glossary, changelog | AUDCON-1 to AUDCON-8 | L02, L03 |
| `SPECS.md` 1.0.0 — eight sections, every clause numbered, byte-exact examples, §9 as obligations | AUD-5, AUD-8 to AUD-14 | L03 |
| every decision in the brief's §4 stated in one of the two documents | AUD-4 | L03 |
| `transcripts/part-1-elicitation.md` — two RPT-1 lists, the rulings, the RPT-3 amendments | RPT-1, RPT-3, DEV-4 | L01–L03 |
| `CLAUDE.md` and `process/` as shipped, or amended only with a changelog entry | DEV-3 | L04 |
| the concept of operations committed before the `SPECS.md` work begins | DEV-2, DEV-7 | L03 |

Nothing here is new. What is new is the game.

---

## The Project 1 deliverables and the rule behind each — Part 2

<style scoped>table { font-size: 21px; }</style>

| Required element | Rule | Shown in |
|---|---|---|
| the approved plan under `plans/` before the implementing commits | DEV-9 | L03 |
| every test cites its clause; every §9 obligation claimed by at least one test | VER-6, VER-8 | L04 |
| the gate green at 100% branch, one pragma | VER-4, VER-5 | L04 |
| `fixtures/scenarios.json`, eight scenario kinds, a loader | VER-7 | L04 |
| at least one amendment committed before the code that depends on it | DEV-2 (c), DEV-3 | L04 |
| `PART-2-REPORT.md` — the amendment; what coverage did not tell you; how the pass and early-end fixtures were checked | VER-8, RPT-5 | L04 |

---

## The fixture shape

```json
{ "name": "dark-opens-d3",
  "moves": ["d3"],
  "flips": [["d4"]],
  "expected": {"to_move": "light", "dark": 4, "light": 1, "over": false} }
{ "name": "flips-nothing", "setup_moves": [], "attempt": "a1" }
```

- squares in your grammar's notation; the literal `"pass"` for a forced pass
- colors `dark` and `light` whatever your glyphs — the same file runs against an engine in another language later
- for each move, the set of squares it flips

The pass and early-end scenarios are hard to construct by hand. Generate them with your engine if you must; **verify them against your specification by hand** before trusting them, and say how in the report. An engine is not the oracle for its own fixtures.

---

## Logistics

- **The process set is adopted, not authored.** The L04 set, identical to the demo's. A rule changes only by amendment with a changelog entry (DEV-3); a change that weakens one is returned.
- **Notation.** `d3` per the sketch. `D3`, ` d3 `, `d9` — yours, stated as a grammar (AUD-10). Where the letter becomes an index — inside the engine (AUD-12).
- **Effort and dates** per the brief. Part 1 due at the end of this week.
- **Where to ask.** The repository first (DEV-10); then `BACKLOG.md` or the course channel. A question about the rules of Reversi is answered by the convergence rule.

<!-- 62–72 min. -->

---

## Questions to think about

1. The sketch says the game ends when the board is full, and that a player with no move forfeits the turn. Neither is wrong; one is incomplete. Which, and how do you know from the document alone?
2. Which rulings in your gap list are yours, and which are the client's? Where does the brief draw the line, and why there?
3. Part 2 requires a scenario containing a pass. Before you trust one your own engine generated, what do you check it against, and how?

---

## Before next meeting

- **Project 1, Part 1** — the brief, §2. Start with the audit you watched, in your own copy of the starter.
- Read the Model Context Protocol documentation's core concepts and the FastMCP quickstart, and the dice-server README from the project unit. Lecture 06: what changes when the reader of a specification is a machine.
