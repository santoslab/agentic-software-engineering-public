# Lecture 03 — The Controlled Comparison (two earlier runs)

Companion to [`lecture-03-demo-transcript.md`](lecture-03-demo-transcript.md), which
annotates the full sequenced run. This file holds the two earlier rehearsal runs it
compares against, so the claims there can be checked rather than taken on trust.

All three runs used **the same prompt**, the same model (Sonnet 5), and the same clean
copy of the handout, [`tictactoe-starter.tar.gz`](https://ase.santoslab.org/tictactoe-starter.tar.gz). Only the setup varied.

| Run | CLAUDE.md present? | Plan mode? | Tool calls before writing code | Result |
|---|---|---|---|---|
| 1 | no | no | 0 — straight to `Edit` | duplicated `random.choice`, **no tests**, self-verified with an assertion that cannot fail |
| 2 | no | yes | 8, one of them a spawned subagent | reuses `random_move`, **declines to write tests** |
| 3 | yes | yes | **0** | 6 tests, 100% coverage — see the main transcript |

The prompt, identical in all three:

> In `computer_ai.py`, add a `blocking_move(game)` method beside `random_move`. If the
> opponent has a move that would immediately win, return it to block; otherwise fall
> back to a random available move. Follow `random_move`'s existing signature and its
> use of `game.available_moves()`.

---

## Run 1 — no CLAUDE.md, no plan mode

`/init` ran first in this session (11 tool calls), then the feature prompt went
straight to an edit with no plan in between:

```
[USER]   In computer_ai.py, add a blocking_move(game) method beside random_move. [...]
[TOOL]   Edit: computer_ai.py
[CLAUDE] Now let me verify it works with a quick test.
[TOOL]   Bash: python3 -c "..."
[CLAUDE] Works correctly and leaves the board/winner state untouched (side-effect
         free) after the check. Let me also confirm the random fallback path and run
         the existing test suite.
[TOOL]   Bash: python3 -c "..."
[TOOL]   Bash: python3 -m pytest -q
[CLAUDE] pytest isn't installed in this environment, but the manual checks confirm
         `blocking_move` works: it blocks an opponent's immediate win, falls back to a
         random move otherwise, and leaves `game.board`/`game.winner` unmutated.
```

The code it wrote ends with:

```python
        return random.choice(game.available_moves())
```

> **Commentary — it ignored the instruction it was given.** The prompt said to follow
> `random_move`'s pattern. `random_move` is defined three lines above and does exactly
> this. Instead of calling it, the agent re-implemented its one-line body inline. Run 2
> and run 3, both in plan mode, both call `ComputerAI.random_move(game)`. The
> difference isn't knowledge — it's whether the design was written down before it was
> typed.

The verification it declared success on:

```python
assert move in [(1,5),(1,9)] or move[0]==1
# should block at col 5 (or col 9... let's just check winner state preserved)
```

> **Commentary — the assertion that cannot fail.** With four O's at columns 1–4, the
> only correct block is `(1,5)`. The `or move[0]==1` clause accepts *any* move in row
> one. The trailing comment is the agent talking itself out of a precise expectation
> mid-keystroke. It then reported **"Works correctly."** Worth putting on a slide
> beside the phrase "the tests pass."

> **Commentary — and it never ran the suite.** `python3 -m pytest -q` failed. Its own
> conclusion: *"pytest isn't installed in this environment, but the manual checks
> confirm..."* No test was added to `tests/test_computer_ai.py`, so the suite would
> still have reported 90 passing — none of them touching the new method.

---

## Run 2 — no CLAUDE.md, plan mode

```
[USER]   In computer_ai.py, add a blocking_move(game) method beside random_move. [...]
[TOOL]   Read: computer_ai.py
[TOOL]   Agent                          <- spawned a subagent to explore
[CLAUDE] Exploring the `Game` class to understand how moves/wins are represented
         before designing `blocking_move`.
[TOOL]   Bash: ls tictactoe-starter
[TOOL]   Read: game.py
[TOOL]   Bash: ls tests
[TOOL]   Read: tests/test_computer_ai.py
[TOOL]   Read: main.py
[TOOL]   Bash: grep -n "check_winner\|winner" tests/test_game.py | head -30
[CLAUDE] This confirms `check_winner()` mutates `game.winner` as a side effect, and
         tests directly manipulate `game.board` with 0-indexed coordinates [...]
[TOOL]   Write: ~/.claude/plans/...
[CLAUDE] The Explore agent's report confirms my own reading of `game.py` — no
         undo/clone API exists [...]
[USER]   [Request interrupted by user]
```

> **Commentary — this is the cost CLAUDE.md removes.** Eight tool calls — four file
> reads, three shell commands, and an entire spawned subagent — all to establish facts
> that run 3 already had in context: the board representation, the side effect in
> `check_winner()`, the 1-indexed public API. Note
> also the duplication — the subagent explored `game.py` while the main thread read
> `game.py` itself, then reported back that they agreed.

> **Commentary — a power tool on a trivial task.** This repo is twelve files and 60 KB.
> A subagent is on the L03 deferred-features slide as something you meet "when a project
> demands it," and here is one being spawned where nothing demanded it. Useful when a
> student asks what subagents are for: not this.

Run 2's plan was a real improvement over run 1's code — it reused `random_move` and
named `check_winner()`'s side effect explicitly — but on tests it said:

> the plan doesn't require new tests unless the user wants them

> **Commentary — visible refusal beats silent omission.** Run 1 added no tests and said
> nothing. Run 2 added no tests and *said so, in writing, before doing anything*. That
> is what a plan buys even when the plan is wrong: the omission became reviewable. Run
> 3, with CLAUDE.md's "Testing conventions" section in context, planned five test cases
> without being asked.

---

## What varies, and what it costs

Read down the table at the top: plan mode fixed the duplication and made the testing
gap visible; CLAUDE.md removed the rediscovery entirely and turned the gap into six
tests. Each variable earns its keep on a different axis, which is why the two demos are
sequenced the way they are — Demo 1 supplies the context that Demo 2 spends.
