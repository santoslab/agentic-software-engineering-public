"""The dependency rule between engine, opponent and cli (plan research.md R3).

cli -> opponent -> engine, and cli -> engine. Nothing points back, other subpackages are
used only through their public API, and only the cli does terminal I/O.

This is evidence for the plan's design rule, not for a spec ID, so it carries no req tag.
"""

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent / "src" / "five_in_a_row"
SUBPACKAGES = ("engine", "opponent", "cli")


def _modules():
    for path in sorted(PACKAGE.rglob("*.py")):
        rel = path.relative_to(PACKAGE)
        owner = rel.parts[0] if len(rel.parts) > 1 else None
        yield path, owner, ast.parse(path.read_text(encoding="utf-8"))


def _imports(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.module


def _target(name):
    """'five_in_a_row.engine.state' -> ('engine', 'five_in_a_row.engine.state')."""
    parts = name.split(".")
    if parts[0] == "five_in_a_row" and len(parts) > 1 and parts[1] in SUBPACKAGES:
        return parts[1]
    return None


def test_engine_imports_neither_opponent_nor_cli():
    for path, owner, tree in _modules():
        if owner == "engine":
            assert {_target(n) for n in _imports(tree)} <= {None, "engine"}, path


def test_opponent_does_not_import_cli():
    for path, owner, tree in _modules():
        if owner == "opponent":
            assert "cli" not in {_target(n) for n in _imports(tree)}, path


def test_other_subpackages_are_used_only_through_their_public_api():
    for path, owner, tree in _modules():
        for name in _imports(tree):
            target = _target(name)
            if target and target != owner:
                assert name == f"five_in_a_row.{target}", f"{path}: imports {name}"


def test_only_cli_does_terminal_io():
    for path, owner, tree in _modules():
        if owner == "cli":
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in ("print", "input"), f"{path}: {node.func.id}()"
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                if node.value.id == "sys":
                    assert node.attr not in ("stdin", "stdout"), f"{path}: sys.{node.attr}"
