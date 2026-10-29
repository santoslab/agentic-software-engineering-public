# TicTacToe Constitution

## Core Principles

### I. Specification and Realization

Development MUST recognize the distinction between specifications and realizations
(implementations). Specifications express developer intent and constrain development;
realizations are the artifacts that are meant to conform to them.

The development process SHOULD emphasize producing evidence that realizations conform
to their specifications — for example, tests or recorded manual reviews.

**Rationale**: Conformance is a relationship between two distinct things. Keeping them
distinct is what makes it possible to ask, and to show, whether one satisfies the other.

### II. Specification Before Realization

A realization changes for exactly one of three reasons, and the history MUST show which:

- **(a) Repair.** The realization did not conform and is changed so that it does.
- **(b) Conformance-preserving change.** The realization conformed before and conforms
  after; what changed lies in what the specification deliberately leaves open — the
  algorithm, its efficiency, the structure or naming of the code. No specification
  change is needed. The change MUST be verified, and its commit message MUST state that
  no specified behavior changed.
- **(c) Change of specified behavior.** A specification has been updated, and the
  realization would no longer conform to the current specification unless it is changed.

**Rationale**: Every change to a realization is either restoring, preserving, or
following conformance. Recording which one makes the history auditable.

### III. A Person Decides Which Side Changes

When a specification and a realization disagree, the finding is a fact about the pair;
which side changes is the developer's decision, not the agent's. The decision and its
reason MUST be recorded — in the changelog when the specification moves, in the commit
message when the realization moves.

**Rationale**: A verification failure does not by itself say whether the intent or the
implementation is wrong. Only the person who owns the intent can settle that.

### IV. Derived Documents Follow Governing Ones

A document derived from a governing specification MUST NOT contradict it. When a derived
document is wrong or incomplete, the agent MUST propose a correction to it rather than
improvising around it. When a derived document and its governing document disagree, the
governing document wins and the derived document is corrected.

**Rationale**: Derived documents are useful only as faithful elaborations; silent
divergence turns them into competing specifications.

### V. Reports

Development SHOULD produce reports that:

- help explain specifications with examples; and
- let the developer easily ascertain the current state of conformance between
  realizations and specifications.

**Rationale**: Evidence of conformance (Principle I) is only useful if the developer can
read it and see where things stand.

## Document Hierarchy

For the purposes of Principle IV, documents govern in this order, each governing those
below it:

1. This constitution.
2. Feature specifications (`specs/<feature>/spec.md`). Each specification's changelog
   (`specs/<feature>/CHANGELOG.md`) is a record of its history, not a derived document.
3. Documents derived from a specification: implementation plans (`plan.md`), research,
   data models, contracts, quickstarts, and task lists (`tasks.md`).
4. Realizations: source code and the configuration that builds it.

Tests serve as evidence of conformance (Principle I); a test that contradicts its
specification is corrected under Principle IV.

## Records of Change

The principles above require the following records:

- Every commit that changes a realization MUST identify which of II(a), II(b), or II(c)
  applies.
- A II(b) commit message MUST state that no specified behavior changed, and the change
  MUST be verified before it is committed.
- When a specification/realization disagreement is resolved, the decision and its reason
  MUST be recorded: in the changelog if the specification changed, in the commit message
  if the realization changed.
- The specification changelog lives with the specification it records: each feature's
  changelog is `specs/<feature>/CHANGELOG.md`, beside its `spec.md`.

## Governance

This constitution supersedes other development practices for this project. Where a
plan, task list, or agent instruction conflicts with it, the constitution wins.

- **Amendments** are made by the developer, through `/speckit-constitution` or a direct
  edit, and recorded in the commit that makes them.
- **Versioning** follows semantic versioning: MAJOR for removing or redefining a
  principle; MINOR for adding a principle or section or materially expanding guidance;
  PATCH for clarifications and wording.
- **Compliance review**: every implementation plan MUST pass its Constitution Check
  against Principles I–V before work begins, and any deviation MUST be justified in the
  plan's Complexity Tracking section.

**Version**: 1.0.1 | **Ratified**: 2026-10-08 | **Last Amended**: 2026-10-08
