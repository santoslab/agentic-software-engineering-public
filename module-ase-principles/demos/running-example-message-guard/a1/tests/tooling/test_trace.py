"""The trace tool's known-violation set: inputs it must report a finding on (Specs-TR-2; CF-06).

Each directory under ``cases/`` overlays one or two files on ``cases/base/`` (a minimal, clean
family of specifications) and states in ``expected.json`` which finding kinds the tool must
report. ``base`` itself must produce no finding. These tests cite no clause: they are tests of a
verifier, not evidence for a product requirement, and the suite accepts them uncited (citations are optional; Specs-TR-1 only requires that a citation resolve).
"""

import json
import shutil
from pathlib import Path

import pytest

from tests.conformance import read
from tools.trace import build

CASES = Path(__file__).resolve().parent / "cases"
BASE = CASES / "base"


def _overlay(case: Path, target: Path) -> None:
    shutil.copytree(BASE, target, dirs_exist_ok=True)
    for path in case.rglob("*"):
        if path.is_file() and path.name != "expected.json":
            destination = target / path.relative_to(case)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(path, destination)


def _run(case: Path, tmp_path: Path):
    _overlay(case, tmp_path)
    citations = {k: tuple(v) for k, v in json.loads((tmp_path / "citations.json").read_text()).items()}
    specs = read(tmp_path / "specs", tmp_path / "reference" / "elicitation.md")
    _, findings = build(specs, citations)
    return sorted({f.kind for f in findings})


def test_base_is_clean(tmp_path):
    assert _run(BASE, tmp_path) == []


@pytest.mark.parametrize("case", sorted(p for p in CASES.iterdir() if p.is_dir() and p.name != "base"), ids=lambda p: p.name)
def test_case_reports_expected_findings(case, tmp_path):
    expected = json.loads((case / "expected.json").read_text())
    assert _run(case, tmp_path) == sorted(expected["findings"]), expected.get("why")
