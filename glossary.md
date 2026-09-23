# Glossary of Agentic Software Engineering Course

Terms the course uses in a fixed sense. The definitions follow the
software-engineering module's Lecture 01 ("Four terms" in
`module-software-engineering/lecture-notes/lecture-01-specifications-realizations-and-conformance.md`)
and the catalog of specification kinds (`specification-kinds.md`). Where a
process document (AUD, AUDCON, DEV, VER, RPT) defines a rule, the process
document is normative and this glossary is a summary. Entries are alphabetical.

**Audit.** The assessment of a specification's quality before the specification
is relied on: is it unambiguous, internally consistent, externally consistent,
complete for its level, and traceable (the generic audit rules AUD-1 to AUD-7),
plus the checks its kind needs (AUD-8 to AUD-14; AUDCON-1 to AUDCON-8 for a
concept of operations). A specification is *audited*; a realization is
*verified*. A person or an agent performs an audit, and the report has the same
form whoever produces it.

**Concept of operations (ConOps).** The specification of purpose: what the system
is for, who uses it, which operations they perform, what they can observe, and
the scenarios of use, written so that a non-programmer can read it and say
whether this is the system that was wanted. It is the governing document of the
family of specifications — every other kind is derived from it or must agree
with it — and the one specification checked by validation rather than by
verification.

**Conformance.** The relationship between a specification S and a realization R
that holds when R satisfies every property S states. It is a yes-or-no question
about the pair; properties S does not state are not part of the question. Under
the module's process, conformance is an invariant of the repository, not a
milestone.

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

**Gate.** An algorithmic verifier placed in front of a step so that the step
cannot complete unless the verifier passes — in the module,
`pytest --cov=. --cov-branch --cov-report=term-missing --cov-fail-under=100`
before an operation is complete and before any commit (VER-4). A program can be
a gate because it returns an exit code; a person or an agent cannot. A green gate
establishes that the code does what the tests claim and that every branch was
reached; it does not establish that the tests claim what the specification says.

**Invariant.** A property every reachable state must satisfy. Under the module's
process the invariant is conformance: every operation on the repository ends
with a check that re-establishes it, and the specification stays fixed while
the set of realizations changes. When the specification itself changes, the
realizations, the verifier, and the derived documents change with it in one
coordinated step.

**Mechanical clause; judgment clause.** A clause of a specification is
*mechanical* when a program can decide it from the artifact alone, and
*judgment* when it needs a reader's assessment ("accurately summarizes"). The
classification is recorded clause by clause (VER-2). An algorithmic verifier
decides mechanical clauses only; the judgment clauses are named as remaining for
a human or agent verifier, never assumed covered.

**Realization.** An artifact built to satisfy a specification. When the artifact
is code the usual word is *implementation*; *realization* is the general term,
because a note, a script, a test suite, or another document can each be built to
satisfy a specification. One specification has many realizations.

**Specification.** A document that states, at a higher level than the artifact
it governs, what the developer intends. It fixes some properties and
deliberately omits others; the omissions leave the realization free where the
developer does not care. Its clauses carry identifiers so that reports can cite
them. A specification is audited before anything is checked against it; the
course distinguishes many kinds (`specification-kinds.md`).

**Validation.** The question whether the specification describes the system that
was wanted — as opposed to verification, which asks whether a realization
satisfies its specification. A person decides it, usually by reading the
scenarios of the concept of operations or walking through its operations.

**Verification.** The activity of trying to confirm that a realization conforms
to its specification. The word *trying* is deliberate: a verification result is
evidence with a scope — which verifier produced it, which version of the
specification it was checked against, which clauses were checked — and it can be
wrong in ways the result does not show.

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
