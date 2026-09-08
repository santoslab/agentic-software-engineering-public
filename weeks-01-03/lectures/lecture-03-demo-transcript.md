# Lecture 03 — Recorded Demo Transcript (annotated)

A real Claude Code session, recorded during rehearsal on **2026-08-31**, covering the
same ground as Demo 1 (`/init`) and Demo 2 (plan mode) run back to back in one
session. It replaces the screen recording: everything here is text, so it can be
projected, read aloud, pasted into a slide, or handed out.

**Use it two ways.** As the fallback if the live demos fail — the beats are all here.
Or as primary material, because this run produced a better teaching example than a
scripted demo would have: the agent made a mistake, was corrected, made *the same
class of mistake inside the correction*, and only stopped when told to actually run
the commands it was writing.

## Provenance

| | |
|---|---|
| Model | Sonnet 5 (what students on Pro will be running) |
| Repo | [`tictactoe-starter.tar.gz`](https://ase.santoslab.org/tictactoe-starter.tar.gz) — the handout. Clean, no CLAUDE.md at the start. |
| Permission mode | `default` — every write was gated, nothing auto-accepted. Confusingly, this one mode has two spellings: `"defaultMode": "default"` in `~/.claude/settings.json`, but `--permission-mode manual` on the CLI. (`manual` is accepted as an alias in settings; `default` is not a valid CLI value.) |
| Test runner | `uv run --with pytest pytest`. Bare `pytest` was **not installed on the demo machine** — see the caveat below |
| Outcome | 96 tests pass, 100% coverage, 6 new tests (90 before) |

> **Reproducing this yourself:** extract [`tictactoe-starter.tar.gz`](https://ase.santoslab.org/tictactoe-starter.tar.gz) and run the same
> prompts. Your results will differ, and the differences are the point. In particular,
> **if you already have `pytest` installed globally, you will not see the central
> failure in this transcript** — the agent prescribes bare `pytest`, which simply works
> on your machine and fails on the demo machine. The agent didn't check either way.
> That is the lesson, not the specific command.
>
> `git diff` shows what the agent changed; `git reset --hard && git clean -fd` puts you
> back to the start for another run.

### Establish the baseline first: 90 tests

**Before you run `/init` or any prompt, run the test suite and confirm you get
`90 passed`.** That is the state of a clean extract, and it is the number every later
claim is measured against — the transcript ends at 96 because the agent added 6.

If you do not see 90, stop and fix your environment before going further. Otherwise
you will spend the exercise unable to tell "the agent broke something" apart from "my
Python setup was never working," and those two look identical from the inside.

**Both paths verified against this tarball, 90 passed:**

```
# with uv (what the demo machine used)
uv run --with pytest pytest

# without uv — plain Python, nothing extra to install
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest
```

Neither dirties `git status`: `__pycache__/` is in `.gitignore`, and `.pytest_cache/`
and `.venv/` each write their own self-ignoring `.gitignore`.

> **If you use the venv path, notice what just happened to the lesson.** The CLAUDE.md
> in this transcript prescribes `pip install -r requirements-dev.txt` and then `pytest`
> — and for you, inside an activated venv, **that is correct**. It was wrong on the demo
> machine and right on yours, and the agent had no idea which it was writing for. The
> failure was never "it doesn't know pytest." It's that it produced the conventional
> answer for a generic Python repo without checking the one environment it was actually
> sitting in. Ask yourself what else in a generated CLAUDE.md is conventional rather
> than checked.

Paths are rewritten relative to the repo root. The transcript omits tool *results*
(file contents, test output) and keeps prompts, replies, and tool calls.

---

## Phase 1 — `/init` (Demo 1)

`/init` expands into a long built-in prompt asking the agent to analyse the codebase
and write CLAUDE.md. It then ran **13 tool calls**: a `find`, six `Read`s of the
source and config files, a hunt for README/Cursor/Copilot rules, four `Read`s of the
test files, and a `git log` / `grep` sweep for a SPECS file.

```
[CLAUDE] No README, no CLAUDE.md, no cursor/copilot rules. Let me check the test
         files to understand conventions used.
[CLAUDE] No SPECS file exists in the repo — it's just a reference comment in a test,
         not a real doc. I have everything needed now to write CLAUDE.md.
[TOOL]   Write: CLAUDE.md
```

The file it produced was good — though "good" turns out to be contested, and Phase 2
returns to that. It caught the twist the repo's name hides:

> A terminal-based Tic-Tac-Toe game, but on a **9x9 board where 5-in-a-row wins**
> (not the classic 3x3/3-in-a-row game).

It documented the 1-indexed public API against the 0-indexed internal board, the
`on_turn` callback that lets one game loop serve both 1P and 2P modes, and the
tie-detection test's `(r + 2*c) % 5` colouring — with a warning to read that
function's docstring before changing it.

> **Commentary — the question to ask the room.** "What could `/init` never have
> written?" With a weak output that question is cheap. This output is strong, which
> makes the honest answer the interesting one: it missed nothing *derivable*. It
> cannot know why the board is 9x9, that `blocking_move` is about to be added, or
> what any of this is for. Intent is not in the code. That is what the human-authored
> half of a CLAUDE.md is for.

> **Commentary — the planted error, which was not planted.** Every command in the
> Commands section was wrong for this machine: `pip install -r requirements-dev.txt`,
> `pytest`, `pytest tests/test_game.py`, `coverage run -m pytest`. Bare `pytest` was
> not installed **on the demo machine** — it may well work on yours, which is the
> whole point. The agent read `requirements-dev.txt`, saw the word `pytest`,
> and wrote confident instructions it never executed. Nothing in the exercise was
> rigged; this is simply what happened, twice, on two separate `/init` runs.

---

## Phase 2 — the feature request, in plan mode (Demo 2)

```
[USER]  In computer_ai.py, add a blocking_move(game) method beside random_move. If
        the opponent has a move that would immediately win, return it to block;
        otherwise fall back to a random available move. Follow random_move's existing
        signature and its use of game.available_moves().

[TOOL]  Write: ~/.claude/plans/in-computer-ai-py-add-a-memoized-muffin.md
[TOOL]  ExitPlanMode
```

> **Commentary — the single most quotable number in this transcript: zero.** Zero
> exploration tool calls between the prompt and the plan. It read nothing, because
> CLAUDE.md already told it everything: the board representation, the side effect in
> `check_winner()`, the 1-indexed convention. An earlier rehearsal ran the *identical
> prompt* in the same repo **without** a CLAUDE.md and needed eight tool calls — four
> file reads, three shell commands, and a spawned subagent — to reach the same starting
> point. That run is in
> [`lecture-03-demo-transcript-comparison.md`](lecture-03-demo-transcript-comparison.md)
> if you want to show it. That is Demo 1's thesis proved by Demo 2, on the clock, with
> no rhetoric required.

### An argument worth having: should that content have been in the file at all?

Both major vendors publish guidance that points the other way.

- **Anthropic**, [*The new rules of context engineering for Claude 5 generation
  models*](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models),
  states it outright: *"Avoid stating 'the obvious' things Claude should know by looking
  at your file system or your repo,"* and *"Keep your CLAUDE.md lightweight ... spend
  most of the tokens on gotchas inside of the codebase."* The
  [Claude Code best-practices docs](https://code.claude.com/docs/en/best-practices)
  carry an explicit exclude row for "anything Claude can figure out by reading code"
  and another for "file-by-file descriptions of the codebase" — and note that
  `/doctor` "proposes cuts for content it can derive from the codebase."
- **OpenAI**, [*Codex best practices*](https://learn.chatgpt.com/guides/best-practices),
  never states the derivability rule for `AGENTS.md`. Its discipline is *earned rules*:
  *"Keep it practical. A short, accurate `AGENTS.md` is more useful than a long file
  full of vague rules,"* and *"Start with the basics, then add new rules only after you
  notice repeated mistakes."*

Different reasoning, opposite directions, same destination: short file, non-obvious
content. That convergence is worth more than either doc alone — it suggests a property
of how these systems work rather than one vendor's house style.

By that standard most of what `/init` wrote here — the module split, the coordinate
convention, the testing conventions — should be cut. And that content is exactly what
produced the zero above. Measured across the two runs, prompt to plan:

| | no CLAUDE.md | CLAUDE.md present |
|---|---|---|
| model calls | 16 | 2 |
| context traffic (tokens) | 762,798 | 131,172 |

Cut the "obvious" half and this run becomes the other one.

**Both can be true, and the reconciliation is the lesson.** It is a break-even, not a
rule. Carrying costs the file's size in *every* session, including the ones that never
touch that subsystem. Rediscovering costs an exploration in *only* the sessions that
need it. Here — roughly a thousand tokens carried against ~630,000 in extra traffic —
carrying wins by orders of magnitude. On a monorepo with a 50,000-token architecture
document that any given task needs 2% of, it flips hard. One of those vendor posts is
titled *"how Claude Code works in large codebases."* The advice is right for the regime
it was written for, and this repo is not that regime.

**And the trade has a second side.** The same derived content that saved 630,000 tokens
also carried a false claim — the `pytest` commands in Phase 1 — which the agent then
trusted and repeated into its plan. A summary is an interpretation, and it inherits its
author's errors; source code does not. Cheap and risky, both measured in one session.

*Caveats, so you can attack this properly: n=1, one small repo, one task, and the
guidance targets a cost that accrues over hundreds of sessions rather than one. Run it
yourself on the handout and see whether the numbers hold.*

Plans are written to `~/.claude/plans/<slug>.md` automatically — the plan is a file,
not something that scrolls away. The plan contained the full implementation, a
justification for reusing `check_winner()` rather than reimplementing the win scan
("could drift out of sync"), and five specific test cases, including this one:

> When multiple opponent-winning cells exist, just assert the returned move is *one*
> of them (don't over-specify which, since the implementation returns the first found
> in `available_moves()` order — that ordering isn't a contract worth locking in).

---

## Phase 3 — push-back, and the mistake inside the fix

The plan's Verification section prescribed bare `pytest` — the same error as
CLAUDE.md. Rejecting a plan sends feedback rather than approving it:

```
[USER REJECTS + STEERS] The verification steps won't work here — bare pytest isn't
        installed on this machine. Use uv run --with pytest pytest instead. Also: the
        CLAUDE.md you generated earlier in this session prescribes the same broken
        command — note that in the plan.

[TOOL]  Edit: ~/.claude/plans/...
[TOOL]  ExitPlanMode
```

It fixed the two pytest lines correctly and added a task to fix CLAUDE.md. It also
rewrote the coverage line as:

```
uv run --with pytest coverage run -m pytest && uv run --with pytest coverage report
```

> **Commentary — read this one slowly.** That command fails:
> `error: Failed to spawn: coverage`. `--with pytest` installs *pytest*; `coverage` is
> a separate distribution and was never there. Asked to fix a command it had never
> run, the agent pattern-substituted the prefix it had just been handed onto a
> different command — and produced **a fresh instance of the exact bug it was
> correcting**, in the same edit where it correctly diagnosed the original. The
> failure mode isn't ignorance. It's that writing a command and running one are
> different acts, and only one of them checks anything.

```
[USER REJECTS + STEERS] The coverage command still won't work — --with pytest doesn't
        provide coverage. It needs uv run --with pytest --with coverage coverage run
        -m pytest && uv run --with coverage coverage report. Please verify each
        command actually runs before putting it in the plan.

[TOOL]  Bash: uv run --with pytest --with coverage coverage run -m pytest
[TOOL]  Bash: uv run --with coverage coverage report
[CLAUDE] Both commands verified working. Also confirming the plain test commands
         still work as written.
[TOOL]  Bash: uv run --with pytest pytest tests/test_computer_ai.py -v && ...
[CLAUDE] All four commands confirmed working. Updating the plan with the verified forms.
```

The rewritten plan now opens its Verification section with:

> The commands below were each actually run against the current (pre-change) codebase
> this session to confirm they work

> **Commentary — the whole lesson in one sentence.** One instruction — *verify each
> command actually runs* — moved it from prescribing to verifying, and it
> self-corrected on the first try afterwards. The arc is: **prescribe →
> correct-by-pattern → verify-by-running.** Steps 1 and 2 are what an agent does with
> plausible-sounding text. Step 3 is what it does when told the difference matters.

---

## Phase 4 — memory (a forward reference to L06)

```
[CLAUDE] No existing memory. I'll create two entries: a project memory about the
         environment (no bare pytest, use `uv run --with`) and a feedback memory about
         verifying commands before writing them into plans/docs.
```

It wrote its own lesson down, unprompted, quoting the instruction verbatim:

> Guessing a plausible-looking fix without executing it produced a second wrong answer.

> **Commentary — one sentence, then move on.** Memory is a week-six topic. Acknowledge
> it ("that's memory — we cover it properly later") and keep going. Two details worth
> knowing: these files live under `~/.claude/projects/<project>/memory/`, so wiping a
> project's directory deletes them; and the memory that says *verify before you write*
> contains an unverified claim — it describes the failure as "silently-ish
> (ImportError)" when the actual error was a loud `Failed to spawn: coverage`. Even
> the lesson learned was written from inference.

---

## Phase 5 — execution, interrupted

```
[USER APPROVES PLAN]
[CLAUDE] Plan approved. Implementing now.
[TOOL]   Edit: computer_ai.py
[CLAUDE] Now adding the test section for `blocking_move`.
[USER]   [Request interrupted by user]
[USER]   Rename it to find_blocking_move. It returns a candidate move rather than
         performing one — your own plan says the caller applies it via
         game.make_move(*move) — so the verb-less name reads like it acts on the board
         when it doesn't.
[TOOL]   Edit: computer_ai.py
[CLAUDE] Renamed to `find_blocking_move`. Now adding the tests, mirroring
         `random_move`'s test style.
```

> **Commentary — plan-to-code fidelity.** The method that landed on disk is
> character-for-character the code block in the approved plan. Approving a plan is a
> real review gate, not a gesture — what you read is what you get. Contrast the
> unplanned run of the same prompt, which duplicated
> `random.choice(game.available_moves())` inline instead of calling the method three
> lines above it, despite the prompt explicitly saying to follow `random_move`'s
> pattern.

> **Commentary — interrupt timing.** This interrupt landed before any test referenced
> the old name, so the rename touched exactly one line and left no debris. A few
> seconds later it would have had six test functions to chase. Worth saying out loud:
> interrupting is cheap early and expensive late, which is an argument for reading the
> plan rather than the diff.

---

## Phase 6 — verification

```
[CLAUDE] All 9 pass. Now the full suite and coverage.
[CLAUDE] All 96 tests pass with 100% coverage, including full branch coverage on the
         new `find_blocking_move` method.
```

Six new tests, all five planned cases plus an unplanned sixth
(`blocks_for_correct_opponent_symbol`). It also updated CLAUDE.md's architecture entry
for `computer_ai.py`, which had described `random_move` as "the only AI strategy" —
a stale claim in prose it had written itself an hour earlier, in a section nobody
pointed at.

---

## Mapping to the lecture blocks

| Block | Use |
|---|---|
| 15–30, Demo 1 | Phases 1 — the CLAUDE.md, and "what could it never have written?" |
| 30–45, Demo 2 | Phases 2, 3, 5 — zero-exploration, the plan, push-back, the interrupt |
| 52–63, failure demo | Phase 3 is a stronger, real version of the vague-prompt beat |
| 63–70, deferred features | Phase 4 (memory) and the subagent spawn from the no-CLAUDE.md run |

## Discussion prompts this transcript earns

1. The agent wrote install and test commands it never ran — twice, then a third time
   inside the fix. What class of claim can an agent make safely without executing
   anything, and what class can't it?
2. Is "the tests do it" a valid justification for production code reaching past a
   public API? An earlier version of this plan argued exactly that.
3. The plan was corrected twice before approval and the implementation then matched it
   exactly. Where did the review actually happen — at the plan, or at the diff?

## A note on reading the raw transcript

The two push-backs are not stored as user messages. They are recorded as *tool
rejections* — `"The user doesn't want to proceed with this tool use... the user said:
<text>"` — attached to the `ExitPlanMode` call they rejected. A naive read of the
JSONL shows the plan being edited with no visible cause. Worth knowing before anyone
tries to reconstruct a session from its transcript.

---

## Appendix — full session flow, unannotated

Every prompt, reply, and tool call in order. Tool *results* are omitted.
The `/init` built-in prompt is truncated to its first lines.

```
[USER] <command-message>init</command-message>
<command-name>/init</command-name>

[USER] (/init built-in prompt: "Please analyze this codebase and create a CLAUDE.md file... commands... architecture..." — truncated)


```

[TOOL] Bash: find . -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' | sort

[TOOL] Read: main.py

[TOOL] Read: game.py

[TOOL] Read: computer_ai.py

[TOOL] Read: pytest.ini

[TOOL] Read: .coveragerc

[TOOL] Read: requirements-dev.txt

[TOOL] Bash: ls -la tictactoe-starter; find tictactoe-starter -iname "README*" -o -iname "CLAUDE.md" -o -iname ".cursorrule

[CLAUDE] No README, no CLAUDE.md, no cursor/copilot rules. Let me check the test files to understand conventions used.

[TOOL] Read: tests/conftest.py

[TOOL] Read: tests/test_game.py

[TOOL] Read: tests/test_computer_ai.py

[TOOL] Read: tests/test_main.py

[TOOL] Bash: cat .gitignore && git log --all --oneline && grep -ri "SPECS" -r . --include="*.py" --include="*.md" -l 2>/dev

[CLAUDE] No SPECS file exists in the repo — it's just a reference comment in a test, not a real doc. I have everything needed now to write CLAUDE.md.

[TOOL] Write: CLAUDE.md

[CLAUDE] Created `CLAUDE.md`. This was a fresh repo with no prior `CLAUDE.md`, README, or Cursor/Copilot rules to merge in, so it's built entirely from reading the three source modules (`game.py`, `computer_ai.py`, `main.py`) and the test suite. Key points captured: the 9x9/5-in-a-row twist on Tic-Tac-Toe, the module split and 1-indexed vs 0-indexed board convention, the `on_turn` callback pattern that unifies 1P/2P loops, and the test-suite's monkeypatch/capsys conventions plus the tie-pattern math worth preserving.

[USER] In computer_ai.py, add a blocking_move(game) method beside random_move. If the opponent has a move that would immediately win, return it to block; otherwise fall back to a random available move. Follow random_move's existing signature and its use of game.available_moves().

[TOOL] Write: ~/.claude/plans/in-computer-ai-py-add-a-memoized-muffin.md

[TOOL] ToolSearch

[TOOL] ExitPlanMode

[USER REJECTS + STEERS] The verification steps won't work here — bare pytest isn't installed on this machine. Use uv run --with pytest pytest instead. Also: the CLAUDE.md you generated earlier in this session prescribes the same broken command — note that in the plan.

Note: The user's next message may contain a correction or preference. Pay close attention — if they explain what went wrong or how they'd prefer you to work, consider saving that to memory for future sessions.

[TOOL] Edit: ~/.claude/plans/in-computer-ai-py-add-a-memoized-muffin.md

[TOOL] ExitPlanMode

[USER REJECTS + STEERS] The coverage command still won't work — --with pytest doesn't provide coverage. It needs uv run --with pytest --with coverage coverage run -m pytest && uv run --with coverage coverage report. Please verify each command actually runs before putting it in the plan.

Note: The user's next message may contain a correction or preference. Pay close attention — if they explain what went wrong or how they'd prefer you to work, consider saving that to memory for future sessions.

[TOOL] Bash: uv run --with pytest --with coverage coverage run -m pytest 2>&1 | tail -20

[TOOL] Bash: uv run --with coverage coverage report 2>&1 | tail -20

[CLAUDE] Both commands verified working. Also confirming the plain test commands still work as written.

[TOOL] Bash: uv run --with pytest pytest tests/test_computer_ai.py -v 2>&1 | tail -10 && uv run --with pytest pytest -q 2>&

[CLAUDE] All four commands confirmed working. Updating the plan with the verified forms.

[TOOL] Edit: ~/.claude/plans/in-computer-ai-py-add-a-memoized-muffin.md

[TOOL] Bash: ls ~/.claude/projects/-Users-robby-Repositories-Courses-tictactoe-starter/memory/ 2>&1; cat ~/.claude/projects

[CLAUDE] No existing memory. I'll create two entries: a project memory about the environment (no bare pytest, use `uv run --with`) and a feedback memory about verifying commands before writing them into plans/docs.

[TOOL] Write: ~/.claude/projects/-Users-robby-Repositories-Courses-tictactoe-starter/memory/env_no_bare_pytest.md

[TOOL] Write: ~/.claude/projects/-Users-robby-Repositories-Courses-tictactoe-starter/memory/verify_commands_before_writing.m

[TOOL] Write: ~/.claude/projects/-Users-robby-Repositories-Courses-tictactoe-starter/memory/MEMORY.md

[CLAUDE] Saved two memories for this project: the `uv run --with pytest`/`--with coverage` requirement (`env_no_bare_pytest.md`), and a general rule to actually run commands before writing them into plans or docs (`verify_commands_before_writing.md`).

Now re-requesting plan approval.

[TOOL] ExitPlanMode

[USER APPROVES PLAN]

[CLAUDE] Plan approved. Implementing now.

[TOOL] Read: computer_ai.py

[TOOL] Read: tests/test_computer_ai.py

[TOOL] Read: CLAUDE.md

[CLAUDE] Now implementing the `blocking_move` method.

[TOOL] Edit: computer_ai.py

[CLAUDE] Now adding the test section for `blocking_move`.

[USER] [Request interrupted by user]

[USER] Rename it to find_blocking_move. It returns a candidate move rather than performing one — your own plan says the caller applies it via game.make_move(*move) — so the verb-less name reads like it acts on the board when it doesn't.

[TOOL] Edit: computer_ai.py

[CLAUDE] Renamed to `find_blocking_move`. Now adding the tests, mirroring `random_move`'s test style.

[TOOL] Read: tests/test_computer_ai.py

[TOOL] Edit: tests/test_computer_ai.py

[CLAUDE] Now updating CLAUDE.md's Commands section and the `computer_ai.py` architecture line, then running verification.

[TOOL] Edit: CLAUDE.md

[TOOL] Edit: CLAUDE.md

[CLAUDE] Now running the verified test commands.

[TOOL] Bash: uv run --with pytest pytest tests/test_computer_ai.py -v 2>&1 | tail -20

[CLAUDE] All 9 pass. Now the full suite and coverage.

[TOOL] Bash: uv run --with pytest pytest -q 2>&1 | tail -10

[TOOL] Bash: uv run --with pytest --with coverage coverage run -m pytest 2>&1 | tail -5 && uv run --with coverage coverage 

[CLAUDE] All 96 tests pass with 100% coverage, including full branch coverage on the new `find_blocking_move` method.

Summary:
- Added `ComputerAI.find_blocking_move(game)` in `computer_ai.py` — blocks the opponent's immediate 5-in-a-row win by simulating each candidate move via `game.check_winner()` (undoing board/winner state after each check), falling back to `random_move` when no threat exists.
- Added 6 tests in `tests/test_computer_ai.py` covering horizontal/diagonal blocks, correct opponent-symbol resolution, multiple-candidate blocks, the random fallback, and no observable side effects on `game`.
- Fixed `CLAUDE.md`'s Commands section and `computer_ai.py` architecture blurb, which prescribed bare `pytest`/`coverage` that don't work on this machine — now use the verified `uv run --with ...` forms.
- Saved two memories for this project: the `uv run --with pytest`/`--with coverage` requirement, and a reminder to actually run commands before writing them into plans or docs.

```
