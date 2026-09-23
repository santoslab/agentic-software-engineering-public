# In-class demo assets

This folder holds the materials for live demonstrations run during lectures.

- Folder naming: `lecture-NN-<slug>-demo/`, where NN is the lecture that runs the
  demo.
- Contents: one instructor script per lecture that runs the demo (keyed to lecture
  sections, with a fallback for each segment), a `starter/` tree in the state the
  demo begins from, and a `completed/` tree in the state it should reach.
- Reference example: `../../weeks-01-03/demos/lecture-05-claude-code-demo/`.

## Demos

- [`lecture-01-note-specs-demo/`](lecture-01-note-specs-demo/) — runs across
  Lectures 01 and 02, interleaved with the concept blocks (each instructor outline
  gives the segment-to-block mapping). Claude Code maintains a small set of Markdown
  study notes under written specifications; the class watches a specification
  audited and amended, a realization verified and repaired, a verifier written,
  and — in Lecture 02 — a concept of operations audited, operations performed under
  contracts, and a change of requirement carried through every artifact while
  conformance is re-established. Contains `demo-script-lecture-01.md`,
  `demo-script-lecture-02.md`, the originating `prompt.md`, `starter/`,
  `starter-l02/`, `completed/`, and `sample-inputs/`; its README maps the states.
