"""Reading entries: squares and menu choices (contracts/cli.md C-1, C-2, C-7)."""

import re

from five_in_a_row.engine import Square

# Row then column: integers separated by spaces, or by a comma with optional spaces.
_MOVE = re.compile(r"^\s*(-?\d+)\s*(?:,|\s)\s*(-?\d+)\s*$")

LEAVE_COMMAND = "m"


def is_leave_command(text: str) -> bool:
    """`m` or `M`, surrounding spaces ignored (C-9). Checked before parse_move."""
    return text.strip().lower() == LEAVE_COMMAND


def parse_move(text: str) -> Square | None:
    """The square named by `text`, or None if it is not a row and column.

    Out-of-range numbers still give a Square; the engine rejects them (C-8).
    """
    match = _MOVE.match(text)
    if not match:
        return None
    return Square(int(match.group(1)), int(match.group(2)))


def parse_menu(text: str, choices: int) -> int | None:
    """The menu choice 1..choices named by `text`, or None (C-1, C-2)."""
    entry = text.strip()
    if entry.isdigit() and 1 <= int(entry) <= choices:
        return int(entry)
    return None
