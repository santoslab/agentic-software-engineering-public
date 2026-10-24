"""Trace matrix: resolve every declared link between the specifications and the suite (Specs-TR-2).

    uv run python tools/trace.py          writes reports/trace-matrix.md; exit 1 on any finding

The matrix runs forward (story -> requirements -> scenarios -> tests) and backward (requirement ->
story; test -> clauses). A link that does not resolve, a story with no requirement, a requirement
with no derivation, a test clause with no citing test, and every finding of the clause reader are
listed under "Findings", and the exit code is non-zero if that list is not empty. The tool decides
links only: whether a requirement says what its story says, or whether a test's assertions check
its clause, still needs a reader. Its requirements, the prompt that produced it, and the cases it
must fail on are on the catalog page ``tooling/trace.md``.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tests.conformance import ELICITATION, SPECS_DIR, Finding, Specs, read

VERSION = "1.0"
REPORT = ROOT / "reports" / "trace-matrix.md"
Citations = dict[str, tuple[str, ...]]  # test nodeid -> clause identifiers it cites


def collect_citations(root: Path = ROOT) -> Citations:
    """Collect the suite without running it and return every test's citations."""
    import pytest

    class Collector:
        def __init__(self) -> None:
            self.tags: Citations = {}

        def pytest_collection_modifyitems(self, items):
            for item in items:
                self.tags[item.nodeid] = tuple(i for m in item.iter_markers("req") for i in m.args)

    collector = Collector()
    args = ["--collect-only", "--no-cov", "-p", "no:cacheprovider", "-p", "no:terminal", str(root / "tests")]
    code = pytest.main(args, plugins=[collector])
    if code != 0:
        raise SystemExit(f"trace: the suite did not collect (pytest exit {code}); run `uv run pytest` first")
    return collector.tags


def link_findings(specs: Specs, citations: Citations) -> list[Finding]:
    """Every declared link that does not resolve, in both directions."""
    findings: list[Finding] = []
    stories = {c.id for c in specs.clauses.values() if c.family == "US"}
    scenario_ids = {s.id for s in specs.scenarios}
    derived: dict[str, list[str]] = {}
    for clause in specs.clauses.values():
        where = f"{clause.file}:{clause.line} {clause.id}"
        for ref in clause.refs("Derived from"):
            if ref not in specs.clauses:
                findings.append(Finding("dangling reference", where, f"Derived from {ref}, which is not defined"))
            derived.setdefault(ref, []).append(clause.id)
        for term in clause.glossary_refs():
            if term not in specs.glossary:
                findings.append(Finding("dangling reference", where, f"Derived from glossary term {term!r}, not defined"))
        if clause.family == "REQ" and not clause.refs("Derived from") and not clause.glossary_refs():
            findings.append(Finding("requirement without derivation", where, "no story or glossary term"))
        for ref in clause.refs("Scenarios"):
            if ref not in scenario_ids:
                findings.append(Finding("dangling reference", where, f"Scenarios names {ref}, which is not in scenarios.json"))
        for ref in clause.refs("Source"):
            if ref not in specs.entries:
                findings.append(Finding("dangling reference", where, f"Source {ref} is not an entry of the elicitation record"))
    for story in sorted(stories):
        if not derived.get(story):
            findings.append(Finding("story without requirement", story, "no requirement derives from it"))
    for scenario in specs.scenarios:
        where = f"scenarios.json {scenario.id}"
        story = specs.clauses.get(scenario.derived_from)
        if story is None or story.family != "US":
            findings.append(Finding("dangling reference", where, f"derived_from {scenario.derived_from} is not a story"))
        elif scenario.id not in story.refs("Scenarios"):
            findings.append(Finding("scenario not listed", where, f"{story.id} does not list it in its Scenarios field"))
    cited: set[str] = set()
    for nodeid, ids in citations.items():
        for ident in ids:
            cited.add(ident)
            if ident not in specs.clauses:
                findings.append(Finding("dangling marker", nodeid, f"cites {ident}, which is not defined"))
    for clause in specs.clauses.values():
        if clause.method == "test" and clause.id not in cited:
            findings.append(Finding("test clause without a citing test", clause.id, "no test cites it"))
    return findings


def _repository_state(root: Path) -> str:
    try:
        head = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True, text=True, check=False
        )
        if head.returncode != 0:
            return "not a git repository"
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=False
        )
        dirty = len([line for line in status.stdout.splitlines() if line.strip()])
        return f"HEAD {head.stdout.strip()}, " + ("clean working tree" if dirty == 0 else f"{dirty} changed or untracked path(s)")
    except FileNotFoundError:
        return "git not available"


def _short(nodeid: str) -> str:
    return nodeid.removeprefix("tests/")


def _tests_citing(ident: str, citations: Citations) -> str:
    tests = sorted(_short(n) for n, ids in citations.items() if ident in ids)
    return "<br>".join(f"`{t}`" for t in tests) or "—"


def build(specs: Specs, citations: Citations, state: str = "not recorded") -> tuple[str, list[Finding]]:
    """Return the report text and every finding (the reader's and the links')."""
    findings = list(specs.findings) + link_findings(specs, citations)
    stories = [c for c in specs.clauses.values() if c.family == "US"]
    requirements = [c for c in specs.clauses.values() if c.family == "REQ"]
    by_story: dict[str, list[str]] = {}
    for req in requirements:
        for ref in req.refs("Derived from"):
            by_story.setdefault(ref, []).append(req.id)
    scen_by_story: dict[str, list[str]] = {}
    for s in specs.scenarios:
        scen_by_story.setdefault(s.derived_from, []).append(s.id)
    files = ", ".join(f"`specs/{f}`" for f in specs.files)
    cited = sum(1 for ids in citations.values() if ids)
    lines = [
        "# Trace Matrix: Message Guard",
        "",
        (
            f"Generated {datetime.now():%Y-%m-%d %H:%M} by `tools/trace.py` {VERSION} from {files} and "
            f"`reference/elicitation.md`; citations from {len(citations)} collected tests ({cited} cite a "
            f"clause). Repository state: {state}."
        ),
        "",
        (
            "**Scope**: every declared link, in both directions. The tool decides whether a link resolves, "
            "not whether the linked texts agree; that review is the audit's (procedure Audit)."
        ),
        "",
        "## Forward: story to requirements to scenarios to tests",
        "",
        "| Story | Source | Requirements | Scenarios | Tests citing the story | Tests citing its requirements |",
        "|---|---|---|---|---|---|",
    ]
    for story in stories:
        reqs = by_story.get(story.id, [])
        req_tests = sorted({_short(n) for n, ids in citations.items() if any(r in ids for r in reqs)})
        lines.append(
            f"| {story.id} | {', '.join(story.refs('Source')) or '—'} | {', '.join(reqs) or '—'} | "
            f"{', '.join(scen_by_story.get(story.id, [])) or '—'} | {_tests_citing(story.id, citations)} | "
            f"{'<br>'.join(f'`{t}`' for t in req_tests) or '—'} |"
        )
    lines += [
        "",
        "## Backward: requirement to its derivation and its tests",
        "",
        "| Requirement | Pattern | Derived from | Tests citing it |",
        "|---|---|---|---|",
    ]
    for req in requirements:
        lines.append(
            f"| {req.id} | {req.fields.get('Pattern', '—')} | {req.fields.get('Derived from', '—')} | "
            f"{_tests_citing(req.id, citations)} |"
        )
    lines += ["", "## Backward: test to the clauses it cites", "", "| Test | Clauses |", "|---|---|"]
    for nodeid in sorted(citations):
        if citations[nodeid]:
            lines.append(f"| `{_short(nodeid)}` | {', '.join(citations[nodeid])} |")
    lines += ["", "## Findings", ""]
    if findings:
        lines += [f"- {f}" for f in findings]
    else:
        lines.append("None.")
    lines.append("")
    return "\n".join(lines), findings


def main() -> int:
    specs = read(SPECS_DIR, ELICITATION)
    citations = collect_citations(ROOT)
    text, findings = build(specs, citations, _repository_state(ROOT))
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(text, encoding="utf-8")
    if findings:
        for finding in findings:
            print(f"trace: {finding}")
        print(f"trace: {len(findings)} finding(s), see {REPORT.relative_to(ROOT)}")
        return 1
    print(f"trace: every declared link resolves; matrix in {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
