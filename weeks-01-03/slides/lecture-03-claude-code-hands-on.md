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

# Claude Code Hands-On: Permissions, CLAUDE.md, Plan Mode

**Agentic Software Engineering — Lecture 3**
Week 2 · Meeting 1 of 2

---

## The one idea

Claude Code is **Lecture 2's loop, productionized**.

Today: drive it deliberately — know what each feature does to the context,
and what each permission prompt is protecting — instead of vibing.

---

## Map the UI onto the loop

| You see… | It is… |
|----------|--------|
| the transcript scrolling | the messages list |
| the spinner | a model call in flight |
| a diff awaiting approval | a `tool_use` request, **paused at the harness** |

Nothing here is a new concept. Keep the mapping and this lecture is easy.

<!-- 0–5 min recap. -->

---

<!-- _class: lead -->

# Permissions

---

## The harness's refusal point

```
Claude wants to run:  pytest -q
  (y) allow once   (a) always allow pytest in this project   (n) deny
```

The two-second habit before any keypress:
**what does this touch, and is it reversible?**

- `pytest -q` — reads code, runs tests. Cheap.
- `rm -rf build/`, `git push` — an actual pause.
- `(a)` is how permissions accumulate into project settings — and how an over-permissive setup happens one keystroke at a time.

<!-- 5–15 min. Auto-accept is a loaded gun in week 2; loosening comes later, deliberately, with git as backstop. Settings live in .claude/settings.json. -->

---

<!-- _class: standout -->

## Demo 1: `/init` vs the curated CLAUDE.md

Generate a CLAUDE.md from the code alone.
Then diff it against the one the maintainer wrote.

<!-- 15–30 min. Clean 3by3 copy with CLAUDE.md moved aside; fresh session; /init; side-by-side diff. Fallback: pre-captured /init output, static diff. -->

---

## What `/init` could never have written

> *"The 1-based-to-0-based translation lives inside `Game` and never escapes its boundary."*

> *"`ComputerAI` exposes strategies as **static methods** only … future strategies plug in by adding another static method and a dispatch entry in `main.py`."*

These aren't facts *about* the code — they're **decisions**.
`/init` describes what is; only a human says what must *remain* true.

**A good CLAUDE.md = the intent that code cannot carry.**

---

## CLAUDE.md as memory

- Injected into **every session** in the project — user-space system prompting
- Rule of thumb: typed the same instruction into prompts twice? **It belongs in CLAUDE.md.**
- You'll practice this judgment in Exercise 2 — improving a generated CLAUDE.md is a graded deliverable

---

## @-mentions and slash commands

- **`@path/to/file`** — force a file into context before answering.
  Surgical. Don't @ half the repo; every token competes (Lecture 6 shows the bill).
- **`/command`** — a *skill*: a reusable prompt stored as a file.

The course's `grill-me` skill, in its entirety:

> *Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree resolving dependencies between decisions one by one. If a question can be answered by exploring the codebase, explore the codebase instead. For each question, provide your recommended answer.*

**A slash command is just a prompt file.** A methodology in a paragraph.

---

<!-- _class: lead -->

# Plan mode

---

<!-- _class: standout -->

## Demo 2: a real feature, plan-first

Add a `blocking_move` strategy to the tic-tac-toe AI —
explore → plan → approve → execute → interrupt and steer.

<!-- 30–45 min. Tests green before class; prompt written on a card. Fallback: recorded rehearsal. -->

---

## The plan the agent proposes (read it like a review)

> 1. Read `computer_ai.py` + tests to match the existing strategy pattern
> 2. Add `blocking_move(game)`: scan for cells completing an opponent five-in-a-row; return it, else fall back to `random_move`
> 3. Register the strategy in `main.py`'s dispatch
> 4. Tests: blocks in each direction; falls back cleanly
> 5. Run the suite

Step 2 hides a design question: does "imminent" include `X X . X X`?

**Catch it in prose for a sentence — or in the diff for a rewrite.**

---

## Why plan-first beats prompt-and-pray

- The plan surfaces the agent's *understanding* before any file changes
- A natural checkpoint to inject constraints while they're cheap
- Approval turns the plan into the working contract for execution

Cheap words before expensive edits; both cheaper than rework.

---

## The cost/context survival kit

| Command | What it does |
|---------|--------------|
| `/context` | what's in the window, and how full |
| `/cost` | what this session has spent |
| `/compact` | summarize to reclaim space (**lossy**) |
| `/clear` | wipe; CLAUDE.md re-injected |

```
CLAUDE.md + settings   1.4k      file reads (9)   31.2k
conversation          17.9k      tool output       6.8k
                          total  57.3k of 200k
```

Nine files re-sent every turn — most no longer needed. *(illustrative)*

<!-- 45–52 min. Just enough for Ex. 2; economics deep-dive is L6. Rule: sluggish or forgetful session → check /context before blaming the model. -->

---

<!-- _class: standout -->

## Demo 3: "fix the AI, it plays bad"

A deliberately vague prompt. A confident, plausible change.
Was it what anyone wanted?

<!-- 52–63 min flex block: this demo (no laptops) OR micro-lab (laptops; install instructions must have shipped with L02). One sentence of specificity transforms the outcome — cold open for L04. -->

---

## Deferred, deliberately

| Feature | Taught |
|---------|--------|
| skills at depth | ~week 5 |
| hooks, subagents | ~week 9 (Project 2) |
| MCP servers, plugins | ~week 12 (Project 3) |
| sandbox | as needed |

Each arrives when a project demands it. Map: `technical-concepts.md`.
The loop, context discipline, and verification carry you through Project 1.

<!-- 63–70 min. Cut to one sentence if running long. -->

---

<!-- _class: standout -->

## Exercise 2 launches

An unfamiliar OSS codebase. Comprehension only — no edits.
Improve the generated CLAUDE.md with intent it couldn't know.
**Catch Claude being wrong at least once — with evidence.**

Due before Lecture 5.

<!-- 70–75 min. Walk the spec; repo + pinned commit announced with it. -->

---

## Questions to think about

1. What belongs in CLAUDE.md vs the prompt vs a spec file? (L4 answers this properly.)
2. Which permission would you *never* auto-accept, even in week 15?
3. `/init` read every line and still missed things. What *category* of knowledge did it miss?

---

## Before next lecture

- **Required:** the *Prompting Cheat Sheet* handout — L4 walks it; arrive having read it
- **Required:** *Claude Code Best Practices* (code.claude.com/docs/en/best-practices)
- **Recommended:** Claude Code docs — permissions, memory, plan mode (links in `technical-concepts.md`)
- **Exercise 1 due before next lecture** · Exercise 2 now open

*Next: why requirements and specs dominate cleverness.*
