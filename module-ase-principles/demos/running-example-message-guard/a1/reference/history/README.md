# The build's history, as patches

Reference material. The four commits of the A1 build, exported with
`git format-patch` from the repository in which the version was built, in
order:

| Patch | Commit | Tag | What it holds |
|---|---|---|---|
| `01-a1-specs.patch` | the first | `a1-specs` | elicitation, the glossary, the EARS requirements, the three audits of the seeded draft, the two skills; the judgments file arranged by form, the procedures, the gap-list template; the assurance report with ConOps-VAL-1 not holding |
| `02-a1-scenarios.patch` | the second | `a1-scenarios` | the scenario file and its loader; the extended clause reader and plugin; the stories' method becomes *test*; Scen-CONF-1; audit 04 |
| `03-a1-trace.patch` | the third | `a1-trace` | the trace tool, its cases, the evaluation command's third step; Specs-TR-2 |
| `04-a1.patch` | the fourth | `a1` | the validation record and sign-off, ConOps-VAL-1 amended, the README, the tool catalog, the skills at 1.1 and 1.2 with their per-form files; audit 05 |

`../../../build-history.sh TARGET_DIR` (in the directory that holds `a0/`
and `a1/`) recreates the history from the `a0` snapshot and these patches,
tagging each commit. The result is a reconstruction: the dates and the
author are the replay's, and each commit message says so. The patch files
are not part of any commit (they could not be, since they describe the
commits), so the replayed `a1` tree equals this snapshot except for this
directory's `.patch` files.

**Provenance of these patches.** The A1 build was made on 2026-10-22 under
an earlier arrangement of the process files (a single rules file with a
commit trigger in every rule, a hand-written ledger). On 2026-10-24 the
snapshots were re-layered into the arrangement described in
`software-engineering/running-example-relayering.md`: judgment clauses per
form, procedures, records beside reports, and an assurance report compiled
at each commit in place of the ledger. The four trees of the original
commits were re-layered one by one, their evaluations run again, their
assurance reports compiled, and the commits remade in order; these patches
are exported from that remade history. The records (the audits, the
elicitation record, the validation record) keep their original dates,
because the activities they record happened then; the assurance reports
carry the date they were compiled.
