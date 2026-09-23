# Concept-of-operations audit (AUDCON)

Version: 1.1
Status: normative; maintained. **Invoked on demand**, together with
`process/spec-audit.md`.

A concept of operations (ConOps) is a specification of purpose: what the system is
for, who uses it, which operations they perform, and what they can observe. It is
audited by `process/spec-audit.md` (AUD-1 through AUD-7) like any specification,
and by the additional rules below, which apply only to this kind of document. The
output is one gap list per RPT-1 covering both the AUD and the AUDCON findings.
The keywords MUST, MUST NOT, SHOULD, and MAY carry their RFC 2119 meanings.

Two skeletons are in use in this course. The **light** skeleton: purpose and
scope; the system; roles; operations with preconditions and postconditions;
conformance; change management. The **full** skeleton: nine numbered sections —
1 Scope; 2 Current Situation; 3 Justification for and Nature of the Changes;
4 Concept for the Proposed System (objectives, operational policies, modes, user
classes and actors, operational environment); 5 Operational Scenarios; 6 Summary
of Impacts; 7 Analysis; 8 Future Operational Capabilities; 9 Glossary — of which
2, 3, and 6 apply only when an existing system is being improved. AUDCON-1
through AUDCON-6 apply to both; AUDCON-7 and AUDCON-8 to the full skeleton.

## In this repository

| Under audit | Skeleton | Cited as |
|---|---|---|
| `CONOPS-sketch.md`, then `CONOPS.md` | full | §1 … §9; §4.2 policies by their bullet |

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

*Example (game):* "the player types a two-digit entry, row then column" belongs;
"the board is a list of nine row lists" does not.

### AUDCON-2 — Observable

Every policy the ConOps states MUST be something a user could observe, or an
operation could demonstrate.

*Test:* for each policy, name the moment at which a user would notice it being
kept or broken.

*Example:* "conformance is an invariant of the set, not a milestone" is
observable — a check requested at any moment passes. "The agent reads the
specifications before every operation" is not a policy of the system but a rule
of the process (DEV-1), and belongs there.

*Example (game):* "an invalid entry never costs a turn" is observable — the same
player is prompted again and the board is unchanged.

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

*Example (game):* a sketch with one scenario (solo play to a win) leaves the tie,
the two-player mode, and recovery from an invalid entry unexercised — three
findings.

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

*Example (game):* a sketch written in the first person ("I type a square") is a
finding under this rule; the content survives the rewrite, the voice does not.

### AUDCON-6 — Versioned

The ConOps MUST carry a version, a status, and a changelog whose entries state the
rationale for each change (DEV-3).

### AUDCON-7 — Skeleton

In the full skeleton, every kept section MUST be filled: a "TBD", an empty
section, or a placeholder is a finding. Sections 2, 3, and 6 MUST be present when
an existing system is being improved and MUST be omitted (or marked as not
applicable, with the reason) when the system is new; their presence or absence
is itself audited against the situation the ConOps describes.

*Test:* is there a baseline system? If yes, sections 2, 3, and 6 exist and say
what it is, what changes, and what the change affects; if no, they are absent
with a note. Then read each remaining section for a placeholder.

*Example (game):* the five-in-a-row sketch keeps 2 and 3 (ordinary 3-by-3 is the
baseline) and skips 6; the Reversi sketch omits all three (a new game). Both
sketches leave §1.3 and §9 as "TBD" — findings.

### AUDCON-8 — Facts in their section

A fact MUST be stated in the section whose purpose it serves. An operational
policy stated under Limitations or Analysis, an environment fact stated under
Objectives, or a scenario detail that is the only statement of a rule, is
misfiled: it is moved to its section (§4.2 for policies, §4.5 for environment)
and the original place refers to it if needed.

*Test:* for each sentence in §7 and §8, ask whether it states a rule the player
observes now. If so, §4.2 must state it.

*Example (game):* "nothing is saved between games" stated only under
§7 Limitations is a policy of the operational environment (§4.5); "no taking a
move back" stated only under Limitations is a policy (§4.2).

## Changelog

- **1.1** (2026-09-19) — Added AUDCON-7 (skeleton, optional sections 2/3/6) and
  AUDCON-8 (facts in their section); the full skeleton enumerated; game examples
  added; binding rewritten for the full skeleton.
- **1.0** (2026-09-19) — Initial: AUDCON-1 through AUDCON-6.
