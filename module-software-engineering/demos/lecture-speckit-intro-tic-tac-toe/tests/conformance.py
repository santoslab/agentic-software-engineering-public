"""Read the requirement IDs that spec.md defines (plan research.md R7).

The spec is the governing document, so the conformance report takes its list of IDs
from there rather than from a hand-kept list.
"""

import re
from pathlib import Path

SPEC_PATH = Path(__file__).resolve().parent.parent / "specs" / "001-five-in-a-row" / "spec.md"

GROUPS = ("Functional Requirements", "Success Criteria", "Acceptance Scenarios", "Edge Cases")

_FR = re.compile(r"\*\*(FR-\d{3})\*\*")
_SC = re.compile(r"\*\*(SC-\d{3})\*\*")
_STORY = re.compile(r"^### User Story (\d+)\b")
_SCENARIO = re.compile(r"^(\d+)\. \*\*Given\*\*")
_EDGE = re.compile(r"^- \*\*(.+?)\*\*:")


def edge_slug(name: str) -> str:
    """'Out-of-range square' -> 'EDGE-out-of-range-square'."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"EDGE-{slug}"


def spec_ids(spec_path: Path = SPEC_PATH) -> dict[str, list[str]]:
    """Return the spec's IDs grouped as in GROUPS, each group in document order."""
    ids: dict[str, list[str]] = {group: [] for group in GROUPS}
    story = None
    in_edge_cases = False
    for line in spec_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            match = _STORY.match(line)
            story = match.group(1) if match else None
            in_edge_cases = line.strip() == "### Edge Cases"
            continue
        ids["Functional Requirements"] += _FR.findall(line)
        ids["Success Criteria"] += _SC.findall(line)
        if story and (match := _SCENARIO.match(line)):
            ids["Acceptance Scenarios"].append(f"US{story}-{match.group(1)}")
        if in_edge_cases and (match := _EDGE.match(line)):
            ids["Edge Cases"].append(edge_slug(match.group(1)))
    # A definition appears once; later mentions in prose are not bold, but keep order unique.
    return {group: list(dict.fromkeys(values)) for group, values in ids.items()}
