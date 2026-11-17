"""Stages B–E. Run with --stage B, D, or E (default); C inspects B on the wire."""
import argparse
from typing import Annotated, Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel, Field

import dice


class RollResult(BaseModel):
    rolls: list[int]
    total: int
    sides: int


class CoinResult(BaseModel):
    flips: str
    heads: int
    tails: int


Count = Annotated[int, Field(strict=True, ge=1, le=20)]
CoinCount = Annotated[int, Field(strict=True, ge=1, le=100)]
Sides = Annotated[int, Field(strict=True)]


def build_server(stage: Literal["B", "D", "E"] = "E") -> MCPServer:
    mcp = MCPServer("dice", instructions="Roll bounded dice or flip coins using these tools.")
    if stage == "B":
        @mcp.tool()
        def roll(count: int = 1, sides: int = 6) -> str:
            """Roll 1–20 dice with 4/6/8/10/12/20 sides. Return rolls and total.

            Invalid values return ordinary text beginning Error:, not an MCP error.
            """
            try:
                result = dice.roll(count, sides)
            except ValueError as exc:
                return f"Error: {exc}"
            return f"rolls: {result['rolls']} total: {result['total']}"
    else:
        @mcp.tool()
        def roll(count: Count = 1, sides: Sides = 6) -> RollResult:
            """Roll 1–20 dice; sides must be 4, 6, 8, 10, 12, or 20.

            Return ordered rolls, their total, and sides. Invalid inputs are tool errors.
            Count is schema-validated; the allowed sides are checked by the function.
            """
            try:
                return RollResult(**dice.roll(count, sides))
            except ValueError as exc:
                raise ToolError(str(exc)) from exc

        if stage == "E":
            @mcp.tool()
            def flip_coins(count: CoinCount = 1) -> CoinResult:
                """Flip 1–100 coins. Return the H/T sequence and head/tail tallies.

                Invalid count is a tool error. Each flip uses the local PRNG.
                """
                return CoinResult(**dice.flip_coins(count))
    return mcp


mcp = build_server()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["B", "D", "E"], default="E")
    build_server(parser.parse_args().stage).run()
