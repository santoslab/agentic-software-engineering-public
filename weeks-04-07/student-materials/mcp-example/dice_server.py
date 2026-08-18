"""A minimal FastMCP server in a neutral domain (Lecture 14's demo).

This example exists to show the *shape* of an MCP server — the decorator, the
type hints becoming the schema, the docstring as the contract the model reads.
Stage E's server queries your real Stage B database instead; do not copy this
file, copy its discipline.

Run directly:      python dice_server.py
Inspect:           mcp dev dice_server.py
Register:          see README.md (verify the command against current docs)
"""

import random

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dice")

ALLOWED_SIDES = (4, 6, 8, 10, 12, 20)


@mcp.tool()
def roll(count: int = 1, sides: int = 6) -> str:
    """Roll dice and report each result and the total.

    Args:
        count: number of dice to roll, 1 to 20.
        sides: faces per die; one of 4, 6, 8, 10, 12, 20.

    Returns one line: the individual rolls in order, then "total: N".
    Out-of-range arguments return an error message naming the limit;
    no exception is raised.
    """
    if not 1 <= count <= 20:
        return "Error: count must be between 1 and 20."
    if sides not in ALLOWED_SIDES:
        return f"Error: sides must be one of {ALLOWED_SIDES}."
    rolls = [random.randint(1, sides) for _ in range(count)]
    return f"rolls: {rolls} total: {sum(rolls)}"


@mcp.tool()
def flip_coins(count: int = 1) -> str:
    """Flip one or more fair coins.

    Args:
        count: number of coins to flip, 1 to 100.

    Returns the flip sequence as a string of H and T characters, then the
    head and tail counts. Out-of-range count returns an error message
    naming the limit; no exception is raised.
    """
    if not 1 <= count <= 100:
        return "Error: count must be between 1 and 100."
    flips = [random.choice("HT") for _ in range(count)]
    return (
        f"flips: {''.join(flips)} "
        f"heads: {flips.count('H')} tails: {flips.count('T')}"
    )


if __name__ == "__main__":
    mcp.run()
