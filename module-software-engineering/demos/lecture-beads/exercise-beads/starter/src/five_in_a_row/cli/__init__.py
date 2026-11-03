"""Terminal interface: menus, prompts, board drawing (contracts/cli.md).

This is the CLI's public API.
"""

import sys

from .app import run


def main() -> int:
    return run(sys.stdin, sys.stdout)


__all__ = ["main", "run"]
