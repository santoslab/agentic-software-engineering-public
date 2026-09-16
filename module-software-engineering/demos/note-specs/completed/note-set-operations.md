# Note Set Operations

Version: 1.1
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
- **Steps:** first run the algorithmic checker — `python3 check_notes.py
  <note.md> ...` for named notes, or `python3 check_notes.py --all` for the
  whole set including the R6 index checks. The script covers the mechanical
  rules (table below). When the user asks for a full check, or when a
  judgment clause is in question, the agent additionally reviews the
  judgment clauses. Violations are reported with rule IDs and the quoted
  rule text; per the working rules, repairs wait for the user's go-ahead.
- **Postcondition:** a conformance report; the set itself is unchanged.

## Mechanical rules vs. judgment clauses

`check_notes.py` decides the mechanical rules deterministically and for
free. The judgment clauses cannot be decided by the script; they remain the
agent's (or the user's) job.

| Rule / clause | `check_notes.py` | Agent or user judgment |
| --- | --- | --- |
| R1 front-matter block | yes | — |
| R2 fields, including date validity | yes | — |
| R3 H1 placement and H1 = `title` | yes | — |
| R4 single H1 | yes | — |
| R5 no skipped heading levels | yes | — |
| R6 index bijection and entry form, including the summary-sentence match | yes (`--all`) | — |
| R7 filename = slug of title | yes | — |
| R8 first section is `## Summary`, exactly one paragraph | yes | — |
| R8 the summary **accurately** summarizes the note (SHOULD) | no | yes |
| O2 conformance repairs preserve the user's meaning | no | yes |

## Deferred questions

- O1 creates blank notes with a placeholder Summary sentence to satisfy
  R8's MUST clause. Should R8 instead exempt notes that have no content
  yet? Current practice: the placeholder names the intended topic, and the
  Summary is rewritten when content arrives.

## Changelog

- **1.1** (2026-09-11) — Spec v2.0.0: O1/O2 now produce a `## Summary`
  section; O4 runs `check_notes.py` first; added the mechanical-vs-judgment
  table (R8 splits across both columns).
- **1.0** (2026-09-11) — Initial version, written when the note set was
  scaffolded.
