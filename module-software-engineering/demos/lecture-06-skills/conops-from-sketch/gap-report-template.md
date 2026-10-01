# Gap report — template

Use the repository's own gap-list rule (RPT-1 in the course method) if it has
one; this template follows it.

```markdown
## Audit of <sketch file> <version> — <date>

Audits applied: <e.g. AUD-1..7 (process/spec-audit.md 1.2), AUDCON-1..8
(process/conops-audit.md 1.1)> — or "no audit in repository; bundled checklist".

### What the sketch states / implies / leaves out
- **States:** <3–6 bullets of what is decided>
- **Implies:** <what follows from it without being said>
- **Leaves out:** <the open areas, one line each — detailed below>

### Gaps
1. **Where:** <file §x.y, bullet/sentence — or "absent">
   **Category:** ambiguous · incomplete · inconsistent within a document ·
   inconsistent between documents · execution gap
   **Quoted:** "<text as written>" — or the text that should exist and does not
   **Found by:** <rule id, e.g. AUD-1; AUDCON-8>
   **Recommended:** <one concrete proposal; "defer to BACKLOG.md" is allowed as a
   recommendation>
   **Status:** open

2. …

Searched: within the document ✔ · between documents ✔ · document vs. execution
(walkthrough) ✔

**Rulings needed on 1–N.** Reply per number: accept the recommendation, give
another ruling, or defer to the backlog.
```
