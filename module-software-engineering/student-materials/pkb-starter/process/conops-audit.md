# Concept-of-operations audit (AUDCON)

Version: 1.1
Status: normative; maintained. **Invoked on demand**, together with
`process/spec-audit.md`.

A concept of operations (ConOps) is a specification of purpose: what the system is
for, who uses it, which operations they perform, and what they can observe. It is
audited by `process/spec-audit.md` (AUD-1 through AUD-7) like any specification,
and by the additional rules below, which apply only to this kind of document. The output is
one gap list per RPT-1 covering both the AUD and the AUDCON findings. The keywords
MUST, MUST NOT, SHOULD, and MAY carry their RFC 2119 meanings.

Two skeletons are in use in this course. The **light** skeleton: purpose and
scope; the system; roles; operations with preconditions and postconditions;
conformance; change management. The **full** skeleton: nine numbered sections, of
which 2 (Current Situation), 3 (Justification for and Nature of the Changes), and
6 (Summary of Impacts) apply only when an existing system is being improved. The
rules below are written for both; rules specific to the full skeleton are added
when it is first applied.

## In this repository

| Under audit | Skeleton | Cited as |
|---|---|---|
| `pkb-conops.md` (until it exists, `pkb-conops-sketch.md`) | light | §1 … §6; operations O1, O2, … |

## Rules

### AUDCON-1 — Implementation-independent

The ConOps MUST NOT name anything that exists only inside the realization: no
programming language, module, class, method, data structure, or internal file.
What the user sees, types, opens, or is told — a markdown file in `notes/`, a
command, a report that cites rule identifiers — is operational and belongs.

*Test:* for each concrete noun, ask whether a user of the system encounters it.
If only a builder would, it is misplaced.

*Example:* "notes are markdown files in `notes/`" belongs. "`check_notes.py`
parses the front-matter as two scalar fields" belongs in a lower-level document.

### AUDCON-2 — Observable

Every policy the ConOps states MUST be something a user could observe, or an
operation could demonstrate.

*Test:* for each policy, name the moment at which a user would notice it being
kept or broken.

*Example:* "conformance is an invariant of the set, not a milestone" is
observable — a check requested at any moment passes. "The agent reads the
specifications before every operation" is not a policy of the system but a rule
of the process (DEV-1), and belongs there.

### AUDCON-3 — Operations and scenarios cover

Every operation the ConOps promises MUST state its input, its precondition (what
must hold before it may start), and its postcondition (what holds when it is
done), from the user's side. Every mode, policy, and user class the ConOps names
MUST appear in at least one operation or scenario.

*Test:* list the operations; for each, can a user tell whether it may start and
whether it finished correctly? List the user classes and policies; is each
exercised somewhere?

*Example:* O3 (remove note) requires "a note with that title exists" — a
precondition a user can check — and its postcondition names both the file and the
index entry.

### AUDCON-4 — Terms

Every term the ConOps uses repeatedly MUST be defined — in a glossary, or in the
text where it first appears — and every defined term MUST be used with that
meaning throughout, consistently with the other specifications (AUD-3).

*Example:* "note", "index", and "the set" are defined in §2; "conformance" is
used in the sense `note-format-spec.md` gives it.

### AUDCON-5 — Voice and self-containment

The ConOps MUST be written in the third person and the present tense, and MUST be
understandable by a reader who has no other document. It MUST NOT cite code. It
SHOULD NOT depend on clauses of lower-level specifications; naming a lower-level
document as the place where a detail is fixed is acceptable.

*Example:* "a conformance report cites the rule identifiers (R1, R2, …) of the
format specification" names the document and describes what the user sees — a
SHOULD-level finding that a ruling may close as *no change: observable behavior*.

### AUDCON-6 — Versioned

The ConOps MUST carry a version, a status, and a changelog whose entries state the
rationale for each change (DEV-3).

## Changelog

- **1.1** (2026-09-25) — Bound to the personal-knowledge-base repository: the
  binding table names `pkb-conops.md`. Rules unchanged.
- **1.0** (2026-09-19) — Initial: AUDCON-1 through AUDCON-6.
