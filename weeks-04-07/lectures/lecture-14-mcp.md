# Lecture 14 — MCP: Giving the Agent New Tools

> **Unit:** weeks-04-07 · **Week 7, meeting 2 of 2** · 75 minutes
>
> **Thesis:** MCP turns your program into something an agent can act *with* — and
> the tool docstring is an interface contract read by a machine that takes it
> literally.

## Learning objectives

After this lecture, students can:

1. Explain the MCP architecture — host, client, server; tools, resources — and
   place it on the agent-loop diagram from Lecture 05.
2. Write a FastMCP tool whose type hints become the schema and whose docstring
   works as the contract the model reads.
3. Register a local stdio server in Claude Code and verify the agent can discover
   and call it.
4. Critique a tool design: granularity, naming, error behavior as contract.

## Before class

- [required] MCP docs: core concepts + FastMCP quickstart.
- [required] `student-materials/mcp-example/README.md`.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–10 | Cold open: you've built this once already | Ex. 4 recall: you hand-wrote a tool schema, dispatched `tool_use` blocks, returned `tool_result`. MCP is that loop, standardized so tools can be *plugged in* rather than hard-coded: a protocol between the host (Claude Code) and tool servers anyone can write. Put the L05 loop diagram up; draw the server on it. Nothing new is happening at the model boundary — the tool list just got an extension socket. |
| 10–24 | Architecture, sized honestly | Host / client / server; local servers speak stdio (a subprocess — no network, no cloud); tools vs resources vs prompts (tools are the 90% case; the other two get one sentence each and a pointer). What registration actually does: the host launches your process, asks it what tools it has, and adds them to the same tool list Ex. 4 taught you to build by hand. Preview L23: today you *build* a server; in week 12 you'll *adopt* strangers' servers — and L24 asks what could go wrong with that. |
| 24–40 | FastMCP anatomy + the docstring as contract | The dice example on screen (~20 lines): `@mcp.tool()`, type hints → the schema, docstring → the description the model reads when deciding to call. Worked example, bad vs good for Stage E's `get_player_stats`: bad — *"gets stats for a player"* (which player? what shape? what if unknown?); good — states parameters, the return shape field by field, ordering, and the unknown-player behavior ("returns an error message naming the player; does not raise"). The model can't read your source; **the docstring is the entire interface** — write it like the API doc it is. |
| 40–54 | Demo 1 — build, register, watch it get called | Live: run the dice server; register it (`claude mcp add`); ask Claude something that needs it; watch the tool call and result flow. Then the reveal that matters for Stage E: change one word of the docstring to make it misleading, restart, and watch the agent misuse or skip the tool — the contract is load-bearing. |
| 54–64 | Tool contract design | Granularity: why `get_leaderboard` beats `run_sql(query)` — a narrow tool is a *contract* (stable, testable, safe); a raw-SQL tool is a capability dump (injection surface, schema coupling, and the agent will write queries you never tested). Error behavior is part of the contract: unknown player → a structured, named error the agent can act on, never a stack trace. Naming: the agent chooses tools by name + description — `get_player_stats` is discoverable; `query2` is not. |
| 64–75 | Stage E walkthrough + unit close | The checklist: two tools over the real Stage B DB, contract-quality docstrings, fresh-clone install per README-mcp.md, and the required transcript of Claude using both tools. The stretch: PKB-search MCP over your Project 0 bundle. Then the unit close: everything (A–E, retrospective) due at the start of week 8; L15 runs the P1 retrospective and opens the team unit. |

## Demos

### Demo 1 — Build, register, watch it get called

- **Artifacts:** `student-materials/mcp-example/dice_server.py` (complete);
  a scratch Claude Code project to register it in.
- **Setup (before class):** dependencies installed (`pip install "mcp[cli]"` or
  uv equivalent) and the server verified *today* on the presentation machine;
  registration command rehearsed; know how to show the tool list.
- **Script:** (1) read the server — 20 lines, mostly docstring; (2) register;
  (3) ask "roll 3d6 and tell me if we beat 12" — watch the call/result;
  (4) the sabotage beat: edit the docstring to claim the wrong return meaning,
  re-register, same question — the agent misreads the result exactly as
  documented; (5) restore. Moral spoken plainly: the docstring is the interface.
- **Expected outcome:** an MCP server demystified to "a Python file with decorated
  functions," and the contract's authority demonstrated, not asserted.
- **Fallback:** recorded run of the same beats; the sabotage moment survives on
  video. If registration misbehaves live, the `mcp dev` inspector is the backup
  path to show the server working in isolation.

## Discussion prompts

1. Where exactly does an MCP tool call appear in the Ex. 4 loop you wrote? Trace
   it: user turn → model → `tool_use` → *what process runs your code?* → 
   `tool_result` → model.
2. Make the case for and against a third Stage E tool, `record_game(...)` — a
   *write* tool. What changes in the contract's obligations the moment a tool
   mutates state?
3. Your PKB-search stretch tool: what should `search_pkb("coverage")` return —
   note bodies, or names + first lines? Defend the granularity.

## Assigned after class

- Readings (for L15, next unit): none — finish the project.
- Project: **Stage E** launched today; **everything due at the start of week 8**,
  including the half-page five-principles retrospective.

## Instructor notes

- **Cut if running long:** the architecture block (10–24) compresses to the
  loop-diagram slide + "stdio subprocess"; never cut the sabotage beat in the
  demo — it is the lecture's thesis made visible.
- **Risks:** MCP tooling moves fast — re-verify the registration command and the
  FastMCP import path against current docs the week of delivery, and pin the
  `mcp` package version in the example's README. The sabotage beat needs the
  *misleading* docstring, not a broken one (a broken server just errors; a lying
  docstring misleads — that's the point).
- **Variants:** strong room — live-code a third tool (`get_head_to_head(a, b)`)
  from a student-dictated docstring, then implement to match it: contract-first
  in miniature.
