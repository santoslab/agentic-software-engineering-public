# Note Set Operations

Version: 1.2
Status: maintained by the agent; changes are proposed to the user before
adoption.

This document specifies how the agent carries out the operations promised by
`note-set-conops.md` (§4–§5), under the rules of `note-format-spec.md`. If
this document disagrees with either specification, the specifications win
and this document must be corrected.

## Conventions

- *slug(title)* means the filename slug defined by rule R7 of
  `note-format-spec.md`.
- Every operation that touches a note ends by checking the affected notes
  for conformance (operation O4) before the closing commit.
- Every completed operation ends with a git commit whose message names the
  operation, e.g. `add-note-with-content: No Silver Bullet`.

## O1 — Add blank note

- **Input:** a title.
- **Precondition:** `notes/slug(title).md` does not exist and no `index.md`
  entry with that title exists.
- **Steps:** create `notes/slug(title).md` containing front-matter (`title`,
  `created` set to today's date in ISO-8601 form), the H1 equal to the
  title, and a `## Summary` section holding a one-sentence placeholder that
  names the note's intended topic; add the R6-form index entry; run O4 on
  the new note; commit.
- **Postcondition:** the note exists, conforms to R1–R5, R7, and R8, and is
  listed in `index.md` exactly once.

## O2 — Add note with initial content

- **Inputs:** a title and initial markdown text.
- **Precondition:** as O1.
- **Steps:** create `notes/slug(title).md`; bring the supplied text into
  conformance while preserving the user's meaning (add front-matter and the
  title H1; adjust heading levels only as conformance requires); write a
  `## Summary` paragraph if the supplied text does not contain one
  (judgment: the summary must reflect the content); add the R6-form index
  entry; run O4 on the new note; commit.
- **Postcondition:** as O1, with the user's content and meaning preserved.

## O3 — Remove note

- **Input:** a title.
- **Precondition:** `notes/slug(title).md` exists.
- **Steps:** delete the file; remove its `index.md` entry; run O4 in whole-set
  mode to confirm R6 still holds; commit.
- **Postcondition:** the file no longer exists and `index.md` no longer
  lists it.

## O4 — Check conformance

- **Input:** one note, several notes, or the whole set.
- **Steps:** first run the algorithmic verifier — `python3 check_notes.py
  <note.md> ...` for named notes, or `python3 check_notes.py --all` for the
  whole set including the R6 index checks. The script decides the mechanical
  clauses; which clauses are mechanical and which are judgment is the VER-2
  table in `process/verification.md`. When the user asks for a full check, or when a
  judgment clause is in question, the agent additionally reviews the
  judgment clauses. Violations are reported with rule IDs and the quoted
  rule text; per RPT-4, repairs wait for the user's ruling.
- **Postcondition:** a conformance report; the set itself is unchanged.

## Mechanical clauses and judgment clauses

The classification of every clause as mechanical (decided by `check_notes.py`)
or judgment (decided by a human or agent verifier) is the VER-2 table in
`process/verification.md`, amended whenever the specification changes.

## Deferred questions

Recorded in `BACKLOG.md` (DEV-6), not here.

## Changelog

- **1.2** (2026-09-20) — The mechanical-vs-judgment table moved to
  `process/verification.md` (VER-2); deferred questions moved to `BACKLOG.md`;
  wording aligned with the process documents.
- **1.1** (2026-09-11) — Spec v2.0.0: O1/O2 now produce a `## Summary`
  section; O4 runs `check_notes.py` first; added the mechanical-vs-judgment
  table (R8 splits across both columns).
- **1.0** (2026-09-11) — Initial version, written when the note set was
  scaffolded.
