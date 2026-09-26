# Weeks 1–3 — Foundations of Agent Development

**Unit thesis:** understand the machine (L1–L2), then the harness (L3–L5), then the
discipline (L4, L6). By week 4, nothing an agent does should look like magic, and
students should have felt — not just heard — why specs, context, and verification are
the load-bearing skills of agentic development.

Weeks 1–3 exercises are deliberately about **the feel of working with an agent**:
reading a real session, exploring an unfamiliar codebase, and building the loop
by hand. The software-engineering module
([`../module-software-engineering/`](../module-software-engineering/README.md))
follows this unit and assigns the first two projects: Project 0, the personal
knowledge base that Lecture 04 previews, and Project 1, the first *coding*
project with Claude.

## The arc

| Lecture | Title | Core question | Repo artifacts used | Launches |
|---------|-------|---------------|--------------------|----------|
| [01](lectures/lecture-01-course-intro-how-llms-work.md) | Course Intro + How LLMs Actually Work | What is the machine underneath? | bundled [tic-tac-toe starter](student-repo/tictactoe-starter/) (hook clip) | — |
| [02](lectures/lecture-02-from-llm-to-agent.md) | From LLM to Agent | How does a stateless predictor *act*? | toy agent (instructor's), raw API JSON | [Ex. 1](exercises/exercise-01-transcript-critique.md) |
| [03](lectures/lecture-03-claude-code-hands-on.md) | Claude Code Hands-On | How do I drive this deliberately? | bundled starter and lecture-note excerpts | [Ex. 2](exercises/exercise-02-codebase-comprehension.md) |
| [04](lectures/lecture-04-prompting-and-spec-driven-development.md) | Prompting + Spec-Driven Development | Why do requirements and specs dominate cleverness? | bundled 9×9 transcript/spec excerpts and NautilusTRX retrospectives | Project 0 preview |
| [05](lectures/lecture-05-anatomy-of-a-coding-agent.md) | Anatomy of a Coding Agent | What is the harness, in code I can read? | toy agent source, Messages API | [Ex. 4](exercises/exercise-04-toy-agent.md) |
| [06](lectures/lecture-06-context-cost-verification-and-the-road-ahead.md) | Context, Cost, Verification, and the Road Ahead | When can I trust the output — and at what price? | bundled retrospective, principles, starter coverage, and process excerpts | Project 1 tease |

## Exercises

| # | File | Assigned | Due | Effort | Needs |
|---|------|----------|-----|--------|-------|
| Ex. 1 | [exercise-01-transcript-critique.md](exercises/exercise-01-transcript-critique.md) | L02 | before L04 | 2–3 h | nothing (PDF handouts) |
| Ex. 2 | [exercise-02-codebase-comprehension.md](exercises/exercise-02-codebase-comprehension.md) | L03 | before L05 | 2–3 h | Claude Pro + Claude Code |
| Ex. 4 | [exercise-04-toy-agent.md](exercises/exercise-04-toy-agent.md) | L05 | start of wk 4 | 4–6 h | Python 3.11+, shared API key |

All completion-based: each spec ends with a required-elements checklist; satisfactory =
all elements present and honest (a documented failure counts; a missing reflection
doesn't).

**Project 0**, the personal knowledge base, is previewed at Lecture 04 and
assigned in the software-engineering module by
[`../module-software-engineering/project-0-pkb-brief.md`](../module-software-engineering/project-0-pkb-brief.md),
after that module's first two lectures have introduced the specification
concepts the project applies.

## Files in this unit

- `lectures/lecture-01…06-*.md` — outline-level lecture plans for the instructor
  (timings, demo setup/fallbacks, cut-if-long notes; format per
  `../templates/lecture-outline-template.md`)
- `lecture-notes/lecture-01…06-*.md` — full prose lecture notes, student-facing and
  self-contained; distribute per lecture (pandoc-convertible to PDF)
- `slides/lecture-01…06-*.md` — Marp slide decks (`slides/build.sh` renders PDF +
  presentable HTML; diagrams kept as Mermaid sources in `slides/diagrams/`)
- `exercises/` — the three exercise specs
- `demos/` — in-class demo assets; `demos/lecture-05-claude-code-demo/` holds the
  Lecture 05 Claude Code demo (starter project, instructor script, completed state)
- `reading-list.md` — consolidated annotated readings, tagged
  [required] / [recommended] / [gap-filler]
- `student-repo/` — student handouts, examples, templates, and starter code

## Standing handouts (live outside this unit)

- `../prompt-cheat-sheet.md` — the five prompting principles; Lecture 04's handout
- `../technical-concepts.md` — concept index with curated doc links; the "where is
  feature X taught" map
- `../specification-kinds.md` — the catalog of kinds of specification the course
  uses; the Project 0 brief's entry format is one of them
