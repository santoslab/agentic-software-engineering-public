# Lecture 14 — MCP: Giving the Agent New Tools

> Week 7, meeting 2 of 2. Companion reading for the lecture; self-contained.
> Launches **Stage E** — the final stage. Everything is due at the start of
> week 8.

## You have built this once already

In Exercise 4 you wrote the tool-use side of an agent by hand: you declared a
tool schema in the API request, watched the model return a `tool_use` block,
dispatched it to your Python function, and sent back a `tool_result`. Nothing
about that machinery was Claude-Code-specific — it is how every tool call in
this course has worked, including every file read Claude Code has ever done for
you.

**MCP (Model Context Protocol) is that loop with an extension socket.** Instead
of tools being hard-coded into the harness, a protocol lets any process offer
tools to any agent host. Claude Code (the *host*) launches your program (the
*server*) as a subprocess, asks it what tools it offers, and adds them to the
same tool list you built by hand in Exercise 4. When the model emits a tool
call, the host routes it to your process over stdio and returns your answer as
the tool result. Draw it on the Lecture 05 loop diagram and exactly one thing
is new: the tool table has a socket in it, and your code is plugged into the
socket.

The vocabulary, sized honestly: servers can offer **tools** (functions the
model calls — the 90% case and all of Stage E), **resources** (readable
context, like files), and **prompts** (canned templates). Local servers speak
stdio — a subprocess, no network. That is the entire architecture you need
this week. In week 12 you will meet the ecosystem of servers other people have
published (L23), and the lecture after that asks what could go wrong with
plugging strangers' processes into your agent (L24). Today, you build your
own, so that when you adopt others' you know exactly what you are adopting.

## FastMCP: the shape of a server

The Python SDK's FastMCP layer makes a server almost embarrassingly small.
The neutral-domain example shipped in `student-materials/mcp-example/`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dice")

@mcp.tool()
def roll(count: int = 1, sides: int = 6) -> str:
    """Roll dice and report each result and the total.

    Args:
        count: number of dice, 1 to 20.
        sides: faces per die, one of 4, 6, 8, 10, 12, 20.

    Returns one line: the individual rolls, then "total: N".
    Out-of-range arguments return an error message naming the limit;
    no exception is raised.
    """
    ...

if __name__ == "__main__":
    mcp.run()
```

Three mappings do all the work, and they are worth staring at because Stage E
is graded on how well you use them:

- **The decorator registers the function** as a tool, under its own name.
  Naming is interface design: the model chooses tools by reading names and
  descriptions. `get_player_stats` announces itself; `query2` is a coin flip.
- **The type hints become the schema.** `count: int = 1` is exactly the JSON
  schema you wrote by hand in Exercise 4, derived. Wrong or missing hints are
  a wrong schema — the model will send you strings you didn't expect.
- **The docstring becomes the description the model reads.** Read that
  sentence again, because it is the lecture's thesis: the model cannot see
  your source code. The docstring is not documentation *about* the interface.
  It **is** the interface.

## The docstring is the contract

Here is the worked pair for Stage E's second tool. The bad version:

```python
@mcp.tool()
def get_player_stats(name: str) -> str:
    """Gets stats for a player."""
```

What is the model supposed to do with that? It does not know what "stats"
contains, in what shape, or what happens when the player does not exist — so
it will guess, confidently, in your user's face. Now the contract-quality
version:

```python
@mcp.tool()
def get_player_stats(name: str) -> str:
    """Look up one player's record in the game database.

    Args:
        name: the player's name, matched case-insensitively and exactly
            (no fuzzy matching).

    Returns the player's wins, losses, and ties, then their five most
    recent games (opponent, result, date), newest first.

    If no player has that name, returns "No player named <name>." --
    it does not raise, and it does not guess at near-matches.
    """
```

Every sentence is there because the model acts differently with it than
without it: the matching rule stops it from apologizing for case mismatches;
the return shape lets it promise the user what is coming; the unknown-player
clause turns a stack trace into a sentence it can relay — **error behavior is
part of the contract**, and "what happens on bad input" is a clause here for
exactly the reason it was a clause in your SPEC.md in week 4. You have been
writing this document all semester; it just moved into a docstring.

In class, the demo makes the authority of this text visible the fun way: we
edit one sentence of a working tool's docstring to lie about the return
meaning, restart, and watch the model misuse the result *exactly as
documented*. The model did not get worse; the contract did.

## Tool design: narrow beats mighty

The tempting Stage E design is one tool: `run_sql(query)`. Look how capable!
It is also wrong, for reasons worth having ready in week 12 when you evaluate
other people's servers:

- **A narrow tool is a contract; a raw-SQL tool is a capability dump.** You
  can state, test, and keep the promises of `get_leaderboard()`. You cannot
  state what `run_sql` returns — its behavior is your schema, and now your
  schema is a public interface you can never refactor.
- **The blast radius is the tool's, not the model's.** Whatever the model is
  talked into — by a user, or by injected text it read somewhere (L24's whole
  subject) — it can only do what your tools can do. `get_leaderboard` can leak
  a leaderboard. `run_sql` can drop it. Design the tool as if the caller is
  clever, literal-minded, and occasionally fooled — because it is.
- **Narrow tools compose forward.** "Who's improved most this month?" — the
  model chains stats calls and reasons over them. The mighty tool tempts you
  to answer every question by exposing more power instead of more contract.

Stage E's two tools are two flavors on purpose: `get_leaderboard()` takes
nothing and summarizes; `get_player_stats(name)` takes an argument and must
handle its failure case. Between them you will touch every design decision
above once. (Discussion question 2 asks what changes for a *write* tool —
have an answer; Project 2's agents will use write tools against your team's
issue queue, and the contract stakes go up a level.)

## Registration, and proof

Registering the server tells the host how to launch it (`claude mcp add`, or
the project's `.mcp.json` — the current syntax is in the docs and in the
example's README; verify against the docs, the tooling moves). After
registration, the host lists your tools like any others, and the model can
call them.

Stage E's required proof is a short transcript of Claude answering a real
question — "who's on top of the leaderboard, and what's their record?" — *via
your tools*: the tool calls visible, the answer grounded in your seeded Stage
B data. And the install must survive a stranger's machine: `README-mcp.md`
documents install and registration from a fresh clone (pin your `mcp` package
version — the README's pin is part of working-from-fresh-clone). Fresh-clone
gate, tool edition; third time this course; it will not be the last.

## Stage E, and the end of the unit

From the brief: the two tools over your real Stage B database,
contract-quality docstrings, registration + transcript, README-mcp.md,
and one honest BACKLOG.md entry — what this server should grow next, and why
it doesn't yet. The stretch, for the ambitious: `search_pkb(query)` over your
Project 0 bundle — your own knowledge base becomes a tool your agent can
consult, which is the course's whole thesis eating its own tail.

Then: **everything — Stages A through E and the half-page five-principles
retrospective — is due at the start of week 8.** Lecture 15 opens the team
unit by holding a retrospective on what you just built. Come having re-read
your own git history; it is the record of five weeks of your own process, and
next unit we start reading process records the way engineers do.

## Questions to think about

1. Trace one Stage E tool call through the Exercise 4 vocabulary: user turn,
   model, `tool_use` block, *which process executes your Python*, 
   `tool_result`, final answer. Where exactly does MCP sit in that chain, and
   which parts are unchanged from your toy agent?
2. Design `record_game(x_player, o_player, winner)` — a write tool. What new
   clauses does its docstring owe that the read tools didn't? (Idempotency?
   Validation? What does the *model* do differently knowing a tool mutates?)
   Would you ship it at all, and what would have to be true first?
3. Your `search_pkb` stretch: should it return whole notes, or names plus
   first lines? Argue from the model's context window and from Lecture 06's
   economics — then notice which of your two Stage E tools made the same
   choice.
