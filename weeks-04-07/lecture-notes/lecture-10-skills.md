# Lecture 10 — Skills: Packaging Reusable Expertise

> Week 5, meeting 2 of 2. Companion reading for the lecture; self-contained.
> Assigns the **Stage B custom skill** (a required element of the stage).

## You have typed this prompt before

Somewhere in the last two weeks you retyped a prompt. Maybe "review this diff
against my SPEC and flag anything the spec doesn't cover." Maybe "walk me through
this file the way you did yesterday." The third time you type a prompt, you are
maintaining software by hand — you have a program that lives in your fingers and
degrades a little with every retelling.

Classical software engineering named this problem decades ago. Mature
organizations keep **process asset libraries**: checklists, runbooks, templates,
review protocols — organizational memory that survives the person who wrote it.
The pilot's pre-flight checklist is the canonical example: expertise, paid for
once (sometimes dearly), packaged so every future flight gets it for free.

A **skill** is that idea with an executor attached. It is a file in your repo
(`.claude/skills/<name>/SKILL.md`) containing a procedure; the agent discovers
it, and either you invoke it by name (`/grill-me`) or the agent invokes it when
its trigger matches. Version-controlled, diffable, reviewable — a checklist that
runs.

## Anatomy: a methodology in thirteen lines

You have been *using* a skill since week 2. Here is grill-me, whole:

```markdown
---
name: grill-me
description: Interview the user relentlessly about a plan or design until
  reaching shared understanding, resolving each branch of the decision tree.
  Use when user wants to stress-test a plan, get grilled on their design, or
  mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until
we reach a shared understanding. Walk down each branch of the design
tree resolving dependencies between decisions one by one.

If a question can be answered by exploring the codebase, explore
the codebase instead.

For each question, provide your recommended answer.
```

Three observations, in rising order of importance:

1. **The body is a procedure, not a wish.** Every sentence is an instruction with
   a discipline attached: *walk each branch*, *resolve dependencies one by one*,
   *explore instead of asking*, *always recommend*. Compare the degenerate
   version — "ask me good questions about my plan" — and you can predict the
   degraded behavior.
2. **The description is the trigger contract.** It is what the model reads when
   deciding whether this skill applies to what you just said. It names the
   situations ("stress-test a plan"), and the literal invocation ("mentions
   'grill me'"). It is an API doc for a function whose caller is a language
   model.
3. **There is nothing else.** No code, no config, no registration step. A skill
   is a prompt with a name, a trigger, and a discipline. The barrier to writing
   one is fifteen minutes — which is exactly why the interesting question is
   *what deserves packaging*, not *how*.

## The four roles, with course-native examples

Skills earn their keep in four recurring roles. You have already met three in
this course's own repositories:

| Role | Question it answers | Course-native example |
|---|---|---|
| **Elicitation** | What should we build? | `grill-me` — the interview protocol |
| **Documentation** | What did we do? | `transcribe` — the experiment repos' transcript convention (verbatim prose, user input as quote blocks, session breaks, amend-don't-recreate) packaged so every session's log comes out identical |
| **Comprehension / review** | What is this? / Is this right? | `walk-me-through` — guided reading of unfamiliar code; your Exercise 2 workflow, packaged |
| **Scaffolding** | Start me correctly | none native yet — the demo builds one today |

The demo skill is worth previewing here because it shows what packaging really
captures. Your Stage B repo now has a `migrate.py` with numbered migration
functions and three unstated conventions: new migrations are appended, never
reordered; each gets the next number; deferred consequences go to BACKLOG.md.
Nothing in the repo *says* any of that. A `/new-migration` skill says it:

```markdown
---
name: new-migration
description: Scaffold the next numbered migration in migrate.py from a short
  description of the schema change. Use when adding any table, column, or index.
---

Read migrate.py and infer the migration conventions (numbering, naming,
idempotency, the MIGRATIONS list). Add the next numbered migration function
implementing the requested change. Never modify or reorder existing
migrations. If the change has consequences you are not implementing (data
backfill, index rebuild), add a BACKLOG.md entry saying so.
```

The expertise being packaged is not "how to write SQL" — the agent knows that.
It is *your project's conventions*: the local rules that exist only in your head
and your git history until a skill states them. That is what "process asset"
means at personal scale.

## Where knowledge lives: the placement table

You now have three homes for project knowledge, and Thursday adds the fourth.
Choosing correctly is the actual skill (the meta-skill, if you must):

| Home | Loaded | Right for | Cost of misplacement |
|---|---|---|---|
| **CLAUDE.md** | Every session, always | Laws and standing facts: the coverage gate, the layering rule, build commands | Bloat — every session pays tokens for what few sessions need |
| **Skill** | On demand (invoked or triggered) | Procedures needed *sometimes*: scaffold a migration, run the spec review | A procedure in CLAUDE.md runs never; a law in a skill gets skipped |
| **Hook** (Thursday) | Automatically, at an event | Actions needed *every time*: cost logging at session end | A hook-shaped task left as a skill depends on remembering — and gets skipped |
| **Your PKB** | You, across projects | Lessons that outlive this repo | A career lesson trapped in one repo's CLAUDE.md |

Worked placement, using this week's own facts: the engine coverage law —
CLAUDE.md (it governs every session). The migration scaffold — skill
(occasional, procedural). Cost logging — hook (every session, zero judgment).
"Migrations should be append-only, and here is the update-anomaly argument from
Lecture 09" — your PKB, because it will be true in every system you ever build,
and CLAUDE.md dies with the repo.

The smells of misplacement are worth naming because you will meet both this
semester: a CLAUDE.md pushing 300 lines (laws drowning in procedures — sessions
get slower and *less* obedient, because everything emphasized is nothing
emphasized); and a skill nobody has invoked in three weeks that everyone was
supposed to run before commits (that is a hook, or a gate — Lecture 20 returns
to exactly this at team scale).

## The Stage B requirement

From the brief: build **one** skill — scaffolding, review, or documentation type
— and *use it* at least once in Stage C or D, citing where. The type menu maps
to the table above; elicitation is excluded only because grill-me already exists
and copying it teaches nothing.

Two grading notes stated plainly. First, this is completion-plus-credibility: a
skill that was obviously never run — no invocation in any transcript, no output
it could have produced, conventions it names that your repo doesn't have — is
worse than no skill, because it is documentation that lies. Second, small is
correct: the best student skills will be ten lines that kill one real
repetition. The over-scoped ones ("/do-stage-c") fail on their own weight.

Choose by looking backward, not forward: what have you *already* typed twice?
That is your skill. If nothing qualifies yet, wait — Stage C will oblige.

## Questions to think about

1. What makes a skill rot? Name the specific commit in your Project 1 future
   that would silently break `/new-migration` as written above — and the
   maintenance rule that prevents it. (Hint: the skill and the conventions it
   infers live in the same repo. When must they change together?)
2. Why is a wrong `description` worse than a wrong body? Trace what the model
   does with each at the moment of deciding whether to invoke.
3. The transcribe skill enforces a documentation *format*. Your Stage B skill
   options include a documentation type. What is the difference between a
   documentation skill worth having and "the agent writes some docs"? (What
   makes output *checkable*?)
