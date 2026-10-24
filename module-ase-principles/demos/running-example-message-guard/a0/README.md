# Message Guard, version A0

Version A0 of the running example of the agentic software engineering
principles module. The system is the smallest cross-domain message guard:
one stage, `filter`, that drops a Critical message and passes anything else
unchanged. Everything else in this directory exists to show how a
specification is written, how five claims about the development state are
defined and evaluated, and how the state of those claims is reported. The
design behind the versions is `software-engineering/running-example-design.md`
at the repository root.

## The artifacts, by category

| Category | Files | Role |
|---|---|---|
| Intent | none | lives with the stakeholders; consulted through the sign-off |
| Specifications | `specs/conops.md` (purpose, scope and terms, user categories, user stories US-1 to US-3); `specs/requirements.md` (REQ-0 to REQ-3) | seven identified verification clauses; contextual specification text is reviewed with them but has no individual conformance-report row |
| Realization | `guard/` (the code); `tests/` (the suite, with optional clause citations) | what was built, and the executable claims about it; every clause assigned method *test* requires citing evidence |
| Judgments | `process/judgments.md` (five definitions; eight clauses, filed by form); `process/templates/assurance-report.md` | what each claim says, per form, and how it is evaluated; the form of the report |
| Records | `records/reviews.md`; `records/walkthrough.md` (the walkthroughs and the sign-off); `records/dev-log.md` | evidence of what people decided and did |
| Reports | `reports/assurance-report.md` (compiled on request); `reports/conformance.md` (generated) | the development state, readable without reading the code |
| Technology | `pyproject.toml`, `uv.lock` | Python 3.12 or later; pytest, pytest-cov, ruff; managed by `uv` |
| Support | `tools/evaluate.sh` (every mechanical evaluation in one command); `tools/walk.py` (walkthrough helper); `CLAUDE.md` (what an agent reads first, and its three roles) | none is a realization of a clause |

## The five judgments, at this version

| Judgment | Clauses | Evaluated by | Evidence |
|---|---|---|---|
| SQ, specification quality | ConOps-SQ-1, Reqs-SQ-1, Specs-SQ-1 | a person reading the two specifications together; the clause reader for the header parts | `records/reviews.md`; the clause table of `reports/conformance.md` |
| RQ, realization quality | Code-RQ-1 | `ruff check`; the suite collects | exit codes, quoted in the assurance report |
| CONF, conformance | Reqs-CONF-1, ConOps-CONF-1 | the test run: every test passes, every *test* clause has passing evidence (requirements coverage), 100 percent branch coverage (structural coverage); a person walking every *walkthrough* story | `reports/conformance.md`; the coverage table; the walkthrough table of `records/walkthrough.md` |
| VAL, validated | ConOps-VAL-1 | a stakeholder of each user category signing the concept of operations | the sign-off in `records/walkthrough.md` |
| TR, traceable | Specs-TR-1 | the plugin for the citations; a person for the derivations | the "Unknown identifiers" section of `reports/conformance.md`; `records/reviews.md` |

A clause has four fields: *Holds when*, *Evaluated by*, *Evidence*, and *In
this project*. The first three depend only on the form (a concept of
operations, a requirements document) and would read the same in another
project; the fourth binds the clause to this one. Nothing in A0 says when a
claim must hold: there is no gate, no hook, and no rule about commits. What
there is instead is the **assurance report**, `reports/assurance-report.md`,
which anyone, and in this version the agent, compiles on request by running
the mechanical evaluations and reading the records. It has one row per
clause with its evidence and its provenance.

## Running it

```sh
uv sync                       # once: creates .venv with pytest, pytest-cov, ruff
tools/evaluate.sh             # every mechanical evaluation: ruff, then pytest with coverage and the plugin
uv run python tools/walk.py Critical 100   # a walkthrough step: prints "drop"
```

`uv run pytest` alone runs the suite with coverage, regenerates
`reports/conformance.md`, and fails if any requirement has no passing test.
To compile the report, start an agent here and ask for the assurance report;
or follow the steps at the end of `process/judgments.md` yourself.

## Breaking it

Each judgment has a sabotage that turns exactly its clause red in the report
and shows which evaluation catches it. Two are for the first lecture; three
wait for the lecture on testing.

1. **CONF, a wrong realization.** In `guard/filter.py`, change the condition to
   `SecurityLevel.RESTRICTED`. Run `tools/evaluate.sh`:
   `test_critical_is_dropped` fails, the conformance report shows REQ-1 as
   FAIL and REQ-2 as FAIL, the run exits non-zero. A report compiled now says
   Reqs-CONF-1 does not hold. Restore the file.
2. **VAL, the wrong system.** Suppose the security officer meant that Restricted
   messages must also be stopped. Every evaluation stays green: the
   specifications are consistent, the tests pass, coverage is complete, every
   link resolves. Only the walkthrough with the officer, and the sign-off they
   withhold, catches it. Nothing in the repository can.
3. **CONF, a missing test** (testing lecture). Delete `test_public_passes_unchanged`.
   Every remaining test passes and branch coverage stays at 100 percent, yet
   the run fails: REQ-3 has no evidence. Requirements coverage is the part of
   Reqs-CONF-1 that catches it.
4. **CONF, an unexercised branch** (testing lecture). Before the final
   `return message`, add `elif message.payload < 0: return None`. Every test
   passes and every requirement has evidence, yet the run fails: the new
   branch was never taken. Structural coverage is the part that catches it,
   and the branch it found is a bug: a Public message with a negative payload
   would be dropped, which no test claimed.
5. **TR, a dangling marker** (testing lecture). Change the marker `"REQ-3"` to
   `"REQ-9"`. The plugin lists REQ-9 under "Unknown identifiers", REQ-3 has no
   evidence, and the run fails.

## Naming against the HAMR example

The guard is the Python sibling of the HAMR Simple Network Guard. Its `Gate`
component is this version's `filter` stage, since in ordinary usage a filter
drops; HAMR's `Filter`, which transforms, will appear as `sanitize` in a later
version. HAMR's Req_C, Req_R_1, and Req_P are REQ-1, REQ-2, and REQ-3.
