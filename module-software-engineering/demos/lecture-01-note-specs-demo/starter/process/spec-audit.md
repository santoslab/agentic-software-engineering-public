# Specification audit (AUD)

Version: 1.0
Status: normative; maintained. **Invoked on demand** — not loaded every session.

This document specifies how the quality of a specification is assessed before the
specification is relied on. Any kind of verifier — human, agent, or
algorithmic — may perform the audit, and the output has the same form whoever produces
it (RPT-1). The keywords MUST, MUST NOT, SHOULD, and MAY carry their RFC 2119
meanings. Rules are numbered AUD-1… so that audit reports, rulings, and later
documents can cite them.

## When the audit runs

- When the developer asks for it ("run the specification audit on X").
- Before any plan is proposed that would realize the specification.
- After any amendment to a specification — on the amended document, and on every document that cites it.

## In this repository

| Under audit | Realizations governed | Clauses cited as |
|---|---|---|
| `note-format-spec.md` | the files in `notes/` | R1, R2, … |

## Rules

### AUD-1 — Unambiguous

Every clause MUST decide yes or no for any realization put in front of it.
Requirement levels MUST use the RFC 2119 keywords. Wherever a clause constrains
form — a date, a filename, a layout — it MUST include an example that is exact to
the character.

*Test:* for each clause, could two careful readers disagree about whether a given
realization satisfies it? If so, the clause is ambiguous.

*Example:* "the `created` field holds a date" is ambiguous; "an ISO-8601 date,
`YYYY-MM-DD`" is not.

### AUD-2 — Internally consistent

No two clauses of one document MUST conflict, and any two clauses that constrain
the same thing MUST state their relationship.

*Test:* list every pair of clauses that touch the same property and write the
relationship down. A pair with no stated relationship is a finding (i.e., a potential 
problem with the specification).

*Example:* R2 requires a `title` field and R3 requires an H1; nothing says they
agree. Two clauses, one property, no relationship.

### AUD-3 — Externally consistent and aligned

Across the specifications of one system: one vocabulary (a glossary), no
requirement in one document that an artifact of another document cannot satisfy,
and every fact stated once or stated identically.

*Test:* for each artifact any document names, check every document's rules against
it; for each term, check that it carries one meaning everywhere.

*Example:* a format specification that governs "every markdown file in the note
set" and a second document that requires an `index.md` with no front-matter: no
`index.md` can satisfy R1. With a single document in the repository this rule has
nothing to compare; it becomes active when a second document arrives.

### AUD-4 — Complete for its level

Completeness is judged at the specification's own level of abstraction, not
against everything that could be said. Every mode, policy, input form, and output
form that a higher-level document names MUST be addressed, and every operation the
specification implies MUST be performable without inventing a convention.

*Test — the execution walkthrough:* perform each operation step by step, on paper,
and list every point at which you had to invent something.

*Example:* "add a blank note" takes a title; no clause says what filename the note
gets. The walkthrough cannot proceed without inventing one.

### AUD-5 — Traceable

Every clause MUST carry a stable identifier. Identifiers MUST NOT be renumbered
when a specification changes; new clauses are appended. A document derived from a
specification MUST cite the clauses it derives from, and a verification result
MUST be able to cite the clause it decides.

*Test:* pick a clause. Can a report, a test, or a derived document name it
unambiguously — and will that name still be right after the next amendment?

### AUD-6 — Search in three places

An audit MUST look (a) within each document, (b) between documents, and (c)
between a document and the act of executing it. The report MUST state which of
the three were searched; a gap list that searched one place is incomplete.

### AUD-7 — Output, and stop

The audit's output is a gap list in the form RPT-1: numbered, each item placed,
categorized, quoted, and given a recommended resolution. The auditor MUST then
stop and wait for rulings. The auditor MUST NOT amend a specification or begin a
plan on the strength of its own findings.

A question that can be answered by reading the repository is answered by reading
the repository, not by asking.

## Changelog

- **1.0** (2026-09-19) — Initial: AUD-1 through AUD-7.
