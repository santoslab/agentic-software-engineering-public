# Re-layering the running example: definition, evaluation, reporting, control

**Status:** proposal, 2026-10-24, for the instructor's review before any
snapshot or lecture is changed. It amends
[running-example-design.md](running-example-design.md); section 7 lists the
amendments precisely. Worked examples of every new artifact are in
[relayering-examples/](relayering-examples/README.md).

## 1. Why

Lecture 01 and version A0 are a student's first exposure to the five
development-state judgments and to process rules, after nothing more than a
short instruction file. The rule template they meet fuses four concerns in
every rule: what the judgment says (*Statement*), who or what establishes it
(*Decided by*), how its status is shown (*Evidence*), and how it steers the
process (*When*, *On failure*). The judgments table in design section 2.1
does the same with its "established by", "evidence", and "goes stale when"
columns. Eight rules are thirty-two concerns.

A trial on 2026-10-24 (two fresh sessions in copies of v1, told only to
commit a specification change that passed the gate but contradicted the
concept of operations) showed where the difficulty actually lies. Both
sessions read the judgments and the specifications, assessed the change,
found the contradiction, reported, and stopped. Neither committed. What went
wrong in both was the control machinery: the audit skill could not be
started by the model, the gate was skipped because the instruction file said
to change nothing without approval, and the gate rule was followed by
neither. The definitions and the evaluations gave the agents no trouble; the
control layer did. The sessions produced, unprompted, the artifact this
proposal makes central: an assurance report.

## 2. Vocabulary

These definitions go into the design (section 2.1) and the root glossary.

- **Judgment.** A claim about the current development state. Five, unchanged:
  SQ, RQ, CONF, VAL, TR.
- **Definition** of a judgment. What the claim says, stated for each
  specification form it concerns and then for the whole. The definition is a
  predicate on the development state; it says nothing about who evaluates it
  or when it must hold.
- **Evaluation.** The activity that produces evidence for or against a
  claim: a run (test, analysis) or a human reading (review, walkthrough,
  sign-off). Each per-form clause names how it is evaluated. "Evaluated by"
  replaces "Decided by": the field names what produces the evidence, not an
  authority.
- **Evidence.** What an evaluation produced and a claim rests on: the results
  of a run, or a record of a human activity.
- **Record.** A document attesting that an activity was performed and what it
  decided: a sign-off record, a walkthrough record, a review record, an audit
  record (the gap list with its rulings), the development log. Records are
  evidence. They live in `records/`.
- **Report.** A presentation of the development and assurance state to the
  developers or to other stakeholders such as auditors. Reports live in
  `reports/`: the assurance report; the conformance report and the trace
  matrix, which an evaluation generates and the assurance report cites;
  later the ledger. A record is not a report, and the word "report" is no
  longer used for the output of a manual task.
- **Provenance.** For each piece of evidence: what produced it (the verifier
  and its version), against which state of which artifacts, over which scope.
  It is the information a reader uses to decide how far to trust the
  evidence.
- **Assurance report.** The document that states, for each judgment and each
  of its per-form clauses, whether it holds, on what evidence, with what
  provenance, compiled on request against a named state of the tree. In A0
  an agent compiles it; from A2 it is kept between requests as the ledger.

**The assurance-case remark for Lecture 01.** The assurance report is a very
simple assurance case. The judgment definitions are its claims, decomposed
once, per form. The evidence is the evidence: test results, records,
generated reports, with the evaluation method as the reason the evidence
bears on the claim (a passing suite bears on REQ-1 because a test cites
REQ-1 and the suite reaches the coverage objective). The provenance is the
information about how each piece of evidence was produced, which is what
governs trust in it. The report has no argument tree beyond that one
decomposition, and that is deliberate.

## 3. The four layers and when each enters

| Layer | What it answers | Artifacts | Enters |
|---|---|---|---|
| Definition | what each judgment claims, per form and aggregated | `process/judgments.md`: five definitions; per-form clauses with *Holds when* | A0 |
| Evaluation | how the truth of each clause is established, mechanically or by a person; later, by a fixed procedure | the *Evaluated by* and *Evidence* fields; the mechanical tools; from A1, `process/procedures.md` (the audit, elicitation) and the skills | A0; procedures A1 |
| Reporting | how the state is presented | `process/templates/assurance-report.md`; `reports/assurance-report.md` compiled on request; the generated conformance report and trace matrix | A0; the trace matrix A1 |
| Ledger | how the report is kept between requests without re-evaluating everything: dependence information, staleness, generation | `reports/ledger.md`; `tools/ledger.py`; the `Ledger-n` rules | A2 |
| Control | when the claims must hold: gates on commits and waves, approval gates, hooks, change control | `process/rules.md`: the `WF-n` rules; hooks or CI | A2 (gate, waves), A3 (change control) |

The ledger is listed as its own layer because it is the step between a
report and control, and because its motivation is best taught on its own:
nobody wants to re-run every evaluation and re-read every record on every
request, and a human sign-off cannot be re-run on demand at all. The ledger
is the report kept, with, per row, the artifact states its evidence was
produced against, so that a change marks the rows it touches as stale and
leaves the others standing. Traceability is what makes that bookkeeping
sound, which is the payoff of the TR row.

A0 therefore has **no process rules**. It has five definitions, eight
per-form clauses, one template, and an instruction file that tells the agent
its roles. Nothing in A0 says when a claim must hold. The report says whether
it holds now.

## 4. Identifiers and file layout

**Form-first identifiers.** Per-form clauses are named `Form-JUDGMENT-n`:
`ConOps-SQ-1`, `Reqs-CONF-1`, `Gloss-SQ-1`, `Scen-CONF-1`, `Code-RQ-1`.
The family of specifications, read together, is the form `Specs`:
`Specs-SQ-1` (the documents agree with one another), `Specs-TR-1`. The form
comes first because the catalog's per-form pages (section 5) list a form's
clauses together, and because the report, which is arranged by judgment,
collects across forms anyway. The mixed case is deliberate: a clause
identifier in a specification matches `[A-Z]+-\d+` (`REQ-1`, `US-3`), and a
judgment clause never does, so the clause reader cannot confuse them and a
reader sees at a glance which kind of identifier is in front of them. `Reqs`
rather than `Req` for the same reason.

**Definitions** carry the bare judgment name: SQ, RQ, CONF, VAL, TR.

**Procedures** (A1) are named by activity, `Audit` and `Elicit`, and
state the steps once, for any form. The per-form parts of an activity (the
audit items for a form, the elicitation taxonomy for a form) live in the
form's section of the judgments file, which is what the catalog page for the
form will carry (section 10, D; this replaces the earlier `Specs-Audit`,
`ConOps-Elicit` naming).

**Ledger rules** (A2) are `Ledger-n`; **control rules** (A2, A3) are `WF-n`.
Report forms are templates in `process/templates/`, not rules. The *form*
style of rule disappears from the early versions as a consequence.

**Fields.** A per-form clause has four: *Holds when*, *Evaluated by*,
*Evidence*, *In this project*. The first three depend only on the form and
read the same in any project that uses the form; the fourth binds the clause
to this project and may carry one instance (section 10, B; this replaces the
earlier *Example* field). A procedure has *Purpose*, *Serves*, *Run by*,
*Steps*, *Stops*, *Record*, *Example*. A control rule keeps the A1 template
(*Style*, *Maintains*, *When*, *Statement*, *Decided by*, *Evidence*, *On
failure*, *Example*), because control is where *When* and *On failure* belong.

**Layout per version.**

```
A0  CLAUDE.md
    process/judgments.md
    process/templates/assurance-report.md
    records/reviews.md  records/validation.md  records/dev-log.md
    reports/assurance-report.md  reports/conformance.md
A1  + process/procedures.md
    + process/templates/gap-list.md
    + records/audit-NN.md   reference/elicitation.md
    + reports/trace-matrix.md
A2  + process/rules.md  (Ledger-n, WF-n)
    + reports/ledger.md  tools/ledger.py  a pre-commit hook
```

## 5. The per-form end state, and the catalog as its index

The example already follows a per-form pattern without naming it: SQ-1 is
the generic definition, SQ-3 arrived with the EARS form, SQ-4 with the
glossary, and the audit checklist's split into within-document and
between-document items is the aggregation. The re-layering names it and
arranges the files by it. From A1 on, `process/judgments.md` has one section
per form, and every form a version introduces brings its section: its SQ
clauses, its CONF method, its VAL clause if it is stakeholder-facing, its
audit checklist items, and whether elicitation applies to it.

The end state the design should lead to: every form in the root catalog
`specification-kinds.md` has a page (or a section of the catalog) with the
suggested format or template, the SQ clauses for the form, the CONF method
and evidence, the VAL clause where one applies, the audit items, the
elicitation note, and an example from the running example. The catalog
becomes the index into those pages. The running example fills a page each
time a form enters; the course does not build a template engine around it.

Two pedagogical consequences. A student can take the A0 and A1 toolkit, the
definitions, the audit, the conformance evidence, without any control layer,
which is what a brownfield project needs: infer specifications for an
existing code base, write their SQ clauses and audit them, write their CONF
clauses and collect evidence. And the per-form pages are what a student
reaches for when their project uses a form the lectures did not cover.

## 6. The agent's roles, as the instruction file states them

The original question that led here was where the agent is told its
responsibilities. In the re-layered example the instruction file says so in
three roles, and nothing else does.

1. **Author.** When the agent writes or changes a specification, code, or a
   test, the result is held to the definitions in the judgments file. The
   file is what its work is checked against, and the instruction file says
   so and names the habits that follow (read the clause before writing to
   it; cite the requirement a test supports; derive a requirement from a
   story). From A1 the author role includes running an authoring procedure
   when asked, elicitation, under its stops.
2. **Assessor, on request.** When asked for the assurance report, the agent
   compiles it by the procedure in the judgments file: it runs every
   mechanical evaluation now and quotes the result; for every human
   evaluation it reads the record and reports who decided, when, against
   which state, and what; it states the tree state at the head. From A1 it
   also runs the audit when the developer starts it, and stops for rulings.
3. **Not a decider of human judgments.** It does not sign, does not walk a
   story on a stakeholder's behalf, does not record a review a person did
   not do, does not rule on an audit gap, and does not report a result it
   did not obtain in this session.

Enforcement does not exist until the control layer, and when it arrives it is
a hook, with the instruction file saying only when the report must be green.
The examples for A0, A1, and A2 show the file at each stage.

## 7. Amendments to running-example-design.md

Applied after the instructor reviews the examples.

1. **Section 2.1.** Split the judgments table into a definition table (ID,
   the claim as a predicate, the forms it concerns, the aggregation; CONF
   stated as a relation between a specification form and the realization)
   and an evaluation table (ID; the parts of the evaluation; the verifier
   kind of each part at the current version, a person, an agent, a skill, or
   a program, which is its rung; the evidence each part produces). See
   section 10, A and C. Move the "goes stale when" column to a new ledger subsection
   (item 3). Move the two-kinds-of-gate paragraph to the control subsection.
   Add the vocabulary of section 2 above and the assurance-case remark.
2. **New section 2.1a, "Four layers."** The table of section 3 above, with
   the sentence that A0 has no process rules.
3. **New section 2.4a, "The ledger as the report kept."** The motivation,
   the dependence information per row, the staleness rules, generation; the
   old "goes stale when" column becomes this section's table.
4. **Section 2.2.** Split the "Reports" row into "Records" (evidence of
   human activity, `records/`) and "Reports" (presentations, `reports/`).
   The "Development rules" row becomes "Judgment definitions" at A0,
   "procedures" from A1, "ledger and control rules" from A2.
5. **Section 2.3.** Retitle "Clauses and rules, filed by form." The
   identifier scheme of section 4 above. The budget: A0 five definitions and
   at most eight per-form clauses, no rules; A1 adds at most two procedures
   and four clauses; A2 at most eight rules.
6. **Section 2.4.** Add the row "the assurance report (compiled on request)
   → the ledger (kept, stale rows marked) → the generated ledger".
7. **Section 2.8.** The "in use from" column: obligation becomes the
   per-form clause (A0); procedure A1; gate, staleness, and policy A2; change
   control A3; form is a template, not a style. The rule template is kept
   for control rules only.
8. **Section 2.9.** Unchanged in substance. T4's "first seen" moves to A2
   with the ledger; a sentence says that at A0 the report's provenance and
   the closing sabotage carry T2.
9. **Section 3, Option A, rows A0 to A2.** Rewrite the last two columns to
   the layout of section 4 above.
10. **Section 4.** Add the per-form end state of section 5 above as the
    target the catalog leads to.
11. **Section 6.** The layout of section 4 above.
12. **Sections 8 and 9.** A status note; CF-12 and CF-15's "prescribed
    versus enforced" language belongs to the control layer and is unchanged;
    CF-14 unchanged.
13. **Root glossary.** Add *evaluation*, *evidence*, *record*, *report*,
    *assurance report*; amend *governance*, *ledger*, *assurance*.

## 8. Effect on what is built and drafted

- **A0.** `process/rules.md` becomes `process/judgments.md` and one
  template. `reports/ledger.md` becomes `reports/assurance-report.md`,
  compiled by the agent from a retained prompt. `reports/walkthrough.md`
  becomes `records/validation.md`; the dev log moves to `records/`. The
  gate script stays as the mechanical bundle the report procedure runs; the
  plugin and the tests are unchanged. The instruction file is the example.
- **Lecture 01.** Untouched except: "The ledger" becomes "The assurance
  report" (with the assurance-case remark and the ledger as a forward
  pointer); "Workflow controls: the gate" is removed and a paragraph in
  "What is not here yet" takes its place; "Breaking it" asks for the report
  instead of running the gate; "The development rules" becomes "The
  judgments file" with the four-field clause; "Process, reporting, and
  assurance tooling" and "Applying this to your own project" change
  vocabulary.
- **A1.** `process/judgments.md` gains the glossary and scenario forms and
  the amended clauses; `process/procedures.md` holds the audit and
  elicitation; no WF-1, RPT-1, RPT-2. The two skills take the form as their
  first argument and keep their per-form content in `forms/` files inside the
  skill directory (section 10, D); the trace tool, the tooling tests, and
  the scenario loader are unchanged; the audit skill
  keeps its developer-only switch, and the instruction file now says so
  instead of contradicting it. Catalog pages reword "decides" to
  "evaluates"; the gate page's goal becomes the mechanical bundle. The
  history patches are rebuilt.
- **Lecture 02 and its sidebars.** The passages on WF-2's commit trigger
  and on the gate change; the rest stands.
- **Lecture 03.** Not yet written; written to the new layering.

## 9. Open points for the instructor

1. The word *record* for sign-offs, walkthroughs, reviews, audits, and the
   dev log, and the directory `records/` beside `reports/`.
   [from John: I approve]
2. Form-first identifiers (`ConOps-SQ-1`) rather than judgment-first
   (`SQ-ConOps-1`). Section 4 gives the reason.
   [from John: I approve]
3. Whether the dev log stays in A0 as a plain record with no rule
   (recommended) or waits for A2.
   [from John: I approve]
4. Whether the assurance report in A0 is a procedure in the instruction
   file (recommended; skills enter at A1 with the ladder) or a skill.
   [from John: I approve]
5. Whether the gate rule enters at A2 with the build plan (recommended) or
   at the end of A1.
   [from John: I approve]
6. Whether the A1 audit keeps the developer-only switch (recommended, now
   that procedures are developer-started by design).
   [from John: I approve]
## 10. Questions of 2026-10-24 and their resolutions

The instructor approved points 1 to 6 of section 9 and raised five further
questions. The resolutions below are recommendations adopted into the
proposal; sections 4, 7, and 8 above were amended to match.

### A. CONF relates two artifacts and can be established by more than one means

- **The second relatum is fixed by the definition.** CONF says the
  realization does what the specifications say, so a CONF clause always
  relates one specification form to the realization. The identifier therefore
  names the specification form, `Reqs-CONF-1`, `Scen-CONF-1`, and the
  preamble of the judgments file says that every CONF clause is about the
  realization against the named form. Agreement between two specifications
  is not CONF; it is SQ (`Specs-SQ-1`) and TR, as the design already has it.
  Should a realization other than the code ever appear (F7's policy table
  realized as a configuration file), the identifier names both relata,
  `Policy-Config-CONF-1`. That case is not built ahead of need.
- **The definition table states the relation.** CONF: for each specification
  form in scope, the realization conforms to it, meaning every clause of the
  form has the evidence its method calls for and that evidence is passing.
- **More than one means, at two levels.** Per specification clause, the
  `Method` field says what evidence the clause demands: one method per clause
  at A0 and A1; from A2, when analysis enters as a second method, a clause may
  list several, and CONF then requires evidence for each. Per form, there is
  one CONF clause per method in use, so that every clause keeps one *Evaluated
  by* and one *Evidence*: `Reqs-CONF-1` is the test evidence; `Reqs-CONF-2`
  arrives when a requirement is first assigned *analysis* (A2's contracts, or
  a proof in a project that has one). The CONF row of the report aggregates
  over forms and methods.
- **Provenance names both states.** CONF evidence is produced against a state
  of the specifications and a state of the realization, and the report's
  provenance column says both. At A2 the ledger's staleness tracks both. This
  is where the relational character of CONF is visible to a reader.

### B. Form-level clauses, project bindings, and the example

- **The first three fields are form-level.** *Holds when*, *Evaluated by*,
  and *Evidence* depend on the form, not on the system, and read the same in
  any project that uses the form. They are written for "the system", never
  "the guard", and they name a project's parameters as the project's: the
  structural-coverage objective, the files that are the form's instances, the
  tools. These three fields are what the catalog page for the form will carry,
  and the identifiers travel with them: `Reqs-CONF-1` means the same thing in
  the running example and in a student's project, so the lectures can name a
  clause generically.
- **The fourth field is *In this project*.** It replaces *Example* and holds
  the binding: which files are the form's instances here, which tools and
  commands evaluate the clause, the values of the parameters; and, when one is
  short, one instance. The binding is required; the instance is optional, and
  when no instance is short the field points to the report or record that
  holds them. That meets the concern that a compact example cannot always be
  written.
- **The pathway for a student's project**, to be named in design section 4
  as what the per-form pages serve: choose the forms from the catalog; copy
  each form's clauses, which are the first three fields; write the *In this
  project* bindings; copy the templates and the instruction file's three
  roles, which are form-level too; build or adapt the tools from the tool
  catalog. The five definitions never change. A `starter/` directory holding
  the generic files is a later deliverable, not part of this build.
- **Worked example**, Reqs-CONF-1 in the new shape:

| Field | |
|---|---|
| Holds when | Every requirement whose method is *test* is cited by at least one test; every citing test passes; and the suite meets the project's structural-coverage objective over the realization. |
| Evaluated by | test: the project's test runner, with a plugin that computes requirements coverage from the citations and the outcomes, and a coverage tool for the structural part. A partial run (tests deselected) is labeled and is not evidence. |
| Evidence | the generated conformance report, `reports/conformance.md`, and the coverage table of the run |
| In this project | The requirements are the REQ clauses of `specs/requirements.md`; the realization is `guard/`; the objective is 100 percent branch coverage; the run is `uv run pytest` with the plugin in `tests/conftest.py` and `pytest-cov`. Instance: REQ-1 is cited by `test_filter.py::test_critical_is_dropped`. |

### C. Agents as evaluators, and the ladder

- ***Evaluated by* names the verifier kind**, using the grid of design
  section 2.6: review (human), review (agent), walkthrough (human),
  walkthrough (agent), analysis, test. For an agent it says whether the
  evaluation is ad hoc or by a named skill and version. That is the rung,
  stated per clause. The field may add the planned next rung, as Gloss-SQ-1
  does ("a person in audit 01, an agent in audit 02, the skill from audit 03;
  planned for A2: analysis by a script"), which makes the ladder visible
  clause by clause. Amendment 7.1 was reworded accordingly: the evaluation
  table's columns are the parts of the evaluation and the verifier kind of
  each part, not "mechanical and human parts".
- **An agent may be asked to review, walk, or audit.** The record it writes
  names it as the reviewer: model, date, prompt or skill version. Whether that
  record is evidence for a clause is decided by the clause's *Evaluated by*:
  if the clause says review (human), the agent's review is input to the
  person, not the evidence; when the clause climbs, the field changes to
  review (agent) and states the independence requirement, a human spot-check.
  The instruction file's third role is reworded so that it forbids signing and
  recording a person's review that did not happen, not an agent's own review.
  The record templates get a "Reviewer kind" field.
- **The report climbs too.** Compiling the assurance report is an evaluation
  activity: an agent by the written procedure at A0 (rung 2); a skill when it
  is repeated (rung 3); `tools/ledger.py` for the mechanical rows at A2
  (rung 4), with the human rows still read from records. Lecture 01's forward
  pointer to the ledger says so.

### D. Skills: one per activity, the form as the argument

Three arrangements were weighed.

| Arrangement | For | Against |
|---|---|---|
| (a) one skill per form and activity: `/elicit-conops`, `/audit-reqs` | each skill self-contained; a precise description; no argument to parse | the procedure is duplicated once per form and drifts; the number of skills grows as forms times activities; a student copies many files |
| (b) one skill per activity, the form as the first argument: `/elicit conops`, `/audit-spec reqs gloss` | the procedure is stated once; the per-form content is a file in the skill directory, `forms/conops.md`, which is the same content the catalog page carries; adding a form adds one file; one skill to port to another harness | the model resolves the argument, so the skill must say what it does with an unknown form; the description must trigger for every form; the skill directory grows |
| (c) a wrapper skill that starts a per-form skill | the appearance of both | both skills keep `disable-model-invocation: true` (section 9, point 6), so a wrapper running as the model cannot start a sub-skill; and skill-to-skill calls are not portable across harnesses |

**Recommendation: (b).** Concretely: `/elicit [form or path] [focus]`,
default `conops`; `/audit-spec [forms or paths]`, default every form under
`specs/`. Per-form content lives in `forms/` inside the skill directory, the
elicitation taxonomy per form and the within-document audit items per form,
with the between-document items in a file of their own that the audit loads
when its scope has more than one form. An unknown form stops the skill with
the list of known ones. The procedures in `process/procedures.md` are `Audit`
and `Elicit`, activity-level and system-independent; the per-form parts are
listed in each form's section of the judgments file, next to its clauses.
The names `/audit-spec` and `/elicit` stay: audits are of specifications, and
the code review that arrives at A2 is a different activity.

### E. Folder names

The rebuilt snapshots are `a0/` and `a1/`, matching the lectures and the
design. The replay tags become `a0`, `a1-specs`, `a1-scenarios`,
`a1-trace`, `a1`; the patches are regenerated under those names; the replay
script, its page, and the demo README change with them. The links to `v0/`
and `v1/` in Lecture 01, Lecture 02, the two sidebars, the Lecture 01
review, the design doc, the A1 plan, the catalog, and the two Spec Kit notes
are updated in the same pass. The new snapshots are built beside `v0/` and
`v1/`, and the old ones are removed in one commit once the lectures and the
replay have moved over; git history keeps them.
