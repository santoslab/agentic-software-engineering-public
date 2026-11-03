"""Evidence for contracts/cli.md §5 (C-17): end of input and interrupt at the start menu.

The mid-game case is in test_two_player.py (tasks.md T020).
"""

import io
import time

import pytest

from five_in_a_row.cli import run

req = pytest.mark.req


class InterruptingInput(io.StringIO):
    def readline(self, *args):
        raise KeyboardInterrupt


def run_timed(stdin):
    out = io.StringIO()
    start = time.monotonic()
    code = run(stdin, out)
    return code, out.getvalue(), time.monotonic() - start


def goodbye_lines(text):
    return [line for line in text.splitlines() if "goodbye" in line.lower()]


@req("FR-020", "US3-6", "EDGE-end-of-input-or-interrupt")
@pytest.mark.parametrize("script", ["", "7\n"], ids=["empty", "after-invalid-choice"])
def test_end_of_input_at_the_start_menu(script):
    code, text, seconds = run_timed(io.StringIO(script))
    assert code == 0
    assert len(goodbye_lines(text)) == 1
    assert "Traceback" not in text
    assert seconds < 1


@req("FR-020", "US3-6", "EDGE-end-of-input-or-interrupt")
def test_interrupt_at_the_start_menu():
    code, text, seconds = run_timed(InterruptingInput())
    assert code == 0
    assert len(goodbye_lines(text)) == 1
    assert seconds < 1
