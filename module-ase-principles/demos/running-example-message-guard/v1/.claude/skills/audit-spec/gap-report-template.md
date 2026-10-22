# Gap report (the gap-list form of rule RPT-2)

```markdown
# Audit <NN>: <specifications audited> (version <N>)

| Field | |
|---|---|
| Audit | <NN> |
| Date | <YYYY-MM-DD> |
| Auditor | <a person: name and role · an agent: model, ad-hoc prompt · a skill: /audit-spec <version>, model> |
| Audited | <files and the version or state audited, e.g. the working tree before commit a1-specs> |
| Checks applied | <C-1 to C-14 of checklist.md <version>, or the rule identifiers the repository names> |
| Read first | <the files read in full before the first check> |

## Checks

| Check | Result |
|---|---|
| C-1 Well-formed header | pass · or: G-3 |
| ... | ... |

## Gaps

| Gap | Location | Check | Quoted | Proposed resolution | Ruling | Amendment |
|---|---|---|---|---|---|---|
| G-1 | <clause id or file §section> | C-3 | "<text exactly as written>" | <one concrete proposal> | open | |
| G-2 | ... | ... | ... | ... | open | |

Searched: within each document · between documents · by execution.

**Rulings needed on G-1 to G-n.** Reply per gap: accept the proposal, rule
otherwise, reject with a reason, or defer.
```

The ruling column takes one of: *accepted* (the proposal stands), *ruled:
<text>* (a different resolution), *rejected: <reason>* (not a gap), or
*deferred: <where>* (kept as a want or a backlog item). The amendment column
names what changed (a clause identifier, a section, a glossary term) once the
ruling is applied. The auditor leaves both columns to the person who rules.
