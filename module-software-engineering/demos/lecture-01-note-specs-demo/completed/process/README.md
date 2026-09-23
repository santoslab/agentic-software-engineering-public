# Process — how development proceeds with respect to the specifications

Version: 1.0
Status: normative; maintained.

## The invariant

Conformance is an invariant of the repository, not a milestone. At every commit:

1. every specification passes its audit — AUD for any specification, and AUDCON
   in addition for the concept of operations;
2. every realization conforms to the current version of its specification — VER;
3. every change to either side is recorded with the decision that caused it —
   DEV, RPT.

The specifications say what the system is. The documents in this folder say how
work proceeds with respect to them. Both are specifications: versioned, audited,
cited by identifier. The realization of *these* documents is the repository's
history — commits, changelog entries, reports — and auditing the process means
reading that history.

## The files

| File | Concern | Prefix | Applies | Loaded |
|---|---|---|---|---|
| `development-rules.md` | how an operation begins, proceeds, and ends; who may change what | DEV | every operation | always |
| `reporting.md` | the forms of a gap list, a conformance report, an amendment proposal, a completion note | RPT | whenever something is reported | always |
| `verification.md` | the kinds of verifier; mechanical vs judgment; when checks run; the gate | VER | after every change; before every commit | always |
| `spec-audit.md` | how a specification's quality is assessed | AUD | before a plan; after an amendment; on request | on demand |
| `conops-audit.md` | rules specific to a concept of operations | AUDCON | with AUD, whenever the ConOps is audited | on demand |

*Always on*: the rules are always in effect — the file is loaded with `CLAUDE.md`.
*On demand*: the rules are invoked only when needed — before any plan, after any
changes to a specification, or when asked.

## How they fit together

An operation begins by reading (DEV-1). If it will change a specification, the
change is proposed (RPT-3), approved (DEV-3), recorded, and the amended document
is audited again (AUD; AUDCON for the ConOps). If it changes a realization, the
realization is verified (VER-3, VER-4) and the result reported (RPT-2). A question
the operation cannot settle goes to `BACKLOG.md` (DEV-6). The operation ends with
a completion note (RPT-5) and a commit named for it (DEV-7).

## Changing these documents

Process documents change by the same mechanism as specifications: an amendment
proposal (RPT-3), approval (DEV-3), a version bump, and a changelog entry. Rule
identifiers are never renumbered; new rules are appended.

## Changelog

- **1.0** (2026-09-19) — Initial.
