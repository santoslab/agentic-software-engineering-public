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

# Prompting + Spec-Driven Development

**Agentic Software Engineering — Lecture 4**
Week 2 · Meeting 2 of 2

---

## The one idea

The two 9×9 attempts in the course archive are **the same task with different discipline**.

Requirements and specifications — not prompt cleverness — separate the outcomes.

---

<!-- _class: lead -->

# A tale of two attempts

---

## Attempt 1 opens with everything in one paragraph

> *"I have a tic tac toe game with a standard 3 by 3 board that I want to adapt to a larger game. Scale the game up for a 9 by 9 board where you need to get 5 in a row to win. Before changing the code, revise the @SPECS.md and @CLAUDE.md files to reflect the adaptations. Picking a move should now be a two step process where a player **first picks a column then a row** to play in…"*

Not careless — it even asks for docs before code.
But every requirement, delivered once, in one breath, never examined.

<!-- 0–10 min cold open. Transcript anchor: Attempt1 Session 12, ~line 1871. -->

---

## The drift

The opening prompt says: **column, then row.**

The shipped SPECS says: *"the player enters the **row first, then the column**."*

Somewhere in between, a requirement quietly flipped. Nobody decided it in a design conversation — **it drifted.**

That's what requirements-as-a-paragraph buys: *whatever survives the session.*

---

## Attempt 2 opens with a diagnosis

> *"@SPECS.md gives a good intro … but it is **sub-par for what a SPECS file should contain**. … Help me fully describe the specs of the program by re-writing @SPECS.md. … Use /grill-me to fully flush out the SPECS file **so we don't have to change it in the future**."*

The spec as a **contract** — written before any code, by interrogation, built to hold.

Neither attempt "failed." But one process produces requirements that hold their shape — and the other produces a second attempt.

<!-- Anchor: Attempt2 Session 14, ~line 2471. The transcripts share Sessions 1–13 as carried-forward history — don't present as independent runs. -->

---

<!-- _class: lead -->

# The five principles

---

## 1 — Provide specific instructions

> **Base:** "Fix the bug with the new login UI"
>
> **Better:** "When using the new login UI, the submit request does not seem to go through. Check that the submit request is handled properly so the page reacts correctly."

The model fills every unspecified gap with the *plausible*, not the intended.
Specificity is not verbosity — one precise sentence beats three vague ones.

<!-- 10–30 min: walk the handout, one 60-second live rewrite on the game per principle. L3's failure demo was principle 1 violated. -->

---

## 2 — Spec-driven development

> **Base:** "Add a new login page to our website"
>
> **Better:** "Use the login section in **@website-spec** to implement the login page"

The prompt names the work; **the spec carries the truth.**
(The rest of this lecture is why this scales like nothing else.)

---

## 3 — Give the agent the tools to check itself

> **Better:** "…Use the unit tests to check your implementation. Verify the UI with the browser tools at your disposal."

An agent that can run the tests catches its own plausible-but-wrong output
before you ever see it.

*(Presumes the tests exist and are trustworthy — that's your job. Full strength in Lecture 6.)*

---

## 4 — Promote positive behaviors

> **Base:** "Don't use bulleted lists in the report"
>
> **Better:** "Strive to use complete paragraphs that flow together"

Prohibitions have their place — safety rules are prohibitions —
but a prompt that is mostly "don't" produces cramped, evasive output.

**Say what good looks like.**

---

## 5 — Point at existing patterns

> **Better:** "Look at how the existing widgets are built (**@HotDogWidget** is a good example). Follow that same pattern for the calendar widget, using only libraries already in the project."

The cheapest specification you'll ever write: **the pattern is the spec.**
You saw this move in the L3 plan-mode demo — "like `random_move`, static method, registered in the dispatch."

---

<!-- _class: lead -->

# Requirement elicitation

---

## Make the agent interview *you*

`/grill-me` — thirteen lines — inverts the conversation:
the model probes for the decisions you haven't made yet.

> **Agent:** Who is this ConOps for — a grader, future developers, a stakeholder? What structure? *Recommendation: formal learning artifact, standard sections.*
> **Human:** Formal artifact; IEEE/AIAA sections; new `CONOPS.md` at root.
>
> **Agent:** Relationship to SPECS.md — may it reference it? Which scenarios? Which actors?
> **Human:** Restate what's needed but **do not reference SPECS** — implementation-independent. Scenarios: solo win, hot-seat, tie, invalid-input recovery.

Each answer **closes a branch of the design tree.**

<!-- 30–45 min. Condensed from Attempt2 Session 16, ~line 3860. -->

---

## The economics

The agent can only be as right as your requirements.

- Elicitation: **a few hundred tokens** of questions
- The alternative: **tens of thousands of tokens** of redevelopment

Elicitation converts unknown-unknowns into decisions *before* they become rework.

*(When is grilling a waste? Small, reversible, well-understood tasks. Discipline scales with stakes.)*

---

<!-- _class: lead -->

# ConOps vs SPECS

---

## The same behavior, two altitudes

> **ConOps:** "The player chooses a row and then a column; while the column is being chosen, the display marks the selected row."

> **SPECS:** "Validate row input: must be a digit 1–9, and `row_has_space(row)` must return `True`; on failure, re-prompt. … The row choice **sticks** once accepted. There is no back-out from the column prompt."

One tells you what the experience *is* — a user could confirm it.
The other legislates precisely enough to **write a failing test against** — including the edge nobody asked about.

<!-- 45–58 min. Hierarchy: ConOps → spec → code+tests. -->

---

<!-- _class: standout -->

## The punchline

The same ConOps produced the Python game **and the Java port** —
Maven, JaCoCo, 100% branch coverage. Nothing in it had to change.

**Specs are portable. Prompts are not.**
The ConOps outlived the codebase.

---

<!-- _class: lead -->

# Prompts shrink as artifacts grow

---

## The development prompt, pass by pass

**First pass:**
> *"Milestone 0 is complete, now implement milestone 1. /grill-me. When complete, allow me to review the code before transcribing and committing."*

**Fifth pass:**
> *"Implement Wave 2. /grill-me"*

Shorter prompt, **better results** (8/10 — "best end product so far").

---

## Where did the words go?

Into durable artifacts:

- requirements → **ConOps**
- structure and locked decisions → **development plan**
- conventions and cycle → **CLAUDE.md**

The prompt stopped *specifying* and started *pointing*.

**Move context out of the conversation and into artifacts** — the course's central trajectory. (Lecture 6 completes it.)

<!-- 58–68 min. -->

---

<!-- _class: lead -->

# Project 0 kickoff

---

## Everything today, applied to a markdown stack

A **personal knowledge base** on agentic SWE, yours all semester. Format: OKF — and a conformant note is just this:

```markdown
---
type: Concept
title: The agent loop
description: The while-loop-with-tools that turns a predictor into an actor.
tags: [agents]
---

An agent is a language model called in a loop by a harness…
See also [context windows](/concepts/context-window.md).
```

One required field (`type`) · reserved `index.md` + `log.md` · **broken links are legal** — they mark knowledge not yet written · Obsidian-viewable

<!-- 68–75 min. Worked example bundle ships in the starter repo — open it in Obsidian first. -->

---

## The kickoff *is* this lecture

1. **Elicit** — grill-me your KB's purpose and organization, *before creating files*
2. **Specify** — a one-page spec: taxonomy, `type` vocabulary, granularity, linking
3. **Scaffold** — Claude builds the bundle from your spec (plus its own CLAUDE.md)
4. **Seed** — 5+ notes from weeks 1–3, in your own words
5. **Stretch** — a conformance checker: principle 3, aimed at knowledge work

Due end of week 3 · checkpoints weeks 6, 10, 15

---

## Questions to think about

1. The ConOps never mentions Python — what exactly did that buy? What else could a team buy with the same property?
2. When is `/grill-me` a waste of time? Construct the smallest task where you'd still use it.
3. Why did the development prompt *shrink* pass over pass — what replaced each deleted clause?

---

## Before next lecture

- **Required:** Anthropic API docs — *Messages API* + *Tool use*, in depth (Ex. 4 builds on them)
- **Required:** Thorsten Ball, *How to Build an Agent* — ~300 lines of Go; you build the Python equivalent
- **Recommended:** *Building Effective Agents* ("agents" section); *Writing effective tools for agents*
- **Project 0 now open** · Exercise 2 due before Lecture 5

*Next: the emperor has no clothes.*
