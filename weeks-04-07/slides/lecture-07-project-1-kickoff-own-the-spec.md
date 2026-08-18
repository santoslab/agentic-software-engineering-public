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

# Project 1 Kickoff — Own the Spec

**Agentic Software Engineering — Lecture 7**
Week 4 · Meeting 1 of 2

---

## The one idea

A spec is not paperwork about the code.

It is the one artifact that **outlives implementations and steers agents** — and your starter ships without one, *on purpose*.

---

## What you receive today

- A working 9x9 tic-tac-toe (five in a row wins)
- Menus, 2-player mode, a random-move computer opponent
- ~90 green pytest tests

**And no specification of any kind.**

Closing that gap is Stage A. The absence *is* the assignment.

<!-- 0-8 min. Recall Attempt2's first act: declaring the inherited SPECS "sub-par" and rebuilding before code. Students start where they ended up. -->

---

## The project at a glance

![w:1100 center](diagrams/stage-ladder.svg)

Each stage: one classical SE practice + one Claude Code capability — landing the week its lecture lands.

---

<!-- _class: lead -->

# What a spec does for an agent

---

## Three loads nothing else carries

1. **Grounding** — read fresh at every session start; conversations rot (L06), the spec doesn't
2. **Drift prevention** — Attempt 1: prompt said *column-then-row*, shipped SPECS said *row-then-column*. Nobody decided. Two artifacts disagreed; one won by accident
3. **Portability** — the 9x9 ConOps produced the *Java* port. Specs cross language boundaries; prompts are soaked in their language

---

<!-- _class: standout -->

## When code and spec disagree,
## one of them is wrong **on purpose.**

A human rules — and the ruling is a commit.

---

## ConOps vs SPEC: different questions

| | ConOps | SPEC |
|---|---|---|
| Question | What is this system, *for its users*? | *Exactly* what does it do? |
| Voice | User's side of the screen | Behavioral contract |
| Test | **Never says "Python"** | Every clause testable |
| Classical root | IEEE Std 1362 | — |

Yours: one page each. The course repo's IEEE-1362 model is the map, not the destination.

<!-- 22-36 min. -->

---

## Build the mini-ConOps in class

Describe the player's goals, actors, environment, and representative scenarios.

No data structures. No language. No terminal.

Could a non-programmer confirm: *"yes, that is the system I want"*?

---

## Turn observations into SPEC clauses

- precise enough to produce an acceptance test
- explicit about boundaries and failure behavior
- clear about which component owns each guard
- backed by a code path, test, or human design ruling

No user talks like a SPEC. **Tests do.**

---

<!-- _class: standout -->

## Demo: grilling the code

Elicitation, reversed — the agent reads the starter and lists every behavior that is a **decision**, not a necessity.

<!-- 36-54 min. Ask the room to predict edge cases while it runs. -->

---

## Preserve the discovery task

The public slides omit the starter-specific worked answer and canonical edge-case
list because finding and ruling on those behaviors is assessed in Stage A.

In class: trace one method path by path, compare tests, and ask:

**Necessity, language accident, or design decision?**

---

## Two laws start today

**The coverage law lives in CLAUDE.md:**
`game.py` at 100% branch coverage, enforced, always.
(Prompts protect one session; CLAUDE.md protects all of them.)

**Plans are artifacts:**
every stage's main build runs through plan mode; approved plans are committed under `plans/`.

Your grader reads your **git history** — spec amendment, then plan, then implementation is the shape it should have.

---

## Stage A checklist (from the brief)

- [ ] `SPEC.md` — with positions on **at least two discovered edge cases**
- [ ] `CONOPS.md` — one page, implementation-free
- [ ] `CLAUDE.md` — the coverage law
- [ ] One spec-driven extension (recommended: configurable board size)
- [ ] 100% branch on `game.py`; pytest green
- [ ] **Amendment committed before the implementing change**
- [ ] Plan committed under `plans/`

<!-- 54-68 min. Walk the brief; extension ripple is Thursday's worked example. -->

---

## Questions to think about

1. Name the *first concrete moment* in Stages B-E where the missing spec would actually hurt.
2. One ambiguous behavior you found: write both competing clauses, pick one, defend it.
3. Stage B adds a database — which document changes, and what exactly changes in it?

---

## Before Thursday

- Read **`project-1-brief.md`** in full — bring questions
- Re-read the Spec-Driven Development section of the prompt cheat sheet
- Start Stage A: the elicitation session is the first move

**Thursday: how a growing program changes without drifting.**
