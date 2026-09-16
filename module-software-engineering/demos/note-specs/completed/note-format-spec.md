# Note Format Specification

Version: 2.0.0
Status: normative; maintained.

This is a normative specification. The keywords **MUST**, **MUST NOT**,
**SHOULD**, and **MAY** carry their RFC-2119 meanings. Rules are numbered so
that conformance reports — whether produced by an agent or by a tool — can
cite them.

**Scope.** Rules R1–R5, R7, and R8 govern the note files in `notes/`.
`index.md` is not a note; it is governed solely by R6.

## Rules

### R1 — Front-matter block

Every note MUST begin with a YAML front-matter block delimited by `---`
lines. The opening `---` MUST be the first line of the file, and a closing
`---` MUST follow the front-matter fields.

### R2 — Front-matter fields

The front-matter MUST contain exactly two fields:

- `title` — a non-empty string.
- `created` — the note's creation date in ISO-8601 form (`YYYY-MM-DD`).

### R3 — Title heading

The note body MUST begin with a level-1 heading (`# `), which MUST be the
first non-blank line after the front-matter. The H1 text MUST be identical
to the front-matter `title`. The front-matter `title` is authoritative:
conformance repairs adjust the heading, not the field.

### R4 — Single H1

A note MUST contain exactly one level-1 heading: the title heading required
by R3.

### R5 — No skipped heading levels

A heading MUST be at most one level deeper than the nearest heading above
it. A `##` section MAY open `###` subsections, but a `##` heading MUST NOT
be followed directly by a `####` heading.

### R6 — Index consistency

Every note file MUST be linked from `index.md` exactly once, and every note
link in `index.md` MUST resolve to an existing note file. Each index entry
MUST have the form:

    - [Title](notes/<slug>.md) — <first sentence of the note's Summary paragraph>

where the separator is an em dash surrounded by single spaces.

### R7 — Filename

A note's filename MUST be the slug of its title plus `.md`. The slug is
formed by lowercasing the title, removing apostrophes, replacing every
remaining maximal run of characters other than ASCII letters and digits with
a single hyphen, and stripping leading and trailing hyphens.

### R8 — Summary section

The first level-2 heading in every note MUST be `## Summary`, and it MUST
appear before any other section heading. The Summary section MUST contain
exactly one paragraph. The paragraph SHOULD accurately summarize the note's
content.

## Changelog

- **2.0.0** (2026-09-11, breaking) — Added R8 (required `## Summary`
  section); amended R6 (index entries display the first sentence of each
  note's Summary). Existing notes required migration; see the migration
  commit in git history.
- **1.0.0** (2026-09-11) — Refinements surfaced during implementation
  planning: scope clarified (`index.md` is not a note); R3 amended to
  require the H1 to equal the front-matter `title`, with the front-matter
  authoritative; R7 (filename slug rule) added.
- **0.1** — Initial draft.
