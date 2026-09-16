# Software Engineering for Agentic Development

**Status:** skeleton. The folder layout, build tooling, and conventions are in place.
One demo is in place (`demos/note-specs/`). Lecture content, exercises, and readings
have not been written yet.

**Position in the course:** a three-week module that follows
[`weeks-01-03/`](../weeks-01-03/README.md) (foundations) and precedes
[`weeks-04-07/`](../weeks-04-07/README.md) (Project 1). Students are expected to have
completed the foundations unit. The folder name omits a week range on purpose: the
module is not tied to specific calendar weeks.

**Purpose:** review the software-engineering concepts that earlier courses introduce
(specification, requirements, verification, validation, process, planning, assurance)
and show how each applies when an agent, rather than a human, produces most of the
code. In agentic development these concepts determine what the agent is told, what
artifacts it must produce, and how its output is checked.

## Candidate topics

The topics below come from the course overview's learning outcomes. They have not yet
been organized into lectures; the lecture arc will be settled during content
development.

- Specification and realization: what a specification abstracts away, what it means
  for a realization to conform, and how conformance is assessed
- Requirements and concept of operations
- Verification and validation as distinct conformance questions
- Traceability between specifications, between a specification and its realization,
  and between artifacts and the changes that produced them
- Development process specifications: steps, gates, handoffs, and work decomposition
- Assurance: arguments and evidence that a specification is well-formed and that a
  realization conforms to it

## The arc

| Lecture | Title | Core question | Launches |
|---------|-------|---------------|----------|
| 01–06 | to be filled in | | |

## Exercises

| # | File | Assigned | Due | Effort | Needs |
|---|------|----------|-----|--------|-------|
| — | to be filled in | | | | |

Exercises in this module are intended to be small, completion-based demonstrations of
individual concepts (the course overview lists specification versus implementation,
verification, validation, plan mode, traceability, and assurance artifacts). Each
spec ends with a required-elements checklist, as in the other units.

## Files in this module

- `lectures-instructor-notes/lecture-NN-*.md` — outline-level lecture plans for the
  instructor (timings, demo setup and fallbacks, cut-if-long notes; format per
  `../templates/lecture-outline-template.md`). This folder plays the role that
  `lectures/` plays in the other units.
- `lecture-notes/lecture-NN-*.md` — full prose lecture notes, student-facing and
  self-contained; distribute per lecture (pandoc-convertible to PDF)
- `slides/lecture-NN-*.md` — Marp slide decks (`slides/build.sh` renders PDF and
  standalone HTML; diagrams kept as Mermaid sources in `slides/diagrams/`)
- `exercises/` — exercise specs
- `demos/` — in-class demo assets; `demos/note-specs/` is a specification-driven
  development demo on an agent-maintained note set
- `reading-list.md` — annotated readings, tagged
  [required] / [recommended] / [gap-filler]
- `student-materials/` — handouts and small example artifacts shipped with exercises

Each subfolder currently holds a README stating its purpose and file conventions.
Delete or rewrite those READMEs as real content arrives.

## Standing references (live outside this module)

- `../prompt-cheat-sheet.md` — the prompting principles handout
- `../technical-concepts.md` — concept index with curated documentation links
- `../templates/lecture-outline-template.md` — the instructor-outline format

## Conventions for this module

- **Lecture numbering.** Lecture files are numbered within the module, `lecture-01`
  through `lecture-06` (two meetings per week for three weeks). The global lecture
  numbers used by `weeks-04-07/` (07 through 14) are unchanged. This avoids a
  repository-wide renumbering now; revisit if a single global scheme is preferred.
- **Three artifacts per lecture.** Every lecture has an instructor outline, a
  student lecture-notes file, and a slide deck, and edits to one usually need to be
  reflected in the other two.
- **Outline header.** Instructor outlines use `**Unit:** module-software-engineering`
  in the template's header line.
- **Prose style.** Use direct, technical language. State a claim and the reason for
  it. Do not use slogans or motivational phrasing.
