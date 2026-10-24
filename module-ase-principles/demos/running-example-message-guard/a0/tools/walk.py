"""Walkthrough helper: show what the guard does with one message.

    uv run python tools/walk.py LEVEL PAYLOAD      LEVEL is Public, Restricted, or Critical

Support for the walkthroughs recorded in records/walkthrough.md. It is not the realization of
any clause, so it sits outside the package and outside the coverage measurement.
"""

import sys

from guard import Message, SecurityLevel, filter_message


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    level, payload = argv
    try:
        message = Message(SecurityLevel(level), int(payload))
    except (TypeError, ValueError) as error:
        print(f"not a message: {error}")
        return 2
    out = filter_message(message)
    print("drop" if out is None else f"pass: {out.level.value} {out.payload}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
