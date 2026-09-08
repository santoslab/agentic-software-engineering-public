# Chapter 0 — What is an agent? The frame and the two-gate scaffold

This is the opening chapter of both the book and the build. Tag `ch-00` ships no agent code. It states the repository's organizing equation — **Agent = Model + Harness + UI** — and introduces the machinery used to evaluate every later chapter: the public documentation, project configuration, and two verification gates. One naming note applies throughout the book: at these tags the project and package are named **gemma**, because the build runs against a local Gemma model served by LM Studio. The project was renamed **carbon** only in later commits on `main`, after `ch-14`. The source excerpts preserve the original name.

## The primitive

No module is added at this tag; the primitive is the frame itself, plus the discipline for proving every later primitive works.

The frame first. An agent is three layers. The **model** is a stateless reasoning engine behind one API call — it holds no memory, reads no files, runs no commands, and in this build it barely changes after the first chapter. The **UI** is just how a human reaches the agent, and it stays a minimal CLI until the final chapter. Everything that makes the system feel like an agent lives in the middle, in the **harness**: the loop, the instructions, the context assembly, the tools, the memory, the sandbox, orchestration, subagents, verification, and observability. Because the model is stateless and swappable, none of those capabilities *can* live in it — each one has to be engineered around the model, and that is why the harness is where the leverage is. It is also why two agents running the same model can behave completely differently. The README puts the diagnostic corollary bluntly: "When an agent 'gets dumb' mid-task, it is almost always a harness problem, not a model problem."

The repository demonstrates this progression with fifteen git tags, `ch-00` through `ch-14`. Each tag adds one main harness capability to the preceding implementation: model call, history, instructions, context delivery, tools, context management, skills, execution environment, durable state, orchestration, subagents, verification, observability, and finally a UI. Checking out a tag produces the runnable program at that stage. This book mirrors the sequence with one frozen snapshot under `stages/` per tag.

The second contribution is the **two-gate rule**, which defines the evidence required for later stages. `uv run verify` performs deterministic, offline checks: formatting, lint, static types, pytest, and smoke imports. `uv run accept ch-NN` runs the chapter's capability against a configured live model. The gates support different claims. Offline tests can identify harness regressions precisely and repeatably; live acceptance can detect mismatches between simulated responses and actual model behavior.

## From the video

The walkthrough opens with the whole series in one line: "An agent is a model plus a harness plus a UI" ([0:55](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=55s)). The model is "a stateless reasoning engine behind one API call," the UI "is just how a human reaches it," and everything that makes it feel like an agent lives in the middle — which is where the entire video is spent. The author is explicit that the agent is small on purpose: this is not the next Claude Code or Codex, but the least code that still teaches each idea, a few thousand lines across three little packages, built so "we actually understand what is going on."

The chapter-zero segment proper ([2:25](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=145s)) covers how the course ships: fifteen chapters, each adding exactly one primitive, distributed as one repository of git tags — check out any chapter and you get the exact runnable agent at that point. The whole thing runs on `uv`, with two ways to interact with a stage: `uv run demo` plays the chapter's scripted demo, and `uv run agent` drops into the live REPL. The diffs shown on the video's "what changed" slides are the real commit diffs for each tag, and the author's advice is exactly the method this book follows: pull up each tag and read every delta.

A few promises get made up front "because each one buys us something later": the model goes behind its own package, so adding a provider is just dropping in a file — a pattern the author notes is borrowed from how real coding agents are built; the UI lives in its own package, so the core never has to know about a screen's existence; and tracing rides on OpenTelemetry rather than a hand-rolled logger, so traces can later go to any OTel-compliant collector. The result is three packages where "the arrows only point one way" — UI to harness, harness to model ([4:43](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=283s)). Every chapter then follows one rhythm: build the primitive, break it to show why it is needed, fix it, and demo it against a real model. And because every chapter is a git tag, "the previous layer wasn't wrong, it just wasn't finished" ([5:01](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=301s)).

## The code

Fourteen files, 758 lines, and none of it is agent code. The commit message is candid about that:
the agent itself is born at ch-01, and the repo root carries no loop file. What ships is the
contract and the gates. This is still executable architecture: packaging determines which modules
can be imported, console-entry declarations determine which functions `uv run` invokes, and exit
codes determine whether automation proceeds.

### Documentation as the architectural contract

[README.md](../stages/ch-00-what-is-an-agent/README.md) is the longest file at the tag and functions
as the project's specification: the thesis, the audience, the chapter table for `ch-00`…`ch-14`,
and a primitive → module map that names the module that will own each primitive —
`model/provider.py` for the provider seam, `harness/tools.py` for tools, `ui/tui.py` for the UI —
files that mostly do not exist yet. Its layout section declares the package shape the next fourteen
chapters will fill in:

```
model/          # the provider seam + costing: provider / openai_compatible / fake / client / pricing
harness/        # the loop + every primitive: agent, context, tools, memory, skills, sandbox,
                #   orchestrator, subagents, verification, observability, events, ...
ui/             # the Textual TUI (the only package that imports textual/rich)
tasks/          # uv-run tooling: verify / accept / demo / tui
tests/episodes/ # one behavioral test file per chapter (test_ch01..test_ch14)
```

Three packages with one-way dependencies — `ui/` → `harness/` → `model/`; the core never imports the UI. At `ch-00`, only `tasks/` exists.

[AGENTS.md](../stages/ch-00-what-is-an-agent/AGENTS.md) restates the same contract as working instructions for anyone — human or coding agent — contributing to the repo. Its version of the two-gate rule is imperative: "`verify` is the floor, `accept` is the truth. Ship a change only when both are green. Never claim a chapter works without a green `accept`." [CLAUDE.md](../stages/ch-00-what-is-an-agent/CLAUDE.md) is a single line, `@AGENTS.md`, so Claude Code loads the same instructions. There is a pleasing recursion here: the repo that will teach instructions-as-a-primitive ships its own `AGENTS.md` from day one, and in ch-03 the agent under construction learns to auto-load exactly this kind of file.

### Packaging and command interfaces

[pyproject.toml](../stages/ch-00-what-is-an-agent/pyproject.toml) names the package and registers the
gate runners as `uv run` scripts:

```toml
[project]
name = "gemma"
version = "0.1.0"
description = "Build a custom agent harness from scratch, one primitive per chapter"
requires-python = ">=3.11"
dependencies = ["httpx>=0.27"]

[project.scripts]
verify = "tasks.verify:main"
accept = "tasks.accept:main"
demo = "tasks.demo:main"
```

The string to the left of each `=` is the command name. The value to the right uses
`module:function` notation, so `uv run verify` imports `tasks.verify` and calls its `main`
function. Each runner exposes `main(argv: list[str] | None = None) -> int`. `accept` and `demo` use
the supplied list for direct tests or command-line arguments when it is `None`; `verify` accepts
the same shape but has no meaningful arguments at this tag. Each returns a process status. The
bottom-of-file `raise SystemExit(main())` converts that integer into the shell exit code when the
module is run directly.

The only runtime dependency is `httpx`, waiting for the provider seam in ch-01; ruff, mypy, and
pytest sit in the dev group. The wheel contains only `tasks` at this tag. This means installing the
package exposes the three runners, but there is not yet a `harness` or `model` package to install.
[conftest.py](../stages/ch-00-what-is-an-agent/conftest.py) is two comment lines whose *presence* at
the repo root puts the root on `sys.path` for pytest, so later tests can `import harness.*` and
`import model.*` directly — the packages are top-level directories, not a `src/` layout.

The command interfaces and their failure behavior are:

| Command | Input | Success | Other outcomes |
|---|---|---|---|
| `verify` | No meaningful arguments at ch-00. | Returns 0 after every offline check succeeds. | Returns 1 with all failed check labels; it continues after an individual failure. |
| `accept ch-NN` | A chapter id read from `argv`. | Returns 0 when the registered function returns a truthy value. | Returns 1 for false or an exception; returns 2 for missing input or no registered check. |
| `demo ch-NN` | A chapter id read from `argv`. | Calls the registered demo and returns 0. | Returns 2 for missing input or no registered demo; a demo exception propagates. |

That last distinction matters: acceptance catches exceptions and converts them to a red verdict,
while the demo runner is presentation tooling and lets an exception show its traceback.

### Gate A: subprocess-based offline verification

[tasks/verify.py](../stages/ch-00-what-is-an-agent/tasks/verify.py) runs the offline checks in
sequence, collects failures rather than stopping at the first, and hits no network:

```python
    if _run(["ruff", "format", "--check", "."]) != 0:
        failed.append("ruff-format")
    if _run(["ruff", "check", "."]) != 0:
        failed.append("ruff-check")
    if _run(["mypy", "tasks"]) != 0:
        failed.append("mypy")

    rc = _run(["pytest"])
    if rc not in (0, 5):  # 5 = "no tests collected", expected in the earliest chapters
        failed.append("pytest")
```

`subprocess.call(cmd)` starts another program, waits for it, and returns its integer exit status.
It does not raise merely because the child returned nonzero, which is why `_run()` can collect all
four results. The `cmd` value is a list such as `["ruff", "check", "."]`; list form passes arguments
directly instead of asking a shell to parse one command string. That avoids shell quoting and
expansion at this boundary. Failure to *start* a command, such as a missing `ruff` executable, can
still raise an exception; ch-00 does not catch that case.

A smoke import of `tasks.checks` follows, then a single `VERIFY OK` / `VERIFY FAILED` verdict.
`importlib.import_module()` is an import performed from a string at runtime. It catches syntax,
missing-dependency, and import-time failures that the preceding static checks may not expose.

### Gate B: a live registry that starts empty

[tasks/checks.py](../stages/ch-00-what-is-an-agent/tasks/checks.py) is the seam every later chapter
plugs into:

```python
from collections.abc import Callable

ACCEPTANCE: dict[str, Callable[[], bool]] = {}
DEMOS: dict[str, Callable[[], None]] = {}
```

[tasks/accept.py](../stages/ch-00-what-is-an-agent/tasks/accept.py) looks the chapter up in `ACCEPTANCE`, and its exit codes are deliberately tri-state — 0 pass, 1 fail, 2 "no check registered":

```python
    check = ACCEPTANCE.get(chapter)
    if check is None:
        print(f"no live acceptance check registered for '{chapter}'")
        return 2

    model = os.environ.get("LLM_MODEL", "google/gemma-4-26b-a4b")
    base = os.environ.get("LLM_BASE_URL", "http://192.168.189.144:1234/v1")
    print(f"== live acceptance: {chapter}  (model={model} @ {base}) ==", flush=True)
    try:
        ok = bool(check())
    except Exception as exc:  # noqa: BLE001
        print(f"ACCEPT ERROR: {exc}")
        return 1
    print("\nACCEPT OK" if ok else "\nACCEPT FAILED")
    return 0 if ok else 1
```

[tasks/demo.py](../stages/ch-00-what-is-an-agent/tasks/demo.py) is the same lookup against `DEMOS`,
running a chapter's scripted, on-camera demonstration against a real model. `Callable[[], bool]`
means “a callable taking no arguments and returning a Boolean”; `Callable[[], None]` means a
no-argument callable used only for its effects. The registries separate lookup from execution:
later stages add entries without changing either runner.

### The opt-in Git hook

[.githooks/pre-commit](../stages/ch-00-what-is-an-agent/.githooks/pre-commit) runs `verify`
unconditionally, then reads the current chapter from a `.current-chapter` file and runs its live
acceptance, using the tri-state exit code to skip cleanly when no check exists yet:

```sh
CH=$(cat .current-chapter 2>/dev/null)
if [ -n "$CH" ]; then
  echo "[pre-commit] (B) live acceptance: uv run accept $CH"
  uv run accept "$CH"
  rc=$?
  if [ "$rc" -eq 2 ]; then
    echo "[pre-commit] no live check registered for $CH yet — skipping"
  elif [ "$rc" -ne 0 ]; then
    echo "[pre-commit] live acceptance failed for $CH — commit blocked"
    exit 1
  fi
fi
```

### Deferred runtime configuration

[.env.example](../stages/ch-00-what-is-an-agent/.env.example) defines the three variables the model
package will read — `LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY` — defaulting to a local LM Studio
server exposing an OpenAI-compatible API, with commented alternatives for OpenRouter or Ollama.
At this tag the file is only a declared interface; no ch-00 function reads it. And
[.gitignore](../stages/ch-00-what-is-an-agent/.gitignore) already reserves `.sessions/` and
`.agent_state/` as “durable state written by the agent in later chapters” — a forward declaration
of ch-09, not evidence that persistence exists yet.

### Verification execution trace

A representative `uv run verify` invocation follows this path:

1. The console-script entry calls `tasks.verify.main()`.
2. `main()` invokes the formatter check, linter, type checker, and pytest in sequence. Each command
   returns an integer process status; nonzero statuses add a label to `failed` rather than stopping
   the remaining checks.
3. The smoke-import block imports the task modules. An exception adds `"smoke"` to `failed`.
4. An empty `failed` list produces exit status 0; any recorded failure produces status 1.
5. When the pre-commit hook invokes the live gate for ch-00, `tasks.accept` finds no registered
   acceptance function and returns status 2. The hook treats 2 as “not applicable,” while status 1
   would block the commit. Later chapters populate the registry and make this second gate active.

## Design decisions & gotchas

- **Two gates, because two claims.** `verify` is fast, deterministic, and offline, so it can run on every commit; `accept` needs a live endpoint and a warm model, so it is a separate command with its own verdict. Splitting them keeps flaky live runs out of the fast loop while keeping "mocked green" out of the definition of done.
- **ch-00's own gates.** This chapter is theory, so it registers nothing in `ACCEPTANCE`; only the deterministic gate has work to perform. `uv run accept ch-00` returns exit code 2, which the pre-commit hook interprets as “not applicable” rather than failure. The three statuses let one hook distinguish success, failure, and the absence of a live check.
- **`pytest` exit 5 is tolerated.** With no `tests/` directory yet, pytest exits 5 ("no tests collected"), and `verify` accepts that. The subtle cost: a later misconfiguration of `testpaths` that collected zero tests would also pass silently. The episode tests arriving from ch-01 onward close that window in practice.
- **`sys.path.insert(0, os.getcwd())`** opens every runner because only `tasks/` is built into the wheel; the agent packages will be imported straight off the repo root. Consequence: run `uv run ...` from the root, not from a subdirectory.
- **The docs are a contract, not a description.** README documents `uv run agent` "(from ch-01 on)" and a module map full of files that do not exist yet. That is deliberate: the map fixes the shape of the build up front, and each chapter fills in one row.
- **"Nothing is mocked" has a precise meaning.** The map already promises a `fake` provider (`model/fake.py`) — a deterministic, offline provider *behind the same seam*, for the verify-level tests. The rule is about the gates: demos and acceptance always run against a live model configured via `.env`.
- **The hook is opt-in.** Git cannot ship enabled hooks, so the gate becomes mandatory only after `git config core.hooksPath .githooks` — noted in the hook's own header.
- **The default endpoint is the author's LAN.** `LLM_BASE_URL` points at `192.168.189.144:1234`; copy `.env.example` to `.env` and aim it at your own LM Studio (or any OpenAI-compatible endpoint) before expecting any live run to work.

## Study pointers

Read the [stage snapshot](../stages/ch-00-what-is-an-agent/) in this order:

1. [README.md](../stages/ch-00-what-is-an-agent/README.md) — the thesis, the chapter table, the primitive → module map, the layout.
2. [AGENTS.md](../stages/ch-00-what-is-an-agent/AGENTS.md) and [CLAUDE.md](../stages/ch-00-what-is-an-agent/CLAUDE.md) — the same contract as working rules.
3. [pyproject.toml](../stages/ch-00-what-is-an-agent/pyproject.toml) and [conftest.py](../stages/ch-00-what-is-an-agent/conftest.py) — the wiring.
4. [tasks/verify.py](../stages/ch-00-what-is-an-agent/tasks/verify.py), [tasks/checks.py](../stages/ch-00-what-is-an-agent/tasks/checks.py), [tasks/accept.py](../stages/ch-00-what-is-an-agent/tasks/accept.py), [tasks/demo.py](../stages/ch-00-what-is-an-agent/tasks/demo.py) — the two gates and their registry.
5. [.githooks/pre-commit](../stages/ch-00-what-is-an-agent/.githooks/pre-commit), [.env.example](../stages/ch-00-what-is-an-agent/.env.example), [.gitignore](../stages/ch-00-what-is-an-agent/.gitignore) — the enforcement and the environment seam.

Things to try: from the stage folder, `uv sync` then `uv run verify` — it is fully offline and should end in `VERIFY OK` (with pytest reporting no tests collected). Then `uv run accept ch-00` to see the tri-state registry answer "no live acceptance check registered." A one-time note for the whole book: from ch-01 onward, running a chapter's demo or acceptance requires a real model endpoint — by default LM Studio serving a local Gemma model, configured in `.env`.

Next chapter: [ch-01-model-only.md](ch-01-model-only.md), where the first real primitive lands — one model call behind a swappable provider seam — and the `ACCEPTANCE` and `DEMOS` registries get their first entries. This chapter has no predecessor. Later chapters that build directly on what was scaffolded here: [ch-03-instructions.md](ch-03-instructions.md) turns `AGENTS.md` from repo documentation into harness payload, [ch-12-verification.md](ch-12-verification.md) teaches the agent itself the same proof-over-trust discipline the gates encode, and [ch-14-ui.md](ch-14-ui.md) completes the three-package promise with the Textual TUI.
