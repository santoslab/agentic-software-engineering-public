# Student Materials

Handouts and small example artifacts distributed with this module's exercises. None
contains a reference solution.

| File or folder | Lecture / exercise | Contents |
|---|---|---|
| [`handout-lecture-01-note-set-starter.md`](handout-lecture-01-note-set-starter.md) | Lecture 01, Exercise 1 | The files the Lecture 01 demo starts from: the draft specification, the loader `CLAUDE.md`, and the three process documents (AUD, RPT, VER), reproduced for reading before class; PDF checked in |
| [`handout-lecture-02-conops-and-operations.md`](handout-lecture-02-conops-and-operations.md) | Lecture 02 | The files Lecture 02 adds: the draft concept of operations, the loader, `process/README.md`, the development rules (DEV), the concept-of-operations audit (AUDCON), and `BACKLOG.md`; PDF checked in |
| [`spec-driven-planning-prompt-template.md`](spec-driven-planning-prompt-template.md) | Lecture 02, Exercise 1 | A prompt template for planning and realizing a system from specifications, with a filled example and a table of which process rule each move lives in |
| [`pkb-starter/`](pkb-starter/) | Lecture 02, Project 0 | The Project 0 starter: the loader `CLAUDE.md`, `process/` (the Lecture 02 set, bound to the PKB's documents), `BACKLOG.md`, the grill-me skill, and a `.gitignore`. No concept of operations, no format specification, no bundle |
| [`pkb-example/`](pkb-example/index.md) | Lecture 02, Project 0 | An Open Knowledge Format bundle of three notes in the profile the Project 0 brief prescribes (§3): `index.md`, `log.md`, two Concept notes, one Reference note. Its unresolved `/concepts/tool-schemas.md` link is intentional. A bundle only; it has no governing documents |
| [`reversi-starter/`](reversi-starter/) | Lecture 05, Project 1 (Phase 1) | The Project 1 starter: the Reversi concept-of-operations sketch (incomplete on purpose), the loader `CLAUDE.md`, `process/` (the Lecture 04 set), `BACKLOG.md`, and the gate's configuration (`.coveragerc`, `pytest.ini`, `requirements-dev.txt`, `.gitignore`). No specification, no code, no tests |

**What is exported, and when.** Each row is exported at the lecture it names —
the handouts before that lecture, the PKB starter and example at Lecture 02
together with the Project 0 brief, the Reversi starter whole at Lecture 05
together with the Project 1 brief. Nothing is staged after that: everything a
kickoff or Phase 1 needs is in its starter on day one.

The handouts are generated from the demo's `starter/` and `starter-l02/` folders
(heading levels shifted so that each handout has one title); regenerate them when
those folders change. PDF versions are checked in for direct distribution; the
Markdown files are the editable sources. To rebuild a PDF, run the pandoc command
given in the repository's `CLAUDE.md`.

Exercise specifications live in [`../exercises/`](../exercises/), and the
student-facing prose for each class meeting lives in
[`../lecture-notes/`](../lecture-notes/).
