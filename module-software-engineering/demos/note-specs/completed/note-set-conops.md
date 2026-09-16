# Note Set — Concept of Operations

Version: 1.0
Status: realized; maintained.

## 1. Purpose and scope

A single user keeps a personal set of study notes on software-engineering
classics. A coding agent performs all structural operations on the note set;
the user writes and edits note content. This document describes the note set
and the operations the agent supports, from the user's point of view.

## 2. The note set

Notes are markdown files stored in a `notes/` directory inside a git
repository. An index file, `index.md`, at the top level of the repository
links to every note in the set. The formatting of notes is governed by
`note-format-spec.md`; a note's filename is derived from its title as
specified by rule R7 of that document. The index file is not itself a note:
only the index-consistency rule (R6) applies to it.

## 3. Roles

There is one user and one agent (Claude Code). The user requests operations
conversationally; the agent performs them and reports what changed.

## 4. Agent operations

### O1 — Add blank note

- **Input:** a title.
- **Precondition:** no note with that title exists in the set.
- **Postcondition:** a new note exists containing well-formed front-matter
  and the title as its heading, with no other content; `index.md` lists it.

### O2 — Add note with initial content

- **Inputs:** a title and initial markdown text.
- **Precondition:** no note with that title exists in the set.
- **Postcondition:** a note exists whose content is the supplied text brought
  into conformance with `note-format-spec.md`, preserving the user's meaning;
  `index.md` lists it.

### O3 — Remove note

- **Input:** a title.
- **Precondition:** a note with that title exists in the set.
- **Postcondition:** the note file no longer exists; `index.md` no longer
  lists it.

## 5. Conformance

Every note in the set is expected to conform to `note-format-spec.md` at all
times — conformance is an invariant of the set, not a milestone. The user may
at any time direct the agent to check one note, or all notes, for
conformance. A conformance report cites the specific rule identifiers (R1,
R2, ...) from the format spec. How checks are carried out is documented in
`note-set-operations.md`.

## 6. Change management

Every operation ends in a git commit. The specifications themselves live in
the same repository and are maintained documents: when they change, they
change by versioned, reviewed edits.

## Changelog

- **1.0** (2026-09-11) — Clarifications surfaced during implementation
  planning: `index.md` is not a note (only R6 applies to it); note filenames
  are derived from titles per R7 of `note-format-spec.md`. See the format
  spec's changelog for the matching amendments.
- **0.1** — Initial draft.
