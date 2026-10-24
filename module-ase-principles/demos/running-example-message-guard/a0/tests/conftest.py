"""Conformance-report plugin: requirements coverage of the test suite.

The evaluation named by Reqs-CONF-1 and by the citation part of Specs-TR-1 in
``process/judgments.md``.

Every test marked ``@pytest.mark.req("REQ-1")`` is evidence for the clauses it names. After a
full run this plugin writes ``reports/conformance.md``, one row per clause of the
specifications, and fails the run if a *test* clause has no passing evidence or a marker names
a clause the specifications do not define. When tests were deselected (``-k``, ``-m``) the
report is still written but the run is not failed, since the evidence is incomplete by choice.

Adapted from the Spec Kit demo in
``module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/tests/conftest.py``.
"""

from datetime import datetime
from pathlib import Path

import pytest

from tests.conformance import SPEC_FILES, clauses

REPORT = Path("reports") / "conformance.md"
WALKTHROUGH = Path("records") / "walkthrough.md"

_tags: dict[str, tuple[str, ...]] = {}  # test nodeid -> clause identifiers it cites
_outcomes: dict[str, str] = {}  # test nodeid -> passed | failed | skipped
_deselected = False
_summary: tuple[list[str], list[str]] | None = None


def pytest_collection_modifyitems(items):
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


def _status(method: str, tests: list[str]) -> str:
    if method != "test":
        return f"{method}: see `{WALKTHROUGH}`"
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
    defined = clauses()
    by_id: dict[str, list[str]] = {}
    for nodeid, ids in _tags.items():
        for i in ids:
            by_id.setdefault(i, []).append(nodeid)

    rows: list[str] = []
    gaps: list[str] = []
    for ident, (spec, method) in defined.items():
        tests = by_id.get(ident, [])
        status = _status(method, tests)
        if method == "test" and status != "pass":
            gaps.append(f"{ident}: {status.strip('*')}")
        listed = "<br>".join(f"`{_short(t)}`" for t in tests) or "—"
        rows.append(f"| {ident} | `{spec}` | {method} | {listed} | {status} |")
    unknown = sorted(i for i in by_id if i not in defined)
    test_clauses = [i for i, (_, m) in defined.items() if m == "test"]
    passing = [i for i in test_clauses if _status("test", by_id.get(i, [])) == "pass"]
    specs = ", ".join(f"`specs/{f}`" for f in SPEC_FILES)
    generated = (
        f"Generated {datetime.now():%Y-%m-%d %H:%M} by the plugin in `tests/conftest.py` "
        f"from the clauses in {specs}; {len(_tags)} tests cite a clause."
    )
    coverage = (
        f"**Requirements coverage**: {len(passing)} of {len(test_clauses)} test clauses "
        "have passing evidence."
    )
    legend = (
        "Status of a *test* clause: **pass**, every citing test passed; **FAIL**, a citing "
        "test failed; **partial**, a citing test was skipped or not run; **no evidence**, no "
        "test cites the clause. A *walkthrough* clause is not decided by this run; its record "
        "is the walkthrough file."
    )

    lines = [
        "# Conformance Report: Message Guard",
        "",
        generated,
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
        lines += [
            f"- `{i}`: " + ", ".join(f"`{_short(t)}`" for t in by_id[i]) for i in unknown
        ]
    else:
        lines.append("None.")
    lines.append("")

    out = Path(session.config.rootpath) / REPORT
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")

    _summary = (gaps, unknown)
    if (gaps or unknown) and not _deselected:
        session.exitstatus = pytest.ExitCode.TESTS_FAILED


def pytest_terminal_summary(terminalreporter):
    if _summary is None:
        return
    gaps, unknown = _summary
    write = terminalreporter.write_line
    if not gaps and not unknown:
        write(f"conformance: every test clause has passing evidence; report in {REPORT}")
        return
    for gap in gaps:
        write(f"conformance: {gap}")
    for ident in unknown:
        write(f"conformance: marker names a clause the specifications do not define: {ident}")
    if _deselected:
        write("conformance: run not failed because tests were deselected (partial run)")
    else:
        write(f"conformance: FAIL, see {REPORT}")
