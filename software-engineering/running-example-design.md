# Running Example for Agentic Software Engineering: Design

> Status: design draft, 2026-10-18. Responds to the brief in
> `running-example.md`. The one open decision is the progression
> (section 3); nothing in this document is built yet. Vocabulary follows
> `../glossary.md` where the glossary has a term and proposes additions
> (section 5) where it does not.

## 0. What this document settles

The brief asks for a running example that teaches agentic software
engineering as a discipline: human intent, specifications, realizations, the
judgments that connect them, and a development process whose state a person or
an auditor can read without reading the code. This document settles:

1. the example itself (section 1) and the pool of capabilities it can grow
   through (1.1);
2. the conceptual core every version carries, whatever the order of
   introduction: five development-state judgments, the artifact categories,
   rule categories with a budget, and the mechanisms that deepen version by
   version (section 2);
3. four candidate progressions, each a sequence of versions with the
   capability, specification forms, judgments, and process artifacts each
   version introduces, with a comparison and a recommendation (section 3);
4. a canonical list of specification forms with, for each, when it is
   appropriate, how conformance is shown, and what it must agree with
   (section 4);
5. the vocabulary changes needed in the glossary and the alignment with the
   Lean model in `AgenticDev` (section 5);
6. where the example lives and what existing code it reuses (section 6);
7. coverage checklists showing that every glossary term and every form appears
   in every progression (section 7).

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
  and checkable with a one-screen test.
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
existence, which is what makes it useful as a teaching step.

| ID | Capability | What it forces into the specifications |
|---|---|---|
| F1 | `filter`: drop Critical; pass Restricted and Public unchanged; no input, no output | requirements; a test suite; a definition of *message* |
| F2 | `sanitize`: clamp Restricted payload to [0, 100], pass Public; pipeline = filter then sanitize | architecture (stages, order, purity); an integration contract (sanitize assumes no Critical input); allocation of requirements to stages; a plan, because the work is now several tasks |
| F3 | audit log: every drop and every change is written as a record | a second output and a second data format; the auditor's user story; a sequence chart with something to show |
| F4 | policy change: out-of-range Restricted payloads are dropped, not clamped (or a fourth level is added) | a change request and a change report; impact analysis; staleness in the ledger |
| F5 | sessions: OPEN, DATA*, CLOSE; DATA outside a session is dropped | a state machine; a sequence chart; trace tests; generation from the transition table |
| F6 | standard message format: messages arrive as JSON (or in an IDL) and are validated at ingress | a schema or IDL; generated types and a validator; well-formedness of the schema itself |
| F7 | configurable policy: which levels are dropped is a table the security officer edits | a policy table as a data specification; a table-driven `filter`; configuration validation |
| F8 | parallel stages with a merge: two independent checks on the same message | a non-linear architecture; ordering and merge semantics |

F1 and F2 are the HAMR system. F3 to F8 are extensions; each progression says
which it uses.

## 2. The conceptual core carried by every version

### 2.1 Five development-state judgments

A *development-state judgment* is a claim about the current artifacts whose
truth is tracked commit by commit. These five are the rows of the ledger in
every version. Four are the Lean model's judgments (`specOK`, `realOK`,
`verified`, `validated`) under course names; the fifth is the brief's
"overarching" traceability, given its own row because it is mechanically
checkable and because the other four are only decidable *per clause* when it
holds.

| ID | Judgment | Question it answers | Established by | Evidence recorded in the ledger | Goes stale when |
|---|---|---|---|---|---|
| **SQ** | Specification quality | Is each specification well-formed, unambiguous, internally consistent, complete for its level, and consistent with its companion specifications? | an audit: an agent applies the SQ rules and a person rules on each gap; later, scripts for the syntactic parts (identifiers unique, EARS pattern, glossary terms) | the audit report with zero open gaps; script exit codes | any specification changes |
| **RQ** | Realization quality | Does the code lint, type-check, pass its own tests, meet the coverage target, and respect the architecture constraints? | algorithmic: `ruff`, `mypy`, `pytest`, the architecture test | the commands and their exit codes | code changes |
| **CONF** | Conformance (verified) | Does the realization satisfy every clause of every specification? | tests that cite clauses; clause coverage; later contracts, trace tests, schema validation | the conformance report: clause, tests, status | a specification or the code changes |
| **VAL** | Validated | Do the specifications describe what the customer intends? | a person walks the user stories and their example messages against the running system and signs off | a sign-off line: who, when, which specification version | the intent or a specification changes |
| **TR** | Traceable | Does every clause carry an identifier, and does every link resolve in both directions (story to requirement to test to task)? | a script over the identifiers | the trace matrix with no dangling links | any artifact changes |

Two kinds of *gate* follow from the "established by" column and both need a
name. An **algorithmic gate** is a program whose exit code decides (RQ, CONF,
TR, and the syntactic part of SQ). An **approval gate** is a recorded human
decision (VAL, the judgment part of SQ, the sign-off that closes a wave). This
widens the glossary's current rule that a person cannot be a gate; the Lean
model's `establish` step with a human proof premise is exactly an approval
gate.

### 2.2 Artifact categories

The essay's draft section "Different Categories of Artifacts" lists intent,
specifications, realization, development rules, plans, and reports. The
example instantiates each category from its first version.

| Category | Instance in the example | Role in the judgments |
|---|---|---|
| Intent | `INTENT.md`: the customer's paragraph | what VAL compares against; not a specification |
| Specifications | `specs/*.md`, every clause with an identifier | the subject of SQ; the reference for CONF and VAL |
| Realization | `guard/*.py`, `tests/*.py` | the subject of RQ; checked by CONF |
| Development rules (governance) | `process/rules.md`, split by category as it grows | say how each judgment is established and when it must hold |
| Plan | `plans/NNN-*.md` | tasks grouped into waves, a gate at the end of each wave; each task cites the clauses it realizes |
| Reports | `reports/dev-log.md`, `reports/ledger.md`, `reports/trace-matrix.md`, gap lists, change reports | the development state as a person reads it |

### 2.3 Rules filed by judgment, with a budget

Rule identifiers carry the category, so the categories are visible from the
first rule: **SQ-**, **RQ-**, **CONF-**, **VAL-**, **TR-**, and two categories
for the process itself, **WF-** (workflow: steps, commits, waves, gates,
staleness) and **RPT-** (the forms reports take). Identifiers are never
renumbered. Every example inside a rule comes from this system.

The budget: no version adds more than **eight rules**. The first version ships
at most eight, one per category, in a single file of about eighty lines. After
the core versions the set is about 28 rules in at most five short files,
against 41 rules in 814 lines at the game demo's starting tag.

### 2.4 Mechanisms that deepen across versions

The five judgments do not change; the mechanisms that establish them get
stronger.

| Judgment | First form | Later forms |
|---|---|---|
| SQ | a person reads three clauses | audit rules and a gap list; scripts for EARS form and glossary use; per-kind checks for architecture, data formats, state machines |
| RQ | `ruff` and `pytest` | add `mypy`; add the architecture test; add branch coverage |
| CONF | `@pytest.mark.req` markers and the generated conformance report | story tests over a fixture file; clause coverage; contracts; trace tests for a state machine; schema validation at ingress |
| VAL | one sign-off line | a walkthrough per user class; a walkthrough per change |
| TR | markers resolve to clause identifiers | `tools/trace.py` builds the matrix story to requirement to test to task; impact analysis reads the matrix |
| the ledger | a hand-written table at a named commit | `tools/ledger.py` generates it from exit codes, the reports, and a sign-off file; stale rows are kept and marked |

## 3. Progression options

Each option is a sequence of versions. A version row names the capability
added (from 1.1), the specification forms introduced, the judgments and
mechanisms introduced, and the process artifacts and rules introduced. No
mapping to lectures is made here. Adjacent versions marked *mergeable* can be
combined to coarsen an option.

### Option A. Spiral: every judgment once, minimally, then deepen

The first version shows all five ledger rows on a one-function system; each
later version deepens one or two of them. Specifications precede code from the
start.

| Version | Capability | Specification forms introduced | Judgments and mechanisms introduced | Process artifacts and rules introduced |
|---|---|---|---|---|
| A0 | F1 | intent statement; plain requirements with identifiers (REQ-0 message, REQ-1 to REQ-4); test suite; technology (`pyproject.toml`) | all five rows, minimal: SQ by reading; RQ `ruff` and `pytest`; CONF markers and the conformance report; VAL one sign-off; TR markers resolve | `process/rules.md` with 8 rules, one per category; hand-written ledger; dev log |
| A1 | F1 (unchanged) | concept of operations (scope; user classes; user stories with example messages); glossary; requirements rewritten in EARS; acceptance fixtures | SQ audit (consistency, EARS form, glossary discipline, story-to-requirement alignment) on six to eight seeded gaps; VAL walkthrough per user class; TR trace-matrix tool; CONF story tests | gap-list form; trace matrix report; 7 rules; first skill, `/audit-spec` |
| A2 | F2 | architecture (stages, order, purity, allocation, integration contract); data format (ad hoc rules); interface contracts (pre- and postcondition per stage); plan | RQ `mypy`, architecture test, coverage; CONF clause coverage; generated ledger | plan with tasks, waves, gates; dev log per task; 8 rules (WF-2 to WF-5, RQ-2 to RQ-4, CONF-3); `/ledger` skill |
| A3 | F4 | change request and change report; workflow graph (the process as a state machine) | staleness shown in the ledger; impact analysis from the trace matrix | branch per change; 4 rules (WF-6, WF-7, RPT-3, RPT-4) |
| A4 | F5 | state machine (table and diagram); message sequence chart | trace tests; table-driven or generated session module | none |
| A5 | F6 | schema or IDL for the message | schema validation at ingress; the generator as the conformance argument | none |
| A6 (optional) | F7 or F8 | policy table as data; non-linear architecture | configuration validation; merge-semantics tests | none |

Mergeable: A4 with A5. **Pros:** the whole picture is visible from A0, so each
later version is "the same five rows, done better"; specifications precede code
throughout. **Cons:** A0 carries four forms and five judgments at once, even
though each is tiny; the concept of operations arrives second, after the
requirements.

### Option B. Artifact flow: specifications first, code only once they are audited

Versions follow the order in which a specification-driven process produces
artifacts. The first two versions contain no code; the judgments that exist
before code (SQ, VAL, TR) are shown on specifications alone.

| Version | Capability | Specification forms introduced | Judgments and mechanisms introduced | Process artifacts and rules introduced |
|---|---|---|---|---|
| B0 | none (no code) | intent statement; concept of operations (scope; user classes; user stories with example messages); glossary | VAL walkthrough of the stories against the intent; SQ for the concept of operations (implementation-independent, observable, terms defined); TR story identifiers | `process/rules.md` with 4 rules (SQ-1, SQ-2, VAL-1, TR-1); ledger with three rows; dev log |
| B1 | none | EARS requirements; acceptance fixtures as data; verification obligations | SQ audit of the requirements (consistency, EARS form, alignment) on seeded gaps; TR trace matrix story to requirement | gap-list form; 4 rules; `/audit-spec` skill |
| B2 | F1 | test suite; technology; interface contract for `filter` | RQ `ruff` and `pytest`; CONF markers, story tests, conformance report; the ledger reaches five rows | 5 rules (RQ-1, CONF-1, CONF-2, WF-1, RPT-1); generated ledger |
| B3 | F2 | architecture; data format; plan | RQ `mypy`, architecture test, coverage; CONF clause coverage | plan with tasks, waves, gates; dev log per task; 6 rules |
| B4 | F4 | change request and report; workflow graph | staleness; impact analysis | 4 rules |
| B5 | F5 | state machine; sequence chart | trace tests; generation | none |
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
| C0 | F1 | technology only (`pyproject.toml`); no specification | RQ: `ruff` and `pytest`; the tests cite nothing | one rule (RQ-1); no ledger: this is vibe coding with tests |
| C1 | F1 | plain requirements with identifiers; verification obligations | CONF and TR: markers; the conformance report with its "no evidence" rows | first ledger (RQ, CONF, TR); 3 rules (CONF-1, TR-1, WF-1 specification before change) |
| C2 | F1 | EARS requirements; glossary | SQ: audit rules, gap list, well-formedness; seeded gaps | ledger with four rows; 3 rules (SQ-1 to SQ-3); `/audit-spec` skill |
| C3 | F1 | intent statement; concept of operations (user classes, stories); acceptance fixtures | VAL: walkthrough per user class, sign-off; story tests | ledger with five rows; trace-matrix tool; 3 rules (VAL-1, VAL-2, SQ-4 alignment) |
| C4 | F2 | architecture; data format; interface contracts; plan | RQ deepened (`mypy`, architecture test, coverage); CONF clause coverage; generated ledger | plan with tasks, waves, gates; dev log per task; 6 rules |
| C5 | F4 | change request and report; workflow graph | staleness; impact analysis | 4 rules |
| C6 | F5 | state machine; sequence chart | trace tests; generation | none |
| C7 | F6 | schema or IDL | schema validation | none |

Mergeable: C1 with C2; C6 with C7. **Pros:** the course's central contrast is
literal, and each version closes one named gap; the smallest first step of any
option. **Cons:** code precedes specification for three versions, against the
habit the course wants to form (it has to be framed as retrofitting discipline
onto an existing system); intent and the concept of operations arrive late.

### Option D. Capability-driven: each version is a customer ask

Every version adds a capability and only the forms that capability needs.
Architecture and planning come early because the second stage needs them; the
concept of operations comes when the human stakeholders have to be named.

| Version | Capability | Specification forms introduced | Judgments and mechanisms introduced | Process artifacts and rules introduced |
|---|---|---|---|---|
| D0 | F1 | intent statement; plain requirements with identifiers; test suite; technology | RQ `ruff` and `pytest`; CONF markers and conformance report; TR markers resolve | 5 rules; hand-written ledger with three rows; dev log |
| D1 | F2 | architecture; interface and integration contracts; data format; plan | RQ architecture test and `mypy`; CONF per stage and clause coverage; generated ledger | plan with tasks, waves, gates; dev log per task; 7 rules (WF-2 to WF-5 among them) |
| D2 | F3 | concept of operations (user classes including the auditor; stories); glossary; EARS; acceptance fixtures; log-record data format | SQ audit on seeded gaps; VAL walkthrough; TR trace matrix; the ledger reaches five rows | gap-list form; 7 rules (SQ-1 to SQ-5, VAL-1, VAL-2); `/audit-spec` and `/ledger` skills |
| D3 | F4 | change request and report; workflow graph | staleness; impact analysis | 4 rules (WF-6, WF-7, RPT-3, RPT-4) |
| D4 | F5 | state machine; sequence chart (with the log as a second lifeline) | trace tests; generation | none |
| D5 | F6 | schema or IDL | schema validation; generator | none |
| D6 (optional) | F7 | policy table as data | configuration validation; table-driven filter | none |

Mergeable: D4 with D5. **Pros:** every form has a visible motivating need; the
plan and its waves arrive at the first multi-task change, which is when they
are first felt; the audit log (F3) gives the concept of operations real user
classes and the sequence chart a second participant. **Cons:** SQ and VAL
arrive after architecture and planning, so the first two versions run on
unaudited, unvalidated specifications, which has to be called out.

### 3.1 Comparison

| | A Spiral | B Artifact flow | C Judgment ladder | D Capability-driven |
|---|---|---|---|---|
| First code | v0 | v2 | v0 | v0 |
| First concept of operations and VAL | v1 | v0 | v3 | v2 |
| All five ledger rows by | v0 | v2 | v3 | v2 |
| Plan, waves, gates by | v2 | v3 | v4 | v1 |
| Versions to reach the change (F4) | 4 | 5 | 6 | 4 |
| The story the sequence tells | the same five rows, done better each time | specifications are judged before code exists | vibe coding to engineering, one gap at a time | each customer ask pulls in the form it needs |
| Main risk | v0 is dense | an abstract start | specification after code | unaudited specifications early |

### 3.2 Density per version

The budget in 2.3 caps rules at eight per version. Forms are harder to cap,
because some are trivial (technology is one file). This table counts both so
the dense versions are visible; each dense version has a natural split.

| Option | Versions and (forms / rules) | Dense versions and their split |
|---|---|---|
| A | A0 (4/8), A1 (4/7), A2 (4/8), A3 (2/4), A4 (2/0), A5 (1/0) | A0 into intent + requirements + tests (RQ, CONF, TR) then SQ + VAL + ledger; A2 into architecture + contracts then data + plan |
| B | B0 (3/4), B1 (3/4), B2 (3/5), B3 (3/6), B4 (2/4), B5 (2/0), B6 (1/0) | none |
| C | C0 (1/1), C1 (2/3), C2 (2/3), C3 (3/3), C4 (4/6), C5 (2/4), C6 (2/0), C7 (1/0) | C4 into architecture + contracts then data + plan |
| D | D0 (4/5), D1 (4/7), D2 (5/7), D3 (2/4), D4 (2/0), D5 (1/0) | D1 as for A2; D2 into concept of operations + glossary then EARS + fixtures + log format |

### 3.3 Recommendation

**Option A with C0 as a prelude.** Keep the spiral, and place the vibe-coding
snapshot (code, tests, no specification, no ledger) *before* A0 as the contrast
the material opens on: the same `filter`, the same tests, and no way to answer
"what did the customer ask for, and how do you know this does it?". A0 then
answers the question with the five rows. This keeps specification-before-code
as the habit from A0 on, makes the central contrast literal, and leaves the
concept of operations one version away. If A0 is judged too dense, the split in
3.2 turns it into D0 followed by a half step.

Whichever option is chosen, each version should end with a **"break it"**
demonstration: one sabotage per judgment introduced in that version, showing
exactly that ledger row turning red and which verifier catches it (a
contradictory requirement for SQ; a lint error for RQ; `filter` passing a
Critical message for CONF; a specification that passes everything but is not
what the customer meant for VAL; a removed marker for TR).

## 4. Canonical list of specification forms

For each form: what it constrains, when it is the right form, how conformance
of a realization is shown and what a pass does not show, what the form must
agree with, how it maps to the catalog in `../specification-kinds.md`, and
which capability from 1.1 first needs it. The three questions the brief asks
of every form are columns 4, 5, and 6.

| # | Form | Constrains | Appropriate when | Conformance mechanism (verifier) | Must agree with | Catalog today | First needed by |
|---|---|---|---|---|---|---|---|
| 1 | Intent statement | purpose, in the customer's words | always; it is what VAL checks against | none: it is the reference, not a specification | nothing above it | not present | any version |
| 2 | Concept of operations (scope, user classes, user stories) | who the users are, what they observe, the scenarios | any system with users; the first document | validation walkthrough (person); acceptance tests derived from the stories' examples (algorithmic) | governs everything; every requirement traces to a story | concept of operations | any version; F3 gives it an auditor |
| 3 | Glossary / domain model | vocabulary; later, entities and attributes | always; it grows into the data model | SQ audit: one definition per term, used consistently (a script for capitalized terms) | every specification uses only its terms; the data format refines it | listed as "not a kind"; promote | with the concept of operations |
| 4 | Behavioral requirements (EARS) | input/output and event behavior | observable functional behavior | unit tests citing clauses; clause coverage (algorithmic); a pass does not show the tests claim the right thing | traces to stories; allocated to a stage; refined by contracts | behavioral requirements | F1 |
| 5 | Acceptance scenarios / fixtures | concrete input-to-output examples | behavior that can be stated by example; portable across realizations | parametrized tests over the fixture file; a pass says nothing about uncovered inputs | derived from stories; agrees with the requirements | fixtures; example session | F1 |
| 6 | Data format (rules, then schema or IDL) | the form of stored or exchanged data | any persisted or exchanged artifact | a validator or generated parser (algorithmic); well-formedness of the schema itself | agrees with the glossary; cited by requirements and contracts | data format (generation new) | F2 ad hoc; F3 the log record; F6 the schema |
| 7 | Architecture (parts, order, dependency constraints, allocation) | structure and boundaries | two or more parts | the architecture test on imports (algorithmic); the allocation table, read (person or agent); a pass does not show the boundaries are right | every requirement allocated; integration contracts across each boundary | architecture ("named only") | F2 |
| 8 | Interface contract (signature, pre- and postcondition; integration assume/guarantee) | per-operation behavior; assumptions between parts | any API boundary | type checker; unit and property tests (algorithmic); later, runtime assertions | refines the allocated requirements; one part's guarantee is the next part's assumption | interface contract (integration part new) | F2 |
| 9 | State machine (protocol) | ordering and modes | stateful behavior; protocols | trace tests; a table-driven realization or generation (then the question is whether the generator is right) | transitions trace to requirements; agrees with the sequence charts | a form of interaction flow; make it a kind | F5 |
| 10 | Message sequence chart | interactions among parts over time | multi-part scenarios | scripted end-to-end tests | agrees with the architecture and the state machine | not present | F3 or F5 |
| 11 | Verification obligations / trace matrix | what must be tested, per clause | once requirements exist | the generated matrix; "no evidence" rows (algorithmic) | maps both ways between requirements and tests | verification obligations | F1 |
| 12 | Test suite | executable claims | always | it is the verifier; sabotage shows that it can fail | each test cites a clause | test suite | F1 |
| 13 | Technology and platform | languages, tools, versions | always | `pyproject.toml` and lock files (algorithmic); provenance by judgment | the gate commands name these tools | technology and platform | F1 |
| 14 | Development rules (governance, by category) | how each judgment is established and when it must hold | always | the repository history, ledger, and dev log read against the rules | the categories mirror the judgments | development process | any version |
| 15 | Plan (tasks, waves, gates) | the decomposition and ordering of one build | any change larger than one task | task status; the ledger at the end of each wave | tasks cite clauses; waves end at gates | listed as "not a kind" (DEV-9); make it explicit | F2 |
| 16 | Workflow graph (the process as a state machine) | the allowed sequences of steps | multi-step or multi-agent work | `git log` read against it; hooks and monitors | its edges are the gates | the essay's sixth example; not in the catalog | F4 |
| 17 | Change request and change report | what a change touches and what it re-established | any change to a governed artifact | the report read against the trace matrix and the ledger diff | lists every affected identifier; names the ledger rows re-established | not present | F4 |

## 5. Vocabulary alignment

### 5.1 Glossary additions proposed

Each entry below would be added to `../glossary.md`; the Lean name is given
where the model in `AgenticDev` has one.

- **intent** (`HI`): what the customer wants, in the customer's words; the
  reference for validation; not a specification.
- **artifact**: anything under version control that a judgment is about:
  intent, a specification, the realization, a rule file, a plan, a report.
- **development state** (`DevState`): the artifacts at a commit together with
  the ledger.
- **development-state judgment** (`Judgment`): one of the five claims in 2.1,
  tracked commit by commit. Distinct from *judgment clause*, which stays as
  defined.
- **ledger** (`Ledger`): the table that states, at a named commit, which
  judgments hold, on what evidence, and which are stale.
- **establish; stale** (`Step.establish`; `Ledger.invalidate`): a judgment is
  *established* when its evidence is produced and recorded; it goes *stale*
  when an artifact it depends on changes, and stays stale until re-established.
- **development log**: the append-only record of what each task or commit did
  and which judgments it touched.
- **traceability**: the links between identified items in different artifacts,
  in named forms: derivation (story to requirement), allocation (requirement to
  part), verification (requirement to test), realization (task to commit),
  change (change request to affected identifiers).
- **plan; task; wave**: a plan decomposes one build into tasks; tasks are
  grouped into waves; each wave ends at a gate.
- **gate**: widened to two kinds, *algorithmic* (a program's exit code) and
  *approval* (a recorded human decision).
- **realization quality**: the judgment that the realization lints,
  type-checks, passes its own tests, and respects the architecture constraints.
- **governance**: the development rules, filed by the judgment they maintain.
- **change request; change report**: the record that opens a change and the
  record that closes it.
- **assurance**: the argument, from the ledger and the reports, that the
  judgments hold.

### 5.2 Conflicts found between the glossary, the catalog, the essay, and the brief

| Conflict | Recommendation |
|---|---|
| The glossary says a person or an agent cannot be a gate; the brief wants human audits as gates | widen *gate* to two kinds, algorithmic and approval (2.1) |
| *judgment clause* (glossary) against *development state judgement* (brief); the spelling also differs | keep the "judgment" spelling throughout; say *development-state judgment* for the five rows; *judgment clause* stays as is |
| the glossary is "not a kind" (catalog) against "an important specification, a simple domain model" (brief) | promote it to a kind; it is cross-cutting and audited |
| validation applies to the concept of operations only (glossary) against "specifications conform to intent" (brief, Lean) | adopt the Lean reading; the concept of operations is where validation is *performed*, not the only specification it covers |
| *audit* means specification quality only (glossary) against audits of conformance and of ledgers (essay, brief) | keep *audit* for the activity of reading artifacts against rules, whatever the judgment; the judgment's name says what is audited |
| realization quality has no home among AUD, DEV, VER, RPT | the RQ category gives it one |
| five specification-quality properties (glossary) against three (brief) | SQ covers unambiguous, internally consistent, externally consistent, well-formed (syntactic), and complete; *traceable* moves to TR |
| *filter* means transform in the HAMR example and drop in ordinary usage | decided: `filter` drops, `sanitize` transforms (section 1) |
| the essay's "test vectors as specifications" is still a TODO | forms 5, 11, and 12 in section 4 stand in for it |

### 5.3 Where the Lean model and the example meet

The example instantiates the Lean model directly: `INTENT.md` is `HI`;
`specs/` is `S`; `guard/` and `tests/` are `R`; the four Lean judgments are
SQ, RQ, CONF, VAL; the ledger is `Ledger`; a task's commit is a `Step`; the
rule "a specification change invalidates CONF, VAL, SQ, TR; a code change
invalidates RQ, CONF, TR" is `Judgment.dependsOn` written out. Suggested
evolutions of the model, none required by the course:

1. a fifth judgment, `traced`, depending on `s` and `r`;
2. clause-level granularity, with `S` a set of identified clauses so that
   `dependsOn` and invalidation work per clause, as the trace matrix does;
3. waves and gates: `StepsWithin allowed` already describes the shape of a
   wave; a gate is a `Policy` required at the wave's last state;
4. ledger rows that record provenance (which verifier, which specification
   version, when) and keep a *stale* status rather than being deleted, as the
   generated `ledger.md` does.

## 6. Repository layout and reuse

- **Location:** `module-software-engineering/demos/running-example-message-guard/`,
  one snapshot directory per version (`v0/`, `v1/`, and so on), plus a
  `build-history.sh` that replays the snapshots into a tagged git repository so
  the dev log has a real `git log` behind it. Lecture notes link to a fixed
  snapshot; students can `diff -r v1 v2`.
- **Reuse:** adapt `tests/conftest.py` and `tests/conformance.py` from
  `module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/`
  (identifier patterns for `REQ-`, `US-`, `ARCH-`, `DATA-`, `IF-`; status
  vocabulary unchanged); adapt its `tests/test_architecture.py` to check stage
  purity and order; copy its `pyproject.toml` marker configuration
  (`--strict-markers`).
- **Licensing:** `specs/`, `process/`, `reports/`, and `INTENT.md` are CC BY
  4.0 prose; `guard/`, `tests/`, `tools/`, and configuration are MIT, per
  `LICENSING.md`.
- **Documents to update when the first version is built:**
  `specification-kinds.md` (the new kinds and a "first needed by" column),
  `glossary.md` (the additions in 5.1), the `CLAUDE.md` demos index, the
  module README, and the brief `running-example.md` (which already points
  here).

## 7. Coverage checklists

### 7.1 Glossary terms, current and proposed, by the first version that illustrates each

| Term | A | B | C | D | Illustrated by |
|---|---|---|---|---|---|
| audit | A1 | B0 | C2 | D2 | the SQ audit and its gap list |
| concept of operations | A1 | B0 | C3 | D2 | `specs/conops.md` |
| conformance | A0 | B2 | C1 | D0 | the CONF row and the conformance report |
| executable specification | A0 | B2 | C1 | D0 | tests that cite clauses; fixtures from A1 / B1 / C3 / D2 |
| family of specifications | A1 | B1 | C2 | D1 | several `specs/*.md` audited together |
| gate (algorithmic) | A0 | B2 | C1 | D0 | the gate command in WF-1 |
| gate (approval) | A2 | B3 | C4 | D1 | the sign-off that closes a wave |
| invariant | A0, A2 | B2, B3 | C1, C4 | D0, D1 | per commit: the gate passes; per wave: the ledger is green |
| mechanical clause; judgment clause | A0 | B2 | C1 | D0 | the ledger's algorithmic rows against its human rows; "manual" status in the conformance report |
| realization | A0 | B2 | C0 | D0 | `guard/` |
| specification | A0 | B0 | C1 | D0 | `specs/requirements.md` or `specs/conops.md` |
| validation | A0 | B0 | C3 | D2 | the VAL row and the sign-off |
| verification | A0 | B2 | C1 | D0 | the test suite under the CONF row |
| verifier (human, agent, algorithmic) | A0 | B2 | C1 | D0 | the "established by" column of the ledger |
| intent | A0 | B0 | C3 | D0 | `INTENT.md` |
| artifact | A0 | B0 | C1 | D0 | the categories in `process/rules.md` |
| development state; ledger | A0 | B0 | C1 | D0 | `reports/ledger.md` |
| development-state judgment (all five) | A0 | B2 | C3 | D2 | the five ledger rows; three rows from B0 / C1 / D0 |
| establish; stale | A2 | B3 | C4 | D1 | rule WF-5 and the regenerated ledger; shown under change in A3 / B4 / C5 / D3 |
| development log | A0 | B0 | C1 | D0 | `reports/dev-log.md` |
| traceability | A0 | B0 | C1 | D0 | markers; the trace matrix from A1 / B1 / C3 / D2 |
| plan; task; wave | A2 | B3 | C4 | D1 | `plans/001-*.md` |
| realization quality | A0 | B2 | C0 | D0 | the RQ row |
| governance | A0 | B0 | C0 | D0 | `process/rules.md` |
| change request; change report | A3 | B4 | C5 | D3 | `reports/CR-001.md` |
| assurance | A0 | B0 | C1 | D0 | the ledger read as an argument |

### 7.2 Specification forms by the first version that introduces each

| Form (section 4) | A | B | C | D |
|---|---|---|---|---|
| 1 intent statement | A0 | B0 | C3 | D0 |
| 2 concept of operations | A1 | B0 | C3 | D2 |
| 3 glossary / domain model | A1 | B0 | C2 | D2 |
| 4 behavioral requirements (EARS) | A1 (plain from A0) | B1 | C2 (plain from C1) | D2 (plain from D0) |
| 5 acceptance scenarios / fixtures | A1 | B1 | C3 | D2 |
| 6 data format | A2 | B3 | C4 | D1 |
| 7 architecture | A2 | B3 | C4 | D1 |
| 8 interface contract | A2 | B2 | C4 | D1 |
| 9 state machine | A4 | B5 | C6 | D4 |
| 10 message sequence chart | A4 | B5 | C6 | D4 |
| 11 verification obligations / trace matrix | A0 (matrix from A1) | B1 | C1 | D0 (matrix from D2) |
| 12 test suite | A0 | B2 | C0 | D0 |
| 13 technology and platform | A0 | B2 | C0 | D0 |
| 14 development rules | A0 | B0 | C0 | D0 |
| 15 plan | A2 | B3 | C4 | D1 |
| 16 workflow graph | A3 | B4 | C5 | D3 |
| 17 change request and report | A3 | B4 | C5 | D3 |

## 8. Open decisions

1. **Which progression** (section 3), and whether to use the C0 prelude.
2. **Whether to adopt the glossary additions in 5.1 and the resolutions in
   5.2**, in particular the widened *gate* and the fifth judgment TR.
3. **Whether the audit log (F3) is part of the core**, which decides whether
   the concept of operations has an auditor user class with something to
   observe.
4. **Whether skills (`/audit-spec`, `/ledger`) enter with the version that
   introduces the mechanism or in a separate pass**, since skills are taught
   before this block.
