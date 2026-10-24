# Glossary of Agentic Software Engineering Course

Terms the course uses in a fixed sense. The definitions follow the
software-engineering module's Lecture 01 ("Four terms" in
`module-software-engineering/lecture-notes/lecture-01-specifications-realizations-and-conformance.md`),
the catalog of specification kinds (`specification-kinds.md`), and the design
of the running example (`software-engineering/running-example-design.md`),
whose sections the entries cite by number ("design 2.6"). Where a process
document (AUD, AUDCON, DEV, VER, RPT) defines a rule, the process document is
normative and this glossary is a summary. Where the Lean model of development
(`AgenticDev`) has a name for a term, the name is given in parentheses.
Entries are alphabetical.

**Artifact.** Anything under version control that a judgment is about: a
specification, the realization, a rule file, a plan, a report. Reference
material is versioned, but no judgment is about it.

**Assurance.** The argument, from the assurance report (later the ledger)
and the records, that the development-state judgments hold. It is as strong
as the mitigations against the threats to each row's evidence (design 2.9).

**Assurance report.** The document that states, for each development-state
judgment and each of its clauses, whether it holds, on what evidence, with
what provenance, compiled on request against a named state of the tree by
running the mechanical evaluations and reading the records. A very small
assurance case: the clauses are its claims, the evaluation method the reason
the evidence bears on each claim, the provenance the ground for trusting it.
In the running example an agent compiles it from A0; from A2 it is kept
between requests as the *ledger* (design 2.1a).

**Audit.** The activity of reading artifacts against rules and reporting the
gaps; the judgment's name says what is audited. The common case is the audit
of a specification's quality before the specification is relied on: is it
well-formed, unambiguous, internally consistent, externally consistent, and
complete for its level (the generic audit rules AUD-1 to AUD-7), plus the
checks its kind needs (AUD-8 to AUD-14; AUDCON-1 to AUDCON-8 for a concept of
operations). Traceability, which the generic rules also cover, is tracked by
the running example as a judgment of its own (TR). A specification's quality
is established by audit; a realization's conformance by verification. A person
or an agent performs an audit, and the report has the same form whoever
produces it.

**Change request; change report.** The record that opens a change to a
governed artifact and the record that closes it, listing every affected
identifier and the ledger rows re-established. A declared change of mind
opens one.

**Concept of operations (ConOps).** The specification of purpose: what the system
is for, who uses it, which operations they perform, what they can observe, and
the scenarios of use, written so that a non-programmer can read it and say
whether this is the system that was wanted. It opens with a purpose statement.
It is the governing document of the family of specifications — every other
kind is derived from it or must agree with it — and the specification on which
validation is performed: a person reads its scenarios or walks through its
operations, and the rest of the family is validated through it.

**Conformance.** The relationship between a specification S and a realization R
that holds when R satisfies every property S states. It is a yes-or-no question
about the pair; properties S does not state are not part of the question. Under
the module's process, conformance is an invariant of the repository, not a
milestone.

**Development log.** The append-only record of what each task or commit did,
which judgments it touched, and which evaluations were run. A *record*.

**Development state** (`DevState`). The artifacts at a commit together with
the ledger.

**Development-state judgment** (`Judgment`). One of five claims about the
current artifacts, tracked commit by commit: specification quality (SQ),
realization quality (RQ), conformance (CONF), validated (VAL), and traceable
(TR) (design 2.1). Each is *defined* once for the repository and then per
form of artifact, as clauses named `Form-JUDGMENT-n` (`Reqs-CONF-1`), each
with what holds, how it is evaluated, what evidence results, and how it is
bound to the project; the definition says nothing about when the claim must
hold, which is the control layer's business. Distinct from a *judgment
clause*, which is a clause of a specification that needs a reader's
assessment.

**Evaluation.** The activity that produces evidence for or against a
development-state judgment: a run (test, analysis) or a human or agent
reading (review, walkthrough, sign-off). A clause's *Evaluated by* field
names it, and the kind of evaluator named is the clause's rung on the
verifier ladder.

**Evidence.** What an evaluation produced and a judgment rests on: the
results of a run, or a record of a human activity. Evidence has a scope and
a producer, which its *provenance* states.

**Elicitation record.** The stakeholders' verbatim words and the questions and
answers of elicitation, kept as reference and used as the source the user
stories cite.

**Establish; stale** (`Step.establish`; `Ledger.invalidate`). A judgment is
*established* when its evidence is produced and recorded; it goes *stale* when
an artifact it depends on changes, or, for validation, when a stakeholder
declares a change of mind, and stays stale until re-established.

**Executable specification.** A specification in a form a program can run: a
test suite, in which each test is a claim about one clause and cites it, or a
fixture file of scenarios with expected outcomes that any implementation, in any
language, must reproduce. The test suite is at once a realization of the
verification obligations and the algorithmic verifier of the code.

**Family of specifications.** The set of specifications, of several kinds, that
together govern one system — for the module's game: a concept of operations,
rules of play, a display format, an input grammar, an interaction flow, an
interface contract, an example session, verification obligations, and later a
test suite, fixtures, and a tool contract. Each kind fixes something the others
leave open, and the family must be consistent across its members (AUD-3).
`specification-kinds.md` lists every kind the course uses.

**Gate.** A condition placed in front of a step so that the step cannot
complete unless the condition holds. There are two kinds. An *algorithmic
gate* is a program whose exit code decides — in the module,
`pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100`
before an operation is complete and before any commit (VER-4); a program can
stand in front of a commit or a build because it returns an exit code. An
*approval gate* is a recorded human decision: the sign-off on validation, the
ruling on a judgment clause, the sign-off that closes a wave. A green
algorithmic gate establishes that the code does what the tests claim and that
every branch was reached; it does not establish that the tests claim what the
specification says, which is why conformance also requires requirements
coverage.

**Governance.** The process files of a project: the judgment definitions
and their per-form clauses, the procedures, the templates, and, when the
control layer exists, the rules that say when a judgment must hold (design
2.1a, 2.3). Filed by form from the first version and by layer as the layers
arrive.

**Independence.** The requirement that the verifier of a clause not be the
author of the realization it verifies, or that an agent's result be
spot-checked by a person. Recorded per clause group in the verification plan.

**Intent** (`HI`). What the stakeholders have in mind for the system. It lives
in their minds and is never fully written down. There may be indications of
it — informal sketches, elicitation, even digital interactions such as a chat
channel (see *reference*) — but ultimately it can be confirmed only by
consulting a person ("tell me what you want", or "does this specification, or
this behavior of the system, represent what you expected"). No development
artifact represents it. A *change of mind* is the step in which it changes,
and the process learns of one only when a stakeholder declares it, which the
process records as a change request. Validation is the judgment that the
specifications match it, and only a person can make that judgment.

**Invariant.** A property every reachable state must satisfy. Under the module's
process the invariant is conformance: every operation on the repository ends
with a check that re-establishes it, and the specification stays fixed while
the set of realizations changes. When the specification itself changes, the
realizations, the verifier, and the derived documents change with it in one
coordinated step.

**Known-violation set.** Inputs that a verifier must fail on, kept beside it
and run whenever it changes. The seeded gaps of an audit and the sabotage that
closes each version of the running example are instances; it is how a program
at rung 4 of the verifier ladder is verified.

**Ledger** (`Ledger`). The assurance report kept between requests: a table
per named checkpoint stating which development-state judgments hold, on
what evidence, and which rows are stale, with the artifact states each
row's evidence was produced against so that a change marks the rows it
touches. Every row carries its provenance. Enters the running example at A2
(design 2.4a); before that the report is recompiled on request.

**Mechanical clause; judgment clause.** A clause of a specification is
*mechanical* when a program can decide it, by examining the artifact or by
executing it, and *judgment* when it needs a reader's assessment ("accurately
summarizes"). The classification is recorded clause by clause: in a table
(VER-2) or as the clause's verification method, where *test* and *analysis*
are mechanical and *review* and *walkthrough* are judgment. An algorithmic
verifier decides mechanical clauses only; the judgment clauses are named as
remaining for a human or agent verifier, never assumed covered. A judgment
clause is distinct from a *development-state judgment*.

**Mitigation.** The rule, procedure, or report field that closes a threat to a
judgment. Every mitigation has a rule style.

**Plan; task; wave.** A build plan decomposes one build into tasks; tasks are
grouped into waves; each wave ends at a gate.

**Product specification; process specification.** A product specification is
a specification of the system being built, against which the code and its
tests are verified. A process specification is a specification of the work,
whose realization is the repository history and whose verification is a hook
or a reading of the log. The same questions apply to both: when the form is
appropriate, how conformance is shown, and what it must agree with (design
section 4).

**Provenance** (of evidence). What is recorded about a piece of evidence:
which verifier and which version of it produced it, against which state of
which artifacts, over which clauses. It is what a reader uses to decide how
far to trust the evidence, and what lets the rows a verifier established be
found when the verifier turns out to be wrong. A row of the assurance report
or the ledger carries it.

**Record.** A document attesting that an activity was performed and what it
decided: a review record, a walkthrough record, a validation record with its
sign-off, an audit record (the gap list with its rulings), the development
log. Records are evidence and live under `records/` in the running example.
Distinct from a *report*.

**Report.** A presentation of the development and assurance state to the
developers or to other stakeholders such as auditors: the assurance report,
the generated conformance report and trace matrix, later the ledger. Reports
live under `reports/` in the running example. A report is not a record: the
output of a manual task is a record.

**Purpose statement.** The one-to-two paragraph opening of the concept of
operations that says what the system is for. An engineering artifact, revised
with the stakeholders until agreed and audited like the rest of the document.
It is the closest written thing to intent, and it is a specification, a
managed engineering artifact, not a record of intent.

**Realization.** An artifact built to satisfy a specification. When the artifact
is code the usual word is *implementation*; *realization* is the general term,
because a note, a script, a test suite, or another document can each be built to
satisfy a specification. One specification has many realizations.

**Realization quality.** The judgment that the realization lints and
type-checks, that its test suite collects and follows the test discipline, and
that its structure is judged appropriate.

**Reference.** Material that informs specifications but is not one: sketches,
research notes, the elicitation record. Not audited; no judgment is about it.

**Requirements coverage; structural coverage.** The two coverage objectives of
a testing-based verification: every mechanical clause has its tests, and the
suite exercises the code to the stated level. *Verified* is their conjunction
with every test passing and every judgment clause reviewed.

**Rule style.** The kind of a process rule, one of obligation, gate, staleness,
procedure, policy, form, and change control (design 2.8). Every rule names its
style, the judgment it maintains, its decider, its evidence, and what failure
does. In the running example the obligation style is carried by the per-form
judgment clauses from A0, procedures enter at A1, and rules in the full
template (gate, staleness, policy, change control) enter with the control
layer at A2; the form style is a template, not a rule.

**Specification.** A document that states, at a higher level than the artifact
it governs, what the developer intends. It fixes some properties and
deliberately omits others; the omissions leave the realization free where the
developer does not care. Its clauses carry identifiers so that reports can cite
them. A specification is audited before anything is checked against it; the
course distinguishes many kinds (`specification-kinds.md`).

**Threat** (to a judgment). A way the evidence recorded for a judgment can be
present while the judgment does not hold. Five classes (design 2.9): a
defective reference, a wrong verifier, a scope narrower than the claim, stale
or unproduced evidence, and a shared mistake between author and verifier.

**Traceability.** The links between identified items in different artifacts,
in named forms: derivation (story to requirement), allocation (requirement to
part), verification (requirement to test), realization (task to commit), and
change (change request to affected identifiers). Tracked as the judgment TR.

**Validation.** The question whether the specifications describe what the
stakeholders intend — as opposed to verification, which asks whether a
realization satisfies its specification. Intent has no artifact, so only a
person can decide it, usually by reading the scenarios of the concept of
operations or walking through its operations; the judgment covers every
specification derived from it. It is the one judgment no tool can regenerate,
and it goes stale when a stakeholder declares a change of mind even if no file
has changed.

**Verification.** The activity of trying to confirm that a realization conforms
to its specification. The word *trying* is deliberate: a verification result is
evidence with a scope — which verifier produced it, which version of the
specification it was checked against, which clauses were checked — and it can be
wrong in ways the result does not show.

**Verification method** (of a clause). One of *test*, *analysis*, *review*,
*walkthrough*, recorded on the clause (design 2.6). The four come from
crossing who decides (a human, an agent, an algorithm) with what is examined
(the artifact as text, or the realization while it runs). A clause is
mechanical when its method is test or analysis and a judgment clause when it
is review or walkthrough; for a judgment clause the method also records the
verifier kind, human or agent. The running example records the method on the
clause in place of the VER-2 table.

**Verification plan.** The project-specific verification choices: methods and
techniques per clause group, environment and tool versions, coverage
objectives, independence, how each verifier is verified, timing, and the
evidence each verification must produce. A process specification beside the
build plan. Until a project needs one, the standing conformance rules are the
plan.

**Verifier.** Whatever performs a verification. The course names three kinds. A
*human verifier* reads the specification and the realization and works through
the clauses; it decides every clause, including judgment clauses, slowly and
only as reliably as its attention. An *agent verifier* is asked to check and
report; it reads both documents, cites clause identifiers, and can decide
judgment clauses, at a cost in tokens and with results that can differ between
runs. An *algorithmic verifier* is a program written to decide the
specification's mechanical clauses; it is deterministic, immediate, and free to
run, and because it returns an exit code it can be a gate. A verifier is itself
a realization of the specification it checks, so "who verifies the verifier" has
to be answered separately. *Instrument* and *checker* are not used for this
role; tool names such as *type checker* keep their names.

**Verifier ladder.** The climb of one clause's verifier from a human (rung 1)
to an agent (2) to a skill (3) to a program (4), at which point the clause
becomes mechanical (design 2.7). Climbing exchanges threats rather than
removing them. Validation does not climb.
