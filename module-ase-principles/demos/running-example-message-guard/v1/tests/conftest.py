"""Conformance-report plugin: requirements coverage of the test suite (rules CONF-1, TR-1).

Every test marked ``@pytest.mark.req("REQ-1")`` is evidence for the clauses it names. After a
full run this plugin writes ``reports/conformance.md``, one row per clause of the
specifications, and fails the run if a *test* clause has no passing evidence, a marker names a
clause the specifications do not define, or the clause reader reports a finding (a malformed
header, a duplicate identifier). When tests were deselected (``-k``, ``-m``) the report is still
written, labeled as a partial run, and the run is not failed, since the evidence is incomplete by
choice. Tests may omit citations; an uncited test still runs and still counts for coverage.

Adapted from the Spec Kit demo in
``module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/tests/conftest.py``; the
catalog page is ``tooling/conformance-plugin.md``.
"""

from datetime import datetime
from pathlib import Path

import pytest

from tests.conformance import read

REPORT = Path("reports") / "conformance.md"
RECORDS = "`reports/validation.md` (walkthroughs) or the review record the rule names"

_tags: dict[str, tuple[str, ...]] = {}  # test nodeid -> clause identifiers it cites
_outcomes: dict[str, str] = {}  # test nodeid -> passed | failed | skipped
_collected = 0
_deselected = False
_summary: tuple[list[str], list[str], list[str]] | None = None


def pytest_collection_modifyitems(items):
    global _collected
    _collected = len(items)
    for item in items:
        ids = tuple(i for marker in item.iter_markers("req") for i in marker.args)
        if ids:
            _tags[item.nodeid] = ids


def pytest_deselected(items):
    global _deselected
    if items:
        _deselected = True


def pytest_runtest_logreport(report):
    if report.nodeid not in _tags:
        return
    if report.failed:
        _outcomes[report.nodeid] = "failed"
    elif report.skipped:
        _outcomes[report.nodeid] = "skipped"
    elif report.when == "call" and report.nodeid not in _outcomes:
        _outcomes[report.nodeid] = "passed"


def _status(method: str | None, tests: list[str]) -> str:
    if method is None:
        return "**malformed header**"
    if method != "test":
        return f"{method}: see {RECORDS}"
    if not tests:
        return "**no evidence**"
    outcomes = [_outcomes.get(t, "not run") for t in tests]
    if "failed" in outcomes:
        return "**FAIL**"
    if all(o == "passed" for o in outcomes):
        return "pass"
    return "**partial**"


def _short(nodeid: str) -> str:
    return nodeid.removeprefix("tests/")


def pytest_sessionfinish(session, exitstatus):
    global _summary
    if session.config.getoption("collectonly"):
        return
    specs = read()
    by_id: dict[str, list[str]] = {}
    for nodeid, ids in _tags.items():
        for i in ids:
            by_id.setdefault(i, []).append(nodeid)

    rows: list[str] = []
    gaps: list[str] = []
    for clause in specs.clauses.values():
        tests = by_id.get(clause.id, [])
        status = _status(clause.method, tests)
        if clause.method == "test" and status != "pass":
            gaps.append(f"{clause.id}: {status.strip('*')}")
        listed = "<br>".join(f"`{_short(t)}`" for t in tests) or "—"
        rows.append(f"| {clause.id} | `{clause.file}` | {clause.method or '—'} | {listed} | {status} |")
    unknown = sorted(i for i in by_id if i not in specs.clauses)
    findings = [str(f) for f in specs.findings]
    test_clauses = [c.id for c in specs.clauses.values() if c.method == "test"]
    passing = [i for i in test_clauses if _status("test", by_id.get(i, [])) == "pass"]
    files = ", ".join(f"`specs/{f}`" for f in specs.files)
    generated = (
        f"Generated {datetime.now():%Y-%m-%d %H:%M} by the plugin in `tests/conftest.py` "
        f"from the clauses in {files}; {_collected} tests collected, {len(_tags)} cite a clause."
    )
    scope = (
        "**Scope**: partial run (tests were deselected); not evidence for CONF."
        if _deselected
        else "**Scope**: full run."
    )
    coverage = (
        f"**Requirements coverage**: {len(passing)} of {len(test_clauses)} test clauses "
        "have passing evidence."
    )
    legend = (
        "Status of a *test* clause: **pass**, every citing test passed; **FAIL**, a citing "
        "test failed; **partial**, a citing test was skipped or not run; **no evidence**, no "
        "test cites the clause. A *walkthrough* or *review* clause is not decided by this run; "
        f"its record is {RECORDS}. A citation declares intended support; it does not establish "
        "that the test's assertions check the clause."
    )

    lines = [
        "# Conformance Report: Message Guard",
        "",
        generated,
        "",
        scope,
        "",
        coverage,
        "",
        "| Clause | Specification | Method | Tests citing it | Status |",
        "|---|---|---|---|---|",
        *rows,
        "",
        legend,
        "",
        "## Unknown identifiers",
        "",
    ]
    if unknown:
        lines += ["Markers that name no clause in the specifications:", ""]
        lines += [f"- `{i}`: " + ", ".join(f"`{_short(t)}`" for t in by_id[i]) for i in unknown]
    else:
        lines.append("None.")
    lines += ["", "## Specification findings", ""]
    if findings:
        lines += ["Headers the clause reader could not accept (rule SQ-1); the run fails on them:", ""]
        lines += [f"- {f}" for f in findings]
    else:
        lines.append("None.")
    lines.append("")

    out = Path(session.config.rootpath) / REPORT
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")

    _summary = (gaps, unknown, findings)
    if (gaps or unknown or findings) and not _deselected:
        session.exitstatus = pytest.ExitCode.TESTS_FAILED


def pytest_terminal_summary(terminalreporter):
    if _summary is None:
        return
    gaps, unknown, findings = _summary
    write = terminalreporter.write_line
    if not gaps and not unknown and not findings:
        write(f"conformance: every test clause has passing evidence; report in {REPORT}")
        return
    for gap in gaps:
        write(f"conformance: {gap}")
    for ident in unknown:
        write(f"conformance: marker names a clause the specifications do not define: {ident}")
    for finding in findings:
        write(f"conformance: specification finding: {finding}")
    if _deselected:
        write("conformance: gate not applied because tests were deselected (partial run)")
    else:
        write(f"conformance: FAIL, see {REPORT}")
