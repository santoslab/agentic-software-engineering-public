"""LLM-free discovery/call rehearsal, with real stdio wire capture."""
import argparse
import asyncio
import json
from pathlib import Path
import sys

from mcp import Client
from mcp.client.stdio import StdioServerParameters

ROOT = Path(__file__).resolve().parent


async def run(stage="E", output=None):
    wire = ROOT / "evidence" / f"wire-{stage}.jsonl"
    params = StdioServerParameters(command=sys.executable, args=[
        str(ROOT / "wire_proxy.py"), str(wire), sys.executable,
        str(ROOT / "dice_server.py"), "--stage", stage])
    async with Client(params) as client:
        listing = await client.list_tools()
        calls = []
        cases = [("roll", {"count": 3, "sides": 6}),
                 ("roll", {"count": 0}), ("roll", {"count": "many"}),
                 ("roll", {"sides": 7})]
        if stage == "E":
            cases.append(("flip_coins", {"count": 5}))
        for name, args in cases:
            result = await client.call_tool(name, args)
            calls.append({"name": name, "arguments": args,
                          "result": result.model_dump(mode="json", by_alias=True, exclude_none=True)})
        report = {"stage": stage, "tools": listing.model_dump(mode="json", by_alias=True, exclude_none=True),
                  "calls": calls}
    rendered = json.dumps(report, indent=2)
    if output:
        Path(output).write_text(rendered + "\n")
    print(rendered)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["B", "D", "E"], default="E")
    parser.add_argument("--output")
    args = parser.parse_args()
    asyncio.run(run(args.stage, args.output))
