# The Running Example in Spec Kit: a Mapping

> Status: design note, 2026-10-20, first round. Responds to
> `speckit-exploration-prompt.md`. Nothing is built; the note proposes options
> and the user chooses one before anything under `demos/` changes. Vocabulary
> follows `../glossary.md`; the running example is `running-example-design.md`
> (cited by section, "design 2.6"); version A0 is
> `../module-ase-principles/demos/running-example-message-guard/a0/`; the Spec
> Kit material is the tic-tac-toe demo,
> `../module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/`
> ("the demo"), at Spec Kit 1.1.1 in skills mode.

## 0. What this note settles

1. For each concept the running example makes explicit, where it lands in Spec
   Kit's workflow, what Spec Kit already has, where the gap is, and what would
   have to be added (section 2, with the step-by-step reading in section 3 and
   the gaps regrouped by what fills them in section 4).
2. Whether Spec Kit can represent three further things: a choice among classes
   of specification, CONF rules set up per chosen form, and RQ rules set up per
   kind of realization file (section 5).
3. Where Spec Kit's vocabulary conflicts with the glossary and which word wins
   where (section 6).
4. Three options for producing A0, and then A1, through Spec Kit, with a
   recommendation (section 7), and the decisions left to the user (section 8).

Two caveats frame everything below. First, Spec Kit is **per feature**: one
`specs/NNN-name/` directory per feature, each with its own `spec.md`,
`plan.md`, `tasks.md`; the running example's concept of operations is
system-level and governs every feature. A0 is a single feature (F1), so the
mismatch does not bite until A2 adds a second. Second, the baseline is the
version the demo installed, 1.1.1. Three mechanisms matter and all three are
present at that version, confirmed in the demo's own files: templates resolve
through an override stack whose first layer is `.specify/templates/overrides/`
(`.specify/scripts/python/common.py`, lines 319 to 329); every skill reads
`.specify/extensions.yml` for `hooks.before_<cmd>` and `hooks.after_<cmd>`
entries and turns a dotted command name into a slash command, so a
project-local skill can be a hook target (`speckit-implement/SKILL.md`, lines
25 to 33); and a bundled workflow runs specify, a human gate, plan, a human
gate, tasks, implement (`.specify/workflows/speckit/workflow.yml`). Presets,
workflow overlays and packaged extensions are documented upstream and are
reported in 4.6 with that caveat.

The demo's tutorial already maps the Lecture 03 artifacts and the fifteen
catalog kinds onto Spec Kit's files (`tutorial/speckit-walkthrough.md`,
sections 13.1 to 13.3). This note does not repeat that; it maps the running
example's *judgments, records and rules*, which the tutorial does not cover.

## 1. The two sides

**The running example** makes these concepts explicit, each with a home in A0:

| Concept | Design | In A0 |
|---|---|---|
| intent with no artifact; the purpose statement | 2.1, 2.2 | no file; `specs/conops.md` section 1 |
| the concept of operations and the requirements as identified clauses, each with a verification method and a derivation | 2.6, 4A | `**US-1** · Method: walkthrough (human) · User category: message sender`; `**REQ-1** · Method: test · Derived from: US-3` |
| the five judgments SQ, RQ, CONF, VAL, TR | 2.1 | the five rows of `reports/ledger.md` |
| conformance as four conjuncts: tests pass, requirements coverage, structural coverage, judgment clauses walked | 2.1, 2.5 | the plugin in `tests/conftest.py`, `pytest-cov`, `reports/walkthrough.md` |
| the ledger with provenance on every row | 2.1, 2.9 | `reports/ledger.md`, columns Judgment, Status, Evidence, Provenance, Goes stale when |
| the rules file in template form, with styles | 2.3, 2.8 | `process/rules.md`: eight rules, fields Style, Maintains, When, Statement, Decided by, Evidence, On failure, Example; styles obligation and gate |
| the gate | 2.1 | `tools/gate.sh` behind WF-1: `ruff check`, then `pytest` with the plugin and coverage |
| the sign-off | 2.1 | `reports/walkthrough.md`, "Sign-off": who, in which role, when, on which document version |
| traceability | 2.1 | markers resolve to clauses; "derived from" resolves; the "Unknown identifiers" section of `reports/conformance.md` |

**Spec Kit** is eight steps, each a skill that reads some files and writes
others, plus two more and the demo's additions:

| Step | Reads | Writes |
|---|---|---|
| constitution | the principles the user states | `.specify/memory/constitution.md`, with a Sync Impact Report and a semver version |
| specify | a natural-language description (the `$ARGUMENTS`, in the demo a seed file passed as `@file`) | `specs/NNN-name/spec.md`; `checklists/requirements.md` (sixteen fixed quality items) |
| clarify | `spec.md` | `spec.md`: a `## Clarifications` section and the answers applied to the sections |
| plan | `spec.md`, the constitution, technical arguments | `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md` |
| tasks | `plan.md`, `spec.md`, the Phase 1 files | `tasks.md` |
| implement | `tasks.md`, the checklists' checkbox state | code and tests; `[X]` on tasks |
| analyze | `spec.md`, `plan.md`, `tasks.md`, the constitution | a report, no file (the demo saved one on request as `analysis-report.md`) |
| checklist | the same three, plus up to five questions to the user | `checklists/<domain>.md` |
| converge | the three, the constitution, the code | an appended `## Phase N: Convergence` in `tasks.md`, or nothing |
| taskstoissues | `tasks.md` | GitHub issues |

The demo adds, outside Spec Kit: a pytest plugin that turns
`@pytest.mark.req("FR-008", "US1-6")` markers into `reports/conformance.md`
(statuses pass, FAIL, manual, partial, no evidence; an "Unknown IDs" section),
`tests/test_architecture.py` (an `ast` walk enforcing the module dependency
rule), `tests/test_manual_checks.py` (a test that skips with the reason
`manual: quickstart.md ...` so that one success criterion shows as *manual*
rather than *no evidence*), and per-feature `CHANGELOG.md` entries with
"decided by the developer". It has no linter, no coverage measurement, no
commit gate, no ledger, no sign-off, and no record of who performed the manual
walkthroughs that `quickstart.md` lists.

## 2. Mapping table

Columns: the concept; the step and file where it lands; what Spec Kit or the
demo already has, named by field or mechanism; the verdict; the kind and rung
of the verifier behind the equivalent (design 2.7: 1 human, 2 agent, 3 skill,
4 program); what would have to be added, tagged with the kind of addition the
prompt names: **principle** (a constitution principle), **template** (a
template change), **skill** (a custom skill), **plugin** (the conformance
plugin and coverage), **ledger** (a ledger step), or **outside** (not
expressible in Spec Kit).

| Concept | Lands in | Spec Kit has | Verdict | Verifier | Add |
|---|---|---|---|---|---|
| Intent, no artifact | specify's argument; clarify's questions | the description is consumed and survives only as the spec header's `Input:` line; clarify consults the person | equivalent: Spec Kit also keeps no intent artifact | human | nothing; the note says so |
| Purpose statement | spec.md | no section; the demo passed a seed ConOps as `@file` and the template's nearest field is each story's "Why this priority" | gap | none | **template**: a `## Purpose` section, written as a clause and audited |
| ConOps: scope and boundary, user categories, stories with example messages, each marked walkthrough | spec.md, "User Scenarios & Testing" | prioritized stories P1 to P3, each with a description, "Independent Test", and numbered Given/When/Then acceptance scenarios; "Edge Cases"; "Assumptions"; scenarios carry no identifiers | partial | human or agent | **template**: story identifiers `US-n`, `Method:` and `Example:` lines, a scope section and a user-category section; the per-feature caveat of section 0 |
| Requirements as clauses with method and derivation | spec.md, "Requirements" | `- **FR-001**: System MUST ...`; `SC-001` measurable outcomes; at most three `[NEEDS CLARIFICATION]` markers; no method, no derivation; the nearest method mapping is the demo's contracts' "Evidence expected" tables and the test-tag lists in its tasks, both demo conventions | partial | none | **template**: the header `**REQ-n** · Method: ... · Derived from: ...`; a checklist item; later a script |
| SQ | specify's built-in `checklists/requirements.md`; clarify's taxonomy scan (ten categories rated Clear, Partial, Missing); checklist ("unit tests for requirements writing"); analyze (passes A to F, four severities, read-only) | the audit activity is well covered, per feature, over spec, plan and tasks | equivalent as an audit at rungs 1 and 2; gap for the rung-4 syntactic checks and for the two clause rules (a method on every clause; a reason on every judgment clause) | human (checklist ticks), agent (analyze) | **template** (checklist items), later a script in the gate |
| RQ | plan's Technical Context ("Testing:", no linting field); constitution; tasks Setup ("configure linting and formatting tools"); implement's final validation | nothing runs a linter, a type checker or test collection; the demo configures none | gap | none | **principle** RQ-1; a task; the gate script; later a per-language set-up (5.3) |
| CONF 1: every test passes | tasks ("Tests are OPTIONAL"), implement (TDD when tests exist) | tests are run by the agent during implement; no gate | partial | agent | **template**: tests required; the gate |
| CONF 2: requirements coverage | the demo plugin; analyze's "Coverage Summary" (requirement to task); converge (code against the triad) | the plugin computes it from markers and reports it; it does not fail the run; analyze's coverage is to tasks, not tests | partial, and demo-only | program (plugin, rung 4); agent (analyze, converge) | **plugin**: A0's variant, which reads the method from the clause and fails on *no evidence* or an unknown identifier |
| CONF 3: structural coverage | nothing | nothing | gap | none | **plugin**: `pytest-cov`, branch, fail-under |
| CONF 4: judgment clauses walked | plan's `quickstart.md` ("Manual walkthroughs" M1 to M8); `test_manual_checks.py`; converge as an agent walkthrough | a script to walk exists; no record of who walked, when, against which commit, what was observed | partial | human (unrecorded) | **template**: the walkthrough record form (CONF-2) and one walkthrough task per judgment clause |
| VAL and the sign-off | the workflow's `gate` steps (approve or reject, verdict in the run's `state.json`); implement's checklist gate ("proceed anyway?"); clarify | gates approve the quality of the spec or the plan, not that the system is the one wanted; the verdict is machine-local | gap | human | **skill** `signoff` or a hand-written section: who, role, date, document version |
| TR | FR, SC, T identifiers; `[USn]` labels; analyze's Coverage Summary and "Unmapped Tasks"; the plugin's "Unknown IDs"; `test_conformance.py` pins the identifier set | requirement to task by an agent; requirement to test by a program; story to requirement absent; one direction only | partial | agent and program | **template**: the derived-from field; a resolver script; the trace matrix at A1 |
| Ledger with provenance | nothing; the nearest are checklist checkbox state, a saved analysis report, converge's "Converged" line, the workflow run's `state.json`, the constitution's Sync Impact Report, the per-feature CHANGELOG | no table of judgments at a commit; no provenance | gap | none | **ledger**: `reports/ledger.md` and a `ledger` skill (rung 3) |
| Staleness | nothing; the Sync Impact Report lists "templates requiring updates" when the constitution changes; spec.md carries `Status: Draft` | no invalidation on artifact change; analyze and converge are re-run on demand | gap | none | a WF staleness rule; the ledger tool compares recorded versions (A2) |
| Rules file: template form and styles | the constitution (principles with MUST and SHOULD, a rationale, a Governance section with semver and an amendment procedure); the plan's Constitution Check; the templates (forms); the skills (procedures) | a home for rules, not the form: no decider, evidence or on-failure field, no filing by judgment; styles present implicitly: obligation and policy (principles), gate (Constitution Check), change control (Governance), procedure (skills), form (templates); staleness absent | partial | agent (Constitution Check) | **principle**: write the eight rules into the constitution in the eight-field form, one section per judgment |
| Algorithmic gate | nothing before a commit; `check_prerequisites.py` checks that files exist; a workflow shell step can condition on an exit code | Spec Kit does not touch git (branches come from a hook) and has no commit hook | gap | none | **outside**: `tools/gate.sh` behind a git or Claude Code hook; or a `verify` skill on `after_implement` |
| Approval gate | the plan's `GATE` line (filled as a PASS table by the agent); implement's checklist gate; the workflow `gate` | the decider is the agent, or the decision is not in the repository | partial | agent or human | name the decider; record the decision in an artifact |
| Reports: dev log, conformance report, walkthrough record | `reports/conformance.md` (demo); CHANGELOG.md with the reason and "decided by the developer"; commit trailers `Change type: II(c)`; the analysis report on request | the conformance report exists; the dev log is split between CHANGELOG and `git log`; no walkthrough record | partial | program; human | RPT-1: a dev log, or CHANGELOG plus `git log` declared to be it |
| Technology form | plan's Technical Context; `pyproject.toml` | Language, Dependencies, Testing, Platform, Constraints | equivalent | none needed | nothing |
| Reference | `research.md` (Decision, Rationale, Alternatives); the seeds; the Clarifications section | research is reference and is treated as such; the Clarifications section is reference embedded in a specification | partial | none | the ruling in 6 |
| Plan, tasks, waves (A2) | `plan.md`; `tasks.md` phases with a Checkpoint after each story | phases are waves; a Checkpoint is a wave end with no decider and no record | nearest home | agent | later version |
| Change request and report (A3) | CHANGELOG; constitution principle II(c); converge's gap table | the reason for a change is recorded; the affected identifiers and the rows re-established are not | nearest home | human | later version |
| Verification plan (A4) | plan's Technical Context "Testing:"; the demo's research entry R7 "conformance evidence and reports" | the per-project choices have a place to be written but no form | nearest home | none | later version |

Three rows deserve a sentence each. The SQ row is Spec Kit's strength: the
course's audit, with its gap list and its ruling by a person, is what clarify,
checklist and analyze do, at rung 2, and the built-in requirements checklist is
the rung-1 form. The CONF rows are its weakness: nothing in core Spec Kit
produces evidence that code conforms to a clause; the only step that looks at
the code against the specification is converge, and converge produces tasks,
not evidence. The ledger and staleness rows are absent outright: Spec Kit has
no notion of a development state whose judgments go stale when an artifact
changes.

## 3. Each step read in the course's terms

**constitution.** A process specification (design 4B, "development rules"),
written as numbered principles in prose with a rationale and governed by its
own Governance section: amendments by the developer, semver (MAJOR when a
principle is removed or redefined, MINOR when one is added, PATCH for wording),
a Sync Impact Report prepended as an HTML comment. In the demo it was built,
nearly word for word, from `demo-seeds/ASE-seed-development-rules.md` and
holds five principles: specification and realization distinct; a realization
changes for one of three recorded reasons; a person decides which side changes;
derived documents follow governing ones; reports explain. Its one gate is the
compliance review: "every implementation plan MUST pass its Constitution Check
against Principles I–V before work begins." In course terms the constitution is
the right home for the rules, but a principle is not yet a rule: it has no
decider, no evidence, no failure behavior (design 2.8, principle 2), and the
file is not organized by the judgment each principle maintains. The constitution
is also *project-level and standing*, which matches the course's "development
rules" and does not match its "plan".

**specify.** Produces the feature specification from a description and allows
at most three `[NEEDS CLARIFICATION]` markers. It also writes the built-in
quality checklist, sixteen fixed items, and re-validates the spec against it up
to three times. In course terms it writes the ConOps half (user stories,
scenarios, edge cases) and the requirements half (FR, SC, key entities) of one
feature in one file, and performs a first rung-1 SQ check with a form. What it
cannot write with the stock template is the clause form the course needs: no
`Method:`, no `Derived from:`, no story identifiers, no purpose statement.

**clarify.** The procedure the user has already chosen as the model for A1's
elicitation. The exact rules, from `speckit-clarify/SKILL.md` lines 131 to
200: a taxonomy of ten categories is scanned and each rated Clear, Partial or
Missing; a queue of candidate questions is built and capped at five for the
whole session, chosen by impact times uncertainty; exactly one question is
presented at a time, never revealing the queue; a question is a full
interrogative, followed by one "Why it matters" sentence; for multiple choice
the recommended option comes first (`**Recommended:** Option [X] - <reasoning>`),
then a table of options A to E, and the user may answer with a letter, "yes",
or a short answer; after each accepted answer the skill appends `- Q: ... → A:
...` under `## Clarifications / ### Session YYYY-MM-DD` and applies the answer
to the section it affects (a requirement bullet, a story, an entity, a measurable
success criterion, an edge case, or a normalized term), replacing contradicted
text rather than adding to it. In course terms clarify is an elicitation
procedure (style: procedure) whose record it writes *into the specification*.
The glossary files the record under reference, not audited; the ruling is in
section 6.

**plan.** Reads the spec and the constitution; fills a Technical Context (the
technology form); fills the Constitution Check, a table the agent completes
with PASS or a justification (`*GATE: Must pass before Phase 0 research.
Re-check after Phase 1 design.*`); writes `research.md` (Decision, Rationale,
Alternatives per open question: reference), `data-model.md` (entities, fields,
validation rules, state transitions: the glossary and data-format forms, and in
the demo two ASCII state machines), `contracts/` (per-operation signatures with
pre- and postconditions, and in the demo the numbered CLI rules C-1 to C-17 with
an "Evidence expected" table mapping each clause to spec identifiers: the
interface-contract form), and `quickstart.md` (runnable scenarios: the
walkthrough procedure). In course terms plan is where the *forms* of the family
are chosen, but the choice is made by a fixed template menu plus the agent's
judgment, not by the developer (section 5). Its "GATE" is a review (agent) with
no exit code and no recorded human decision, so it is not a gate in the
glossary's sense; the ruling is in section 6.

**tasks.** Writes `tasks.md` in phases: Setup, Foundational, one phase per user
story with a Checkpoint, Polish. Format `- [ ] T001 [P] [US1] Description with
file path`. Tests are optional ("only include them if explicitly requested in
the feature specification"); there is no field for the requirement a task
realizes, only the story label. The demo's constitution forced a convention on
top: every test carries `@pytest.mark.req(...)` and every task names the
identifiers its tests tag. In course terms a task list is the build plan (design
4B) with phases as waves and Checkpoints as wave ends without a decider; the
course needs every task to cite the clauses it realizes and the tests to be
required, both template changes.

**implement.** First reads every checklist's checkbox state as a gate: if any
item is unchecked it stops and asks "Do you want to proceed with implementation
anyway?", and it must not change the markers. Then it executes the phases in
order, in TDD order when tests exist, marks tasks `[X]`, and "validates" against
the spec, plan and tests. In course terms the checklist gate is an approval gate
whose decision is the user's yes at the prompt, not recorded; the final
"validation" is verification by the agent (rung 2) and not the glossary's
validation; and nothing here produces evidence a person can reread. The
`after_implement` hook is the lifecycle point where a `verify` skill would run
the gate and write the reports.

**analyze.** "STRICTLY READ-ONLY." Builds an inventory keyed by FR and SC
identifiers, maps tasks to requirements by identifier or keyword, and runs six
passes: duplication, ambiguity (vague adjectives, placeholders),
underspecification, constitution alignment, coverage gaps (requirements with no
task, tasks with no requirement), inconsistency (terminology drift, entity
mismatch, ordering conflicts). Severities: CRITICAL (a constitution MUST
violated, a core artifact missing, a requirement with zero coverage that blocks
baseline function), HIGH, MEDIUM, LOW; at most fifty findings. The report has a
findings table (ID, Category, Severity, Location, Summary, Recommendation), a
Coverage Summary (Requirement Key, Has Task?, Task IDs), constitution issues,
unmapped tasks, metrics, and an offer to propose edits. The demo's saved run
found 1 CRITICAL, 1 HIGH, 5 MEDIUM, 10 LOW over 26 requirements and 40 tasks,
the CRITICAL being `tasks.md` weakening a constitution MUST to "should". In
course terms analyze is an *audit* of the feature triad against the
constitution at rung 2: a procedure with a gap-list form. Its "coverage" is the
TR link requirement to task, not requirements coverage, and it never reads
code or tests (tutorial 9.4).

**checklist.** "Checklists are UNIT TESTS FOR REQUIREMENTS WRITING"; the
metaphor is "If your spec is code written in English, the checklist is its unit
test suite." Items that start "Verify", "Test", "Confirm" or "Check" against
implementation behavior are prohibited. Each item is a question with a quality
dimension and a reference (`[Clarity, Spec §NFR-2]`), at least eighty percent of
items traceable; categories are completeness, clarity, consistency, acceptance
criteria quality, scenario coverage, edge cases, non-functional requirements,
dependencies, ambiguities. The reviewer owns the checkboxes: `[x]` means the
criterion is satisfied for requirements quality, "It does not mean
implementation work is complete." In course terms a checklist is the gap-list
*form* of an SQ audit, generated per feature and per domain, with a person
ruling on each item: rung 1 with a form written by an agent. It has no standing
rule behind it with a decider and evidence; the SQ rules are that standing
part, and a checklist is an instance of running them.

**converge.** Runs after implement; reads the triad "as the sole source of
intent" and the code; inventories one key per FR, per buildable SC, per
acceptance scenario (`US1/AC2`), per plan decision and constitution principle;
classifies each as missing, partial, contradicts or unrequested; appends a
`## Phase N: Convergence` of tasks or leaves `tasks.md` byte-for-byte unchanged
and reports "Converged". It treats "completion claims are not evidence" and
checks the code regardless of task checkboxes. In course terms converge is a
*review (agent)* of conformance at rung 2, and the only Spec Kit step that
compares code with specification. It produces tasks, not evidence; its verdict
line is the nearest thing Spec Kit has to a CONF row, and it carries no
provenance and no scope.

**The hooks and the workflow.** A hook entry under `hooks.before_<cmd>` or
`hooks.after_<cmd>` names a command (`speckit.verify` becomes
`/speckit-verify`), with `optional`, `enabled`, `priority`, `prompt`,
`condition`; a mandatory hook is executed, an optional one is offered. The
bundled workflow places a human `gate` (approve or reject, `on_reject: abort`)
after specify and after plan. In course terms a mandatory hook is the place for
an algorithmic gate inside Spec Kit's lifecycle, and a workflow gate is an
approval gate whose record is the run state, not the repository.

## 4. The gaps, grouped by what fills them

### 4.1 Constitution principles

Write the course's rules into the constitution in the eight-field form, one
section per judgment, so that the constitution *is* `process/rules.md`. A0's
eight rules fit: SQ-1, RQ-1, CONF-1, CONF-2, VAL-1, TR-1, WF-1, RPT-1, within
the budget of design 2.3. The constitution's Governance section already gives
semver and an amendment procedure, which is change control; "identifiers are
never renumbered" is added as a Governance sentence. The plan's Constitution
Check then lists rule identifiers rather than principle numerals, and analyze's
constitution-alignment pass reads a rule's Statement as the MUST it checks. One
rule in the form the constitution would carry, taken from A0 unchanged:

```
## CONF-1 · Every mechanical clause has passing evidence, and the code is exercised
| Style      | obligation |
| Maintains  | CONF |
| When       | at every commit; applies to every clause whose method is *test* |
| Statement  | Every clause with method *test* MUST be cited, by marker, by at
|            | least one test; every citing test MUST pass; and the suite MUST
|            | reach 100 percent branch coverage of `guard/`. |
| Decided by | analysis: `uv run pytest` with the plugin and `pytest-cov` |
| Evidence   | `reports/conformance.md`; the coverage table |
| On failure | a test is added or fixed, or the code is fixed; a clause is
|            | never weakened to make the run pass |
| Example    | REQ-1 is cited by `test_filter.py::test_critical_is_dropped` |
```

What this does not fix: the constitution is prose for an agent to read, and
nothing in Spec Kit executes a Decided-by field. The field tells the `verify`
skill and the person what to run; it does not run itself.

### 4.2 Template changes

All five are project-local files under `.specify/templates/overrides/`,
resolved before the core templates.

| Template | Change | Fills |
|---|---|---|
| spec | a `## Purpose` section; `## Scope and system boundary` with Terms; `## User categories`; stories as `**US-n** · Method: walkthrough (human) · User category: ...` with an `Example:` line; requirements as `**REQ-n** · Method: ... · Derived from: ...`; success criteria kept only if a clause needs them, each with a method; the `Status:` header replaced by a version line "agreed <date>" | purpose statement; ConOps; clause form; derivation |
| constitution | the eight-field rule form in place of free principles; sections per judgment; the Governance sentence on identifiers | rules file |
| plan | the Constitution Check as a table of rule identifiers; a `## Specification forms` table (form, needed because, verification method, coverage objective, rule); a `## Verification` section (gate command, coverage objectives, the method values in use); Phase 1 files made conditional on the forms table | forms choice (5.1); verification objectives; the technology form stays as Technical Context |
| tasks | "Tests are REQUIRED"; a `Clauses:` field per task; one walkthrough task per judgment clause; a final task that runs the gate and writes the ledger | CONF 1 and 4; TR; the ledger step |
| checklist | SQ items that the course needs and the stock sixteen do not state: every clause carries an identifier and a method; every judgment clause states why it is not mechanical; every "derived from" resolves; EARS form (from A1); glossary discipline (from A1) | SQ |

### 4.3 Custom skills

| Skill | Rung | Reads | Writes | When |
|---|---|---|---|---|
| `speckit-verify` | 3, calling rung-4 programs | the gate command from the constitution or plan | runs `tools/gate.sh`; records exit codes, the coverage table and the conformance summary in the dev log | `after_implement` hook (mandatory); before a commit |
| `speckit-signoff` | 1, with a form | the ConOps; the user categories | the Sign-off section: the stakeholder's statement, role, date, document version; one line per user category | after the walkthroughs; again whenever the ConOps changes |
| `speckit-ledger` | 3 | exit codes recorded by verify, `reports/conformance.md`, the coverage table, the checklist state, the walkthrough record, the sign-off, the current commit | `reports/ledger.md`: five rows with evidence, provenance and "goes stale when"; marks a row stale when an artifact it depends on changed since the recorded commit | the last step before a commit; after `verify` and `signoff` |
| `speckit-walkthrough` (optional) | 1, with a form | the judgment clauses and their examples; `quickstart.md` | the walkthrough record: Clause, Role, Command, Observed, Finding, with who and when | after implement, before the ledger |

Each skill is rung 3 of the ladder by construction: a procedure packaged so
that every run follows the same steps and reports under the skill's version.
The elicitation procedure for A1 does not need a new skill if clarify is used
as is; it needs one (`speckit-elicit`, a thin wrapper around clarify's protocol)
only if the record is to go to `reference/elicitation.md` rather than into the
spec (section 6, 8).

### 4.4 The conformance plugin and coverage

Use A0's `tests/conftest.py` and `tests/conformance.py`, not the demo's: A0's
reads the method from the clause header (`^\*\*([A-Z]+-\d+)\*\* · Method:
(\w+)`), prints a walkthrough row for a judgment clause instead of *no
evidence*, computes "N of M test clauses have passing evidence", and fails the
run on a gap or an unknown identifier unless tests were deselected. The only
change for Spec Kit is where it reads clauses from: `specs/*/spec.md` (and
`specs/conops.md` once that exists) instead of A0's two files. Add `pytest-cov`
with `--cov-branch --cov-fail-under` to `addopts`, as A0's `pyproject.toml`
does and the demo's does not. Spec Kit's own identifier families (FR, SC, the
synthesized `US1-2` scenario keys) are replaced by the course's `US-n`, `REQ-n`
and, later, `ARCH-n`, `IF-n`, `ST-n`; the plugin's regex already accepts any
`[A-Z]+-\d+`.

### 4.5 The ledger step, and what stays outside

The ledger step lands *after* implement, verify and sign-off, at the commit:
the point at which all five judgments have evidence to cite. In Spec Kit's
lifecycle that is either the end of an `after_implement` hook chain
(`verify`, then `ledger`, in priority order) or an explicit `/speckit-ledger`
before committing. Staleness is not expressible in Spec Kit and is done by the
ledger skill itself: each row records the commit it was established at, and a
later run compares.

Two things stay outside Spec Kit. The **commit gate**: Spec Kit never touches
git (even the feature branch comes from a hook), so WF-1 is enforced by a git
`pre-commit` hook or a Claude Code hook that runs `tools/gate.sh`, exactly as A0
does today without Spec Kit. **Staleness on a declared change of mind** (VAL
going stale when no file changed, design 2.1): no Spec Kit step observes a
stakeholder's declaration; it enters as a change request (A3) that the ledger
skill reads.

### 4.6 Upstream mechanisms beyond 1.1.1

Reported with a version caveat; none is needed for A0 or A1.

- **Presets** (`.specify/presets/<id>/` with `preset.yml`, `templates/`,
  `commands/`, `scripts/`; strategies replace, prepend, append, wrap) override
  templates, commands and terminology across projects and stack by priority.
  A course preset would carry 4.2 and the vocabulary of section 6.
- **Extensions** (`extension.yml`; `commands/`, `templates/`, `scripts/`;
  hooks declared into `.specify/extensions.yml`; a config template) package 4.3
  and 4.4 so that `specify extension add` installs them.
- **Workflow overlays** (`.specify/workflows/overlays/<id>/*.yml`, with
  `insert_after`, `insert_before`, `replace`, `remove`) add steps to the bundled
  workflow without forking it: a shell step `ruff check` after implement is the
  documented example, and a shell step with a `condition` on `exit_code` is an
  algorithmic gate at the workflow level.
- **Custom step packages** (`step.yml` plus a Python `StepBase` subclass) could
  make `ledger` a workflow step type rather than a skill.

## 5. The three capability questions

### 5.1 Classes of specification

**Can Spec Kit represent a choice of specification forms, made at planning, with
the CONF framework set up for the forms chosen?** Partly, and only by changing
the plan template.

What it does today: the plan template fixes an implicit menu. Phase 0 always
writes `research.md`; Phase 1 always writes `data-model.md`, `contracts/` and
`quickstart.md`. Which *forms* appear inside them is the agent's decision: the
demo's `data-model.md` acquired two ASCII state machines (GameState; the CLI
session with START_MENU, PLAYING, GAME_OVER) because the agent judged them
useful, and `contracts/cli.md` acquired seventeen numbered binding rules with
an "Evidence expected" table because the constitution's demand for evidence
pushed it there. Nothing asked the developer which forms the system needs, and
nothing attached a verification objective to a form once it appeared: the two
state machines have no transition-coverage objective and no test task was
generated from them.

What would make it a capability: a `## Specification forms` table in the plan
template (4.2), filled by the agent from the catalog (`../specification-kinds.md`
and design 4A) and *approved by the developer at the review-plan gate*, with
one row per form: the form, why this system needs it, its verification method
(design 2.5: verifier, specification coverage, realization coverage, evidence),
and the rule it falls under. Each form named in the table then has a
sub-template in `.specify/templates/overrides/forms/<form>.md` (a state
machine as a transition table; an interface contract as signatures with pre-
and postconditions; a data format as rules with an example), and Phase 1 writes
the files the table names instead of the fixed three. This is a template change
plus a convention; it needs no new tooling at 1.1.1. The catalog's advice that
choosing the kinds is itself a decision, made by the developer or defaulted to
the agent, is exactly the thing the table makes visible.

### 5.2 CONF rules per specification form

**If state machines are a supported form and the plan chooses one, can Spec Kit
set up the CONF rules (trace tests, transition coverage) for it automatically?**
Not in core; yes as a bundle keyed off the forms table, at the cost of
building the bundle.

A per-form bundle has five parts, and each has a Spec Kit home:

| Part | Home | Example for a state machine |
|---|---|---|
| the form's template | `.specify/templates/overrides/forms/state-machine.md` | a transition table with `ST-n` identifiers, each row `Method: test`, plus the diagram |
| its SQ checks | a checklist fragment merged into `checklists/requirements.md` | every state reachable; every event handled in every state or explicitly ignored; no two rows fire on one event |
| its test tasks | a tasks-template fragment | one trace test per transition; a negative test per ignored event; `Clauses: ST-1 ...` on each |
| its plugin configuration | the plugin's identifier families and a per-family coverage objective | family `ST`, objective "every transition cited by a passing trace test" reported as a second requirements-coverage line |
| its rule | a CONF rule in the constitution, added by amendment | CONF-5 of design option A4: transition coverage as a realization-coverage objective |

The trigger is the forms table of 5.1: when it names "state machine", the plan
skill (overridden) copies the form template, the tasks skill (overridden)
includes the fragment, and the plugin reads the family from configuration. At
1.1.1 this is three template overrides and a plugin option. As an extension it
would be an `after_plan` hook that reads the table and writes the fragments.
Either way the capability is built by the course, not found in Spec Kit; what
Spec Kit contributes is the place in the lifecycle (plan, then tasks) and the
review-plan gate at which the developer approves the choice.

### 5.3 RQ rules per kind of realization file

**Can Spec Kit set up RQ rules by realization file type, such as `ruff` for
Python and `clippy` for Rust?** It records the choice; it does not act on it.

Where the choice is recorded today: the plan's Technical Context names the
language and the test framework; the constitution can state a quality
principle; the tasks template's Setup phase has "Configure linting and
formatting tools" as a sample task. Nothing then runs the tools: implement's
final "validation" is the agent's reading, and the demo shipped without a
linter or coverage configured.

What would make it a capability, in increasing order of packaging:

1. **A rule and a task.** RQ-1 in the constitution names the command set per
   language (`ruff check`, `mypy`, `pytest --collect-only` for Python); the
   tasks override emits the Setup task and the gate task; `speckit-verify`
   runs the set. The language is read from Technical Context. This is enough
   for A0 to A5, which are Python only.
2. **A language-keyed table.** RQ-1 becomes a table (language, analyzer, type
   checker, collector, coverage tool, gate command) and `verify` picks the row
   for each file type present. One rule covers a polyglot repository.
3. **A preset per language** (upstream): `python-rq`, `rust-rq`, each carrying
   its RQ rows, its tasks fragment and its gate script, installed at
   `specify init`. Or an extension whose `after_implement` hook runs the set
   for every language the plan names.

The course's position (design 2.4) is that RQ deepens version by version
(`ruff`, then `mypy`, then the test-discipline review), which argues for 1 now
and 2 when a second language appears, which for the guard is the Rust sibling
mentioned in design section 1.

## 6. Vocabulary: where the words conflict and which wins

The principle for every row: **the glossary's word wins in course prose and in
the fields of every artifact; Spec Kit's word wins only as the name of the
command a student types or the file they open.** So a lecture says "the
development rules, which Spec Kit keeps in the file it calls the constitution,"
and a student still runs `/speckit-constitution`.

| Spec Kit says | The glossary says | The difference | Ruling |
|---|---|---|---|
| *spec*, `spec.md` | *specification*; *concept of operations*; *requirements* | Spec Kit's spec is one per-feature document bundling stories, scenarios, requirements, success criteria and entities. The glossary's specification is any S; the ConOps is system-level and governs the family | In prose: "the feature specification", which holds the ConOps clauses and the requirements for one feature. `spec.md` names the file only. From A2 a system ConOps sits above the feature files (section 8) |
| *constitution* | *development rules*; *governance* | project-level principles with semver and an amendment procedure, in prose without decider or evidence | "development rules" in prose; "the constitution" for the file; the rules inside it in the eight-field form |
| *clarify* | *elicitation* | a procedure: five questions at most, options with a recommended default, answers encoded into the spec | elicitation is the activity; clarify is the name of this procedure and A1 adopts it; "clarify-style elicitation" is acceptable in a lecture once |
| the `## Clarifications` section | *elicitation record* (reference) | the record lives inside the specification, so SQ audits it with the clauses | the record is reference: it moves to `reference/elicitation.md` with the stakeholder's words verbatim and who answered; if clarify is left unmodified, the section stays but is declared non-normative and the audit skips it |
| *analyze* | *audit* | a read-only cross-artifact report over spec, plan and tasks against the constitution, four severities; its "coverage" is requirement to task | audit is the activity; analyze is "the audit of the feature triad"; its Coverage Summary is a TR report (requirement to task), not requirements coverage |
| *checklist* | *specification-quality rules*; *gap list* | per-feature generated items a reviewer ticks; "unit tests for English" | the SQ rules are standing; a checklist is the per-feature instance, the gap-list form; `[x]` means the item is *established*, not that work is done |
| *GATE* (the plan's Constitution Check) | *gate*: algorithmic (an exit code) or approval (a recorded human decision) | the agent fills a PASS table; no exit code, no recorded decision | not a gate in the glossary's sense; call it the constitution review in the plan, a review (agent). Gates proper are `tools/gate.sh` and the recorded sign-off |
| *converge* | *verification*; *conformance* | an agent's assessment of the code against the triad that appends tasks; "completion claims are not evidence" | a review (agent) of conformance at rung 2; not CONF; its verdict is a finding, not evidence. The phrase about completion claims agrees with design 2.9 and may be quoted |
| *success criteria* (`SC-nnn`) | *requirement*; *clause* with a method | measurable, technology-agnostic outcomes, often not decidable by a unit test | each SC is a clause and carries a method (walkthrough, analysis or test); the `SC` family may be kept as an identifier prefix |
| *acceptance scenario* (Given/When/Then, unnumbered) | the story's *example*; a *scenario* (fixture) | no identifiers; the demo's plugin synthesizes `US1-2` | give each an identifier; the example line is the seed of the A1 fixture |
| *Independent Test* (per story) | *verification method* of a clause | prose per story | replaced by `Method:` |
| *research.md* | *reference* | | reference; not audited; no judgment is about it |
| *data-model.md*, *contracts/*, *quickstart.md* | glossary and data format; interface contract; walkthrough procedure or example session | | catalog names in prose; the file names are kept |
| *feature* | capability (F1 to F8); version | | "feature" only when naming Spec Kit's directory |
| implement's "validation" | *verification* | the agent checks the code against spec, plan and tests | that is verification; validation is the sign-off and only a person gives it |
| *manual* (plugin status) | *walkthrough* | | A0's plugin already prints "walkthrough: see reports/walkthrough.md" |
| *phases*, *Checkpoint* | *waves*, *gate at the end of a wave* | a Checkpoint has no decider and no record | course words in prose; a Checkpoint becomes a wave end when a decider and a record are named |
| `Status: Draft` | *established*; *stale* | a free header field | not an equivalent; the ledger row is |
| *evidence* | *evidence* | converge and the demo's constitution use it as the course does | no conflict |

## 7. Options for producing A0, then A1, through Spec Kit

All three options keep A0's system, clauses, rules and reports as they are;
they differ in how much of the production runs through Spec Kit's steps and in
what a student would copy into their own project.

### Option 1. Vanilla Spec Kit, the course artifacts beside it

Run the stock skills and templates. The constitution is written from the eight
rules as prose principles. Specify takes the purpose statement and the three
stories as its description and produces a stock `spec.md`: three stories with
Given/When/Then scenarios, FR-001 to FR-004, success criteria, key entities.
Clarify is skipped at A0. Plan produces the stock files; its Technical Context
is the technology form. Tasks are generated with tests explicitly requested.
Implement writes `guard/` and `tests/`. Beside this, by hand and outside the
workflow: the demo's plugin (FR and `US1-2` families), `pytest-cov`,
`tools/gate.sh`, a walkthrough record, a sign-off, a ledger and a dev log, and a
README that maps the two vocabularies.

A1: clarify over the stock spec, with the Clarifications section as the record;
checklist for the audit; analyze; fixtures and story tests by hand.

- Pros: students see Spec Kit as they will meet it; the smallest build; every
  gap of section 2 is visible as the hand work that fills it, which is itself a
  lecture.
- Cons: the clause form does not survive the stock template, so there is no
  `Method:` and no `Derived from:` on a clause and the method is implied by the
  identifier family (FR means test, a scenario means walkthrough); two
  vocabularies in one repository; the five rows live outside the workflow and
  the agent follows the course's rules only as far as the prose constitution
  carries them; A1's record is inside the spec.
- Cost: a day of hand assembly from A0's files; nothing to maintain.

### Option 2. Project-local template overrides and three skills (recommended)

The five overrides of 4.2, the three skills of 4.3 (`verify`, `signoff`,
`ledger`), A0's plugin (4.4) and `pytest-cov`, and a `.specify/extensions.yml`
with `verify` as a mandatory `after_implement` hook. No packaging. Clarify,
analyze, checklist and converge are used as shipped.

**A0 through the steps.**

| Step | Emits |
|---|---|
| constitution | the eight rules in the eight-field form, sections SQ, RQ, CONF, VAL, TR, WF, RPT; version 1.0.0; the Sync Impact Report deleted before commit |
| specify | `specs/001-filter/spec.md`: Purpose (the agreed statement); Scope and boundary with Terms; User categories (message sender, security officer); US-1 to US-3 with method and example; REQ-0 to REQ-3 with method and derivation; no success criteria in this version; `checklists/requirements.md` with the SQ items of 4.2, ticked by the person: this is A0's rung-1 SQ reading (design option A, A0), now with a form |
| clarify | not run: A0's specifications are given as agreed, as lecture 01 says |
| plan | Technical Context as the technology form (Python 3.12, `uv`, `pytest`, `pytest-cov`, `ruff`); Constitution Check as a table over SQ-1 to RPT-1; Specification forms table with four rows (concept of operations, behavioral requirements, test suite, technology and platform) and the two methods in use; Verification section naming the gate command and the two coverage objectives; Project Structure `guard/`, `tests/`, `tools/`, `reports/`; `research.md` empty of decisions (no `[NEEDS CLARIFICATION]` existed) and kept as reference; `data-model.md` reduced to the Message entity, which REQ-0 already fixes; `quickstart.md` as the walkthrough procedure (`tools/walk.py LEVEL PAYLOAD`) |
| tasks | T001 Setup (markers, coverage, `ruff`); T002 `guard/message.py` with tests, `Clauses: REQ-0`; T003 `guard/filter.py` with tests, `Clauses: REQ-1, REQ-2, REQ-3`; T004 walk US-1 to US-3 and record; T005 sign-off; T006 gate and ledger; a dev-log entry per task. Tests required |
| implement | the checklist gate passes on the ticked SQ checklist; the code and tests; the `after_implement` hook runs `verify`: `ruff check`, `pytest` with the plugin and coverage, exit codes and the coverage table into the dev log, `reports/conformance.md` written |
| walkthrough and signoff | the record (Clause, Role, Command, Observed, Finding; who and when) and the Sign-off section, by the person playing the two roles |
| ledger | the five rows with evidence, provenance and "goes stale when", at the commit |
| analyze, checklist, converge | not run at A0; analyze is the audit that arrives at A1; converge is available as a rung-2 agent walkthrough but A0 uses a person |
| commit | `tools/gate.sh` in a `pre-commit` hook, outside Spec Kit |

The result is A0's file set with two differences a reader would notice: the
rules live in `.specify/memory/constitution.md` rather than `process/rules.md`,
and the two specifications are one feature file rather than two files. Both
are placement, not content, and section 8 asks the user to rule on the second.

**A1 through the steps.**

| Step | Emits |
|---|---|
| clarify, as the elicitation procedure | the taxonomy scan over the ConOps half of the feature spec; at most five questions, one at a time, each with a recommended option, answered by the person playing the stakeholders (the glossary-discipline gaps, the meaning of "unchanged", the fourth level, the negative payload, who reads a drop); the answers applied to the ConOps sections; the Q→A record written to `reference/elicitation.md` by the `speckit-elicit` wrapper, or left in `## Clarifications` and declared non-normative (section 8) |
| specify, re-run on the revised description or edited in place | the Terms section promoted to a glossary with identifiers; requirements rewritten in EARS; six to eight gaps seeded on purpose |
| checklist | an SQ checklist with the audit items (consistency, EARS form, glossary discipline, story-to-requirement alignment, a method on every clause, a reason on every judgment clause); first ticked by a person who misses some gaps (T1 of design 2.9), then the agent's analyze over the same spec, which over-reports one; the seeded gaps are the known-violation set both must flag |
| analyze | the audit at rung 2; its report saved as the gap list; its Coverage Summary is the first TR matrix (requirement to task) |
| plan | the forms table gains "acceptance scenarios / fixtures" and "glossary"; the Verification section gains the fixture loader |
| tasks | fixture file derived from the story examples; a parametrized story test per fixture row, `Clauses: US-1 ...`; the trace-matrix script |
| implement, verify | the story tests run under the plugin; US rows now show tests *and* the walkthrough |
| walkthrough and signoff | a walkthrough per user category; the re-sign-off, because the ConOps changed and VAL went stale |
| ledger | regenerated; the rows that were stale after the specification change are re-established, and the ledger shows which verifier re-established each |

- Pros: everything flows through Spec Kit's steps, so a student learns one
  workflow; the clause form, the rule form and the vocabulary are set by files
  the student can read and copy; the verifier ladder is visible in place
  (checklist at rung 1, analyze at rung 2, the skills at rung 3, the plugin and
  `pytest-cov` at rung 4); the commit gate and the ledger are the same files A0
  has now.
- Cons: overrides are per project, so a student copies `.specify/templates/overrides/`
  and `.claude/skills/speckit-*` into each new repository (the role
  `.claude-template/` plays today); the overrides drift when upstream templates
  change; Spec Kit still has no commit gate, so the `pre-commit` hook is outside
  it; the per-feature layout has to be reconciled with a system ConOps at A2.
- Cost: five template overrides, three short skills (each a page), A0's plugin
  with one path change, a hooks file, a `pre-commit` hook. About the size of
  A0 itself.

### Option 3. Packaged: a preset and an extension

The overrides of Option 2 become a preset (`ase-course`: templates,
terminology); the skills, the plugin and the gate become an extension
(`speckit-conformance`: commands `verify`, `signoff`, `ledger`, `walkthrough`,
`forms`; hooks `after_implement: verify` and `before_implement` checking the
SQ checklist and the sign-off; a config file with the identifier families, the
coverage threshold, the language tool table of 5.3 and the forms table of 5.1);
a workflow overlay inserts shell gate steps and the ledger step into the bundled
workflow. Students install both with one command each.

- Pros: one install per student project; the per-form CONF set-up (5.2) and the
  per-language RQ set-up (5.3) become configuration rather than editing; the
  hooks give the gate a lifecycle slot without a git hook.
- Cons: the largest build and the only one that must track Spec Kit's extension
  and preset APIs, which are newer than the 1.1.1 baseline and documented
  upstream rather than exercised in the demo; packaging hides the mechanism
  from students, which works against lecture 01's point that a process that is
  a file can be both followed and audited; the forms and rules it would package
  are not stable before A2.
- Cost: Option 2 plus manifests, configuration, the overlay, tests of the
  extension against at least two Spec Kit versions, and documentation. Several
  times Option 2.

### Recommendation

**Option 2 now**, for A0 and A1: it produces the running example's artifacts
through Spec Kit's own steps with changes a student can read, and it keeps
clarify, checklist, analyze and converge as shipped, which is where Spec Kit
is strongest and where A1's elicitation and audit live. **Option 3 later**, as
packaging, once A2 has fixed the forms table and the rule set that the
configuration would carry; the Option 2 files are its contents. **Option 1 as a
contrast**, not a production route: one lecture segment runs stock Spec Kit on
the same system and shows, against the mapping table, which of the five rows
can be established from what it produced and which cannot.

## 8. Decisions left to the user

1. **Placement of the specifications.** For A0 and A1, one feature file
   `specs/001-filter/spec.md` holding the ConOps clauses and the requirements
   (recommended, because clarify, analyze, checklist and the demo's plugin all
   read one `spec.md`), or A0's two files kept and the skills overridden to
   read both. From A2, a system-level `specs/conops.md` above the feature
   directories (Spec Kit's numbering only looks at `NNN-` directories, so a
   plain file beside them is safe), with each feature's clauses deriving from
   it.
2. **Where clarify's record goes.** A thin `speckit-elicit` wrapper that runs
   clarify's protocol and writes `reference/elicitation.md` (recommended, since
   the glossary files the record under reference), or clarify unmodified with
   the `## Clarifications` section declared non-normative.
3. **Whether to track upstream Spec Kit beyond 1.1.1** for presets and overlays
   now, or stay on the demo's version until Option 3 is wanted.
4. **Whether the constitution replaces `process/rules.md`** in the Spec Kit
   route (recommended, so there is one rules file), or `process/rules.md` stays
   and the constitution cites it.
