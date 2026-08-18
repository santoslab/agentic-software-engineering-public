# Lecture 07 — Project 1 Kickoff — Own the Spec: ConOps, Classical and Agentic

> Week 4, meeting 1 of 2. Companion reading for the lecture; self-contained.
> Launches **Project 1, Stage A** (see `project-1-brief.md`).

## The gap you are handed

Today you receive a working program: a 9x9 tic-tac-toe variant where five in a row
wins, with menus, a two-player mode, a computer opponent that plays randomly, and
about ninety green pytest tests. It is decent code. You could read all of it in an
hour.

What it does not have is a specification. No SPEC, no ConOps, no design note, not
even a README that says what the rules are. If you want to know whether a move that
was rejected costs you your turn, there is exactly one place to find out: the code.

That absence is not an oversight. **Closing it is Stage A.** By the end of this week
you will have written the two documents this program should have shipped with, made
one real change governed by them, and bound the project's first law into CLAUDE.md.
Everything else in Project 1 — the database, the web layer, the TypeScript port, the
MCP server — will stand on what you write this week. If that sounds dramatic, wait
until Stage D, when your spec has to survive a language it has never met.

You have seen this movie before, from the outside. In Lecture 04 we read the two
9x9 experiment transcripts: the first attempt delivered its requirements as one
prose paragraph and drifted (the prompt said column-then-row; the shipped spec said
row-then-column; nobody decided). The second attempt began by declaring the
inherited spec "sub-par" and rebuilding it by interrogation *before touching code* —
"so we don't have to change it in the future." Project 1 starts where Attempt 2
ended up: with you owning the spec, from the first day.

## What a spec does for an agent

The classical answer to "why write a spec?" is about human coordination: shared
understanding, contracts between teams, a place for review to bite. All still true.
But agentic development adds three loads the spec carries that nothing else can.

**1. Grounding.** A conversation with an agent is disposable — it rots, it gets
compacted, it ends. The spec is read fresh at the start of every session, by every
session, forever. When Lecture 06 told you to move context out of the conversation
and into artifacts, this is the artifact it meant. An agent with a good SPEC.md
starts every session already knowing what the program must do; an agent without one
starts every session guessing from code.

**2. Drift prevention.** The Attempt 1 bug is worth restating precisely, because
you are about to be vulnerable to it. The opening prompt asked for a two-step move:
*pick a column, then a row*. The SPECS.md that shipped says: *pick a row, then a
column*. The code does what the spec says. Which one was intended? Nobody knows —
no artifact records a decision, because no one ever made one; two artifacts just
quietly disagreed and one of them won by accident. The rule that prevents this is
blunt: **when the code and the spec disagree, one of them is wrong on purpose** —
a human rules, and the ruling is a commit.

**3. Portability.** The 9x9 project's ConOps was written for a Python program. It
was later handed, essentially unchanged, to a session that produced a Java
implementation with its own build system and a 100% branch-coverage gate. The
prompts from the Python sessions would have been useless — they are full of Python.
The ConOps crossed the language boundary because it never mentioned a language.
*Specs are portable; prompts are not.* In week 7 your SPEC.md makes the same trip,
to TypeScript, and the fixtures will check what survived.

## ConOps and SPEC are different documents

You are writing two documents this week, and they answer different questions.

A **ConOps** (Concept of Operations — the classical reference is IEEE Std 1362)
answers: *what is this system, in the world, for its users?* It is written from the
user's side of the screen and it is implementation-free. The section skeleton is
scope, operational environment, user classes, and representative scenarios; yours
is one page.
The fastest test of a ConOps: **it never says "Python," "class," "database," or
"terminal" unless the user would.**

A **SPEC** answers: *exactly what does the system do?* It is a behavioral contract:
precise, testable, edge-case-bearing. It is allowed to say things no user would ever
say.

The ConOps should describe the player's goals, actors, environment, and representative
scenarios without naming implementation mechanisms. The SPEC should turn those
observations into precise clauses whose acceptance tests are obvious.

> **Public-edition note:** the starter-specific mini-ConOps, example SPEC clauses,
> and canonical edge-case list used during the live class exercise are omitted here.
> They overlap Stage A's assessed work. In class, build and verify those examples
> directly from the starter rather than treating an instructor example as an answer
> key.

## Reverse-engineering the contract

Stage A's core exercise is elicitation running in the opposite direction from
Lecture 04. There, the agent grilled *you* until your intent was pinned down. Here,
*you* (with the agent's help) grill the *code* until its behavior is pinned down —
and, crucially, until you have found the places where its behavior is a **decision**
rather than a necessity.

During the live exercise, read a small public method path by path and ask what each
branch implies for callers. Compare the implementation with its tests, distinguish
language accidents from portable behavior, and identify where a reasonable
implementer could choose differently. Do not transcribe the code into English:
record decisions and their evidence.

## Binding the law: CLAUDE.md and plan mode

Two process rules start today and never stop.

**The coverage law lives in CLAUDE.md.** Your project CLAUDE.md must state: the
engine (`game.py`) holds 100% branch coverage, always, enforced by `pytest --cov`.
Why there and not in your prompts? Because prompts protect one session and
CLAUDE.md protects all of them — you learned the three kinds of memory in Lecture
06; laws go in the layer every session loads. The Java port's CLAUDE.md states its
coverage gate as flatly as a compiler error, and its sessions obeyed it. Write
yours the same way.

**Plans are artifacts.** Every stage's main build runs through plan mode, and the
approved plan gets committed under `plans/`. Partly this is for you — a plan you
can re-read beats a plan you remember. Partly it is process evidence: your grader
reads your git history, and "spec amendment, then plan, then implementation" is
the shape that history is supposed to have. And partly it is rehearsal: in Project
2, committed plans become how *teammates* review what an agent is about to do
before it does it.

## Stage A, concretely

From the brief, compressed: (1) elicit `SPEC.md` from the starter — including
explicit positions on at least two discovered edge cases; (2) write the one-page
`CONOPS.md`; (3) make one spec-driven extension — recommended: configurable board
size and win length, whose ripple through the hard-coded "1-9" prompt strings and
the render function is next lecture's worked example; (4) bind the coverage law in
`CLAUDE.md`. The required-elements checklist in the brief is the definition of
done. The evidence rule to tattoo somewhere: **the spec amendment is committed
before or with the implementing change — never after.**

## Questions to think about

1. The starter works and its tests are green. Name the *first concrete moment* in
   Stages B-E where the absence of a spec would actually hurt — what goes wrong,
   and who notices?
2. Pick one ambiguous behavior from your own elicitation. Write two competing SPEC
   clauses, choose one, and explain what evidence or design goal tipped you.
3. Stage B adds persistence. Which document changes, what exactly changes in it,
   and what does that tell you about where the session/persistence boundary should
   be documented?
