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

# Skills: Packaging Reusable Expertise

**Agentic Software Engineering — Lecture 10**
Week 5 · Meeting 2 of 2 · assigns the **Stage B skill**

---

## The one idea

A skill is a **process asset**: expertise you paid for once, packaged so every future session gets it free.

The `description` line is its API.

---

## You've typed this prompt before

The third time you retype a prompt, you are maintaining software by hand — a program that lives in your fingers and degrades with every retelling.

Classical SE named this: **process asset libraries** — checklists, runbooks, templates. The pilot's pre-flight checklist: expertise paid for once (sometimes dearly), packaged forever.

A skill = that idea, with an executor attached.

<!-- 0-10 min. -->

---

## Anatomy: a methodology in 13 lines

```markdown
---
name: grill-me
description: Interview the user relentlessly about a plan or design
  until reaching shared understanding... Use when user wants to
  stress-test a plan... or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until
we reach a shared understanding. Walk down each branch of the design
tree resolving dependencies between decisions one by one.

If a question can be answered by exploring the codebase, explore
the codebase instead.

For each question, provide your recommended answer.
```

---

## Three observations, rising in importance

1. **The body is a procedure, not a wish** — every sentence carries a discipline (*walk each branch*, *explore instead of asking*, *always recommend*)
2. **The description is the trigger contract** — it's what the model reads when deciding the skill applies. An API doc whose caller is a language model
3. **There is nothing else** — no code, no registration. Fifteen minutes to write one. So the real question is *what deserves packaging*

<!-- 10-24 min. -->

---

## The four roles, with course-native examples

| Role | Question | Example |
|---|---|---|
| Elicitation | What should we build? | `grill-me` |
| Documentation | What did we do? | `transcribe` — the transcript convention, enforced |
| Comprehension / review | What is this? | `walk-me-through` — your Ex. 2, packaged |
| Scaffolding | Start me correctly | **none native — we build one now** |

---

<!-- _class: standout -->

## Demo: build a skill in ten minutes

`/new-migration` — scaffold the next numbered migration, *in this repo's style*

<!-- 38-54 min. The expertise packaged is YOUR conventions, not "how to write SQL". -->

---

## What the demo skill actually captures

Your repo has three **unstated** conventions: migrations are appended, never reordered; next number wins; deferrals go to BACKLOG.md.

```markdown
Read migrate.py and infer the migration conventions (numbering,
naming, idempotency, the MIGRATIONS list). Add the next numbered
migration function implementing the requested change. Never modify
or reorder existing migrations. If the change has consequences you
are not implementing, add a BACKLOG.md entry saying so.
```

Nothing in the repo *said* any of that — now something does, and it **runs**.

---

## Where knowledge lives

| Home | Loaded | Right for | Misplacement cost |
|---|---|---|---|
| **CLAUDE.md** | Always | Laws, standing facts | Bloat — everyone pays for what few need |
| **Skill** | On demand | Occasional procedures | A law in a skill gets skipped |
| **Hook** (Thu) | At an event | Every-time actions | A hook-shaped skill depends on remembering |
| **PKB** | You, forever | Cross-project lessons | A career lesson trapped in one repo |

Worked: coverage law → CLAUDE.md · migration scaffold → skill · cost logging → hook · "append-only migrations, and why" → **PKB**

<!-- 54-66 min. Smells: the 300-line CLAUDE.md; the skill nobody has run in 3 weeks. -->

---

## The Stage B requirement

Build **one** skill — scaffolding, review, or documentation — and **use it in Stage C or D, citing where**.

- Completion **plus credibility**: a skill that was obviously never run is worse than none — it's documentation that lies
- **Small is correct**: the best will be ten lines that kill one real repetition
- Choose by looking *backward*: what have you already typed twice?

---

## Questions to think about

1. Name the future commit that silently breaks `/new-migration` — and the maintenance rule that prevents it.
2. Why is a wrong `description` worse than a wrong body?
3. What separates a documentation skill worth having from "the agent writes some docs"? (What makes output *checkable*?)

---

## Before Tuesday

- [required] Flask docs: Quickstart + Testing
- [recommended] The gate-table excerpt in Tuesday's notes
- **PKB checkpoint 1 due Tuesday**

**Tuesday: the testing taxonomy grows teeth.**
