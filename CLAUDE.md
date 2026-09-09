# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Public materials for a graduate course on agentic software engineering. It is almost entirely Markdown content — there is no application to build at the root. The only runnable code is the Python starter in `weeks-01-03/student-repo/tictactoe-starter/`; everything else "builds" into slide decks (Marp) or handout PDFs (Pandoc).

## Commands

**Build all slide decks for a unit** (renders Mermaid diagrams, then every `lecture-*.md` to PDF + standalone HTML; needs Node, PDF export needs Chrome):

```sh
weeks-01-03/slides/build.sh   # or weeks-04-07/slides/build.sh (identical scripts)
```

**Build one deck / one diagram:**

```sh
npx -y @marp-team/marp-cli@latest --allow-local-files lecture-NN-*.md -o lecture-NN-*.pdf
npx -y @mermaid-js/mermaid-cli -i diagrams/NAME.mmd -o diagrams/NAME.svg
```

`--allow-local-files` is required because decks embed local `diagrams/*.svg`.

**Rebuild a handout PDF** (handout PDFs, unlike slide output, are checked in for distribution):

```sh
pandoc FILE.md -f markdown-raw_tex -o FILE.pdf \
  --pdf-engine=xelatex -V geometry:margin=1in -V colorlinks=true
```

**Run the tic-tac-toe starter tests:**

```sh
cd weeks-01-03/student-repo/tictactoe-starter
python -m venv .venv && . .venv/bin/activate
python -m pip install -r requirements-dev.txt
pytest                          # all tests
pytest tests/test_game.py::test_name   # single test
```

## Structure: three parallel artifacts per lecture

Each unit (`weeks-01-03/`, `weeks-04-07/`) keeps **three versions of every lecture**, and edits to lecture content usually need to be reflected across all three:

- `lectures/lecture-NN-*.md` — instructor outline: timings, demo scripts with fallbacks, cut-if-long notes. Format is defined by `templates/lecture-outline-template.md` (75-minute blocks, student-testable objectives, required-elements structure).
- `lecture-notes/lecture-NN-*.md` — full prose, student-facing and self-contained; distributed per lecture, pandoc-convertible to PDF.
- `slides/lecture-NN-*.md` — Marp decks. Speaker notes are HTML comments (presenter view via P in the HTML output). Each deck carries a shared inline style block (purple theme, `lead`/`source`/`code-dense`/`references` section classes) in its front matter — copy it from an existing deck when creating a new one.

Diagrams live as Mermaid sources in `slides/diagrams/*.mmd` (the editable source of truth, agent-maintainable); slides embed the pre-rendered `.svg`. Slide `.pdf`/`.html` output and `.svg` files are gitignored build artifacts — never commit them.

Each unit README (`weeks-01-03/README.md`, `weeks-04-07/README.md`) is the map: the lecture arc, which exercise each lecture launches, and what is ready vs. draft. Files that identify themselves as drafts need instructor review before being assigned.

## Other top-level pieces

- Root standing handouts: `course-overview.md`, `technical-concepts.md` (the "where is feature X taught" index), `prompt-cheat-sheet.md`, `glossary.md`.
- `carbon-layer/` — source material (book chapters, masterclass transcript, figures) used to draft the harness-anatomy lectures. Reference corpus, not a course deliverable.
- `weeks-01-03/student-repo/` — handouts (Markdown sources + checked-in PDFs), the `pkb-example/` knowledge base, and `tictactoe-starter/`.
- `weeks-04-07/student-materials/` — per-stage artifacts shipped with the Project 1 brief; its README states what is exported to students and when.
- `.claude-template/` — a *teaching artifact* students copy into their own projects, not this repo's live Claude Code configuration. Keep it minimal and permission-free.

## Intentional quirks — do not "fix"

- `pkb-example` contains one unresolved `/concepts/tool-schemas.md` link on purpose (demonstrates links to unwritten knowledge).
- `tictactoe-starter` deliberately ships with no project specification and no agent-memory file — creating those is the student assignment.
- Tic-Tac-Toe, NautilusTRX, and lost-communities are historical case studies; the private prototype repositories are intentionally not referenced as prerequisites.

## Licensing

Dual-licensed with a content/code boundary (see `LICENSING.md`): instructional prose, slides, and media are CC BY 4.0; code, scripts, configuration, templates, and starters are MIT. Keep new files on the right side of that boundary.
