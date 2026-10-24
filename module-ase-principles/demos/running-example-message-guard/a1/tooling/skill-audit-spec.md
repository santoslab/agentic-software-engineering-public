# `/audit-spec`: the specification audit skill

## Goal

Audit the specifications for specification quality by a fixed procedure
(`Audit` in `process/procedures.md`), form by form, and report every gap in
a fixed form (`process/templates/gap-list.md`), under a version, and stop for
the developer's rulings. It is the verifier skill of
A1: rung 3 of the verifier ladder for the SQ checks, between a person
reading (audit 01) and an agent with an ad-hoc prompt (audit 02), and before
the script that A2 writes for the syntactic items. The assurance report
records its version as provenance.

## Requirements

1. Reads every file in scope in full, the glossary, and the process files,
   before the first check; defers to any SQ clause the repository adds.
2. Applies a fixed checklist, kept as one file per form under `forms/` and
   indexed by `checklist.md` (version 1.2; one file in 1.0 and 1.1), in three
   places: within each
   document (well-formed headers, EARS form, glossary discipline,
   ambiguity, a reason on judgment clauses, implementation independence,
   completeness), between documents (derivation both ways, contradiction,
   one sense per term, assumptions not requirements, deferred wants
   deferred, references resolve), and by execution (examples and scenarios
   against the clauses, with `tools/walk.py` where a realization exists).
3. Reports every item as *pass* or as the gaps it produced, so the report
   says what was checked.
4. Reports gaps in the gap-list form: location, item, exact quotation, one
   proposed resolution, ruling column left to the person.
5. Does not report two things the checklist names as not gaps: an
   implementation choice the specification leaves open, and an assumption
   stated as an assumption.
6. Never amends a file; stops and asks for rulings.
7. Only the developer can start it, and names the forms to audit as its
   arguments (every form under `specs/` by default).

## The prompt

The skill was written by the build agent from the A1 plan's section 8,
condensed to its operative sentences:

> Package procedure Audit as a skill in the house style of the course's
> `conops-from-sketch`: a short body with the reasons, bundled detail, a
> narrow description, and a stop where the person rules. Its first step is
> to read every file under `specs/` in full. Put the checks in a
> `checklist.md` with identifiers, in the order the procedure gives (within,
> between, by execution), with the two negative rules that keep it from
> over-reporting (an implementation choice left open is not an ambiguity; an
> assumption stated as an assumption is not a finding). Put the gap-list form
> in a template under `process/templates/`. Cite identifiers and quote text;
> never amend; report under a version.

## Review points

Every checklist item appears in the report with a result; each gap quotes
the text exactly and names the check; the two negative rules are applied
(the object-identity reading of "unchanged" is not reported); the skill
read the whole family before checking; it ran the examples; it did not edit
anything; it stopped.

## Deliberate-failure checks

The known-violation set is `reference/drafts/`: the pre-audit specifications
with the seven seeded gaps of the A1 plan and, as it turned out, several
unseeded ones. Any change to the skill is rerun on the drafts and must still
find the seven and report nothing for the non-gap. The key is the gap table
of `records/audit-03-skill.md`.

**First run, version 1.0, 2026-10-22** (`records/audit-03-skill.md`):

| | Result |
|---|---|
| Seeded gaps found | 7 of 7 (G1 to G7) |
| The non-gap (object identity) | not reported; listed under "considered and not reported" |
| Unseeded findings | 4: two forward references to artifacts of a later commit (a rule and a record file), the missing `Reason` on three judgment clauses, a story whose `Source` was the other category's answer |
| Items reported pass or finding | 14 of 14, plus one check it added under Specs-SQ-1 |
| By execution | ran `walk.py` on all six examples; one disagreement, the seeded one |
| Files amended | none |
| Against the ad-hoc audit (audit 02) | 02 found the seven and the non-gap, and two content judgments the skill did not (an assumption that described the guard; a deferred want that reopened Critical); 02 missed the two header findings the skill made; 02 invented its own severity scale and read files the prompt did not name |

**Later runs on clean trees.** The build audited before every commit that
changed a specification (a practice, not a rule: nothing in A1 says when the
audit must run), so the skill ran twice more in A1, at version 1.1: audit 04, before commit a1-scenarios (`records/audit-04-skill.md`),
fourteen items, ten pass, four wording gaps, all accepted, one of which
corrected a ruling of audit 03 that the 1.1 checklist does not admit; and
audit 05, before commit a1 (`records/audit-05-skill.md`), on a tree whose
only specification changes were references. A pass report that lists every
item is what the procedure produces once the family is clean, and the cost
of running it is the reason it can run every time.

What the first run changed in the skill (version 1.1, committed with the
audit): the checklist's item identifiers were A-1 to A-14 and collided with
the assumption identifiers A-1 and A-2 of the concept of operations; the
skill noticed and the items are now C-1 to C-14. Item C-5 (a reason on every
judgment clause) said no such clause existed at A1, which was true of the
final state and false of the audited commit; it now applies to whatever the
tree holds. Item C-13 (references resolve) was added because the skill had
to report two findings under a rule with no item to cite. The two content
judgments that only the ad-hoc audit made were not turned into items: they
are judgments of meaning, not checks of form, and a checklist that tried to
hold them would be a list of everything.

**Version 1.2 (2026-10-24): one file per form, the form as the argument.**
The checklist was split into `forms/conops.md`, `forms/reqs.md`,
`forms/gloss.md`, `forms/scen.md`, and `forms/between.md`, with
`checklist.md` left as the index; the items and their identifiers are
unchanged. The skill takes the forms to audit as its arguments, reads the
glossary whatever the scope, and reports the between-document items as *not
in scope* when one form is audited alone. The reason is the per-form
arrangement of the judgments file: a form's clauses, its audit items, and
its elicitation taxonomy are meant to travel together, so that a project
that adds a form adds one file here. The rerun on the known-violation set
that the discipline below asks for after any change to the skill was made
the same day: `records/audit-06-skill.md`, a fresh session running
`/audit-spec` 1.2 on the drafts, found seven of seven seeded gaps, did not
report the non-gap, and reported eighteen gaps against audit 03's twelve,
the difference being the finer split of the per-form files and the items
now read against a fuller judgments file.

## Adapting it to your project

Project-specific: the per-form files for the forms your specifications
use (the EARS item for requirements; a data-format file when there is a
schema; an allocation item when there is an architecture, which A2 adds);
the header format the clause reader fixes; the helper used for the
by-execution step. Carries over as an idea: read everything first; check in
three places; report what was checked; quote; never amend; stop. The
"not a gap" rules are the part most worth copying: they are where the skill
beats a free reading.

## Making it shared infrastructure

Share the skill with the clause-header format and the checklist as one
package; an organization that fixes its specification kinds fixes the
checklist's items with them. Version it, keep the drafts of each project as
its known-violation set, and rerun them on every release: the skill is a
verifier, and a verifier that has never been seen to fail has not been
verified. When a syntactic item becomes a script (A2), the item stays in its form's
file with a note that the script decides it and the audit reports the
script's result.
