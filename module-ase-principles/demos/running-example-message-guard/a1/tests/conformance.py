"""Read the identified clauses, scenarios, and findings that the specifications define.

The specifications govern, so every report takes its list of clauses from them rather than from a
hand-kept list. A clause header is one line of the form

    **REQ-1** · Method: test · Pattern: event-driven · Derived from: US-3

The identifier comes first; the rest of the line is ` · `-separated ``Key: value`` fields. A header
that is malformed (no ``Method``, an unknown method, key, or pattern, a duplicate identifier, a
judgment method without a ``Reason``, an identifier family in the wrong file) is reported as a
finding and never dropped silently (ConOps-SQ-1, Reqs-SQ-1, Reqs-SQ-2, Specs-TR-1; catalog page
``tooling/clause-reader.md``). Scenarios are read from ``specs/scenarios.json``, glossary terms from
``specs/glossary.md``, and the elicitation entries that ``Source`` fields cite from
``reference/elicitation.md``. Link resolution between all of these is ``tools/trace.py``'s job.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = ROOT / "specs"
ELICITATION = ROOT / "reference" / "elicitation.md"
SPEC_FILES = ("conops.md", "requirements.md")
SCENARIO_FILE = "scenarios.json"
GLOSSARY_FILE = "glossary.md"

METHODS = frozenset(
    {
        "test",
        "analysis",
        "review (human)",
        "review (agent)",
        "walkthrough (human)",
        "walkthrough (agent)",
    }
)
JUDGMENT_METHODS = frozenset(m for m in METHODS if m not in {"test", "analysis"})
PATTERNS = frozenset(
    {"ubiquitous", "event-driven", "state-driven", "unwanted-behavior", "optional-feature", "complex"}
)
KEYS = {
    "US": frozenset({"Method", "Scenarios", "User category", "Validated by", "Source", "Reason"}),
    "REQ": frozenset({"Method", "Pattern", "Derived from", "Reason"}),
}
FAMILY_FILE = {"US": "conops.md", "REQ": "requirements.md"}

_HEADER = re.compile(r"^\*\*([A-Z]+-\d+)\*\*(.*)$")
_IDENT = re.compile(r"\b[A-Z]+-\d+\b")
_TERM = re.compile(r"^- \*\*([^*]+?)\*\*")
_ENTRY = re.compile(r"^### (E-\d+)\b")
_SCENARIO_ID = re.compile(r"^SC-\d+$")


@dataclass(frozen=True)
class Finding:
    """One thing the reader could not accept; ``kind`` is a fixed vocabulary (see the catalog)."""

    kind: str
    where: str
    detail: str

    def __str__(self) -> str:
        return f"{self.kind} at {self.where}: {self.detail}"


@dataclass(frozen=True)
class Clause:
    id: str
    file: str
    line: int
    method: str | None
    fields: dict[str, str] = field(default_factory=dict, compare=False, hash=False)

    @property
    def family(self) -> str:
        return self.id.split("-")[0]

    def refs(self, key: str) -> list[str]:
        """Identifiers named in a field, e.g. ``Derived from: US-3`` or ``Scenarios: SC-1, SC-2``."""
        return _IDENT.findall(self.fields.get(key, ""))

    def glossary_refs(self) -> list[str]:
        """Terms named by a ``Derived from: Glossary: message, payload`` field."""
        value = self.fields.get("Derived from", "")
        if not value.startswith("Glossary:"):
            return []
        return [t.strip() for t in value.removeprefix("Glossary:").split(",") if t.strip()]


@dataclass(frozen=True)
class Scenario:
    id: str
    derived_from: str
    role: str
    input: dict
    expected: dict | None
    note: str | None = None


@dataclass
class Specs:
    """Everything the reader found, in document order, plus every finding."""

    clauses: dict[str, Clause]
    scenarios: list[Scenario]
    glossary: set[str]
    entries: set[str]
    findings: list[Finding]
    files: list[str]


def _parse_header(file: str, line_no: int, ident: str, rest: str, findings: list[Finding]) -> Clause:
    where = f"{file}:{line_no} {ident}"
    fields: dict[str, str] = {}
    for part in rest.split(" · "):
        part = part.strip()
        if not part:
            continue
        key, sep, value = part.partition(":")
        if not sep:
            findings.append(Finding("malformed header", where, f"field without a colon: {part!r}"))
            continue
        fields[key.strip()] = value.strip()
    family = ident.split("-")[0]
    allowed = KEYS.get(family)
    if allowed is None:
        findings.append(Finding("unknown family", where, f"no clause family {family!r}"))
    else:
        if FAMILY_FILE[family] != file:
            findings.append(Finding("wrong file", where, f"{family} clauses belong in {FAMILY_FILE[family]}"))
        for key in fields:
            if key not in allowed:
                findings.append(Finding("unknown key", where, f"{key!r} is not a field of a {family} clause"))
    method = fields.get("Method")
    if method is None:
        findings.append(Finding("malformed header", where, "no Method field"))
    elif method not in METHODS:
        findings.append(Finding("unknown method", where, f"{method!r} is not a verification method"))
    elif method in JUDGMENT_METHODS and "Reason" not in fields:
        findings.append(Finding("missing Reason", where, "a judgment clause states why it is not mechanical"))
    if family == "REQ":
        pattern = fields.get("Pattern")
        if pattern is None:
            findings.append(Finding("missing Pattern", where, "a requirement declares its EARS pattern"))
        elif pattern not in PATTERNS:
            findings.append(Finding("unknown pattern", where, f"{pattern!r} is not an EARS pattern"))
    return Clause(ident, file, line_no, method, fields)


def _read_scenarios(path: Path, findings: list[Finding]) -> list[Scenario]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        findings.append(Finding("malformed scenarios", path.name, str(error)))
        return []
    scenarios: list[Scenario] = []
    seen: set[str] = set()
    for index, raw in enumerate(data.get("scenarios", [])):
        where = f"{path.name} scenario {index + 1}"
        missing = [k for k in ("id", "derived_from", "input", "expected") if k not in raw]
        if missing:
            findings.append(Finding("malformed scenario", where, f"missing {', '.join(missing)}"))
            continue
        ident = raw["id"]
        if not _SCENARIO_ID.match(ident):
            findings.append(Finding("unknown family", where, f"{ident!r} is not an SC identifier"))
        if ident in seen:
            findings.append(Finding("duplicate identifier", where, f"{ident} is defined twice"))
            continue
        seen.add(ident)
        scenarios.append(
            Scenario(ident, raw["derived_from"], raw.get("role", ""), raw["input"], raw["expected"], raw.get("note"))
        )
    return scenarios


def _read_glossary(path: Path, findings: list[Finding]) -> set[str]:
    terms: set[str] = set()
    if not path.exists():
        return terms
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if match := _TERM.match(line):
            term = match.group(1).split(" (")[0].strip()
            if term in terms:
                findings.append(Finding("duplicate term", f"{path.name}:{line_no}", f"{term!r} is defined twice"))
            terms.add(term)
    return terms


def _read_entries(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {m.group(1) for line in path.read_text(encoding="utf-8").splitlines() if (m := _ENTRY.match(line))}


def read(specs_dir: Path = SPECS_DIR, elicitation: Path = ELICITATION) -> Specs:
    """Read every specification under ``specs_dir`` and report what could not be accepted."""
    findings: list[Finding] = []
    clauses: dict[str, Clause] = {}
    files: list[str] = []
    for name in SPEC_FILES:
        path = specs_dir / name
        if not path.exists():
            findings.append(Finding("missing specification", name, "file not found"))
            continue
        files.append(name)
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not (match := _HEADER.match(line)):
                continue
            clause = _parse_header(name, line_no, match.group(1), match.group(2), findings)
            if clause.id in clauses:
                first = clauses[clause.id]
                findings.append(
                    Finding(
                        "duplicate identifier",
                        f"{name}:{line_no} {clause.id}",
                        f"already defined at {first.file}:{first.line}",
                    )
                )
                continue
            clauses[clause.id] = clause
    scenarios = _read_scenarios(specs_dir / SCENARIO_FILE, findings)
    if (specs_dir / SCENARIO_FILE).exists():
        files.append(SCENARIO_FILE)
    glossary = _read_glossary(specs_dir / GLOSSARY_FILE, findings)
    if (specs_dir / GLOSSARY_FILE).exists():
        files.append(GLOSSARY_FILE)
    return Specs(clauses, scenarios, glossary, _read_entries(elicitation), findings, files)


def clauses(specs_dir: Path = SPECS_DIR) -> dict[str, tuple[str, str]]:
    """{identifier: (specification file, method)} for every clause with a method, in document order."""
    return {c.id: (c.file, c.method) for c in read(specs_dir).clauses.values() if c.method is not None}
