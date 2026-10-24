# Drafts before the audit

Reference material, not a specification. These are the specifications as
they stood after elicitation and the EARS rewrite and **before** the three
audits of task 6 (`records/audit-01-human.md`, `audit-02-agent.md`,
`audit-03-skill.md`): the working tree that the audits examined. They were
never committed: the build audited every specification change before committing it. They
carry the seven seeded gaps of the A1 plan (G1 to G7), and, as the audits
found, a handful of unseeded ones (forward references to artifacts of later
commits, a missing `Reason` on judgment clauses, an assumption that was a
property of the guard). They are kept so that the audit can be replayed: in
a scratch copy of this snapshot, overlay them onto `specs/` and run
`/audit-spec`, a person, or the ad-hoc prompt of
`reference/prompts/03-audit-adhoc.md`.

```sh
cp reference/drafts/conops.md reference/drafts/glossary.md reference/drafts/requirements.md specs/
```

The drafts are also the **known-violation set** of the `/audit-spec` skill:
any change to the skill is rerun on them and must still find the seven gaps
and report nothing for the one non-gap (REQ-2's value equality, which an
unguided reading tends to flag as an ambiguity about object identity). The
key, with each gap's location, the check that finds it, and the ruling, is
the gap table of `records/audit-03-skill.md`.

`glossary.md` here is identical to the audited glossary; it is kept so that
the overlay above restores the whole family in one step.
