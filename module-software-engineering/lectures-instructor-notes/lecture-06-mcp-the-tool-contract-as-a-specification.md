# Lecture 06 — MCP: The Tool Contract as a Specification

> **Unit:** module-software-engineering · **Module week 3, meeting 2 of 2** · 75 minutes
>
> **Thesis:** The ConOps names a "computer opponent" and says nothing about how
> it is built; an LLM can play that role through a tool contract — and the
> docstring is the whole interface the model can read.

## Learning objectives

After this lecture, students can:

1. Explain the MCP architecture — host, client, server; tools — and place a
   tool call on the agent-loop diagram from the foundations unit.
2. Write a FastMCP tool whose type hints become the schema and whose docstring
   is a contract: parameters and their ranges, the return shape, and error
   behavior as data.
3. Add the tool contract to the family of specifications and say what it must
   state that the interface contract need not.
4. Demonstrate that a contract is load-bearing by showing a misleading docstring
   change the agent's behavior.
5. Explain how a tool-call transcript serves as evidence against a ConOps
   scenario.

## Before class

Assigned at Lecture 05:

- [required] MCP documentation: core concepts; the FastMCP quickstart.
- [required] The dice-server README in the Project 1 student materials.
- [recommended] The *interface contract* and *tool contract* entries of the
  course catalog of specification kinds (`../../specification-kinds.md`).

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–8 | Cold open | `CONOPS.md` §4.4: "computer opponent — currently a uniformly random legal move." Today the actor is substituted without touching the ConOps. AUDCON-1 read the other way: because the ConOps names no implementation, a new implementation of an actor costs it nothing. |
| 8–20 | MCP, sized honestly | Host, client, server; a local server is a stdio subprocess; tools (resources and prompts get one sentence). On the loop diagram: the tool list gained an extension socket; nothing new happens at the model boundary. Registration = the host launches the process, asks what tools it has, adds them to the list. (Lifted from the Project 1 unit's MCP lecture, 10–24.) |
| 20–32 | The tool contract as a kind of specification | The last kind the module adds; its entry in the course catalog of specification kinds (`../../specification-kinds.md`). Derived from the interface contract (DEV-5) but obliged to say more, because the consumer cannot read the source: what an unknown `game_id` returns; that an illegal move returns a structured error and never raises; return shapes field by field. AUD-12 applied to a tool: behavior outside the precondition. Verified how: the schema, algorithmically; the behavior, by a call transcript a human or agent reads (VER-2, judgment) — a new VER binding row, not a new rule. |
| 32–52 | Demo 1 — build, register, play, sabotage (`t6`) | `tictactoe_server.py` pre-written: `new_game`, `board`, `legal_moves`, `make_move`, `computer_move`, `status`. Live-code only `make_move`'s docstring. `mcp dev` shows what the model reads. Register. *"Start a game and play as X against the random opponent; tell me each move you make and why."* Watch the calls. Sabotage: the docstring now claims rows are 0-indexed; restart; the agent plays off by one; restore. Variant to rehearse: `board` returning only the byte-exact string versus the string plus `legal_moves`. |
| 52–62 | Contract design | Granularity: why six narrow tools and not `run_python`. Errors as data the agent can relay. Naming: the agent chooses by name and description. State: the games live in the server for the session; every call ends in a known state. The call trace as evidence against `CONOPS.md` §5.1 (solo play to a win): validation by transcript. |
| 62–72 | Stage E previewed; the module closes | No project phase launches today — Phase 1 is in progress and due next week. Stage E of the project unit's brief puts this server shape over the Reversi engine Phase 1 produces; `legal_moves` becomes *necessary* — flanking is not readable off an ASCII board; the leaderboard variant after persistence. The catalog's summary table, with every kind the module demonstrated marked. The module's arc on one slide: S and R → ConOps → several kinds → tests as executable specification → a contract read by a machine. What the port lecture does with the "survives a port?" column. |

Blocks sum to 72 minutes; 3 minutes slack.

## Demos

### Demo 1 — Build, register, play, sabotage

- **Artifacts:** `../demos/lecture-06-mcp-demo/tictactoe_server.py` (to write; the demo folder does not exist yet)
  wrapping the `t5` engine; `mcp[cli]` pinned in the venv; the misleading
  docstring on a scratch branch; a recorded game transcript.
- **Setup (before class):** the server verified with `mcp dev` and registered on
  the presentation machine *that week* (the registration command and the
  FastMCP import path re-checked against current docs); a game rehearsed both
  with `board` alone and with `legal_moves`; captures at each step.
- **Script:** (1) read the server — mostly docstrings; (2) live-code
  `make_move`'s docstring from a student-dictated contract; (3) `mcp dev`; (4)
  register; (5) the game prompt; watch two or three exchanges; (6) sabotage,
  restart, the off-by-one move, restore (start a new game — server state was
  lost on restart, and say so); (7) the board-only variant if time allows.
- **Expected outcome:** the ConOps unchanged while its actor changed; a
  docstring shown to be load-bearing; a transcript that reads as scenario 5.1.
- **Fallback:** the recorded transcript; the sabotage moment survives on stills;
  `mcp dev` as the backup if registration misbehaves.

## Discussion prompts

1. Where in the specification family does the tool contract sit — derived from the interface
   contract, or a peer of it? What would AUD-3 check between the two?
2. The tool returned the byte-exact board string and the model misread it. Whose
   defect is that — the display specification's, the tool contract's, or
   neither's? What does the answer say about who a display specification is for?
3. Make the case for a `resign(game_id)` tool. What does the ConOps have to say
   first, and which process rule makes you say it there?

## Assigned after class

- Readings: none.
- Project: no new phase; **finish Project 1, Phase 1** (launched at Lecture 05,
  due one week after it, date per the brief). Stage E of
  `../../weeks-04-07/project-1-brief.md` will follow the shape shown today, over
  your Phase 1 engine.

## Instructor notes

- **Cut if running long:** the architecture block (8–20) compresses to the loop
  diagram and "a stdio subprocess"; the contract-design block to granularity and
  errors-as-data. Never cut the docstring sabotage.
- **Risks:** MCP tooling moves fast — re-verify the week of delivery and pin the
  package. The sabotage needs a *misleading* docstring, not a broken one. The
  model may read the 9×9 board correctly, in which case the board-only variant
  becomes "why expose structured state anyway" — either outcome teaches, but
  decide the framing at rehearsal, not live. In-memory game state is lost on
  restart; plan the sabotage as a new game.
- **Variants:** strong room — dictate a docstring for `resign`, implement to
  match, and audit the pair: contract-first in miniature.
