# In-class demo assets

This folder holds the materials for live demonstrations run during lectures.

- Folder naming: `lecture-NN-<slug>-demo/` once the lecture that runs the demo is
  fixed. Until the lecture arc is settled, demo folders carry only the slug.
- Contents: `demo-script.md` (instructor script, keyed to lecture sections, with a
  fallback for each beat), a `starter/` tree in the state the demo begins from, and a
  `completed/` tree in the state it should reach.
- Reference example: `../../weeks-01-03/demos/lecture-05-claude-code-demo/`.

## Demos

- [`note-specs/`](note-specs/) — a 75-minute live demo in which Claude Code
  maintains a small set of Markdown study notes under two written specifications
  (a concept of operations and a note-format spec). The class watches the
  specification–implementation conformance relationship being maintained while
  both sides change. Contains `demo-script.md` (with a checked-in PDF), the
  originating `prompt.md`, `starter/`, `completed/`, and `sample-inputs/`.
