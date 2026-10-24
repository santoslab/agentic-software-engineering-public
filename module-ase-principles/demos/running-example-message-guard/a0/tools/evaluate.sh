#!/bin/sh
# The mechanical evaluations of process/judgments.md, in one command: Code-RQ-1 (ruff; the suite
# collects, which pytest checks before it runs anything), then Reqs-CONF-1 and the citation part
# of Specs-TR-1 (every test passes; requirements coverage, by the plugin in tests/conftest.py;
# structural coverage, by pytest-cov). Stops at the first failure. Exit 0 means every mechanical
# clause holds for the tree it was run on; the header says which state was checked and with which
# tool versions, and the assurance report copies it as provenance. Nothing runs this command for
# you and nothing waits for its result: it evaluates, it does not gate.
set -e
cd "$(dirname "$0")/.."
head=$(git rev-parse --short HEAD 2>/dev/null || echo "no repository")
dirty=$(git status --porcelain 2>/dev/null | grep -c . || true)
echo "evaluate: $(date '+%Y-%m-%d %H:%M') · HEAD $head, $dirty changed or untracked path(s) · $(uv run python --version) · $(uv run pytest --version 2>&1 | head -1) · pytest-cov $(uv run python -c 'import importlib.metadata as m; print(m.version("pytest-cov"))') · $(uv run ruff --version)"
uv run ruff check .
uv run pytest
