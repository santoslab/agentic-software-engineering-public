# In-class demo assets

This folder holds the materials for live demonstrations run during lectures.

- Folder naming: `lecture-NN-<slug>/`, where NN is the lecture that runs the
  demo, or the first of the lectures that share it.
- Contents: one instructor script per lecture that runs the demo (keyed to lecture
  sections, with a fallback for each segment); where the demo starts from a
  repository state, a `starter/` tree in that state and a `completed/` or
  `reference/` tree in the state it should reach.
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
- [`lecture-03-game-demo/`](lecture-03-game-demo/) — runs across Lectures 03 and
  04. A five-in-a-row tic-tac-toe is taken from a concept-of-operations sketch to
  a family of specifications, a planned realization, a test suite under a 100%
  branch-coverage gate, and fixtures. Contains `demo-script-lecture-03.md`,
  `demo-script-lecture-04.md`, `starter/` (the `t0` state), and `reference/` (the
  `t5` state — the worked example the Project 1 brief cites step by step); its
  README maps the tags.
- [`lecture-05-reversi-audit/`](lecture-05-reversi-audit/) — the Lecture 05
  walk-through of the Project 1 brief: step 1 (the audit of the Reversi sketch)
  from rehearsal captures, steps 2 to 5 by opening the reference game's
  artifacts. Contains `demo-script-lecture-05.md` and the instructor key
  `expected-gaps.md`; the starter it runs on is
  `../student-materials/reversi-starter/`.
