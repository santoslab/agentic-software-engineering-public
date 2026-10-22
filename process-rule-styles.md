# Styles of Process Rule — A Handout for the Course

> Companion to `specification-kinds.md`, which catalogs the kinds of product
> specification. This handout catalogs the *styles* a process rule can take,
> gives the template every rule is written in, the principles for writing
> one, the design grid a process is designed on, and the threats to a
> judgment that most rules exist to close. Every example comes from the
> message guard running example (`module-ase-principles/demos/running-example-message-guard/`);
> the design behind it is `software-engineering/running-example-design.md`,
> sections 2.8 and 2.9. Four of the seven styles are in use through version
> A1; the other three arrive with A2 and A3, and their sections say so.

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
| an artifact at rest | **obligation** | every X MUST have property P | every clause carries a method (SQ-1); every requirement is in EARS form (SQ-3); every test clause has passing evidence (CONF-1) | A0 |
| a transition | **gate** | WHEN step S would complete, condition C MUST hold, decided by D | before a commit, `tools/gate.sh` exits 0 (WF-1) | A0 |
| a transition | **staleness** | WHEN artifact X changes, judgments J become stale and MUST be re-established before gate G | a specification change makes CONF, VAL, SQ, and TR stale; a declared change of mind makes VAL stale | A2 (until then, the ledger's "goes stale when" column carries it by hand) |
| an activity | **procedure** | to do activity A: steps 1 to n; stop at k and report | the audit: read everything, check within, between, by execution, stop and list the gaps (SQ-2); elicitation: at most five questions, recorded verbatim, applied one by one (WF-2) | A1 |
| an activity | **policy** | parameter V of activity A is set to value X; exceptions are granted by R | branch coverage 100 percent (today inside CONF-1; a policy rule of its own when the verification plan arrives) | A2 |
| a record | **form** | record R has fields F, is produced by whom and when, and is read by whom | the gap list (RPT-2); the trace matrix (TR-2); the validation record (VAL-2) | A1 |
| authority | **change control** | artifact X may be changed only by whom, with record R and approval A | the scenario file is never edited to make a test pass (today a sentence in the file; a rule with the change request) | A3 |

Definitions are deliberately not a style: what a verifier is, or what a
mechanical clause is, belongs in the glossary and on the clauses, never in a
rule list.

## The template

Every rule carries the same fields, so a reader can see when one is
complete. CONF-1 of version A1, condensed:

```
ID          CONF-1
Style       obligation
Maintains   CONF
When        at every commit; applies to every clause whose method is test
Statement   Every clause with method test MUST be cited, by marker, by at
            least one test; every citing test MUST pass; the suite MUST reach
            100 percent branch coverage of guard/; the loader MUST run every
            scenario of specs/scenarios.json, citing its story.
Decided by  analysis: uv run pytest; the plugin fails the run on a clause
            with no evidence, a failing citation, an unknown marker, or a
            reader finding; pytest-cov fails it below 100 percent
Evidence    reports/conformance.md; the coverage table, recorded in the dev log
On failure  a test is added or fixed, or the code is fixed; a clause is never
            weakened, and a scenario never edited, to make the run pass
Example     REQ-1 is cited by test_filter.py::test_critical_is_dropped
```

*Decided by* is the verification method of a product clause applied to the
rule itself, so a rule is mechanical or judgment like any clause, and the
verifier ladder applies to rules: a rule often starts as a habit, becomes a
checklist, then a skill, then a hook. *When* says both the trigger and the
scope, and it is where a rule says whether it applies throughout development
or only at a checkpoint. *On failure* is what keeps a red result from having
nowhere to go.

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
7. Rules are earned: start with one gate and the ledger; add a rule the
   second time a check is done by hand, which is when a procedure is written
   and a skill is near.
8. One example per rule, from this system.

## The design grid

A process is designed by filling the cells of a grid whose rows are the five
judgments (and the process records) and whose columns are the seven styles.
Most cells stay empty at first; the CONF row, made project-specific, is the
verification plan. The grid at version A1:

| | obligation | gate | staleness | procedure | policy | form | change control |
|---|---|---|---|---|---|---|---|
| SQ | SQ-1, SQ-3, SQ-4 | | (A2) | SQ-2 | | RPT-2 | |
| RQ | RQ-1 | | | | | | |
| CONF | CONF-1, CONF-2 | WF-1 | (A2) | | (A2) | | (A3) |
| VAL | VAL-1 | | (A3) | WF-2 | | VAL-2 | |
| TR | TR-1 | | | | | TR-2 | |
| records | RPT-1 | | | | | | |

Fifteen rules, four styles, three empty columns. A reader of the grid can
see at once what the process does not yet govern.

## Threats to a judgment, and the style that answers each

A ledger row is a claim with evidence, not a truth. Evidence is produced by
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
| T4 | the evidence is stale or was never produced | a completion message that says "all tests pass" with no run behind it; the old suite still passing after a requirement changed | staleness rules; the ledger from exit codes at a named state; provenance on every row | staleness; form | A1 (provenance by hand); A2 (the generated ledger) |
| T5 | a shared mistake: the author of the realization is also its verifier | an agent reads "unchanged" the same wrong way in the code and in its unit test | independence: a verifier that does not share the author's reading; the person-authored scenario file | change control; policy | A1 (the scenarios); A4 (the verification plan) |

Climbing the verifier ladder exchanges threats rather than removing them:
from a person to an agent trades attention and capacity for memory and
non-determinism; a skill fixes the procedure but not the findings; a program
removes non-determinism and introduces silent mis-implementation and a fixed
scope. The mitigation changes with the rung, which is what the verification
plan will record per clause group.

## One worked example per style in use

- **Obligation, SQ-4 (glossary discipline).** Every domain term used in a
  specification MUST be defined exactly once in the glossary and used only
  in that sense. Decided by review within the audit; in A2 by a script.
  Failure: the term is defined, or the sentence rewritten. The draft of A1
  said "sensitive"; the ruling rewrote the story with the defined term.
- **Gate, WF-1.** WHEN work would be committed, `tools/gate.sh` MUST exit 0.
  Decided by its exit code. Failure: no commit; the work goes back to its
  task. Its header line says which state was checked and with which tool
  versions, which is provenance by hand until A2 generates the ledger.
- **Procedure, SQ-2 (the audit).** Read every specification in full; check
  within each document, between documents, and by executing the examples;
  stop and report every gap in the gap-list form; a person rules on each.
  The procedure became the `/audit-spec` skill, which is rung 3 of the
  ladder: the same steps every run, even where the findings differ.
- **Form, RPT-2 (the gap list).** Audit identifier, date, auditor with
  version, what was audited, every check with pass or its gaps, then one row
  per gap: location, check, exact quotation, proposed resolution, ruling,
  amendment. Produced by the auditor; read by the person who rules. A report
  in this form says what was checked, not only what was found.

The three styles not yet in use will each arrive with the version that
first needs them: staleness and policy with the build plan and its wave-end
approval gate (A2), change control with the change request (A3).
