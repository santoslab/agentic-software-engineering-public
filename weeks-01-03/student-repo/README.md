# Weeks 1–3 Student Materials

This directory collects the handouts, worked example, templates, and starter code
used by the foundations unit.

## Handouts

- [Tic-Tac-Toe transcript](handouts/handout-A-tictactoe-transcript.md) — a
  multi-session coding-agent transcript used in Exercise 1
- [Scaling to 9×9 excerpts](handouts/handout-B-9by9-excerpts.md) — contrasting
  prompt-first and elicitation-first development sessions
- [Agentic development principles](handouts/handout-agentic-principles.md)
- [NautilusTRX retrospectives](handouts/handout-nautilustrx-retrospectives.md)
- [Prompting cheat sheet](handouts/prompt-cheat-sheet.md)

PDF versions of the handouts are checked in for direct distribution. The Markdown
files are the editable sources.

## Examples and starter code

- [`pkb-example/`](pkb-example/index.md) — a tiny Open Knowledge Format bundle.
  Its unresolved `/concepts/tool-schemas.md` link is intentional: it demonstrates
  how an unwritten knowledge topic appears in Obsidian.
- [`tictactoe-starter/`](tictactoe-starter/) — the Python game and tests used by
  Project 1. It intentionally has no project specification or agent-memory file;
  creating those artifacts is part of the assignment.
- [`.claude-template/`](.claude-template/) — minimal, valid configuration and
  agent-template examples to adapt rather than copy blindly.

Exercise specifications live in [`../exercises/`](../exercises/), and the
student-facing prose for each class meeting lives in
[`../lecture-notes/`](../lecture-notes/).

## Verification

To run the starter tests from a clean Python 3.11+ environment:

```sh
cd tictactoe-starter
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
pytest
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`.

To rebuild a handout PDF, install Pandoc and XeLaTeX, then run:

```sh
pandoc FILE.md -f markdown-raw_tex -o FILE.pdf \
  --pdf-engine=xelatex -V geometry:margin=1in -V colorlinks=true
```

