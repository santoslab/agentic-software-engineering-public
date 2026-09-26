# Reporting (RPT)

Version: 1.2
Status: normative; maintained. **Always on.**

This document specifies the forms in which findings, results, proposed changes,
and completed operations are reported, so that a person can act on them and so
that the repository's history records what was found, what was decided, and why.
A report is evidence with a scope; the forms below exist so that the scope is
always stated. The keywords MUST, MUST NOT, SHOULD, and MAY carry their RFC 2119
meanings.

## In this repository

Reports cite `pkb-format-spec.md` clauses as R1, R2, …; the concept of
operations as §1 … §6 and O1, O2, …; the operations document as O1, O2, …;
process rules as AUD-n, AUDCON-n, DEV-n, VER-n, RPT-n. Reports are delivered in
the conversation; a report that leads to a change is summarized in that change's
commit message.

## Rules

### RPT-1 — Gap list (the output of an audit)

A numbered list. Each item MUST give:

- **Where** — document and clause or section, or "absent".
- **Category** — one of: ambiguous · incomplete · inconsistent within a document
  · inconsistent between documents · execution gap (a step that cannot be
  performed without inventing something).
- **Quoted text** — the clause as written, or the text that should exist and does not.
- **Recommended resolution** — one concrete proposal.
- **Status** — open · ruled: *the ruling* · deferred.

Items are ordered by the document they concern. The list MUST end by stating
which of the three search places (AUD-6) were covered.

*Example:*

> 3. **Where:** `note-format-spec.md`, R2 and R3. **Category:** inconsistent
> within. **Quoted:** R2 "`title` — a non-empty string"; R3 "The note body MUST
> begin with a level-1 heading". **Recommended:** amend R3 to require the H1 text
> to equal `title`, with the field authoritative. **Status:** open.

### RPT-2 — Conformance report (the output of a verification)

Before any finding, a conformance report MUST state:

- **Verifier** — which kind (human, agent, or algorithmic) and which one, with a
  version: the script's commit; the model and date for an agent; the reader's
  name for a person.
- **Specification and version** — the document, and the version it was checked against.
- **Clauses checked** and **clauses not checked**, by identifier.

Then, for each finding: the clause identifier; the clause text, quoted; the
location in the realization; what was observed. Then a verdict: *conformant*, or
the list of violated clauses. Repairs MAY be proposed; none are applied (RPT-4).

The three scope lines exist because a pass against a stale version, a verifier
that decides only some clauses, and a result that does not say which verifier
produced it are the three ways a true-looking result misleads.

*Example:*

> **Verifier:** agent (Claude Code, 2026-09-11). **Specification:**
> `note-format-spec.md` 1.0.0. **Checked:** R1–R7. **Not checked:** none.
> **R2** — "`created` — the note's creation date in ISO-8601 form
> (`YYYY-MM-DD`)": front-matter line 3 reads `created: Sept 11, 2026`.
> **R3** — "The H1 text MUST be identical to the front-matter `title`": the H1
> is `The Waterfall Paper`; `title` is `Royce 1970 Waterfall Paper`.
> **Verdict:** nonconformant (R2, R3, R4, R5). Repairs proposed below; none applied.

### RPT-3 — Amendment proposal (a change to a specification or a process document)

A numbered list. Each amendment MUST give: the document; the clause, or "new
clause" with its identifier; the old text and the new text; the rationale, citing
the gap-list item or finding that motivates it; the version bump the whole
proposal implies (patch, minor, or breaking); and the changelog entry that will
record it. The proposal MUST be marked *awaiting approval*, and nothing MUST be
edited until approval is given.

### RPT-4 — Report before repair

When a finding is made — by an audit or by a verification — the report MUST be
delivered and read before any realization or specification is changed on its
account. Which side moves is the developer's decision (DEV-4). The decision and
its reason are recorded in the changelog entry when the specification moves, and
in the commit message when the realization moves.

### RPT-5 — Operation completion note

When an operation ends (DEV-7), the agent MUST report, in this order: the
operation performed; the artifacts created, changed, or removed; which
verifications ran, by which verifier, with their result (the gate's exit code, or
a pointer to the RPT-2 report); which judgment clauses, if any, remain for a
human or agent verifier; any question deferred to `BACKLOG.md`; and the commit
message.

*Example:*

> **Operation:** O2 add note with initial content — "No Silver Bullet".
> **Artifacts:** created `notes/no-silver-bullet.md`; `index.md` entry added.
> **Verification:** `check_notes.py --all` (algorithmic, commit `3f2a9c1`),
> spec 1.0.0, R1–R7: exit 0. R8 not in force at this version.
> **Remaining judgment clauses:** O2 "preserving the user's meaning" — reviewed
> by the agent; headings adjusted only as R5 required.
> **Deferred:** none. **Commit:** `add-note-with-content: No Silver Bullet`.

## Changelog

- **1.2** (2026-09-25) — Bound to the personal-knowledge-base repository: the
  binding block names the PKB's documents. Rules unchanged.
- **1.1** (2026-09-19) — Added RPT-5 (operation completion note); binding
  extended to the concept of operations and the operations document.
- **1.0** (2026-09-19) — Initial: RPT-1 through RPT-4.
