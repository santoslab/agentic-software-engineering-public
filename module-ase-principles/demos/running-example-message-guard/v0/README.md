# Message Guard, version A0

Version A0 of the running example of the agentic software engineering
principles module. The system is the smallest cross-domain message guard:
one stage, `filter`, that drops a Critical message and passes anything else
unchanged. Everything else in this directory exists to show how a specification
is written, how code is shown to conform to it, and how the state of that
showing is recorded. The design behind the versions is
`software-engineering/running-example-design.md` at the repository root.

## The artifacts, by category

| Category | Files | Role |
|---|---|---|
| Intent | none | lives with the stakeholders; consulted through the sign-off |
| Specifications | `specs/conops.md` (purpose, scope and terms, user categories, user stories US-1 to US-3); `specs/requirements.md` (REQ-0 to REQ-3) | seven identified verification clauses; contextual specification text is reviewed with them but has no individual conformance-report row |
| Realization | `guard/` (the code); `tests/` (the suite, with optional clause citations) | what was built, and the executable claims about it; every clause assigned method test requires citing evidence |
| Development rules | `process/rules.md` (SQ-1, RQ-1, CONF-1, CONF-2, VAL-1, TR-1, WF-1, RPT-1) | how each judgment is established and when it must hold |
| Reports | `reports/ledger.md`; `reports/dev-log.md`; `reports/walkthrough.md`; `reports/conformance.md` (generated) | the development state, readable without reading the code |
| Technology | `pyproject.toml`, `uv.lock` | Python 3.12 or later; pytest, pytest-cov, ruff; managed by `uv` |
| Support | `tools/gate.sh` (the gate command); `tools/walk.py` (walkthrough helper); `CLAUDE.md` (what an agent reads first) | none is a realization of a clause |

## The five judgments, at this version

| Judgment | Established by | Evidence |
|---|---|---|
| SQ, specification quality | a person reads the two specifications together (rule SQ-1) | the SQ row of the ledger |
| RQ, realization quality | `ruff check`; the suite collects (RQ-1) | exit codes in the dev log |
| CONF, conformance | the aggregate: every test passes, every *test* clause has passing evidence (requirements coverage), 100 percent branch coverage (structural coverage), every *walkthrough* clause walked (CONF-1, CONF-2) | `reports/conformance.md`; the coverage table; `reports/walkthrough.md` |
| VAL, validated | a stakeholder of each user category signs the concept of operations (VAL-1) | the sign-off in `reports/walkthrough.md` |
| TR, traceable | every marker and every "derived from" resolves (TR-1) | the "Unknown identifiers" section of the conformance report |

The ledger, `reports/ledger.md`, has one row per judgment with its evidence and
its provenance. The gate, `tools/gate.sh`, decides the mechanical parts (RQ and
the first three conjuncts of CONF) before any commit (WF-1).

Taken literally, CONF-1 and WF-1 require the implementation, tests, and
checking infrastructure before the first commit. This snapshot demonstrates
the completed A0, not a sequence of independently committed construction
tasks; `reports/dev-log.md` records those tasks without claiming a commit for
each. This restriction is a teaching example of development rules that need
to be "debugged." A2 will introduce intermediate commits and acceptance
checkpoints. A passing script does not discharge the separate human-review
and reporting obligations.

## Running it

```sh
uv sync                       # once: creates .venv with pytest, pytest-cov, ruff
tools/gate.sh                 # the gate: ruff, then pytest with coverage and the conformance plugin
uv run python tools/walk.py Critical 100   # a walkthrough step: prints "drop"
```

`uv run pytest` alone runs the suite with coverage, regenerates
`reports/conformance.md`, and fails if any requirement has no passing test.

## Breaking it

Each judgment has a sabotage that turns exactly its row red and shows which
verifier catches it. Two are for the first lecture; three wait for the lecture
on testing.

1. **CONF, a wrong realization.** In `guard/filter.py`, change the condition to
   `SecurityLevel.RESTRICTED`. Run `tools/gate.sh`: `test_critical_is_dropped`
   fails, the conformance report shows REQ-1 as FAIL and REQ-2 as FAIL, the gate
   is red. Restore the file.
2. **VAL, the wrong system.** Suppose the security officer meant that Restricted
   messages must also be stopped. Every check stays green: the specifications are
   consistent, the tests pass, coverage is complete, every link resolves. Only
   the walkthrough with the officer, and the sign-off they withhold, catches it.
   Nothing in the repository can.
3. **CONF, a missing test** (testing lecture). Delete `test_public_passes_unchanged`.
   Every remaining test passes and branch coverage stays at 100 percent, yet the
   gate is red: REQ-3 has no evidence. Requirements coverage is the conjunct that
   catches it.
4. **CONF, an unexercised branch** (testing lecture). Before the final
   `return message`, add `elif message.payload < 0: return None`. Every test
   passes and every requirement has evidence, yet the gate is red: the new
   branch was never taken. Structural coverage is the conjunct that catches it,
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
