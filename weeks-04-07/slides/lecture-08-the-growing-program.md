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

# The Growing Program: Elicitation, Change, and the Backlog

**Agentic Software Engineering — Lecture 8**
Week 4 · Meeting 2 of 2

---

## The one idea

Programs grow by **requests**, not rewrites.

The discipline: elicit → **amend the spec** → plan → build → verify.
What you decide *not* to do goes in the **backlog**, not in your head.

---

## The drift bug happened at a *change*

Attempt 1's prompt: *pick a column, then a row.*
Attempt 1's shipped SPECS: *row, then column.*

Not a green-field failure — the artifacts already existed. The drift happened when requirements moved and **only some artifacts moved with them**.

Change requests are where drift breeds.

<!-- 0-10 min. -->

---

## Change control: classical → agentic

| Classical step | Your version |
|---|---|
| Change request | The **spec amendment**, as a commit |
| Impact analysis | Elicitation + **plan mode** (the approved plan *is* the impact statement) |
| Approval | You, green-lighting the plan → `plans/` |
| Implement + verify | The build, then your gates |
| Update artifacts | **Already done — the amendment came first** |

The last row is the whole point: amendment-first makes forgetting structurally impossible.

---

<!-- _class: lead -->

# Worked example: the ripple hunt

---

## "Just two constants," they said

```python
BOARD_SIZE = 9
WIN_LENGTH = 5
```

Make board size configurable. Two lines?

**Grill the change:**

---

## What the hunt finds

- `main.py` says **"Enter a row (1-9)"** in *prose* — and checks `1 <= value <= 9` with its own literals
- `render()` hard-codes the header `"     1 2 3 4 5 6 7 8 9"` and a `"-" * 18` border
- 3x3 board + win length 5 = **unwinnable** — forbid, clamp, or allow? A *decision* → a clause
- Tests assume 9x9 — fixtures need to know their configuration
- The AI survives unchanged — *"unaffected, because it never mentions geometry"* is a finding, not a shrug

**One "two-constant change": four files, the spec, one genuinely new rule.**

<!-- 24-40 min. The amendment is where the ripple gets found while finding it is cheap. -->

---

<!-- _class: standout -->

## Demo: a governed change, end to end

grill-me → amendment commit → plan mode → implement → gates → commit citing the amendment

**Twenty minutes. That is the full price of the discipline.**

<!-- 40-54 min. This is the exact workflow Stage A grades. -->

---

## Deferred work needs a home with a *reader*

| Home | Fate |
|---|---|
| TODO comment | Dies in the file — archaeology, not a queue |
| Your head | Dies tonight (L06 told you what memory is worth) |
| **BACKLOG.md** | Read at the start of **every next stage — mandatorily** |

---

## The case study's backlog rules

> *"Written by the Report phase. **Read by the Gather phase of the next milestone — this is mandatory**, and it is what stops the Report from being write-only."*

Entry shape: **bold one-liner** + *why it matters* + which milestone absorbs it.

Entries close by ~~strikethrough~~ with a pointer to what closed them — **never silently deleted.** The backlog is an honest ledger.

<!-- 54-66 min. lost-communities BACKLOG.md excerpts in the notes. -->

---

<!-- _class: standout -->

## An empty backlog after a week of real work

does not mean you finished everything.

It means you stopped writing things down.
**Your grader will believe exactly that.**

---

## When to skip the pipeline

Behavior-preserving refactors, typos, comments: just commit.

The boundary question:

**"Would any test's expected value change?"**

Yes → spec matter. No → housekeeping.
Not sure → that uncertainty *is* the impact-analysis signal.

---

## Workshop: start your ripple hunt

In your seat, on your chosen Stage A extension:

**Find three ripple items your amendment must cover.**

Instructor circulating.

<!-- 66-75 min. Shock-absorber block. -->

---

## Questions to think about

1. Sort into backlog / TODO / do-now: the render() header break; the O(81) win-scan; seed.py's player-count argument. Who *reads* each placement?
2. A backlog entry three stages old: what are the three honest moves?
3. Price the *undisciplined* version of today's change when the TS port meets an undocumented render assumption in week 7.

---

## Before Tuesday

- [recommended] Python `sqlite3` docs — the tutorial section
- Stage A checkpoint: **end of this week**

**Tuesday: your program gets state — and your repo must learn to reproduce it.**
