# Exercise 1 — Transcript Critique

> **Assigned:** Lecture 02 · **Due:** before Lecture 04 · **Effort:** 2–3 hours
>
> **Requires:** nothing — all readings are provided as PDF handouts. No installs, no
> subscriptions. (Use the week to get Claude Pro sorted for Exercise 2.)

## Goal

Learn to read an agent session as an engineering artifact. Before you drive an agent
yourself, you will watch someone else do it across a real multi-session project — and
grade the *human*, not the model. This builds the vocabulary (steering, vagueness,
rework, loop structure) that the rest of the course assumes.

## Background

The transcripts come from the instructor's experiments building tic-tac-toe variants
with Claude Code. You get:

- **Handout A:** the complete 3×3 project transcript — 7 sessions, from project
  initialization through test development.
- **Handout B:** excerpts from two later experiments scaling the game to a 9×9 board
  with a 5-in-a-row win condition (plus the final 9×9 SPECS input-handling section for
  question 4):
  - **B1 (Attempt 1):** the session that scales the game by delivering all
    requirements in a single prose paragraph, with documentation revised in passing.
  - **B2 (Attempt 2):** the do-over — the session that declares the existing spec
    "sub-par" and rebuilds it by having the agent interview the developer *before any
    code*, and the later session where an implementation-independent Concept of
    Operations is built the same way.

## Task

Read Handout A in full and both excerpts in Handout B. Then answer the following in a
written critique:

1. **Steering (Handout A).** Identify three places where the human redirected,
   corrected, or constrained the agent. For each: quote the prompt, say what would
   likely have happened without it, and label it (correction / constraint /
   clarification).
2. **Vagueness → rework (Handout A).** Identify one place where an underspecified
   prompt caused avoidable work in a later exchange or session. Rewrite the original
   prompt using at least two of the five cheat-sheet principles (the cheat sheet is
   included with the handouts).
3. **The loop, observed (Handout A).** Pick one exchange and map it onto the agent
   loop from Lecture 02: what went into context, what tool activity is implied by the
   transcript, what came back, and how the human closed the iteration.
4. **Two disciplines (Handout B).** Compare how B1 and B2 open. What does the human
   ask for in each? What does the *shape* of the resulting conversation (who talks
   more, who asks the questions) tell you before you've seen a line of code? Then a
   forensic detail: B1's opening prompt specifies the move-input order one way; the
   final SPECS specifies it the other way (both are in your handouts). What does that
   drift suggest about requirements delivered as a single paragraph — and why do you
   think a second attempt exists at all?

## Deliverable

A 1–2 page markdown or PDF critique, structured by the four questions above. Quote
sparingly — one or two lines per citation, with the session number.

## Completion checklist (all required for satisfactory)

- [ ] Three steering points identified, each with quote, counterfactual, and label
- [ ] One vagueness case with a principled prompt rewrite (principles named)
- [ ] One exchange mapped onto the agent loop
- [ ] B1-vs-B2 comparison addressing conversation shape AND the trailing-spec risk
- [ ] 1–2 pages; session numbers cited

Honest observations that criticize the instructor's own prompting are not just
allowed — they're the point.
