# Note Format Specification

Version: 0.1 (draft)
Status: draft for review; not yet realized.

This is a normative specification. The keywords **MUST**, **MUST NOT**,
**SHOULD**, and **MAY** carry their RFC-2119 meanings. Rules are numbered so
that conformance reports — whether produced by an agent or by a tool — can
cite them. Every markdown file in the note set MUST satisfy the rules below.

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
first non-blank line after the front-matter.

### R4 — Single H1

A note MUST contain exactly one level-1 heading.

### R5 — No skipped heading levels

A heading MUST be at most one level deeper than the nearest heading above
it. A `##` section MAY open `###` subsections, but a `##` heading MUST NOT
be followed directly by a `####` heading.

### R6 — Index consistency

Every note file MUST be linked from `index.md` exactly once, and every note
link in `index.md` MUST resolve to an existing note file.
