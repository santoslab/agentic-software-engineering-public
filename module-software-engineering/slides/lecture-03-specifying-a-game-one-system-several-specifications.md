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

# Specifying a Game: One System, Several Specifications

**Agentic Software Engineering — Software-Engineering Module, Lecture 03**
Meeting 3 of 6 · runs part 1 of the game demo · Exercise 3 (optional)

## Lecture Purpose

- Illustrate concepts of spec-driven development with agents using a simple program
- Review the idea of a "Concept of Operations" (ConOps), and illustrate how development can be 
initiated by only a sketch of a ConOps document.

A system needs several specifications of different kinds; 
> starting from a ConOps, the agent helps you discover the specifications by 
> audit and interrogation.


---

## Illustrating spec-based development with a program

What carries over: the audit, the reports, the three kinds of verifier, the development rules, the invariant. None of it depended on the realization being a note.

What changes:

- the specification starts as a **sketch** — a client's general idea, first person, two sections marked TBD
- the realization is code, and it must satisfy **several kinds** of specification
- three process rules and one appendix, all about building: DEV-8, DEV-9, DEV-10; AUDCON-7, AUDCON-8; AUD-8 to AUD-14

`ls` at `t0`: `CONOPS-sketch.md`, `CLAUDE.md`, `process/`, `BACKLOG.md`. Nothing else.

<!-- 0–6 min. Why a game: grid, two players, rules, a terminal condition; small enough to specify in a lecture, large enough to need several kinds. Project 1 has the same shape. -->

---

## A concept of operations for a program

The full skeleton: scope · current situation · justification and nature of the changes · concept for the proposed system (objectives, policies, modes, user classes, environment) · scenarios · summary of impacts · analysis · future capabilities · glossary

- Sections 2, 3, 6 only when an existing system is improved — **AUDCON-7** audits their presence and every kept section
- Policies a player can observe (**AUDCON-2**); nothing that exists only inside the realization (**AUDCON-1**)
- Answers a validation question: is this the game that was wanted?

The game's O1 is a move — precondition: the cell is empty and the game is not over; postcondition: the mark is placed and the turn has passed. The rules of play are the invariant.

<!-- 6–14 min. The sketch keeps 2 and 3 short (ordinary 3x3 is the baseline) and skips 6. -->

---

<!-- _class: standout -->

## Round 1: turning the sketch into a concept of operations

Our development rule DEV-8: audit before any plan.

<!-- 14–30 min. Demo Segment 2. Plan mode. Type the prompt; the room writes its own list for two minutes. -->

---

## The prompt

> Read `CONOPS-sketch.md` and the process documents. I want a `CONOPS.md` 1.0 that realizes this sketch as a full-skeleton concept of operations. Before proposing anything, run the audits in `process/conops-audit.md` and `process/spec-audit.md` on the sketch (DEV-8) and report the gap list per RPT-1 — numbered, each with your recommended resolution. Then stop and wait for my rulings.

<!-- Seeded findings, for your eyes: fourteen, in the script's round-1 table. Rule on six or seven live; defer "quit mid-game" on purpose. -->

---

## What the audit finds in a sketch

<style scoped>table { font-size: 21px; }</style>

| Gap | Found by | Ruling |
|---|---|---|
| "five in a row" — does six win? | AUD-1 | five **or more** |
| the last square completes five: win or draw? | AUD-4 | a win takes precedence |
| §4.3 "play again or menu" vs §5.1 "play again or quit" | AUD-2 | three options |
| "type its row and column" — in what form? | AUD-1 | two digits, row then column |
| "nothing is saved" stated under Limitations | AUDCON-8 | moved to §4.5, environment |
| one scenario, and it assumes a win | AUDCON-3 | add two-player, tie, bad-entry scenarios |
| glossary: TBD | AUDCON-7 | define the terms |
| first person throughout | AUDCON-5 | third person, implementation-free |
| quitting mid-game | AUD-4 | **deferred** to `BACKLOG.md` (DEV-6) |

Amendments per RPT-3; `CONOPS.md` 1.0; audited again; shown from `t1`.

<!-- Two of these are faults, not gaps: the inconsistency and the misfiled fact. Both found by reading, before anything realized the document. -->

---

## Several kinds of specification

<style scoped>table { font-size: 17px; } p { font-size: 20px; }</style>

| Kind | Fixes | Form | Verified by |
|---|---|---|---|
| concept of operations | what the game is for; what a player observes; scenarios | prose, full skeleton | a person reading — validation |
| rules of play | win, tie, precedence, initial state, the turn | numbered clauses | tests; fixtures |
| display format | exactly what the screen shows | example + measurements | golden-string tests |
| input grammar | every accepted and rejected form; effect of a rejection | a grammar | rejection tests |
| interaction flow | menus, options, the loop, every exit | numbered steps | scripted-input tests |
| interface contract | each operation: parameters, pre/post, behavior outside the precondition | signatures with contracts | unit tests |
| example session | one whole transcript | specification by example | an end-to-end run |
| verification obligations | what the tests must claim, traced to clauses | a list of categories | reading the suite |

Per-kind checks: **AUD-8 to AUD-14**; agreement across kinds: **AUD-3**. All eight are kinds in the course catalog `specification-kinds.md`; *rules of play* is the one game-specific name.

<!-- The catalog's "survives a port?" column: some kinds survive a change of language unchanged, some are re-expressed. Lecture 04 returns to it. -->

---

## What we are really setting up

<style scoped>section { font-size: 26px; }</style>

**Important**: in agentic development we are less focused on writing code — the agent does that — and more focused on the *development framework*:

- choosing which kinds of specification to use
- writing the quality rules (the audits) that keep the specifications in a good state as development proceeds
- designing what it means for a realization to conform to a specification

The specification family, the process documents, and the verifiers are that framework.

**Who chooses the kinds?** The developer — or the organization: many companies fix a standard collection, with a format for each. Without that guidance someone decides, and by default it is the agent. Here and in the Reversi assignment the kinds are **pre-picked** — the loader, the round-2 prompt, and AUD-8 to AUD-14 all name them — to keep the demo simple and deterministic.

---

<!-- _class: standout -->

## Round 2: deriving specifications from the concept of operations

One section per kind. The specifications are the contract our realization must adhere to.

<!-- 30–46 min. Demo Segment 3. -->

---

## The prompt

> Read `CONOPS.md` and the process documents. Derive `SPECS.md` 1.0.0 from it: one section per kind — board and coordinates; rules of play; display format, byte-exact; input grammar; interaction flow; interface contract with preconditions and postconditions; an example session; verification obligations. Before writing, run the audit (DEV-8) and list every decision the concept of operations leaves open, grouped by the kind of specification that must settle it, per RPT-1 with a recommendation each. Wait for my rulings.

The list comes back grouped. The groups are the table on the previous slide.

---

## Four rulings, and one non-decision

- **Display** (AUD-4, AUD-9): the concept of operations never says what the board looks like. Byte-exact: labels always; `.` for empty; four leading spaces; nineteen dashes; two examples.
- **Input grammar** (AUD-10): strip; exactly two characters; each `1`–`9`; `0` and `123` rejected, the turn does not pass.
- **A move after the game is over** (AUD-12): rejected, no change of state. The reference implementation's specification never said this — today's specification is stricter than that code.
- **"Picks at random"** (AUD-14): the obligation is a property — the result is always among the available moves — not a distribution.
- **The coverage policy** is not a decision the technical specifications make. It is in `process/verification.md` — a quality constraint on the implementation. §9 holds what the tests must claim about *this* game.

<!-- Shown from t2: grep '^## ' SPECS.md; the eight sections; §4.1 "five or more"; §9. -->

---

## One fact, five statements, one chain

| Where | Says |
|---|---|
| `CONOPS.md` §4.2 | a player wins with **five or more** marks in a line |
| `SPECS.md` §4.1 | overlines count |
| `SPECS.md` §9 | at least one overline case |
| a test (Lecture 04) | `"""SPECS §4.1: overlines count."""` |
| a fixture (Lecture 04) | `x-wins-row-overline` |

AUD-3 across the family of specifications. If the rules said "exactly five," the audit finds it.

---

## Quality across the family of specifications

- **Unambiguous (AUD-1)** — "the board looks like this" is not a display specification; "four leading spaces, then the digits 1 to 9 separated by single spaces" is
- **Complete for its level (AUD-4)** — the walkthrough: play one game on paper from the menu to the post-game menu; what does the display say about a full board? what does `make_move` do when the game is over?
- **Traceable (AUD-5)** — every clause has a number; a test says `SPECS §4.1`; nothing is renumbered

<!-- 46–56 min. -->

---

## Implementation as a consequence of the specifications

DEV-8 is satisfied. DEV-9: a plan, in plan mode, approved, committed under `plans/`, citing for each step the clauses it realizes.

> Read `SPECS.md` and the process documents. Propose a plan for the engine module, the computer opponent, and the command-line interface, citing for each step the clauses it realizes, and wait for my approval.

Shown from `t3`: three modules — an engine with no I/O, strategies, an entry point that owns every prompt — and a history that reads specification → plan → realization. `CLAUDE.md` is still two rules.

Nothing verified yet, except by playing one move each way.

<!-- 56–64 min. cat plans/*.md | head; python main.py; git log --oneline. -->

---

## What is new in the process documents

| Rule | Says | Today |
|---|---|---|
| DEV-8 | audit before any plan; again after any amendment | rounds 1 and 2 |
| DEV-9 | plan, then build; the plan cites clauses | the implementation |
| DEV-10 | a question the repository can answer is answered by reading it | throughout |
| AUDCON-7 | the full skeleton; sections 2, 3, 6 only with a baseline | the TBD glossary |
| AUDCON-8 | a fact in the section whose purpose it serves | "nothing is saved" |
| AUD-8 … AUD-14 | checks by kind | round 2 |

<!-- 64–72 min. -->

---

## Exercise 3, and next

**Exercise 3 (optional)** — from your own copy of the starter, run round 1 and compare your list with the script's table; continue to round 2 and submit the grouped list with your rulings.

**Lecture 04** — the implementation verified: a test suite that cites clauses, a coverage gate, and what coverage does not tell you.

**Lecture 05** — a sketch of a different game; these moves, in your own session.

---

## Questions to think about

1. "How is the random opponent tested?" ended up in the obligations, not in the rules. Why is *how it is tested* not a property of the game?
2. The sketch said "five in a row"; the concept of operations says "five or more." Which side moved, who decided, where is it recorded — and what does §4.1 add?
3. Of the fourteen gaps, which would a player have noticed first, and which only an implementer? Sort them with AUDCON-2.

---

## Before next meeting

- Read `process/verification.md` at its Lecture 04 level — VER-5 through VER-8 — and the shared-fixtures README.
- Exercise 2 is due before Lecture 04. Exercise 3 is optional.
