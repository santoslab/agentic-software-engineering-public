# Audit checklist: the index (procedure Audit; skill version 1.2)

Every item is applied and reported, as *pass*, *not in scope*, or the gaps
it produced. Items are cited as C-1 to C-14; the identifiers have been
stable since version 1.1 (version 1.0 cited them as A-1 to A-14, which
collided with the assumption identifiers of the concept of operations;
audit 03 noticed, and 1.1 renamed them). Version 1.2 moved the items into
one file per form, so that a form's items can be read, audited, and
extended on their own; the text of each item is unchanged from 1.1 except
where a form-specific sentence was split out. The judgment each item
serves is SQ unless the item says otherwise.

| Item | Title | Applies to | File |
|---|---|---|---|
| C-1 | Well-formed header | conops (US clauses), reqs (REQ clauses), scen (SC identifiers) | [forms/conops.md](forms/conops.md), [forms/reqs.md](forms/reqs.md), [forms/scen.md](forms/scen.md) |
| C-2 | EARS form | reqs | [forms/reqs.md](forms/reqs.md) |
| C-3 | Glossary discipline | gloss (defined once); conops, reqs, scen (used in the defined sense) | [forms/gloss.md](forms/gloss.md) and each form's file |
| C-4 | Unambiguous | conops, reqs | [forms/conops.md](forms/conops.md), [forms/reqs.md](forms/reqs.md) |
| C-5 | Judgment clauses state why | conops, reqs | [forms/conops.md](forms/conops.md), [forms/reqs.md](forms/reqs.md) |
| C-6 | Implementation-independent purpose and stories | conops | [forms/conops.md](forms/conops.md) |
| C-7 | Complete for the stated scope and level | conops, reqs | [forms/conops.md](forms/conops.md), [forms/reqs.md](forms/reqs.md) |
| C-8 | Derivation both ways | between documents | [forms/between.md](forms/between.md) |
| C-9 | No contradiction | between documents (and within one) | [forms/between.md](forms/between.md) |
| C-10 | One term, one sense | between documents | [forms/between.md](forms/between.md) |
| C-11 | Assumptions are not requirements | between documents | [forms/between.md](forms/between.md) |
| C-12 | Deferred wants stay deferred | between documents | [forms/between.md](forms/between.md) |
| C-13 | References resolve | between documents | [forms/between.md](forms/between.md) |
| C-14 | Examples and scenarios agree with their clauses | scen; the story examples, between documents | [forms/scen.md](forms/scen.md), [forms/between.md](forms/between.md) |

The clauses of `process/judgments.md` cite these items in their *Evaluated
by* fields: ConOps-SQ-1 (C-1, C-4 to C-7, C-11, C-12), Reqs-SQ-1 (C-1, C-4,
C-7, C-8), Reqs-SQ-2 (C-2), Gloss-SQ-1 (C-3, C-10), Specs-SQ-1 (C-8 to
C-14), Specs-TR-1 (C-8, C-13, for the parts a person reads).
