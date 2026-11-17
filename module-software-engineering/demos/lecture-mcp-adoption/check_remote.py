"""Real LLM-free discovery and documentation calls; stores bounded evidence."""
import argparse
import asyncio
from datetime import datetime, timezone
import json
import hashlib
from pathlib import Path

from mcp import Client

ENDPOINT = "https://learn.microsoft.com/api/mcp"
ARTICLE = "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.5"


def dump(obj):
    return obj.model_dump(mode="json", by_alias=True, exclude_none=True)


async def run(endpoint, output):
    async with Client(endpoint, read_timeout_seconds=45) as client:
        listing = await client.list_tools()
        calls = []
        for name, arguments in [
            ("microsoft_docs_search", {"query": "Get-ChildItem Recurse Depth parameter"}),
            ("microsoft_docs_fetch", {"url": ARTICLE}),
        ]:
            result = await client.call_tool(name, arguments)
            if result.is_error:
                raise RuntimeError(f"{name}: {result.content}")
            text = "\n".join(getattr(block, "text", "") for block in result.content)
            summary = {"isError": result.is_error, "content_types": [block.type for block in result.content],
                       "text_characters": len(text), "text_sha256": hashlib.sha256(text.encode()).hexdigest()}
            if name == "microsoft_docs_fetch":
                offset = text.find("### -Depth")
                summary["excerpt"] = " ".join(text[max(0, offset):].split()[:20])
            calls.append({"name": name, "arguments": arguments, "observed_result_summary": summary})
        # Read only non-secret negotiation information; never log HTTP headers.
        report = {"captured_at": datetime.now(timezone.utc).isoformat(),
                  "endpoint": endpoint, "kind": "LLM-free SDK client",
                  "tools": dump(listing), "calls": calls,
                  "protocol_version": str(client.session.protocol_version)}
    Path(output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"tools": [t.name for t in listing.tools],
                      "calls": [c["name"] for c in calls], "saved": output}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", default=ENDPOINT)
    parser.add_argument("--output", default="evidence/remote.json")
    args = parser.parse_args()
    asyncio.run(run(args.endpoint, args.output))
