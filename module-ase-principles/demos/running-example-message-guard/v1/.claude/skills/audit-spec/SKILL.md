---
name: audit-spec
description: >-
  Audits the specifications of this repository for specification quality by
  the fixed procedure of rule SQ-2: read every specification in full, check
  within each document, between documents, and by executing the examples,
  then report every gap in the gap-list form of rule RPT-2 and stop for the
  developer's rulings. Use only when the developer explicitly asks for an
  audit of the specifications. Not for amending a specification, not for
  eliciting one, not for reviewing code or tests.
argument-hint: "[optional: the specification files to audit, default all of specs/]"
disable-model-invocation: true
allowed-tools: Read Grep Glob
---

# Audit the specifications

Version 1.1. The scope is `$ARGUMENTS` (if empty, every file under `specs/`).

The specifications are the reference that every test, every conformance
report, and the stakeholders' sign-off rest on. A defect in them gives a
confident answer to the wrong question, and an agent that writes code and
tests from them will realize either reading of an ambiguous clause. This
skill finds the gaps; the developer rules on every one of them. The skill
never amends a file.

## 1. Read everything first

Read, in full and before the first check: every file under `specs/`
(including `specs/glossary.md` and `specs/scenarios.json`), and
`process/rules.md`. If `reference/elicitation.md` exists, read it too: it is
not audited, but it says what a stakeholder meant, which a ruling may need.
Checking from memory of an earlier read is the characteristic failure of an
agent verifier; reading first is how this procedure guards against it. If
the repository's rules name checks this skill does not (an SQ rule added
after version 1.0), apply those too and cite them.

## 2. Check within each document

Apply the "within a document" items of [checklist.md](checklist.md) to each
specification on its own: well-formed clause headers, the declared EARS
pattern against the sentence, every domain term defined once in the
glossary and used in that sense, a reason on every judgment clause, no
unquantified adjective where a definition or a number is needed, nothing in
a purpose statement that only a builder would see.

## 3. Check between documents

Apply the "between documents" items: every story has at least one
requirement and every requirement derives from a story or a glossary term;
no two clauses contradict, in one document or across two; one term means one
thing everywhere; each scenario agrees with the example of the story it
derives from; assumptions are stated as assumptions and not as requirements;
a want recorded as deferred has no requirement deriving from it; every file,
rule, and record entry a specification names exists at this commit.

## 4. Check by execution

For every story example and every scenario, decide from the clauses what the
output must be and compare it with the stated expectation. Where the
realization exists, you may also run `uv run python tools/walk.py LEVEL
PAYLOAD` (it needs the developer's permission); a disagreement between the
run and the expectation is a finding about the pair, not evidence of which
one is wrong.

## 5. Report and stop

Write the report in the form of [gap-report-template.md](gap-report-template.md):
the header with this skill's version as the auditor; every checklist item
with *pass* or the gap identifiers it produced, so that the report says what
was checked and not only what was found; then one numbered gap per finding,
with the location (clause identifier or section), the check, the text
quoted exactly, and one proposed resolution. One gap holds one question; an
item that bundles two is split. Then **stop** and ask for rulings. Do not
amend any file, and do not re-run after amendments unless asked.

Two findings are not gaps, and the checklist says why: an implementation
choice the specification deliberately leaves open, and a deployment
assumption that is stated as an assumption.
