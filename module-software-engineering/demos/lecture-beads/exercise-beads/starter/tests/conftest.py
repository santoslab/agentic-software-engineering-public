"""Conformance-report plugin (constitution Principles I and V; plan research.md R7).

Every test tagged ``@pytest.mark.req(...)`` is evidence for the spec IDs it names. After
each run this plugin writes ``reports/conformance.md``: one row per spec ID, the tests
tagged with it, and their combined status.
"""

from datetime import datetime
from pathlib import Path

import pytest

from tests.conformance import GROUPS, SPEC_PATH, spec_ids

MANUAL_PREFIX = "manual:"

_tags: dict[str, tuple[str, ...]] = {}  # nodeid -> spec IDs
_outcomes: dict[str, tuple[str, str]] = {}  # nodeid -> (outcome, skip reason)


def pytest_collection_modifyitems(items):
    for item in items:
        ids = tuple(i for marker in item.iter_markers("req") for i in marker.args)
        if ids:
            _tags[item.nodeid] = ids


def pytest_runtest_logreport(report):
    if report.nodeid not in _tags:
        return
    if report.failed:
        _outcomes[report.nodeid] = ("failed", "")
    elif report.skipped:
        reason = report.longrepr[2] if isinstance(report.longrepr, tuple) else ""
        _outcomes[report.nodeid] = ("skipped", reason.removeprefix("Skipped: "))
    elif report.when == "call" and report.nodeid not in _outcomes:
        _outcomes[report.nodeid] = ("passed", "")


def _status(tests: list[str]) -> str:
    outcomes = [_outcomes.get(t, ("not run", "")) for t in tests]
    if not tests:
        return "**no evidence**"
    if any(o == "failed" for o, _ in outcomes):
        return "**FAIL**"
    if all(o == "passed" for o, _ in outcomes):
        return "pass"
    if all(o == "skipped" and r.startswith(MANUAL_PREFIX) for o, r in outcomes):
        return "manual"
    return "partial"


def _short(nodeid: str) -> str:
    return nodeid.removeprefix("tests/")


def pytest_sessionfinish(session):
    root = Path(session.config.rootpath)
    groups = spec_ids()
    known = {i for ids in groups.values() for i in ids}
    by_id: dict[str, list[str]] = {}
    for nodeid, ids in _tags.items():
        for i in ids:
            by_id.setdefault(i, []).append(nodeid)

    rows: dict[str, list[tuple[str, str, str]]] = {}
    counts: dict[str, int] = {}
    for group in GROUPS:
        rows[group] = []
        for i in groups[group]:
            tests = by_id.get(i, [])
            status = _status(tests)
            counts[status] = counts.get(status, 0) + 1
            listed = "<br>".join(f"`{_short(t)}`" for t in tests) or "—"
            rows[group].append((i, listed, status))

    lines = [
        "# Conformance Report: 001-five-in-a-row",
        "",
        f"**Generated**: {datetime.now():%Y-%m-%d %H:%M} | "
        f"**Spec**: `{SPEC_PATH.relative_to(root)}` | "
        f"**Tests tagged**: {len(_tags)}",
        "",
        "**Summary**: " + ", ".join(f"{s.strip('*')}: {n}" for s, n in sorted(counts.items())),
        "",
        "Status: **pass** — every tagged test passed; **FAIL** — a tagged test failed; "
        "**manual** — checked by hand (see quickstart.md); **partial** — some tagged tests "
        "skipped or not run; **no evidence** — no test is tagged with this ID.",
        "",
    ]
    for group in GROUPS:
        lines += [f"## {group}", "", "| ID | Tests | Status |", "|----|-------|--------|"]
        lines += [f"| {i} | {tests} | {status} |" for i, tests, status in rows[group]]
        lines.append("")

    unknown = sorted(i for i in by_id if i not in known)
    lines += ["## Unknown IDs", ""]
    if unknown:
        lines += ["Tags that name no ID in the spec:", ""]
        lines += [f"- `{i}`: " + ", ".join(f"`{_short(t)}`" for t in by_id[i]) for i in unknown]
    else:
        lines.append("None.")
    lines.append("")

    out = root / "reports" / "conformance.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
