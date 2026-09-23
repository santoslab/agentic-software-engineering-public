# The note-set demo

One demonstration, run across two lectures. An agent maintains a small set of
markdown study notes under written specifications; the class watches the
specification and its realizations change while conformance is re-established
after every change.

| Lecture | Script | Starts from | Ends at |
|---|---|---|---|
| 01 | `demo-script-lecture-01.md` | `starter/` | the state in `starter-l02/`, less the L02 additions |
| 02 | `demo-script-lecture-02.md` | `starter-l02/` | `completed/` |

## Folders

- `starter/` — the state at the start of Lecture 01: `note-format-spec.md` 0.1
  (draft, with three seeded findings), `CLAUDE.md` (the loader), and
  `process/` (the L01 set: `spec-audit.md`, `reporting.md`, `verification.md`).
  No concept of operations, no notes.
- `starter-l02/` — the state at the start of Lecture 02: the specification at
  1.0.0, one conformant note and `index.md`, `check_notes.py` for 1.0.0, plus
  `note-set-conops.md` 0.1 (draft), the L02 `CLAUDE.md`, the L02 `process/`
  (adds `README.md`, `development-rules.md`, `conops-audit.md`), and
  `BACKLOG.md`.
- `completed/` — the state at the end of Lecture 02: the specification at
  2.0.0, the concept of operations at 1.0, the operations document at 1.2,
  three notes, the index, `check_notes.py` for 2.0.0, the L02 `process/` with
  its VER-2 table at 2.0.0, and `BACKLOG.md` with one deferred question.
- `sample-inputs/` — text the instructor pastes: the careless Royce note
  (Lecture 01, Segment 3), the No Silver Bullet content (Lecture 02, Segment 4),
  and the Lehman's Laws content (optional). Kept outside the live repository.
- `prompt.md` — the prompt from which the original single-lecture demo was
  planned; kept as history.

The `process/` folders are installed sets, not documents the demo edits: the
Lecture 01 set (AUD, RPT, VER) in `starter/`, and the Lecture 02 set (adding
`process/README.md`, DEV, and AUDCON) in `starter-l02/` and `completed/`. The
one permitted difference from an installed set is its binding block:
`completed/process/verification.md` carries the VER-2 table for specification
2.0.0, as VER-2 itself requires.

Every live run differs from `completed/`: different gap lists, different summary
wording. That is expected; `completed/` shows the destination, not the path.
