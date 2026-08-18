# MCP Example — Dice Server

A complete, minimal FastMCP server in a domain deliberately unrelated to Stage E
(so the *shape* transfers and the solution doesn't). Two tools, both showing the
contract discipline Lecture 14 grades: parameter limits stated, return shape
stated, error behavior stated — because the docstring is the interface.

## Install

```sh
pip install "mcp[cli]"
```

Pin the version that works for you in your own project's requirements (the MCP
SDK moves quickly; a pinned version is part of "works from a fresh clone").

## Try it without an agent

```sh
mcp dev dice_server.py
```

opens the MCP Inspector: see the tool list (note: derived entirely from
decorators + type hints + docstrings), call `roll(3, 6)` by hand, read what the
model would read.

## Register with Claude Code

```sh
claude mcp add dice -- python dice_server.py
```

(Verify the exact syntax against the current Claude Code MCP docs — the tooling
evolves; the docs, not this README, are authoritative.) Then ask Claude to roll
dice and watch the tool call in the transcript — the Lecture 14 demo.

## What to steal for Stage E

- One `@mcp.tool()` function per contract; type hints on every parameter.
- Docstrings that state: what each argument means and its limits, the exact
  return shape, and what happens on bad input ("returns an error message; no
  exception is raised" — an agent can relay that; it cannot relay a traceback).
- Bounded inputs (`count <= 20`): a tool is a promise, and unbounded promises
  are how a helpful agent accidentally rolls a million dice.
