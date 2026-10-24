# Message Guard, version A1

Version A1 of the running example of the agentic software engineering
principles module. The system is the one A0 built, unchanged: one stage,
`filter`, that drops a Critical message and passes anything else unchanged;
`guard/` is byte-identical to `a0/`. Everything that changed is how the
product is specified, evaluated, and reported. The concept of operations was
revised through elicitation with its stakeholders, its terms became a
glossary, the requirements were rewritten in EARS, the stories' examples
became a scenario file that any realization must reproduce, the
specifications were audited three times on a draft with seeded gaps, a trace
tool resolves every declared link, two skills package the elicitation and
the audit, and the assurance report was recompiled at each of four commits.
The design is `software-engineering/running-example-design.md` at the
repository root; the build plan was
`software-engineering/running-example-a1-plan-fable.md`; the snapshot was
re-layered on 2026-10-24 as `software-engineering/running-example-relayering.md`
describes.

## The artifacts, by category

| Category | Files | Role |
|---|---|---|
| Intent | none | lives with the stakeholders; consulted through `/elicit` and the sign-off |
| Specifications | `specs/conops.md` (agreed purpose; scope with assumptions A-1 and A-2; user categories; stories US-1 to US-3; deferred wants D-1 to D-3); `specs/glossary.md`; `specs/requirements.md` (REQ-0 to REQ-3, EARS); `specs/scenarios.json` (SC-1 to SC-6) | seven identified verification clauses, all with method *test*; contextual text and the scenarios are audited with them |
| Reference | `reference/elicitation.md` (E-1 to E-5, the stakeholders' words); `reference/drafts/` (the specifications before the audit, with the seven seeded gaps); `reference/prompts/` (the EARS-rewrite and ad-hoc-audit prompts); `reference/history/` (the patches that replay the build) | informs the specifications; not audited; no judgment is about it |
| Realization | `guard/` (unchanged); `tests/` (the unit tests of A0, the scenario loader, the tooling tests) | what was built, and the executable claims about it |
| Judgments | `process/judgments.md` (five definitions; eleven clauses filed by six forms; a changelog); `process/procedures.md` (Audit, Elicit); `process/templates/` (the assurance report, the gap list) | what each claim says, per form, and how it is evaluated; how two activities are carried out; the forms of the records and the report |
| Skills | `.claude/skills/elicit/` (procedure Elicit; `forms/conops.md` is its taxonomy); `.claude/skills/audit-spec/` (procedure Audit; `forms/` holds the items per form, `checklist.md` the index) | the two procedures, packaged; both started by the developer |
| Records | `records/reviews.md`; `records/audit-01-human.md`, `audit-02-agent.md`, `audit-03-skill.md` (the three audits of the seeded draft), `audit-04-skill.md`, `audit-05-skill.md` (the clean audits before the later commits), `audit-06-skill.md` (the skill at 1.2 rerun on the seeded drafts); `records/validation.md` (the validation walkthroughs and the sign-offs, with the earlier walkthrough records as its appendix); `records/dev-log.md` | evidence of what people decided and did |
| Reports | `reports/assurance-report.md` (compiled at commit `a1`; the history holds the one compiled at each earlier commit); `reports/conformance.md` and `reports/trace-matrix.md` (generated) | the development state, readable without reading the code |
| Technology | `pyproject.toml`, `uv.lock` | Python 3.12 or later; pytest, pytest-cov, ruff; managed by `uv` |
| Tools | `tools/evaluate.sh`; `tools/trace.py`; `tools/walk.py` | every mechanical evaluation in one command; the trace tool; the walkthrough helper |
| Tool catalog | `tooling/README.md` and one page per tool | how each tool was specified, prompted for, reviewed, and checked, and how to adapt or share it |

## The five judgments, at this version

| Judgment | Clauses | Evaluated by | Evidence |
|---|---|---|---|
| SQ, specification quality | ConOps-SQ-1, Reqs-SQ-1, Reqs-SQ-2, Gloss-SQ-1, Specs-SQ-1 | the audit (procedure Audit), run on the draft by a person, by an agent, and by the `/audit-spec` skill, with a ruling on every gap, and twice more on clean trees; the clause reader for the header parts | `records/audit-0{1,2,3,4,5}.md`; the SQ section of the assurance report |
| RQ, realization quality | Code-RQ-1 | `ruff check`; the suite collects | the exit codes, quoted in the assurance report with the header of the run |
| CONF, conformance | Reqs-CONF-1, Scen-CONF-1 | the test run: every test passes; every *test* clause, the four requirements and the three stories, has passing evidence (requirements coverage); 100 percent branch coverage of `guard/` (structural coverage) | `reports/conformance.md`; the coverage table of the run |
| VAL, validated | ConOps-VAL-1 | a stakeholder of each user category walks their stories on the running guard with the scenarios' inputs and decides, then signs the concept of operations for version A1 | `records/validation.md` |
| TR, traceable | Specs-TR-1, Specs-TR-2 | the plugin for the citations; `tools/trace.py` for every `Derived from`, `Scenarios`, and `Source` reference, in both directions | the "Unknown identifiers" section of `reports/conformance.md`; `reports/trace-matrix.md` |

The judgments file is arranged by form: the concept of operations, the
requirements, the glossary, the scenarios, the specifications read together,
and the code each have a section with every clause about them. A clause's
first three fields depend only on the form; the fourth, *In this project*,
binds it to this repository. Two activities have procedures of their own,
the audit and elicitation, each with its steps and its stop stated once and
its per-form parts kept with the skill that packages it. Nothing in A1 says
when a claim must hold: as in A0, there is no gate and no rule about
commits. The build audited before every commit that changed a specification
and recompiled the assurance report at every commit, as a practice; A2 turns
such practices into rules.

The assurance report at each commit is in the history: `git show
a1-specs:reports/assurance-report.md` shows ConOps-VAL-1 not holding after
the revision, while the four other judgments hold, and the report at `a1`
shows all five holding, with the VAL row's provenance naming a stand-in for
the stakeholders.

## Running it

```sh
uv sync                                    # once: creates .venv with pytest, pytest-cov, ruff
tools/evaluate.sh                          # every mechanical evaluation: ruff, pytest with coverage and the plugin, then trace.py
uv run python tools/walk.py Critical 100   # a walkthrough step: prints "drop"
uv run pytest tests/tooling                # the tools' own known-violation cases
```

In a Claude Code session started here, `/elicit conops` revises the concept
of operations with its stakeholders (procedure Elicit) and `/audit-spec`
audits the specifications, every form or the forms named as arguments, and
stops for rulings (procedure Audit). Asking the session for the assurance
report makes it run the evaluations, read the records, and write
`reports/assurance-report.md`. To replay the audit on the pre-audit draft,
overlay `reference/drafts/` onto `specs/` in a scratch copy
(`reference/drafts/README.md`).

## Which files are generated, and which are written by hand

| Generated by a run | Written by the agent or the skill, then ruled on or reviewed by hand | Written by hand |
|---|---|---|
| `reports/conformance.md` (the plugin, every pytest run); `reports/trace-matrix.md` (`tools/trace.py`) | `reports/assurance-report.md` (the agent compiles it from the runs and the records); `records/audit-02-agent.md`, `records/audit-03-skill.md`, `audit-04-skill.md`, `audit-05-skill.md` (the gap lists; the rulings column is a person's); `reference/elicitation.md` (the questions are the skill's; the answers are the stakeholders') | `records/dev-log.md`; `records/validation.md`; `records/reviews.md`; `records/audit-01-human.md`; every specification; the judgments and the procedures |

The report is recompiled on request in A1; A2 keeps it between requests as
the ledger, generated from the evaluations' outputs and the records.

## Breaking it

A0's five sabotages (a wrong realization; a wrong system with every
evaluation green; a missing test; an unexercised branch; a dangling marker)
still work as described in `a0/README.md`, with one change worth noticing.
Sabotage 4's branch, `elif message.payload < 0: return None`, is now
exercised by scenario SC-2 (Public, -3): the run fails on a failing scenario
while coverage stays at 100 percent, because the stakeholder's example
reaches the bug before the coverage tool does. To see the structural-coverage
part alone, use a condition no scenario reaches, such as `payload < -1000`:
every clause is still cited, every test passes, and coverage drops to 94
percent. A1 adds five sabotages for the clauses it introduced, each run in a
scratch copy and restored afterwards.

6. **SQ, a contradiction after the audit.** Add to `specs/requirements.md` a
   REQ-6 in good EARS form, "When the filter is given a message whose
   security level is Restricted and whose payload is greater than 1000, the
   filter shall drop the message," with `Method: test`, `Pattern:
   event-driven`, and `Derived from: US-2`; add to `filter.py` the branch
   `if message.level is SecurityLevel.RESTRICTED and message.payload > 1000:
   return None`; add a test that cites REQ-6 with payload 5000 and passes.
   Run `tools/evaluate.sh`: exit 0. Every clause has evidence, the new branch
   is covered, every link resolves, and every scenario passes, because no
   scenario sends a payload above 1000. Run `/audit-spec`: REQ-6 contradicts
   REQ-2 and US-2, which say a Restricted message passes unchanged whatever
   its payload (item C-9). The mechanical evaluations check what is cited
   and exercised; only the audit checks what is consistent, which is why
   Specs-SQ-1 is evaluated by a reader. Restore.
7. **CONF and independence, a shared misreading.** Replace, together, the
   return in `filter.py` with `return Message(message.level,
   abs(message.payload))` for non-Critical messages and the assertion of
   `test_restricted_passes_unchanged` with one that expects the absolute
   value: the agent that wrote both read "unchanged" the same wrong way.
   The unit test passes; `SC-2` (Public, -3), written from the sender's
   words, fails; Scen-CONF-1 does not hold. The verifier that does not share
   the author's reading is the one that catches it (threat T5).
8. **TR, a wrong derivation.** Change REQ-3's `Derived from: US-1` to `US-2`.
   The plugin is green. `tools/trace.py` reports "story without requirement
   at US-1" and the run exits non-zero. Change it to `US-9`: a dangling
   reference, a different finding. Restore.
9. **VAL, scenarios pass and the officer declines.** No command. The
   security officer reads the revised concept of operations and says that a
   Restricted message with a payload above 100 must not leave. Every
   scenario passes, including SC-4, which encodes the opposite. The
   signature is withheld; ConOps-VAL-1 does not hold; nothing else moves. In
   A1 the resolution is a sign-off scoped to the version with the want
   deferred, as D-2 is; the unscoped version is A3's change request.
10. **A verifier that has never failed.** Delete one directory under
    `tests/tooling/cases/`. Nothing fails. A finding kind with no case is a
    finding kind nobody has seen the tool report (`tooling/tooling-tests.md`).

### Breaking the verifiers

Four demonstrations of the evidence machinery itself (CF-01), scripted on
`tooling/conformance-plugin.md`: an uncited passing test is accepted; an
invalid citation is rejected; a test clause with no citing test is a
coverage gap; and an uncited failing test fails the suite while every clause
row of the report stays green. The last one is why the run's exit code, not
the clause table, is what the assurance report quotes for Reqs-CONF-1.

## Replaying the history

`../build-history.sh TARGET_DIR` recreates the build as a tagged git
repository from the `a0` snapshot and the patches in `reference/history/`
(`tooling/replay.md`). The result is a reconstruction, not the original
history; its commit messages say so.

## Naming against the HAMR example

The guard is the Python sibling of the HAMR Simple Network Guard. Its `Gate`
component is this version's `filter` stage, since in ordinary usage a filter
drops; HAMR's `Filter`, which transforms, will appear as `sanitize` in A2.
HAMR's Req_C, Req_R_1, and Req_P are REQ-1, REQ-2, and REQ-3. HAMR's
No_Input_No_Output has no counterpart here: a library that takes one message
has no "no input" event, which is what the audit said of the draft's REQ-4.
