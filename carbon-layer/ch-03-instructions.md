# Chapter 3 — Instructions: set behavior once, prepend it every turn

Chapter 2 gave the agent memory of the conversation, but nothing tells it *how to behave* across that conversation: every session starts with a blank personality, and any rule you want enforced has to be typed again by hand. This chapter adds the instructions primitive — a system prompt the harness assembles once and prepends to every model call — and layers a second, per-project source onto it: an `AGENTS.md` file auto-loaded from the working directory, the same convention used by Codex and Claude Code. It also quietly lands the `Workspace` class, a path-confined directory the agent will own for the rest of the book.

## The primitive

The instruction primitive is a persistent behavior setting. You state the rules once — "you are a concise coding assistant," "you are Gemma," "always run the tests" — and they hold on every subsequent turn without anyone repeating them.

The model cannot provide this on its own for the same reason it could not provide history: the chat API is stateless. There is no "settings" endpoint on a model; the only way behavior persists is if something re-sends it with every request. That something is the harness. Just as ch-02's harness owned the message list and replayed it each turn, ch-03's harness owns the instruction text and prepends it each turn. From the model's point of view nothing is remembered — it simply finds a `system` message at the head of every payload it receives.

The second layer makes the case for harness ownership even stronger. Real projects keep their rules in a file, and the model cannot read files at all (a lesson this stage sets up deliberately — see the end of the video section). Only the harness can open `AGENTS.md`, fold its contents into the system text, and do so freshly on every call. Instructions are therefore pure prompt-assembly work: the `model/` seam still just ships a list of messages, and the harness decides what that list contains.

## From the video

The walkthrough opens the chapter at [8:10](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=490s) by naming the residual problem from ch-02: the agent remembers the conversation now, "but it still behaves like a stranger every turn." A system prompt fixes that — one message, prepended by the harness on every turn. "You set it once and it sticks."

Then comes the project layer at [8:28](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=508s): real projects have a whole file of rules, so the harness auto-loads `AGENTS.md` from the working directory onto the system prompt — "the same convention as Codex and Claude Code." The author walks the code: one step in the agent folds two things into a single system message — the built-in prompt (`self.system`) and the `AGENTS.md` contents — while a loader in `instructions.py` reads the file and, if it's absent, does nothing. The framing at [9:01](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=541s) is the line to remember: "the instructions are a layer, not a replacement." The same segment notes that this chapter also lands a workspace — a directory the agent owns, every path confined to it — even though the write and edit tools that use it don't arrive until later chapters.

The demo puts an `AGENTS.md` saying "you are Gemma" in the agent's directory, and asking the name question now gets "Gemma" without any session setup. The chapter closes by naming its own limitation at [9:29](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=569s): "a path that we hand it is just a string of characters." Reading that file is what the next chapter, context delivery, will fix.

## The code

Six files change at this tag. The runtime additions divide into instruction assembly, a supporting
workspace abstraction, tests that isolate ambient files, and live checks.

### Agent construction and payload assembly

Start at [harness/agent.py](../stages/ch-03-instructions/harness/agent.py). The REPL's `main()` now
constructs `Agent(system=DEFAULT_SYSTEM)`, where
`DEFAULT_SYSTEM = "You are a concise, helpful coding assistant."` — and the constructor grows two
parameters: `system` (the built-in prompt, default `None`) and `agents_dir` (where `AGENTS.md` is
auto-loaded from, default `"."`).

| New interface | Inputs and defaults | Result or state change | Failure behavior |
|---|---|---|---|
| `Agent(..., system=None, agents_dir=".")` | Optional built-in text and a string path used for project instructions. | Stores both values; it does not read a file during construction. | Construction does not validate the directory. |
| `_system_text()` | No arguments; reads current object settings. | Returns non-empty instruction layers joined by a blank line, or `""`. | A missing file contributes `""`; read and decoding errors propagate. |
| `_payload()` | No arguments. | Returns a new list whose optional system head precedes references to the existing message dictionaries. | Propagates instruction-loading errors. It does not mutate `self.messages`. |
| `load_agents_md(directory=".")` | A string or `Path`. | Returns the complete `AGENTS.md` text, or `""` if no regular file exists. | Read and decoding failures propagate. |

Instruction assembly is implemented by two small private methods:

```python
    def _system_text(self) -> str:
        """The instruction layer = built-in system prompt + project AGENTS.md."""
        parts = [p for p in (self.system, load_agents_md(self.agents_dir)) if p]
        return "\n\n".join(parts)

    def _payload(self) -> list[dict]:
        """System prompt first (if any), then the full conversation history."""
        sys_text = self._system_text()
        head = [{"role": "system", "content": sys_text}] if sys_text else []
        return head + self.messages
```

`_system_text` joins the non-empty layers — built-in prompt first, project file second — and `_payload` puts the result at the head of the history as a single `system` message. The only change to `send` is one line: `chat` now receives `self._payload()` instead of `self.messages`. Everything from ch-02 (append the user turn, replay, append the reply) is untouched, and the call still goes through the `model/` seam, so no provider code changes.

The list comprehension keeps each `p` from the two-element tuple only when that string is truthy;
for strings, “truthy” means non-empty. `"\n\n".join(parts)` places a blank line between the retained
layers without leaving extra separators when one layer is absent.

Notice what is *not* stored: the system message never enters `self.messages`. History stays pure
conversation; the instruction head is reassembled at call time, every turn. Two properties fall
out of that. First, the head can never drift or get duplicated into the transcript. Second, because
`_system_text` runs on every `send`, `AGENTS.md` is re-read live — edit the file mid-session and the
very next turn sees the new rules.

### The instruction loader

The loader is the whole of the new [harness/instructions.py](../stages/ch-03-instructions/harness/instructions.py):

```python
def load_agents_md(directory: str | Path = ".") -> str:
    """Return ``<directory>/AGENTS.md`` contents, or '' if it doesn't exist."""
    path = Path(directory) / "AGENTS.md"
    return path.read_text() if path.is_file() else ""
```

No file → empty string → the `if p` filter in `_system_text` drops it → nothing changes. That is the
“layer, not a replacement” rule enforced in code: an absent project file leaves the built-in prompt
alone, and an absent built-in prompt leaves a lone `AGENTS.md` still working. The function tests
existence with `is_file()` before `read_text()`, but this is not a no-failure API: permissions can
change between those operations, and the default text decoder can reject non-text bytes.

### The supporting `Workspace` interface

The other new module is [harness/workspace.py](../stages/ch-03-instructions/harness/workspace.py), a
small path-confined wrapper around a directory with `write`, `read`, and `edit` methods. Its safety
core is `_safe`:

```python
    def _safe(self, path: str) -> Path:
        p = (self.root / path).resolve()
        if p != self.root and self.root not in p.parents:
            raise ValueError(f"path escapes workspace: {path}")
        return p
```

Every path is resolved and checked against the root before use, so a traversal like
`../../etc/passwd` raises instead of escaping — a boundary, enforced in the harness. By default the
root is a fresh temp dir (`tempfile.mkdtemp(prefix="workspace-")`), so an experiment cannot touch a
real project unless the caller supplies `root` deliberately.

| Method | Inputs | Success result and mutation | Failure behavior |
|---|---|---|---|
| `Workspace(root=None)` | Optional string or `Path`; `None` or an empty string creates a new temporary directory. | Stores an absolute, resolved root and creates it if necessary. | Directory creation errors propagate. |
| `write(path, content)` | Workspace-relative path and text. | Creates parent directories, replaces the file, returns `"wrote <path> (<N> chars)"`. | Escape raises `ValueError`; filesystem and encoding failures propagate. |
| `read(path)` | Workspace-relative path. | Returns the file text. | Escape raises `ValueError`; a missing file returns an `error:` string; other read failures propagate. |
| `edit(path, old, new)` | Path and exact text fragments. | Replaces only the first `old`, writes the result, returns `"edited <path>"`. | Missing file or absent `old` returns an `error:` string; escape raises `ValueError`; other file failures propagate. |

At ch-03 the class is used only by the checks and tests below; the file *tools* that let the model
drive it arrive in ch-05.

### Offline tests and pytest fixtures

The two gates evaluate different layers. `uv run verify` runs deterministic formatting, typing, import, and test checks offline. `uv run accept ch-03` uses the configured live model. [tasks/checks.py](../stages/ch-03-instructions/tasks/checks.py) registers two live behaviors: a system prompt constrains the answer to `BANANA`, and an automatically loaded project instruction supplies a separate required response.

```python
    ws = Workspace()
    ws.write("AGENTS.md", "You are Gemma, a coding assistant. When asked your name, reply 'Gemma'.")
    a = agent.Agent(system=agent.DEFAULT_SYSTEM, agents_dir=str(ws.root))
    reply = a.send("What is your name? Answer with just the name.")
    print("reply:", reply)
    return "gemma" in reply.lower()
```

The check stages the identity rule in a fresh `Workspace` and points `agents_dir` at it, so it controls exactly which `AGENTS.md` gets loaded. `_accept_ch03` ANDs both parts, so neither capability can silently regress.

On the deterministic side, the interesting change is [tests/conftest.py](../stages/ch-03-instructions/tests/conftest.py). This file existed as an empty placeholder since ch-01, waiting — its old docstring said so — for the chapter that gives the agent "something worth isolating between tests." That chapter is this one. The repo root has its own [AGENTS.md](../stages/ch-03-instructions/AGENTS.md) (the project's real working instructions — the two-gate rule, the package layout), so any test that constructs `Agent()` with the default `agents_dir="."` would silently absorb it — ambient state leaking into assertions. The fix is an autouse fixture:

```python
@pytest.fixture(autouse=True)
def isolate_cwd(tmp_path) -> Iterator[None]:
    """Run each test in a clean temp dir so no ambient AGENTS.md is auto-loaded."""
    prev = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield
    finally:
        os.chdir(prev)
```

`@pytest.fixture` registers a setup/cleanup function with pytest. `autouse=True` applies it to every
test without adding a fixture parameter, and `tmp_path` is pytest's own per-test temporary-directory
fixture. The annotation `Iterator[None]` describes a generator that yields one `None` value. Code
before `yield` is setup; pytest runs the test while the generator is suspended; code after `yield`
is teardown. `finally` guarantees that the previous cwd is restored even when the test assertion
fails. Without that restoration, one test could change how every later relative path resolves.

Every test now runs in a clean temp dir; instruction auto-loading sees nothing unless a test stages
a file itself. [tests/episodes/test_ch03.py](../stages/ch-03-instructions/tests/episodes/test_ch03.py)
then patches `chat` with a `_capture` helper that records the exact payload the harness sends — the
tests assert on what was *sent*, not on what a model says. `test_system_message_is_prepended` checks
the head is `{"role": "system", "content": "You are terse."}`; `test_no_system_by_default` checks a
bare `Agent()` sends no system message at all, so earlier chapters' payloads are byte-for-byte
unchanged; and the third test proves the layering:

```python
def test_agents_md_layers_onto_system():
    ws = Workspace()
    ws.write("AGENTS.md", "Project rule: be terse.")
    seen, fake = _capture()
    with patch.object(agent_mod, "chat", side_effect=fake):
        agent_mod.Agent(system="You are helpful.", agents_dir=str(ws.root)).send("hi")
    system_text = seen[0][0]["content"]
    assert "You are helpful." in system_text
    assert "Project rule: be terse." in system_text
```

### Instruction-assembly execution trace

For `Agent(system="You are helpful.", agents_dir=project).send("hi")`, where the project's
`AGENTS.md` contains `Project rule: be terse.`, the path is:

1. `send()` appends the user message to conversation history.
2. `_payload()` calls `_system_text()` before the model request.
3. `_system_text()` reads `AGENTS.md`, keeps both non-empty instruction sources, and joins the
   constructor-supplied text first and the project text second with a blank line.
4. `_payload()` creates a new system-role dictionary and places it before the conversation list;
   it does not insert that dictionary into `self.messages`.
5. `chat()` receives a two-message payload: the assembled system message followed by `hi`.

Because the file is read during each call, editing `AGENTS.md` between turns changes the next
payload without reconstructing the agent.

### Live acceptance evidence

The system-prompt half requires the live model to answer `BANANA`; the project-file half requires
it to answer `Gemma` from a freshly written `AGENTS.md`. These checks exercise instruction following
as well as assembly. They do not prove an absolute priority relationship when built-in and project
instructions conflict—the code establishes text order, while the model still interprets both.

## Design decisions & gotchas

**Layering order is a policy choice.** `_system_text` puts the built-in prompt first and `AGENTS.md` second, joined by a blank line. Project rules refine the base behavior rather than replace it, and a project file can always add to — but never delete — what the harness operator set. Compare the alternative of letting `AGENTS.md` *replace* the system prompt: then a project file could strip safety or formatting rules the operator intended to be permanent.

**Assembly at call time, not construction time.** Because the system head is rebuilt inside every `send`, instructions are live: editing `AGENTS.md` changes the next turn. The cost is one small file read per turn — a deliberate simplicity trade at this stage. It also means the head is recomputed identically each turn, which becomes valuable in ch-06 when context assembly needs a cache-stable prefix.

**Defaults are conservative.** `Agent()` with no arguments sends no system message — `DEFAULT_SYSTEM` is applied only by the REPL's `main()`, not by the constructor. That keeps the class neutral for embedding and keeps ch-01/ch-02 behavior (and their tests) exactly intact. The flip side is a subtle asymmetry: `agents_dir` *does* default to `"."`, so a bare `Agent()` run from a directory containing an `AGENTS.md` will pick it up. That is the feature working as designed — and precisely the ambient-state hazard `isolate_cwd` exists to contain in tests. The general lesson: auto-loaded instructions are ambient state, and any harness with them needs isolation in its test suite.

**Always-on files are trusted input.** Whatever sits in `AGENTS.md` becomes part of the system message on every call. The convention (shared with Codex and Claude Code) implicitly trusts the working directory; pointing an agent at an untrusted directory means letting that directory contribute to the system prompt. The repository uses the same convention for its own maintenance instructions. That real root file is why the test suite changes to an empty temporary directory before constructing an agent.

**The workspace lands before its tools — on purpose.** `Workspace` appears now so the accept check can stage an `AGENTS.md` behind a safe boundary, but the model has no way to invoke `write`/`read`/`edit` yet. Chapters stay scoped to one primitive: the tool interface is ch-05's job. Two details worth noticing anyway: `_safe` resolves paths (so `..` and symlink games are normalized before the containment check), and `edit` replaces only the first occurrence of `old` (`text.replace(old, new, 1)`) — a foreshadowing of the exact-match edit tools in real harnesses.

**Deliberately deferred.** The agent still cannot read files in conversation — hand it a path and it sees only a string of characters. File content injection is ch-04 (context delivery); acting on files is ch-05 (tools); the growing cost of an always-prepended head is ch-06 (context management); and a third instruction layer — procedures loaded on demand rather than always-on — is ch-07 (skills).

## Study pointers

Read the stage folder in this order:

1. [harness/agent.py](../stages/ch-03-instructions/harness/agent.py) — the constructor's two new parameters, then `_system_text` → `_payload` → `send`.
2. [harness/instructions.py](../stages/ch-03-instructions/harness/instructions.py) — the four-line loader and its docstring's "layer, not a replacement" rule.
3. [harness/workspace.py](../stages/ch-03-instructions/harness/workspace.py) — `_safe` first, then the three file methods.
4. [tests/conftest.py](../stages/ch-03-instructions/tests/conftest.py) and [tests/episodes/test_ch03.py](../stages/ch-03-instructions/tests/episodes/test_ch03.py) — cwd isolation, and the capture-the-payload testing pattern.
5. [tasks/checks.py](../stages/ch-03-instructions/tasks/checks.py) — the BANANA override check and the staged-`AGENTS.md` check.

Things to try (the demo and accept gate need LM Studio serving a local model, per [.env.example](../stages/ch-03-instructions/.env.example); `uv run verify` runs offline): run `uv run demo ch-03` and watch the same question answered with and without a staged `AGENTS.md`; then drop an `AGENTS.md` with one odd rule ("answer every question in a haiku") into a scratch directory, point `agents_dir` at it, and confirm it sticks across turns. As an exercise, flip the join order in `_system_text` and predict which test fails (none — then decide whether that test gap matters).

Previous: [ch-02 — history](ch-02-history.md) · Next: [ch-04 — context delivery](ch-04-context-delivery.md). This primitive is built on later by [ch-05 — tools](ch-05-tools.md) (the workspace gains its write/edit tools), [ch-06 — context management](ch-06-context-management.md) (the stable system head meets a finite window), and [ch-07 — skills](ch-07-skills.md) (instructions loaded on demand instead of always-on).
