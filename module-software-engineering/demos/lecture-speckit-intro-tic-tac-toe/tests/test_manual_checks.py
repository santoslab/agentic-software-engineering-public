"""Spec criteria that only a person can check (shown as "manual" in the report)."""

import pytest


@pytest.mark.req("SC-002")
def test_learnable_by_watching_one_game():
    pytest.skip("manual: quickstart.md — a person who watched one game plays one unaided")
