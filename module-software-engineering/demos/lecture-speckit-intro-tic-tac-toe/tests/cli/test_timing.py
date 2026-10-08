"""Evidence for SC-001: the first move can be made well within 15 seconds of launch.

This measures the program's part only; the person's part is checked in quickstart.md M4.
"""

import io
import time

import pytest

from five_in_a_row.cli import run

req = pytest.mark.req


@req("SC-001")
def test_first_move_prompt_appears_quickly():
    out = io.StringIO()
    start = time.monotonic()
    run(io.StringIO("2\n"), out)
    elapsed = time.monotonic() - start
    assert "X to move" in out.getvalue()
    assert elapsed < 15
