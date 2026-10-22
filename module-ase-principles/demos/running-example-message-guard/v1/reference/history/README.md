# The build's history, as patches

Reference material. The four commits of the A1 build, exported with
`git format-patch` from the repository in which the version was built, in
order:

| Patch | Commit | Tag | What it holds |
|---|---|---|---|
| `01-a1-specs.patch` | the first | `a1-specs` | elicitation, the glossary, the EARS requirements, the three audits of the seeded draft, the two skills, five rules; the ledger with VAL stale |
| `02-a1-scenarios.patch` | the second | `a1-scenarios` | the scenario file and its loader; the extended clause reader and plugin; the stories' method becomes *test*; audit 04 |
| `03-a1-trace.patch` | the third | `a1-trace` | the trace tool, its cases, the gate's third step and header; rule TR-2 |
| `04-v1.patch` | the fourth | `v1` | the validation record and sign-off, rule VAL-2, the ledger at v1, the README, the tool catalog; audit 05 |

`../../../build-history.sh TARGET_DIR` (in the directory that holds `v0/`
and `v1/`) recreates the history from the `v0` snapshot and these patches,
tagging each commit. The result is a reconstruction: the dates and the
author are the replay's, and each commit message says so. The patch files
are not part of any commit (they could not be, since they describe the
commits), so the replayed `v1` tree equals this snapshot except for this
directory's `.patch` files.
