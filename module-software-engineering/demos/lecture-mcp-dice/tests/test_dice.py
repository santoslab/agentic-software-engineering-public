import asyncio
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

from mcp import Client
from mcp.client.stdio import StdioServerParameters
import pytest

import dice
from dice_server import build_server

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("sides", dice.ALLOWED_SIDES)
@pytest.mark.parametrize("count", [1, 20])
def test_roll_bounds(count, sides):
    result = dice.roll(count, sides)
    assert len(result["rolls"]) == count
    assert all(1 <= n <= sides for n in result["rolls"])
    assert result["total"] == sum(result["rolls"])


def test_controlled_randomness():
    with patch("dice.random.randint", side_effect=[1, 6, 3]):
        assert dice.roll(3) == {"rolls": [1, 6, 3], "total": 10, "sides": 6}
    with patch("dice.random.choice", side_effect=list("HTH")):
        assert dice.flip_coins(3) == {"flips": "HTH", "heads": 2, "tails": 1}


@pytest.mark.parametrize("count", [1, 100])
def test_coin_bounds(count):
    result = dice.flip_coins(count)
    assert len(result["flips"]) == count
    assert set(result["flips"]) <= set("HT")
    assert result["heads"] == result["flips"].count("H")
    assert result["tails"] == result["flips"].count("T")
    assert result["heads"] + result["tails"] == count


@pytest.mark.parametrize("fn,kwargs", [(dice.roll, {"count": c}) for c in [0, 21, -1, True, 1.5, "3"]]
                         + [(dice.roll, {"sides": s}) for s in [0, 7, True, "6"]]
                         + [(dice.flip_coins, {"count": c}) for c in [0, 101, -1, False, 2.5, "2"]])
def test_invalid_functions(fn, kwargs):
    with pytest.raises(ValueError):
        fn(**kwargs)


def test_sdk_contracts():
    async def check():
        for stage, names in [("B", ["roll"]), ("D", ["roll"]), ("E", ["roll", "flip_coins"])]:
            async with Client(build_server(stage)) as client:
                listing = await client.list_tools()
                assert [t.name for t in listing.tools] == names
                tool = listing.tools[0]
                assert "sides" in tool.description
                if stage != "B":
                    assert tool.input_schema["properties"]["count"]["maximum"] == 20
                    assert tool.output_schema["properties"]["rolls"]["type"] == "array"
                with patch("dice.random.randint", return_value=4):
                    result = await client.call_tool("roll", {"count": 3})
                assert not result.is_error
                if stage == "B":
                    assert "total: 12" in result.content[0].text
                else:
                    assert result.structured_content == {"rolls": [4, 4, 4], "total": 12, "sides": 6}
                    assert json.loads(result.content[0].text) == result.structured_content
                result = await client.call_tool("roll", {"count": 0})
                assert result.is_error == (stage != "B")
                for kwargs in [{"count": "many"}, {"sides": 7}]:
                    result = await client.call_tool("roll", kwargs)
                    assert result.is_error == (kwargs == {"count": "many"} or stage != "B")
                if stage == "E":
                    for kwargs in [{"count": 0}, {"count": 101}, {"count": True}, {"count": "2"}]:
                        assert (await client.call_tool("flip_coins", kwargs)).is_error
                    assert (await client.call_tool("roll", {"count": True})).is_error
                    assert (await client.call_tool("roll", {"sides": "6"})).is_error
                    for count in [1, 100]:
                        result = await client.call_tool("flip_coins", {"count": count})
                        assert not result.is_error
                        assert result.structured_content["heads"] + result.structured_content["tails"] == count
    asyncio.run(check())


def test_stdio_launch_and_calls():
    async def check():
        async with Client(StdioServerParameters(command=sys.executable,
                          args=[str(ROOT / "dice_server.py")]), read_timeout_seconds=10) as client:
            assert len((await client.list_tools()).tools) == 2
            for name in ["roll", "flip_coins"]:
                assert not (await client.call_tool(name, {"count": 2})).is_error
            assert (await client.call_tool("roll", {"sides": 7})).is_error
    asyncio.run(check())


def test_protocol_failure():
    request = {"jsonrpc": "2.0", "id": 99, "method": "tools/call",
               "params": {"_meta": {"io.modelcontextprotocol/protocolVersion": "2026-07-28",
                                    "io.modelcontextprotocol/clientCapabilities": {}}}}
    process = subprocess.run([sys.executable, str(ROOT / "dice_server.py")],
                             input=json.dumps(request) + "\n", text=True, capture_output=True, timeout=10)
    assert process.returncode == 0
    response = json.loads(process.stdout)
    assert response["id"] == 99
    assert "error" in response and "result" not in response
    assert response["error"]["code"] == -32602
