# Software Engineering for Agentic Development

**Status:** in development. Lectures 01 through 05 (instructor outlines, lecture
notes, slide decks, diagrams), the two-part note-set demo, the two-part game demo,
the Reversi audit walkthrough, the Project 1 brief and starter, Exercises 1 and 2,
and the handouts are drafted and need instructor review before use; the brief's
due dates and effort estimates are not yet set. Lecture 06 has an instructor
outline; its notes, deck, and demo server are not yet written. Lecture 05 is a
walk-through of the Project 1 brief, step by step; its demo folder holds the
script and the instructor key.

**Position in the course:** a three-week module that follows
[`weeks-01-03/`](../weeks-01-03/README.md) (foundations) and precedes the
project unit. Students are expected to have completed the foundations unit. The
folder name omits a week range on purpose: the module is not tied to specific
calendar weeks.

**Purpose:** review the software-engineering concepts that earlier courses introduce
(specification, requirements, verification, validation, process, planning, assurance)
and show how each applies when an agent, rather than a human, produces most of the
code. In agentic development these concepts determine what the agent is told, what
artifacts it must produce, and how its output is checked.

## The arc

| Lecture | Title | Core question | Launches |
|---------|-------|---------------|----------|
| [01](lectures-instructor-notes/lecture-01-specifications-realizations-and-conformance.md) | Specifications, Realizations, and Conformance | What holds a specification and its realization together, and how do you check? | [Ex. 1](exercises/exercise-01-conformance-three-ways.md) |
| [02](lectures-instructor-notes/lecture-02-concept-of-operations-operations-and-the-invariant.md) | The Concept of Operations, Operations with Contracts, and the Specification as an Invariant | What is the system for, what may an agent do to it, and how is conformance kept while it changes? | [Ex. 2](exercises/exercise-02-operations-under-contract.md) |
| [03](lectures-instructor-notes/lecture-03-specifying-a-game-one-system-several-specifications.md) | Specifying a Game: One System, Several Specifications | What kinds of specification does a program need, and how does an agent help discover them? | Ex. 3 (optional) |
| [04](lectures-instructor-notes/lecture-04-verifying-a-game-tests-as-executable-specification.md) | Verifying a Game: Tests as Executable Specification | What does a test suite claim, and what does coverage not tell you? | — |
| [05](lectures-instructor-notes/lecture-05-reversi-kickoff-applying-the-method.md) | Reversi Kickoff: Applying the Method | Can you run the same moves on a game you were just handed? | Project 1, Phase 1 |
| [06](lectures-instructor-notes/lecture-06-mcp-the-tool-contract-as-a-specification.md) | MCP: The Tool Contract as a Specification | What changes when the reader of a contract is a machine? | — (Phase 1 continues; Stage E previewed) |

Across the six lectures the module introduces most of the kinds of
specification in the course catalog (`../specification-kinds.md`); Lecture 03's
table is the module's view of it, and Lecture 06 adds the last kind.

## The process documents

From Lecture 01 on, every demo repository and every starter carries a `process/`
folder beside its specifications. Its documents say how work proceeds with
respect to the specifications, and their rules are numbered so that reports can
cite them: `spec-audit.md` (AUD), `conops-audit.md` (AUDCON),
`development-rules.md` (DEV), `verification.md` (VER), `reporting.md` (RPT), and
a `README.md` that states the invariant they maintain. The set grows lecture by
lecture — Lecture 01 ships three documents, Lecture 02 six — and a rule, once
numbered, is never renumbered. `CLAUDE.md` in each repository is a short loader
that names the governing documents and the process documents and states two
rules.

## Exercises

| # | File | Assigned | Due | Effort | Needs |
|---|------|----------|-----|--------|-------|
| Ex. 1 | [exercise-01-conformance-three-ways.md](exercises/exercise-01-conformance-three-ways.md) | L01 | before L03 | 2–3 h | Claude Code, Python 3.11+, git |
| Ex. 2 | [exercise-02-operations-under-contract.md](exercises/exercise-02-operations-under-contract.md) | L02 | before L04 | 2–3 h | Claude Code, Python 3.11+, git |
| Ex. 3 (optional) | to write | L03 | before L05 | 1–2 h | Claude Code |

**Project 1** is assigned in this module — Phase 1 (specifications,
implementation, tests) at Lecture 05, due one week later — by
[`project-1-reversi-brief.md`](project-1-reversi-brief.md), with its starter in
`student-materials/reversi-starter/`. It is Stage A of the project unit's
Project 1, re-targeted to Reversi; Stages B–E of
[`../weeks-04-07/project-1-brief.md`](../weeks-04-07/project-1-brief.md) follow
it unchanged. Lecture 06 launches no further phase.

Exercises in this module are small, completion-based demonstrations of individual
concepts. Each spec ends with a required-elements checklist, as in the other units.

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
- `project-1-reversi-brief.md` — the Project 1 brief (Phase 1: from the sketch to
  fixtures, step by step)
- `demos/` — in-class demo assets; `demos/lecture-01-note-specs-demo/` is the
  note-set demo that Lectures 01 and 02 run in two parts (three repository
  states, two scripts); `demos/lecture-03-game-demo/` the game demo Lectures 03
  and 04 run in two parts; `demos/lecture-05-reversi-audit/` the Lecture 05
  walkthrough of the brief and its instructor key
- `reading-list.md` — annotated readings, tagged
  [required] / [recommended] / [gap-filler]
- `student-materials/` — handouts (Markdown sources with checked-in PDFs) and
  small example artifacts shipped with exercises

Each subfolder holds a README stating its purpose and file conventions.

## Standing references (live outside this module)

- `../specification-kinds.md` — the catalog of kinds of specification the
  course uses: purpose, audit, verification, and examples for each; cited from
  Lectures 01–06 and the Project 1 brief
- `../prompt-cheat-sheet.md` — the prompting principles handout
- `../technical-concepts.md` — concept index with curated documentation links
- `../templates/lecture-outline-template.md` — the instructor-outline format

## Conventions for this module

- **Lecture numbering.** Lecture files are numbered within the module, `lecture-01`
  through `lecture-06` (two meetings per week for three weeks).
- **Three artifacts per lecture.** Every lecture has an instructor outline, a
  student lecture-notes file, and a slide deck, and edits to one usually need to be
  reflected in the other two.
- **Outline header.** Instructor outlines use `**Unit:** module-software-engineering`
  in the template's header line.
- **Terminology.** *Verification* is the activity; a *verifier* performs it —
  human, agent, or algorithmic. *Instrument* and *checker* are not used for the
  role. A specification is *audited* (AUD, AUDCON); a realization is *verified*
  (VER); both produce reports in the forms of RPT.
- **Prose style.** Use direct, technical language. State a claim and the reason for
  it. Do not use slogans or motivational phrasing.
