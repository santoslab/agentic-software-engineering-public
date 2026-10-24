# Version A1 of the Message Guard: Build Plan

> Status: plan, 2026-10-22. Nothing in it is built. It implements the A1 row
> of option A in `running-example-design.md` (section 3), the section 9 items
> that apply to A1, and the A1 priorities in
> `../module-ase-principles/review-lecture-01-a0.md` (section 8). It assumes
> that A1 may be taught in two lectures: Lecture 2 on elicitation, the concept
> of operations, and fixtures; Lecture 3 on deriving requirements from the
> concept of operations, the EARS format, and the audit. The decisions in
> section 3 need answers before the build starts. Vocabulary follows
> `../glossary.md`.

## 1. New features in A1 and how each supports teaching

The product does not change. A1 is still the `filter` stage on a message
with a security level and an integer payload: a Critical message is dropped
and every other message passes unchanged. The single possible exception is
decision D4, rejecting a true/false payload, which would be the only product
change and would need approval. Everything else that is new is in the
specifications, the evidence, the tooling, and the process.

The features are grouped by the lecture that would use them. Under the
two-lecture split they land in two snapshots, `v1a/` and `v1/` (decision D2).

### Lecture 2, snapshot `v1a/`: elicitation, the concept of operations, the glossary, acceptance scenarios

1. **An elicitation procedure (rule VAL-2) and an `/elicit` skill.** These
   follow the protocol of Spec Kit's clarify. The skill scans the concept of
   operations against a fixed list of categories and asks at most five
   questions per session, one at a time. Each question is a complete
   sentence, followed by one sentence on why it matters, a recommended option
   with up to four alternatives, and the role (security officer or message
   sender) of the person who must answer. The skill shows each proposed edit
   to the concept of operations before applying it. It flags any answer that
   would change product behavior for explicit approval, and it never asks
   about the implementation.
   *Teaching:* answers the question Lecture 1 ends on: how could the author of
   `conops.md` have found out what the security officer wanted? It shows that
   intent can be consulted only through people, and that a bounded procedure
   can do it. This is the design's mitigation for threat T1 when the intent
   itself is unclear. It replaces the open-ended grill-me questioning that
   overwhelmed students. It also shows that a skill can package a procedure
   that is not a verifier, before `/audit-spec` shows one that is.

2. **The elicitation record, `reference/elicitation.md`, with the session
   transcript kept beside it.**
   *Teaching:* the first instance of the *reference* category. It holds the
   stakeholders' words verbatim, who answered in which role, and the options
   offered. It is not a specification, it is not audited, and no judgment is
   about it. It records the path from a stakeholder's answer to a sentence in
   the concept of operations. It also holds needs the stakeholders stated but
   that are not part of this version, such as limiting Restricted payloads or
   keeping a record of drops, without turning them into requirements. That
   shows that scope is a decision, not an omission.

3. **A revised concept of operations.** The purpose statement is agreed
   again. The scope section gains two subsections: *Assumptions*, which holds
   the no-bypass deployment assumption, and *Outside this version*, which
   holds the deferred needs. The user categories are unchanged. Each story
   gains examples chosen by equivalence class and boundary, and each example
   is named by a scenario identifier.
   *Teaching:* the four parts of a concept of operations in depth, with the
   quality criteria specific to it: implementation-independent, observable,
   terms defined, and self-contained. These criteria are reused from AUDCON-1
   to AUDCON-5 of `module-software-engineering` Lecture 02. It also teaches
   the difference between a requirement and an environmental assumption
   (review 8.1.E) and how to choose examples by equivalence class.

4. **A glossary, `specs/glossary.md`, and rule SQ-3 on glossary
   discipline.** The glossary replaces the Terms section of the concept of
   operations and adds the terms elicitation forces: *drop* (no output)
   versus *reject* (not a message at all); *unchanged* (same level and same
   payload, which is value equality, not object identity); and *integer
   payload*, which settles CF-13 or records it as open.
   *Teaching:* vocabulary is a specification with its own quality check: one
   term, one meaning, across the whole family of specifications. Glossary
   discipline is the check that climbs the verifier ladder in Lecture 3 and in
   A2. The *integer* entry shows a type from the realization language (in
   Python, `bool` is a subclass of `int`) leaking into a domain term.

5. **Acceptance scenarios (fixtures).** The file `specs/scenarios.json`,
   with a short document stating its shape, holds scenarios that the person
   (not the coding agent) derived from the story examples. The story tests,
   `tests/test_stories.py`, are parametrized over the file, and each row
   cites its story.
   *Teaching:* the design's "scenarios and tests: one concept, two bindings"
   (section 4A). A scenario binds values only; a test binds values and the
   interface. Scenarios under-approximate requirements: a scenario is one
   case, while a requirement covers all cases. Scenarios are governed on the
   specification side, so a wrong expectation is reported as a gap and never
   edited to make a test pass. They are portable, so a later Rust port must
   pass the same file. Because a person writes them rather than the coding
   agent, they are the first instance of independence (T5).

6. **The stories' verification method changes from walkthrough (human) to
   test, and the walkthrough moves to validation.** Rule VAL-1 is amended: a
   stakeholder of each user category walks the stories of that category
   against the running system and then signs the named versions of the
   specifications.
   *Teaching:* the verifier ladder on a whole clause group. Checking the
   stories' behavior climbs from a person to a program, while validation does
   not climb (design 2.7). The lecture demonstrates CF-04 directly: every
   story test passes while the security officer rejects a story.

7. **A real cycle of stale and re-established judgments.** The ledger keeps
   its v0 section. It adds a section for the state after the revision, which
   lists the stale rows and the reason for each, and a v1a section, which
   shows the rows re-established and names the verifier for each.
   *Teaching:* establish and stale shown on actual artifacts rather than on
   the hypothetical sidebar. A revision that changes no product code still
   makes SQ, CONF, VAL, and TR stale. RQ also goes stale, because the tests
   changed.

8. **(Only if D4 is decided as (b).) One approved behavior change found by
   elicitation:** a true/false payload is rejected. This takes an amended
   REQ-0, one scenario, one test, and one condition in `guard/message.py`.
   *Teaching:* elicitation finds an in-scope question that A0's reading
   missed (T1, limited capacity). It shows a specification change
   propagating to the code, tests, scenarios, and ledger, and it uses the
   approval path that CF-13 prescribes.

### Lecture 3, snapshot `v1/`: from the concept of operations to EARS requirements; the audit; traceability

9. **Requirements rewritten in EARS.** Each requirement is derived from a
   story or from a glossary term. REQ-0 is split into REQ-0a (the three
   levels), REQ-0b (an integer payload; an unwanted-behavior pattern for
   anything else), and REQ-0c (a message does not change after it is
   created). REQ-1 to REQ-3 use the event-driven pattern. Rule SQ-2 requires
   every requirement to follow an EARS pattern.
   *Teaching:* how requirements are derived. One story can yield several
   requirements, and a glossary term can yield a requirement. The lecture
   covers the EARS patterns and why a fixed sentence shape leaves an agent
   less to guess. It shows completeness as a case analysis over the three
   levels, and it shows the general requirement behind each specific
   scenario.

10. **A structured specification audit.** Rule SQ-4 is a procedure: read the
    current files and record their versions; check within each document;
    check between documents; check by execution (run the trace tool and the
    story tests); then stop and report, never fixing anything. Rule RPT-2 is
    a form, the *gap list*, with these fields: gap identifier, check, location,
    quoted text, finding, proposed resolution, ruling, ruled by, and
    resolution.
    *Teaching:* an audit is a procedure together with a form. The agent
    reports, and a person rules on each finding; the two are separate steps.
    These are the two new rule styles of this version (procedure and form),
    within the budget of design 2.3.

11. **A copy of the requirements with eight defects deliberately inserted
    (the seeded draft), kept as the audit's known-violation set:**
    `audit/known-violations/` with `expected-gaps.md`.
    *Teaching:* a verifier is trusted only to the extent it has been seen to
    catch known defects (design 2.9). The same set is used again in A2 to
    check the script that replaces the skill. Whatever the person misses
    illustrates threat T1, the limited capacity of a reader. In class, the
    students can act as the rung-1 verifier themselves.

12. **The verifier ladder, rungs 1 to 3, on one check, ending in the
    `/audit-spec` skill.** The same seeded draft is audited three times: by a
    person following the checklist, by an agent given an ad hoc prompt, and
    by the packaged skill. Each result is compared with the known-violation
    set.
    *Teaching:* what each rung changes. Moving from a person to an agent
    trades the person's attention and capacity for the agent's
    nondeterminism and its tendency to answer from memory. Packaging the
    procedure as a skill fixes the steps but not the findings. The skill's
    first step is to read the current files before checking them. Running the
    skill twice on the same draft shows the same procedure producing
    different findings. This sets up rung 4 in A2.

13. **A trace matrix:** `tools/trace.py` writes `reports/trace-matrix.md`,
    runs in the gate, and falls under rule TR-2. Its links run in both
    directions: story to requirement to scenario to test. It reports stories
    that nothing derives from, references that resolve to nothing, and
    markers that name unknown clauses.
    *Teaching:* traceability as a computed report, and the limit of what it
    shows. It checks that declared links resolve, not that a link is the
    right one. One seeded defect is a derivation that resolves but points to
    the wrong story, and only the audit finds it.

14. **Requirements for the checking tools, and an implementation that an
    agent built and a person reviewed against them (CF-14).** The file
    `tools/requirements.md` has clauses TOOL-n for the clause parser, the
    trace report, and the gap-list format. The prompt, the agent's proposed
    layout, the review notes, and the implementation are all kept.
    *Teaching:* reports and gates are engineered artifacts with their own
    requirements. The lecture shows how to prompt an agent from such
    requirements, and which parts are read from the specifications, which are
    computed, and which remain a human judgment. It also shows checking a
    checker against malformed inputs before relying on it.

15. **Parser robustness (CF-06).** Duplicate identifiers, malformed clause
    headers, unsupported verification methods, judgment clauses with no
    stated reason, and derivations that resolve to nothing all become
    findings.
    *Teaching:* a verifier that silently skips an input can leave the report
    green. Demonstration: in v0, a clause with a malformed header and no test
    drops out of requirements coverage while the gate stays green; in v1 the
    parser reports it (threats T2 and T3).

16. **Demonstrations of the evidence machinery under optional citations
    (CF-01).** An uncited passing test (the fixture-shape test) is accepted.
    An invalid citation is rejected. A test clause with no citing test is
    reported as a gap. An uncited failing test turns the gate red while every
    clause row still reads pass.
    *Teaching:* clause-linked status, the suite result, and the gate result
    are three different things (review 8.1.B, consequence 3). A citation
    declares only that a test is intended to support a clause (CF-02).

17. **A second re-sign-off, after the EARS rewrite.**
    *Teaching:* a rewrite intended to preserve meaning still changes the
    documents the stakeholder signed. Under the conservative staleness rule,
    VAL goes stale, and the stakeholder must confirm that the meaning was
    preserved. This raises the question of finer-grained invalidation, which
    is deferred to A2 (CF-12).

**Process totals.** A1 adds six rules: SQ-2, SQ-3, SQ-4, VAL-2, TR-2, and
RPT-2. It amends seven: SQ-1, CONF-1, CONF-2, VAL-1, TR-1, WF-1, and RPT-1.
The two new styles are procedure and form. This is within the budget of eight
new rules and two new styles per version. A1 has two skills, a trace tool, and
the tooling requirements. The ledger stays handwritten (CF-03).

**What does not change.** The code in `guard/` (except under D4 (b)), the
user categories, the commit policy (the automated gate before every commit;
CF-15 keeps this until A2), RQ (`ruff` and test collection; `mypy` arrives in
A2), and the structural-coverage objective (100 percent branch coverage).

## 2. Constraints carried into A1

| Item | What it requires of A1 | Where this plan satisfies it |
|---|---|---|
| CF-01 (accepted) | test citations stay optional; four demonstrations of the evidence machinery | feature 16; steps 1.6, 2.14 |
| CF-02 (accepted) | report labels and lecture claims keep citation coverage, structural coverage, and assertion adequacy distinct; a failure triggers investigation, most likely of the specification or the implementation | step 2.2 (report legend); lecture notes |
| CF-03 (accepted) | handwritten ledger; product behavior preserved; no audit log, no negative-payload policy from Exercise 1, no API for "no input" | section 1, "What does not change"; step 1.7 check |
| CF-04 (accepted) | fixture tests check behavior, not intent; one validation walkthrough per user category; a fresh sign-off | features 5, 6; sabotage S2 |
| CF-14 (accepted) | requirements for the audit and trace reports; the lecture shows the agent building the tooling from them; prompts, plans, and checks kept | feature 14; step 2.3; Lecture 3 segment |
| CF-15 (accepted) | keep the simple per-commit gate in A1 | WF-1 is amended only to add the trace tool |
| CF-05, CF-06, CF-07 (proposed) | need a decision | D6, D7, D8 |
| CF-13 (open) | settle or record the question of true/false payloads | D4; elicitation question Q1 |
| Review 8.2 | say whether the gate is prescribed or enforced; identify what was checked; keep role names consistent (message sender, security officer, developer); keep scope; keep definitions consistent | WF-1 text; RPT-1 provenance; `/elicit` names the answering role |
| Design 2.3 | at most eight new rules and two new styles per version | six rules; procedure and form |

## 3. Decisions needed before the build

**D1. Production route: build A1 the way A0 was built, or through Spec Kit
(Option 2 of `speckit-mapping.md`)?** Recommended: build it the same way as
A0, and bring clarify's protocol into the course's own `/elicit` skill. If
the route changed at A1, `diff -r v0 v1` would mix the change of layout
(Spec Kit's single `spec.md` and its constitution) with the change of
content. Spec Kit's clarify, checklist, and analyze can still be shown side
by side with `/elicit` and `/audit-spec` in Lectures 2 and 3, as the
contrast that Option 1 of the mapping proposes.

**D2. One snapshot or two?** Recommended: two. `v1a/` holds the material for
Lecture 2. `v1/` is A1 complete, so that A2 still diffs `v1` against `v2`.
Each lecture then has a self-contained snapshot to run, and Lecture 2 does
not show EARS requirements before Lecture 3 teaches them. If A1 gets only one
lecture, `v1a/` stays as an intermediate snapshot and is not taught
separately.

**D3. The stories' verification method.** Recommended: change US-1 to US-3
to method *test*, with evidence from the story tests over the scenarios, and
move the walkthrough under VAL-1 as a validation walkthrough per user
category. This is what design 2.7 and Lecture 1 describe: checking behavior
climbs the ladder, and validation does not. One consequence is that A1 has no
product clause with method walkthrough or review. CONF-2 then applies to no
clause until the allocation table arrives in A2, and the lecture should say
so. The alternative is to keep the stories as walkthrough clauses and add
scenarios as separate test clauses. That keeps CONF-2 in use, but then
nothing climbs the ladder.

**D4. CF-13: is a true/false payload an integer?** The options are (a) keep
A1's behavior identical and record the question as open in the elicitation
record and the glossary, or (b) approve rejecting it as the one product
change in A1. Recommended: (b). An elicitation that changes nothing teaches
less, and this change is one condition, one scenario, and one test. It shows
that A0's person reading missed an in-scope question, and it follows CF-13's
approval path. Under (a), if the question is asked at all, the
stakeholder's natural answer ("a payload is a number") leaves a known
mismatch between the specification and the code. That mismatch must then be
recorded as such, never hidden behind a green ledger.

**D5. Should elicitation be a skill?** Recommended: yes, `/elicit`. The gentler
protocol has to be reproducible, and students will reuse it in their own
projects. Design 2.7 says skills enter at rung 3 of the verifier ladder. That
sentence should be qualified: a skill packages a procedure, and `/audit-spec`
is the first skill that is a verifier. The alternative is a prompt template
in `process/`, together with rule VAL-2.

**D6. CF-06: parser and trace-input robustness.** Your note proposes to accept
it. Recommended: accept it, limited to the shared clause parser and the trace
tool, built from the tooling requirements in step 2.2. It also supplies
demonstration S4.

**D7. CF-05: labeling runs in which some tests were deselected.** Recommended:
add one line at the top of the saved conformance report: "Run scope: partial,
tests were deselected; this report is not evidence that CONF-1 holds." It
costs a few lines in the plugin and removes the case where the terminal said
"partial" but the saved file did not. Leave the behavior of tools that
consume the report, such as a generated ledger, to A2.

**D8. CF-07: reproducible evidence identity.** What accepting it would mean in
practice, in three parts:

1. *The identity of the checked inputs.* The snapshot is checked before it is
   committed, so the evidence cannot cite its own commit hash. A
   fingerprint of the content can stand in for it. For example, `git
   write-tree --prefix=<path>/v1/specs/` on the staged files gives the hash
   of the tree that `git rev-parse HEAD:<path>/v1/specs` will return after
   the commit, so a reader can check it. A sha256 manifest of the input
   files (`specs/`, `guard/`, `tests/`, `tools/`, `pyproject.toml`,
   `uv.lock`) does the same job without git. Generated files under
   `reports/` are excluded, because they change when they are written.
2. *Tool versions.* Read from `uv.lock` and `--version`; A0's provenance
   already records most of them.
3. *Retained output.* `tools/gate.sh` copies its full output to
   `reports/runs/<timestamp>-gate.txt`, and the ledger row cites that file.

This is close to an attestation in the HAMR sense, without the signature:
evidence bound to the identity of what it examined. Recommended: adopt parts
2 and 3 in A1. They are cheap, and they let the ledger cite an actual run
rather than a sentence describing one (T4). Defer part 1 to A2's generated
ledger, where the tool can compute the fingerprint.

**Defaults, unless you say otherwise.**

- Scenarios are stored as JSON, as in the course's existing fixture files,
  with a short Markdown document stating their shape. Each scenario has an
  identifier `SCN-n`, a `story` field, and a `requirements` field. Each story
  test cites only its story.
- REQ-0 is split as REQ-0a to REQ-0c, following the design's REQ-5a to 5c
  convention. The identifier pattern becomes `[A-Z]+-\d+[a-z]?`.
- The elicitation record begins at "starting point: `specs/conops.md` at v0,
  signed 2026-10-20". Any illustration of eliciting a first concept of
  operations from a request belongs in the lecture notes, not in the record,
  so that the record contains only what actually happened.
- The rung-1 audit in the build record must be blind. An agent inserts the
  defects from a list of defect types without saying where, and the
  instructor audits without the answer key. In class, the students are the
  rung-1 auditors.
- Tests of the tools live in `tests/tooling/` as uncited tests over known-bad
  inputs. The TOOL-n clauses are traced within `tools/requirements.md` and do
  not appear in the product's conformance report.
- The script that replays snapshots into a tagged git history is deferred to
  A2, where the checkpoint policy of CF-15 gives the replay a meaningful
  commit policy. Update the "planned with A1" line in the demo README to say
  so.
- The standing handout `process-rule-styles.md` (open decision 6) is deferred
  to A2, when five of the seven styles have guard examples.

## 4. Snapshot contents

`v1a/` starts as a copy of `v0/` without `.venv`, `__pycache__`, the pytest
cache, or the coverage data file. Legend: (new), (changed), (unchanged).

```
v1a/
  CLAUDE.md                       (changed) read the glossary; reference/ is not a specification; the skills
  README.md                       (changed) artifacts; judgments at this version; sabotages S1–S3
  pyproject.toml                  (changed) description and version
  .claude/skills/elicit/SKILL.md  (new)     elicitation procedure, with a version line
  reference/elicitation.md        (new)     the session record; deferred needs
  reference/transcripts/          (new)     the elicitation session transcript
  specs/conops.md                 (changed) purpose; scope with Assumptions and Outside this version; stories as test, with scenario IDs
  specs/glossary.md               (new)
  specs/scenarios.json            (new)
  specs/scenarios.md              (new)     shape; rules the scenarios assume; governance
  specs/requirements.md           (changed) derivation fields; REQ-0 if D4 (b)
  guard/                          (unchanged, or one condition if D4 (b))
  tests/test_stories.py           (new)     story tests and an uncited fixture-shape test
  process/rules.md                (changed) SQ-3, VAL-2 new; SQ-1, CONF-1, CONF-2, VAL-1, TR-1 amended
  reports/walkthrough.md          (changed) validation walkthroughs per user category; sign-off
  reports/ledger.md, dev-log.md, conformance.md   (changed)
  tools/                          (unchanged)

v1/  (a copy of v1a/, then:)
  .claude/skills/audit-spec/      (new)     SKILL.md (with a version line) and checklist.md
  audit/known-violations/         (new)     the seeded draft and expected-gaps.md
  reference/tooling/              (new)     prompt, agent's proposed layout, review notes (CF-14)
  specs/requirements.md           (changed) EARS
  tools/requirements.md           (new)     TOOL-n clauses
  tools/trace.py                  (new)
  tools/gate.sh                   (changed) adds trace.py; keeps its output (D8)
  tests/conformance.py            (changed) shared parser with findings (location per the agent's reviewed proposal)
  tests/conftest.py               (changed) parser findings; REQ-0a IDs; legend (CF-02); scope line (D7)
  tests/test_message.py           (changed) markers REQ-0a to REQ-0c
  tests/tooling/                  (new)     known-bad inputs and expected findings
  process/rules.md                (changed) SQ-2, SQ-4, TR-2, RPT-2 new; WF-1, RPT-1 amended
  reports/audit/                  (new)     gap lists: person, agent, skill runs on the seeded draft; skill run on the final specs
  reports/trace-matrix.md         (new, generated)
  reports/runs/                   (new)     gate output (D8)
```

Licensing: `reference/`, `audit/`, `specs/`, `process/`, and `reports/` are
CC BY 4.0. `tools/`, `tests/`, and configuration are MIT. Confirm that the
`SKILL.md` files fall under MIT as configuration.

## 5. Build steps

Every step records its dev-log entry under RPT-1, naming the task, the
files, the judgments touched, and the gate result. Agent sessions keep their
prompt and output. Results are recorded as they actually occurred, never
arranged to fit the lecture.

### Phase 0: before building

- **0.1** Record decisions D1 to D8 in the design document: the A1 row of
  section 3, the section 9 dispositions, and the qualification of 2.7 if D5
  is accepted.
- **0.2** Run `uv sync` and `tools/gate.sh` on v0 with the current toolchain.
  This is the baseline.
- **0.3** Create `v1a/` from `v0/` as described in section 4.

### Phase 1: `v1a/`

- **1.1 Rules.** Write VAL-2 and SQ-3 in the template form. Amend SQ-1,
  CONF-1, CONF-2, VAL-1, and TR-1 as in section 8.
- **1.2 The `/elicit` skill.** It contains:
  - the list of categories it scans: purpose; boundary (inputs, outputs,
    what is outside); assumptions about the environment; user categories;
    story coverage per user category; example choice per equivalence class
    and boundary; terms; deferred needs;
  - the rating of each category as clear, partial, or missing;
  - the cap of five questions, asked one at a time, in the question format;
  - the record format;
  - the propose-then-apply step;
  - the flag for answers that change behavior.

  Do a trial run on a scratch copy of v0. Revise the skill if it asks more
  than five questions, asks about implementation, or omits the answering
  role.
- **1.3 The session.** The instructor answers in role, and the transcript is
  kept. Section 6 lists the questions the session should reach. Compare the
  skill's actual questions with that list and record the comparison.
- **1.4 Apply the answers.** Approve and apply the edits to the concept of
  operations. Create the glossary, and replace the Terms section with a
  pointer to it.
- **1.5 D4.** Under (b): amend REQ-0, add the test and the scenario, change
  `message.py`, and record the approval in the elicitation record and the
  dev log. Under (a): record the question as open.
- **1.6 Scenarios.** Write the scenarios by hand from the story examples,
  plus one representative of each level and the payload boundaries. Include
  (Restricted, 150) and (Restricted, -3), both passing unchanged; in A2 their
  expected outputs change through a specification change, which is the
  legitimate way a scenario changes. Write `test_stories.py` and the uncited
  fixture-shape test. Change the stories' method to test.
- **1.7 Gate and checks.** Run the gate and keep its output. Check that
  `diff -r v0/guard v1a/guard` is empty, or shows only the D4 (b) change. Run
  CF-01 demonstrations (a) and (d).
- **1.8 SQ at rung 1.** The instructor reads the family, including the SQ-3
  glossary check, and records the reading.
- **1.9 VAL.** Hold the validation walkthroughs per user category with
  `tools/walk.py`, then the sign-off, naming the versions of the concept of
  operations, glossary, scenarios, and requirements.
- **1.10 Records.** Write the ledger (sections for v0, after the revision,
  and v1a), the dev log, the conformance report, the README, and
  `CLAUDE.md`.
- **1.11 Sabotages for Lecture 2.** Run each one, keep its output, and
  restore.
  - **S1.** Change the expected output of the (Restricted, 7) scenario to
    *drop*. US-2 fails and REQ-2 passes. This is a gap about the pair
    (scenario, requirement): it is resolved on the specification side, and
    neither the code nor the scenario is edited just to make the test pass.
  - **S2.** Every story test passes, and the security officer, walking US-2,
    rejects the story. VAL is not established, and no automated check can
    see why (CF-04).
  - **S3.** Add an uncited failing test. Every clause row still reads pass,
    while pytest and the gate fail (CF-01 (d)).

### Phase 2: `v1/`

- **2.1** Copy `v1a/` to `v1/`.
- **2.2 Tooling requirements (CF-14).** Write `tools/requirements.md`:
  - TOOL clauses for the clause parser: inputs, the list of clauses it
    returns, and findings (malformed header, duplicate identifier,
    unsupported method, judgment clause without a reason, derivation that
    resolves to nothing). It never silently omits a clause.
  - TOOL clauses for the trace report: its rows and columns, both
    directions, and its exit codes.
  - The gap-list format.
  - The plugin changes: REQ-0a identifiers, the legend wording (CF-02), and
    the scope line (D7).

  For each clause, state what is read from the specifications, what is
  computed, and what remains human judgment.
- **2.3 The agent builds the tools.** Give an agent the tooling requirements
  and ask for a proposed layout and plan. The instructor reviews it and
  records the decisions. The agent implements the tools and adds known-bad
  cases with expected findings under `tests/tooling/`. Keep everything in
  `reference/tooling/`. Add `trace.py` to the gate.
- **2.4 S4.** Add a clause with a malformed header and no test. Run the v0
  tooling (the gate stays green and the clause disappears from the report)
  and then the v1 tooling (the parser reports it). Record both.
- **2.5 EARS and the seeded draft.** Write the EARS requirements. Produce the
  seeded draft as the default in section 3 describes, using the defect types
  of section 7, and write `expected-gaps.md`. Check each seeded gap for
  genuineness (CF-06), and do not use REQ-2's equality as a gap (review
  8.1.E).
- **2.6 Rung 1.** A person audits the seeded draft with the SQ-4 checklist
  and writes a gap list. Compare it with the answer key and record the
  misses.
- **2.7 Rung 2.** Give an agent an ad hoc prompt to audit the same draft.
  Record its gap list, its misses and over-reports exactly as they occurred,
  the model identifier, and the date.
- **2.8 Rung 3.** Write `/audit-spec`. Its steps: read the current files and
  record their versions; check within each document (parser findings, EARS
  form, glossary discipline, ambiguity); check between documents (each
  derivation against the story it cites, scenarios against requirements, the
  glossary against the concept of operations); check by execution (run
  `trace.py` and the story tests, and cite their output); check completeness
  for scope and whether each statement is a requirement or an assumption;
  write the gap list; stop. Run it on the seeded draft at least twice and
  compare the runs. Revise the skill until it finds all eight seeded gaps,
  and record each revision. Those runs are the verification of the verifier
  against its known-violation set.
- **2.9 The final specifications.** Run `/audit-spec` on the final v1
  specifications. The person rules on every finding. Findings that are not
  seeded are real, and are resolved and recorded. Reaching zero open gaps
  gives the SQ evidence.
- **2.10 Gate.** Update the test markers to REQ-0a to REQ-0c. Run the gate,
  now including `trace.py`, keep its output, and generate the trace matrix.
- **2.11 VAL.** The requirements changed, so VAL is stale. The security
  officer and the message sender confirm that the EARS wording preserves the
  meaning they signed, and sign again. Repeat the validation walkthroughs
  only if a story or a scenario changed.
- **2.12 Records.** Write the ledger (sections for v0, v1a, after the
  rewrite, and v1). The SQ provenance names the skill version, the model
  identifier, the files and their versions, and the skill's result on its
  known-violation set. Write the dev log, the README, and `CLAUDE.md`.
- **2.13 Sabotages for Lecture 3.** Run each one, keep its output, and
  restore.
  - **S4.** As in step 2.4.
  - **S5.** REQ-2 cites "Derived from: US-1". `trace.py` stays green,
    because the link resolves, and `/audit-spec` flags the misalignment.
  - **S6.** An undefined term appears in a requirement. The gate stays
    green, because SQ is not part of the gate, and `/audit-spec` flags the
    term.
  - **S7.** A derivation cites "US-9". `trace.py` fails.
- **2.14 CF-01.** Confirm that all four CF-01 demonstrations have recorded
  output: (a) and (d) from step 1.7, (b) from S7 and the marker sabotage, and
  (c) from deleting a story's last citing test.

### Phase 3: repository updates (after the build, before the lecture notes)

- Design document: the A1 row and the section 3.2 density count; the section
  7 checklists; section 8; the section 9 completion evidence for CF-01 to
  CF-07, CF-13, and CF-14.
- The demo README's version table (v1a, v1) and its replay line; the module
  README; the root `CLAUDE.md` line that says only `v0/` is built.
- `glossary.md`: add *elicitation*, *EARS*, *acceptance scenario*, *gap
  list*, *user category* and *user story*, and decide whether *skill* gets
  an entry.
- `specification-kinds.md`: the catalog rows of design 5.2 (the glossary as
  a kind, *user categories*), EARS under behavioral requirements, and the
  fixtures entry pointing at the guard's scenarios.
- Memory.

### Phase 4: teaching materials (after the build)

- Lecture 2 notes first, as you planned, then the Lecture 3 notes.
- A demo script per lecture, in the form of `demo-script-lecture-01.md`.
- Decks generated by python-pptx build scripts, following your readability
  rule: 18 pt minimum, except code, tables, and captions.
- Instructor outlines.
- Exercises (section 9).

## 6. Questions the elicitation session should reach

The skill picks its own questions. This list checks that the five it chooses
cover what matters, and that none of the answers changes behavior without
approval.

| # | Question | Why it matters | Recommended answer | Effect |
|---|---|---|---|---|
| Q1 | Can a payload be a true/false value, or only a whole number? | the meaning of *integer* in the domain; CF-13 | only whole numbers | glossary; D4 |
| Q2 | When the guard drops a message, should anyone be told, or a record kept? | whether there is a second output | not in this version | *Outside this version*; a deferred need, with no commitment to F3 |
| Q3 | May a Restricted message leave with any payload, or must its content be limited? | whether the guard changes messages | any payload in this version | a deferred need, the seed of A2's `sanitize`; scenarios with large and negative Restricted payloads |
| Q4 | What should happen to something that arrives without a recognized security level? | drop versus reject | it is not a message; it is rejected before filtering | glossary *reject*; REQ-0 wording |
| Q5 | Will the three security levels stay fixed? | whether the set of levels is closed | fixed for this version; a change comes as a change request | glossary; *Outside this version* |

## 7. Candidate seeded gaps

Eight genuine defects in a copy of the EARS requirements. Six can be found
only by judgment. One is mechanical and one is partly mechanical, which shows
that some SQ checks are already mechanical in A1 while glossary discipline is
not until A2.

| ID | Defect in the seeded draft | Check that should find it | Mechanical in A1? | Correction |
|---|---|---|---|---|
| G1 | REQ-1 says "drops every *sensitive* message"; *sensitive* is not a glossary term | glossary discipline (SQ-3) | no | "whose security level is Critical" |
| G2 | REQ-3 says *forward* where the glossary says *pass* | glossary discipline (SQ-3) | no | "passes" |
| G3 | "Restricted messages should not be modified by the guard." | EARS form (SQ-2); unambiguous | no | the event-driven pattern, "shall pass … unchanged" |
| G4 | an added requirement: when the filter receives a message whose level is not Public, it shall drop it | internal and external consistency (it contradicts REQ-2, US-2, and the scenarios); running the tests also shows "no evidence" for it | partly: the coverage gap is mechanical, the contradiction is not | remove it |
| G5 | REQ-2: "Derived from: US-1" | story-to-requirement alignment; the link resolves, so TR passes | no | US-2 |
| G6 | two clauses with the identifier REQ-3 | well-formed: unique identifiers (SQ-1; CF-06) | yes, the parser | remove the duplicate |
| G7 | REQ-0c: "Method: review (agent)", with no reason given | method choice; a judgment clause must state why it is not mechanical (SQ-1) | the missing reason is mechanical; whether review is justified is not | Method: test |
| G8 | "The guard shall ensure every message leaving the enclave passes through it." | requirement versus environmental assumption; completeness for scope | no | move it to the concept of operations' Assumptions |

G4 must not be the negative-payload policy of Exercise 1, which would give
away that exercise's answer.

## 8. Rule changes

| ID | Title | Style | Maintains | Enters |
|---|---|---|---|---|
| VAL-2 | Elicitation follows the procedure and is recorded | procedure | VAL | v1a |
| SQ-3 | Domain terms are defined once in the glossary and used in that sense | obligation | SQ | v1a |
| SQ-2 | Every requirement follows an EARS pattern | obligation | SQ | v1 |
| SQ-4 | The specification audit | procedure | SQ | v1 |
| TR-2 | The trace matrix: every story has a requirement and a scenario derived from it; every derivation resolves | obligation | TR | v1 |
| RPT-2 | The gap list | form | the record of SQ | v1 |

Amendments:

- **SQ-1:** a judgment clause states why it is not mechanical; the glossary
  and the scenarios belong to the family of specifications; requirements are
  distinguished from assumptions.
- **CONF-1:** the stories are covered through the scenarios; on failure, an
  expected outcome is never edited to make a test pass.
- **CONF-2:** applies to no clause in A1 and is kept for A2's review clauses.
- **VAL-1:** a validation walkthrough per user category; the sign-off names
  the versions of every specification signed.
- **TR-1:** a derivation may name a glossary term; each scenario's story
  field must resolve.
- **WF-1:** the gate adds `trace.py`; the rule says the gate is prescribed,
  not enforced by a hook.
- **RPT-1:** provenance includes tool versions and the kept gate output
  (D8).

Identifiers do not collide with the design's plan for later versions (A2:
WF-2 to WF-5, RQ-2, RQ-3, CONF-3, CONF-4; A3: WF-6, WF-7, RPT-3, RPT-4; A4:
CONF-5, CONF-6, WF-8).

## 9. Mapping to lectures, and density

**Lecture 2 (v1a): elicitation, the concept of operations, the glossary, and
acceptance scenarios.**

| Segment | Minutes |
|---|---|
| Lecture 1's closing question; intent consulted only through people; reference versus specification | 5 |
| The elicitation procedure; `/elicit` run live for two questions | 15 |
| The four parts of the concept of operations and their quality criteria; requirement versus assumption | 12 |
| The glossary and its discipline | 8 |
| Scenarios versus tests; under-approximation; equivalence classes | 12 |
| The method change from walkthrough to test; validation stays with a person; sabotages S1 and S2 | 12 |
| The cycle of stale and re-established judgments in the ledger; launch the exercise | 6 |

Suggested Exercise 2: run `/elicit` for one session on a small request for a
different system, with a classmate playing the stakeholder. Produce the
record, a concept of operations, a glossary, and 6 to 10 scenarios with a
justification by equivalence class.

**Lecture 3 (v1): from the concept of operations to requirements, EARS, the
audit, and traceability.**

| Segment | Minutes |
|---|---|
| Deriving requirements from stories and terms | 8 |
| The EARS patterns; rewriting REQ-0 to REQ-3 | 12 |
| The audit procedure and the gap list | 8 |
| The class audits the seeded draft (rung 1) | 10 |
| The agent with an ad hoc prompt versus `/audit-spec`; comparison with the known-violation set | 12 |
| The tooling: requirements, the agent's build, malformed-input checks, sabotage S4 | 12 |
| The trace matrix and its limit (S5); re-sign-off; the ledger | 8 |

Lecture 3 is dense. CF-14 requires explicit time for building and checking
the tooling, so the tooling segment should keep at least ten minutes. If the
lecture runs long:

- show the kept prompt and plan instead of building live, with the full
  construction in A2's worked session;
- show the agent's ad hoc audit from the record instead of running it;
- move the EARS pattern catalog to a handout.

Suggested Exercise 3: derive EARS requirements from the Exercise 2 concept of
operations. Audit a different seeded draft, provided separately, both by
hand and with `/audit-spec`, and report the misses against the answer key,
which is released after submission.

**If A1 gets one lecture:** teach from `v1/`, keep `v1a/` as an intermediate
snapshot, show the elicitation record rather than running `/elicit` live,
and move the EARS catalog and the tooling construction to a handout and to
A2.

## 10. Completion report

When A1 is built, the report names the evidence for each item and lists
anything unresolved or deferred.

| Item | Evidence to cite |
|---|---|
| Product behavior preserved (CF-03) | `diff -r v0/guard v1/guard`, empty or the D4 (b) change with its approval |
| CF-01 (a) to (d) | the outputs kept from steps 1.7, 2.13, and 2.14 |
| CF-02 | the report legend; the wording of the lecture notes |
| CF-04 | the validation walkthrough records kept separate from the story test results; the S2 record |
| CF-06 (if accepted) | `tests/tooling/` cases and their findings; the S4 record |
| CF-07 parts 2 and 3 (if accepted) | `reports/runs/`; the RPT-1 provenance |
| CF-13 | the elicitation record entry; the glossary entry |
| CF-14 | `tools/requirements.md`; `reference/tooling/` (prompt, plan, review); the known-bad cases |
| CF-15 | WF-1 still requires the gate before every commit |
| The ladder, rungs 1 to 3 | the three gap lists on the seeded draft against `expected-gaps.md`; the skill revisions; at least two skill runs |
| Rule budget | six new rules; styles procedure and form |

## 11. Risks

- **Agent results are not repeatable.** The rung-2 and rung-3 runs may not
  show the misses or over-reports the design anticipates. Teach from what
  actually happened, and never stage it.
- **Independence is weak.** One instructor plays both stakeholders and the
  auditor. The blind seeding default and the in-class rung-1 audit reduce
  this; the lecture should say that it remains.
- **Maintenance across snapshots.** Two A1 snapshots mean that a correction
  to v0 may have to be repeated in v1a and v1.
- **Model drift.** A skill's behavior changes with the model. The ledger and
  the gap lists record the model identifier.
- **Seeded gaps that are not genuine defects** would teach the wrong audit
  criteria. Each seeded gap is reviewed against review 8.1.E before use.
