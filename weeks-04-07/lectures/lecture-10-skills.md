# Lecture 10 — Skills: Packaging Reusable Expertise

> **Unit:** weeks-04-07 · **Week 5, meeting 2 of 2** · 75 minutes
>
> **Thesis:** A skill is a process asset — expertise you paid to acquire once,
> packaged so the next session, teammate, or agent gets it for free; the
> description line is its API.

## Learning objectives

After this lecture, students can:

1. Recognize when a repeated prompt has earned packaging (the rule of three) and
   when packaging would be premature.
2. Write a complete skill: frontmatter whose `description` works as a trigger
   contract, and a body that states a procedure, not a wish.
3. Classify skills by role — elicitation, scaffolding, review, documentation — and
   name a course-native example of each.
4. Choose the right home for project knowledge: CLAUDE.md (always loaded), a skill
   (on demand), or a hook (automatic) — and justify the choice.

## Before class

- [required] Claude Code docs: Skills / slash commands.
- [recommended] The grill-me skill file, re-read as a program.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–10 | Cold open: you've typed this three times | By now everyone has retyped some prompt: "update the docs after schema changes," "review this diff against my SPEC." Classical SE solved this decades ago — process asset libraries, checklists, runbooks: organizational memory that survives the person. Skills are that idea with an executor attached. |
| 10–24 | Anatomy of a 13-line skill | grill-me, whole, on one slide. Frontmatter: `name`; `description` — **the trigger contract**: it's what the model reads when deciding the skill applies, so it's written like an API doc ("Use when the user wants to stress-test a plan… or mentions 'grill me'"). Body: a procedure — imperative, bounded, with an output obligation ("provide your recommended answer"). Note what's absent: no code, no config. A skill is a prompt with a name, a trigger, and a discipline. |
| 24–38 | The four roles, with native examples | *Elicitation*: grill-me (interrogate until the decision tree is resolved). *Documentation*: transcribe (the course repo's transcript convention — verbatim prose, `>` blockquotes, session breaks — is a skill enforcing a format). *Comprehension/review*: walk-me-through (guided reading of unfamiliar code — your Ex. 2, packaged). *Scaffolding*: none native yet — we build one today. Each role answers a different question: what should we build / what did we do / what is this / start me correctly. |
| 38–54 | Demo 1 — build a skill in ten minutes | Live: create `/new-migration` — a scaffolding skill that takes a description ("add a played_at index") and produces the next numbered migration function in the project's `migrate.py` style, plus the BACKLOG.md line if it defers anything. Write SKILL.md by hand (it's ~15 lines), run it on the demo repo, watch it follow the house style. The lesson: the skill encodes *your* conventions — that's the expertise being packaged. |
| 54–66 | Where knowledge lives | The decision table: CLAUDE.md = facts every session needs (laws, commands, layout — paid on every load, so keep it lean); skill = procedures needed *sometimes*, invoked by name or trigger; hook (Thursday) = actions needed *always at an event*, no human in the loop. Worked example: the coverage law (CLAUDE.md — it governs everything), the migration scaffold (skill — occasional, procedural), cost logging (hook — every session, mechanical). Wrong-home smells: a 300-line CLAUDE.md; a skill nobody remembers to run that should be a hook. |
| 66–75 | Stage B skill assignment + Q&A | The brief's requirement: build one skill — scaffolding, review, or documentation type — and *use it* in Stage C or D, citing where. Grading is completion + credibility: a skill that was obviously never run is worse than none. Preview: in Project 2, team process itself gets encoded this way (L20). |

## Demos

### Demo 1 — Build a skill in ten minutes

- **Artifacts:** the instructor's Stage-B-complete tictactoe repo (has
  `migrate.py` with two numbered migrations and a BACKLOG.md); empty
  `.claude/skills/new-migration/` directory.
- **Setup (before class):** rehearse the ten-minute cut; have the target SKILL.md
  text in your head, not on a crib sheet — writing it live *is* the demo; a
  candidate migration request chosen ("index on games.played_at").
- **Script:** (1) show the repetition it kills (two hand-written migrations that
  follow a convention nothing states); (2) write SKILL.md live: name,
  description-as-trigger, body: read `migrate.py`, infer the convention, add the
  next numbered function, never reorder existing ones, note deferrals in
  BACKLOG.md; (3) run `/new-migration add an index on games.played_at`; (4) diff —
  the new function matches house style; (5) run `migrate.py` twice (still
  idempotent).
- **Expected outcome:** a skill goes from nothing to working in one class block,
  and visibly encodes conventions the repo only *implied* before.
- **Fallback:** pre-recorded run; the SKILL.md builds up as three progressive
  slides (frontmatter → trigger → procedure).

## Discussion prompts

1. What makes a skill rot, and what's the maintenance story? (Conventions drift
   out from under it — same failure mode as documentation, same cure: it lives in
   the repo and changes in the same commits.)
2. Your Stage B skill: which type did you pick and — the real question — when will
   it *actually run* in Stage C or D? Name the moment.
3. Why is a wrong `description` worse than a wrong body?

## Assigned after class

- Readings (for L11):
  - [required] Flask docs: Quickstart + Testing (test client sections).
  - [recommended] Your GATES.md-to-be: skim the gate-table excerpt in the
    [Lecture 11 notes](../lecture-notes/lecture-11-the-web-layer.md)
    excerpt in today's notes before Tuesday.
- Project: Stage B continues; the custom skill is now a required element.
- **PKB checkpoint 1 is due at L11** — mechanics in the Project 0 spec.

## Instructor notes

- **Cut if running long:** the four-roles block (24–38) can drop walk-me-through;
  the where-knowledge-lives table (54–66) is load-bearing for L12 — compress it
  before cutting it.
- **Risks:** the live skill may need one nudge to follow the numbering convention
  — that's fine, narrate it ("the skill body wasn't specific enough; watch me
  tighten it"), which is truer to real skill authoring than a clean take. Students
  routinely over-scope their Stage B skill; steer them to the smallest procedure
  they have already repeated twice.
- **Variants:** collect two candidate repeated-prompts from the room at minute 5
  and build whichever gets the vote, if you trust the improv.
