#!/bin/sh
# The gate command named by rule WF-1: realization quality (ruff, collection), then the
# conformance aggregate (every test passes; requirements coverage, by the plugin in
# tests/conftest.py; structural coverage, by pytest-cov). Exit 0 is green.
set -e
cd "$(dirname "$0")/.."
uv run ruff check .
uv run pytest
