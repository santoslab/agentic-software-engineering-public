# Development rules (DEV)

Version: 1.2
Status: normative; maintained. **Always on.**

This document specifies how development proceeds with respect to the
specifications: how an operation begins, what may change and with whose approval,
what is written down instead of guessed, what must precede a build, and how an
operation ends. The keywords MUST, MUST NOT, SHOULD, and MAY carry their RFC 2119
meanings.

## In this repository

An *operation* is: producing or amending a specification (`CONOPS.md`,
`SPECS.md`); producing a plan; building or changing a module of the game;
writing or changing tests; or a change to a process document. Governing
documents, in authority order: `CONOPS.md`, `SPECS.md`; derived: the plans under
`plans/`. Deferred questions go to `BACKLOG.md`. Session exports go to
`transcripts/`.

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

*Example (a, game):* the engine declared a tie on a full board that also held a
winning line, against the winner-over-tie clause; repaired after the report and
the ruling, with no change to the specification.

*Example (b, game):* the scan of all 81 cells in four directions is replaced by a
check around the last move; every test passes unchanged, and the commit states
that no specified behavior changed.

*Example (c, game):* the ruling that `0` is not a valid digit in a move entry was
written into the input grammar before the validation code that rejects it. A move
accepted after the game was over is the same kind: the specification was silent,
so the clause was added first and the engine changed after — not a repair.

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

*Example (game):* the engine accepted a move after the game was over and the
specification was silent. The ruling — a move after `is_over()` is rejected with
no state change — was written into the interface contract, and the engine was
changed to match.

### DEV-5 — Derived documents follow governing ones

A document derived from a governing specification MUST NOT contradict it. When
it is wrong or incomplete, the agent proposes a correction to it rather than
improvising; when it and the governing document disagree, the governing document
wins and the derived document is corrected — unless a DEV-4 ruling moves the
governing document instead, in which case both changelogs record it.

*Example:* the operations document of the note set says so itself: "If this
document disagrees with either specification, the specifications win and this
document must be corrected."

*Example (game):* `SPECS.md` is derived from `CONOPS.md`, and a plan is derived
from `SPECS.md`. A plan that proposes a `reset()` method the interface contract
does not have is corrected before it is approved, not followed.

### DEV-6 — Defer explicitly

A question the operation cannot settle MUST be written to `BACKLOG.md` — the
question, where it arose, the options if known — and MUST NOT be settled by a
silent guess. A deferred question is closed by a ruling, recorded where DEV-4
says.

*Example:* "O1 creates blank notes with a placeholder Summary to satisfy R8's
MUST clause. Should R8 instead exempt notes that have no content yet?" — deferred,
with the current practice stated alongside.

*Example (game):* "Can a player quit in the middle of a game, or only from a
menu?" — the ConOps sketch is silent; deferred, and the game is built without it.

### DEV-7 — Every operation ends the same way

An operation is complete only when the affected realizations have been verified
(VER-3, VER-4) and the result reported (RPT-2); a completion note has been given
(RPT-5); and a commit has been made whose message names the operation.

*Example:* `add-note-with-content: No Silver Bullet`.

*Example (game):* `conops: 0.1 sketch -> 1.0`; `specs: 1.0.0`;
`engine: game.py per SPECS 5.1`.

### DEV-8 — Audit before planning

Before proposing any plan, the agent MUST run the specification audit
(`process/spec-audit.md`; with `process/conops-audit.md` when the plan concerns
the concept of operations) on every specification the plan would realize,
deliver the gap list (RPT-1), and wait for rulings. After any amendment the
audit MUST be run again before the plan is revised. A plan that rests on an
unaudited specification is not approved.

*Example (game):* the audit of `SPECS.md` 1.0.0 before the implementation plan
found that the interface contract said nothing about a move after the game is
over (see DEV-4).

### DEV-9 — Plan, then build

Any build — a module, a test suite, a migration, a port — MUST be preceded by a
plan proposed in plan mode, approved by the developer, and committed under
`plans/` before the first implementing commit. The plan MUST cite, for each step,
the specification clauses that step realizes (AUD-5), so that the history can be
read as specification → plan → realization.

*Example (game):* the approved plan for the engine cites `SPECS.md` §3 (board),
§4 (win condition), and §5.1 (the `Game` interface) step by step.

### DEV-10 — Read the repository before asking

A question that can be answered by reading the repository — the specifications,
the plans, the code, the history — MUST be answered that way, not by asking the
developer. This generalizes the last sentence of AUD-7 to every operation. A
question the repository cannot answer is asked, or deferred (DEV-6).

## Changelog

- **1.2** (2026-09-19) — DEV-2 restated as three kinds of realization change — repair, conformance-preserving, change of specified behavior — with what the history must show for each.
- **1.1** (2026-09-19) — Added DEV-8 (audit before planning), DEV-9 (plan, then
  build), DEV-10 (read the repository before asking); DEV-5 clarified — a DEV-4
  ruling may move the governing document instead, recorded in both changelogs;
  game examples added; binding rewritten for a code repository.
- **1.0** (2026-09-19) — Initial: DEV-1 through DEV-7.
