# Dice: one tool, several integration layers

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/). Tested versions and
remaining host rehearsal are in [verification](reports/verification.md).
No model account is required for the automated checks.

From this directory:

```sh
uv sync --locked
uv run --frozen python dice.py roll --count 3 --sides 6
uv run --frozen python dice.py flip_coins --count 5
uv run --frozen pytest -q
uv run --frozen python protocol_demo.py --stage E --output evidence/protocol-E.json
```

`dice.py` is an ordinary library with a JSON CLI. `dice_server.py` adds the
protocol adapter; it never prints diagnostics to stdout. SDK logs go to stderr.
Use `.venv/bin/python` directly after setup if uv's cache is unavailable.

| Stage | Launch / inspect | Change to observe |
|---|---|---|
| A | `uv run --frozen python dice.py roll --count 3` | Direct JSON result, no MCP |
| B | `uv run --frozen python dice_server.py --stage B` | One decorator tool, text results; domain errors are successful text |
| C | `uv run --frozen python protocol_demo.py --stage B` | Actual discovery and calls to B; see `evidence/wire-B.jsonl` |
| D | `uv run --frozen python protocol_demo.py --stage D` | Bounds in schema, strict integers, output model, explicit tool errors |
| E | `uv run --frozen python protocol_demo.py --stage E` | Coins added; host can select either tool |

A server launch waits for an MCP client on stdin. It is not a REPL. C is an
observation step, not another copy of the implementation. One factory exposes
the differences without maintaining several nearly identical servers.

The domain contract is always 1–20 dice, sides in 4/6/8/10/12/20, and 1–100 coins.
B uses SDK integer parsing (which may coerce some values), plain text, and catches
function errors into `Error:` text. D/E use strict integer fields; count bounds
are in the schema, and the sides whitelist deliberately remains a function check.
Descriptions say so. A future enum schema could advertise that whitelist too.
D/E return Pydantic models, yielding output schemas and structured results.
They do not claim cryptographic randomness or demonstrate statistical fairness.

See [the rehearsal script](DEMO.md), [development prompt](agent-prompt.md), and
[tests](tests/test_dice.py). The JSON/JSONL evidence is a real LLM-free capture;
random values will vary on rerun. `wire_proxy.py` is a teaching tee around a real
subprocess, not part of the server or a general logging framework.
