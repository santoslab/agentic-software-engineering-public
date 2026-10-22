# Message Guard, version A1

Version A1 of the running example of the agentic software engineering
principles module. The system is the one A0 built, unchanged: one stage,
`filter`, that drops a Critical message and passes anything else unchanged;
`guard/` is byte-identical to v0. Everything that changed is how the product
is specified, checked, and recorded. The concept of operations was revised
through elicitation with its stakeholders, its terms became a glossary, the
requirements were rewritten in EARS, the stories' examples became a scenario
file that any realization must reproduce, the specifications were audited
three times on a draft with seeded gaps, a trace tool resolves every declared
link, two skills package the elicitation and the audit, and the ledger
records two checkpoints. The design is
`software-engineering/running-example-design.md` at the repository root; the
build plan is `software-engineering/running-example-a1-plan-fable.md`.

## The artifacts, by category

| Category | Files | Role |
|---|---|---|
| Intent | none | lives with the stakeholders; consulted through `/elicit` and the sign-off |
| Specifications | `specs/conops.md` (agreed purpose; scope with assumptions A-1 to A-3; user categories; stories US-1 to US-3; deferred wants D-1 to D-3); `specs/glossary.md`; `specs/requirements.md` (REQ-0 to REQ-3, EARS); `specs/scenarios.json` (SC-1 to SC-6) | seven identified verification clauses, all with method *test*; contextual text and the scenarios are reviewed with them |
| Reference | `reference/elicitation.md` (E-1 to E-5, the stakeholders' words); `reference/drafts/` (the specifications before the audit, with the seven seeded gaps); `reference/prompts/` (the EARS-rewrite and ad-hoc-audit prompts); `reference/history/` (the patches that replay the build) | informs the specifications; not audited; no judgment is about it |
| Realization | `guard/` (unchanged); `tests/` (the unit tests of A0, the scenario loader, the tooling tests) | what was built, and the executable claims about it |
| Development rules | `process/rules.md` (SQ-1 to SQ-4, RQ-1, CONF-1, CONF-2, VAL-1, VAL-2, TR-1, TR-2, WF-1, WF-2, RPT-1, RPT-2; four styles; a changelog) | how each judgment is established and when it must hold |
| Skills | `.claude/skills/elicit/`, `.claude/skills/audit-spec/` | the elicitation procedure (WF-2) and the audit procedure (SQ-2), packaged |
| Reports | `reports/ledger.md` (tables at v0, a1-specs, a1-scenarios, a1-trace, v1); `reports/dev-log.md`; `reports/audit-01-human.md`, `audit-02-agent.md`, `audit-03-skill.md` (the three audits of the seeded draft), `audit-04-skill.md`, `audit-05-skill.md` (the clean audits before the later commits); `reports/validation.md`; `reports/conformance.md` and `reports/trace-matrix.md` (generated) | the development state, readable without reading the code |
| Technology | `pyproject.toml`, `uv.lock` | Python 3.12 or later; pytest, pytest-cov, ruff; managed by `uv` |
| Tools | `tools/gate.sh`; `tools/trace.py`; `tools/walk.py` | the gate; the trace tool; the walkthrough helper |
| Tool catalog | `tooling/README.md` and one page per tool | how each tool was specified, prompted for, reviewed, and checked, and how to adapt or share it |

## The five judgments, at this version

| Judgment | Established by | Evidence |
|---|---|---|
| SQ, specification quality | the audit procedure (SQ-2) run by a person, by the agent, and by the `/audit-spec` skill on the draft, with a ruling on every gap; EARS form (SQ-3) and glossary discipline (SQ-4) checked within it; the amended family read together (SQ-1) | `reports/audit-0{1,2,3}.md`; the SQ row of the ledger |
| RQ, realization quality | `ruff check`; the suite collects (RQ-1) | the gate header and exit codes in the dev log |
| CONF, conformance | the aggregate: every test passes; every *test* clause, the four requirements and the three stories, has passing evidence (requirements coverage); 100 percent branch coverage of `guard/` (structural coverage); no clause carries method walkthrough, so CONF-2 has nothing in scope (CONF-1, CONF-2) | `reports/conformance.md`; the coverage table in the gate run |
| VAL, validated | a stakeholder of each user category walks their stories on the running guard and decides (VAL-2), then signs the concept of operations for version A1 (VAL-1) | `reports/validation.md` |
| TR, traceable | every marker, `Derived from`, `Scenarios`, and `Source` reference resolves, in both directions, decided by `tools/trace.py` in the gate (TR-1, TR-2) | `reports/trace-matrix.md` |

The ledger, `reports/ledger.md`, now has three tables: at v0, at a1-specs
(the intermediate checkpoint after the specifications were revised, where
VAL is stale), and at v1. The gate, `tools/gate.sh`, decides RQ, the
mechanical part of CONF, and TR before any commit (WF-1), and prints a header
saying which state it checked and with which tool versions. A1 is the first
version whose dev-log entries each correspond to a commit that passed the
gate: the tags `a1-specs`, `a1-scenarios`, `a1-trace`, and `v1`.

## Running it

```sh
uv sync                                    # once: creates .venv with pytest, pytest-cov, ruff
tools/gate.sh                              # the gate: ruff, pytest with coverage and the plugin, then trace.py
uv run python tools/walk.py Critical 100   # a walkthrough step: prints "drop"
uv run pytest tests/tooling                # the tools' own known-violation cases
```

In a Claude Code session started here, `/elicit` revises the concept of
operations with its stakeholders (rule WF-2) and `/audit-spec` audits the
specifications and stops for rulings (rule SQ-2). To replay the audit on
the pre-audit draft, overlay `reference/drafts/` onto `specs/` in a scratch
copy (`reference/drafts/README.md`).

## Which files are generated, and which are written by hand

| Generated by a run | Written by the agent or the skill, then ruled on by hand | Written by hand |
|---|---|---|
| `reports/conformance.md` (the plugin, every pytest run); `reports/trace-matrix.md` (`tools/trace.py`) | `reports/audit-02-agent.md`, `reports/audit-03-skill.md` (the gap lists; the rulings column is a person's); `reference/elicitation.md` (the questions are the skill's; the answers are the stakeholders') | `reports/ledger.md`; `reports/dev-log.md`; `reports/validation.md`; `reports/audit-01-human.md`; every specification; the rules |

The ledger is still handwritten in A1; A2 generates it from the gate's
outputs and the recorded decisions.

## Breaking it

A0's five sabotages (a wrong realization; a wrong system with a green
ledger; a missing test; an unexercised branch; a dangling marker) still work
as described in `v0/README.md`, with one change worth noticing. Sabotage 4's
branch, `elif message.payload < 0: return None`, is now exercised by scenario
SC-2 (Public, -3): the gate goes red on a failing scenario while coverage
stays at 100 percent, because the stakeholder's example reaches the bug
before the coverage tool does. To see the structural-coverage conjunct alone,
use a condition no scenario reaches, such as `payload < -1000`: every clause
is still cited, every test passes, and coverage drops to 94 percent. A1 adds
five sabotages for the judgments it introduced, each run in a scratch copy
and restored afterwards.

6. **SQ, a contradiction after the audit.** Add to `specs/requirements.md` a
   REQ-6 in good EARS form, "When the filter is given a message whose
   security level is Restricted and whose payload is greater than 1000, the
   filter shall drop the message," with `Method: test`, `Pattern:
   event-driven`, and `Derived from: US-2`; add to `filter.py` the branch
   `if message.level is SecurityLevel.RESTRICTED and message.payload > 1000:
   return None`; add a test that cites REQ-6 with payload 5000 and passes.
   Run the gate: green. Every clause has evidence, the new branch is
   covered, every link resolves, and every scenario passes, because no
   scenario sends a payload above 1000. Run `/audit-spec`: REQ-6 contradicts
   REQ-2 and US-2, which say a Restricted message passes unchanged whatever
   its payload (check C-9). The gate checks what is cited and exercised;
   only the audit checks what is consistent. Restore.
7. **CONF and independence, a shared misreading.** Replace, together, the
   return in `filter.py` with `return Message(message.level,
   abs(message.payload))` for non-Critical messages and the assertion of
   `test_restricted_passes_unchanged` with one that expects the absolute
   value: the agent that wrote both read "unchanged" the same wrong way.
   The unit test passes; `SC-2` (Public, -3), written from the sender's
   words, fails; the gate is red. The verifier that does not share the
   author's reading is the one that catches it (threat T5).
8. **TR, a wrong derivation.** Change REQ-3's `Derived from: US-1` to `US-2`.
   The plugin is green. `tools/trace.py` reports "story without requirement
   at US-1" and the gate is red. Change it to `US-9`: a dangling reference,
   a different finding. Restore.
9. **VAL, scenarios pass and the officer declines.** No command. The
   security officer reads the revised concept of operations and says that a
   Restricted message with a payload above 100 must not leave. Every
   scenario passes, including SC-4, which encodes the opposite. The
   signature is withheld; VAL is not established; nothing else moves. In A1
   the resolution is a sign-off scoped to the version with the want
   deferred, as D-2 is; the unscoped version is A3's change request.
10. **A verifier that has never failed.** Delete one directory under
    `tests/tooling/cases/`. Nothing fails. A finding kind with no case is a
    finding kind nobody has seen the tool report (`tooling/tooling-tests.md`).

### Breaking the verifiers

Four demonstrations of the evidence machinery itself (CF-01), scripted on
`tooling/conformance-plugin.md`: an uncited passing test is accepted; an
invalid citation is rejected; a test clause with no citing test is a
coverage gap; and an uncited failing test fails the suite while every clause
row of the report stays green. The last one is why the gate's exit code, not
the clause table, is the evidence the ledger cites.

## Replaying the history

`../build-history.sh TARGET_DIR` recreates the build as a tagged git
repository from the v0 snapshot and the patches in `reference/history/`
(`tooling/replay.md`). The result is a reconstruction, not the original
history; its commit messages say so.

## Naming against the HAMR example

The guard is the Python sibling of the HAMR Simple Network Guard. Its `Gate`
component is this version's `filter` stage, since in ordinary usage a filter
drops; HAMR's `Filter`, which transforms, will appear as `sanitize` in A2.
HAMR's Req_C, Req_R_1, and Req_P are REQ-1, REQ-2, and REQ-3. HAMR's
No_Input_No_Output has no counterpart here: a library that takes one message
has no "no input" event, which is what the audit said of the draft's REQ-4.
