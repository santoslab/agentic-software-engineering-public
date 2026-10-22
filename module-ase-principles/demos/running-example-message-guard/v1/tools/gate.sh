#!/bin/sh
# The gate command named by rule WF-1: realization quality (ruff, collection), then the
# conformance aggregate (every test passes; requirements coverage, by the plugin in
# tests/conftest.py; structural coverage, by pytest-cov), then traceability (every declared link
# resolves, by tools/trace.py). Exit 0 is green. The header line records what was checked and by
# which versions (the hand convention for provenance, catalog page tooling/gate.md).
set -e
cd "$(dirname "$0")/.."
head=$(git rev-parse --short HEAD 2>/dev/null || echo "no repository")
dirty=$(git status --porcelain 2>/dev/null | grep -c . || true)
echo "gate: $(date '+%Y-%m-%d %H:%M') · HEAD $head, $dirty changed or untracked path(s) · $(uv run python --version) · $(uv run pytest --version 2>&1 | head -1) · pytest-cov $(uv run python -c 'import importlib.metadata as m; print(m.version("pytest-cov"))') · $(uv run ruff --version) · trace.py 1.0"
uv run ruff check .
uv run pytest
uv run python tools/trace.py
