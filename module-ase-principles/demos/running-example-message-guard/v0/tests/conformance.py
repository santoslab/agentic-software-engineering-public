"""Read the clause identifiers and verification methods that the specifications define.

The specifications govern, so the conformance report takes its list of clauses from them
rather than from a hand-kept list. A clause is a line of the form
``**REQ-1** · Method: test ...``; the identifier and the method are read from it.
"""

import re
from pathlib import Path

SPECS_DIR = Path(__file__).resolve().parent.parent / "specs"
SPEC_FILES = ("conops.md", "requirements.md")

_CLAUSE = re.compile(r"^\*\*([A-Z]+-\d+)\*\* · Method: (\w+)")


def clauses(specs_dir: Path = SPECS_DIR) -> dict[str, tuple[str, str]]:
    """Return {identifier: (specification file, method)}, in document order."""
    found: dict[str, tuple[str, str]] = {}
    for name in SPEC_FILES:
        for line in (specs_dir / name).read_text(encoding="utf-8").splitlines():
            if match := _CLAUSE.match(line):
                found[match.group(1)] = (name, match.group(2))
    return found
