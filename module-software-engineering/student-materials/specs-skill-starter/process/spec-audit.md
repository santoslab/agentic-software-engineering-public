# Specification audit (AUD)

Version: 1.2
Status: normative; maintained. **Invoked on demand** — not loaded every session.

This document specifies how the quality of a specification is assessed before the
specification is relied on. Any kind of verifier — human, agent, or
algorithmic — may perform the audit, and the output has the same form whoever
produces it (RPT-1). The keywords MUST, MUST NOT, SHOULD, and MAY carry their
RFC 2119 meanings. Rules are numbered AUD-1… so that audit reports, rulings, and
later documents can cite them. AUD-1 through AUD-7 apply to every specification;
AUD-8 through AUD-14 apply to a specification, or a section of one, of the named
kind.

A concept of operations is audited by this document **and** by
`process/conops-audit.md` (AUDCON), which adds rules specific to that kind of
specification.

## When the audit runs

- When the developer asks for it ("run the specification audit on X").
- Before any plan is proposed that would realize the specification (DEV-8).
- After any amendment to a specification — on the amended document, and on every document that cites it.

## In this repository

| Under audit | Realizations governed | Clauses cited as |
|---|---|---|
| `CONOPS.md` (until it exists, `CONOPS-sketch.md`) | the game as a whole, as a player experiences it | §1 … §9 |
| `SPECS.md` | the engine, the computer opponent, the command-line interface, the tests | §n.m |
| the plans under `plans/` (derived) | the build they describe | by step |

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

*Example (game):* "five in a row wins" is ambiguous about six; "five **or more**
consecutive same-symbol cells" is not.

### AUD-2 — Internally consistent

No two clauses of one document MUST conflict, and any two clauses that constrain
the same thing MUST state their relationship.

*Test:* list every pair of clauses that touch the same property and write the
relationship down. A pair with no stated relationship is a finding (i.e., a potential 
problem with the specification).

*Example:* R2 requires a `title` field and R3 requires an H1; nothing says they
agree. Two clauses, one property, no relationship.

*Example (game):* "the game ends when the board is full" and "a player with no
legal move forfeits the turn" both constrain how a game ends, and with forced
passes the board may never fill.

### AUD-3 — Externally consistent and aligned

Across the specifications of one system: one vocabulary (a glossary), no
requirement in one document that an artifact of another document cannot satisfy,
and every fact stated once or stated identically.

*Test:* for each artifact any document names, check every document's rules against
it; for each term, check that it carries one meaning everywhere.

*Example:* the format specification governs "every markdown file in the note
set"; the concept of operations requires an `index.md` with no front-matter; no
`index.md` can satisfy R1. Neither document says whether the index is a note.

*Example (game):* the ConOps says "five or more"; the rules of play say
"exactly five"; the verification obligations require "at least one overline
case". Three statements of one fact — two of them agree.

### AUD-4 — Complete for its level

Completeness is judged at the specification's own level of abstraction, not
against everything that could be said. Every mode, policy, input form, and output
form that a higher-level document names MUST be addressed, and every operation the
specification implies MUST be performable without inventing a convention.

*Test — the execution walkthrough:* perform each operation step by step, on paper,
and list every point at which you had to invent something.

*Example:* O1 (add a blank note) takes a title; no clause says what filename the
note gets. The walkthrough cannot proceed without inventing one.

*Example (game):* the ConOps promises that an invalid entry is rejected; the
input grammar must therefore enumerate every rejected form, including a `0`
digit and surrounding whitespace, or the validation code invents the list.

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

## Appendix — checks by kind of specification

A behavioral contract for an interactive program is written one section per
kind. Each rule below applies to the section of that kind, in addition to
AUD-1 through AUD-7. When a kind is absent from a specification that a
higher-level document implies (a game with no display section), that absence is
an AUD-4 finding.

### AUD-8 — Rules of play

The rules of play MUST state every terminal condition and the precedence between
them when one move could satisfy two (a win on the last empty cell; a pass when
the board is full), what happens to the turn on an accepted move and on a
rejected one, and the initial state.

### AUD-9 — Display format

A display format MUST be byte-exact, with examples for at least the initial
state, a mid-play state, and a terminal state, and MUST state every glyph and
every fixed measurement (leading spaces, rule lengths). "Looks like the example"
is an AUD-1 finding.

### AUD-10 — Input grammar

An input grammar MUST enumerate every accepted form and every rejected form,
with the effect of each rejection on the turn and on the state, and MUST say how
whitespace, case, and length are treated.

### AUD-11 — Interaction flow

An interaction flow MUST give every menu with every option, every exit from
every loop, and the state in which the program is after each; no option may lead
to an unstated state.

### AUD-12 — Interface contract

An interface contract MUST give, for every public operation, its parameters and
their ranges, its precondition, its postcondition (including what it returns and
what state it changes), and its behavior when called outside its precondition —
including after the game is over.

### AUD-13 — Example session

An example session MUST be consistent, character for character, with the display
format, the input grammar, and the interaction flow; a discrepancy is a finding
against whichever of them is wrong (DEV-4).

### AUD-14 — Verification obligations

The verification obligations MUST map every clause of the contract to at least
one obligation, and every obligation to the clauses it verifies, so that clause
coverage can be reported (VER-2) independently of code coverage.

## Changelog

- **1.2** (2026-09-19) — Appendix added: AUD-8 through AUD-14, checks by kind of
  specification; game examples added; binding rewritten for a code repository.
- **1.1** (2026-09-19) — The concept of operations and the derived operations
  document added to the binding table; AUDCON named as the companion audit; the
  AUD-3 and AUD-4 examples now refer to documents present in the repository.
- **1.0** (2026-09-19) — Initial: AUD-1 through AUD-7.
