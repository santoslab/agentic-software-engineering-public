# Development rules (DEV)

Version: 1.1
Status: normative; maintained. **Always on.**

This document specifies how development proceeds with respect to the
specifications: how an operation begins, what may change and with whose approval,
what is written down instead of guessed, and how an operation ends. The keywords
MUST, MUST NOT, SHOULD, and MAY carry their RFC 2119 meanings.

## In this repository

An *operation* is one of the agent operations the concept of operations promises
— O1 add blank note, O2 add note with initial content, O3 remove note, and the
conformance check — or a change to a specification, or a change to a process
document. Governing documents, in authority order: `note-set-conops.md`,
`note-format-spec.md`; derived: `note-set-operations.md`. Deferred questions go to
`BACKLOG.md`.

## Rules

### DEV-1 — Read before acting

Before any operation the agent MUST read the governing documents and the
always-on process documents in full, from the files — not from its recollection
of an earlier reading. A check driven by memory is one of the ways a verification
result becomes invalid (VER-1).

### DEV-2 — Specification before realization

A realization changes for one of three reasons, and the history MUST show which.

(a) **Repair.** The realization did not conform and is changed so that it does.
No specification change precedes it; a report (RPT-2) and a ruling (DEV-4,
RPT-4) do.

(b) **Conformance-preserving change.** The realization conformed before and
conforms after; what changed lies in what the specification deliberately leaves
open — the algorithm, its efficiency, the structure or naming of the code. No
specification change is needed. The change MUST be verified (VER-3), and its
commit message MUST state that no specified behavior changed.

(c) **Change of specified behavior.** The realization would no longer conform to
the current specification. Such a change MUST trail a committed amendment to the
specification (DEV-3, RPT-3) — in the same commit or an earlier one. The intent
changes first; the realization follows.

A change of kind (b) motivated by a property the developer would not do
without — a bound on time or size, a portability constraint — is a sign that the
specification is incomplete at its own level (AUD-4): the property is added by
amendment, after which kind (c) governs it, or deferred explicitly (DEV-6).

*Test:* for each commit that touches a realization — which kind is it, and does
the history show what that kind requires?

*Example (a):* the careless Royce note violated R2–R5 and was repaired after the
report and the ruling; the specification did not move.

*Example (b):* `check_notes.py` is restructured so that each rule is one
function; its output on every note is unchanged, the gate is green, and the
commit says so.

*Example (c):* the scope amendment ("`index.md` is not a note") and the filename
rule were committed before the scaffold that created `index.md` and the first note.

### DEV-3 — Amend only with approval

No governing document and no process document MUST be edited without explicit
approval. Changes are proposed as an amendment proposal (RPT-3); each approved
amendment bumps the document's version and adds a changelog entry stating the
rationale.

### DEV-4 — In a verification failure, a person decides whether the specification or realization gets changed

When a specification and a realization disagree, the finding is a fact about the
pair; which side changes is the developer's decision. The decision and its reason
MUST be recorded — in the changelog when the specification moves, in the commit
message when the realization moves.

*Example:* a note's H1 disagreed with its `title` field. The ruling — the field is
authoritative; repairs adjust the heading — was written into R3 so that nobody has
to decide it case by case.

### DEV-5 — Derived documents follow governing ones

A document derived from the governing specifications — here
`note-set-operations.md` — MUST NOT contradict them. When it is wrong or
incomplete, the agent proposes a correction to it rather than improvising; when it
and a governing document disagree, the governing document wins and the derived
document is corrected.

*Example:* the operations document says so itself: "If this document disagrees
with either specification, the specifications win and this document must be
corrected."

### DEV-6 — Defer explicitly

A question the operation cannot settle MUST be written to `BACKLOG.md` — the
question, where it arose, the options if known — and MUST NOT be settled by a
silent guess. A deferred question is closed by a ruling, recorded where DEV-4
says.

*Example:* "O1 creates blank notes with a placeholder Summary to satisfy R8's
MUST clause. Should R8 instead exempt notes that have no content yet?" — deferred,
with the current practice stated alongside.

### DEV-7 — Every operation ends the same way

An operation is complete only when the affected realizations have been verified
(VER-3, VER-4) and the result reported (RPT-2); a completion note has been given
(RPT-5); and a commit has been made whose message names the operation.

*Example:* `add-note-with-content: No Silver Bullet`.

## Changelog

- **1.1** (2026-09-19) — DEV-2 restated as three kinds of realization change — repair, conformance-preserving, change of specified behavior — with what the history must show for each.
- **1.0** (2026-09-19) — Initial: DEV-1 through DEV-7.
