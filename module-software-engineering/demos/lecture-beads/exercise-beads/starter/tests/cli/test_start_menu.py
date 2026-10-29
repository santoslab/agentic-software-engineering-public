"""Evidence for contracts/cli.md §2: the start menu."""

import io

import pytest

from five_in_a_row.cli import run

req = pytest.mark.req

CHOICES = ("Play the computer", "Play a friend", "Quit")


def session(*lines):
    out = io.StringIO()
    code = run(io.StringIO("".join(f"{line}\n" for line in lines)), out)
    return code, out.getvalue()


def menu_count(text):
    return text.count("Choose 1, 2 or 3")


@req("FR-014", "US3-1")
def test_start_menu_offers_exactly_three_numbered_choices():
    _, text = session("3")
    for number, label in enumerate(CHOICES, start=1):
        assert f"{number}  {label}" in text
    assert menu_count(text) == 1


@req("FR-016", "US3-4")
def test_quit_ends_the_program():
    code, text = session("3")
    assert code == 0
    assert menu_count(text) == 1  # the menu was shown once and nothing else was asked


@req("FR-016")
def test_quit_accepts_surrounding_spaces():
    code, text = session(" 3 ")
    assert code == 0
    assert menu_count(text) == 1


@req("FR-017", "SC-006", "EDGE-invalid-menu-choice")
@pytest.mark.parametrize("entry", ["7", "x", "", "1 2"])
def test_invalid_choice_is_rejected_and_the_menu_shown_again(entry):
    code, text = session(entry, "3")
    assert code == 0
    assert "not a choice" in text.lower()
    assert menu_count(text) == 2
