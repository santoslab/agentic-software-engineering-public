# Weeks 1–3 — Foundations of Agent Development

**Unit thesis:** understand the machine (L1–L2), then the harness (L3–L5), then the
discipline (L4, L6). By week 4, nothing an agent does should look like magic, and
students should have felt — not just heard — why specs, context, and verification are
the load-bearing skills of agentic development.

Weeks 1–3 exercises are deliberately about **the feel of working with an agent**:
reading a real session, exploring an unfamiliar codebase, curating knowledge, and
building the loop by hand. The first *coding* project with Claude (tic-tac-toe scale)
starts in week 4.

## The arc

| Lecture | Title | Core question | Repo artifacts used | Launches |
|---------|-------|---------------|--------------------|----------|
| [01](lectures/lecture-01-course-intro-how-llms-work.md) | Course Intro + How LLMs Actually Work | What is the machine underneath? | bundled [tic-tac-toe starter](student-repo/tictactoe-starter/) (hook clip) | — |
| [02](lectures/lecture-02-from-llm-to-agent.md) | From LLM to Agent | How does a stateless predictor *act*? | toy agent (instructor's), raw API JSON | [Ex. 1](exercises/exercise-01-transcript-critique.md) |
| [03](lectures/lecture-03-claude-code-hands-on.md) | Claude Code Hands-On | How do I drive this deliberately? | bundled starter and lecture-note excerpts | [Ex. 2](exercises/exercise-02-codebase-comprehension.md) |
| [04](lectures/lecture-04-prompting-and-spec-driven-development.md) | Prompting + Spec-Driven Development | Why do requirements and specs dominate cleverness? | bundled 9×9 transcript/spec excerpts and NautilusTRX retrospectives | [Project 0](exercises/project-0-pkb-kickoff.md) |
| [05](lectures/lecture-05-anatomy-of-a-coding-agent.md) | Anatomy of a Coding Agent | What is the harness, in code I can read? | toy agent source, Messages API | [Ex. 4](exercises/exercise-04-toy-agent.md) |
| [06](lectures/lecture-06-context-cost-verification-and-the-road-ahead.md) | Context, Cost, Verification, and the Road Ahead | When can I trust the output — and at what price? | bundled retrospective, principles, starter coverage, and process excerpts | Project 1 tease |

## Exercises and Project 0

| # | File | Assigned | Due | Effort | Needs |
|---|------|----------|-----|--------|-------|
| Ex. 1 | [exercise-01-transcript-critique.md](exercises/exercise-01-transcript-critique.md) | L02 | before L04 | 2–3 h | nothing (PDF handouts) |
| Ex. 2 | [exercise-02-codebase-comprehension.md](exercises/exercise-02-codebase-comprehension.md) | L03 | before L05 | 2–3 h | Claude Pro + Claude Code |
| Project 0 | [project-0-pkb-kickoff.md](exercises/project-0-pkb-kickoff.md) | L04 | kickoff end of wk 3; semester-long | 2–3 h + ~30 min/wk | Claude Code, Obsidian (free) |
| Ex. 4 | [exercise-04-toy-agent.md](exercises/exercise-04-toy-agent.md) | L05 | start of wk 4 | 4–6 h | Python 3.11+, shared API key |

All completion-based: each spec ends with a required-elements checklist; satisfactory =
all elements present and honest (a documented failure counts; a missing reflection
doesn't).

## Files in this unit

- `lectures/lecture-01…06-*.md` — outline-level lecture plans for the instructor
  (timings, demo setup/fallbacks, cut-if-long notes; format per
  `../templates/lecture-outline-template.md`)
- `lecture-notes/lecture-01…06-*.md` — full prose lecture notes, student-facing and
  self-contained; distribute per lecture (pandoc-convertible to PDF)
- `slides/lecture-01…06-*.md` — Marp slide decks (`slides/build.sh` renders PDF +
  presentable HTML; diagrams kept as Mermaid sources in `slides/diagrams/`)
- `exercises/` — the three exercise specs + Project 0 kickoff spec
- `reading-list.md` — consolidated annotated readings, tagged
  [required] / [recommended] / [gap-filler]
- `student-repo/` — student handouts, examples, templates, and starter code

## Standing handouts (live outside this unit)

- `../prompt-cheat-sheet.md` — the five prompting principles; Lecture 04's handout
- `../technical-concepts.md` — concept index with curated doc links; the "where is
  feature X taught" map
