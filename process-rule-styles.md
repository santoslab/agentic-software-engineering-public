# Styles of Process Rule — A Handout for the Course

> Companion to `specification-kinds.md`, which catalogs the kinds of product
> specification. This handout catalogs the *styles* a process rule can take,
> gives the template every rule is written in, the principles for writing
> one, the design grid a process is designed on, and the threats to a
> judgment that most rules exist to close. Every example comes from the
> message guard running example (`module-ase-principles/demos/running-example-message-guard/`);
> the design behind it is `software-engineering/running-example-design.md`,
> sections 2.1a, 2.8, and 2.9. The example introduces the process material
> in layers (design 2.1a): A0 and A1 have no rules in the full sense, only
> per-form *judgment clauses* (what holds, how it is evaluated, what
> evidence, how it is bound to the project) and, from A1, *procedures*;
> rules with a trigger and a failure clause arrive with A2's ledger and
> control layers. This handout therefore describes where each style stands
> at A1 and which version brings it in the full template.

## Why styles

A process rule is a requirement on the development process, and the toolkit
for product clauses applies to it unchanged: an identifier, a statement, a
verification method, evidence, coverage. Students writing process rules run
into three problems. Rules of different kinds sit in one numbered list,
unlabeled, so a definition, a threshold, a gate, and a procedure look alike.
There is no template, so nobody can see when a rule is complete. And most
first drafts name no decider, no evidence, and no failure behavior, which
makes them wishes. The styles answer the first problem, the template the
second, and the principles the third.

## The seven styles

| Constrains | Style | Shape | Example in the guard | In use from |
|---|---|---|---|---|
| an artifact at rest | **obligation** | every X MUST have property P | every requirement carries a method and a derivation (Reqs-SQ-1); every requirement is in EARS form (Reqs-SQ-2); every test clause has passing evidence (Reqs-CONF-1) | A0, as the per-form judgment clauses: an obligation whose trigger and failure clause are left to the control layer |
| a transition | **gate** | WHEN step S would complete, condition C MUST hold, decided by D | before a commit, `tools/evaluate.sh` exits 0 (WF-1, enforced by a pre-commit hook) | A2 (in A0 and A1 the command evaluates and does not gate) |
| a transition | **staleness** | WHEN artifact X changes, judgments J become stale and MUST be re-established before gate G | a specification change makes the CONF, VAL, SQ, and TR rows stale; a declared change of mind makes VAL stale (Ledger-2) | A2 (until then the report is recompiled on request, so nothing is kept long enough to go stale) |
| an activity | **procedure** | to do activity A: steps 1 to n; stop at k and report | the audit: read everything, check within, between, by execution, stop and list the gaps (Audit); elicitation: at most five questions, recorded verbatim, applied one by one (Elicit) | A1, in `process/procedures.md`; nothing says when a procedure must run |
| an activity | **policy** | parameter V of activity A is set to value X; exceptions are granted by R | branch coverage 100 percent (today the *In this project* binding of Reqs-CONF-1; a policy rule of its own when the verification plan arrives) | A2 |
| a record | **form** | record R has fields F, is produced by whom and when, and is read by whom | the gap list, the assurance report (templates in `process/templates/`); the trace matrix and the validation record (described in the *Evidence* fields of Specs-TR-2 and ConOps-VAL-1) | A0 and A1, as templates and evidence descriptions, not as rules |
| authority | **change control** | artifact X may be changed only by whom, with record R and approval A | the scenario file is never edited to make a test pass (today a sentence in the file; a rule with the change request) | A3 |

Definitions are deliberately not a style: what a verifier is, or what a
mechanical clause is, belongs in the glossary and on the clauses, never in a
rule list.

## The template, and the clause it grows from

A rule of the control layer carries eight fields, so a reader can see when
one is complete. Four of them are already present on every per-form
judgment clause of A0 and A1, under other names; the other four are what
the control layer adds. Reqs-CONF-1 of version A1, condensed, beside the
rule A2 wraps around it:

```
Clause (A1)                              Rule (A2)
Reqs-CONF-1                              WF-1
                                         Style       gate
                                         Maintains   RQ, the mechanical part of
                                                     CONF, and TR
                                         When        WHEN work would be committed
Holds when   every requirement with      Statement   Code-RQ-1, Reqs-CONF-1,
             method test is cited by a               Scen-CONF-1, Specs-TR-1,
             passing test, and the                   and Specs-TR-2 MUST hold
             suite meets the coverage                for the tree being committed
             objective
Evaluated by test: the runner, the       Decided by  analysis: the exit code of
             citation plugin, the                    tools/evaluate.sh; enforced
             coverage tool                           by the pre-commit hook
Evidence     the conformance report;     Evidence    the header of the run in the
             the coverage table                      dev-log entry; the hook's
                                                     refusal
In this      REQ clauses of              On failure  the commit is not made; the
project      specs/requirements.md;                  work returns to its task
             guard/; 100 percent
             branch coverage;
             uv run pytest               Example     the hook refusing a test
                                                     with no marker
```

*Decided by* is the verification method of a product clause applied to the
rule itself, so a rule is mechanical or judgment like any clause, and the
verifier ladder applies to rules: a rule often starts as a habit, becomes a
checklist, then a skill, then a hook. *When* says both the trigger and the
scope, and it is where a rule says whether it applies throughout development
or only at a checkpoint. *On failure* is what keeps a red result from having
nowhere to go. A clause has neither field, on purpose: it says what holds
and how one finds out, and leaves when to the process that uses it, which
is why a clause can be copied into a project that has no process rules at
all.

## Principles for writing rules

1. Every rule names the judgment it maintains; a rule that maintains none is
   deleted.
2. Every rule names its decider and its evidence. A rule you cannot check is
   a wish.
3. Separate the rule from the number: thresholds are policy rules, later the
   verification plan; gates cite them.
4. Rules do not define terms.
5. State the trigger and the scope.
6. Say what failure does. Never silently.
7. Rules are earned: start with the judgment clauses and the assurance
   report; add a procedure the second time an activity is done by hand,
   which is when a skill is near; add a rule when the process needs a claim
   to hold at a named step.
8. One example per rule, from this system.

## The design grid

A process is designed by filling the cells of a grid whose rows are the five
judgments and whose columns are the seven styles. Most cells stay empty at
first; the CONF row, made project-specific, is the verification plan. The
grid at version A1, with the clauses in the obligation column and the
procedures in theirs:

| | obligation (clauses) | gate | staleness | procedure | policy | form | change control |
|---|---|---|---|---|---|---|---|
| SQ | ConOps-SQ-1, Reqs-SQ-1, Reqs-SQ-2, Gloss-SQ-1, Specs-SQ-1 | | (A2) | Audit | | the gap-list template | |
| RQ | Code-RQ-1 | | | | | | |
| CONF | Reqs-CONF-1, Scen-CONF-1 | (A2: WF-1) | (A2) | | (A2) | | (A3) |
| VAL | ConOps-VAL-1 | | (A3) | Elicit | | the validation record, in the clause's *Evidence* field | |
| TR | Specs-TR-1, Specs-TR-2 | | | | | the trace matrix, likewise | |

Eleven clauses, two procedures, two templates, no rule in the full
template, and four columns still empty. A reader of the grid can see at
once what the process does not yet govern: nothing in A1 says when a claim
must hold.

## Threats to a judgment, and the style that answers each

A row of the assurance report, or of the ledger that keeps it, is a claim
with evidence, not a truth. Evidence is produced by
a verifier, against a reference, within a scope, at a version, and each of
those is a place where the claim can come apart from the fact. A threat is a
way the evidence can be present while the judgment does not hold; a
mitigation is the rule, procedure, or report field that closes it. Most
styles exist because of a threat.

| ID | Threat | Shown in the guard | Mitigation | Style | First seen |
|---|---|---|---|---|---|
| T1 | the reference is defective: an ambiguous or inconsistent specification, or an intent nobody can hold whole in mind | "every sensitive message" in a story; a want that leaked into a requirement; both audits of A1 found them, a one-pass reader misses the second | the audit before anything is checked against the specification; more than one reader; an agent pre-reads and a person rules | procedure; gate | A0 as a remark; A1 as the audit |
| T2 | the verifier is wrong: a program mis-implements a clause, a reader misreads one, attention lapses | A0's clause reader dropped a header without a method silently; an ad-hoc agent audit reported a non-gap | a known-violation set the verifier must fail on; the seeded drafts; a second verifier for comparison | obligation; procedure | A1 (the seeded gaps, the tooling cases); A2 (the script) |
| T3 | the scope is narrower than the claim: clauses not decided, code not exercised, a pass read as total | a partial run read as a full one; a clause with no citing test | the two coverages; the scope line of every report; the "no evidence" row | policy; form | A0; the scope line in A1 |
| T4 | the evidence is stale or was never produced | a completion message that says "all tests pass" with no run behind it; the old suite still passing after a requirement changed | staleness rules; the ledger from exit codes at a named state; provenance on every row; the report compiled from runs made now and records read now, never from memory | staleness; form | A0 (the report's provenance and its "what was run and read" section); A2 (the generated ledger) |
| T5 | a shared mistake: the author of the realization is also its verifier | an agent reads "unchanged" the same wrong way in the code and in its unit test | independence: a verifier that does not share the author's reading; the person-authored scenario file | change control; policy | A1 (the scenarios); A4 (the verification plan) |

Climbing the verifier ladder exchanges threats rather than removing them:
from a person to an agent trades attention and capacity for memory and
non-determinism; a skill fixes the procedure but not the findings; a program
removes non-determinism and introduces silent mis-implementation and a fixed
scope. The mitigation changes with the rung, which is what the verification
plan will record per clause group.

## One worked example per style in use

- **Obligation, as a clause: Gloss-SQ-1 (glossary discipline).** Holds when
  every domain term used in a specification is defined exactly once in the
  glossary and used only in that sense, and no other specification defines a
  term. Evaluated by review within the audit (a person in audit 01, an agent
  in audit 02, the skill from audit 03; a script in A2). Evidence: the C-3
  and C-10 rows of the latest audit record. In this project:
  `specs/glossary.md`; the draft of A1 said "sensitive", and the ruling
  rewrote the story with the defined term. No *When* and no *On failure*: a
  report compiled while the term is undefined says the clause does not hold,
  and what follows from that is the process's business.
- **Procedure, Audit.** Read every specification in scope in full; check
  within each document by its form's items, between documents, and by
  executing the examples; stop and report every gap in the gap-list form; a
  person rules on each. The procedure became the `/audit-spec` skill, which
  is rung 3 of the ladder: the same steps every run, even where the findings
  differ, with the form as its argument and one file of items per form.
  Nothing says when it must run; the assurance report says whether the
  latest audit is older than the specifications.
- **Form, as a template: the gap list.** Audit identifier, date, auditor with
  version, what was audited, every item with pass or its gaps, then one row
  per gap: location, item, exact quotation, proposed resolution, ruling,
  amendment. Produced by the auditor; read by the person who rules. A record
  in this form says what was checked, not only what was found. The
  assurance report has a template of the same kind: one row per clause,
  with its evidence and provenance, and a closing section listing what was
  run and read.
- **Gate, WF-1 (A2).** WHEN work would be committed, `tools/evaluate.sh`
  MUST exit 0, decided by its exit code and enforced by the pre-commit hook.
  Failure: no commit; the work goes back to its task. In A0 and A1 the same
  command exists and the same header says which state was checked with
  which tool versions, but nothing runs it unasked: the rule is what turns
  an evaluation into a gate.

The other styles arrive with the version that first needs them: staleness
with the ledger (A2), policy with the build plan and its wave-end approval
gate (A2), change control with the change request (A3).
