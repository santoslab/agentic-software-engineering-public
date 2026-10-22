# Review: Lecture 01 and message guard A0

Reviewed 2026-10-21 against repository HEAD `9a37882`. This is a review, not an implementation of the proposed edits. Line numbers refer to that checkout.

## 1. Summary

The example runs, and the central distinction between conformance and validation works.
The baseline and all four executable sabotages reproduce the intended outcomes; the recorded tool versions match.
The most important technical correction is to distinguish evidence sufficient under A0's policy from proof of conformance: citations and coverage do not establish that tests assert the requirements.
The second is to distinguish a prescribed gate from enforced commit blocking, and stale evidence from a failed judgment; the current text mixes these.
The largest teaching problem is the long abstract opening, compounded by a deck that teaches the abstractions twice before completing the example.
The PDF needs repair before distribution: test identifiers overlap the status column, and the figure floats after text calling it “above.”
Exercise 1 is feasible and its contradiction is real, but its sign-off and submission requirements need clarification.
Section 5 provides 41 individually selectable edits; none has been applied.

## 2. Technical findings

### Reading key and verification scope

For compact citations below:

- **N** = `module-ase-principles/lecture-notes/lecture-01-intent-specifications-realizations-and-judgments.md`.
- **A0** = `module-ase-principles/demos/running-example-message-guard/v0/`; paths such as `A0/tests/conftest.py` are relative to this root.
- **D** = `software-engineering/running-example-design.md`.
- **G** = `glossary.md`; **K** = `specification-kinds.md`.
- **Demo** = `module-ase-principles/demos/running-example-message-guard/demo-script-lecture-01.md`.
- **Slides** = `module-ase-principles/slides/build-lecture-01.py`.

I read the background before the primary materials, all primary text and code, the figure, the slide-generation script, and the module README. I inspected all 18 pages of the requested PDF build. The slide review is of the script, as requested, not the rendered PowerPoint. Claims below distinguish observations from source inspection and proposed changes.

### T1. Passing the four checks is a verification policy, not an equivalence to conformance

**Severity: must-fix. Location:** N:599–608, 610–637, 713–719; Slides:408–412, 588–599; D:167, 258–275.

**Claim:** A realization is “verified … or … conform[s] to S” when the relationship is found to hold; “Within that scope it can be trusted”; “conformance is not one thing but four.”

**Evidence:** N:595 correctly defines conformance as satisfaction of *every* specified property. The tests sample three Critical payloads and just one payload for each other level. The plugin checks names and outcomes, not the semantic adequacy of assertions. In an additional diagnostic, I replaced the REQ-2 test's callable with `lambda: None` **in memory**, leaving all files unchanged. Actual output was:

```text
PROBE: REQ-2 test body replaced with no assertions in memory
conformance: every test clause has passing evidence; report in reports/conformance.md
TOTAL                  21      0      6      0   100%
Required test coverage of 100% reached. Total coverage: 100.00%
10 passed in 0.02s
```

The walkthrough record was unchanged, so all four advertised kinds of evidence can still be present despite the vacuous test. N:713–719 and D:477–492 correctly acknowledge wrong verifiers, but that caveat needs to qualify the initial definition. The three ways a green suite misleads are correct examples, not an exhaustive list: wrong assertions, inadequate input selection, and a shared misunderstanding can survive both coverage checks.

**Proposed correction — edit 1:** “A0 permits its CONF row to be established when these four evidence obligations are met. This is a scoped, fallible verification result, not a proof that every specified behavior holds.” Replace “within that scope it can be trusted” with “the result is evidence only within that scope, and its strength depends on the verifier.” Describe the three failure modes as “three coverage gaps” and retain the wrong-verifier paragraph immediately afterward. Apply the same distinction to the slides and the design's stronger “sound only when” explanation.

**Related claim, N:553–560:** A marker “rules out” a test that exercises code without claiming anything. The diagnostic directly disproves this.

**Proposed correction — edit 2:** “A marker declares what a test is intended to support; reviewing its assertions determines whether it actually supports that clause.” Name the computed metric *citation-based requirements coverage* when first introducing it, while retaining the course's shorter name thereafter.

### T2. “Every test must cite a clause” is neither stated by the cited rules nor enforced

**Severity: must-fix. Location:** N:560, 932; Slides:574–578; Demo:161–162; A0/process/rules.md:43, 82; A0/tests/conftest.py:29–33.

**Claim:** “A test that cites no clause is, under A0's rules, not allowed in the suite”; the slide attributes this to CONF-1 and TR-1.

**Evidence:** CONF-1 requires **each test-method clause** to have a citing test. TR-1 requires **each existing marker** to resolve. Neither requires each test to have a marker. The plugin's `if ids:` simply omits unmarked tests from its `_tags` dictionary. Removing the REQ-0 marker from `test_exactly_three_security_levels` in memory, before the report plugin collected markers, produced exit 0:

```text
PROBE: removed REQ-0 citation in memory from test_exactly_three_security_levels
conformance: every test clause has passing evidence; report in reports/conformance.md
Required test coverage of 100% reached. Total coverage: 100.00%
10 passed in 0.02s
```

The generated report then said `9 tests cite a clause` and `4 of 4 test clauses have passing evidence`. Other REQ-0 tests keep that clause covered. `--strict-markers` cannot detect the absence of a marker.

**Proposed correction — edit 3:** Preserve the apparent intended A0 discipline by adding “Every collected test MUST cite at least one clause” to TR-1 and rejecting unmarked collected tests in the plugin, with an explicit diagnostic. This amends an existing rule and preserves the eight-rule budget. It does not substitute for assertion review in T1.

### T3. A0 prescribes a gate but does not enforce it before commits

**Severity: must-fix. Location:** N:417–418, 844–859, 1073–1075; Demo:133–135; Slides:520, 679–692; A0/tools/gate.sh:5–8.

**Claim:** “a program that nobody has to remember to run”; “A gate makes the checks a property of every commit.”

**Evidence:** The script contains `set -e`, changes directory, runs `uv run ruff check .`, and runs `uv run pytest`. It neither performs nor intercepts a commit. A0 ships no commit hook or required CI check. The demo's `git init` does not install one. WF-1:95 is a written obligation to run the command, and `CLAUDE.md` tells an agent to follow that obligation. This does not make bypass impossible.

**Proposed correction — edit 4:** “A0 supplies the algorithmic check and a process rule requiring it before each commit. Compliance is recorded in the log; automatic enforcement requires a hook or required CI check.” Qualify the invariant as a property of histories that follow WF-1. Keep A0 minimal; do not silently add a new enforcement system to this lecture.

### T4. The sabotage explanation conflates invalidation, failure, and ledger mutation

**Severity: must-fix. Location:** N:815–820, 863–887; A0/README.md:50–75; A0/reports/ledger.md:14–17; Demo:237–242; Slides:694–703.

**Claim:** Every judgment has a sabotage turning “exactly its row red”; after the code sabotage “SQ, VAL, and TR are untouched.”

**Evidence:** The ledger explicitly invalidates RQ on code or test changes, CONF on specification or code changes, and TR on **any artifact** change. A code edit therefore first makes **RQ, CONF, TR** stale. The subsequent gate can supply fresh passing RQ and marker-resolution evidence, while CONF fails. It does not rewrite the handwritten ledger or re-read the human part of TR. Sabotage 5 demonstrably breaks both marker resolution and REQ-3 coverage. The README has three CONF cases, one VAL case, and one TR case, not a separate SQ and RQ sabotage. The slide displays CONF as “stale” after new failing evidence has been obtained.

**Proposed correction — edit 5:** Say that these examples expose different failure modes. For sabotage 1 explicitly narrate “RQ, CONF, and TR become stale; rerunning the checks re-establishes the applicable RQ/TR evidence, while CONF fails; the handwritten ledger must be updated separately.” For sabotage 5 name both TR and CONF. Remove the one-sabotage-per-judgment promise. Keep the two live sabotages.

**Additional defect:** The CONF row's stale-when cell omits test changes even though tests are its verifier. Slides:668 correctly includes them. Changes to coverage configuration, the plugin, or the tool environment can also invalidate a result without changing `guard/`.

**Proposed correction — edit 6:** Extend CONF's dependency statement to “a specification, code, tests, verifier, or relevant verification configuration/environment changes,” with the same wording in N:811 and the slide. Retain the useful counts: specification change → SQ/CONF/VAL/TR; product-code change → RQ/CONF/TR; declared intent change alone → VAL.

**Status vocabulary:** N:815 permits only established/stale, but N:999 recommends “not established,” SQ-1:20 and VAL-1:72 use that state, and a failed check is not merely old evidence.

**Proposed correction — edit 7:** Define established, stale, and not established; distinguish “not yet checked” from “checked and failed” in the evidence/finding field. Use “not established; current check failed” on the sabotage slide rather than suggesting a failing result is just stale.

### T5. The parser and the report have a narrower scope than the teaching shorthand

**Severity: should-fix. Location:** N:460–463, 640–657, 787–793; A0/tests/conformance.py:11–24; A0/tests/conftest.py:53–63, 70–139.

**Claim:** The program reads which clauses exist and fails when a clause has no evidence; the “Unknown identifiers” section evidences TR.

**Evidence from the implementation:**

- It scans only `conops.md` and `requirements.md`, recognizing lines matching `^\*\*([A-Z]+-\d+)\*\* · Method: (\w+)`. It does not parse prose, derivations, role qualifiers, uniqueness, or the meaning of assertions. Duplicate identifiers overwrite earlier dictionary entries; malformed headers are invisible; any method other than the exact word `test` gets a pointer to the walkthrough file rather than an automatic obligation.
- A citation consists of positional arguments to any `req` marker yielded by `item.iter_markers("req")`; inherited/class/module markers and multiple IDs also count. Parametrized cases count as separate test items. A docstring or a `# REQ-1` comment is not a citation for this plugin.
- For a test clause, a stored failed outcome for any citing item gives FAIL; no citing items gives no evidence; skipped or unrun citing items give partial; every cited item must pass for pass. The hook records setup/call/teardown failures and skips, and records an ordinary pass at the call phase. Thus “at least one passing test” alone is not sufficient when another citing test is skipped.
- With `--collect-only`, the plugin returns without writing the report or applying its gate. If any items were deselected, it still overwrites the report but does **not** impose its gap/unknown-ID failure. Other pytest failures and coverage failures remain effective. A positional subset need not trigger the deselection hook, so this is specifically a hook-based exemption, not a general understanding of all partial runs.
- Non-test rows are pointers, not checks that the walkthrough file exists or is current. The Markdown report does not clearly mark a deselected run as unsuitable to replace complete evidence; the terminal does.
- `--strict-markers` validates the marker name `req`, not the argument `REQ-9`; the report plugin finds the latter. Derivation links are checked by a person, not by this report.

These are reasonable limitations of a small A0 tool, but important limitations for students copying it.

**Proposed correction — edit 8:** Add a short “Scope of this report” paragraph: valid headers in the two configured files, marker-name versus clause-ID checks, all citing tests passing, human derivation/walkthrough checks, and the full-suite requirement. Explicitly label partial reports in generated Markdown, and warn that they do not replace the full gate's evidence. Leave broader parser validation for A1's SQ work.

### T6. Provenance is useful, but the named snapshot and a precise sentence are not retained execution evidence

**Severity: should-fix. Location:** N:806–835; A0/reports/ledger.md:3–17; A0/reports/dev-log.md:4–5; Demo:45–63, 297–301; Slides:670–677.

**Claim:** The ledger is “at a named commit”; “pytest 9.1.1 exited 0 at v0” distinguishes evidence from an agent's description of evidence.

**Evidence:** `git tag --list` returned no tags, and `git rev-parse --verify 'v0^{commit}'` returned `fatal: Needed a single revision` (exit 128). The running-example README:20–22 explicitly says snapshots are currently directories and the tagged replay history is planned for A1. The demo creates commits but no `v0` tag. A0 is therefore a recognizable snapshot name, not currently a resolvable commit reference. The report records a time and source paths, but no source hash. The dev log summarizes coverage; it does not contain the coverage table promised by CONF-1's evidence field. A precise sentence can still be fabricated.

**Proposed correction — edit 9:** Say “snapshot A0 in directory v0” where that is what exists, distinguish snapshot names from commits, and have the demo record the checked source commit SHA (and whether the source tree was dirty). Do not require a ledger to contain the hash of the same commit that introduces that ledger; identify the checked source revision separately.

**Proposed correction — edit 10:** Explain that provenance makes a claim identifiable and reproducible, while retained run output/report artifacts support it. In the demonstration, retain the gate output, including coverage, and link it from the dev log/ledger; do not backfill a purported historical run. Name both the plugin and test suite as versioned verifier inputs. Provenance helps find affected claims when a verifier is wrong; it does not repair or verify that verifier. The existing closing sabotage is one useful, limited check of the verifier.

### T7. The stories are assigned walkthroughs in A0, not inherently beyond tests

**Severity: should-fix. Location:** N:408–425, 624–625, 675–677, 1021–1027; D:286–305, 362–366.

**Claim:** “the clauses that no test can decide, the stories”; “A judgment clause costs a person's attention every time.”

**Evidence:** US-1 to US-3 describe observable pass/drop behavior and concrete messages. D:A1 explicitly moves their behavior into fixture tests while retaining validation sign-off. G:136–144 and 225–232 allow human **or agent** judgment. N:705 itself permits agent verifiers of judgment clauses. N:1023's “every mechanical clause [has] a test” also excludes analysis-method clauses introduced elsewhere in the same section.

**Proposed correction — edit 11:** “In A0 we assign stories to human walkthroughs; A1 automates evidence for their behavior. Whether these are the right stories remains a human validation decision.” Generalize judgment clauses to a human or agent reader, retaining the explicit `(human)` assignment here. For transfer to other projects, say “tests or analyses appropriate to each mechanical clause's method.”

### T8. Exercise 1 is correct, but its required updates and sign-off policy are underspecified

**Severity: should-fix. Location:** N:1079–1091; Slides:767–769; A0/specs/conops.md:15–18, 38–43, 62–83.

**Claim:** The negative-payload requirement forces amendment; “If a story is affected,” say what the sign-off must now say. The deliverable lists specifications, realization, and ledger, but the task also requires a dev-log entry.

**Evidence / worked answer:** Adding “drop negative payloads at every level” makes `requirements.md` **internally inconsistent** with REQ-2 and REQ-3: `(Restricted, -1)` and `(Public, -1)` are required both to pass and to produce no output. It is **externally inconsistent** with US-1, US-2, the purpose's “every other message leaves,” and the payload term's “does not inspect.” REQ-0 permits negative integers; making them invalid would evade rather than implement the requested drop behavior. REQ-1 and US-3 remain valid: Critical messages are still dropped regardless of payload. Overlap between two drop rules is not a contradiction.

A consistent solution is:

- Retain REQ-0 and REQ-1. Amend REQ-2/REQ-3 to pass the corresponding level **when payload is nonnegative**.
- Add an identified test-method requirement, for example REQ-4, dropping any negative payload. Add an identified story/policy clause, for example US-4, to which it derives; merely citing unchanged US-3 would not justify dropping Public/Restricted negatives.
- Amend US-1/US-2 and the ConOps purpose, payload/filter terms, and relevant user-category policy description; add negative examples. Scope can continue to prohibit **modifying** a payload while allowing its inspection.
- Implement the negative check and add a marked test covering negative Public and Restricted messages, with a Critical negative case if the new universal clause is to have explicit evidence at all three levels. Keep/check nonnegative boundary behavior, including zero. Parametrization is already taught by example.
- Mark SQ/CONF/VAL/TR stale on the specification amendment; RQ joins them when code/tests change. A person rechecks SQ and derivations, the gate re-establishes RQ and the mechanical evidence, and the affected walkthroughs must be rerun. VAL requires a fresh human decision on the revised ConOps.
- Revised sign-off: “Critical messages and messages with negative payloads are dropped; other Public and Restricted messages leave unchanged,” naming the revised version, roles, person, and date. Never relabel the instructor's existing signature as approval of this new policy.

This uses only techniques presented in the lecture and A0. Full change-request machinery is not needed. The ambiguity is whether students may play both stakeholder roles or should submit VAL as not established pending instructor approval. The slide speaker note additionally says a re-sign occurs “before the test and the gate,” a sequencing constraint absent from VAL-1 and the notes.

The amendment is justified by the exercise's explicit new stakeholder policy, not by a wish to make failing tests green; that distinction keeps it compatible with CONF-1's prohibition on weakening a clause merely to pass the run.

**Proposed correction — edit 12:** State that the affected stories and other ConOps policy text must be amended, specify whether students may role-play sign-off (otherwise VAL remains not established), require the changed walkthrough/sign-off, dev-log entry, generated conformance report, gate output, and ledger in the submission, and remove the slide's unsupported pre-test sign-off ordering. Explicitly say no new change-request workflow is required. Keep the exercise's core conflict for students to discover.

### T9. Question 1's intended ambiguity is largely resolved by the actual requirement

**Severity: should-fix. Location:** N:464–473, 1095–1097; Demo:137–143; Slides:528–535, 773; A0/specs/requirements.md:20–23.

**Claim:** REQ-2's “unchanged” has a possible identity reading under which the equality assertion is too weak.

**Evidence / worked answer:** REQ-2 immediately specifies “the output is **a message with the same level and the same payload**.” Returning a newly constructed equal `Message` satisfies that formulation. Requiring `out is input` is a stronger, representation-specific requirement, not an established defect in this test. The ConOps phrases “that message”/“same message” could invite the question, but its term `pass` only repeats “unchanged”; it does not resolve identity. The notes attribute the resolution to the wrong text.

**Proposed correction — edit 13:** Ask: “Could the test distinguish returning the same object from returning a new equal message? Does REQ-2 require that distinction? If the stakeholder requires identity, which specification and test must change?” Expected answer: no; the present explicit value criterion is satisfied; a new identity requirement would need an explicit contract and `is` assertion. Use the same wording in the SQ discussion, demo, and slide. This preserves the teaching point without asking students to manufacture an ambiguity.

### T10. The prescribed PDF build succeeds but is not ready to distribute

**Severity: must-fix for the conformance table; should-fix for placement/overflow. Location:** N:5, 230–241, 270–272, 529–551, 645–653, 809–811, 908–917.

**Evidence:** Built from the lecture-notes directory with the requested options, using pandoc 3.10.2 and XeLaTeX from TeX Live 2022; exit 0, no reported build error, 18 pages. I rasterized and visually inspected every page. A successful build did not establish layout correctness.

| Element | Actual rendering |
|---|---|
| Bullet and numbered lists, including the opening five judgments and the four CONF conditions | Correct nesting and numbering; no accidental code block. |
| Purpose, clause, and sign-off block quotes | Readable, properly indented; no missing content. |
| Artifact table, pp. 3–4 | Splits across pages with repeated header; readable. |
| Judgment table, p. 6 | Readable; long paths press into adjacent space in places. |
| Conformance table, p. 11 | Long test node IDs overprint the **Status** column and extend beyond the table's right edge. The entries are not reliably readable. |
| Walkthrough table, pp. 11–12 | Readable but splits a three-row example over two pages. |
| Ledger table, p. 14 | Readable but narrow equal-width columns force a very tall provenance cell, leaving a large gap after its introduction on p. 13. |
| CONF-1 table, p. 15 | Readable but the almost-empty field column receives about half the width. |
| Figure, p. 5 | Complete, sharp enough to read, correct diagram; floats to a separate page **after** “The figure above” on p. 4. |
| Code blocks | Filter docstring on p. 4 exceeds the normal right text margin; `test_public_passes_unchanged` is split between pp. 9 and 10 after its `def`. Terminal output remains readable. |
| Opening long inline path, p. 1 | Exceeds the intended one-inch right text margin. |

**Proposed correction — edit 14:** Replace the conformance table's long node IDs with short test labels and put the exact node IDs in a separate listing. Give ledger and rule examples a field/value layout with a narrow field column; keep the short walkthrough table together where feasible. Rebuild under the exact distribution command and recheck affected pages.

**Proposed correction — edit 15:** Give the diagram a stable identifier and reference it as “Figure 1,” not “above”; size/place it to accompany its discussion. Add a caption sentence that TR also links specifications to one another and evidence/report artifacts, since the diagram shows only one representative TR connection.

**Proposed correction — edit 16:** Wrap the displayed filter docstring (labeling it as wrapped), avoid an unbreakable full path in the opening quote, and keep each short test function together, for example by splitting the displayed suite into per-test blocks. Do not change the executable code merely to fix PDF layout.

### T11. The verifier comparison overgeneralizes speed, cost, and decisiveness

**Severity: should-fix. Location:** N:701–708; Slides:627–633; G:241–250.

**Claim:** A human “can decide any clause”; an algorithmic verifier is “deterministic, immediate, and free to run”; the slide guarantees the same result on repeat.

**Evidence:** This follows the glossary, so it is not a notes-versus-glossary mismatch. It is nevertheless too strong technically. Human review is bounded by competence and attention; automated checks can be costly, depend on environment, and include randomized testing or concurrent execution. The fixed A0 examples are fast and repeatable, which does not establish a property of every algorithmic verifier.

**Proposed correction — edit 17:** Describe A0's programs as fast and repeatable for fixed inputs/environment, with low marginal cost; describe human/agent readers as capable of judgment clauses within their competence. Qualify the glossary and slide comparison consistently. This preserves the practical contrast without teaching a universal guarantee.

### T12. A failed check identifies a discrepancy, conditional on the verifier

**Severity: should-fix. Location:** N:889–895; Demo:252–256; Slides:705–707.

**Claim:** A failed conformance check “reports a fact about the pair: the specification and the realization do not agree.”

**Evidence:** That is correct for sabotage 1, whose failing assertions match REQ-1/REQ-2. In general, a wrong test, parser error, environment failure, or coverage shortfall does not establish semantic nonconformance. Sabotage 3 gives an actual nonzero gate with correct unchanged product code; its failure is missing evidence.

**Proposed correction — edit 18:** “A failure identifies a discrepancy or an unmet verification obligation. Inspect the specification, realization, verifier, and environment before deciding what to change.” Then specialize to the genuine specification/code mismatch in sabotage 1. Retain the human decision about which artifact should change.

### Execution record and exact comparisons

Commands ran in A0. Initial sandbox attempts could not access uv's cache; the approved reruns succeeded. These are environment permission failures, not defects in A0.

`uv sync` exited 0:

```text
Resolved 10 packages in 18ms
Checked 9 packages in 3ms
```

Baseline `tools/gate.sh` exited 0. Relevant output, preserving the actual numbers and wording:

```text
All checks passed!
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.7.0
plugins: cov-7.1.0
collected 10 items
conformance: every test clause has passing evidence; report in reports/conformance.md
Name                Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------
guard/__init__.py       3      0      0      0   100%
guard/filter.py         5      0      2      0   100%
guard/message.py       13      0      4      0   100%
---------------------------------------------------------------
TOTAL                  21      0      6      0   100%
Required test coverage of 100% reached. Total coverage: 100.00%
============================== 10 passed in 0.03s ==============================
```

The notes' baseline count, timing on this run, conformance line, and every coverage number match. Their table omits the empty `Missing` column; that is an abridgment, not a numerical defect. `ruff --version` returned `ruff 0.17.1`; the ledger's RQ and CONF tool versions match the installed environment and lockfile. Python 3.14.7 meets `>=3.12`; it does not contradict “3.12 or later.”

| Run | Exit | Actual pytest summary | Report/coverage |
|---|---|---|---|
| Baseline | 0 | `10 passed in 0.03s` | 4/4; all three US rows refer to walkthrough; no unknown identifiers; 100.00%. |
| Sabotage 1: CRITICAL → RESTRICTED | 1 | `4 failed, 6 passed in 0.03s` | REQ-1 and REQ-2 FAIL; REQ-0/REQ-3 pass; 2/4; no unknowns; 100.00%. |
| Sabotage 3: remove Public test and its decorator | 1 | `9 passed in 0.02s` | REQ-3 no evidence; other requirements pass; 3/4; no unknowns; 100.00%. |
| Sabotage 4: literal one-line `elif message.payload < 0: return None` | 1 | `10 passed in 0.03s` | 4/4; no unknowns; filter 90%, total 96.67%. |
| Sabotage 4: same logic with `return None` on the following indented line | 1 | `10 passed in 0.03s` | 4/4; no unknowns; filter 82%, total 93.55%. |
| Sabotage 5: REQ-3 marker → REQ-9 | 1 | `10 passed in 0.03s` | REQ-3 no evidence; 3/4; REQ-9 unknown; 100.00%. |
| Restored baseline | 0 | `10 passed in 0.03s` | 4/4; no unknowns; 100.00%. |

Sabotage 1's conformance lines exactly match the notes:

```text
conformance: REQ-1: FAIL
conformance: REQ-2: FAIL
conformance: FAIL, see reports/conformance.md
```

The only discrepancy in its quoted terminal result is elapsed time: N:878 and Slides:700 say `0.05s`, the observed run was `0.03s`. Treat elapsed times as illustrative, not stable expected values. All four actual failing test IDs were the expected three `test_critical_is_dropped` cases and `test_restricted_passes_unchanged`.

Sabotage 3:

```text
conformance: REQ-3: no evidence
conformance: FAIL, see reports/conformance.md
```

Literal sabotage 4:

```text
ERROR: Coverage failure: total of 97 is less than fail-under=100
conformance: every test clause has passing evidence; report in reports/conformance.md
guard/filter.py         6      0      4      1    90%   10->exit
TOTAL                  22      0      8      1    97%
FAIL Required test coverage of 100% not reached. Total coverage: 96.67%
```

The multiline spelling instead reported `total of 94`, filter `7 1 4 1 82% 11`, total `23 1 8 1 94%`, and `Total coverage: 93.55%`. This is a line-accounting difference, not a different verdict. The displayed percentage combines measured statements and branch exits; with the threshold at 100, full coverage requires both. Neither README nor notes promises an exact percentage for sabotage 4.

Sabotage 5:

```text
conformance: REQ-3: no evidence
conformance: marker names a clause the specifications do not define: REQ-9
conformance: FAIL, see reports/conformance.md
```

Its Markdown section was:

```markdown
## Unknown identifiers

Markers that name no clause in the specifications:

- `REQ-9`: `test_filter.py::test_public_passes_unchanged`
```

Thus the README's executable sabotage predictions are correct. The issue is the associated “exactly one row” interpretation, not the commands' effects.

The walkthrough helper produced, in story order, `pass: Public 42`, `pass: Restricted 7`, `drop`, `drop`, matching every observed cell. `pytest --collect-only -q --no-cov` exited 0 and ended `10 tests collected in 0.01s`. RQ-1 names that command; the gate does **not** invoke it separately, but normal pytest collection occurs before running the tests, so a duplicate collection step is unnecessary. WF-1 should be read as requiring successful collection, not as evidence that two pytest invocations occurred.

All sabotage source edits were restored. The final full gate passed before restoring `reports/conformance.md` with the specifically requested `git checkout -- <that file>`. No other tracked source change remained. The pre-existing untracked files are recorded in section 7.

### Other technical checks and worked questions

**Quotation and inventory checks.** The complete `filter.py` quote is exact. US-1 and REQ-1 are accurate; the purpose quote is the first of the actual purpose's two paragraphs, so should be called an excerpt if treated as complete. The sign-off wording, roles, date `2026-10-20`, and A0 version match. The conformance table correctly abbreviates five REQ-0 tests and three parametrized REQ-1 cases; the walkthrough table matches the file. The CONF row is accurately condensed, including its problematic stale-when condition. The reproduced CONF-1 table preserves the rule's content while omitting the explanatory parentheticals “requirements coverage” and “structural coverage”; label it condensed rather than an exact transcription. There are seven **identified** US/REQ clauses, eight rules with the named IDs, five numbered ConOps sections (plus Terms subsection), and three dev-log entries. Paths to actual A0 artifacts exist. Counts and scope qualifications are discussed in C5/C9.

**Python 3.12.** The enum identity comparison, `Message | None`, frozen dataclass, equality assertions, and parametrization are idiomatic and compatible. A direct import/execution probe on installed Python `3.12.14` succeeded; the full locked suite ran under `3.14.7`, not under 3.12. Generated dataclass equality compares fields; frozen dataclasses emulate read-only fields rather than providing a tamper-proof security boundary. These behaviors agree with the [Python 3.12 dataclass documentation](https://docs.python.org/3.12/library/dataclasses.html). One unresolved domain choice: `Message(SecurityLevel.PUBLIC, True)` is accepted, observed on Python 3.12.14, because `bool` is a subclass of `int`. The [Python type documentation](https://docs.python.org/3.12/library/stdtypes.html#boolean-type-bool) confirms that relationship. I do not call this a definite bug without knowing whether “integer” is intended to exclude Python booleans; see section 7.

**Question 2, N:1098–1101.** Insert the negative-payload `elif` after the Critical check, as in sabotage 4. Existing tests pass because the only negative payload they send is Critical and returns before the new check. A Public or Restricted negative message would now be dropped. Citation coverage still says 4/4; structural coverage makes the gate fail. This is an achievable, useful question, but not a unique answer: adding an unused import would also make the gate red through RQ, without finding an untested behavior. Its request to describe the unsent message usefully points students toward the intended branch example.

**Question 3, N:1102–1105.** SQ is human; RQ is algorithmic; CONF is **mixed** (tests/coverage plus human walkthroughs); VAL is human; TR is **mixed** (markers plus human derivation review). Syntax/identifier rules and derivation links can become machine-readable; concrete story scenarios can become fixtures. General semantic SQ judgments do not become decidable merely by writing a checklist, and automating story checks does not automate confirmation of stakeholder intent. VAL retains a human decision; a program can check that a signature exists, not supply the decision. Edit 40 makes this mixed/partly-automatable answer explicit in the question's wording.

**Argument verdicts.** The four-condition scheme is useful as a process policy with T1's qualification. The three coverage gaps are real but non-exhaustive. “Branch coverage is not a strong property” is correct in the specific sense that it neither checks oracle quality nor explores all inputs/paths; it should not be heard as “coverage has no value.” Validation's human authority is consistent with the course definition; this does not mean agents cannot assist elicitation or organize evidence. TR merits its own row for visibility and diagnosis, but trace existence is not semantic correctness, and A0's TR is partly human. VAL can lose currency on a declared intent change without product-file changes; recording the declaration subsequently creates an artifact, which is not a contradiction. Provenance supports investigation and reproducibility, not proof of a verifier's correctness.

## 3. Cross-artifact inconsistencies

### C1. “Managed” changed meaning, and the new sentence accidentally puts intent in version control

**Severity: must-fix. Location:** N:52–56; Slides:299–300; G:109–118.

**Claim:** A process is managed when “the entities above are tracked in a source control system” and are reviewed/updated in a way that “aims” to maintain the judgments.

**Evidence:** The entities listed at N:32–34 include intent. The notes and glossary elsewhere explicitly deny that intent is an artifact. The earlier notes at commit `14bc9fd` say: “when the truth of those five judgments can be stated at any commit, with evidence, by someone who did not write the code.” Slides:300 still uses that earlier definition. The revision changes an inspectable evidence criterion into an activity/aspiration criterion, dropping the reader-independent visibility requirement. The glossary has no **Managed** entry; neither definition can be presented as its wording.

**Proposed correction — edit 19:** Reconcile notes and slide with: “Here, a managed process versions its development artifacts, records evidence for the judgments at identified checkpoints, and tracks when that evidence must be renewed. Intent remains with the stakeholders.” Retain the goal that a reader other than the author can inspect the state. Call this a lecture-local definition unless the instructor chooses to add it to the glossary. This is a real change from the earlier draft, not merely a difference in voice.

### C2. The slides retain the obsolete claim that humans cannot stand in gates

**Severity: must-fix. Location:** Slides:521–525, 632; N:848–853; G:89–100; D:193–200, 875.

**Claim:** The methods slide says walkthrough/review cannot be in a gate; the verifier slide says human “no,” agent “with effort,” algorithmic “yes.”

**Evidence:** The glossary and notes explicitly distinguish algorithmic and approval gates, and D:875 records the deliberate removal of the old ban on human gates. The diagram of an automated commit check does not override that definition.

**Proposed correction — edit 25:** Label the methods column “Automatically decided by the algorithmic gate?” and the comparison row “Role in gating”: human approval gate, agent evidence under the applicable approval policy, program exit-code gate. Keep A0's actual sign-off timing distinct from A2's wave-end approval. The A2 design specifies approval at a **wave end**, not necessarily before every commit; use that phrasing at N:851–853 and Slides:691.

### C3. A0 does not yet have the test-discipline review the notes claim

**Severity: should-fix. Location:** N:282, 575–584; Slides:313, 402–405, 580–584; A0/process/rules.md:23–34; D:250, 569.

**Claim:** A0 RQ includes the test discipline, and its three constraints “are reviewed rather than computed in A0.”

**Evidence:** RQ-1 says only that the realization passes ruff and the suite collects. The RQ ledger row records exactly those two results, with no test-discipline review record. The design explicitly introduces that review in **A2**, along with mypy. Rules elsewhere in the older game module are not automatically A0's rules. G:176–178 gives a broader course-level RQ definition that includes structure and type checks, so “in a state where it can be checked at all” is also too narrow as the general definition.

**Proposed correction — edit 21:** Define RQ as the realization meeting its stated quality criteria, then say A0 implements only lint/collection; introduce assertion discipline as an important limitation to be reviewed systematically in A2. Remove the unsupported claim of a completed A0 review. Also call A0's SQ reading an *informal audit*, becoming a structured audit in A1: G:22–32 already calls reading against rules an audit, so N:497 and 973 should not imply that A0's reading is a different species of activity.

### C4. SQ-1 does not explicitly require all five properties attributed to it

**Severity: should-fix. Location:** N:457–501; A0/process/rules.md:16–20; A0/reports/ledger.md:13.

**Claim:** “rule SQ-1 requires the properties” after naming all five.

**Evidence:** SQ-1 requires IDs, methods, derivations, absence of contradictions, and absence of multiple readings. Its “specifications together” scope reasonably covers both internal and external consistency. It does **not** state completeness for the chosen level. The ledger records seven clauses, derivations, no contradiction, and no multiple readings, but no completeness check.

**Proposed correction — edit 22:** Add “The specifications MUST be complete for their stated scope and level” to SQ-1 and add an explicit completeness check to the next actual SQ review record. This can remain one rule. Do not silently assert that an undocumented historical review was performed.

### C5. “Every clause” exceeds the seven items actually identified and reported

**Severity: should-fix. Location:** N:340–346, 398–400, 495; A0/specs/conops.md:3–5, 9–43; A0/specs/requirements.md:9; A0/process/rules.md:17.

**Claim:** The purpose statement “is a clause”; every clause has an identifier/method; there are seven clauses; every derivation names a clause identifier.

**Evidence:** The purpose, scope, and terms have no US/REQ identifiers or method fields. REQ-0 derives from `ConOps §2 (Terms)`, a section reference rather than a stable clause ID. The report finds the three US headers and four REQ headers only. The purpose's “Nothing leaves the enclave except through the guard” is an assumed deployment context for a library, not a property this one function can establish about an organization's network.

**Proposed correction — edit 23:** Explicitly define A0's seven *identified verification clauses*. Describe purpose/scope/terms as governing contextual specification text included in SQ/VAL review, and REQ-0's derivation as a permitted section reference in this minimal version. Say the no-bypass network boundary is an environmental assumption. Replace the categorical “purpose statement is a clause” and “every clause” claims where they incorrectly imply complete machine-readable coverage. Label the quoted purpose as its first paragraph and CONF-1 as condensed. This preserves A0's deliberate size rather than inventing many additional clause IDs.

### C6. Assurance's broader introduction is not itself a contradiction, but it needs the course definition

**Severity: should-fix. Location:** N:68–86; G:18–20; D:475–492.

**Claim:** Assurance means evidence-based confidence including resilience, cyber threats, and the whole lifecycle.

**Evidence:** The glossary defines it specifically as the argument from ledger and reports that development-state judgments hold, qualified by threats to evidence. The notes explicitly narrow their scope at N:71–77, so the suspected issue is **not** a direct denial of the glossary. It is an unreferenced broad introduction that never lands on the promised course definition, and may suggest a security assurance scope the toy does not have.

**Proposed correction — edit 20:** Lead with “In this course, assurance is the argument, from the ledger and reports, that the development-state judgments hold.” Retain at most one sentence that broader assurance contexts can include other properties. Tie confidence to the strength and scope of the evidence, rather than an unspecified lifecycle promise.

### C7. The CONF provenance labels dynamic code testing as “analysis”

**Severity: should-fix. Location:** N:811; A0/reports/ledger.md:15; Slides:676; D:286–305.

**Claim:** The CONF row begins `analysis: pytest ...` for the verifier of REQ-0 to REQ-3.

**Evidence:** Those clauses carry method `test`, and the course's method grid distinguishes executing the realization (test) from examining it statically (analysis). The CONF-1 process-rule checker can reasonably analyze metadata/coverage resulting from tests; that is a different subject from the product clauses in the ledger's provenance cell. The current row does not explain this distinction.

**Proposed correction — edit 24:** Label the product evidence `test (algorithmic): pytest ...; analysis of citation/coverage results: plugin and pytest-cov ...; walkthrough (human): ...`. Explain the process-level aggregation if keeping `analysis` in CONF-1's decider. Keep tool versions as they are: they are correct.

### C8. The linked catalog still describes the older module's taxonomy

**Severity: should-fix. Location:** N:503–505, 970–971, 1042–1045; K:71–78, 135–168, 517–544, 812–815; D:865–885.

**Claim:** Students are directed to the catalog without a warning that its vocabulary differs from this module.

**Evidence:** The catalog's five SQ properties include traceability and omit well-formedness; the new notes/glossary move traceability to TR. The catalog calls the glossary “not a kind,” while A1 deliberately makes it a specification of its own. It treats verification obligations as a separate form and says the ConOps is the one specification answering validation, whereas the new design distributes obligations across method fields/rules/report/plan and lets validation cover the derived family. D:869–871 explicitly records these catalog updates as pending. These are known migration differences, not errors introduced by A0.

**Proposed correction — edit 26:** At the catalog link, add a brief scope note: it is the menu of forms, its examples/rule IDs describe the older game module, and this module's definitions and progression are governed by the updated glossary and Option A. Name the SQ/TR and glossary/obligations differences. Do not silently redefine the older module's normative rules.

### C9. Forward references mostly match Option A, with two qualifications

**Severity: should-fix for the promised audit log; nit for the capability shorthand. Location:** N:201–206, 433–439, 967–984; A0/specs/conops.md:17–18; D:139–143, 567–573, 1058–1073.

**Claim:** Later versions “add … a record of what was stopped”; A0 realizes F1.

**Evidence:** A1's elicitation/glossary/EARS/fixtures/audit, A2's sanitize/architecture/contracts/plan/generated ledger, A3's change of mind/change request, A4's sessions, and A5's standard format all match Option A. The running-example README's A0/A1/A2 table agrees. But an audit log is F3, not assigned to an Option A core row, and D:1071–1073 leaves its inclusion open. Also F1:139 includes “no input, no output,” whereas the built A0 accepts one `Message`, not `None`, and has no REQ-4. Section 8 explicitly records the REQ-0–REQ-3 decision; do not demand an extra requirement as a defect.

**Proposed correction — edit 27:** Call the audit log a possible later extension, pending the open design decision, in both notes and the ConOps forward reference.

**Proposed correction — edit 28:** Annotate the design's A0/F1 mapping as the mandatory-message subset: no-message input is not part of the A0 API. This records the departure from the broad capability description without undoing the deliberate four-requirement choice.

The other recorded deviations—terms inside ConOps, plain prose requirements, two live sabotages with three deferred—and the deferred C0 prelude are intentional and appropriate. The handwritten ledger, lack of standalone glossary/elicitation record, and instructor playing both roles are not findings.

### C10. The line counts are correct only with an unstated counting convention

**Severity: nit for counts; should-fix for the inference. Location:** N:190, 945–956; Demo:319–329; Slides:554, 737–740.

**Claim:** Ten lines for the filter; under thirty lines of code; more than three hundred for specifications/rules/reports; the ratio is “not just a property of this small example.”

**Evidence:** Physical lines are `filter.py` 10, `message.py` 26, `__init__.py` 6: **42** total. The demo's command counts nonblank lines, giving **29**, including docstrings/imports; it excludes tests, the report plugin, and support tools. Specifications/rules/reports have **335 physical lines**, including blanks. The ten-line and over-three-hundred claims are correct. The comparison mixes metrics, and a single heavily annotated toy cannot establish a general effort ratio.

**Proposed correction — edit 29:** “The product package has 29 nonblank lines (42 physical lines); its specifications, rules, and reports occupy 335 physical lines. The ratio is amplified by this teaching example, but it illustrates the work of specifying and checking agent output.” Apply the same labels to the deck/demo. Do not count prose lines as measured human effort.

### C11. The framework examples are fair, but use a broader label and the primary Spec Kit link

**Severity: nit. Location:** N:14–16.

**Claim:** Spec Kit, OpenSpec, AWS Kiro, and BMAD are agent-oriented spec-driven development frameworks.

**Evidence:** The grouping is substantively fair: [GitHub's Spec Kit documentation](https://github.github.com/spec-kit/) describes a core SDD process, [OpenSpec](https://openspec.dev/) describes a configurable specification framework, [Kiro](https://kiro.dev/) describes spec-driven development in its agentic product, and [BMad's requirements documentation](https://docs.bmad-method.org/plan/define-requirements-and-a-specification/) describes specifications and traced requirements guiding implementation. They are not all the same category of product, nor do these sources establish that each implements this lecture's exact five-row ledger. The notes' weaker “appear in some form” qualification is appropriate. The Spec Kit repository identifies `github.github.com/spec-kit/` as its documentation; prefer that primary source over the current `speckit.org` link.

**Proposed correction — edit 30:** Say “tools and methods supporting specification-driven agentic development,” retain “in some form,” and link Spec Kit to its official documentation. No detailed framework comparison is needed in Lecture 01.

### C12. The technology file does not contain all information attributed to it

**Severity: nit. Location:** N:1017–1020; A0/pyproject.toml:5, 16, 20.

**Claim:** `pyproject.toml` provides language/tool versions and “the one command that is the gate.”

**Evidence:** It contains a Python lower bound, tool version constraints, and pytest configuration. Exact resolved package versions are in `uv.lock`; the gate command is named in the README/rules and implemented by `tools/gate.sh`. It does not pin the interpreter patch version. All four pytest flags claimed in the notes (`--strict-markers`, coverage target, branch coverage, 100% threshold) are present.

**Proposed correction — edit 31:** Attribute the technology statement collectively to `pyproject.toml`, `uv.lock`, and the README/gate script. For walkthrough command examples, state once that `tools/walk.py ...` abbreviates `uv run python tools/walk.py ...`; the helper has no shebang and the shorter form is not the advertised executable invocation.

### C13. The specification definition is narrowed to system behavior despite the generalization to documents and process

**Severity: should-fix. Location:** N:366–370, 509–512, 901–936; G:152–158, 193–198; K:53–69, 728–759.

**Claim:** A specification states “what the system must do.”

**Evidence:** The glossary defines a specification relative to the artifact it governs. The notes later correctly treat configurations, tests, and documents as realizations and rules as specifications of the work. An architecture can constrain structure, and a process specification can govern history rather than a software system's observable behavior.

**Proposed correction — edit 32:** “A specification states selected properties that its governed artifact or process must satisfy, at a higher level of abstraction. A0's product specifications state what the guard must do.” Preserve the simple behavior-focused example without narrowing the general term.

### Definition reconciliation checklist

This records terms checked, including those with no finding; it is not a proposal to add another student-facing table.

| Term(s) in notes | Alignment with glossary/design |
|---|---|
| Intent | Matches G:109–118 and D:171–175, except the managed-process sentence C1. No intent file is needed. |
| Purpose statement | Agreed engineering specification text, not a transcript: correct. Completeness of the quote and “clause” scope need C5. |
| Specification; clause | General definition needs C13; identified clause representation and seven-item scope need C5. Derivation examples are real. |
| Mechanical clause; judgment clause; verification method | Four method values and their static/dynamic distinction match D:286–305. Qualify human-only and inherent non-automatable wording under T7. |
| Realization; executable specification | Correctly allows many realizations and dual roles for tests. A suite supplies claims for tested inputs, not all possible inputs. |
| Realization quality | A0/full-course distinction and unsupported review need C3. |
| Conformance; verification; verified | Relationship/activity distinction is sound; result-versus-truth wording needs T1/T12. |
| Human, agent, algorithmic verifier | The categories match; universal cost/determinism and gating claims need T11/C2. |
| Validation; sign-off | Matches the course's human authority and dated/versioned decision. Walkthrough evidence and stakeholder approval are correctly separated. |
| Traceability | Broad link concept matches; A0's mixed deciders and limited syntactic checks must stay explicit (T5). A resolvable link need not be a correct derivation. |
| Artifact; development state; development-state judgment; ledger | Definitions match G:14–16, 57–64, 132–134. Commit references and evidence status need T4/T6. |
| Established; stale | Core evidence dependency idea matches G:70–73. Add missing status/dependencies under T4; declared intent changes are already correctly discussed later. |
| Provenance | Correct fields and motivation; needs resolvable scope and a distinction from retained evidence (T6). |
| Gate, algorithmic gate, approval gate | Notes' definitions match G:89–100; implementation/enforcement distinction and slide mismatch need T3/C2. |
| Obligation/gate rule styles | The “every X” and “when S” forms match D:397–405; eight A0 rules use these two styles as intended. |
| Requirements coverage; structural coverage | Correct two-sided coverage idea, qualified by syntactic citation and input/oracle limits (T1/T5); 100% combined statement/branch metric explained in the run record. |
| Managed; assurance | Managed has no glossary entry and diverges from earlier notes/slides (C1); assurance's broad introduction needs a bridge to the narrower course definition (C6). |

## 4. Pedagogical findings

### P1. Move the motivating code and question ahead of the long abstract preface

**Impact: high. Location:** N:9–172, 174–266; Slides:298–429.

The opening spends roughly two PDF pages on frameworks, managed processes, assurance, records, effort shifts, and layered specifications, followed by ten objectives. The first code is on page 4. A student must retain names for things whose practical need is not yet visible. The deck compounds this: after purpose/effort/objectives it teaches all entities and judgments abstractly in Part 1, then begins A0 in Part 2 and teaches most of them again. Static inspection counts 52 new content slides, two section slides, and two inherited slides: **56 slides**, before integrating a 48–53 minute demonstration.

**Proposed change — edit 33:** Keep a one-paragraph purpose, present the enclave and two roles, show `filter.py` and ask “right according to what?”, then introduce the figure and proceed through specifications, evidence, validation, traceability, ledger, and rules. Move the fuller effort/layering discussion to a short closing reading sidebar. Interleave the deck's diagram callouts with the corresponding A0 artifacts, eliminating the duplicate abstract/concrete pass. This retains the vocabulary-first goal through one overview figure without requiring students to learn it twice.

### P2. The introductory stakeholder list substitutes the developer for the message sender

**Impact: high. Location:** N:193–199, 284, 350, 385; A0/specs/conops.md:45–54.

The introduction names an unnamed policy setter and “a stakeholder (a developer)” implementing the system. It does not name the two **user categories** the remainder depends on. The security officer first appears by name in the Intent section; the message sender appears in the US-1 quotation. The actual ConOps correctly names and motivates sender/officer. Development stakeholders and user categories can differ, but the notes do not say so.

**Proposed change — edit 34:** Add immediately after the story: “A0 has two user categories: the message sender wants permitted messages delivered unchanged; the security officer owns the policy governing what may leave. The developer builds the guard but is not one of these two operational user categories.” Define enclave as the protected internal network, and say that the library models the boundary decision rather than deploying a network barrier. The figure itself correctly puts SQ/RQ on single entities and VAL/CONF between entities; keep it, with T10's TR scope caption.

### P3. Define or gloss the terms that the opening asks students to carry

**Impact: medium to high. Location:** opening/objectives and first uses listed below.

The table includes substantive new course/domain/tool terms used before definition or concrete illustration. It excludes ordinary graduate-course prerequisites such as source control and Python function, but identifies where those prerequisites deserve a local reminder.

| Term | First use | First adequate explanation/illustration | Assessment |
|---|---|---|---|
| Managed process | N:11 | N:52 | Early definition exists but conflicts across artifacts (C1). |
| Spec-driven framework; harness; agent-read Markdown | N:14–19 | Framework links; no local harness explanation | Assumes prior agent-tool familiarity; a parenthetical is enough. |
| Intent, specification, realization | N:32–34 | Inline glosses there; developed at 310, 364, 507 | Acceptable preview; these are not completely unexplained first uses. |
| Judgment | N:38 | Listed at 40–45; explicit claim definition at 275–277 | Reasonable preview, but acronyms/examples arrive much later. |
| Artifact | N:44 | N:288–290 | “A versioned development item” would make the early sentence readable. |
| Development state; task/work step; gating | N:63–66 | State at 290–292; gate at 848; tasks not worked here | “Task” has a useful synonym; defer the orchestration inventory. |
| Assurance; ledger | N:68; 81 | Assurance loosely scoped there; ledger lightly glossed at 83–86, concretely at 292 and 806 | Ledger is not wholly undefined, but an early one-row example would help more than a new label. |
| Verification method; evidence | N:108 | Method at 408; evidence concretely at 639 and defined at 822 | Too early in the motivation without an example. |
| Layered/composable abstraction; contract; ConOps | N:112–120 | ConOps at 323–330; contracts only previewed at 980 | Contracts/composability are not taught sufficiently to assess here. |
| Audit; verify | N:130–131 | SQ reading at 494; verification at 599; glossary for audit | Say “review against quality rules” once; call A0's reading an informal audit. |
| Clause; identifier; derivation | N:151–154 | N:382–431 | Objective says “small chunks,” which is a good partial definition; an example can complete it. |
| Mechanical/judgment clauses | N:155–156 | N:408–425 | Acceptable objective preview if the example follows promptly. |
| Provenance; stale | N:164–165 | N:815–835 | Both need short parentheticals in the objective. |
| Gate | N:166 (verb “gating” at 66) | File at 218, run at 685, definition at 848 | Define before the first gate command. |
| Enclave; security level; payload; filter | N:179–187 | Same paragraph gives most meaning; enclave implicit | Add “protected internal network”; other three are adequately introduced. |
| User category | N:284 | N:377 names the section; no general definition | Explain as an operational role, not a person count. |
| Walkthrough | N:283–284 | N:411–412; concrete record at 679–683 | Briefly define at the first judgment table. |
| Security officer; message sender | N:350; 385 | Names used, but their full role definitions remain only in ConOps | Add the role sentences in P2. |
| User story; operational scenario | N:328–330 | Worked US-1 at 385–391 | Reasonable short gap if ordering is tightened. |
| RQ lint; suite collection; ruff | N:282 | N:575–584 | Gloss “lint” and “collect” at first use; the distinction matters. |
| Requirements/structural coverage | N:283 says two measures; fully named at 640/658 | Same numbered examples | Definitions work; do not front-load their machinery earlier. |
| Enum; frozen dataclass; pytest marker; parametrization | N:519–550 | Code illustrates them, but not all syntax is explained | One caption should explain three cases, value equality, and ordinary immutability. |
| Fixture; skill; EARS | N:972–975 (EARS only in other artifacts) | Preview only | Explicitly label future material; do not expect Exercise 1 to use them. |
| Wave; approval gate | N:853, 981 | Brief preview only; approval gate defined at 850 | Define wave as a group of tasks ending at a checkpoint, or defer. |

**Proposed change — edit 35:** Add the short first-use glosses above where terms must remain, put a one-sentence Python reading guide above the tests, and move the task/contract/composability inventory to the future-material sidebar. This is a vocabulary repair, not a request for a long glossary in Lecture 01.

### P4. Keep the conversational motivation, but remove its unsupported guarantees and defensive asides

**Impact: medium. Location:** N:88–126, 249–266, 451–455, 558–573, 767–772, 928–963, 1008–1011, 1073–1075.

The two voices share the same intended argument, but their confidence levels differ. The opening says agents produce code/tests “very well” and that producing them “is no longer the problem”; later paragraphs explain wrong tests and unreliable evidence. “An agent given a specification will realize that specification” is stronger than the verification section permits. The claim that humans recover true meaning while agents take literal readings substitutes a categorical psychology claim for the more useful shared-mistake risk. A prompt can be logged, versioned, and audited; it is not inherently unauditable. Reading code against an explicit specification is one of the lecture's own verifier methods, so an answer drawing on code is not automatically mere opinion.

There are also clear seams rather than factual contradictions: the effort-shift argument repeats at N:88, 249, 627, and 945; the long unmarked-test aside interrupts the path from the test example to RQ; “not something burdensome … arbitrarily being imposed on you” sounds defensive amid otherwise precise explanation. The late “all of what we are showing” paragraph reprises the opening's criticality/prototyping qualification.

**Proposed change — edit 36:** Use conditional claims: “Agents can produce code and tests quickly; human effort increasingly includes specifying and checking that output.” Replace the human/literal-agent contrast with the shared-misunderstanding risk. Say durable versioned rules are easier to inspect than ephemeral prompts. In the optional demo, assess whether the answer connects specification, code, current checks, and scope, not whether it avoided opening source. Keep one motivation passage; shorten the long unmarked-test discussion to a sidebar, and cut the defensive user-story aside.

### P5. Objectives are mostly covered, but one worked state-change example and clearer scope are needed

**Impact: medium. Location:** N:146–172, 815–820, 986–1075.

| Objective in order | Delivering section(s) | Can a student demonstrate it from notes alone? |
|---|---|---|
| 1. Three entities/five judgments and A0 artifacts | Example; figure/table; individual entity/judgment sections | Mostly. Intent has no artifact; ask students to identify that exception rather than “point at” one for every entity. |
| 2. Intent has no artifact but must be accounted for | Intent; validation counterexample | Yes; strong worked motivation. |
| 3. Clause formatting, methods, derivation, mechanical/judgment split | Specification; US-1/REQ-1; tests | Yes for A0 once T7/C5 are corrected; not for designing arbitrary analysis/review methods. |
| 4. Five SQ properties and checking a small spec | Specification quality; Exercise 1 | Yes for a small informal audit. The REQ-2 question needs T9; completeness must actually be in SQ-1 (C4). |
| 5. Passing tests insufficient; four conditions/evidence | Conformance; reports; sabotage | Yes after the evidence-versus-proof correction T1. |
| 6. Validation authority and independent failure | Validation; Restricted-message scenario | Yes; the clearest assessable objective. |
| 7. Read ledger/provenance/staleness and map changes | Ledger; Exercise 1 | Partial. The notes state counts but reproduce only CONF's dependency cell. The full five-row dependency table is in an external file; a worked example is missing. |
| 8. Explain gate before commit | The gate; WF-1 | Concept yes; actual enforcement claim currently wrong (T3). |
| 9. Read rule template, decider, evidence, failure | Development rules; CONF-1 table | Yes. This asks students to read, not invent a complete process. |
| 10. Transfer versus adaptation | Applying this to your own project | Yes for identification/discussion, not a production-ready process setup. |

Content without a matching demonstrable objective includes framework comparison, lifecycle assurance, layered composability/contracts, the Lean model aside, and general claims about agent/human cognition. They can remain optional context; they need not become more objectives. The slides' objective 2 also asks “which judgments an agent can establish alone,” which the notes do not fully resolve: being able to review a clause is distinct from having authority to approve it under A0's human rules.

**Proposed change — edit 37:** Add a small worked example beside the ledger: code edit → RQ/CONF/TR stale → checks rerun → passing rows re-established and CONF either established or failed. Include the five-row dependency summary there. Reword objective 1 to acknowledge the no-artifact exception and align slide objective 2 with the notes' narrower intent objective. Keep advanced layering/framework material as context rather than an implicit assessment requirement.

### P6. The demo and slides are not actually in the same order, and the demo's references are stale

**Impact: medium. Location:** Demo:8–14, 69–81, 175–178, 222–294, 331–387; Slides:619–741; N:721–901.

**Evidence:**

- Notes put validation/its counterexample before traceability, ledger, gate, and code sabotage. The demo puts the gate and walkthroughs in Segment 4, code sabotage in Segment 5, intent mismatch in Segment 6, and the ledger explanation afterward in Segment 7. This is a workable demo sequence, but not the notes' claimed exact order.
- The deck places “Breaking it: a wrong system with a green ledger” at Slides:651 before “Breaking it: a wrong realization” at 694. Running demo Segments 5 and 6 in order therefore requires jumping backward in the deck.
- Segment 7 names *The development rules: eight, in one form* and *Why the rules are a file, and where the effort goes*. The script actually creates *The development rules: eight, by judgment*, *One rule in the template form*, *Why the rules are a file*, and *Where the effort goes*. Segment 4's *The evidence* and *Who decided* references abbreviate multiple slide titles. These are navigational mismatches, not substantive different test results.
- Setup steps 3 and 5 say Segment 7 is optional/the agent demonstration; the optional agent demonstration is **Segment 8**.
- The listed segment times sum correctly: 48 minutes required, 53 with optional Segment 8. That leaves 27 or 22 minutes for the rest of a 75-minute meeting, including conceptual framing, questions, exercise explanation, and transitions. The 56-slide deck makes those remaining minutes unusually tight unless many slides are backup/reference.

**Proposed change — edit 38:** Adopt one run-of-show across notes' demo callouts, deck, and script: introduce the evidence/ledger briefly, run the gate and walkthrough, perform code sabotage, then the intent-mismatch scenario, then summarize rules/staleness. Update slide titles and Segment 8 references; mark repeated explanatory slides as backup after edit 33. Reserve explicit time for a short exercise conflict discussion. Keep the two main sabotages; they do more teaching work than repeating the abstract diagram.

### P7. The transfer section belongs near the end but is too long for the live lecture

**Impact: medium. Location:** N:986–1075; Slides:751–765.

The placement before Exercise 1 is good: it answers why students should care about the small guard. Its seven direct-transfer items and six adaptations, however, revisit most of the lecture and introduce additional method/platform choices. It occupies much of two PDF pages. Students need one example of an adaptation more than another declaration that the ideas apply everywhere.

**Proposed change — edit 39:** Keep a brief live section with three actions—identify intended behavior, connect it to checks, record current evidence—and one concrete adaptation, such as replacing pytest markers with the project's test framework's metadata. Keep the full checklist as companion-reading/sidebar material; qualify “always/begin by hand regardless” as a useful starting pattern rather than an obligation for every project.

### P8. Question 3 should explicitly allow mixed evidence and limits to automation

**Impact: medium. Location:** N:1102–1105.

The current “program or a person” phrasing invites a false binary for CONF and TR. “What would have to be written down before a program could produce it instead” suggests all human judgments eventually become mechanical, despite the validation argument and the design's ceiling on some SQ reviews. The worked answer is in section 2.

**Proposed change — edit 40:** “Classify each row's evidence as program-produced, person-produced, or mixed. For the human parts, which can be made mechanical by specifying inputs, rules, and expected outcomes; which remain judgments; and why can automating signature checks not replace validation?”

### P9. The rehearsal instructions should make safe restoration concrete

**Impact: medium. Location:** Demo:45–70, 217–220, 247–250, 359–364; N:1109–1111.

Setup starts with `rm -rf ~/message-guard-demo`, and the fallback uses `git checkout -- .`. These are avoidable risks if a student has reused the directory or is in the wrong checkout. The fallback also asserts that any nonzero gate means setup was incomplete, although dependency/environment failures are possible. Both test runs rewrite the tracked conformance report; restoring only `filter.py` does not restore the original snapshot. This review needed the explicit report restoration supplied in the review prompt but absent from the student instructions.

**Proposed change — edit 41:** Use a newly created disposable demo directory, identify it clearly, restore only the sabotaged source and generated report after rehearsal, and end with `git status --short`. Treat unexpected failures as diagnostics to inspect rather than immediately discarding all changes. Do not suppress all errors from the report-refresh commit. No delete/reset operation was run from these demo instructions during this review.

## 5. Proposed edits

Each numbered item is one selectable change; where the same claim appears in several artifacts, those locations are grouped to prevent another mismatch. These are proposals only. The numbers are referenced from the findings above.

1. **N:599–637; Slides:408–412, 588–599; D:167, 258–275:** “verified … conform / within scope trusted / four conditions” → “four evidence obligations for establishing A0's fallible CONF claim; scoped verification is not proof,” with the three omissions labeled coverage gaps rather than all possible failure modes.
2. **N:553–560, 640–657; matching marker/coverage slides:** “a marker rules out a test claiming nothing” → “a marker declares intended support; assertion review establishes whether it supports the clause,” introducing the measured quantity as citation-based requirements coverage.
3. **A0/process/rules.md:82; A0/tests/conftest.py:29–33:** “every existing marker resolves” → additionally require every collected test to cite at least one clause and reject/report unmarked tests, making the existing notes' prohibition real without adding a ninth rule.
4. **N:417–418, 844–859; Demo:133–135; Slides:520, 679–692:** “nobody remembers / invariant at every commit” → “A0 prescribes and records this check; hooks or required CI are needed to enforce it automatically.”
5. **N:863–887; A0/README.md:50–75; Demo:237–242; Slides:694–703:** “exactly its row red / TR untouched” → distinguish initial RQ/CONF/TR staleness, fresh passing RQ/TR checks, failed CONF, and manual ledger updates; state that sabotage 5 affects both TR and CONF and that no separate SQ/RQ sabotage is supplied.
6. **A0/reports/ledger.md:15; N:811; Slides:668:** “CONF stale on specification or code changes” → include changes to tests, verifier, and relevant verification configuration/environment.
7. **N:815–820, 999; ledger-status slide and sabotage slide:** “established or stale” → add not established, distinguish never checked from currently failed in the finding/evidence, and display the failing sabotage accordingly.
8. **N:640–657, 787–793; A0/tests/conftest.py:93–105:** unrestricted report claims → add the parser/citation/full-run scope paragraph, distinguish strict marker names from clause IDs, and label deselected-run Markdown reports as partial evidence.
9. **N:806–833; A0 ledger/dev-log headings; Demo setup/provenance; Slides:666–677:** “v0 is a named commit/tag” → identify it as a snapshot directory today and record the checked source SHA/dirty state for actual runs, without self-referential ledger commit hashes.
10. **N:825–835; A0 evidence-recording instructions; Demo:297–301; Slides:670–677:** “provenance distinguishes evidence from description” → “provenance identifies a reproducible claim; retained reports/run output support it,” retaining fresh gate output and naming versioned tests/plugin as verifier inputs.
11. **N:408–425, 624–625, 675–677, 1021–1027; corresponding slides:** “stories no test can decide / judgment always costs a person / mechanical means test” → “A0 assigns human walkthroughs; A1 automates behavioral evidence; human or agent judgment remains where needed; mechanical clauses use their assigned test or analysis method.”
12. **N:1079–1091; Slides:767–769:** “if a story is affected / partial deliverable / re-sign before test” → require affected ConOps/stories, specify role-play versus pending approval, list reports/log/run output in the submission, and clarify that neither pre-test sign-off nor an A3 change-request workflow is required.
13. **N:464–473, 1095–1097; Demo:137–143; Slides:528–535, 773:** “find an identity reading making REQ-2's test too weak” → ask whether equality distinguishes identity, what REQ-2 actually requires, and which contract/test must change if identity is newly required.
14. **N:645–653, 679–683, 809–811, 908–917:** overflowing/tall tables → use short test labels with exact IDs separately, field/value layouts for long ledger/rule content, and a kept-together short walkthrough table; verify under the stated PDF command.
15. **N:270–272 and figure caption:** “figure above” → stable “Figure 1” reference with suitable size/placement and a caption noting that TR also spans specification and evidence artifacts beyond the illustrated link.
16. **N:5, 230–241, 529–551:** unbreakable path/docstring and split test → shorten/break the display path, wrap and label the displayed docstring, and present short tests in blocks that stay together in PDF.
17. **N:701–708; Slides:627–633; G:241–250:** “any clause / deterministic, immediate, free” → readers within competence and A0 programs fast/repeatable for fixed inputs/environment, with low marginal cost rather than universal guarantees.
18. **N:889–895; Demo:252–256; Slides:705–707:** “failed check proves the pair disagree” → “failure indicates a discrepancy or unmet verification obligation; inspect specification, realization, verifier, and environment before deciding what changes.”
19. **N:52–56; Slides:299–300:** competing definitions of managed → one lecture-local definition based on versioned artifacts, inspectable evidence at identified checkpoints, and renewal of stale evidence, explicitly excluding intent from version control.
20. **N:68–86:** broad lifecycle/cyber assurance introduction → lead with the glossary's argument from ledger/reports that the judgments hold, then at most one sentence about broader assurance contexts.
21. **N:282, 494–501, 575–584, 973–975; Slides:313, 402–405, 580–584:** “test discipline reviewed in A0 / audit replaces reading” → A0 RQ is lint/collection, systematic discipline review arrives in A2, and A0's informal SQ audit becomes a structured audit in A1.
22. **A0/process/rules.md:17; next SQ review record:** implicit completeness → explicitly require completeness for stated scope/level and record its check during the next real review, without inventing historical evidence.
23. **N:332–346, 398–400, 495, 906; A0/specs/conops.md:3–5; SQ/README scope descriptions:** “every clause / purpose is a clause” → distinguish seven identified verification clauses from audited contextual specification text, permit REQ-0's section reference explicitly, mark no network bypass as an assumption, and label the purpose/rule quotations as excerpt/condensed.
24. **A0/reports/ledger.md:15; N:811; Slides:676; CONF-1 explanation:** “analysis: pytest” for product clauses → “test (algorithmic)” plus analysis of citation/coverage results, explaining the separate process-rule aggregation.
25. **Slides:521–525, 632; N:851–853; Slides:691:** “humans cannot gate / A2 before commits” → distinguish algorithmic decision from human approval and describe A2's approval as wave-end gating.
26. **N:1042–1045:** unqualified catalog pointer → a brief older-module scope note identifying the SQ/TR, glossary, and verification-obligation differences and pointing to the updated glossary/Option A for this module.
27. **N:201–206, 433–439; A0/specs/conops.md:17–18:** promised dropped-message record → possible later extension pending the design's audit-log decision.
28. **D:139, 567 and nearby A0 scope note:** A0 simply labeled F1 → explicitly say mandatory-message subset; no-message/`None` input is outside the A0 API, without adding a redundant/new requirement.
29. **N:190, 945–956; Demo:319–329; Slides:554, 737–740; terminal-output captions:** “under thirty versus over three hundred implies a general ratio” → state 29 nonblank product lines/42 physical lines versus 335 physical prose lines, qualify the toy's ratio, and label measured timings as illustrative.
30. **N:14–16:** homogeneous “frameworks” and `speckit.org` → “tools and methods supporting specification-driven agentic development,” retaining “in some form,” with the official GitHub Spec Kit documentation link.
31. **N:1017–1020, walkthrough command-table introduction:** pyproject supplies everything/direct helper invocation → distribute constraints, locked versions, and gate command across pyproject/lockfile/README-script, and explain the `uv run python` command abbreviation.
32. **N:366–370:** specification as only “what the system must do” → selected properties of a governed artifact/process, specializing to guard behavior for A0.
33. **N opening through first code; Slides Parts 1/2:** long abstract opening and repeated conceptual pass → one short purpose, concrete story/code question, overview figure, then interleaved concepts and artifacts; move extended layering/effort discussion to closing companion material.
34. **N:179–199:** unnamed policy stakeholder plus developer → introduce message sender/security officer as the two operational user categories, distinguish the developer, and gloss enclave/library boundary.
35. **N first uses cataloged in P3:** delayed jargon definitions → concise glosses for artifact, ledger/provenance/stale, user category, walkthrough, gate, lint/collection, and Python test syntax; defer task/contract/composability machinery.
36. **N motivational repetitions/asides; matching slides and Demo optional agent segment:** categorical agent guarantees, literal-agent psychology, unauditable prompts, code-as-opinion, defensive user-story language → qualified claims, the shared-mistake risk, durable inspectable context, and assessment of an answer's evidence chain; consolidate repeated motivation and move the long test-policy aside.
37. **N:146–172, 815–820; slide objectives:** all entities have an artifact/unsupported independent-agent objective/no worked staleness → acknowledge intent's exception, align objectives, and add the five-row dependency summary plus one worked code-change/recheck example.
38. **Demo slide references, setup Segment 7 references, and run order; corresponding deck order:** inconsistent sequence/stale titles → one aligned gate/walkthrough → code sabotage → intent mismatch run-of-show, correct titles and Segment 8 references, explicit backup slides and exercise-discussion time.
39. **N:986–1075; transfer slides:** thirteen-item live recap and universal setup prescriptions → three live actions plus one adaptation example, retaining the full qualified checklist as companion reading.
40. **N:1102–1105:** “program or person; what must be written down to automate” → allow mixed evidence and explicitly ask which judgments remain human and why signature checking does not automate validation.
41. **Demo setup/fallback/reset; N:1109–1111:** delete/reuse fixed directory, broad checkout, and source-only restore → fresh disposable checkout, targeted restoration including generated conformance report, visible failure diagnostics, and final git-status check.

## 6. What works and should be preserved

- The tiny filter is an effective way to separate “what the program does” from “what someone wanted.” The two live sabotages make that distinction observable without building software during class.
- The four-part evidence account, once framed as policy rather than proof, makes requirements coverage and structural coverage distinct and useful. Sabotage 3/4 are particularly good follow-on testing material.
- The walkthrough's two questions—behavior matches the story, story matches intent—are clear. Preserve the human sign-off when A1 adds fixture tests.
- Identifiers, clause-local methods, compact rules with decider/evidence/failure fields, and the handwritten ledger form a coherent minimal system. Keep the eight-rule budget and the planned gradual progression.
- Exercise 1 creates a real consistency problem rather than merely asking students to add a branch. Preserve that challenge and the requirement to explain stale evidence.

## 7. Open questions for the instructor

1. **Managed process:** Is the weaker “aims to maintain” wording deliberate, or should inspectable evidence at checkpoints remain the defining criterion? Edit 19 proposes a reconciliation, not a claim that the glossary already settles it.
2. **Exercise sign-off:** May a student explicitly play both roles, as the instructor does in A0, or must VAL remain not established until a designated reviewer signs? Either is teachable; the assignment must say which.
3. **Coverage policy:** Should A0 enforce the stated every-test-cites rule now (edit 3), or is an explicitly documented limitation preferred until a later version? The current text and code cannot both remain as written.
4. **Integer domain:** Does “integer payload” intentionally include Python `bool` values? If not, the requirement/type validation and tests need an explicit exclusion. The current type check is idiomatic Python but does not settle the domain choice.
5. **Future audit log:** Is F3 now committed to the taught sequence? If yes, assign it a version in Option A; otherwise edit 27 avoids promising an undecided feature.
6. **Delivery balance:** Are all 56 script-generated/inherited slides intended for live use? The current demo consumes 48 minutes before its optional agent segment. Marking much of the deck as reference is a practical alternative to a larger rewrite.

**Review limits and final workspace state.** The executable checks demonstrate the requested examples, not complete correctness over all possible inputs. I did not recreate historical stakeholder decisions, build planned A1–A3, run the optional agent demonstration, or inspect the PowerPoint visually. The full suite was run on the recorded Python 3.14.7 environment; only a direct product-code probe ran on Python 3.12.14. External framework checks used the linked primary sources on 2026-10-21.

The generated review PDF was temporary and deleted after all 18 pages were inspected. Sabotage source edits and the regenerated tracked conformance report were restored. `git diff --exit-code -- module-ase-principles/demos/running-example-message-guard/v0` exited 0. No commit was made.

The working tree was **not clean at the start**: these three untracked files already existed and were preserved:

```text
?? module-software-engineering/slides/agentic-development-skills-from-Andrew-King.pptx
?? software-engineering/ase-principles-review-prompt.md
?? software-engineering/speckit-exploration-prompt.md
```

The only added deliverable is `module-ase-principles/review-lecture-01-a0.md`. Therefore “clean when finished” means no residual changes from the review other than this requested report, not deletion of the user's pre-existing files.

## 8. Priorities for proceeding to A1 and its associated lecture

**Recommendation:** Do not delay A1 for the full Lecture 1 revision. Make a small foundation-correction pass, then build A1 and its lecture, followed by the broader Lecture 1 cleanup.

The important distinction is between correcting the concepts and mechanisms that A1 will inherit and updating every place those concepts appear in the existing teaching material. The former should happen now; the latter need not block A1. Edit numbers below refer to section 5. These are prioritization recommendations, not a record of implemented changes or approval of all the referenced edits in full.

### 8.1. Definitely correct before using A0 as A1's foundation

#### A. The meaning of verification evidence — edits 1, 2, 18

[status - resolved through substantial rewording in several places in
the lecture notes that acknowledge the possible *semantic gap* between
a test and the specification clause that it cites.]

Settle these formulations before drafting the next lecture:

- Passing the prescribed checks establishes a **fallible, scoped conformance claim**, not proof of correctness.
- A requirement marker records a claimed relationship between a test and a requirement. It does not establish that the assertions actually check that requirement.
- A failed gate indicates a discrepancy or unmet evidence obligation. The defect might be in the specification, implementation, test, tooling, or environment.

This matters especially in A1: fixtures, trace matrices, and an audit skill will produce more evidence, but they must not be presented as making these limitations disappear.

**Minimum now:** Correct the governing explanation and use it consistently in A1. Rewriting every corresponding Lecture 1 paragraph and slide can follow.

#### B. The inherited evidence-checking machinery — edits 3 and 8
[status - resolved by agreeing with Codex that the "every test cites a
clause" concept is not strictly needed.  This policy is not currently 
enforced in the tooling anyway, and the text in the lecture notes is 
adjusted to explain the agreed policy and its potential downsides].

**Follow-up decision: clause citations are optional for tests.** The original recommendation to require every collected test to cite a clause is withdrawn. This decision supersedes edit 3's mandatory-citation proposal; that numbered proposal remains above as part of the original review record. Additional regression, implementation-detail, and test-infrastructure tests can be useful without a direct requirement citation. The existing CONF-1 and TR-1 rules already largely express the agreed policy; the mismatch was primarily in the lecture's stronger language.

The agreed formulation is:

> Every clause assigned verification by test must be cited by at least one test, and every test citing that clause must pass for its test evidence to be accepted. Tests may have no clause citations. Every supplied citation must identify a clause defined in the specifications. A valid citation declares an intended evidence relationship; it does not establish that the test adequately checks the clause.

The qualification “assigned verification by test” is important: walkthrough, analysis, and review clauses have different evidence obligations. Separately, all tests included in the gate remain subject to the gate's test-execution policy, whether or not they cite a clause. **Optional traceability is not optional execution or permission to ignore failures.**

This policy introduces no fundamental obstacle to A1, but the following consequences should be addressed as later versions deepen the process:

1. **Change-impact analysis is incomplete without other checks (especially A3).** The trace matrix can identify tests citing a changed requirement, but it cannot identify every affected uncited test. An uncited regression test may encode an old policy expectation and need revision. Treat trace-based impact analysis as a starting set, not an exhaustive dependency analysis; continue running the full suite at the relevant checkpoint. Do not assume that running only tests linked to changed requirements is sufficient.

2. **Uncited tests can become unofficial requirements (review in A2's test-discipline work).** A test can assert behavior that the specification leaves open and later constrain changes as though that behavior were approved. For example, an uncited test might require the filter to return the same object although REQ-2 requires only equal field values. When such a test fails after a change, ask what justifies its expectation: it may protect a useful implementation property, expose a missing requirement, or encode a restriction that should be removed. The test's existence does not settle the product contract. Review this distinction rather than forcing artificial requirement citations.

3. **A green clause report can coexist with a failed overall gate (A1 reporting and A2's generated ledger).** The current plugin tracks clause outcomes only for cited tests. An uncited test can fail while every clause row remains green; pytest still fails the overall run. Distinguish clause-linked evidence status, the overall test-suite result, and the overall gate result. When generating the ledger, use the required aggregate results, not just the green clause table. Reporting counts of cited and uncited tests may help, without treating uncited tests as defects.

4. **Coverage claims need careful interpretation (throughout A1 and later versions).** Uncited tests can contribute to branch coverage. Therefore, passing cited evidence for every test clause plus 100 percent branch coverage does not establish that every exercised branch was checked against a requirement-specific expectation. Mandatory citations would not solve this either: a citation can be valid while the assertions are inadequate. Keep citation-based requirements coverage, structural coverage, and substantive review of test adequacy distinct. There is no need to exclude uncited tests from structural coverage.

**Revised A1 prerequisite:** Align the lecture language with optional test citations rather than changing the plugin to reject uncited tests. The recommendation to clearly label reports from deselected/partial runs remains: such reports must not be mistaken for complete conformance evidence. Continue validating supplied citations.

Also establish that A1's new audit/trace machinery must detect duplicate identifiers, malformed clause declarations, and unsupported methods. **That broader parser work belongs within A1 development**, once its EARS/glossary formats are defined; it need not become a separate A0 modernization project.

#### C. Judgment status and evidence dependencies — edits 5, 6, 7, 24

Correct the ledger conventions that will be copied:

- Test, verifier, and relevant configuration/environment changes can invalidate CONF evidence—not just specification and product-code changes.
- “Stale,” “not yet checked,” and “checked and failed” must not be conflated.
- Product behavior checked by pytest is **test evidence**; analysis of coverage/citations is a separate aggregation step.
- A change can affect multiple judgments. There is no general “one sabotage, one red row” rule.

The ledger can remain handwritten. Automated ledger generation should stay in A2.

#### D. The boundary between behavioral checking and validation — edits 11, 21, 25, 40

This is probably the most important conceptual preparation for the next lecture:

> A1 automates behavioral checks previously demonstrated through walkthroughs; it does not automate deciding whether the stories express the stakeholders' intent.

Preserve the distinction between checking an implementation against a story and approving the story itself. Human approval can be a gate; algorithmic execution is not what makes something a gate.

Also describe A1 as making A0's informal specification audit **structured and repeatable**, not as replacing “mere reading” with an entirely different activity. Keep the planned systematic test-discipline review in A2.

#### E. Specification quality and scope — edits 22, 23, 32

Before designing A1's audit checklist and seeded defects:

- Explicitly include completeness **for the stated scope and abstraction level**.
- Distinguish identified verification clauses from contextual specification material that still needs review.
- Distinguish requirements from environmental assumptions.
- Preserve the broader definition of specification: selected properties of an artifact or process, not exclusively executable system behavior.

Otherwise A1 could encode the wrong audit criteria into its rules, forms, and skill.

**Do not reuse the REQ-2 identity-versus-equality discussion as a known ambiguity without correcting it**—edit 13. The existing requirement explicitly requires equal field values; object identity is a possible new requirement, not an established omission.

### 8.2. Handle these as part of building A1—not as a separate prerequisite project

| Concern | Minimum needed in A1 |
|---|---|
| Gate enforcement — edit 4 | Say whether the gate is prescribed or automatically enforced. No need to add hooks/CI merely to start A1. |
| Provenance — edits 9–10 | Identify the actual checked revision and relevant working-tree state; retain actual run evidence. Do not treat the `v0/` directory name as a Git tag. |
| Roles — edit 34 | Use message sender and security officer consistently in elicitation, stories, and sign-off; distinguish the developer. |
| Scope — edits 27–28 | Keep A1's product functionality unchanged. Do not accidentally introduce audit logging or a `None`-input API through inherited wording. |
| Definitions — edits 19–20, 26 | Use consistent, scoped meanings of managed development and assurance; make the authoritative vocabulary clear without rewriting the whole older catalog. |

One additional safeguard: **Exercise 1's negative-payload policy change should not silently become the canonical A1 baseline.** A1's planned contribution is richer specification and evidence for the same product behavior.

The review did not establish a product-logic defect requiring a redesign of the filter before A1. Most urgent changes concern the assurance machinery and its interpretation.

### 8.3. Lecture 1 work that can wait

Defer these until A1 and its lecture are produced:

- PDF layout, table overflow, figure placement, and code wrapping: **14–16**.
- Major opening/reordering work, jargon scaffolding, repetition reduction, and transfer-section shortening: **33, 35, editorial portions of 36, 39**.
- Deck/demo synchronization and pacing: **38**.
- Counts, illustrative timings, framework links, and command/documentation precision: **29–31**.
- Full exercise-deliverable and discussion-question revisions: **12–13, 40**, provided they are corrected before assigning the exercise again.
- Expanded Lecture 1 objectives and worked staleness explanation: **37**, once the underlying status model is settled.

Deferral means **the old documents can wait**, not that inaccurate claims should be copied into the new lecture. Likewise, apply edit 41's safe rehearsal practices immediately if reusing the demo instructions; the old script's editorial update need not block A1.

The recommended sequence is therefore: **correct the five foundational areas above, build A1 against those corrected conventions, then revise Lecture 1 for consistency and presentation.** That prevents conceptual defects from propagating without turning preparation for A1 into a full rewrite of the first lecture.
