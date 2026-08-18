# Agentic Software Engineering

Public course materials for a graduate course on building software with AI coding
agents through specifications, repeatable workflows, review, and verification.

## Status

This repository is a curated snapshot of course development through weeks 1–7,
exported from planning commit `43876fb` on 2026-08-18. The course is still being
developed: published materials may change, and files that explicitly identify
themselves as drafts are not yet ready to assign without instructor review.

## Start here

- [Course overview](course-overview.md) — purpose, semester arc, and learning outcomes
- [Weeks 1–3: Foundations](weeks-01-03/README.md) — LLMs, agent architecture,
  prompting, context, and verification
- [Weeks 4–7: The Growing Tic-Tac-Toe](weeks-04-07/README.md) — a staged project in
  specification-driven agentic development
- [Technical concepts](technical-concepts.md) — topic index and further reading
- [Prompting cheat sheet](prompt-cheat-sheet.md) — compact prompting principles

Each unit contains instructor lecture outlines, student-facing lecture notes, Marp
slide sources, assignments, and supporting student materials. The unit READMEs
identify what is ready and how the pieces fit together.

## Prerequisites

The course exercises assume:

- Git and a command-line development environment
- Python 3.11 or newer for the foundations exercises and starter project
- Claude Code with an appropriate account for agent-based exercises
- Node.js and TypeScript for the Project 1 porting stage

Pandoc with XeLaTeX and Marp are optional; they are needed only to regenerate PDF
handouts or rendered slide decks from the checked-in Markdown sources.

## Notes for readers

The named Tic-Tac-Toe, NautilusTRX, and lost-communities projects are historical
course case studies. Required readings and exercises in this public edition use
materials bundled here; the private prototype repositories are not prerequisites.

The example personal knowledge base intentionally contains one unresolved
`/concepts/tool-schemas.md` link. It demonstrates that Open Knowledge Format and
Obsidian vault-root links may point to knowledge that has not been written yet.

## Licensing

Course prose and media are licensed under CC BY 4.0; repository code and
configuration are licensed under MIT. See [LICENSING.md](LICENSING.md) for the
boundary, attribution, and third-party-material exceptions.

