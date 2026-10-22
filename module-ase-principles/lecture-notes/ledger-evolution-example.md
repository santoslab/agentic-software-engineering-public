# How a ledger evolves during development

Optional companion to [Lecture 1: Intent, specifications, realizations, and
judgments](lecture-01-intent-specifications-realizations-and-judgments.md#the-ledger).

A ledger records claims supported by evidence about a particular development
state. Relevant changes can make that evidence out of date. Checking again
may support a claim—or reveal a problem. This example follows those changes
without requiring you to memorize a dependency rule for every ledger row.

This is a **hypothetical teaching history**, not a reconstruction of A0's
actual development log. Most steps are working states, not commits. The two
commit checkpoints below are illustrative labels, not repository tags or
hashes. Under A0's process rule, a failed gate prevents a commit; the
deliberately broken states remain uncommitted.

## Reading a ledger entry

The five judgments ask different questions: specification quality (SQ),
realization quality (RQ), conformance to the specification (CONF), validation
against stakeholder intent (VAL), and traceability (TR).

- **Established:** the required checks and reviews succeeded, and their
  evidence supports the claim for the recorded scope and development state.
- **Stale:** earlier evidence is no longer sufficient for the current state;
  renewed checking is needed. This is not a finding that the system is wrong.
- **Not established:** the required checking is incomplete or has found a
  problem. The accompanying finding explains which.

An established entry is a supported, fallible claim—not a guarantee of truth.
A test can be inadequate or a review can miss something. An old passing
result remains a record of what happened then; it does not automatically
justify a claim about what exists now.

## From a draft to a checked implementation

Imagine building the A0 guard: Critical messages are dropped; Public and
Restricted messages pass unchanged.

| Step | Action | What to record or conclude |
|---|---|---|
| 1 | Draft the ConOps and requirements. | SQ is not established: writing the specifications is not the same as reviewing them. The other judgments also await their evidence. |
| 2 | Review the specifications; obtain stakeholder agreement on the named specification version. | Record SQ's review and VAL's sign-off separately. A specification can be well formed without saying what stakeholders want. |
| 3 | Write the implementation and tests. | Their existence alone establishes neither RQ nor CONF. Record which checks remain outstanding. |
| 4 | Run lint and collect the test suite successfully. | Record RQ evidence under A0's limited quality rule. Collection shows that tests can be discovered, not that their assertions pass. |
| 5 | Run the full suite with the required coverage checks; complete the story walkthroughs and check the trace references. | Record CONF and TR evidence once their obligations are met. Automated citation checks do not replace the review of specification derivations or stakeholder sign-off. |
| Checkpoint 1 | Confirm the gate passes, complete the evidence records and dev-log entry, and commit. | All five judgments now have recorded support for this state. Identify the checked source state in the evidence; a commit itself establishes none of the judgments. |

This ordering is illustrative. Reviews and testing can be interleaved. What
matters is that the ledger claims no more than the available evidence
supports. In particular, passing the automated gate alone does not establish
all five judgments.

## A code change followed by a failed check

Next, reproduce the lecture's deliberate defect: change the condition in
`guard/filter.py` from Critical to Restricted. The guard now drops Restricted
messages and lets Critical messages through.

**Immediately after the edit:** earlier code-dependent evidence needs
renewal. We have not yet obtained a new test result. A suitable CONF entry
would say:

> Stale — the implementation has changed since the recorded successful
> verification; checking the changed state is pending.

**After rerunning the gate:** lint and collection succeed, and the clause
citations still resolve. Four behavioral tests fail, covering REQ-1 and
REQ-2, even though branch coverage remains 100 percent. Now the CONF entry
has a current finding:

> Not established — the current run reports failures for REQ-1 and REQ-2;
> see the conformance report and retained run output.

This is more informative than leaving the entry merely stale: we checked
and found a problem. The other successful checks do not cancel that result.
Conversely, CONF's failure does not mean that every other judgment failed.

These entries are examples of what a developer would record. A0's gate
rewrites the conformance report; it does **not** rewrite the handwritten
ledger. The ledger at Checkpoint 1 remains a historical record, not evidence
that the edited working tree is still green.

**Checkpoint 2:** repair the defect, rerun the gate, and complete or renew the
required reviews and evidence records for the repaired state, including the
walkthrough evidence needed for CONF. Once the obligations are met, record
CONF as established and commit. The failed intermediate state is not
committed under A0's gate rule. The dev log can still record the failed run
and the repair; committing only the repaired state does not mean hiding the
problem's history.

## A changed intention while the tests still pass

Continue from Checkpoint 2. The security officer now says, "Restricted
messages must also be stopped." No specification, code, or test has changed
yet. The existing suite can still pass: it checks the old policy.

The earlier validation no longer supports the current intent:

> VAL stale — the security officer has declared a policy change; agreement
> on a revised specification is pending.

The unchanged artifacts can still agree with each other. That does not make
them suitable for the newly intended system. Validation answers a question
that rerunning the old tests cannot answer.

Now revise the affected story and requirement. Their earlier quality review
and the earlier conformance evidence need renewal; check the affected trace
relationships as well. The old tests may still pass because a marker refers
to an identifier, not to the meaning of the revised sentence. Retaining the
identifier REQ-2 does not make the old assertion correct for its new meaning.

Review the revised specifications, obtain fresh stakeholder agreement, align
the implementation and tests with the new policy, and renew the required
evidence before claiming that the revised system is established. Trace links
help identify affected tests but do not identify every possible dependency:
uncited tests are permitted and can also need revision.

This scenario previews later change-management material. It does not change
the canonical A1 functionality, which remains the same as A0's.

## Evidence can need renewal without a product-code change

Two further situations explain why the ledger's dependencies extend beyond
the product implementation:

- **A test changes.** Suppose a developer changes a REQ-2 assertion. The
  previous successful run was over a different test suite. Review the revised
  assertion and rerun the required checks before relying on it as current
  evidence. If it accidentally stops checking the output, a green run and a
  valid citation may still be inadequate support for the requirement.
- **A checking tool is found defective.** Suppose the conformance plugin
  mistakenly overlooks an invalid citation. The recorded result happened,
  but the affected claim can no longer rely on it without reassessment.
  Identify the affected evidence, correct or replace the checker, and renew
  the checks. Repeating the same defective check is not sufficient.

Relevant configuration or environment changes can likewise require renewed
evidence. Later versions make these dependency decisions more systematic.
For now, ask three questions: **What claim are we making? What supports it?
Has anything changed that makes that support insufficient?**
