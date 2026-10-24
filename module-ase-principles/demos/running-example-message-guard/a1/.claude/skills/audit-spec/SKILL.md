---
name: audit-spec
description: >-
  Audits the specifications of this repository for specification quality by
  the fixed procedure Audit: read every specification in scope in full, check
  within each document by its form's items, between documents, and by
  executing the examples and scenarios, then report every gap in the
  gap-list form and stop for the developer's rulings. The arguments name the
  forms to audit (conops, reqs, gloss, scen) or paths; the default is every
  form under specs/. Use only when the developer explicitly asks for an audit
  of the specifications. Not for amending a specification, not for eliciting
  one, not for reviewing code or tests.
argument-hint: "[forms (conops reqs gloss scen) or paths, default all of specs/]"
disable-model-invocation: true
allowed-tools: Read Grep Glob
---

# Audit the specifications

Version 1.2. This skill packages procedure `Audit` of
`process/procedures.md`: the steps are the procedure's, stated once for any
form; the items that depend on the form are files under [forms/](forms/),
indexed by [checklist.md](checklist.md).

The specifications are the reference that every test, every conformance
report, and the stakeholders' sign-off rest on. A defect in them gives a
confident answer to the wrong question, and an agent that writes code and
tests from them will realize either reading of an ambiguous clause. This
skill finds the gaps; the developer rules on every one of them. The skill
never amends a file.

## 0. Resolve the scope

`$ARGUMENTS` is a list of forms or paths; if it is empty, the scope is every
form of the table below that has a file under `specs/`.

| Form | Document | Within-document items |
|---|---|---|
| `conops` | `specs/conops.md` | [forms/conops.md](forms/conops.md) |
| `reqs` | `specs/requirements.md` | [forms/reqs.md](forms/reqs.md) |
| `gloss` | `specs/glossary.md` | [forms/gloss.md](forms/gloss.md) |
| `scen` | `specs/scenarios.json` | [forms/scen.md](forms/scen.md) |

A path is mapped to its form by its file name. A form or path that is not in
the table stops the skill: say which forms have items and ask the developer
to add a file under `forms/` before auditing a new form. The glossary is
read whatever the scope, because every form's glossary-discipline item needs
it.

## 1. Read everything first

Read, in full and before the first check: every file in scope, the
glossary, and `process/judgments.md` and `process/procedures.md`. If
`reference/elicitation.md` exists, read it too: it is not audited, but it
says what a stakeholder meant, which a ruling may need. Checking from memory
of an earlier read is the characteristic failure of an agent verifier;
reading first is how this procedure guards against it. If the judgments file
names checks this skill's files do not (an SQ clause added after this
version), apply those too and cite the clause.

## 2. Check within each document

Apply the form's file to each document in scope on its own: well-formed
clause headers, the declared EARS pattern against the sentence, every domain
term defined once in the glossary and used in that sense, a reason on every
judgment clause, no unquantified adjective where a definition or a number is
needed, nothing in a purpose statement that only a builder would see,
completeness for the stated scope. Each file says which items apply to its
form and keeps the item identifiers C-1 to C-14 of the index.

## 3. Check between documents

When the scope has more than one form, apply [forms/between.md](forms/between.md):
every story has at least one requirement and every requirement derives from
a story or a glossary term; no two clauses contradict, in one document or
across two; one term means one thing everywhere; each scenario agrees with
the example of the story it derives from; assumptions are stated as
assumptions and not as requirements; a want recorded as deferred has no
requirement deriving from it; every file, clause, procedure, and record
entry a specification names exists at this commit. When the scope is one
form, report the between-document items as *not in scope* rather than
omitting them.

## 4. Check by execution

For every story example and every scenario in scope, decide from the
clauses what the output must be and compare it with the stated expectation
(item C-14, in [forms/scen.md](forms/scen.md) and in `between.md`). Where
the realization exists, you may also run `uv run python tools/walk.py LEVEL
PAYLOAD` (it needs the developer's permission); a disagreement between the
run and the expectation is a finding about the pair, not evidence of which
one is wrong.

## 5. Report and stop

Write the record in the form of `process/templates/gap-list.md`: the header
with this skill's version as the auditor and the scope as audited; every
item of the index with *pass*, *not in scope*, or the gap identifiers it
produced, so that the record says what was checked and not only what was
found; then one numbered gap per finding, with the location (clause
identifier or section), the item, the text quoted exactly, and one proposed
resolution. One gap holds one question; an item that bundles two is split.
Then **stop** and ask for rulings. Do not amend any file, and do not re-run
after amendments unless asked.

Two findings are not gaps, and the items say why: an implementation choice
the specification deliberately leaves open, and a deployment assumption that
is stated as an assumption.
