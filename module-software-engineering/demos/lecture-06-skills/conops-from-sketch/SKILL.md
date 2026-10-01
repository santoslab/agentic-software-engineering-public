---
name: conops-from-sketch
description: >-
  Turns a concept-of-operations sketch (e.g. CONOPS-sketch.md) into a governed
  CONOPS.md 1.0 by the audit-first method: audit the sketch, report a numbered
  gap list, wait for the developer's rulings, propose amendments, wait for
  approval, then write and re-audit. Use only when the developer explicitly asks
  to turn a sketch into a CONOPS. Not for explaining what a ConOps is,
  summarizing a sketch, or editing an existing CONOPS.md.
argument-hint: "[path to sketch, default CONOPS-sketch.md]"
disable-model-invocation: true
allowed-tools: Read Grep Glob
---

# CONOPS from a sketch

The sketch is `$ARGUMENTS` (if empty, `CONOPS-sketch.md` in the repository root).

A concept of operations is a governing document: every later specification,
plan, and test derives from it. So a guess written into it is not a small
error — it becomes a requirement nobody decided. The whole point of this skill
is that **the developer decides every open question; you find them.** That is
why the work is split into three phases, each ending in a stop.

Work out which phase you are in from the conversation so far:
no gap list delivered yet → phase 1; gap list delivered and rulings given →
phase 2; amendments approved → phase 3.

## Phase 1 — Audit the sketch, report, stop

1. Read the sketch in full, and the repository's own process documents
   (look for a `process/` directory, `CLAUDE.md`, a backlog). If the repository
   has a ConOps audit and a specification audit (in the course method:
   `process/conops-audit.md` = AUDCON and `process/spec-audit.md` = AUD), **they
   are the authority** — cite their rule identifiers and use their report form
   (RPT-1), and leave the bundled checklist unopened. Only if the repository
   has no audit, say so in one line and use [checklist.md](checklist.md).
2. Audit by reading, in the three places: within the sketch, between the sketch
   and the other documents, and by walking through each operation step by step
   as a user would. Then work through [probes.md](probes.md) — reading probes
   that surface the gaps audits most often miss. Do not skip it: the first
   read of a sketch finds the obvious gaps, the probes find the rest.
3. Report the gap list in the form [gap-report-template.md](gap-report-template.md)
   gives: first a short "what the sketch states / implies / leaves out"
   summary, then numbered gaps, each with where, category, the quoted text, the
   rule that found it, one recommended resolution, and status *open*.
4. **Stop.** End by asking for rulings. Do not write or edit any file.

One open question per gap. When one item bundles two questions (a missing
scenario *and* whether that outcome is final), the developer rules on one and
the other is silently lost — split them.

A recommendation is not a ruling. Even when the answer looks obvious, list it
as a gap with your recommendation — the developer may rule it in one word.
Deferring a question to `BACKLOG.md` is also a ruling the developer makes; you
may recommend it, not choose it. A question the repository itself answers is
answered by reading the repository, not asked.

## Phase 2 — Record rulings, propose amendments, stop

Restate each ruling against its gap number (ruled / deferred). For any gap
without a ruling, ask again rather than filling it in. Then propose the
amendments in the repository's amendment form (RPT-3 in the course method):
numbered; section; old text (or "absent") and new text; rationale citing the
gap number; the version this produces (0.1 sketch → 1.0); the changelog entry;
and any `BACKLOG.md` entries for deferred gaps. Mark it *awaiting approval* and
**stop**.

## Phase 3 — Write CONOPS.md 1.0, re-audit, report

Only after approval:

1. Write `CONOPS.md` in the full skeleton the repository's audit names (in the
   course method, nine sections; 2, 3, and 6 present only when a baseline system
   exists, otherwise marked not applicable with the reason). Every kept section
   filled — no TBD. Third person, present tense, implementation-free (nothing
   only a builder would see). Version 1.0, status, and a changelog whose entry
   cites the rulings. Write deferred questions to `BACKLOG.md`.
2. The content is the sketch plus the rulings — nothing else. If writing a
   section forces a decision nobody ruled on, stop and ask; do not smooth it over.
3. Re-run the same audits on `CONOPS.md` and report per the gap-list form,
   including "no findings" per rule where that is the result, and which of the
   three search places were covered.
4. Do not commit unless the developer asks; if asked, use their message.
