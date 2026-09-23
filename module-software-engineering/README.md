# Software Engineering for Agentic Development

**Status:** in development. Lecture 01 (instructor outline, lecture notes, slide
deck, diagrams), Exercise 1, and the prompt-template handout are drafted and need
instructor review before use. The note-set demo that Lecture 01 runs is in place.
Lectures 02 through 06 are not yet written.

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

The topics below come from the course overview's learning outcomes. Lecture 01
covers the first of them. Lecture 02 is planned to treat the concept of operations
and the operations document as further expressions of intent, and to begin building
specifications with the agent. The remaining topics have not yet been assigned to
lectures.

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
| [01](lectures-instructor-notes/lecture-01-specifications-realizations-and-conformance.md) | Specifications, Realizations, and Conformance | What holds a specification and its realization together, and how do you check? | [Ex. 1](exercises/exercise-01-conformance-three-ways.md) |
| 02–06 | to be filled in | | |

## Exercises

| # | File | Assigned | Due | Effort | Needs |
|---|------|----------|-----|--------|-------|
| Ex. 1 | [exercise-01-conformance-three-ways.md](exercises/exercise-01-conformance-three-ways.md) | L01 | before L03 | 2–3 h | Claude Code, Python 3.11+, git |

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
- `demos/` — in-class demo assets; `demos/lecture-01-note-specs-demo/` is the
  note-set demo that Lecture 01 runs (two draft specifications, an agent that
  realizes them, three conformance-checking instruments)
- `reading-list.md` — annotated readings, tagged
  [required] / [recommended] / [gap-filler]
- `student-materials/` — handouts (Markdown sources with checked-in PDFs) and
  small example artifacts shipped with exercises; currently the Lecture 01
  starter-specifications handout and the specification-driven planning prompt
  template

Each subfolder holds a README stating its purpose and file conventions.

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
