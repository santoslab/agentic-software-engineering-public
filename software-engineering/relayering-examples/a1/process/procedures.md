# Procedures: Message Guard (version A1)

A procedure is a fixed sequence of steps for an activity, with a stop at
the point where a person decides. Writing the steps down is what makes an
activity repeatable by a person, by an agent, or by a skill, and what lets
a record say which steps were followed. Two procedures are in use. Each
names the judgment clauses it serves, who runs it, where it stops, and the
record it leaves.

## Specs-Audit · The audit of the specifications

| Field | |
|---|---|
| Purpose | Evaluate the SQ clauses together: ConOps-SQ-1, Reqs-SQ-1, Reqs-SQ-2, Gloss-SQ-1, and Specs-SQ-1. An audit is one reading of every specification against one checklist, so that the between-document items are checked by the same reader that checked the within-document items. |
| Serves | SQ |
| Run by | a person, by the checklist in `.claude/skills/audit-spec/checklist.md`; or an agent running `/audit-spec`, which the developer starts. Rulings are a person's in either case. |
| Steps | (1) Read every file under `specs/` in full before the first check. (2) Within each document: well-formed headers, EARS form against the declared pattern, glossary discipline, a reason on every judgment clause. (3) Between documents: every story has a requirement and every requirement a derivation; no contradictions; one sense per term; assumptions and deferred wants have not become requirements; every named file, rule, and entry exists. (4) By execution: decide from the clauses what every example and scenario must output and compare with the stated expectation. (5) Stop and report every gap in the gap-list form. |
| Stops | After step 5. A person rules on each gap: accepted, ruled otherwise, rejected with a reason, or deferred. An accepted gap is amended by the author, and the audit is run again on the amended text. The auditor never amends a file. |
| Record | `records/audit-NN.md`, in the form of `process/templates/gap-list.md`: the audit number; the date; the auditor (a person by name and role, an agent by model and prompt, or a skill by name and version); the specifications and the state audited; every checklist item with *pass* or the gaps it produced; one row per gap with location, the item violated, the text quoted exactly, one proposed resolution, the ruling, and the amendment made. |
| Example | audit 03: `/audit-spec` 1.0 on the pre-audit draft; eleven gaps; the ruling on gap 8 deleted the record-of-drop clause from REQ-1 and kept D-1 |

When to run it is not stated here. The assurance report says whether the
latest audit record is older than the specifications; the control layer of
a later version turns that into a rule.

## ConOps-Elicit · Revising the concept of operations with its stakeholders

| Field | |
|---|---|
| Purpose | Obtain or revise the concept of operations from its stakeholders, so that it says what they intend and ConOps-VAL-1 can be evaluated against it. This is an authoring procedure, not an evaluation: it produces a specification and a reference record, not evidence for a judgment. |
| Serves | VAL (the document it produces is what the stakeholders sign); SQ (its answers settle terms and assumptions) |
| Run by | an agent running `/elicit`, which the developer starts; the stakeholders answer; the developer reviews the resulting change |
| Steps | (1) Read the concept of operations, the glossary, and the existing elicitation record. (2) Scan the document for what it does not settle, by the eight-part taxonomy, and queue at most five questions, ranked by how much the answer changes the document times how uncertain it is; a fact the repository answers is looked up, not asked. (3) Ask one question at a time, addressed to a user category, with options and a recommended answer. (4) Record each question and the verbatim answer, with who answered and when, under an E identifier in `reference/elicitation.md`; then apply the answer to the one part of the document it affects, citing the identifier, and replace contradicted text rather than adding to it. (5) Report: questions asked, sections touched, coverage, and the next steps. |
| Stops | After five questions, when the queue is empty, or when the stakeholder says "done". The developer reviews the whole change. The procedure never writes a decision nobody gave and never touches the requirements, the scenarios, the tests, or the code. The next step after a revision is the audit (Specs-Audit), because the revision changes what SQ is about. |
| Record | `reference/elicitation.md`: reference material in the stakeholders' words, cited by the `Source` field of every story. It is not audited, and no judgment is about it. |
| Example | E-2: the security officer's "I'd like one eventually; not needed for this version" became deferred want D-1 and no requirement |
