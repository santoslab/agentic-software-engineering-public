# Plan for Version A1 of the Message Guard

> Status: proposal, 2026-10-22, written independently of
> `running-example-a1-plan.md` (not read) so that the two can be compared.
> Inputs: `running-example-design.md` (sections 2, 3 option A, 4, 8, 9),
> the built A0 snapshot (`../module-ase-principles/demos/running-example-message-guard/v0/`),
> Lecture 01 and its demo script, the ledger-evolution sidebar, the review's
> section 8 priorities, `glossary.md`, and the catalog entries for the
> concept of operations, behavioral requirements, and fixtures.
>
> Scope: A1 keeps the A0 product (one stage, `filter`, drop Critical, pass the
> rest unchanged) and changes only how the product is specified, checked, and
> recorded. Nothing in this plan changes `guard/`.
>
> Built 2026-10-22: the snapshot is
> `../module-ase-principles/demos/running-example-message-guard/v1/`, with
> four commits replayed by `build-history.sh`. Deviations from this plan are
> listed in the dev log and the ledger of the snapshot: the human audit
> (audit 01) is a rehearsal prediction until the instructor runs it live;
> two further audits (04, 05) ran before the later commits because rule SQ-2
> requires one before any commit that changes a specification; the
> `/audit-spec` checklist is at version 1.1 after its first run caught the
> build's own setup; the ledger has a table at every commit, as the amended
> RPT-1 requires.
>
> Revised 2026-10-22 after instructor feedback: (1) elicitation ships as the
> skill `/elicit`, modeled on Spec Kit's `speckit-clarify` (Q3 decided (b);
> Q13 decided: answers are applied immediately); (2) L2 is organized around
> the concept of operations: why we write it, its format, how we get it, what
> we do with it; (3) no lecture time goes to building tooling; v1 carries a
> tool catalog (`tooling/`) that teaches it instead; (4) two sidebar files
> accompany the L2 notes. Q1, Q2, and Q4 to Q12 stand as recommended unless
> the instructor overrides them.

Section 1 is the list the brief asked for first: every new feature of A1 and
what it teaches. Sections 2 to 12 are the plan proper. Section 13 lists the
decisions I want settled before building, with a recommendation for each.
Section 14 is what the completion report must show.

---

## 1. What is new in A1, and what each feature teaches

Twelve things are new. The first five are specification forms, the next
four are verification and process mechanisms, the last three are records and
teaching apparatus. Each row names the lecture that carries it under the
two-lecture split the instructor proposed (L2: the concept of operations,
why we write it, its format, how we get it, what we do with it; L3: from the
concept of operations to requirements, EARS, the audit, traceability), with
the audit and the trace tool placed in L3 (section 11 explains why). Tooling
is taught by the catalog in v1 and a sidebar, not by lecture time.

| # | New in A1 | What it is, concretely | What it teaches | Lecture |
|---|---|---|---|---|
| N1 | **The `/elicit` skill and the elicitation record** | A skill modeled on Spec Kit's `speckit-clarify` and governed by rule WF-2: it reads the A0 concept of operations, scans it against a ConOps-shaped taxonomy, and asks the stakeholders at most five questions, one at a time, each addressed to a user category, with options and a recommended default; each accepted answer is recorded verbatim in `reference/elicitation.md` under an identifier E-1 to E-5 (who answered, when, and the consequence) and applied to the concept of operations and the glossary at once. It is A1's second skill; `/audit-spec` remains the first *verifier* skill, so the ladder story is unchanged. Two sidebars accompany it: grill-me compared with `/elicit`, and tooling as engineering (section 11.3) | How a purpose statement and stories are *obtained*, not just written; intent is consulted through a person and the agent must stop and ask; the boundary between reference material (not audited, no judgment about it) and a specification; why the grill-me procedure overwhelmed students and what a coverage scan, the five-question cap, and the recommended default change | L2 |
| N2 | **The revised concept of operations** | Purpose statement now stated as *agreed* (both user categories, dated, citing E-ids); scope with an explicit **Assumptions** list (level assigned before arrival; routed through the guard; one message at a time); user categories unchanged (message sender, security officer) with the developer named as *not* a user category; the three stories reworded in the stakeholders' words with a `Source:` field; a new **Deferred wants** section (a record of drops; sanitizing; policy change) that points at the elicitation record and at nothing in the requirements | Anatomy of a concept of operations; the difference between an assumption (the deploying organization's obligation) and a requirement (ours); a want that was heard, recorded, and deliberately not promised; and the first real staleness: revising the document makes VAL stale while every file that was green stays green | L2 |
| N3 | **The glossary as a specification** | `specs/glossary.md`: the A0 "Terms" section promoted to its own document and kind (message, security level, payload, pass, drop, filter, enclave, guard, output, message sender, security officer); every term defined once; REQ-0 now derives from the glossary | The shared vocabulary the brief asked for (a simple domain model); the **glossary-discipline check** is the one SQ check whose verifier climbs the ladder in plain view: a person (audit 1), an agent (audit 2), the skill (audit 3), and in A2 a script | L2 (the document), L3 (the check) |
| N4 | **Requirements in EARS** | REQ-0 to REQ-3 rewritten in EARS with their identifiers kept and a `Pattern:` field added (ubiquitous for REQ-0; event-driven for REQ-1 to REQ-3); the draft that the audit sees also contains two requirements that should not survive (REQ-4, REQ-5, section 5.3) | Structured natural language: a fixed subject, "shall", and a trigger make a clause checkable for form before it is checkable for content; which EARS pattern each later version will need (state-driven for sessions in A4, unwanted-behavior for the policy change in A3, optional-feature for the policy table in A6); an identifier can stay the same while the sentence changes, which is why evidence goes stale on a specification change | L3 |
| N5 | **Acceptance scenarios as data, and the stories' climb from walkthrough to test** | `specs/scenarios.json`: one scenario per story example (SC-1 to SC-6), each with `derived_from`, the role, the input message, the expected output or `null`, plus `assumes` and `blind_spots` fields; `tests/test_scenarios.py` parametrizes over the file and cites the story each scenario derives from; the stories' method changes from *walkthrough (human)* to *test* | One concept, two bindings (values only versus values and interface); a scenario set under-approximates the requirement; the fixture is stakeholder-readable and person-authored, which is the first instance of **independence** (threat T5: an agent that misreads "unchanged" in both its code and its unit tests still fails the stakeholder's scenario); the verification of the story's behavior climbs to rung 4 while **validation does not climb** (the sign-off is kept) | L2 |
| N6 | **The specification audit: procedure, gap list, seeded gaps, three runs** | Rule SQ-2 (style *procedure*): read everything first; check within each document, between documents, and by executing the examples; stop and report. Rule RPT-2 (style *form*): the gap list. The pre-audit draft carries seven seeded gaps (section 6). The same draft is audited three times: by a person in class, by the agent with an ad-hoc prompt, and by the agent running `/audit-spec`; the person rules on every gap; amendments follow | Threat T1 (a reader's capacity: the person misses the between-document gaps), threat T2 (a verifier can be wrong: the agent over-reports one non-gap, the REQ-2 identity question from Lecture 01); the two new rule styles; "mechanical or judgment is discovered, not declared" (the EARS-form and glossary checks turn out decidable and become a script in A2; the purpose statement's implementation-independence stops at rung 3); the seeded gaps are the audit's known-violation set | L3 |
| N7 | **The verifier skill, `/audit-spec`** | `.claude/skills/audit-spec/` with `SKILL.md`, `checklist.md` (the SQ-2 checks in order), and `gap-report-template.md` (the RPT-2 form); its first step is to read every file under `specs/` in full; it cites identifiers and quotes text; it never amends; it reports under a version | A skill is rung 3 of the verifier ladder: the procedure becomes an artifact that is versioned and the same every run, even where the findings differ; the ledger records the skill's version as provenance; read-before-check is the mitigation for the agent's characteristic threat (judging from memory) | L3 |
| N8 | **The trace tool and the trace matrix** | `tools/trace.py` reads the four specifications and the suite's citations, writes `reports/trace-matrix.md` (story to requirement to scenario to test, and the reverse), lists findings (dangling reference, duplicate identifier, malformed clause header, unsupported method, story with no requirement, requirement with no story, test clause with no citing test), exits non-zero on any finding, and runs in the gate (rule TR-2); `tests/tooling/` holds small malformed specifications with expected findings | TR made mechanical in both directions; the "derived from" check climbs from a person (A0, TR-1) to a program; **the tooling is engineered** (CF-14): its requirements are written first, the prompt that built it is kept, and it is verified on cases it must fail on before its findings are trusted (CF-06) | L3 |
| N9 | **Validation per user category and the re-sign-off** | Rule VAL-2 (style *form*): `reports/validation.md` records, per user category, the stories walked on the running v1 with the scenario inputs, what was observed, and the decision; VAL-1's sign-off follows, naming version A1 and the deferred wants it is scoped to. CONF-2 keeps its wording and has no clause in scope at A1 | Behavioral checking and validation are different activities even when one person does both in one sitting (CF-04): every scenario passes and the officer may still decline; a sign-off is scoped to a version; what the walkthrough record is *for* changes when the behavioral check becomes a test | L2 |
| N10 | **The ledger at two checkpoints, and a dev log that is a commit sequence** | `reports/ledger.md` gains a second table, "At a1-specs", between the A0 table and the final "At v1" table: SQ established by the skill's audit plus rulings, VAL stale (the concept of operations changed), CONF and TR renewed by rerun with a note that the assertions were re-read against the EARS sentences, RQ unchanged; at v1 all five rows established with new provenance. A1 is the first version whose dev-log entries each correspond to a commit that passed the gate | Established, stale, and renewed on a real intermediate state rather than a hypothetical one; provenance changes when the verifier climbs (SQ: "the instructor" becomes "`/audit-spec` 1.0 plus rulings by the instructor"; TR: "read by a person" becomes "`tools/trace.py` 1.0"); the per-commit gate policy works once the infrastructure exists, which is the contrast with A0's first-commit problem | L2 (VAL stale), L3 (the rest) |
| N11 | **Conformance report: a scope line and story rows backed by scenarios** | The plugin writes "Scope: full run" or "Scope: partial run (tests were deselected); not evidence for CONF" at the head of the saved report (the minimal CF-05); story rows now list the citing scenario tests; the plugin's clause reader no longer drops a malformed header silently but reports it | A report says its own scope (threats T3 and T4); a green row table and a green gate are different claims | L3 |
| N12 | **The tool catalog** | `tooling/README.md`, a table of every assurance tool in v1 with its goal, plus one page per tool (goal, requirements, the prompt that produced it or guidance for one, review points, deliberate-failure checks, how to adapt it to another project, how to make it shared infrastructure); `reference/prompts/` keeps only the non-tool prompts (the EARS rewrite, the ad-hoc audit) | CF-14 by supplementary material rather than lecture time: reports and gates do not appear by themselves; a student reads the catalog to set up the same tooling in their own project, or to build infrastructure shared across projects | reading, pointed at from L2 and L3 |

Not new, and deliberately so: `guard/` is byte-identical to A0; `tests/test_filter.py`, `tests/test_message.py`, and `tools/walk.py` are unchanged; the ledger is still written by hand; the gate still stands before every commit (WF-1); no audit log, no negative-payload policy, no "no message" input (CF-03).

---

## 2. Constraints this plan inherits

From design section 9, the accepted items that bind A1 and how the plan meets each: CF-01 (optional citations) is kept as policy and demonstrated on the evidence machinery (section 9.4); CF-02 (fallible, scoped claims) governs every report legend and every ledger row; CF-03 (handwritten ledger, unchanged behavior) is met by construction and checked by `diff -r v0/guard v1/guard`; CF-04 (fixtures do not automate validation) is the design of N5 and N9; CF-14 (tooling built explicitly) is N8 and N12.

The proposed items with the instructor's notes, and what this plan does with each (decisions in section 13): CF-05, adopt only the one-line scope label; CF-06, adopt in full, it is cheap and it is the known-violation set of the trace tool; CF-07, adopt as a hand convention now and a mechanism in A2, with the practical shape spelled out in section 9.5; CF-13, resolve through elicitation question E-4 with no product change.

Design-level constraints: at most eight new rules and two new styles (this plan adds seven rules and the styles *procedure* and *form*); every clause carries a method; CONF is the aggregate; every ledger row carries provenance; the version ends with a "break it" demonstration of the judgments it introduced.

---

## 3. The story A1 tells

Between v0 and v1 the following happens, in this order, and the artifacts are the trace it leaves.

1. The author of the A0 concept of operations asks the two stakeholders five questions through `/elicit`. The answers define the terms, separate the assumptions from the requirements, and surface two wants (a record of drops; a later sanitizing stage) that are recorded and deferred. The purpose statement is agreed in the stakeholders' own words.
2. The concept of operations is revised, the terms become a glossary, and the agent rewrites the requirements in EARS. The draft is plausible and has seven gaps, two of them the agent's own doing (a want that leaked into REQ-1; an assumption that became REQ-5).
3. The draft is audited three times by three verifiers. A person finds four or five of the seven. The agent finds six and reports one that is not a gap. The skill finds seven and reports nothing else. The person rules on every gap, including the false one. The amended specifications are committed; the gate (still A0's) is green; VAL is stale.
4. The stories' examples become a scenario file that the stakeholders can read, and a loader turns every scenario into a test that cites its story. The stories' method becomes *test*. The gate is green.
5. The trace tool is specified, built by the agent from its requirements, verified on cases it must fail on, and added to the gate. The matrix shows the whole chain from story to test with no findings. The gate is green.
6. Each stakeholder walks their stories on the running system and signs the revised concept of operations for version A1, scoped to the deferred wants. The ledger at v1 has five established rows with new provenance.
7. The version closes by breaking it: a contradiction the skill catches and the gate does not; a shared misreading the person-authored scenario catches; a wrong derivation the trace tool catches; and a stakeholder who declines to sign while every scenario passes.

---

## 4. The v1 snapshot

Directory `../module-ase-principles/demos/running-example-message-guard/v1/`. Changed or new against v0 (everything else identical):

| Category | File | Status |
|---|---|---|
| Specifications | `specs/conops.md` | revised (section 5.1) |
| | `specs/glossary.md` | new (5.2) |
| | `specs/requirements.md` | rewritten in EARS, identifiers kept (5.3) |
| | `specs/scenarios.json` | new (5.4) |
| Reference | `reference/elicitation.md` | new (5.5) |
| | `reference/drafts/` | new: the pre-audit `conops.md`, `glossary.md`, `requirements.md` with the seeded gaps, for replaying the audit |
| | `reference/prompts/` | new: the retained non-tool prompts (the EARS rewrite, the ad-hoc audit) |
| Realization | `tests/test_scenarios.py` | new: the fixture loader |
| | `tests/conformance.py` | extended: generic field parsing, scenarios, findings instead of silent omission |
| | `tests/conftest.py` | extended: scope line; story rows; reads the extended clause records |
| | `tests/tooling/` | new: known-violation cases for `trace.py` and the clause reader |
| Rules | `process/rules.md` | seven rules added, five amended, a changelog section added (section 7) |
| Skills | `.claude/skills/elicit/` | new (section 8a) |
| | `.claude/skills/audit-spec/` | new (section 8) |
| Tools | `tools/trace.py` | new (section 9) |
| Tool catalog | `tooling/README.md` and one page per tool | new (section 9) |
| | `tools/gate.sh` | runs `trace.py` after `pytest`; prints a provenance header |
| Reports | `reports/audit-01-human.md`, `audit-02-agent.md`, `audit-03-skill.md` | new: the three gap lists with rulings |
| | `reports/trace-matrix.md` | new, generated |
| | `reports/conformance.md` | regenerated, new form |
| | `reports/validation.md` | new; replaces `reports/walkthrough.md` (which does not exist in v1) |
| | `reports/ledger.md` | two tables added |
| | `reports/dev-log.md` | entries 4 to 9 appended |
| Support | `CLAUDE.md`, `README.md`, `pyproject.toml` (version `0.1.0`, description) | revised |

Which files update automatically (CF-03's completion check, to be stated in the README): `reports/conformance.md` and `reports/trace-matrix.md` are generated by the gate. The ledger, the dev log, the validation record, and the audit rulings are written by hand. The audit *reports* are written by the agent or the skill, then ruled on by hand.

---

## 5. The specifications in detail

### 5.1 `specs/conops.md`, revised

Sections: 1 Purpose (agreed); 2 Scope and system boundary, with 2.1 Assumptions; 3 User categories; 4 User stories; 5 Deferred wants; 6 Sign-off (pointer). The Terms section is gone, replaced by a one-line pointer to the glossary.

- **Purpose.** The A0 text, tightened, with one new sentence that the decision rests on the marking alone and that the guard does not inspect the payload in this version (from E-1), and a closing line: "Agreed by the security officer and a message sender on 2026-10-DD; their words are in `reference/elicitation.md` (E-1, E-3)."
- **Assumptions (2.1).** A-1: a message's security level is assigned before it reaches the guard and the guard trusts it (E-5). A-2: every message leaving the enclave is routed through the guard (A0's deployment assumption, now labeled). A-3: the guard handles one message at a time and keeps no state between messages. Each is marked "assumption: the deploying organization's obligation, not a requirement on this library."
- **User categories.** Message sender and security officer as in A0, each with an "observes" line derived from E-3 and E-2. One added sentence: the developer who builds the guard is not a user category; the developer's obligations are in `process/rules.md`.
- **Stories.** US-1 to US-3, reworded closer to the record, each with the header `**US-n** · Method: test · Scenarios: SC-a, SC-b · Validated by: walkthrough (human), <user category> · Source: E-k`. The example line is kept in prose and is the same message as the cited scenarios. In the pre-fixtures commit (section 10, commit 1) the header still says `Method: walkthrough (human)`; the flip happens with the fixtures.
- **Deferred wants.** D-1: a record of every dropped message, observable by the security officer (E-2); D-2: changing the payload of a Restricted message before it leaves (E-1 follow-up); D-3: a change to which levels are stopped (E-1). Each says "recorded, not promised in A1; no requirement derives from it."

### 5.2 `specs/glossary.md`, new

One entry per term, `**term**: definition`, defined once, alphabetical, with a header that states the discipline (rule SQ-4): every specification uses these terms in this sense and defines none of them itself. Entries: drop, enclave, filter, guard, message, message sender, output, pass, payload, security level, security officer, stage, unchanged. The *payload* entry records E-4: "a single integer; the specification does not constrain how a programming language represents integers" (this is the CF-13 resolution: recorded, open at the language level, no product change).

### 5.3 `specs/requirements.md`, in EARS

Header fields: `**REQ-n** · Method: test · Pattern: <EARS pattern> · Derived from: <US-n or Glossary: term>`. The final text:

| ID | Pattern | Statement |
|---|---|---|
| REQ-0 | ubiquitous | The guard shall accept as a message exactly a security level, which is one of Public, Restricted, or Critical, and an integer payload; a message shall not change after it is created. (Derived from: Glossary: message, security level, payload) |
| REQ-1 | event-driven | When the filter receives a message whose security level is Critical, the filter shall produce no output. (US-3) |
| REQ-2 | event-driven | When the filter receives a message whose security level is Restricted, the filter shall output a message with the same security level and the same payload. (US-2) |
| REQ-3 | event-driven | When the filter receives a message whose security level is Public, the filter shall output a message with the same security level and the same payload. (US-1) |

The existing tests cite these identifiers and need no change; the dev-log entry for commit 1 records that the assertions were re-read against the new sentences (the A2 test-discipline review is where this becomes systematic).

The *draft* (kept under `reference/drafts/`) differs from the final text in the seven places section 6 lists, including two extra clauses: REQ-4 (no input, no output, with a malformed header) and REQ-5 (the routing assumption written as a requirement).

### 5.4 `specs/scenarios.json`, new

```json
{
  "specification": "Acceptance scenarios for the message guard, derived from the user stories in specs/conops.md. Any realization, in any language, must reproduce them.",
  "version": "A1",
  "assumes": "A message is a security level and an integer payload (REQ-0). The filter stage alone (A1).",
  "governance": "Never edited to make a test pass. A scenario that looks wrong is a gap about the pair (scenario, story) and goes to the audit.",
  "scenarios": [
    {"id": "SC-1", "derived_from": "US-1", "role": "message sender",
     "input": {"level": "Public", "payload": 42}, "expected": {"level": "Public", "payload": 42}},
    {"id": "SC-2", "derived_from": "US-1", "role": "message sender",
     "input": {"level": "Public", "payload": -3}, "expected": {"level": "Public", "payload": -3},
     "note": "E-1: the payload is not inspected; a negative payload leaves like any other"},
    {"id": "SC-3", "derived_from": "US-2", "role": "message sender",
     "input": {"level": "Restricted", "payload": 7}, "expected": {"level": "Restricted", "payload": 7}},
    {"id": "SC-4", "derived_from": "US-2", "role": "message sender",
     "input": {"level": "Restricted", "payload": 150}, "expected": {"level": "Restricted", "payload": 150},
     "note": "E-1 follow-up: no clamping in A1 (deferred want D-2)"},
    {"id": "SC-5", "derived_from": "US-3", "role": "security officer",
     "input": {"level": "Critical", "payload": 100}, "expected": null},
    {"id": "SC-6", "derived_from": "US-3", "role": "security officer",
     "input": {"level": "Critical", "payload": 0}, "expected": null}
  ],
  "blind_spots": [
    "Only the listed payload values; the requirements are universal over integers.",
    "No scenario for a malformed message; REQ-0 is verified by unit tests, not scenarios."
  ]
}
```

SC-2 and SC-4 are the two scenarios that exist because of elicitation: they pin behavior the stakeholders explicitly confirmed and that a later version will change. Scenarios are not rows of the conformance report; the story is the clause and the loader cites it (decision Q2).

The loader, `tests/test_scenarios.py`, builds `pytest.param(scenario, marks=pytest.mark.req(scenario["derived_from"]), id=scenario["id"])` for every entry, constructs the message, calls `filter_message`, and compares the output to `expected`. One test function, six cases, each cited to its story.

### 5.5 `reference/elicitation.md`, new

Header: date, who asked (the agent, with the instructor directing), who answered (the instructor playing the security officer and a message sender, as in A0's sign-off), the procedure (WF-2, run as `/elicit`; at most five questions, options, a recommended default, one at a time; answers applied as they are accepted). Then per question:

```
### E-1 · to the security officer
Question: Does whether a Critical message is stopped depend on anything besides its marking?
Why it matters: it decides whether the guard inspects the payload or the sender.
Options: A. the marking alone (recommended) · B. marking and payload range · C. marking and sender
Answer (verbatim): "The marking alone. We don't look inside in this version. Later I may want
large Restricted payloads cut down, but that is later."
Consequences: purpose statement sentence 3; glossary "security level"; deferred want D-2; SC-2, SC-4
```

E-1 the marking alone (officer); E-2 a record of drops, deferred (officer); E-3 what a sender observes on a drop, nothing (sender); E-4 what a payload is, a whole number, with the agent's follow-up about true/false answered "a number is a number" (both); E-5 who assigns the marking and whether the guard trusts it (officer). The record closes with the agreed purpose statement as spoken and a "what was not asked" line (nothing about ordering, throughput, or transport, all outside the boundary).

The record is produced by a real run of `/elicit` (section 8a), with the agent asking and the instructor answering in both roles, and then edited only for length; the skill's completion report is kept with it. Authenticity of the agent's questions is part of what L2 shows. The ConOps and glossary changes the run makes are the draft that section 6's audits examine, once the seven gaps are seeded into it.

### 5.6 Clause formats, defined for the tools (CF-06)

A clause header is one line: `**ID** · Key: value · Key: value ...`. Identifiers match `[A-Z]+-\d+` with families `US`, `REQ`, `SC` (in JSON), `E` (reference), `A` and `D` (contextual, not clauses). Keys and where they are allowed: `Method` (required on US and REQ; values `test`, `walkthrough (human)`, `walkthrough (agent)`, `review (human)`, `review (agent)`, `analysis`), `Pattern` (REQ; one of the six EARS patterns), `Derived from` (REQ; a US identifier or `Glossary: term, ...`), `Scenarios` (US; SC identifiers), `Validated by` (US), `Source` (US; E identifiers), `Reason` (required when the method is a judgment method; absent at A1 because no clause has one). The clause reader reports, as findings rather than silently skipping: a header with an identifier and no `Method`; an unknown method value; an unknown key; a duplicate identifier; an identifier family in the wrong file. Everything that is not a clause header is contextual specification text: audited by SQ-2, not a row of any report.

---

## 6. The seeded gaps and the three audits

All three audits run on the same draft (the working tree before commit 1), so their findings compare. Expected findings are a rehearsal prediction for the agent and the skill and a plausible pattern for a person; the demo script will say that the live human result varies and that this variation is the point.

| # | Where (draft) | Seeded text | Check that finds it (SQ-2 step) | Person | Agent | Skill | Threat | Ruling and amendment |
|---|---|---|---|---|---|---|---|---|
| G1 | US-3 | "I need every **sensitive** message stopped" | glossary discipline, within document: undefined term | finds | finds | finds | T1 | amend to "every message whose security level is Critical" |
| G2 | REQ-1 against ConOps 2 and D-1 | REQ-1 ends "...shall produce no output **and shall record the drop**"; the scope says no record is kept | between documents: contradiction; a deferred want leaked into a requirement | misses | finds | finds | T1 (capacity: between-document) | delete the clause; D-1 stays deferred (E-2) |
| G3 | REQ-2 | "Restricted messages are allowed through." | EARS form: no trigger, no subject, no "shall"; Pattern field says event-driven | finds | finds | finds | none (syntactic; becomes a script at A2) | rewrite as in 5.3 |
| G4 | US-2 example | "the guard is given (Restricted, 7); it outputs (**Public**, 7)" | by execution: run the example with `walk.py`; the observed output contradicts the example | may miss | finds | finds | T1 | amend the example; SC-3 is the corrected scenario |
| G5 | REQ-5 (draft only) | "The guard shall receive every message that leaves the enclave." Method: test | assumption written as a requirement; outside the library's boundary; nothing in `guard/` can realize it (the gate on the draft shows "REQ-5: no evidence", the symptom, not the cause) | misses | finds | finds | T1; T3 | delete; it is Assumption A-2 |
| G6 | REQ-4 (draft only) | header `**REQ-4** · Derived from: US-3`, no Method; "The filter shall produce no output when it receives no message." | well-formedness: malformed header (A0's reader would drop it silently; A1's reader and `trace.py` report it); content: "no message" is not an input of a function of one message, and the clause is implied by REQ-1 to REQ-3 | finds the missing field; may accept the content | finds both | finds both | T2 (the parser's silent omission) | delete; note in the HAMR mapping that No_Input_No_Output has no counterpart in a one-message library |
| G7 | Purpose statement | "...the message guard is a **Python function** that decides..." | implementation-independence of the purpose statement (the check whose ceiling is rung 3) | finds | finds | finds | none | amend; the language lives in `pyproject.toml` |
| false | REQ-2 | "the same security level and the same payload" | the agent's ad-hoc audit flags ambiguity about object identity versus value equality | not raised | **reports** | does not report: `checklist.md` says an implementation choice the specification leaves open is not an ambiguity | T2 (agent over-reporting) | rejected, with the Lecture 01 reasoning recorded as the ruling |

The three reports use the RPT-2 form (section 7) and are kept as `reports/audit-01-human.md`, `audit-02-agent.md`, `audit-03-skill.md`, each with the rulings column filled by the instructor. The seeded set is also the known-violation set of the `/audit-spec` skill and, in A2, of the script that replaces its syntactic steps.

---

## 7. The rules at A1

Seven new rules (budget: eight) in the A0 template; two new styles, *procedure* and *form*. Statements condensed here; the file carries the full fields and one example each from this system.

| ID | Style | Maintains | Statement (condensed) | Decided by | Evidence | On failure |
|---|---|---|---|---|---|---|
| SQ-2 | procedure | SQ | To audit the specifications: (1) read every file under `specs/` in full; (2) within each document check well-formed headers, EARS form, glossary discipline, a reason on every judgment clause; (3) between documents check that every story has at least one requirement and every requirement a story or glossary term, that no two clauses contradict, that each term is used in one sense; (4) by execution run every example and scenario against its stated expectation; (5) stop and report every gap in the RPT-2 form; a person rules on each gap | review (agent) running `/audit-spec`, or review (human); rulings by a person | `reports/audit-NN.md` | SQ is not established while a gap is open; amendments are made and the audit rerun |
| SQ-3 | obligation | SQ | Every requirement MUST state one of the six EARS patterns in its `Pattern` field and MUST have that pattern's shape: a trigger where the pattern has one, the stage or the guard as subject, and "shall" | review within SQ-2 at A1; analysis by a script at A2 | the EARS section of the audit report | the clause is rewritten before any test cites it |
| SQ-4 | obligation | SQ | Every domain term used in a specification MUST be defined exactly once in `specs/glossary.md` and used only in its defined sense; no other specification MUST define a term | review within SQ-2 (a person, then the agent, then the skill); analysis by a script at A2 | the glossary section of the audit report | the term is defined or the sentence is rewritten |
| VAL-2 | form | VAL | The validation record MUST state, per user category: who walked, in which role, when, against which realization version, which stories, with which scenario inputs, what was observed, and the decision to sign or to withhold; it is produced before the sign-off and read by the auditor | review (human) | `reports/validation.md` | VAL is not established |
| TR-2 | form | TR | At every commit `tools/trace.py` MUST write `reports/trace-matrix.md`: forward (story to requirements to scenarios to tests), backward (requirement to story; test to clauses), findings; the findings section MUST be empty | analysis: the exit code of `tools/trace.py`, run by the gate | `reports/trace-matrix.md` | the gate is red; the reference is corrected |
| RPT-2 | form | the record of SQ | A gap list MUST carry: audit identifier, date, auditor (person, agent, or skill with version), specifications and versions audited, checks applied; one row per gap: identifier, location (clause or section), check violated, quoted text, proposed resolution, ruling (open, accepted, rejected with reason, deferred), amendment | review (human) | `reports/audit-NN.md` | the report is completed before rulings are given |
| WF-2 | procedure | VAL and SQ | To revise the concept of operations with its stakeholders, run `/elicit` or follow its steps by hand: (1) read it, the glossary, and the existing elicitation record; (2) ask at most five questions, one at a time, each addressed to a user category, with options and a recommended default; (3) record each question and the verbatim answer, with who answered and when, under an E identifier; (4) apply each accepted answer to the part of the specification it affects, citing the identifier; (5) the person reviews the resulting diff and runs `/audit-spec` before the revision is committed | review (human) of the record and the diff; the audit that follows | `reference/elicitation.md`; the dev-log entry | the revision is not committed |

Amendments to A0 rules, each with a one-line changelog entry at the end of `process/rules.md` (this changelog is the lightweight precursor of A3's change control):

- **SQ-1**: scope now names the four specifications; "Terms" becomes `specs/glossary.md`.
- **CONF-1**: scope now includes stories, whose citing tests are the scenario tests; add "and the loader MUST run every scenario in `specs/scenarios.json`".
- **CONF-2**: wording unchanged; evidence field reads "a walkthrough record; no clause carries method walkthrough at A1, so none is required"; this is said out loud in L2 (the clause climbed; the rule waits for A2's review clauses).
- **TR-1**: the "derived from" part is now decided by `tools/trace.py`; `Glossary:` and `Source: E-n` references are permitted forms.
- **WF-1**: the gate runs `ruff`, `pytest`, then `trace.py`.
- **RPT-1**: a ledger table per named checkpoint, not only per version.

Not added, on purpose: a staleness rule (A2, with the tool that applies it), a change-control rule for the scenario file (A3; the file's `governance` field and SQ-2 step 4 carry the convention until then), a reason-on-judgment-clause rule (no judgment clause exists at A1; the check is an SQ-2 step and the `Reason` key is defined so A2 can enforce it). Rules are earned.

---

## 8. The skill `/audit-spec`

`.claude/skills/audit-spec/SKILL.md` (MIT, as configuration): frontmatter with name, a description that triggers on "audit the specifications", and version `1.0`. Body: the five steps of SQ-2 in order, with the constraints that make rung 3 different from rung 2: read every file under `specs/` completely before the first check; for every finding cite the clause identifier or the section and quote the text; apply `checklist.md` item by item and say for each whether it passed, so that a run reports what it checked and not only what it found; never amend a specification; write the report from `gap-report-template.md` with the skill's version in the auditor field; stop.

`checklist.md`: the per-step checks, including the two negative rules that prevent the over-report: an implementation choice the specification leaves open is not an ambiguity; a deployment assumption is a finding only when it is written as a requirement. `gap-report-template.md`: the RPT-2 form.

The skill's first run is audit 3 in section 6. Its known-violation set is the draft under `reference/drafts/`; the README says that any change to the skill is rerun on the draft and must still find G1 to G7 and not the false one.

---

## 8a. The skill `/elicit`

`.claude/skills/elicit/` (MIT, as configuration), modeled closely on Spec
Kit's `speckit-clarify` and written in the house style of the course's
`conops-from-sketch` skill. Front matter: `name: elicit`; a description that
says when (the developer asks to elicit or revise a concept of operations
with its stakeholders) and when not (not for requirements, not for auditing,
not for explaining what a ConOps is); `argument-hint: "[path to the concept
of operations, default specs/conops.md] [optional focus]"`;
`disable-model-invocation: true`; `allowed-tools: Read Grep Glob`, so that
the writes prompt for permission, which is itself a visible approval moment;
an `agents/openai.yaml` beside it for Codex.

The body, step by step, with the adaptation from clarify named:

1. **Read** the concept of operations, `specs/glossary.md` if present, the
   existing `reference/elicitation.md`, and `process/rules.md`. Deference to
   the repository: WF-2 governs the procedure.
2. **Coverage scan** against a ConOps taxonomy (bundled as `taxonomy.md`)
   that replaces clarify's ten feature categories, each rated Clear,
   Partial, or Missing: purpose (what the system is for; agreed by whom);
   scope and boundary (inputs, outputs, what is outside); environmental
   assumptions; user categories (who, what each observes); stories (at least
   one per category, each with a concrete example); terms (undefined words;
   unquantified adjectives such as "sensitive" or "large"); wants and
   non-goals (mentioned, not promised); validation (who can sign).
3. **A queue of at most five questions**, ranked by impact times
   uncertainty, each answerable with a letter or at most five words. A fact
   the repository answers is looked up, not asked (grill-me's July 2026 rule,
   with its reason: a question the repository answers wastes a stakeholder's
   attention); implementation questions are excluded.
4. **One question at a time**, addressed to a named user category:
   `**Question:**` as a full interrogative; one "Why it matters" sentence;
   `**Recommended:** Option X - reason`; the options table A to E plus
   Short; the reply line. The writing rules are clarify's step 5, bundled as
   `question-format.md`.
5. **After each accepted answer, immediately** (Q13, decided): append an
   `E-n` entry to `reference/elicitation.md` from `record-template.md`
   (question, why it matters, options, the recommended one, the answer
   verbatim, who answered in which role, when, consequences); then apply the
   answer to the part it affects (a purpose sentence, an assumption, a user
   category's "observes" line, a story and its example, a deferred want, a
   glossary entry), replacing contradicted text rather than adding to it, and
   save after each integration. No approval stop inside the skill: the person
   reviews the whole diff at the completion report, and `/audit-spec` runs
   before the commit, since SQ-1 holds at every commit.
6. **Validation after each write**, as clarify's step 7: one E entry per
   accepted answer; no contradictory text left behind; only the allowed
   headings added.
7. **Completion report**: questions asked and answered; sections touched;
   a coverage summary (Resolved, Deferred, Clear, Outstanding); the next
   steps named as `/audit-spec`, then the validation walkthrough and the
   sign-off (VAL-2, VAL-1).

Deliberately not carried over from clarify: the extension-hook machinery; the
checklist re-validation (the audit skill is the next step instead); writing
the record into the specification (the course files it under reference, with
the stakeholders' words verbatim).

Evaluation, in the manner of the skills lecture, recorded on the skill's
catalog page `tooling/skill-elicit.md`: three runs on the A0 concept of
operations; the number of questions each asked; whether the queue reached the
five areas the A1 story needs (terms, assumptions, wants, the payload domain,
what a sender observes on a drop); and any run that wrote a decision nobody
gave. The run that produces `reference/elicitation.md` is a fourth, real run
with the instructor answering.

---

## 9. Tooling: the catalog (CF-14 by supplementary material)

No lecture time goes to building the assurance tooling. Instead v1 carries a
**tool catalog**, `tooling/`, that a student reads to set up the same tooling
in their own project or to build infrastructure shared across projects, and
L2 carries a sidebar on the philosophy (section 11.3). The design doc's CF-14
completion check ("lecture plans must allocate explicit time") is amended
accordingly (section 12). The catalog is prose (CC BY 4.0); the tools stay
MIT.

### 9.1 `tooling/README.md`, the catalog

Two paragraphs: the shift of effort (from writing code to building the
environment and tooling that directs agents and reports on whether the code
and the process meet the goals), pointing at the sidebar; and how to read a
page. Then one table, one row per tool:

| Tool | Kind | Goal (one sentence) | Decides or supports | Reads | Writes | A0 or A1 | Page |
|---|---|---|---|---|---|---|---|
| `tests/conformance.py` | program | read the identified clauses and their fields from the specifications, so that no report depends on a hand-kept list | SQ-1 (well-formedness), TR-1 | `specs/*.md`, `specs/scenarios.json` | clause records; findings | A0, extended | `tooling/clause-reader.md` |
| `tests/conftest.py` | program (pytest plugin) | turn test citations and outcomes into requirements coverage, and fail the run on missing or failing evidence | CONF-1, TR-1 | citations, outcomes | `reports/conformance.md` | A0, extended | `tooling/conformance-plugin.md` |
| `tools/gate.sh`, with the pytest and coverage settings in `pyproject.toml` | configuration | one command that decides RQ and the mechanical part of CONF and TR with an exit code | WF-1, RQ-1, CONF-1, TR-2 | the repository | an exit code; a provenance header | A0, extended | `tooling/gate.md` |
| `tools/walk.py` | program | let a person exercise one message in a role and see what the guard does | VAL-2 (in A0, CONF-2) | one message | one line | A0 | `tooling/walkthrough-helper.md` |
| `tests/test_scenarios.py` | program | run every scenario in the fixture file as a test that cites its story | CONF-1 | `specs/scenarios.json` | outcomes | A1 | `tooling/scenario-loader.md` |
| `tools/trace.py` | program | resolve every declared link in both directions and report the ones that do not resolve | TR-2 | the specifications, the citations | `reports/trace-matrix.md`; an exit code | A1 | `tooling/trace.md` |
| `tests/tooling/` | program (tests of the tools) | show each tool failing on inputs it must fail on, before its findings are trusted | the trustworthiness of CONF and TR evidence | case directories | outcomes | A1 | `tooling/tooling-tests.md` |
| `.claude/skills/elicit/` | agent procedure | obtain a concept of operations from its stakeholders in at most five questions and record their words | WF-2 | `specs/conops.md`, the glossary, the record | the record, the ConOps, the glossary | A1 | `tooling/skill-elicit.md` |
| `.claude/skills/audit-spec/` | agent procedure | audit the specifications by a fixed procedure and report gaps in a fixed form, under a version | SQ-2, RPT-2 | `specs/` | `reports/audit-NN.md` | A1 | `tooling/skill-audit-spec.md` |
| `build-history.sh` (if Q7(a) stands) | program | replay the snapshots into a tagged history, labeled as a reconstruction | none | `v0/`, `v1/reference/history/` | a git repository | A1 | `tooling/replay.md` |

### 9.2 One page per tool

Every page has the same seven headings, so that a student can compare the
tools and can write a page for a tool of their own:

1. **Goal.** The question the tool answers, for whom, and which rule names
   it as decider or as evidence.
2. **Requirements.** Numbered: inputs; outputs; the findings it reports; exit
   code; determinism; what it does not decide and what still needs a person.
3. **The prompt.** For a tool new in A1, the prompt actually used, verbatim,
   plus the layout the agent proposed and the instructor approved. For a tool
   inherited from A0, the prompt that would produce it, labeled as guidance,
   with the provenance chain the design records (the seed rules, Spec Kit
   research decision R7, tasks T004 to T006, commit `4d6a2cd`, A0 dev-log
   entry 2).
4. **Review points.** What to check in the agent's proposed design before
   accepting it: identifiers are read from the specifications and never from
   a hand-kept list; a clause with no evidence fails the run; a partial run is
   labeled; the report states its scope and the tool's version.
5. **Deliberate-failure checks.** The inputs the tool must fail on or must
   report, where they live (`tests/tooling/cases/` or a README sabotage), and
   how to run them.
6. **Adapting it to your project.** What is project-specific (the clause
   header regex, the specification file list, the marker name, the coverage
   threshold, the language and test framework) and what carries over as an
   idea.
7. **Making it shared infrastructure.** How to package it (a pytest plugin
   distributed as a package; a template repository; an organization skill),
   what to version, and why a shared defect misleads every project that uses
   it.

### 9.3 The trace tool's page, the worked example

`tooling/trace.md` is written before the tool is prompted for. Its
requirements (plain numbered items T1 to T8, not plugin-read clauses at A1;
decision Q8 asks whether they become identified clauses in A2's framework
session):

- T1 Inputs: the clause headers of `specs/conops.md` and `specs/requirements.md` through `tests/conformance.py`; the scenarios of `specs/scenarios.json`; the E identifiers of `reference/elicitation.md`; the citations of the suite, obtained by running `pytest --collect-only -q --no-cov` with the conformance plugin's collection hook (no second marker parser).
- T2 Output: `reports/trace-matrix.md` with a header (tool version, files read, git HEAD if available and whether the working tree was clean), the forward table, the backward table, a findings section, and a scope line.
- T3 Findings, each with the identifier and the file: dangling `Derived from`, `Scenarios`, `Source`, or marker; duplicate identifier; malformed header (identifier without `Method`); unsupported method or key; story with no requirement; requirement with no story or glossary derivation; `test` clause with no citing test (reported here as a link finding; the plugin reports its outcome).
- T4 Exit code non-zero if the findings section is non-empty; zero otherwise.
- T5 No judgment: the tool reports links and their resolution, never whether a link is semantically right; the README says which questions still need a person (does the requirement say what the story says; does the test's assertion check the clause).
- T6 Determinism: same inputs, same report except the date line.
- T7 Verified on `tests/tooling/cases/`: one minimal specification set per finding kind, with the expected findings; the tool must report each.
- T8 Runs under `uv run python tools/trace.py` from the snapshot root and is the last step of `tools/gate.sh`.

The prompt, retained on the same page under "The prompt": it hands the agent T1 to T8 and `tests/conformance.py`, asks for a proposed layout first (what is read, what is computed, what is reported) and a list of cases for T7, and says to wait for approval before implementing. The approved layout and the agent's completion message are kept with it, labeled as the agent's description, not evidence. The page's remaining sections are filled from the build: the review points are the questions the instructor asked of the proposed layout, and the adapting section names the three things another project changes (its identifier families, its specification file list, and the citation mechanism of its test framework).

### 9.4 The conformance plugin's page: checks of the evidence machinery (CF-01, CF-06)

`tests/tooling/test_trace.py` runs the tool over each case directory and asserts the expected findings (automated); the cases are listed on `tooling/trace.md` under "Deliberate-failure checks". The plugin's four CF-01 behaviors are scripted demonstrations on `tooling/conformance-plugin.md` and in the README under "Breaking the verifiers", not tests, because they need a run of the whole suite: an uncited passing test is accepted (add one, gate green, the report's cited-test count unchanged); an invalid citation is rejected (the A0 dangling-marker sabotage); a `test` clause with no citing test is a coverage gap (delete `test_public_passes_unchanged`); an uncited failing test fails the gate while every clause row stays green (add `def test_uncited(): assert False`). The last one is the demonstration CF-08 needs again in A2, so its wording is written once here.

### 9.5 Provenance in practice (CF-07, the explanation the instructor asked for)

What it would mean to accept CF-07, concretely and minimally. A piece of evidence identifies the state it was produced from by three things: the artifacts' content, the verifier's version, and the command. At A1, by hand: the gate prints a header (date; `git rev-parse --short HEAD` or "no repository"; the number of modified and untracked files, so a run on a dirty tree says so; the versions of python, pytest, pytest-cov, ruff, and `trace.py`), and the dev-log entry for the commit copies that header. The ledger's provenance column cites the dev-log entry rather than restating the versions. That already satisfies "a reviewer can find the inputs and outputs of a checkpoint without an agent's completion message."

The mechanism, for A2's generated ledger: identify the checked working tree before the commit exists by its tree hash (`GIT_INDEX_FILE=$(mktemp) git add -A && git write-tree`, two lines), which is the same hash the commit will carry if nothing changes afterwards; the ledger generator records it and the ledger tool later compares the recorded hash with the current one to decide staleness. This is the HAMR-style attestation idea at the scale of a shell script, and it answers "do not infer a tag from the directory name" without needing a report to contain its own commit hash. Recommendation: the hand convention in A1, the tree hash in A2 (decision Q5).

### 9.6 Reused and new

Reused: `tests/conformance.py` (A0, from the Spec Kit demo) as the clause
reader, extended; the conformance plugin's collection hook for citations;
`tools/gate.sh` and `tools/walk.py`. New: `tools/trace.py`,
`tests/test_scenarios.py`, `tests/tooling/`, the scope line and the findings
in the plugin, the two skills. Unchanged: `pytest-cov`, `ruff`. Every catalog
page says which of these its tool is.

---

## 10. Build sequence: tasks, commits, and the gate at each

The build happens in a git repository initialized from the v0 snapshot ("v0: message guard, version A0", the baseline commit the design asks for). Every A1 commit passes the gate as it stands at that commit; the dev-log entries 4 to 9 correspond to commits, which A0's entries could not. The final working tree is copied to `v1/`.

| Task (dev-log entry) | What is done | Files | Gate at the commit | Ledger |
|---|---|---|---|---|
| 4 · Build and run `/elicit` | Write the skill (section 8a) and its catalog page; evaluate it three times on the A0 concept of operations and record the evaluation on the page; then run it for real with the instructor answering in both roles, which writes `reference/elicitation.md` and applies the answers to `specs/conops.md` and `specs/glossary.md` | `.claude/skills/elicit/`, `tooling/skill-elicit.md`, `reference/`, `specs/` | no commit yet (the audit of task 6 precedes it) | — |
| 5 · Draft | Finish the revised `conops.md` by hand where the run left it (stories still *walkthrough (human)*), have the agent rewrite the requirements in EARS with the retained prompt; seed G1 to G7; copy the draft to `reference/drafts/` | `specs/`, `reference/drafts/` | not run; the draft is never committed (SQ-1 is "at every commit", so the audit precedes the commit); the demo may run it to show REQ-5 "no evidence" as a symptom | — |
| 6 · Audit three times, rule, amend | Audit 1 by the instructor (timed); audit 2 by the agent with `reference/prompts/03-audit-adhoc.md`; write the skill; audit 3 with `/audit-spec`; rulings; amendments | `reports/audit-0{1,2,3}.md`, `.claude/skills/audit-spec/`, `tooling/skill-audit-spec.md`, `specs/`, `process/rules.md` (SQ-2, SQ-3, SQ-4, RPT-2, WF-2; SQ-1 and TR-1 amended) | **commit 1, `a1-specs`**: A0's gate, green (REQ-0 to REQ-3 keep their citing tests; US-1 to US-3 still walkthrough) | table "At a1-specs": SQ established (skill 1.0 + rulings); RQ established; CONF renewed by rerun, with the note that the assertions were re-read; VAL **stale**; TR renewed (markers by the plugin, derivations by a person) |
| 7 · Scenarios | Write `scenarios.json` from the stories and the record; the loader; extend the plugin (scope line, story rows, findings); flip the stories' method to *test*; amend CONF-1 and CONF-2 | `specs/scenarios.json`, `tests/test_scenarios.py`, `tests/conformance.py`, `tests/conftest.py`, `specs/conops.md`, `process/rules.md` | **commit 2, `a1-scenarios`**: green; 16 tests (10 plus 6 scenarios); 7 of 7 test clauses with evidence | not written (the dev log records the run) |
| 8 · Trace tool | Write `tooling/trace.md` (T1 to T8) before prompting; approve the layout; build `trace.py` and `tests/tooling/`; fill the page's remaining sections; add to the gate; add TR-2, amend WF-1 | `tooling/trace.md`, `tools/`, `tests/tooling/`, `process/rules.md`, `reports/trace-matrix.md` | **commit 3, `a1-trace`**: green; the matrix has no findings | not written |
| 9 · Validate, sign, catalog, close | Walk the stories per user category on the running system with the scenario inputs; sign for A1; write `reports/validation.md`, the ledger at v1, the README, `CLAUDE.md`; add VAL-2; `pyproject.toml` version; write `tooling/README.md` and the remaining catalog pages (clause reader, plugin, gate, walkthrough helper, scenario loader, tooling tests, replay) | `reports/`, `tooling/`, `README.md`, `CLAUDE.md`, `process/rules.md`, `pyproject.toml` | **commit 4, `v1`**: green | table "At v1": five rows established, new provenance |

Order matters in two places. The stories' method flips only in task 7, so that commit 1 is green under A0's gate without scenario tests. The trace tool enters the gate only in task 8, so that commits 1 and 2 are judged by the gate that existed when they were made; the dev log says so, which is itself the CF-07 point. The two sidebars (section 11.3) are written after v1 is closed, from the catalog and the `/elicit` evaluation; they live under `lecture-notes/`, not in the snapshot.

`build-history.sh`: a minimal replay that creates the baseline commit from `v0/`, then one commit per task 6 to 9 by overlaying the files each task touched. The overlays are derived from the v1 build's actual commits (`git diff` per commit, stored under `v1/reference/history/`). Labeled as a reconstruction. Decision Q7 asks whether to ship it with A1 or defer it to A2; the plan assumes A1, because A1 is the first version whose history is worth replaying.

---

## 11. Breaking it, and the lectures

### 11.1 The A1 sabotages (README "Breaking it", continued from A0's five)

6. **SQ, a contradiction after the audit.** Add to `requirements.md` a REQ-6, in good EARS form, "When the filter receives a message whose security level is Restricted and whose payload is greater than 100, the filter shall produce no output," with method *test* and a test that cites it and passes against a two-line patch. Run the gate: green (every clause has evidence, coverage holds, every link resolves). Run `/audit-spec`: REQ-6 contradicts REQ-2 and SC-4. Only the audit catches it; the gate checks what is cited, not what is consistent. Restore.
7. **CONF and T5, a shared misreading.** Replace `filter.py` and `test_filter.py::test_restricted_passes_unchanged` together so that both treat "unchanged" as "same level, payload normalized to non-negative" (the agent that wrote both read the word the same wrong way). The unit test passes; SC-2's person-authored expectation fails; the gate is red. The verifier with independence from the author catches it. Restore.
8. **TR, a wrong derivation.** Change REQ-3's `Derived from: US-1` to `US-2`. The plugin is green (markers resolve). `trace.py` is green too, because the link resolves; the matrix now shows US-1 with no requirement, which is a finding, and the gate is red. Then change it to `US-9`: dangling, a different finding. Restore.
9. **VAL, scenarios pass and the officer declines.** No command. The officer reads the revised concept of operations and says Restricted messages with a payload above 100 must not leave. Every scenario passes, including SC-4 which encodes the opposite. The sign-off is withheld; VAL is not established; nothing else moves. The resolution in A1 is a scoped sign-off: the want is D-2 and the officer signs "for version A1, with D-2 deferred." The unscoped version of this is A3's change request.
10. **A verifier that has never failed (tooling).** Delete one case from `tests/tooling/cases/`; nothing fails, and the README says why that is the threat: a finding kind with no known-violation case is a finding kind nobody has seen the tool report.

### 11.2 Lecture mapping

The instructor's split, with timings for 75-minute blocks and the tooling time CF-14 requires made explicit.

**L2, The concept of operations: why we write it, its format, how we get it, what we do with it** (about 70 minutes of content):

| Segment | Minutes | Content | Uses |
|---|---|---|---|
| Why we write a ConOps | 7 | the question L1 left (how could the author have found out what the officer wanted); the governing document; the one specification a non-programmer can read and sign; the agent's first read | A0 `conops.md` |
| The format | 15 | the A1 ConOps section by section: the agreed purpose; scope and boundary with assumptions; user categories and what each observes; stories with examples and their header fields; deferred wants; the terms as the glossary; what is contextual text and what is a clause | `specs/conops.md`, `specs/glossary.md` |
| How we get it: `/elicit` | 20 | the coverage scan; five questions live (captured fallback); each answer landing in the file and in the record; reference versus specification; grill-me compared with `/elicit`, two slides from the sidebar | `.claude/skills/elicit/`, `reference/elicitation.md`, the sidebar |
| What we do with it, 1: validation | 10 | walkthrough per user category; the sign-off scoped to a version; scenarios pass and the officer may still decline (CF-04; sabotage 9) | `reports/validation.md` |
| What we do with it, 2: fixtures | 13 | stories to scenarios to the loader; values versus interface; under-approximation; independence (sabotage 7); the climb, with the sign-off kept | `specs/scenarios.json`, `tests/test_scenarios.py` |
| What we do with it, 3: a preview | 5 | the requirements derive from it (L3); the audit; the ledger after the revision, VAL stale; Exercise 2 launch | `reports/ledger.md` |

**L3, From the concept of operations to requirements: EARS, the audit, traceability** (about 70 minutes):

| Segment | Minutes | Uses |
|---|---|---|
| Derivation: what a requirement adds to a story; the chain US to REQ to test, and US to SC to test | 10 | `reports/trace-matrix.md` |
| EARS: the six patterns, REQ-0 to REQ-3, the `Pattern` field, which patterns later versions need | 16 | `specs/requirements.md` |
| The audit: SQ-2 and RPT-2; the draft with seeded gaps; a five-minute human audit by the room; the agent's audit and its over-report; the skill; rulings; amendments; threats T1 and T2 | 30 | `reference/drafts/`, `reports/audit-0{1,2,3}.md`, `.claude/skills/audit-spec/` |
| The trace matrix as evidence, and a pointer to the catalog page that shows how the tool was built (no lecture time for building it) | 3 | `reports/trace-matrix.md`, `tooling/trace.md` |
| Sabotages 6 and 8; the dev log as commits; the v1 ledger | 8 | `README.md`, `reports/dev-log.md` |
| Exercise 3 launch | 3 | |

Why the audit sits in L3 rather than L2: the audit's checks are mostly about the requirements (EARS form, derivation, the leaked want in REQ-1), its seeded gaps need the EARS material to be readable, and L2 is already carrying elicitation and fixtures. If a third meeting is available, the cleanest cut is L3a (derivation and EARS, 35 minutes, plus a longer live audit) and L3b (the audit as a verifier ladder, the trace tool), which gives the live audit room to run twice.

Exercises, sketched: **Exercise 2** (after L2): run `/elicit` on a system of the student's own (or on the guard with D-1 as the want): the record, a revised concept of operations, a glossary, a scenario file, a validation record; then evaluate the skill the way the skills lecture evaluates one (three runs; which taxonomy areas it reached; any decision it took without asking) and propose one change to its taxonomy. **Exercise 3** (after L3): on a copy of v1, seed three gaps of three different kinds, run a human audit and `/audit-spec`, compare; add one finding kind to `trace.py` (an unused glossary term) with its case under `tests/tooling/cases/`; and, from its catalog page, build one v1 tool for another language or project and write the page for it.

Deliverables after the build, following the module's three-artifact layout: lecture notes for L2 and L3 with the two sidebars of 11.3, `demo-script-lecture-02.md` and `-03.md` (setup from `v1/`, overlay of `reference/drafts/` for the audit segment, restores after each sabotage), and the two decks built the way `build-lecture-01.py` builds the first.

### 11.3 Two sidebars beside the L2 notes

Both live in `../module-ase-principles/lecture-notes/`, beside the existing
sidebar `ledger-evolution-example.md`, and are linked from the L2 notes.

**`sidebar-elicitation-grill-me-vs-elicit.md`** (one to two pages). A
side-by-side table, then an argument.

| | `grill-me` (as shipped to students) | `/elicit` |
|---|---|---|
| Purpose | a developer stress-tests their own plan or design | a stakeholder's intent is obtained for a governing document |
| Bound | none: "interview me relentlessly"; sessions of about 45 minutes in its author's own use | five questions per session; retries of one question do not count |
| What decides the questions | walking every branch of the design tree | a coverage scan of the document against a fixed taxonomy, ranked by impact times uncertainty |
| Form of a question | open; later versions ask several per round | one full interrogative, one "why it matters" sentence, a recommended option first, lettered options a non-programmer answers with a letter or five words |
| Addressee | the developer | a named user category, in their words |
| Record | none; the answers live in the chat transcript | `reference/elicitation.md`: the question, the verbatim answer, who answered, when, and the consequence, under an identifier the specification cites |
| Where the answer lands | wherever the agent decides | in the section it affects, visibly, as each answer is accepted; the person reviews the diff; the audit follows |
| End state | none | a completion report: resolved, deferred, clear, outstanding |
| Facts versus decisions | facts looked up in the repository (since July 2026) | the same rule, with its reason stated |
| Portability | "Call the Skill tool" binds to one harness | harness-neutral wording; an `agents/openai.yaml` beside it |

The argument: both are legitimate; grill-me is for a developer's own design
decisions, `/elicit` for a stakeholder's intent. The students were
overwhelmed because an unbounded design interview was pointed at a
stakeholder-facing document, where every question costs a stakeholder's
attention and where a guess written down becomes a requirement nobody
decided. The cap, the ranking, and the recommended default change what one
session can be expected to produce and let a stakeholder answer in one word.
The yardstick is the skills lecture's own criteria (stops where a human
decides; concrete over adjectival; reasons with the rules; deference to the
repository); the sidebar draws on the grill-me history that lecture already
records and on the `/elicit` evaluation from `tooling/skill-elicit.md`.

**`sidebar-tooling-as-engineering.md`** (one to two pages). The shift of
effort stated for tooling: with agentic development, effort moves from
writing code to building the environment and tooling that directs agents to
build the code and reports on whether the code and the development process
meet the goals. What counts as assurance tooling (readers, checkers, report
writers, gates, agent procedures). The v1 tool table (tool, goal) from the
catalog. How to read a catalog page. The organization model: a shared
foundation maintained by an infrastructure team, product teams supplying
specifications, tests, and configuration; versioned releases and controlled
updates. What to do in your own project: start with the gate and one report;
add a tool the second time you do a check by hand. A pointer to
`v1/tooling/`.

---

## 12. Documents outside `v1/` to update with A1

- `../module-ase-principles/demos/running-example-message-guard/README.md`: the A1 row from "planned" to built; the replay note.
- `../module-ase-principles/README.md`: A1 complete; lectures 02 and 03 drafted when they are.
- `running-example-design.md`: the status header (A1 built); section 9 dispositions and completion evidence for CF-01 to CF-07, CF-13, CF-14 (section 14 below); CF-14's completion check amended: no lecture time is allocated to building tooling, v1's catalog and the L2 sidebar carry it; section 8 item 1 amended: the redesigned elicitation procedure is `/elicit`, modeled on clarify; open decision 3 (audit log) noted as "recorded as deferred want D-1 in A1; version still undecided."
- `../specification-kinds.md`: the glossary promoted to a kind; *user categories* for *user classes*; a "first needed by" column; the fixture entry pointing at `scenarios.json` as the course's second instance (deferred since A0; this is the version that makes two of the three changes real).
- `../process-rule-styles.md`: create with the four styles now in use (obligation, gate, procedure, form) and the template, the principles, and the design grid, leaving the other three styles as headings to be filled at A2 and A3. Or defer the whole handout to A2 (decision Q9).
- `../glossary.md`: no change expected; verify the *elicitation record*, *known-violation set*, and *independence* entries read correctly against what A1 built.
- The course `CLAUDE.md` demos index, if it lists versions.

---

## 13. Decisions to settle before building

Numbered Q so they do not collide with the other plan's numbering. Each has my recommendation; the plan above assumes the recommendation. Q3 and Q13 were decided by the instructor on 2026-10-22; Q1, Q2, and Q4 to Q12 stand as recommended unless overridden.

| # | Decision | Options | Recommendation and reason |
|---|---|---|---|
| Q1 | The stories' verification method at A1 | (a) flip to *test* via the scenarios, so CONF-2 has no clause in scope; (b) keep *walkthrough (human)* on the story and make the scenarios separate *test* clauses | **(a)**. The design says the story walkthrough climbs to a test; (b) keeps the walkthrough doing double duty for CONF and VAL, which is the conflation CF-04 warns against. The empty CONF-2 is a one-sentence teaching point, not a defect |
| Q2 | Scenario identifiers as conformance-report rows | (a) no: the story is the clause, the loader cites the story, the matrix lists scenarios; (b) yes: SC-n are clauses with method test | **(a)**. Fewer identifiers, no double counting; the matrix still shows every scenario and its test. Reconsider at A2 if contracts want scenario-level citation |
| Q3 | Packaging of elicitation | (a) rule WF-2 plus a retained prompt, skill in Exercise 2; (b) a `/elicit` skill shipped in v1 | **Decided (b)** by the instructor, 2026-10-22: a skill modeled closely on Spec Kit's clarify (section 8a), with the comparison sidebar (11.3) explaining why it serves this job better than grill-me |
| Q4 | CF-05, partial-run labeling | (a) one scope line in the saved conformance report and the matrix; (b) also counts of cited and uncited tests; (c) defer entirely | **(a)**. One line, already computable from the plugin's existing flag, and it is the T3/T4 lesson in its smallest form. Defer (b) and any aggregate-consumer logic to A2 |
| Q5 | CF-07, evidence identity | (a) hand convention now (gate header copied into the dev log), tree hash in A2; (b) tree hash now; (c) nothing beyond A0 | **(a)**; section 9.5 says what each looks like |
| Q6 | CF-13, the integer payload and `bool` | (a) resolve by elicitation (E-4): the specification says integer and does not constrain language representation; no product change; (b) add an exclusion and a test | **(a)**. It is the better teaching example: a question the stakeholder cannot answer stays open at the specification level and is recorded as such |
| Q7 | Where the pre-audit draft lives, and the replay script | (a) `v1/reference/drafts/` plus a minimal `build-history.sh` with per-task overlays; (b) drafts only, script deferred to A2; (c) a sibling `v1-draft/` snapshot | **(a)**. The drafts are reference by definition; the replay is cheap once the build is done in git, and A1 is the first version with a history worth replaying. (b) is acceptable if time is short |
| Q8 | Tooling requirements as identified clauses | (a) plain numbered items on the tool's catalog page (`tooling/trace.md`) at A1; (b) a `process/tooling.md` with plugin-read clauses and citing tests now | **(a)**. A2's framework session is where the tooling gets its own clause family and report; doing it now would add a third report form to A1 |
| Q9 | `process-rule-styles.md` | (a) create at A1 with four of seven styles; (b) defer to A2 | **(a)**, because L3 is where the two new styles are first explained and the handout is where students will look them up; the empty headings are honest about what comes later |
| Q10 | The eighth rule | (a) leave the slot empty (seven rules); (b) add a known-violation-set obligation for every program in the gate | **(a)**. The design places that rule at A2 with the script; at A1 the cases exist (`tests/tooling/`) and the README states the convention. Rules are earned |
| Q11 | Who plays the stakeholders in the elicitation and the sign-off | (a) the instructor plays both, as in A0, stated in the record; (b) a second person for one role | **(a)** for the snapshot; the record and the sign-off say so. For the live L2 session, a student volunteer as the message sender is worth trying once |
| Q12 | Lecture split | (a) the instructor's two lectures, audit and trace in L3; (b) three meetings (L3a, L3b) | **(a)** unless the schedule has the room; section 11.2 gives the cut if it does |
| Q13 | Apply mode of `/elicit` | (a) apply each accepted answer immediately, as clarify does, the person reviewing the diff at the end; (b) collect the answers, propose amendments, stop for approval | **Decided (a)** by the instructor, 2026-10-22; WF-2 step 5 and the L2 demo follow it |

---

## 14. What the completion report must show

Per the design's instruction to identify the evidence satisfying each applicable item:

- **CF-01**: the four "Breaking the verifiers" demonstrations in the README with captured output; `tests/tooling/test_trace.py` passing.
- **CF-02**: the legends of `conformance.md` and `trace-matrix.md`, the audit template's header, and the ledger's closing sentence use "supports a scoped claim" wording; a grep for "proves" and "guarantees" across `v1/` finds nothing.
- **CF-03**: `diff -r v0/guard v1/guard` empty; `diff v0/tests/test_filter.py v1/tests/test_filter.py` empty; the README's table of generated versus handwritten files; the ledger handwritten.
- **CF-04**: `reports/validation.md` is a different file from the scenario tests; sabotage 9 in the README; L2 segment 6 in the demo script.
- **CF-05** (if Q4 accepted): run `uv run pytest -k message`; the saved report's first line says "partial run"; nothing in `v1/` consumes it as full-run evidence.
- **CF-06**: the eight case directories under `tests/tooling/cases/` with expected findings; `tooling/clause-reader.md` and `tooling/trace.md` state the parser scope; G6 in the audit reports; the REQ-2 identity question appears only as the rejected over-report.
- **CF-07** (hand convention): the gate header in dev-log entries 6 to 9; the ledger provenance cites those entries; no tag is cited that the repository does not have.
- **CF-13**: glossary entry *payload* and E-4 in the record.
- **CF-14**: `tooling/README.md` and one page per tool in the catalog table, each new tool's page carrying the verbatim prompt and the approved layout; `tooling/skill-elicit.md` carrying the three-run evaluation; `tests/tooling/`; the sidebar `sidebar-tooling-as-engineering.md`; the design doc's CF-14 check amended to say that no lecture time is allocated.
- **Design 2.7 and 2.9**: the glossary-discipline check appears in audits 1, 2, 3 with three different verifiers in their provenance; the purpose-statement check is marked "ceiling: rung 3" in `checklist.md`; sabotages 6 to 10 cover T1, T2, T3, T5 and the verifier-never-seen-to-fail point.
- **Unresolved or deferred**: the staleness rule, the change-control rule for scenarios, the reason-on-judgment-clause rule, the tree-hash mechanism, scenario-level citation, and F3's version, each with the version it is deferred to.
