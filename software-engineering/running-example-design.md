# Running Example for Agentic Software Engineering: Design

> Status: design draft, 2026-10-18; revised 2026-10-19 after the discussions
> of intent (intent has no artifact; the concept of operations opens with an
> agreed purpose statement) and of verification (conformance is an aggregate
> of tests passing and two coverages; each clause carries a verification
> method; a verification plan is a form, later in the progression; the
> verifier of a clause climbs from a human to an agent to a skill to a
> program; specification forms fall into a product and a process category,
> and process rules come in seven styles; scenarios and tests are one concept
> with two bindings; a ledger row is a claim, and the threats to a judgment are
> classified with their mitigations). Responds to the brief in
> `running-example.md`. The progression is decided (option A; section 8) and
> version A0 is built under
> `../module-ase-principles/demos/running-example-message-guard/v0/`; nothing
> else is built yet. Vocabulary follows `../glossary.md`; the additions and
> amendments this design proposed (section 5) were applied to the glossary on
> 2026-10-20.

> Review follow-up: updated 2026-10-21 with the agreed test-citation and
> ledger-evidence conventions and the version-specific handoff in section 9.
> Recording a decision is not evidence that its implementation is complete.
>
> A1 built 2026-10-22 under
> `../module-ase-principles/demos/running-example-message-guard/v1/`, from
> the plan `running-example-a1-plan-fable.md`; its four commits replay with
> `build-history.sh`. Section 9's A1 items carry their completion evidence
> below. A2 and later versions remain unbuilt. The rule-style handout the
> design proposed exists as `../process-rule-styles.md`.

**For the agent building a version:** read section 9's shared constraints and
the items applicable to that version before planning. Include applicable
**accepted** items in the implementation plan. In the completion report,
identify the evidence satisfying each item and list unresolved questions or
proposed deferrals. **Proposed** items are not authorization to expand the
version's scope; obtain approval before treating them as additional required
work. Use this document for current design decisions and the linked review
for rationale, not as a competing set of implementation instructions.

## 0. What this document settles

The brief asks for a running example that teaches agentic software
engineering as a discipline: human intent, specifications, realizations, the
judgments that connect them, and a development process whose state a person or
an auditor can read without reading the code. This document settles:

1. the example itself (section 1) and the pool of capabilities it can grow
   through (1.1);
2. the conceptual core every version carries, whatever the order of
   introduction: five development-state judgments, the artifact categories,
   rule categories with a budget, the mechanisms that deepen version by
   version, the shape of a verification method, the verification method of
   each clause, the verifier ladder from a human to an algorithm, and the
   styles of process rule (section 2);
3. four candidate progressions, each a sequence of versions with the
   capability, specification forms, judgments, and process artifacts each
   version introduces, with a comparison and a recommendation (section 3);
4. a canonical list of specification forms in two categories, product and
   process, with, for each, when it is appropriate, how conformance is
   shown, and what it must agree with (section 4);
5. the vocabulary changes needed in the glossary and the alignment with the
   Lean model in `AgenticDev` (section 5);
6. where the example lives and what existing code it reuses (section 6);
7. coverage checklists showing that every glossary term and every form appears
   in every progression (section 7);
8. implementation constraints and version-specific carry-forward items from
   review, distinguishing accepted decisions from proposals and open questions
   (section 9).

### 0.1 What the earlier attempts taught

The Lecture 03 game demo and the Project 0 knowledge base were the first
attempts at this material. Three things went wrong, and the design below is
shaped by each.

- **Too much at once.** The game demo's starter shipped 41 numbered rules in
  814 lines of process text (AUD 14, AUDCON 8, DEV 10, VER 4, RPT 5) before
  the first lecture on them, with 22 seeded gaps, and the rules carried
  examples from two different systems. Section 2.3 sets a budget of at most
  eight new rules per version.
- **Grouped by activity, not by what is judged.** The rules were filed as
  audit / develop / verify / report. Specification-quality rules sat in two
  files; conformance rules were spread over DEV-2, DEV-4, VER-1 to VER-4,
  RPT-2, RPT-4, and AUD-14; realization-quality rules barely existed. Section
  2.3 files every rule under the judgment it maintains, with the judgment's
  name in the rule identifier.
- **Fragile identifiers; no ledger.** Clauses were cited by section number
  (`§4.1`), which moves when a section moves, and the development state lived
  only in git history and per-file changelogs. The example uses per-item
  identifiers (`REQ-3`, `US-2`, `ARCH-1`) from the first version and a ledger
  that states, at a named commit, which judgments hold.

Two existing pieces are reused rather than rebuilt: the Spec Kit demo's pytest
plugin, which turns `@pytest.mark.req("FR-001")` markers into a generated
conformance report (one row per clause: tests, status in pass / FAIL / manual /
partial / no evidence), and its `test_architecture.py`, which enforces an
import-dependency rule with `ast`.

## 1. The example: a message guard

The brief proposes a library for message filtering and transformation, modeled
on the HAMR Simple Network Guard (SNG) example. **The proposal is endorsed.**
The example is a *message guard*: a toy cross-domain guard that sits between an
internal and an external network, drops messages that must not leave, and
sanitizes the ones that may. Python package `guard/`.

Why it fits better than the alternatives:

- **Data starts tiny and scales.** A message is two fields (a level in
  {Public, Restricted, Critical} and an integer payload). It can later become a
  JSON schema or an IDL with generated types and validators. No game example
  does that gracefully.
- **Behavior is local.** Drop, pass, clamp. Requirements are crisp, fit the
  EARS patterns, and are easy to seed with ambiguities ("sensitive messages",
  "large payload", "sanitize").
- **Stages compose.** Architecture constraints (stage order, purity, allocation
  of requirements to stages, an integration contract between stages) are real
  and checkable with a one-screen analysis.
- **Stateless until you choose otherwise.** Sessions (OPEN, DATA, CLOSE) can be
  added when a state machine and a sequence chart are wanted, not before.
- **The security framing explains the auditor.** A Critical message that leaks
  is a real failure, which is why a green ledger matters and why an auditor
  reads it.
- **It is the Python sibling of the HAMR example.** The same requirements and
  contracts can reappear in SysML, GUMBO, and Rust for students who continue.

Alternatives considered and set aside: tic-tac-toe again (already used; its
rules do not fit EARS or pipelines); a notes or to-do application (data format
is natural, protocol and architecture are not); a thermostat or vending machine
(a state machine from day one, which front-loads the hardest form).

### Naming, and the mapping to the HAMR example

Two names in the HAMR example collide with course vocabulary. Its drop/pass
component is `Gate`, and *gate* is the course's word for a condition a step
must pass. Its transform component is `Filter`, and in ordinary usage a filter
*drops*. The example therefore renames the stages so that each word means what
students expect.

| Message guard (this example) | HAMR SNG | Role |
|---|---|---|
| system: *message guard*, package `guard/` | Simple Network Guard | the system |
| stage `filter` | component `Gate` | pass or drop by level |
| stage `sanitize` | component `Filter` | clamp the payload of Restricted messages |
| REQ-1 | Req_C | Critical messages are dropped |
| REQ-2 | Req_R_1 | Restricted messages pass the filter unchanged |
| REQ-3 | Req_P | Public messages pass unchanged |
| REQ-4 | No_Input_No_Output | no input, no output |
| REQ-5a, 5b, 5c | Req_R_2 (a, b, c) | payload above 100 becomes 100; below 0 becomes 0; otherwise unchanged |
| ARCH-4 and the stages' integration contract | Gate `No_Critical_Output`, Filter `No_Critical_Input` | `sanitize` assumes no Critical message reaches it |

### 1.1 The pool of capabilities the progressions draw from

Every progression in section 3 grows the system through some of these
capabilities. Each one is listed with the specification forms it *forces* into
existence, which is what makes it useful as a teaching step. (Capabilities are
numbered F1 to F8; specification forms, in section 4, are cited by name and
never by number.)

| ID | Capability | What it forces into the specifications |
|---|---|---|
| F1 | `filter`: drop Critical; pass Restricted and Public unchanged; no input, no output | requirements; a test suite; a definition of *message* |
| F2 | `sanitize`: clamp Restricted payload to [0, 100], pass Public; pipeline = filter then sanitize | architecture (stages, order, purity); an integration contract (sanitize assumes no Critical input); allocation of requirements to stages; a plan, because the work is now several tasks |
| F3 | audit log: every drop and every change is written as a record | a second output and a second data format; the auditor's user story; a sequence chart with something to show |
| F4 | policy change: out-of-range Restricted payloads are dropped, not clamped (or a fourth level is added) | a change request and a change report; impact analysis; staleness in the ledger |
| F5 | sessions: OPEN, DATA*, CLOSE; DATA outside a session is dropped | a state machine; a sequence chart; trace tests with transition coverage; generation from the transition table; the first project-specific verification plan |
| F6 | standard message format: messages arrive as JSON (or in an IDL) and are validated at ingress | a schema or IDL; generated types and a validator; well-formedness of the schema itself |
| F7 | configurable policy: which levels are dropped is a table the security officer edits | a policy table as a data specification; a table-driven `filter`; configuration validation |
| F8 | parallel stages with a merge: two independent checks on the same message | a non-linear architecture; ordering and merge semantics |

F1 and F2 are the HAMR system. F3 to F8 are extensions; each progression says
which it uses.

## 2. The conceptual core carried by every version

### 2.1 Five development-state judgments

A *development-state judgment* is a claim about the current development state
whose supporting evidence and status are tracked at recorded checkpoints.
An established judgment is a supported, fallible claim, not proof that the
claim is true. These five are the rows of the ledger in
every version. Four are the Lean model's judgments (`specOK`, `realOK`,
`verified`, `validated`) under course names; the fifth is the brief's
"overarching" traceability, given its own row because it is mechanically
checkable and because the other four are only decidable *per clause* when it
holds.

| ID | Judgment | Question it answers | Established by | Evidence recorded in the ledger | Goes stale when |
|---|---|---|---|---|---|
| **SQ** | Specification quality | Is each specification well-formed, unambiguous, internally consistent, complete for its level, and consistent with its companion specifications? Does every clause carry a verification method, and does every judgment clause say why it is not mechanical? | an audit: an agent applies the SQ rules and a person rules on each gap; later, scripts for the syntactic parts (identifiers unique, EARS pattern, glossary terms, a method on every clause) | the audit report with zero open gaps; script exit codes | any specification changes |
| **RQ** | Realization quality | Does the realization lint and type-check, does its test suite collect cleanly and follow the test discipline (a test can fail; a citing test's assertions adequately check its clause; direct assignment for setup only), and is its structure judged appropriate? | analysis: `ruff`, `mypy`, `pytest --collect-only`; a review for the test discipline and the structure | the commands and their exit codes; the review record | code or tests change |
| **CONF** | Conformance (verified) | Does the realization satisfy the specification clauses in scope? The standing evidence obligations are: the required suite passes; each clause has the evidence its assigned method demands; structural coverage meets the stated objective; judgment clauses have the required review or walkthrough records. These support a scoped claim, not a proof of conformance | tests and analyses that cite clauses; the two coverage objectives; reviews and walkthroughs for judgment clauses; later contracts, trace tests with transition coverage, schema validation | the test run; the generated conformance report (requirements coverage); the coverage report (structural coverage); the review and walkthrough records | relevant specifications, code, tests, or verification tools/configuration/environment change |
| **VAL** | Validated | Do the specifications describe what the stakeholders have in mind? | a person walks the user stories and their example messages against the running system and signs off | a sign-off line: who, when, which specification version | a stakeholder declares a change of mind, or the concept of operations or a specification changes |
| **TR** | Traceable | Do identified clauses have unique identifiers, and do the declared links resolve (story to requirement to test to task)? Links can be followed in either direction; not every test must have a clause link | identifier/reference checks, automated where supported and otherwise reviewed | the trace matrix and reference-check findings, with no dangling declared links | relevant linked artifacts or reference-checking machinery change |

Intent has no row and no artifact. It lives in the stakeholders' minds and is
consulted only through a person (*intent* in `../glossary.md`), which is why VAL is the one row
of the ledger that no tool can regenerate, and why it can go stale on a
*declaration* (a change of mind, recorded as a change request) when no file
has changed.

A passing test suite records that its assertions passed on the executed
cases. The CONF row adds evidence obligations, not a guarantee of correctness:
requirements coverage accounts for clauses, while structural coverage
accounts for the code exercised at the chosen coverage level. Section 2.5
generalizes these obligations to other verification methods.

**Test citations are optional; clause coverage is not.** Every clause assigned
verification by test must be cited by at least one test, and every test citing
that clause must pass for its test evidence to be accepted. Every supplied
citation must resolve to a defined clause identifier. Tests may omit citations
and still remain subject to the gate's test-execution policy. A citation
declares intended support; review of the assertions is needed to assess
whether the test actually supports the clause. Uncited tests may contribute
to structural coverage. Neither a valid citation nor branch coverage proves
test adequacy (CF-01 and CF-02 in section 9).

**Ledger status concerns current support.** Established means the required
checks and reviews succeeded and their evidence was recorded. Stale means a
relevant change makes earlier evidence insufficient for the current state;
it does not mean that a defect has been found. Not established can mean that
checking is incomplete or that a current check found a problem; the finding
must distinguish these cases. A failed check calls for investigation of the
specification, realization, verifier, and environment. Changes can affect
multiple judgments, and successful reruns can renew some evidence while
other obligations remain unmet. Detailed maintenance belongs with A2's
generated ledger, not Lecture 1 (CF-03 and CF-09).

Every entry in the evidence column carries its **provenance**: which verifier
and which version of it, which version of each artifact it examined, and which
clauses it decided. These are the three scope lines that Lecture 01's RPT-2
puts at the head of a conformance report, moved onto the ledger row. They are
there because a row is a claim made by a verifier, and a claim can be wrong in
the ways section 2.9 classifies; the provenance is what makes the claim
checkable, and what makes it possible to say which rows to distrust when a
verifier turns out to be wrong.

Two kinds of *gate* follow from the "established by" column and both need a
name. An **algorithmic gate** is a program whose exit code decides (RQ's
analyses, CONF's mechanical conjuncts, TR, and the syntactic part of SQ). An
**approval gate** is a recorded human decision (VAL, the judgment part of SQ,
the reviews and walkthroughs in CONF, the sign-off that closes a wave). This
widens the glossary's earlier rule that a person cannot be a gate; the Lean
model's `establish` step with a human proof premise is exactly an approval
gate.

### 2.2 Artifact categories

The essay's draft section "Different Categories of Artifacts" lists seeds and
sketches, plans, specifications, development rules, reporting, and development
state. The example instantiates each from its first version, except that
reference material enters only with the version that teaches elicitation.

| Category | Instance in the example | Role in the judgments |
|---|---|---|
| Specifications | `specs/*.md`, every clause with an identifier and a verification method; the concept of operations opens with the agreed purpose statement | the subject of SQ; the reference for CONF and VAL |
| Realization | `guard/*.py`, `tests/*.py` | the subject of RQ; checked by CONF |
| Development rules (governance) | `process/rules.md`, split by category as it grows | say how each judgment is established and when it must hold; the CONF rules are the standing verification plan |
| Plan | `plans/NNN-*.md`; later `plans/verification-plan.md` | a build plan: tasks grouped into waves, a gate at the end of each wave, each task citing the clauses it realizes; a verification plan: the project-specific verification choices (section 4) |
| Reports | `reports/dev-log.md`, `reports/ledger.md`, `reports/trace-matrix.md`, `reports/conformance.md`, the coverage report, gap lists, change reports | the development state as a person reads it |
| Reference | `reference/elicitation.md`: the stakeholders' verbatim words, questions and answers; sketches | informs the specifications; is not a specification; not audited; no judgment is about it; kept from the elicitation version on |

Intent is not in the table because it is not an artifact. The purpose
statement at the head of the concept of operations is the closest written
thing to it, and it is a specification: an engineering artifact, revised with
the stakeholders until agreed, and audited like the rest of the document.

### 2.3 Rules filed by judgment, with a budget

Rule identifiers carry the category, so the categories are visible from the
first rule: **SQ-**, **RQ-**, **CONF-**, **VAL-**, **TR-**, and two categories
for the process itself, **WF-** (workflow: steps, commits, waves, gates,
staleness) and **RPT-** (the forms reports take). Identifiers are never
renumbered. Every rule is also typed by one of the seven styles of 2.8, and a
version introduces at most two new styles. Every example inside a rule comes
from this system. The CONF rules
state the standing verification objectives, the same for every project: what
counts as requirements coverage, the structural-coverage level, and how a
judgment clause is covered; a project-specific verification plan adds to them
only when a project makes choices beyond them.

The budget: no version adds more than **eight rules**. The first version ships
at most eight, one per category, in a single file of about eighty lines. After
the core versions the set is about 30 rules in at most five short files,
against 41 rules in 814 lines at the game demo's starting tag.

### 2.4 Mechanisms that deepen across versions

The five judgments do not change; the mechanisms that establish them get
stronger.

| Judgment | First form | Later forms |
|---|---|---|
| SQ | a person reads the clauses | audit rules and a gap list; scripts for EARS form, glossary use, and a method on every clause; the rule that a judgment clause states why it is not mechanical; per-kind checks for architecture, data formats, state machines |
| RQ | `ruff`; the suite collects | add `mypy`; add the test-discipline review; add a structure review |
| CONF | tests pass; `@pytest.mark.req` markers and the generated conformance report as requirements coverage; branch coverage from `pytest-cov` as structural coverage; stories walked | story tests over a fixture file; analysis as a second method (the import rule for the architecture clauses, the type checker for the signature part of the contracts); reviews for judgment clauses (the allocation table); trace tests with transition coverage for a state machine; schema validation at ingress; the verification plan for project-specific objectives |
| VAL | one sign-off on the concept of operations | a walkthrough per user category; re-sign-off after a revision or a declared change of mind; a walkthrough per change |
| TR | markers resolve to clause identifiers | `tools/trace.py` builds the matrix story to requirement to test to task; impact analysis reads the matrix |
| the ledger | a hand-written table at a named commit | `tools/ledger.py` generates it from exit codes, the reports, and a sign-off file; stale rows are kept and marked |

### 2.5 The shape of a verification method

Whatever the method, the verification process accounts for four parts:
a **verifier**; a **specification-coverage objective**
(did we check every clause the method is responsible for); a
**realization-coverage objective** (did we exercise every part of the
realization the method is responsible for); and **evidence** of each. Meeting
these obligations supports the scoped claim; it does not by itself establish
that the verifier is sound or that its assertions adequately express the
specification.

| Method | Verifier | Specification coverage | Realization coverage | Evidence |
|---|---|---|---|---|
| requirements-based testing | the test suite | every clause assigned method test has citing tests (citation-based requirements coverage); assertion adequacy is reviewed separately | branch coverage to the stated level (structural coverage) | the test run; the conformance report; the coverage report |
| trace tests on a state machine | the trace suite | every transition exercised (transition coverage) | branch coverage of the session module | the trace run; the transition report |
| import analysis for an architecture | the import rule | every constraint checked | every module examined | the analysis run |
| walkthrough of a concept of operations | a person | every story walked | every user-visible operation exercised | the behavioral walkthrough record; separate stakeholder sign-off for validation |

Requirements coverage is a coverage metric over the specification, as branch
coverage is one over the code. Passing tests and satisfying both coverage
objectives fulfill prescribed evidence obligations, not a proof of all
required behavior. The standing CONF rules state the objectives for every
version; a project-specific verification plan (section 4) states them when a
project's choices go beyond the standing rules.

### 2.6 The verification method of each clause

Every clause of every specification carries a **verification method**, one of
four values. The four come from crossing who decides with what is examined.
Who decides is Lecture 01's three kinds of verifier: a human, an agent, or an
algorithm. What is examined is the artifact as text, or the realization while
it runs.

| Verifier (Lecture 01) | examines the artifact (static) | executes the realization (dynamic) |
|---|---|---|
| **a human decides** | **review** (human): a person reads the artifact against the clause and records a finding | **walkthrough** (human): a person exercises the realization along a scenario and judges what they observe |
| **an agent decides** | **review** (agent): an agent reads both and reports, citing clause identifiers | **walkthrough** (agent): an agent drives the realization and reports, as the call transcript of Lecture 06 is read against a scenario |
| **an algorithm decides** | **analysis**: a type checker, a linter, the import rule, a schema validator, a Logika or Verus proof | **test**: unit, golden-string, scripted-input, fixture-driven, property-based |

The method value says what is done; the verifier kind says who does it. For a
mechanical clause the verifier is always algorithmic, so the method value
suffices. A judgment clause records both, `review (agent)` or `walkthrough
(human)`, because the two differ in cost, repeatability, and the evidence the
ledger holds (an agent's report against a signed line), which is Lecture 01's
comparison table of the three verifiers.

This refines, and does not replace, Lecture 01's distinction between
**mechanical** and **judgment** clauses. That distinction is the first axis,
and it remains the primary one because it carries the consequence that
matters: a mechanical clause can sit behind a gate, a judgment clause cannot,
and a judgment clause is named as remaining, never silently assumed covered. A
clause is mechanical exactly when its method is *test* or *analysis*, and a
judgment clause exactly when its method is *review* or *walkthrough*.
"Testable" means precisely that the method is *test*; an architecture clause
decided by the import analysis is mechanical but not tested.

What changes against Lecture 01 is where the classification lives and how fine
it is. The game demo's VER-2 keeps it in a table in the process document, by
clause group, amended by hand; here it sits beside each clause in the
specification, where a tool reads it and it cannot drift from the clause it
classifies. Three rules follow: every clause carries a method (SQ); a judgment
clause states why it cannot be made mechanical (SQ), which pushes the
specification toward mechanical clauses; and each clause is covered by the
method it names (CONF).

The four values appear gradually. The first version with requirements needs
only two: every requirement is *test* and every user story is *walkthrough*,
and students meet the mechanical/judgment split through those two. *Analysis*
arrives with the type checker and the architecture rule; *review* with the
first artifact that is read rather than run, the allocation table. Finer
distinctions (unit against golden-string against property-based) are
techniques within a method and belong in the verification plan.

The values line up with the industry vocabularies: DO-178C's reviews,
analyses, and tests are review, analysis, and test; the MIL-STD and INCOSE set
test, analysis, inspection, demonstration is test, analysis, review,
walkthrough. The standards cut by *how*; the course adds the *who* axis
because gate-ability is what agentic development runs on.

### 2.7 The verifier ladder: from a human to an algorithm

For one clause, the verifier can climb. The idea, stated in Lecture 01 and
carried through the example, is that verification often starts with a person;
when the person finds themself doing the same check repeatedly, they ask an
agent; when the agent does it repeatedly, the procedure becomes a skill; and
when the procedure turns out to be deterministic, the agent writes a program.

| Rung | Verifier | What the ledger records | What changes |
|---|---|---|---|
| 1 | a human reviews or walks through | a sign-off | one-off; a judgment |
| 2 | an agent is asked to check and report | an agent report citing clause identifiers | repeated work delegated; costs tokens; two runs can differ |
| 3 | the agent's procedure is packaged as a skill | the skill's report, under the skill's version | the procedure is an artifact: versioned, auditable, the same steps every run even where the findings differ |
| 4 | the procedure is decidable, so the agent writes a program | an exit code | the method flips from review to analysis, or walkthrough to test; the clause is now mechanical and can sit behind a gate; "who verifies the verifier" now applies to the program |

Four things follow.

- **Mechanical or judgment is discovered, not declared.** The ladder is how a
  team finds out which a clause is: write the skill's checklist, and if every
  step is decidable, write the program. The SQ rule that a judgment clause
  states why it cannot be made mechanical is the standing pressure up the
  ladder, and the reason it records is "we tried; this step needs a reader."
  Some clauses have a ceiling at rung 3 ("the purpose statement is
  implementation-independent"); the verification plan records the ceiling and
  the independence requirement (a person spot-checks the agent's report) per
  clause group.
- **A skill is rung 3.** Skills enter the example when a clause first reaches
  that rung, which is the first repeated agent verification: the `/audit-spec`
  skill in the version that introduces the audit. The skills lecture earlier
  in the course and the example tell the same story.
- **Validation does not climb.** A story walked by a person becomes fixture
  tests one version later; what climbed is the verification of the behavior
  the story describes. The validation question, whether it is the right
  story, stays with a person at rung 1, and the sign-off is retained after the
  tests exist. This is the place to say so, because it is where students will
  otherwise conclude that validation can be automated too.
- **Climbing exchanges threats.** Each rung removes one way the verifier can
  be wrong and introduces another (2.9): rung 1 to 2 trades attention and
  capacity for memory and non-determinism; rung 3 fixes the procedure but not
  the findings; rung 4 removes non-determinism and introduces silent
  mis-implementation and scope. The mitigation changes with the rung, which is
  why the verification plan records the rung per clause group.

Lecture 01 climbs the whole ladder in one demonstration when the agent writes
`check_notes.py`. The example spreads the deep dive out: two clauses climb in
plain view, the glossary-discipline check (a human audit, then an agent audit
and the skill, then a script, so review becomes analysis) and the story
walkthrough (a person, then fixture tests, with the sign-off kept), and one
clause is named that stops at rung 3. The verification plan, when it arrives,
records the rung and the independence requirement for every clause group.

### 2.8 Styles of process rule

A process rule is a requirement on the development process, and the toolkit
for product clauses applies to it unchanged: an identifier, an EARS-shaped
statement, a verification method, evidence, coverage. Students struggle to
write verification rules for three reasons that are visible in the game
demo's files. Rules of different kinds sit in one numbered list, unlabeled:
VER-1 is a definition, VER-2 a classification, VER-3 a staleness rule, VER-4 a
gate, VER-5 a threshold, VER-6 an obligation, VER-7 a prohibition, VER-8 a
reporting obligation. There is no template, so a student cannot see when a
rule is complete. And most student rules name no decider, no evidence, and no
failure behavior, which makes them wishes. The seven styles below, the
template, and the principles answer each of the three.

| Constrains | Style | Shape | Example in the guard | Game demo rules of this style |
|---|---|---|---|---|
| an artifact at rest | **obligation** | every X MUST have property P | every test cites a clause; every clause carries a method | AUD-1 to AUD-5, AUD-8 to AUD-14, AUDCON-1 to AUDCON-8, VER-6, VER-8, DEV-5 |
| a transition | **gate** | WHEN step S would complete, condition C MUST hold, decided by D | before a commit the aggregate CONF check passes; before a wave closes a person signs | VER-4, DEV-7, DEV-8 |
| a transition | **staleness** | WHEN artifact X changes, judgments J become stale and MUST be re-established before gate G | a specification change invalidates CONF, VAL, SQ, TR; a declared change of mind invalidates VAL | VER-3 |
| an activity | **procedure** | to do activity A: steps 1 to n; stop at k and report | the audit: search within a document, between documents, and by execution; then stop and list the gaps | AUD-6, AUD-7, DEV-1, DEV-6, DEV-9, DEV-10 |
| an activity | **policy** | parameter V of activity A is set to value X; exceptions are granted by R | branch coverage 100 percent, one pragma, exceptions by amendment | VER-5 |
| a record | **form** | record R has fields F, is produced by whom and when, and is read by whom | the gap list; the conformance report; a ledger row | RPT-1, RPT-2, RPT-4, RPT-5 |
| authority | **change control** | artifact X may be changed only by whom, with record R and approval A | fixtures are never edited to pass; a rule changes only by amendment | DEV-2, DEV-3, DEV-4, VER-7, RPT-3 |

Definitions are deliberately not a style: VER-1 (the three verifiers) and the
VER-2 table belong in the glossary and on the clauses, never in a rule list.
Re-sorting the game demo's 45 rules into the table is itself evidence that
seven styles suffice, and it shows how freely the old files mixed them.

Most styles exist because of a threat to a judgment (2.9): staleness answers
stale evidence, policy and form answer a scope narrower than the claim, change
control answers the shared mistake between author and verifier, and procedure
answers the limits of a reader. The threat table names the style of each
mitigation, which gives a student a second way to find the rule they need.

**Recording work, reporting judgments, and accepting work.**

A commit can record an intermediate development state; it need not mean that
the work is ready for acceptance. There is a useful distinction here:

- **Recording work:** an intermediate state may have unmet obligations.
- **Reporting judgments:** the ledger must accurately describe what is
  established, stale, or not established.
- **Accepting work:** the judgments designated by the checkpoint policy must
  be established with applicable evidence.

Relaxing the first does not weaken the other two. Permission to commit
failing tests does not make CONF established; it means that establishing CONF
is not a condition for that particular commit. Similarly, stale evidence
must not be presented as current merely because the process permits work to
continue.

When checks run and when their results block advancement are separate
decisions. Checks may run after every commit to provide feedback, while their
results become acceptance conditions at selected checkpoints. Each checkpoint
identifies the work being accepted, the required judgments and their scope,
the evidence needed, and who or what decides whether work may proceed. These
conditions are declared before the work begins, not improvised after a check
fails. Rules distinguish obligations that apply throughout development from
conditions required only at designated checkpoints; their *When* fields make
that distinction explicit.

A0 and A1 use a simple policy: the automated gate must pass before every
commit. A2 introduces intermediate commits within a planned wave, followed
by an acceptance gate requiring the judgments designated for that wave.
A scoped acceptance must not be reported as conformance of the entire
product. A3 develops the more general workflow model. CF-15 records the A2
implementation and teaching obligations.

**A0 teaching limitation.** Taken literally, CONF-1 and WF-1 require the
implementation, passing tests, and checking infrastructure before the first
commit. A specifications-only first commit is not permitted. Lecture 1
acknowledges this as a reason to examine and "debug" process rules, rather
than introducing an initial-construction phase or a baseline-acceptance
protocol in A0. Its log records tasks leading to a completed snapshot, not
one commit per task. Keep this limitation explicit until A2 addresses it
under CF-15. Also distinguish the automated gate's checks from the full set
of applicable obligations: a passing script does not discharge SQ review,
human trace review, or reporting duties.

**The rule template.** Every rule carries the same fields, so a reader can see
when one is complete. This example uses the simple per-commit policy; A2's
rules name the applicable checkpoints instead:

```
ID          CONF-2
Style       obligation
Maintains   CONF
When        at every commit; applies to every mechanical clause
Statement   Every mechanical clause MUST be cited by at least one test
            or analysis of the method the clause names.
Decided by  analysis: tools/trace.py; a "no evidence" row fails it
Evidence    reports/conformance.md
On failure  the gate is red and the work is returned; a test is added,
            or the clause's method is changed by amendment
Example     REQ-3 is cited by test_public_passes_unchanged
```

*Decided by* is the verification method of 2.6 applied to the rule itself, so
a rule is mechanical or judgment like any clause, and the ladder of 2.7
applies to rules: a rule often starts as a habit, becomes a checklist, then a
skill, then a hook.

**Principles for writing rules.**

1. Every rule names the judgment it maintains; a rule that maintains none is
   deleted.
2. Every rule names its decider and its evidence. A rule you cannot check is
   a wish.
3. Separate the rule from the number: thresholds are policy rules, later the
   verification plan; gates cite them.
4. Rules do not define terms.
5. State the trigger and the scope.
6. Say what failure does. Never silent.
7. Rules are earned: start with one gate and the ledger; add a rule the
   second time a check is done by hand, which is when a procedure is written
   and a skill is near.
8. One example per rule, from this system.

**The design grid.** A grid with the five judgments as rows and the seven
styles as columns. A process is designed by filling cells, and most cells stay
empty at first. The CONF row of the grid, made project-specific, is the
verification plan, which is the cleanest statement of what a verification
plan contains.

**Pace.** Styles enter two at a time: obligation and gate with the first
version (the ledger is a provided file, not yet a form rule); procedure and
form with the audit, where the procedure becomes the skill; policy and
staleness with the plan and its wave-end approval gate; change control with
the change request; the verification plan as the bundle of a project's
policies and procedures. Section 3.2 counts styles per version beside rules.

**Material to ship with the example.** A standing handout beside
`../specification-kinds.md`, proposed as `process-rule-styles.md`, with the
table, the template, the principles, the grid, the threat table of 2.9, and
one worked example per style from the guard; and a `process/rules.md`
template whose header carries the fields above.

### 2.9 Threats to a judgment

A ledger row is a claim with evidence, not a truth. The evidence is produced
by a verifier, against a reference, within a scope, at a version, and each of
those four is a place where the claim can come apart from the fact. A
**threat to a judgment** is a way the evidence can be present while the
judgment does not hold; a **mitigation** is the rule, procedure, or report
field that closes it. Lecture 01 lists six ways a verification result can be
invalid; they sort into five classes, and each class has a "green ledger,
wrong system" demonstration in the guard.

| ID | Threat | Lecture 01 item | Guard demonstration: the ledger is green and the system is wrong | Mitigation | Style of the mitigating rule | First seen (option A) |
|---|---|---|---|---|---|---|
| T1 | the reference is defective: the specification is ambiguous or inconsistent, or the intent behind it is unclear or beyond what one person can hold in mind | a defective S | "sensitive messages are dropped" with "sensitive" undefined; the test encodes one reading, the stakeholder meant another; every test passes | SQ before CONF; specifications exist to write down what a person cannot hold; more than one reader; an agent pre-reads for inconsistencies and a person rules on each | gate; procedure | A0 as a remark; A1 as the audit |
| T2 | the verifier is wrong: a program mis-implements a clause, a reader misreads one, or attention lapses | the verifier mis-implements a clause; attention | the import analysis reads `import x` and misses `from guard.sanitize import clamp`; the architecture row stays green | a known-violation set the verifier must fail on; a review of the program against its clauses; a second verifier for comparison | obligation; procedure | A1 the seeded gaps; A2 the script |
| T3 | the scope is narrower than the claim: clauses not decided, code not exercised, and the pass read as total | clauses not decided | a clause whose status in the conformance report is "manual" with no walkthrough recorded, and the CONF row read as green | the two coverages; the "clauses not checked" line of the report; CONF's fourth conjunct | policy; form | A0 |
| T4 | the evidence is stale or was never produced: run at an older commit or against an older specification, or reported from a narrative rather than a run | wrong version of S; checking from memory | the completion note says "all tests pass" and the log shows no run; the suite written for the old requirement still passes after the change | staleness rules; the ledger generated from exit codes at the named commit; provenance on every row; the gate run by a hook, never read from a note | staleness; form | A2 the generated ledger; A3 the change |
| T5 | a shared mistake: the author of the realization is also its verifier, so one misreading sits in both the code and the tests | not in the list | the agent reads "clamp" as "drop when out of range" in both `sanitize` and its tests; the person-authored fixtures from the stories disagree | independence: a different verifier, or a human spot-check; fixtures governed on the specification side (4A) | change control; policy | A1 the fixtures; A4 the plan |

The intent threat in T1 deserves its own sentence. Intent is the reference
for VAL, so a person who is mistaken about their own intent is the VAL
verifier being wrong, and no evidence can show it. The course answers it by
process: the purpose statement is agreed by several stakeholders, elicitation
is a procedure, and the declared change of mind in the change version is the
demonstration.

**The three kinds of verifier, with their threats.** Lecture 01 compares the
three verifiers by cost, repeatability, what they decide, and whether they can
stand in a gate. The threats characteristic of each, and the mitigation that
fits, complete the comparison.

| | Human | Agent | Algorithm |
|---|---|---|---|
| Strength | decides judgment clauses; the only verifier for VAL | cheap; decides judgment clauses; exhausts a large specification better than a person can | deterministic, immediate, composable into a gate |
| Weakness | slow; the result varies with attention | costs tokens; two runs differ | decides only what it was written to decide |
| Characteristic threats | inattention; limited capacity, so inconsistencies in a large specification go unseen; the intent itself unclear; bias toward one's own work | judging from memory instead of the current file; a plausible report with no run behind it; over-reporting; the same agent wrote the code it verifies | silent mis-implementation of a clause; built for one version of the specification; drift in the environment and tool versions |
| Fitting mitigations | write it down; several readers of differing experience; an agent's pre-read; a checklist, which becomes a skill | read before checking; cite identifiers and quote text; evidence is a tool output, never a sentence; a person spot-checks; independence from the author | a known-violation set; a review against the clauses; the version stated in every report; coverage reports for the scope; tool qualification, in DO-178C terms |

The consequence for the ladder of 2.7 is the line for the lecture:
**climbing exchanges threats rather than removing them.** Rung 1 to 2 trades
attention and capacity for memory and non-determinism. Rung 3 fixes the
procedure but not the findings. Rung 4 removes non-determinism and introduces
silent mis-implementation and scope. The mitigation therefore changes with the
rung, and the verification plan is where a project records, per clause group,
which rung applies, what independence is required, and how the verifier is
itself verified.

**Pace.** Early in the progression the concept costs no rules; it enters
through two things that the first version already has. Every ledger row
carries its provenance (2.1), and the lecture says once that a row is a claim
and that the ways it can be wrong are listed in one place. The closing
sabotage of each version (3.3) is reframed as the first mitigation: a verifier
that has never been seen to fail has not been verified. From there one threat
surfaces per version with its mitigation, as the "first seen" column records:
the seeded gaps of the audit version double as the audit's known-violation
set, and the script that replaces the skill one version later is verified on
them before it is trusted; the generated ledger takes exit codes at the named
commit, never completion notes; the old suite still passes after a requirement
changes, and the staleness rule, not the suite, turns the row red. The deep
dive comes with the verification plan: the lecture that introduces the plan
opens with the threat table and motivates each field of the plan by a threat,
one rule is added (independence), and that version's sabotage is of a verifier
rather than of the product. Section 5.3 says what the Lean model needs in
order to express the same thing.

## 3. Progression options

Each option is a sequence of versions. A version row names the capability
added (from 1.1), the specification forms introduced, the judgments and
mechanisms introduced, and the process artifacts and rules introduced. No
mapping to lectures is made here. Adjacent versions marked *mergeable* can be
combined to coarsen an option.

In every option, the concept of operations has the same four essential parts
whenever it appears: (a) the purpose statement, (b) the scope, meaning the
system boundary, (c) the user categories, and (d) the user stories. The
elicitation record enters only with the version that teaches elicitation.
Every clause carries its verification method from the first version that has
requirements. CONF is defined as the aggregate of 2.1 from that same version,
because the lesson that passing tests are not verification belongs at the
start; the conformance plugin and `pytest-cov` give the two coverages for one
flag each. The CONF rules are the implicit verification plan until a version
introduces the explicit form.

### Option A. Spiral: every judgment once, minimally, then deepen

The first version shows all five ledger rows on a one-function system; each
later version deepens one or two of them. Specifications precede code from the
start.

Read these rows together with section 9. A1 preserves A0's product behavior;
the exercise's negative-payload policy change is not the A1 baseline. Fixture
tests automate behavioral evidence for the stories, not stakeholder approval
of those stories. The ledger remains handwritten through A1; generation and
systematic test-discipline review enter in A2.

| Version | Capability | Specification forms introduced | Judgments and mechanisms introduced | Process artifacts and rules introduced |
|---|---|---|---|---|
| A0 | F1 | minimal concept of operations (purpose statement, scope, two user categories, three user stories with example messages, each story marked *walkthrough*); plain requirements with identifiers (REQ-0 message, REQ-1 to REQ-3, each marked *test*); test suite; technology (`pyproject.toml`) | all five rows, minimal: SQ by a person reading the clauses (ladder rung 1); RQ `ruff` and the suite collects; CONF as the aggregate: tests pass, requirements coverage from the markers and the conformance report, branch coverage from `pytest-cov`, the stories walked by a person (rung 1); VAL one sign-off on the concept of operations; TR markers resolve; every ledger row carries its provenance, and the closing sabotage is the first verification of a verifier (2.9) | `process/rules.md` with 8 rules, one per category (styles: obligation, gate); hand-written ledger from a provided template; dev log |
| A1 | F1 (unchanged) | the concept of operations revised through elicitation with the stakeholders; the elicitation record (reference, not a specification); glossary; requirements rewritten in EARS; acceptance fixtures derived from the stories | SQ audit (consistency, EARS form, glossary discipline, story-to-requirement alignment, a method on every clause, a reason on every judgment clause) on six to eight seeded gaps, first by a person, then by the agent, then as the `/audit-spec` skill (ladder rungs 1 to 3 on the glossary-discipline check; the seeded gaps double as the audit's known-violation set: the person misses some, which is T1's capacity threat, the agent over-reports one, and the skill's first step is read-before-check); VAL walkthrough per user category and re-sign-off, since the revision made VAL stale; TR trace-matrix tool; CONF story tests over the fixtures (the story walkthrough climbs to a test; the sign-off is kept) | gap-list form; trace matrix report; 8 rules (styles added: procedure, form); first skill, `/audit-spec` (rung 3) |
| A2 | F2 | architecture (stages, order, purity, allocation, integration contract); data format (ad hoc rules); interface contracts (pre- and postcondition per stage); build plan | RQ `mypy` and the test-discipline review; CONF gains *analysis* as a second method (the import rule for the architecture clauses, `mypy` for the signature part of the contracts, and a script for the glossary-discipline check, which reaches rung 4: review becomes analysis, and the script is verified on the A1 seeded gaps before it replaces the skill, T2) and *review* as a third (the allocation table as `review (agent)` with a human spot-check; the purpose statement's implementation-independence stays at rung 3); generated ledger, from exit codes at the named commit and never from completion notes (T4) | plan with tasks, waves, gates, and checkpoint-specific obligations: intermediate commits may have unmet judgments, while wave acceptance requires designated judgments for its declared scope (CF-15); revise inherited per-commit requirements accordingly, rather than merely adding a wave gate; dev log per task; 8 rules (WF-2 to WF-5, RQ-2, RQ-3, CONF-3, CONF-4; styles added: policy, staleness, the approval gate); `/ledger` skill |
| A3 | F4 | change request and change report; workflow graph (the process as a state machine) | a declared change of mind makes VAL stale while the unchanged artifacts can still agree; the subsequent specification revision makes affected evidence stale; impact analysis uses the declared trace links without assuming they capture every dependency; the old suite still passes after the requirement changed, but stale CONF evidence cannot support the revised claim (T4) | branch per change; 4 rules (WF-6, WF-7, RPT-3, RPT-4; style added: change control) |
| A4 | F5 | state machine (table and diagram); message sequence chart; **verification plan**, the first project-specific one: transition coverage as a second realization-coverage objective, and the ladder rung, the independence requirement, and how the verifier is verified, for every clause group | trace tests with transition coverage; table-driven or generated session module; the verification results reviewed against the plan; the deep dive on threats to a judgment (2.9): this version's sabotage is of a verifier, the import analysis made to ignore `from` imports, and its known-violation set catches it | 3 rules (CONF-5 transition coverage; CONF-6 independence; WF-8 the verification plan precedes its tests); the verification plan bundles the project's policies and procedures |
| A5 | F6 | schema or IDL for the message | schema validation at ingress; the generator as the conformance argument | none |
| A6 (optional) | F7 or F8 | policy table as data; non-linear architecture | configuration validation; merge-semantics tests | none |

Mergeable: A4 with A5. The verification plan may instead enter at A3, beside
the workflow graph, if the two process specifications are to be taught
together. **Pros:** the whole picture is visible from A0, so each later
version is "the same five rows, done better"; specifications precede code
throughout; a real sign-off on a real concept of operations is in the first
version. **Cons:** A0 carries four forms and five judgments at once, even
though each is tiny; elicitation, the glossary, and the fixtures wait for A1.

### Option B. Artifact flow: specifications first, code only once they are audited

Versions follow the order in which a specification-driven process produces
artifacts. The first two versions contain no code; the judgments that exist
before code (SQ, VAL, TR) are shown on specifications alone.

| Version | Capability | Specification forms introduced | Judgments and mechanisms introduced | Process artifacts and rules introduced |
|---|---|---|---|---|
| B0 | none (no code) | concept of operations (purpose statement, scope, user categories, user stories with example messages, each story marked *walkthrough*), produced through elicitation; the elicitation record (reference); glossary | VAL walkthrough of the stories by a person (ladder rung 1) and sign-off; SQ for the concept of operations (implementation-independent, observable, terms defined), by a person; TR story identifiers | `process/rules.md` with 4 rules (SQ-1, SQ-2, VAL-1, TR-1; style: obligation); ledger with three rows; dev log |
| B1 | none | EARS requirements, each marked *test*; acceptance fixtures as data | SQ audit of the requirements (consistency, EARS form, alignment, a method on every clause, a reason on every judgment clause) on seeded gaps, by a person, then the agent, then the skill (rungs 1 to 3 on the glossary-discipline check); TR trace matrix story to requirement | gap-list form; 5 rules (styles added: procedure, form); `/audit-spec` skill (rung 3) |
| B2 | F1 | test suite; technology; interface contract for `filter` | RQ `ruff` and the suite collects; CONF as the aggregate: tests pass, requirements coverage, branch coverage, stories walked, then story tests over the fixtures (the walkthrough climbs to a test; the sign-off is kept); the ledger reaches five rows | 5 rules (RQ-1, CONF-1, CONF-2, WF-1, RPT-1; style added: gate); generated ledger |
| B3 | F2 | architecture; data format; build plan | RQ `mypy` and the test-discipline review; CONF *analysis* and *review* as further methods; the glossary-discipline check reaches rung 4 as a script | plan with tasks, waves, gates; dev log per task; 6 rules (styles added: policy, staleness) |
| B4 | F4 | change request and report; workflow graph | a declared change of mind makes VAL stale; impact analysis | 4 rules (style added: change control) |
| B5 | F5 | state machine; sequence chart; verification plan | trace tests with transition coverage; generation; results reviewed against the plan | 2 rules |
| B6 | F6 | schema or IDL | schema validation | none |

Mergeable: B0 with B1; B5 with B6. **Pros:** literally specification-driven;
shows that quality, validation, and traceability are judgments about
specifications, not code; mirrors the Spec Kit flow students meet later.
**Cons:** two code-free versions can feel abstract; the first verification
appears only at B2.

### Option C. Judgment ladder: from vibe coding to engineering, one ledger row at a time

The first version *is* vibe coding (code and tests, no specification). Each
version adds exactly one judgment, so the ledger grows one row per version and
the gap each row closes is felt before it is closed.

| Version | Capability | Specification forms introduced | Judgments and mechanisms introduced | Process artifacts and rules introduced |
|---|---|---|---|---|
| C0 | F1 | technology only (`pyproject.toml`); no specification | RQ: `ruff` and the suite collects; the tests run green but cite nothing, so they verify nothing | one rule (RQ-1; style: obligation); no ledger: this is vibe coding with tests |
| C1 | F1 | plain requirements with identifiers, each marked *test* | CONF and TR: markers; the conformance report with its "no evidence" rows; CONF as the aggregate: tests pass, requirements coverage, branch coverage | first ledger (RQ, CONF, TR); 3 rules (CONF-1, TR-1, WF-1 specification before change; style added: gate) |
| C2 | F1 | EARS requirements; glossary | SQ: audit rules, gap list, well-formedness, a method on every clause and a reason on every judgment clause; seeded gaps; by a person, then the agent, then the skill (rungs 1 to 3 on the glossary-discipline check) | ledger with four rows; 4 rules (SQ-1 to SQ-4; styles added: procedure, form); `/audit-spec` skill (rung 3) |
| C3 | F1 | concept of operations (purpose statement, scope, user categories, user stories marked *walkthrough*), produced through elicitation; the elicitation record (reference); acceptance fixtures | VAL: walkthrough per user category by a person (rung 1), sign-off; story tests over the fixtures (the walkthrough climbs to a test; the sign-off is kept) | ledger with five rows; trace-matrix tool; 3 rules (VAL-1, VAL-2, SQ-5 alignment) |
| C4 | F2 | architecture; data format; interface contracts; build plan | RQ deepened (`mypy`, the test-discipline review); CONF *analysis* and *review* as further methods; the glossary-discipline check reaches rung 4 as a script; generated ledger | plan with tasks, waves, gates; dev log per task; 6 rules (styles added: policy, staleness) |
| C5 | F4 | change request and report; workflow graph | a declared change of mind makes VAL stale; impact analysis | 4 rules (style added: change control) |
| C6 | F5 | state machine; sequence chart; verification plan | trace tests with transition coverage; generation; results reviewed against the plan | 2 rules |
| C7 | F6 | schema or IDL | schema validation | none |

Mergeable: C1 with C2; C6 with C7. **Pros:** the course's central contrast is
literal, and each version closes one named gap; the smallest first step of any
option. **Cons:** code precedes specification for three versions, against the
habit the course wants to form (it has to be framed as retrofitting discipline
onto an existing system); the concept of operations arrives late.

### Option D. Capability-driven: each version is a customer ask

Every version adds a capability and only the forms that capability needs.
Architecture and planning come early because the second stage needs them; the
concept of operations comes when the human stakeholders have to be named.

| Version | Capability | Specification forms introduced | Judgments and mechanisms introduced | Process artifacts and rules introduced |
|---|---|---|---|---|
| D0 | F1 | plain requirements with identifiers, each marked *test*, with a one-line purpose in the preamble; test suite; technology | RQ `ruff` and the suite collects; CONF as the aggregate: tests pass, requirements coverage from the markers and the conformance report, branch coverage; TR markers resolve | 5 rules (styles: obligation, gate); hand-written ledger with three rows; dev log |
| D1 | F2 | architecture; interface and integration contracts; data format; build plan | RQ `mypy` and the test-discipline review; CONF *analysis* for the architecture clauses and the contract signatures, *review* for the allocation table; generated ledger | plan with tasks, waves, gates; dev log per task; 7 rules (WF-2 to WF-5 among them; styles added: policy, staleness) |
| D2 | F3 | concept of operations (purpose statement, scope, user categories including the auditor, user stories marked *walkthrough*), produced through elicitation; the elicitation record (reference); glossary; EARS; acceptance fixtures; log-record data format | SQ audit on seeded gaps, with a method on every clause and a reason on every judgment clause, by a person, then the agent, then the skill (rungs 1 to 3 on the glossary-discipline check); VAL walkthrough by a person (rung 1) and sign-off, then story tests over the fixtures with the sign-off kept; TR trace matrix; the ledger reaches five rows | gap-list form; 8 rules (SQ-1 to SQ-6, VAL-1, VAL-2; styles added: procedure, form); `/audit-spec` (rung 3) and `/ledger` skills |
| D3 | F4 | change request and report; workflow graph | a declared change of mind makes VAL stale; impact analysis; the glossary-discipline check reaches rung 4 as a script | 4 rules (WF-6, WF-7, RPT-3, RPT-4; style added: change control) |
| D4 | F5 | state machine; sequence chart (with the log as a second lifeline); verification plan | trace tests with transition coverage; generation; results reviewed against the plan | 2 rules |
| D5 | F6 | schema or IDL | schema validation; generator | none |
| D6 (optional) | F7 | policy table as data | configuration validation; table-driven filter | none |

Mergeable: D4 with D5. **Pros:** every form has a visible motivating need; the
plan and its waves arrive at the first multi-task change, which is when they
are first felt; the audit log (F3) gives the concept of operations real user
categories and the sequence chart a second participant. **Cons:** SQ and VAL
arrive after architecture and planning, so the first two versions run on
unaudited, unvalidated specifications, which has to be called out.

### 3.1 Comparison

| | A Spiral | B Artifact flow | C Judgment ladder | D Capability-driven |
|---|---|---|---|---|
| First code | v0 | v2 | v0 | v0 |
| First concept of operations and VAL | v0 | v0 | v3 | v2 |
| Elicitation and the elicitation record | v1 | v0 | v3 | v2 |
| CONF as the aggregate (tests, two coverages) | v0 | v2 | v1 | v0 |
| All five ledger rows by | v0 | v2 | v3 | v2 |
| Plan, waves, gates by | v2 | v3 | v4 | v1 |
| Verification plan | v4 (or v3) | v5 | v6 | v4 |
| The verifier ladder: rungs 1 to 3 shown, then rung 4 reached | v1, v2 | v0 to v1, v3 | v2, v4 | v2, v3 |
| Threats to a judgment: surfaced, then the deep dive | v0, v4 | v0, v5 | v1, v6 | v0, v4 |
| Versions to reach the change (F4) | 4 | 5 | 6 | 4 |
| The story the sequence tells | the same five rows, done better each time | specifications are judged before code exists | vibe coding to engineering, one gap at a time | each customer ask pulls in the form it needs |
| Main risk | v0 is dense | an abstract start | specification after code | unaudited specifications early |

### 3.2 Density per version

The budget in 2.3 caps rules at eight per version and new rule styles at two.
Forms are harder to cap, because some are trivial (technology is one file).
This table counts all three so the dense versions are visible; each dense
version has a natural split.

| Option | Versions and (forms / rules / new rule styles) | Dense versions and their split |
|---|---|---|
| A | A0 (4/8/2), A1 (4/8/2), A2 (4/8/2), A3 (2/4/1), A4 (3/3/0), A5 (1/0/0) | A0's concept of operations is minimal and its story fixtures wait for A1; if still too dense, split A0 into requirements + tests (RQ, CONF, TR) then concept of operations + SQ + VAL + ledger; A2 into architecture + contracts then data + plan |
| B | B0 (3/4/1), B1 (3/5/2), B2 (3/5/1), B3 (3/6/2), B4 (2/4/1), B5 (3/3/0), B6 (1/0/0) | none |
| C | C0 (1/1/1), C1 (2/3/1), C2 (2/4/2), C3 (3/3/0), C4 (4/6/2), C5 (2/4/1), C6 (3/3/0), C7 (1/0/0) | C4 into architecture + contracts then data + plan |
| D | D0 (3/5/2), D1 (4/7/2), D2 (5/8/2), D3 (2/4/1), D4 (3/3/0), D5 (1/0/0) | D1 as for A2; D2 into concept of operations + glossary then EARS + fixtures + log format |

### 3.3 Recommendation

**Option A with C0 as a prelude.** Keep the spiral, and place the vibe-coding
snapshot (code, tests, no specification, no ledger) *before* A0 as the contrast
the material opens on: the same `filter`, the same tests, and no way to answer
"what did the stakeholders ask for, and how do you know this does it?". A0
then answers the question with the five rows. This keeps
specification-before-code as the habit from A0 on, makes the central contrast
literal, and puts a minimal concept of operations, and so a real VAL sign-off,
in the first version. If A0 is judged too dense, the split in 3.2 turns it
into D0 followed by a half step. The verification plan enters at A4 with the
state machine, where the first project-specific objective appears, or at A3
beside the workflow graph.

Whichever option is chosen, each version should end with a **"break it"**
demonstration emphasizing the judgments introduced in that version and which
verifiers reveal a problem. A change can affect more than one judgment;
distinguish initially stale evidence from fresh failing results. Examples are a
contradictory requirement for SQ; a lint error for RQ; for CONF, `filter`
passing a Critical message (a test fails), and then a test deleted so that one
clause has no evidence while every remaining test passes and branch coverage
barely moves (the requirements-coverage conjunct fails, which is the lesson of
the game demo's VER-8); for VAL, a concept of operations and a requirement
that pass every check while a stakeholder withholds the sign-off, since
nothing in the automated behavioral checks catches the mismatch; an invalid
clause citation for TR. Removing a citation is not itself a TR violation:
tests may be uncited, although removing a clause's last citing test leaves a
CONF coverage gap.

The sabotage is also the first verification of the verifier (2.9): a verifier
that has never been seen to fail has not been verified, and the ledger row it
establishes is trusted only to that extent. From the version that introduces
the verification plan, the sabotage is of a verifier rather than of the
product: the import analysis is made to ignore `from` imports, the
architecture row stays green, and the known-violation set kept beside the
analysis catches it. The seeded gaps of the audit version are reused as the
known-violation set of the script that replaces the skill one version later.

## 4. Canonical list of specification forms

The forms fall into two categories. A **product specification** constrains
the system being built, and the code and its tests are verified against it. A
**process specification** constrains the work; its realization is the
repository history, and the history is verified against it. The two are kept
in separate tables because students must never confuse a rule about how to
build with a clause about what to build, and because the second category is
introduced more slowly than the first (2.8).

For each form: what it constrains, when it is the right form, its verification
method in the shape of 2.5 (verifier; specification coverage; realization
coverage; what a pass does not show), what the form must agree with, how it
maps to the catalog in `../specification-kinds.md`, and which capability from
1.1 first needs it. The three questions the brief asks of every form are the
third, fourth, and fifth columns. Forms are cited by name, never by number, as
the catalog does.

### 4A. Product specifications

| Form | Constrains | Appropriate when | Verification method (verifier; specification coverage; realization coverage; what a pass does not show) | Must agree with | Catalog today | First needed by |
|---|---|---|---|---|---|---|
| Concept of operations: purpose statement, scope (the system boundary), user categories, user stories | what the system is for, who the users are, what they observe, the scenarios | any system with users; the first document; present in every version that has a VAL row | walkthrough by a person; every story walked; every user-visible operation exercised; acceptance tests derived from the stories' examples add a *test* method; a pass does not establish any technical clause | governs everything; the purpose statement is agreed with the stakeholders before the rest is derived; every requirement traces to a story | concept of operations | any version with a VAL row; F3 gives it an auditor |
| Glossary / domain model | vocabulary; later, entities and attributes | always; it grows into the data model | analysis by a script; every term defined once and every capitalized term in every specification resolved; review for meaning; a pass does not establish that the definitions are right | every specification uses only its terms; the data format refines it | listed as "not a kind"; promote | with the concept of operations |
| Behavioral requirements (EARS) | input/output and event behavior | observable functional behavior | test; every mechanical clause has its tests (requirements coverage); branch coverage to the stated level (structural coverage); a pass does not establish that the tests' expectations are right | traces to stories; allocated to a stage; refined by contracts | behavioral requirements | F1 |
| Acceptance scenarios / fixtures | concrete input-to-output examples | behavior that can be stated by example; portable across realizations | test, parametrized over the file; every scenario run; the clauses the scenarios cover reported; a pass says nothing about inputs no scenario covers | derived from stories; agrees with the requirements | fixtures; example session | F1 |
| Data format (rules, then schema or IDL) | the form of stored or exchanged data | any persisted or exchanged artifact | analysis by a validator or generated parser; every rule checked on every instance; the schema itself validated against its metaschema; a pass does not establish anything about meaning | agrees with the glossary; cited by requirements and contracts | data format (generation new) | F2 ad hoc; F3 the log record; F6 the schema |
| Architecture (parts, order, dependency constraints, allocation) | structure and boundaries | two or more parts | analysis by the import rule; every constraint checked against every module; review of the allocation table, every requirement allocated; a pass does not establish that the boundaries are right | every requirement allocated; integration contracts across each boundary | architecture ("named only") | F2 |
| Interface contract (signature, pre- and postcondition; integration assume/guarantee) | per-operation behavior; assumptions between parts | any API boundary | analysis by the type checker for signatures; test (unit, property) for pre- and postconditions on every operation; branch coverage; a pass does not establish behavior on inputs no test uses | refines the allocated requirements; one part's guarantee is the next part's assumption | interface contract (integration part new) | F2 |
| State machine (protocol) | ordering and modes | stateful behavior; protocols | test by traces; every transition exercised (transition coverage); branch coverage of the session module; or generation, which moves the question to the generator; a pass does not establish transitions no trace takes | transitions trace to requirements; agrees with the sequence charts | a form of interaction flow; make it a kind | F5 |
| Message sequence chart | interactions among parts over time | multi-part scenarios | test by scripted end-to-end runs; every chart run; the parts it names exercised; a pass does not establish other interleavings | agrees with the architecture and the state machine | not present | F3 or F5 |
| Test suite | executable claims | always | it is the verifier; its own verification is a review for test discipline and a sabotage (a broken realization must fail it); green establishes that the suite's claims hold, not that they are the right claims | each test cites a clause | test suite | F1 |
| Technology and platform | languages, tools, versions | always | analysis of dependency and lock files; every named tool present at the named version; review for provenance; a pass does not establish that the tools are correct or safe | the gate commands name these tools | technology and platform | F1 |

#### Scenarios and tests: one concept, two bindings

Two product forms, acceptance scenarios and the test suite, both specify
slices of behavior, and students ask why there are two. The answer starts
with quantification. A requirement is universal: for every Restricted message
with a payload above 100, the output payload is 100. A scenario is
existential: this message, this output. A set of scenarios therefore
*under-approximates* the requirement, in the verification sense: every
behavior it checks is one the requirement demands, but the requirement demands
behaviors the set never checks. Conformance by scenarios is sound for failure
(a failing scenario is a real nonconformance, if the scenario is right) and
incomplete for success (passing is not conformance). That incompleteness is
why the CONF row carries two coverages: citation-based requirements coverage
says every test clause has citing evidence, and structural coverage reports
which code structures the suite exercised. Neither establishes that the
assertions adequately instantiate the clauses. The "slice" has a
classical name, the equivalence class: a good scenario set takes one
representative per class and the boundaries between classes, which is why
REQ-5 is written as 5a, 5b, and 5c.

A scenario can also be read as a *refinement* of the requirement: the
universal clause interpreted at particular values. Instantiating a clause
fixes two things, not one: the values, and the *interface* through which the
check is made (which function is called, how state is set up, what counts as
the output). The two forms differ in how much they bind.

| | Acceptance scenarios / fixtures | Test suite |
|---|---|---|
| Binds | values only | values and the interface |
| Is | data (a JSON file) | code in one language and one framework |
| Readable by | a stakeholder: "Restricted 150 in, Restricted 100 out" | a programmer |
| Portable | yes: every realization in every language must reproduce it | no: re-expressed per language |
| Role | a specification only; needs a loader to run | a specification and the verifier at once |
| Can constrain | observable input to output through the public interface | anything: internal state, exceptions, call order, structure |
| Can go beyond examples | no | yes: a property-based test samples the universal clause directly |
| Governance | specification side: never edited to make a test pass; a wrong expectation is a gap about the pair (fixture, specification) | realization side: edited under the test discipline |
| Serves as an oracle | yes: two realizations passing the same file; the plain one specifies the clever one | tied to one realization |

So an acceptance fixture is intended to refine the requirement while remaining
interface-independent, and its implementing test binds the scenario to a
realization. Review must establish whether those refinements are faithful;
the trace matrix records the declared requirement-to-scenario-to-test chain,
not proof of its semantic correctness. Additional implementation-detail or
regression tests may be uncited and need not belong to that chain.

If the system had one realization in one language and no stakeholder who
reads, the test suite alone would do and the fixtures would be a duplicate.
Three things make the fixture form earn its place in the example:

- **It is the bridge from validation to verification.** The scenarios are
  derived from the user stories and are the one executable artifact a
  stakeholder can read and sign. On the ladder of 2.7 they are where a human
  walkthrough's behavioral checks become tests while approval of the stories
  remains a separate human judgment. Checking that a signature exists does
  not automate validation. Fixtures therefore enter with the revision of the
  concept of operations rather than later.
- **They outlive the realization.** The HAMR example is the same system in
  Rust; a port and any second realization pass the same file. The published
  test vectors of a hash function are the industrial version.
- **They separate the two change-control regimes.** The test suite's dual
  role, a specification of the code and a realization of the verification
  objectives, confuses students. The fixture is purely on the specification
  side, so "never edited to pass" has a clean home, and the lesson that a
  wrong expectation is a gap and not a bug has a clean example.

The test suite earns its place as an executable verifier: it can participate
in an algorithmic gate, reach inside the interface, and state a property
over sampled inputs, which is as close as a test gets to the requirement's
universal form. One line for the lecture follows: a test suite does not stop
being an under-approximation when it is large, a property-based test narrows
the gap without closing it, and the only thing that closes it is analysis, a
proof or an exhaustive check over a finite domain, which is the method the
contract and state-machine forms reach for when the domain allows it.

### 4B. Process specifications

A process specification's realization is the repository history: the commits,
the reports, the ledger, the completion notes. Its conformance question is
whether the history followed it. Its verification is a hook or a script where
a rule is mechanical (analysis) and a reading of the log where it is not
(review), and its two coverages are "every rule checked" and "every commit
examined". Every rule in these forms has one of the seven styles of 2.8, and
the four questions the course asks of a product specification apply to it
unchanged.

| Form | Constrains | Appropriate when | Verification method (verifier; specification coverage; realization coverage; what a pass does not show) | Must agree with | Catalog today | First needed by |
|---|---|---|---|---|---|---|
| Development rules (governance, by category) | how each judgment is established and when it must hold | always | review of the repository history, ledger, and dev log against every rule; analysis where a rule is a gate; a pass establishes only what the history records | the categories mirror the judgments | development process | any version |
| Build plan (tasks, waves, gates) | the decomposition and ordering of one build | any change larger than one task | review; every task done; every wave closed at its gate; the ledger at each wave end | tasks cite clauses; waves end at gates | listed as "not a kind" (DEV-9); make it explicit | F2 |
| Verification plan | for each clause group: method and technique, environment and tool versions, coverage objectives (the requirements-coverage criterion, the structural-coverage level, transition coverage), independence (who may verify what; whether an agent-written suite needs a human review), how each verifier is verified (its known-violation set, a review against its clauses, or a comparison with a second verifier), when each verification runs, and the evidence each must produce | when a project makes verification choices beyond the standing CONF rules: a second realization-coverage objective, or an independence requirement; until then the CONF rules are the plan | review of the verification results against the plan; every objective met with its evidence; every independence requirement met; a pass does not establish that the objectives were the right ones | the method attribute on every clause; the CONF rules; the gates of the workflow graph | the policy part of VER-4 to VER-8, and the per-clause part of "verification obligations"; the Software Verification Plan of DO-178C is the industry form | F5 |
| Workflow graph (the process as a state machine) | the allowed sequences of steps | multi-step or multi-agent work | review of `git log` against the graph; every step in an allowed order; every gate passed; analysis by hooks and monitors where written | its edges are the gates | the essay's sixth example; not in the catalog | F4 |
| Change request and change report | what a change touches and what it re-established | any change to a governed artifact, including a declared change of mind | review against the trace matrix and the ledger diff; every affected identifier listed; every stale row re-established | lists every affected identifier; names the ledger rows re-established | not present | F4 |

The elicitation record is not in either table: it is reference material, not
a specification (section 2.2). "Verification obligations", a kind in the
catalog, is not a form here: its per-clause part is the verification method on
each clause, its policy part is the CONF rules, its evidence is the generated
conformance report, and the choices that are not derivable from those are the
verification plan (section 5.2).

## 5. Vocabulary alignment

### 5.1 Glossary additions (applied 2026-10-20)

The entries this design proposed were added to `../glossary.md` on
2026-10-20, and the glossary is now the home of their definitions; the Lean
name is given there where the model in `AgenticDev` has one. The terms added
are: artifact; assurance; change request and change report; development log;
development state; development-state judgment; elicitation record; establish
and stale; governance; independence; intent; known-violation set; ledger;
mitigation; plan, task, and wave; product and process specification;
provenance; purpose statement; realization quality; reference; requirements
and structural coverage; rule style; threat; traceability; verification
method; verification plan; verifier ladder. The existing entries for *audit*,
*concept of operations*, *gate*, *mechanical clause; judgment clause*, and
*validation* were amended as 5.2 recommends.

### 5.2 Conflicts found between the glossary, the catalog, the essay, and the brief

The rows whose recommendation changes `../glossary.md` were applied on
2026-10-20: the widened *gate*, the *mechanical clause* wording, *validation*
covering every specification, *audit* as the activity whatever the judgment,
and the five quality properties with traceability moved to TR. The rows that
change the catalog (`../specification-kinds.md`: the glossary as a kind,
*verification obligations*, *user categories*) wait for the build, as section
6 says.

| Conflict | Recommendation |
|---|---|
| The glossary says a person or an agent cannot be a gate; the brief wants human audits as gates | widen *gate* to two kinds, algorithmic and approval (2.1) |
| *judgment clause* (glossary) against *development state judgement* (brief); the spelling also differs | keep the "judgment" spelling throughout; say *development-state judgment* for the five rows; *judgment clause* stays as is |
| the glossary's *mechanical clause*, "a program can decide it from the artifact alone", reads as static-only; VER-2's table counts unit tests as mechanical | reword to "by examining the artifact or by executing it"; mechanical = test or analysis (2.6) |
| Lecture 01 names three kinds of verifier; the first draft of 2.6 had two rows, an algorithm and "a reader" | the reader row is split: human and agent are the two reader kinds, and a judgment clause records which (2.6); the ladder from one to the next is 2.7 |
| the glossary is "not a kind" (catalog) against "an important specification, a simple domain model" (brief) | promote it to a kind; it is cross-cutting and audited |
| validation applies to the concept of operations only (glossary) against "specifications conform to intent" (brief, Lean) | adopt the Lean reading; the concept of operations is where validation is *performed*, not the only specification it covers |
| the first draft of this design had an intent-statement artifact; the brief and the Lean model treat intent as having no artifact | removed; the purpose statement of the concept of operations is the nearest written thing and is a specification; the elicitation record is reference |
| the catalog lists *verification obligations* as a kind, and `SPECS.md` section 9 of the game is one | not a form here: the per-clause part is the verification method on each clause, the policy part the CONF rules, the evidence the generated conformance report; the non-derivable choices are the verification plan |
| VER-8 reports clause coverage and branch coverage separately but the gate (VER-4) checks only branch coverage | CONF gates on both: verified is the conjunction of every test passing, requirements coverage, structural coverage, and every judgment clause reviewed |
| the glossary bans *checker* for the verifier role; the first draft of the method values used *check* | the value is *analysis*, which also matches DO-178C and the MIL-STD/INCOSE set; a human's analysis is a *review* |
| the catalog says *user classes*; this design says *user categories* | adopt *user categories*; update the catalog when the example is built |
| *audit* means specification quality only (glossary) against audits of conformance and of ledgers (essay, brief) | keep *audit* for the activity of reading artifacts against rules, whatever the judgment; the judgment's name says what is audited |
| realization quality has no home among AUD, DEV, VER, RPT | the RQ category gives it one |
| five specification-quality properties (glossary) against three (brief) | SQ covers unambiguous, internally consistent, externally consistent, well-formed (syntactic), and complete; *traceable* moves to TR |
| *filter* means transform in the HAMR example and drop in ordinary usage | decided: `filter` drops, `sanitize` transforms (section 1) |
| the essay's "test vectors as specifications" is still a TODO | the acceptance scenarios and test suite entries in section 4, and 2.5, stand in for it |
| Lecture 01 lists six ways a verification result can be invalid; this design classifies five threats to a judgment (2.9) | keep the lecture's list and cite it; the six sort into the five (a defective S into T1; wrong version of S and checking from memory into T4; clauses not decided into T3; mis-implementation and attention into T2); the shared mistake, T5, is new; a later lecture may re-cut the list |

Where the game demo's verification rules go in this design:

| Game demo rule | Home here |
|---|---|
| VER-1 verifiers and scope | the "established by" column of the ledger; the *who decides* axis of 2.6 |
| VER-2 mechanical and judgment clauses, the table | the verification method on each clause (2.6); an SQ rule that every clause carries one |
| VER-3 when verification runs | WF rules: A0/A1 require the automated gate before every commit; A2 separates intermediate checks from wave-acceptance gates requiring designated judgments for a declared scope |
| VER-4 the gate | the algorithmic gate: CONF's mechanical conjuncts together with RQ's analyses |
| VER-5 coverage policy | CONF's structural-coverage objective, a standing CONF rule; a verification plan when project-specific |
| VER-6 test discipline | RQ (a test can fail; assertion adequacy; setup discipline) and TR (every supplied clause citation resolves; citations are optional for tests); CONF requires citing evidence for every clause assigned method test |
| VER-7 fixtures are never edited to pass | a WF rule: governance of executable specifications |
| VER-8 coverage is not conformance | CONF defined as the aggregate; both coverages gated and both reported |
| AUD-14 obligations map both ways | TR (every link resolves) and CONF's requirements-coverage objective; the conformance report's "no evidence" rows |
| `SPECS.md` section 9, verification obligations | dissolved into the method on each clause, the CONF rules, and the generated report; the verification plan holds the non-derivable choices |

The method values against the industry vocabularies:

| This design | DO-178C (reviews, analyses, tests) | MIL-STD and INCOSE (test, analysis, inspection, demonstration) |
|---|---|---|
| test | test | test |
| analysis | analysis | analysis |
| review | review | inspection |
| walkthrough | (no named activity) | demonstration |

DO-178C also names two of the mitigations of 2.9: *independence* between the
author and the verifier of an item (T5), and *tool qualification* under
DO-330 for a tool whose output is trusted without review, which is "who
verifies the verifier" at rung 4 (T2).

### 5.3 Where the Lean model and the example meet

The simple example maps to the Lean model as follows. `HI` has no artifact: it is
what the stakeholders have in mind, and `updateHI` is a change of mind, which
the process records as a change request. `specs/` is `S`; `guard/` and
`tests/` are `R`; the four Lean judgments are SQ, RQ, CONF, VAL, with
`Verification s r` read as the aggregate of 2.1; the ledger is `Ledger`; a
task's commit is a `Step` in this simple mapping. This correspondence does
not require every repository commit in a richer workflow to be an acceptance
checkpoint. A later model could represent intermediate commits explicitly
and require designated judgments only at acceptance transitions, or abstract
the intermediate commits within a step representing an accepted transition.
These are modeling choices, not claims that the existing model already
implements A2's checkpoint policy.

The coarse dependency sketch "a specification change
invalidates CONF, VAL, SQ, TR; a code change invalidates RQ, CONF, TR; a declared change of mind
invalidates VAL only" illustrates the intended dependency idea. It is not a
complete implementation rule: the course evidence model also accounts for
tests, verifier versions, relevant configuration/environment, and a verifier
later found defective. Use section 2.1 and CF-09 for the practical ledger
semantics rather than inferring an exact invalidation matrix from this sketch.
Suggested evolutions of the model, none required by the course:

1. a fifth judgment, `traced`, depending on `s` and `r`;
2. clause-level granularity, with `S` a set of identified clauses so that
   `dependsOn` and invalidation work per clause, as the trace matrix does;
3. waves and gates: `StepsWithin allowed` already describes the shape of a
   wave; a gate is a `Policy` required at the wave's last state;
4. ledger rows that record provenance (which verifier, which specification
   version, when) and keep a *stale* status rather than being deleted, as the
   planned generated `ledger.md` will do;
5. evidence that can be wrong, which is the model's own roadmap (its items on
   actors, richer dashboard entries, and unsound assessments): `establish`
   carries evidence rather than a proof; each verifier has a soundness
   hypothesis; `LedgerSound` becomes conditional on the soundness of the
   verifiers the rows cite; and distrusting a verifier invalidates the rows
   whose provenance cites it, a second kind of invalidation beside
   `dependsOn`. The policy "CONF may be established only while SQ is current"
   is T1 of 2.9 as a theorem, and actors give T5 as "no certified verification
   without a step by someone other than the author". An inconsistent intent is
   outside the model, since intent is its reference by construction; that
   threat stays a matter of process.

## 6. Repository layout and reuse

- **Location:** `module-ase-principles/demos/running-example-message-guard/`,
  one snapshot directory per version (`v0/`, `v1/`, and so on), plus a planned
  `build-history.sh` that replays the snapshots into a tagged git repository.
  Replay starts with the completed A0 as a baseline commit; its dev-log tasks
  must not be represented as separate commits claimed to satisfy A0's rules.
  Label replayed history as a reconstruction, not the original build history.
  Later intermediate commits must follow the checkpoint policy applicable to
  their version. Lecture notes link to a fixed snapshot; students can
  `diff -r v1 v2`.
- **Reuse:** adapt `tests/conftest.py` and `tests/conformance.py` from
  `module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/`
  (identifier patterns for `REQ-`, `US-`, `ARCH-`, `DATA-`, `IF-`; status
  vocabulary unchanged; the report is the requirements-coverage evidence);
  adapt its `tests/test_architecture.py` as the import analysis for the
  architecture clauses; copy its `pyproject.toml` marker configuration
  (`--strict-markers`); add `pytest-cov` for structural coverage.
- **Licensing:** `specs/`, `process/`, `reports/`, and `reference/` are CC BY
  4.0 prose; `guard/`, `tests/`, `tools/`, and configuration are MIT, per
  `LICENSING.md`.
- **Documents to update when the first version is built:**
  `specification-kinds.md` (the new kinds, *user categories*, the verification
  plan, and a "first needed by" column), the `CLAUDE.md` demos index, the
  module README, and the brief `running-example.md` (which already points
  here). The glossary was updated on 2026-10-20 and needs no further change.
- **Document to create:** `process-rule-styles.md` at the repository root,
  beside `specification-kinds.md`, with the rule-style table, the template,
  the principles, the design grid, and one worked example per style from the
  guard (2.8).

## 7. Coverage checklists

### 7.1 Glossary terms by the first version that illustrates each

| Term | A | B | C | D | Illustrated by |
|---|---|---|---|---|---|
| audit | A1 | B0 | C2 | D2 | the SQ audit and its gap list |
| concept of operations | A0 | B0 | C3 | D2 | `specs/conops.md` with its four essential parts |
| conformance | A0 | B2 | C1 | D0 | the CONF row as the aggregate; the conformance and coverage reports |
| executable specification | A0 | B2 | C1 | D0 | tests that cite clauses; fixtures from A1 / B1 / C3 / D2 |
| family of specifications | A0 | B1 | C2 | D1 | several `specs/*.md`; audited together for consistency from A1 / B1 / C2 / D2 |
| gate (algorithmic) | A0 | B2 | C1 | D0 | the gate command in WF-1 |
| gate (approval) | A2 | B3 | C4 | D1 | the sign-off that closes a wave |
| invariant | A0, A2 | B2, B3 | C1, C4 | D0, D1 | A0/A1: the automated gate passes before each commit; A2: designated judgments are established before wave acceptance |
| mechanical clause; judgment clause | A0 | B0 | C1 | D0 | the verification method on each clause: mechanical = test or analysis, judgment = review or walkthrough |
| verification method (of a clause) | A0 | B0 | C1 | D0 | *test* and *walkthrough* first; *analysis* and *review* from A2 / B3 / C4 / D1 |
| requirements coverage; structural coverage | A0 | B2 | C1 | D0 | the conformance report's "no evidence" rows; the coverage report |
| verification plan | A4 | B5 | C6 | D4 | `plans/verification-plan.md`; the CONF rules stand in for it before |
| realization | A0 | B2 | C0 | D0 | `guard/` |
| specification | A0 | B0 | C1 | D0 | `specs/conops.md` or `specs/requirements.md` |
| validation | A0 | B0 | C3 | D2 | the VAL row and the sign-off |
| verification | A0 | B2 | C1 | D0 | the test suite and the two coverages under the CONF row |
| verifier (human, agent, algorithmic) | A0 | B0 | C1 | D0 | the "established by" column of the ledger; the verifier kind on each judgment clause |
| verifier ladder | A1, A2 | B1, B3 | C2, C4 | D2, D3 | the glossary-discipline check: a person, the agent, the skill, then a script; the story walkthrough becoming fixture tests with the sign-off kept |
| intent | A0 | B0 | C3 | D2 | no artifact: the VAL sign-off, and the declared change of mind that makes VAL stale in A3 / B4 / C5 / D3 |
| purpose statement | A0 | B0 | C3 | D2 | the opening of `specs/conops.md` |
| elicitation record (reference) | A1 | B0 | C3 | D2 | `reference/elicitation.md` |
| artifact | A0 | B0 | C1 | D0 | the categories in `process/rules.md` |
| development state; ledger | A0 | B0 | C1 | D0 | `reports/ledger.md` |
| development-state judgment (all five) | A0 | B2 | C3 | D2 | the five ledger rows; three rows from B0 / C1 / D0 |
| establish; stale | A1, A2 | B3 | C4 | D1 | the re-sign-off after A1's revision; rule WF-5 and the regenerated ledger; the declared change of mind in A3 / B4 / C5 / D3 |
| development log | A0 | B0 | C1 | D0 | `reports/dev-log.md` |
| traceability | A0 | B0 | C1 | D0 | markers; the trace matrix from A1 / B1 / C3 / D2 |
| plan; task; wave | A2 | B3 | C4 | D1 | `plans/001-*.md` |
| realization quality | A0 | B2 | C0 | D0 | the RQ row |
| governance | A0 | B0 | C0 | D0 | `process/rules.md` |
| rule style (seven) | A0 | B0 | C0 | D0 | obligation and gate first; procedure and form with the audit; policy and staleness with the plan; change control with the change |
| change request; change report | A3 | B4 | C5 | D3 | `reports/CR-001.md` |
| assurance | A0 | B0 | C1 | D0 | the ledger read as an argument |
| threat to a judgment; mitigation | A0 (deep dive A4) | B0 (B5) | C1 (C6) | D0 (D4) | the closing sabotage as the first verification of a verifier; the threat table with the verification plan |
| provenance (of a ledger row) | A0 | B0 | C1 | D0 | the verifier, artifact version, and clauses on every row of `reports/ledger.md` |
| known-violation set | A1 | B1 | C2 | D2 | the seeded gaps of the audit, reused to verify the script one version later |
| independence | A4 | B5 | C6 | D4 | the per-clause-group requirement in `plans/verification-plan.md`; the person-authored fixtures from A1 / B1 / C3 / D2 are the first instance |

### 7.2 Specification forms by the first version that introduces each

| Form (section 4) | A | B | C | D |
|---|---|---|---|---|
| concept of operations | A0 | B0 | C3 | D2 |
| glossary / domain model | A1 | B0 | C2 | D2 |
| behavioral requirements (EARS) | A1 (plain from A0) | B1 | C2 (plain from C1) | D2 (plain from D0) |
| acceptance scenarios / fixtures | A1 | B1 | C3 | D2 |
| data format | A2 | B3 | C4 | D1 |
| architecture | A2 | B3 | C4 | D1 |
| interface contract | A2 | B2 | C4 | D1 |
| state machine | A4 | B5 | C6 | D4 |
| message sequence chart | A4 | B5 | C6 | D4 |
| test suite | A0 | B2 | C0 | D0 |
| technology and platform | A0 | B2 | C0 | D0 |
| development rules (process) | A0 | B0 | C0 | D0 |
| build plan (process) | A2 | B3 | C4 | D1 |
| verification plan (process) | A4 | B5 | C6 | D4 |
| workflow graph (process) | A3 | B4 | C5 | D3 |
| change request and report (process) | A3 | B4 | C5 | D3 |

## 8. Open decisions

1. **Which progression**: settled 2026-10-20, option A. The first lecture
   opens on a diagram of intent, the specifications, the realization, and the
   five judgments, each illustrated by an A0 artifact; the later deep dives
   (elicitation, the concept of operations, and EARS; testing, the two
   coverages, and traceability) are A1 and the CONF machinery. A0 is built
   first, under `../module-ase-principles/`, a new module kept beside
   `module-software-engineering/` while that module is still taught. A1
   follows once the elicitation procedure is redesigned: the grill-me skill
   overwhelmed students with questions on the game and the note set, and Spec
   Kit's clarify, at most five questions with options and a recommended
   default, is the model. (Done 2026-10-22: the redesigned procedure is the
   `/elicit` skill of A1, modeled on clarify with a concept-of-operations
   taxonomy and a verbatim record under reference; A1 is built.) C0 is
   deferred, not rejected. Three adjustments
   keep A0 self-sufficient: the domain terms are a section of the concept of
   operations, the requirements stay plain with identifiers and methods, and
   the first lecture runs two sabotages (CONF and VAL), the other three
   waiting for the testing lecture, which tells the maturing of a suite into a
   verification method by subtraction on A0 rather than by versions. The user
   categories are the message sender and the security officer. A0 has REQ-0 to
   REQ-3; a fourth requirement would have been implied by the other three,
   which an audit would flag.
2. **The glossary**: settled 2026-10-20. The additions in 5.1 and the
   glossary rows of 5.2, including the widened *gate* and the fifth judgment
   TR, are applied to `../glossary.md`; the catalog rows of 5.2 wait for the
   build.
3. **Whether the audit log (F3) is part of the core**, which decides whether
   the concept of operations has an auditor user category with something to
   observe.
4. **When skills enter**: settled by 2.7. A skill is rung 3 of the verifier
   ladder, so `/audit-spec` enters with the first audit and `/ledger` with the
   generated ledger; the earlier skills lecture and the example tell the same
   story.
5. **Where the verification plan enters**: with the state machine (A4, B5,
   C6, D4), where the first project-specific objective appears, or one version
   earlier beside the workflow graph.
6. **Whether the rule-style handout** (2.8) is a standing document at the
   repository root beside `specification-kinds.md`, or a section added to that
   catalog.
7. **Where the deep dive on threats to a judgment lands** (2.9): with the
   verification plan version, as recommended, because the plan's fields are
   the mitigations; or a standalone lecture after it, which would also be the
   place to re-cut Lecture 01's six-item list into the five classes. Until
   then the lecture's list stands and is cited.

## 9. Implementation constraints and carry-forward items from review

This is the implementation handoff for the chosen Option A progression.
The [A0/Lecture 1 review](../module-ase-principles/review-lecture-01-a0.md)
retains findings, discussion, superseded proposals, and rationale. This
section records what should carry forward without requiring the next agent
to reconstruct decisions from that history. It does not approve all 41
original review edits.

**Disposition and completion are different.** Accepted means a governing
decision or an existing design commitment; proposed means an improvement
awaiting approval; open question means a choice still needs resolution.
Acceptance is not evidence of implementation. A completion check below is a
future obligation for an accepted item, or a proposed check if the item is
not yet accepted. A1 and later implementation evidence is still pending.
Later versions inherit earlier accepted constraints unless an explicit
decision supersedes them; do not read only the target version's subsection.

Keep identifiers stable. When a proposal is accepted, update its disposition
and the governing design text together. When a version is built, retain the
item and link its completion evidence and remaining work. A resolution in
Lecture 1 does not close the corresponding A1/A2 implementation work. These
IDs organize the build handoff; they are not new `process/rules.md` rules and
do not increase the progression's rule budget.

### 9.1 Shared constraints

#### CF-01 — Optional test citations

**Disposition:** Accepted. **Applies from:** A1 onward; preserves the agreed
A0 policy in section 2.1.

Tests may omit clause citations. Each clause assigned method *test* needs
citing evidence; supplied citations must resolve, and all citing tests must
pass for the clause's test evidence to be accepted. Uncited tests remain
subject to the suite's execution policy and may contribute to branch
coverage. Do not invent requirement links merely to make every test traced.

**Completion check:** demonstrate acceptance of an otherwise valid suite with
an uncited passing test, rejection of an invalid citation, a coverage gap
when a test clause has no citing test, and an overall gate failure when an
uncited test fails. These are checks of the evidence machinery, not new
product requirements.

**A1 completion (2026-10-22):** all four demonstrated and scripted on
`v1/tooling/conformance-plugin.md` ("Deliberate-failure checks") and in
`v1/README.md` ("Breaking the verifiers"); the tooling tests under
`v1/tests/tooling/` cite no clause and are accepted by the suite.

**Source:** [review section 8.1.B](../module-ase-principles/review-lecture-01-a0.md),
which supersedes the original mandatory-citation proposal in edit 3.

#### CF-02 — Evidence supports a fallible claim

**Disposition:** Accepted. **Applies from:** A1 onward, in code/report wording
and the associated lectures.

Keep citation-based requirements coverage, structural coverage, and assertion
adequacy distinct. Passing prescribed checks supports a scoped CONF claim,
not proof of all required behavior. A failed check requires investigation;
the defect may be in the specification, implementation, (these first
two should be the focus, and descriptions should indicate that these
are the most likely), verifier, or setup (descriptions should indicate
that we need to keep these in mind to understand all the potential
failure modes, but the proposed methodology does not aim to address
these directly).

**Completion check:** review generated report labels, audit explanations, and
lecture claims for these distinctions. Include assertion adequacy in the
planned A2 test-discipline review; a valid citation alone is not its result.

**A1 completion (2026-10-22):** the conformance report's legend says a
citation declares intended support and does not establish that the
assertions check the clause; the trace matrix's scope line says the tool
decides links, not meaning; the ledger's tables call every row a supported,
fallible claim. Assertion adequacy remains A2's.

**Source:** [review section 8.1.A and B](../module-ase-principles/review-lecture-01-a0.md).

#### CF-03 — Ledger intuition and progression scope

**Disposition:** Accepted. **Applies from:** A1 onward; automation enters A2.

Use the status meanings in section 2.1. Distinguish stale evidence from a
fresh failure or unfinished checking, and do not promise one affected row
per change. Product behavior checked with pytest is test evidence; analysis
of citations and coverage is a separate aggregation step. Keep the A1 ledger
handwritten and the early lecture explanation high level. Preserve A1's
unchanged product behavior: do not import Exercise 1's negative-payload
policy change, an audit log, or a new no-message input API into its baseline.

**Completion check:** the A1 diff preserves product behavior, its lecture and
reports use the agreed distinctions, and the demo accurately identifies
which files update automatically. The A2 build addresses CF-08 and CF-09.

**A1 completion (2026-10-22):** `guard/` is byte-identical between v0 and
v1 (`diff -r v0/guard v1/guard` is empty); the ledger is handwritten, with
tables at a1-specs (VAL stale) and v1; `v1/README.md` has a table of which
files a run generates and which are written by hand.

**Source:** [review sections 8.1.C and 8.2](../module-ase-principles/review-lecture-01-a0.md).
The linked [ledger evolution sidebar](../module-ase-principles/lecture-notes/ledger-evolution-example.md)
is an optional teaching aid, not an actual execution history or a complete
dependency algorithm. Issue C is resolved for Lecture 1; future automation
is not thereby implemented.

### 9.2 A1 implementation and lecture

#### CF-04 — Behavioral fixtures do not automate validation

**Disposition:** Accepted; clarification of the existing Option A plan.
**Applies from:** A1 onward.

Acceptance fixtures supply behavioral examples derived from stories. Their
tests check the implementation against those examples; stakeholder agreement
that the stories express the intended system remains separate. Retain the
per-user-category validation and fresh sign-off after specification revision.
Signature checking must not be described as deciding stakeholder intent.

**Completion check:** the fixtures trace to stories, behavioral results and
validation records remain distinguishable, and the lecture explains how
passing fixture tests can coexist with a stakeholder rejecting the stories.

**A1 completion (2026-10-22):** every scenario of `v1/specs/scenarios.json`
carries `derived_from` and its story lists it; the behavioral evidence is
the loader's rows in `reports/conformance.md`, the validation decision is
`v1/reports/validation.md`; sabotage 9 in `v1/README.md` is the
scenarios-pass-and-the-officer-declines case, for the lecture to use.

**Source:** sections 3 and 4A;
[review section 8.1.D](../module-ase-principles/review-lecture-01-a0.md).

#### CF-05 — Partial-run evidence and report scope

**Disposition:** Proposed. **Target:** A1 reporting; carry forward to A2's
ledger generator if accepted. [Note from John: the notion of partial
evidence run this sounds useful in practice but it may over-complicate
key issues meant to be addressed in A2.]

Label deselected/partial runs explicitly in saved reports, not only terminal
output. Prevent their use as evidence that the full verification obligations
were met. Preserve the distinction between clause-linked results, overall
suite results, and the gate result. Counts of cited and uncited tests are an
optional reporting enhancement, not a requirement to eliminate uncited tests.

**Proposed completion check:** run a selected subset and inspect its saved
report; its scope must remain apparent when read without terminal output.
An aggregate consumer must not treat it as a successful full run.

**Disposition and A1 completion (2026-10-22):** accepted in its minimal
form only: the saved conformance report carries a scope line ("full run" or
"partial run (tests were deselected); not evidence for CONF"), and the trace
matrix a scope line of its own. Counts of cited and uncited tests are shown
in the report header; aggregate-consumer behavior is deferred to A2's ledger
generator.

**Source:** [review section 8.1.B and edit 8](../module-ase-principles/review-lecture-01-a0.md).

#### CF-06 — Audit and trace-input robustness

**Disposition:** Proposed. **Target:** A1, after defining its clause formats.
[Note from John: these concepts seem like interesting examples for
automated SQ checks. I propose that we accept these suggestions.]

Make duplicate identifiers, malformed clause declarations, and unsupported
verification methods visible audit/trace findings rather than silent
omissions. Define which contextual text is audited without being an
identified verification clause. Check completeness for the stated scope and
level, and distinguish assumptions from requirements. Review the seeded
gaps for genuine defects: the current REQ-2 requires equal field values, so
object identity must not be presented as an existing obligation it omits.

**Proposed completion check:** retain small malformed-input cases with
expected findings, document parser scope, and review the expected findings
for the planned six to eight audit gaps. This strengthens the planned audit;
it does not require a separate A0 parser rewrite before starting A1.

**Disposition and A1 completion (2026-10-22):** accepted. The clause reader
reports a malformed header, an unknown method, key, or pattern, a duplicate
identifier, and a missing reason as findings; `v1/tests/tooling/cases/`
holds a clean base and twelve cases with expected findings; the parser's
scope is on `v1/tooling/clause-reader.md`. The seeded gaps were reviewed:
seven, each a genuine defect; the REQ-2 identity question appears only as the
ad-hoc audit's rejected over-report (`v1/reports/audit-02-agent.md`, item
10). The skill's own run on the drafts found four unseeded defects of the
build's setup, which is what a known-violation set is for.

**Source:** [review sections 8.1.B and E](../module-ase-principles/review-lecture-01-a0.md).

#### CF-07 — Reproducible evidence identity

**Disposition:** Proposed implementation refinement of the existing provenance
requirement. **Target:** A1 records and A2 automation.
[Note from John: these notions seem important in practice (related to 
HAMR's notion of attestation?) but I worry that this may over-complicate
key issues meant to be demostrated.  I need a deeper explanation of
what accepting this proposal would look like in practice.]

Record the checked source revision and relevant working-tree state, the
tests/verifier/configuration used, and retained run outputs. Do not infer a
Git tag from the snapshot directory name `v0/`. If the replay mechanism in
section 6 creates tags, verify their existence before citing them. Provenance
identifies a claim; it is not a substitute for retained execution evidence.

**Proposed completion check:** a reviewer can identify the actual inputs and
find the corresponding outputs for a checkpoint without relying on an agent
completion message. Document how pre-commit evidence identifies the checked
state without requiring a report to contain its own eventual commit hash.

**Disposition and A1 completion (2026-10-22):** accepted as a hand
convention for A1, with the mechanism deferred to A2. In practice: the gate
prints a header naming the date, HEAD, the number of changed or untracked
paths, and the versions of every tool; the dev-log entry of each commit
copies it; the ledger's provenance column cites the entry. For A2, the
checked working tree is identified before the commit exists by its tree
hash (`git write-tree` on a temporary index), which the generated ledger
records and later compares. The explanation is section 9.5 of the A1 plan.

**Source:** [review section 8.2 and edits 9–10](../module-ase-principles/review-lecture-01-a0.md).

### 9.3 A2 implementation and lecture

#### CF-08 — Aggregate results in the generated ledger

**Disposition:** Accepted; follows CF-01 and the existing requirement to use
actual run results. **Applies from:** A2.

The ledger generator must consider the required suite/gate results and
human evidence, not merely green clause rows. An uncited test failure can
leave all clause-linked rows green while pytest and the overall gate fail.
The generator must not establish aggregate CONF from that clause table.

**Completion check:** demonstrate an uncited failing test with otherwise
passing clause-linked evidence. Show the failed suite/gate result and the
resulting ledger finding. Also demonstrate that missing required walkthrough
or validation evidence is not supplied by an automated passing result.

**Source:** [review section 8.1.B, consequence 3](../module-ase-principles/review-lecture-01-a0.md).

#### CF-09 — Ledger dependencies and status transitions

**Disposition:** Accepted semantics; representation remains an open question
under CF-12. **Applies from:** A2 automation.

Account for relevant specifications, product code, tests, verifiers,
configuration, and environment when determining whether evidence remains
current. Use established, stale, and not-established meanings from section
2.1; explain whether a not-established finding is incomplete checking or a
current failure. Preserve historical evidence without presenting it as
current. Do not turn the simplified Lean dependency sketch into an exhaustive
implementation rule.

**Completion check:** exercise a code edit before rerun, a fresh failing run,
a successful renewal, and a test/verifier change without a product-code
change. Show the checked artifact identities and the reason for each status.
Keep this detailed demonstration out of the required Lecture 1 explanation.

**Source:** [review section 8.1.C](../module-ase-principles/review-lecture-01-a0.md)
and the [ledger sidebar](../module-ase-principles/lecture-notes/ledger-evolution-example.md).

#### CF-10 — Uncited tests and unofficial requirements

**Disposition:** Proposed addition to the already planned test-discipline
review. **Target:** A2.

Review the justification for expectations in uncited tests. They may protect
implementation choices, expose missing requirements, or impose unintended
product restrictions. Their existence does not decide the product contract;
do not force artificial citations as the remedy.

**Proposed completion check:** record the disposition of a representative
uncited implementation-detail test, explaining why its expectation should
remain, change, or become a proposed requirement. Use REQ-2's value equality
versus object identity as a possible discussion example, not a new identity
requirement.

**Source:** [review section 8.1.B, consequence 2](../module-ase-principles/review-lecture-01-a0.md).

#### CF-15 — Checkpoint-specific judgment obligations

**Disposition:** Accepted design and teaching commitment, 2026-10-22.
**Target:** A2 implementation and lecture; general workflow modeling in A3.
**Completion:** Lecture 1 qualification and first-commit teaching remark
added; A0 task/replay claims corrected. A2 implementation and worked
demonstration remain pending. A0 retains its existing rules, without a new
initial-construction phase or baseline-acceptance protocol.

Use section 2.8's distinction between recording work, reporting judgments,
and accepting work. Keep A0/A1's simple automated per-commit gate. In A2,
allow intermediate commits within a planned wave to contain incomplete work
or failing checks, while requiring designated judgments before wave
acceptance and integration. The ledger must accurately report established,
stale, and not-established judgments throughout; permission to record an
intermediate state does not establish its judgments.

**Completion checks:**

1. The build plan declares each acceptance checkpoint, the work and scope it
   covers, the required judgments and evidence, and who or what decides
   whether acceptance is permitted. Distinguish when checks run from when
   their results block advancement. Do not present scoped acceptance as
   whole-product conformance.
2. Explicitly revise WF-1 and the inherited obligations' *When* fields and
   failure behavior where necessary. Merely adding a wave gate leaves the
   old per-commit prohibitions in force. Keep reporting obligations in force
   during intermediate work; identify which other obligations continue to
   apply throughout development.
3. Demonstrate a new sanitizer specification and contracts, affected evidence
   becoming stale, a commit with failing tests before implementation, and
   an attempt at wave acceptance that is blocked. Then implement the behavior,
   obtain the required evidence and reviews, and demonstrate successful
   acceptance. Preserve the intermediate ledger findings rather than
   retroactively marking those states established.
4. Coordinate the implementation with CF-08's aggregate results and CF-09's
   status/dependency semantics, CF-12's representation and enforcement
   choices, and CF-14's tooling-construction lesson. Record whether the gate
   is prescribed or automatically enforced; do not imply an enforcement
   mechanism that has not been implemented.
5. Extend the [ledger-evolution sidebar](../module-ase-principles/lecture-notes/ledger-evolution-example.md)
   with this A2 sequence when building A2. Retain the existing A0 sequence
   under its stricter policy. Keep the detailed checkpoint lesson out of
   Lecture 1; A3 generalizes the two-level policy into a workflow graph.
6. Address the initial-build case explicitly: the revised policy must permit
   a specifications-only intermediate commit before implementation, tests,
   or checking infrastructure are complete, without claiming CONF is
   established. State how the process identifies an acceptance checkpoint
   and records its decision, and show that incomplete work cannot pass it.
   Check the human-review and reporting obligations as well as the automated
   gate; a successful script is not evidence of compliance with every rule.
   Use the A0 first-commit restriction to motivate testing the process rules
   against plausible development sequences, not just testing the product.

**Source:** section 2.8 and the Lecture 1 gate qualification and rule summary.
This item changes workflow policy, not product behavior, and does not require
a Lean model extension or a full workflow engine.

### 9.4 A3 and later change management

#### CF-11 — Limits of trace-based impact analysis

**Disposition:** Proposed workflow safeguard; the limitation itself follows
from optional citations. **Target:** A3 and later.

Treat the trace matrix's affected-test set as a starting set, not a complete
dependency analysis. Uncited tests can encode an old policy and require
revision. Retain a full-suite checkpoint rather than assuming that running
only tests linked to changed requirements is sufficient.

**Proposed completion check:** use a policy-change scenario with an affected
uncited test. The change report identifies the limitation and records the
full-suite result and the test expectation's disposition.

**Source:** [review section 8.1.B, consequence 1](../module-ase-principles/review-lecture-01-a0.md).

### 9.5 Open choices to resolve when relevant

#### CF-12 — Ledger representation and invalidation granularity

**Disposition:** Open question. **Resolve during:** A2 planning, before
implementing the generator.

Choose a small representation for current status, reason, evidence scope,
and relevant dependencies. Decide whether conservative whole-row invalidation
is sufficient or whether a limited finer-grained scheme is warranted. The
accepted semantics do not mandate a full dependency engine or a particular
JSON schema. Automated checks may verify records of human decisions but must
not invent those decisions. Distinguish prescribed gates from any actual
hook/CI enforcement selected for the build.

**Resolution check:** document the choice and its limits in the build plan,
then use CF-08 and CF-09's scenarios to test it. Do not defer the agreed
semantics merely because the representation is undecided.

**Source:** [review section 8.1.C and section 8.2](../module-ase-principles/review-lecture-01-a0.md).

#### CF-13 — Integer payload boundary

**Disposition:** Open question, not an authorized product change.
**Resolve when relevant:** A1 elicitation/domain-glossary work.

Does the domain's integer payload include Python `bool` values? A0's type
check accepts them. Record the domain decision explicitly; if exclusion is
desired, obtain approval for the corresponding requirement and behavior
change rather than silently altering the unchanged A1 baseline.

**Resolution check:** the elicitation/glossary record identifies the decision
or explicitly records that it remains open, with any proposed product change
handled separately.

**Resolved in A1 (2026-10-22):** the `/elicit` skill excluded the question
in all three evaluation runs as answered by the repository (REQ-0 says
integer) with the residue an implementation matter; the glossary entry
*payload* records that the specification does not constrain how a language
represents integers, and the elicitation record's "Not asked" section says
why. No product change.

**Source:** [review section 7, question 4](../module-ase-principles/review-lecture-01-a0.md).

### 9.6 Cross-version tooling construction and teaching

#### CF-14 — Build the process, reporting, and assurance tooling explicitly

**Disposition:** Accepted teaching commitment, 2026-10-22. **Applies to:** A1
and A2 implementation and lectures. **Completion:** Lecture 1 acknowledgment
added; future worked sessions and their evidence remain pending.

Do not present reports, gates, and ledger utilities as infrastructure that
appears automatically once product requirements have been written. Their
goals, report formats, status meanings, failure behavior, and organization
also require design and implementation. Teach students how to prompt an
agent to build or adapt this infrastructure, review its proposed design, and
check its behavior before relying on the evidence it produces.

- **A1:** introduce requirements for the audit and trace reports. Show how
  these requirements guide the agent's proposed artifact layout and
  implementation, including what is read from specifications, what is
  computed, and what still requires human judgment.
- **A2:** reserve a substantial worked teaching session for constructing the
  framework: report schemas, reusable utilities, gate integration, generated
  ledger, and tests of the checking machinery. Show the actual sequence from
  prompt to plan to implementation to deliberate-failure checks. Use the
  existing CF-01, CF-08, and CF-09 scenarios where appropriate; resolve
  proposed refinements such as CF-05 before treating them as required work.
- **Shared ownership:** explain how a team or company can share report
  formats, conventions, utility programs, and workflow integration, with a
  dedicated infrastructure team maintaining the common foundation and product
  teams supplying specifications, tests, and configuration. Include the need
  for versioned releases and controlled updates: a shared reporting defect
  can mislead multiple projects. This is an organizational model to explain,
  not a requirement to build a company-wide platform for the course.

**Completion check:** retain the prompts, approved tooling requirements,
implementation tasks, example reports, and checks that expose missing or
misleading evidence. Record which utilities are reused and which are newly
implemented. This adds a teaching focus to the existing progression, not
new product behavior or an authorization to implement every proposed
carry-forward item.

**Amended 2026-10-22:** no lecture time is allocated to building the
tooling (the instructor's decision). Instead each version carries a **tool
catalog**: in A1, `v1/tooling/README.md` (one table of every assurance tool
with its goal) and one page per tool with its goal, requirements, the prompt
that produced it (verbatim for a tool new in A1, guidance for one inherited
from A0, with the provenance chain below), review points, deliberate-failure
checks, how to adapt it to another project, and how to make it shared
infrastructure. A sidebar beside the Lecture 02 notes states the philosophy
and tabulates the tools. The A1 bullet above is met by the catalog; the
"shared ownership" paragraph is the sidebar's and the catalog pages' last
section.

**Provenance example for the worked teaching session:** A0's conformance
helpers were adapted from the tic-tac-toe demo, where an agent built custom
reporting utilities during the Spec Kit workflow. They were not installed
as standard Spec Kit conformance-reporting utilities. The recorded chain is:

1. The instructor's [seed development rules](../module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/demo-seeds/ASE-seed-development-rules.md)
   supplied reporting goals, carried into Principle V of the project's
   constitution.
2. Planning decision [R7](../module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/specs/001-five-in-a-row/research.md#r7-conformance-evidence-and-reports-constitution-principles-i-and-v)
   selected requirement markers, a pytest plugin, and a generated conformance
   report with explicit missing-evidence results.
3. [Tasks T004–T006](../module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/specs/001-five-in-a-row/tasks.md#evidence-tooling-constitution-principles-i-and-v-researchmd-r7)
   specified the clause reader, its tests, and the report-writing plugin.
4. Public commit `4d6a2cd`, dated 2026-10-08, introduced both helpers during
   the foundational implementation phase. The [session transcript](../module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/specs/001-five-in-a-row/transcript/session-transcript.md)
   records that phase under `/speckit-implement`; its original commit hash
   `2ff1e1c` maps to the public hash in the demo README.
5. [A0's development log, entry 2](../module-ase-principles/demos/running-example-message-guard/v0/reports/dev-log.md)
   records adapting the plugin and adding the gate command. The A0 files
   first appear in public commit `4a9d077`, dated 2026-10-20.

Spec Kit supplied the planning/task/implementation workflow; the project's
goals and the agent's design work supplied this particular reporting
mechanism. Do not confuse Spec Kit's cross-artifact analysis report with the
pytest-generated conformance evidence report.

**Teaching introduction:** [Lecture 1, Process, Reporting, and Assurance Tooling](../module-ase-principles/lecture-notes/lecture-01-intent-specifications-realizations-and-judgments.md#process-reporting-and-assurance-tooling).
