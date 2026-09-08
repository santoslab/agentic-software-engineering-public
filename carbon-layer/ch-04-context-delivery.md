# Chapter 4 — Context delivery: the harness reads files into the prompt

By the end of chapter 3 the agent had memory and standing instructions, but it still lived entirely on typed text: the only facts it could reason about were the ones the user pasted into the prompt. A model cannot open a file — it has no filesystem, no I/O, nothing but the tokens it is handed. This chapter adds the first *context* primitive: when the user writes `@path` in a message, the harness reads that file off disk and injects its contents into the prompt before the model ever sees the question. The stage snapshot is [stages/ch-04-context-delivery](../stages/ch-04-context-delivery/), tagged `ch-04` upstream, and the walkthrough segment starts at [9:37](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=577s).

## The primitive

**Context delivery** is the harness noticing that the user referred to an external artifact, fetching that artifact, and placing its contents into the model's window. The mechanism here is deliberately minimal: a marker symbol (`@`), a scan of the user's text for `@path` references, a `read_text()` per readable file, and one injected message per file — all before the real turn is appended.

The capability this unlocks is qualitative, not incremental. Before this stage, "who is Raveena?" only works if someone already typed the trivia into the conversation. After it, `@facts.txt Who is Raveena?` works because the harness turned a nine-character reference into the file's full contents inside the prompt. The agent can now ground its answers in artifacts that were never typed.

This primitive belongs in the harness for two reasons. First, the model request contains text, not a capability to open paths on the caller's filesystem. If the client does not read the file and put its contents in a message, this request cannot use those contents. Second, the client must define a delivery policy: which marker syntax counts as a reference, how injected blocks are labeled, where they appear relative to the question, and how large they may be. The `@` syntax is a convention selected by this harness, just as chapter 3 selects `AGENTS.md` as an instruction source.

It is worth naming the direction of flow. This is *push* delivery: the user points, the harness fetches, the model receives. The model has no say in what gets loaded. Chapter 5 adds the complementary *pull* motion — tools that let the model ask for a file itself — and chapter 6 adds the discipline (caps, compaction) that both motions eventually require.

## From the video

The segment opens by stating the gap left after instructions: the agent obeys its system prompt now, but [9:38](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=578s) "it only ever sees the text we hand it." Reading a file and getting its contents in front of the model is, in the author's framing, exactly the kind of work the harness exists to do.

The design is presented as a choice, not a standard. The author picks `@` — "at the rate," as he calls the symbol — as the file marker, and immediately flags that the symbol is arbitrary: "it's our harness, we get to decide" ([9:57](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=597s)). Before each call the harness scans for `@path` references, reads the files off disk, and injects the contents *ahead of* the question. He is careful to keep the implementation in proportion: "In code, that's just one loop in send" ([10:12](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=612s)) — the loop over the blocks the `deliver` function returns. He also flags the deliberate roughness: "Notice the blocks are raw for now" — the whole file goes in, and capping a giant file so it doesn't flood the window is explicitly deferred to a later chapter ([10:18](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=618s)).

The on-camera demo ([10:31](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=631s)) is a `facts.txt` of movie trivia — "Raveena is Karishma and Karishma is Raveena" — referenced with `@facts.txt` and followed by "who is Raveena?"; the model answers "Karishma" because the entire file was added to its context. The segment closes on the seam to the next chapter: the agent can now *read* a file, but acting on one is where tools come in.

## The code

The diff from `ch-03` to `ch-04` touches four files: one new harness module, a small change to the
drive loop, a new episode test, and a new acceptance/demo pair.

### The `deliver()` interface

The new public helper has one deliberately narrow contract:

| Interface | Input | Return value | State and failure behavior |
|---|---|---|---|
| `deliver(user_text)` | A required string scanned left to right. | A list containing one labeled text block per readable matched file, in match order. | Does not mutate the input or agent. Missing paths, directories, and caught `OSError`s contribute no block; decoding errors are not caught. |

There is no parameter for a root directory, encoding, maximum count, or maximum size at this tag.
Relative paths resolve against the process cwd. Repeated references produce repeated blocks, and
the function reads the current file contents each time it is called.

### Integration into `Agent.send()`

Start at the entry point.

[harness/agent.py](../stages/ch-04-context-delivery/harness/agent.py) — `send` gains a pre-loop. In chapter 3 it appended the user turn and called `chat`; now it first asks `deliver` for context blocks and appends each one as its own message:

```python
    def send(self, user_text: str) -> str:
        """Inject any @path files, append the turn, replay, keep the reply."""
        for block in deliver(user_text):  # @file references → injected context
            self.messages.append({"role": "user", "content": f"Context file:\n{block}"})
        self.messages.append({"role": "user", "content": user_text})
        resp = chat(self._payload(), model=self.model, provider=self.provider)
        self.messages.append({"role": "assistant", "content": resp.content})
        return resp.content
```

The ordering is intentional: file contents enter history *before* the user's turn, so the request presents the reference material before the question that refers to it. Everything else from chapter 3 is unchanged: `_system_text` still joins the built-in prompt and `AGENTS.md`, `_payload` still places that text first, and the single model call still uses `chat()`. Apart from the `deliver` import, only the REPL banner changes.

### Path recognition and file loading

[harness/context.py](../stages/ch-04-context-delivery/harness/context.py) — the new module is
thirty-two lines, half of them docstring. The working core:

```python
_ATTACH = re.compile(r"@(\S+)")


def deliver(user_text: str) -> list[str]:
    """Return a context block for each readable ``@path`` referenced in the text."""
    blocks: list[str] = []
    for match in _ATTACH.finditer(user_text):
        path = Path(match.group(1))
        if path.is_file():
            try:
                body = path.read_text()
            except OSError:
                continue
            blocks.append(f"--- {path} ---\n{body}")
    return blocks
```

`re.compile(...)` creates a reusable **regular expression**, a small pattern language for matching
text. In `r"@(\S+)"`, the leading `r` makes a raw Python string so backslashes reach the regex
unchanged. `@` matches that literal character; `\S` means any non-whitespace character; `+` means
one or more; and parentheses create capture group 1. `finditer()` yields match objects from left to
right, and `match.group(1)` returns the captured path without the `@`. Consequently spaces cannot
appear in a referenced path, while punctuation remains part of it.

`Path(...)` creates a path object; it does not read the file. `is_file()` follows the path and
returns true only for an existing regular file. `read_text()` then opens, decodes, reads, and closes
the file. The `try`/`except OSError` handles operating-system failures such as a permission error or
a file disappearing between the two calls. `UnicodeDecodeError` is a subclass of `UnicodeError`,
not `OSError`, so binary or incorrectly encoded content can still terminate the turn at this tag.

`deliver` has no dependency on message roles or the model client. Each block is labeled with its
path (`--- {path} ---`), allowing the request to associate the retained `@` reference with the
injected text. Blocks are not size-limited until chapter 6.

### Offline payload tests

[tests/episodes/test_ch04.py](../stages/ch-04-context-delivery/tests/episodes/test_ch04.py) — the episode test patches `chat` at the agent module and captures the exact payload sent through the seam, so it proves injection without a network:

```python
def test_attached_file_is_injected(tmp_path):
    f = tmp_path / "notes.txt"
    f.write_text("SECRET=42")
    seen, fake = _capture()

    with patch.object(agent_mod, "chat", side_effect=fake):
        agent_mod.Agent().send(f"@{f} what is the secret?")

    payload_text = " ".join(m["content"] for m in seen[0])
    assert "SECRET=42" in payload_text
```

The second test checks the unchanged path: with no `@` reference, the captured payload is *exactly*
`[{"role": "user", "content": "just a plain question"}]`. No context block is added, and the
`isolate_cwd` fixture from chapter 3's
[tests/conftest.py](../stages/ch-04-context-delivery/tests/conftest.py) prevents an ambient
`AGENTS.md` from adding a system message. The tests do not cover multiple paths, punctuation,
unreadable files, binary files, or path confinement; those remain limits of this stage rather than
implied guarantees.

### Live acceptance evidence

[tasks/checks.py](../stages/ch-04-context-delivery/tasks/checks.py) — the second gate. The repo's rule is that every chapter is green on two gates: `uv run verify` (ruff, mypy, pytest, smoke import — deterministic and offline, which is where the mocked episode test runs) and `uv run accept ch-04`, which asserts the capability against a real model:

```python
def _accept_ch04() -> bool:
    """The real agent answers from a file it was handed via @path."""
    import tempfile
    from pathlib import Path

    from harness import agent

    d = Path(tempfile.mkdtemp())
    (d / "facts.txt").write_text("The launch code is GOGO-9.\n")
    a = agent.Agent(system="Answer using the provided context files.")
    reply = a.send(f"@{d / 'facts.txt'} What is the launch code? Reply with just the code.")
    print("model replied:", repr(reply))
    return "gogo-9" in reply.lower()
```

The check plants a fact the model cannot reasonably infer — a made-up launch code in a fresh temp
directory — so a correct constrained answer is evidence that the payload contained the file.
`_demo_ch04`, registered alongside it, reproduces the video's Raveena/Karishma demo. Both use
absolute temp paths, which matters because `deliver` resolves relative paths against the process's
working directory. The acceptance test does not inspect the payload directly; the episode test and
live response support complementary claims.

### Context-delivery execution trace

For a user message `@facts.txt What is the launch code?`:

1. `Agent.send()` passes the complete user string to `deliver()`.
2. The regular expression finds `facts.txt`; `Path.is_file()` rejects missing paths and
   directories. `read_text()` reads the file, and an `OSError` contributes no block.
3. `deliver()` reads the file and returns a labeled string containing its path and full text.
4. `send()` appends that string as a user-role `Context file:` message, then appends the user's
   original question as a separate user message.
5. `_payload()` adds any system instructions ahead of both messages and calls the model.

The original `@facts.txt` marker remains in the question. The preceding labeled block gives the
model the bytes to which that marker refers; the model itself never opens the path.

## Design decisions & gotchas

**`deliver` returns strings; the agent shapes messages.** The split between the two files is a deliberate seam. `context.py` does scanning and reading; `agent.py` decides that each block becomes a `user`-role message prefixed `Context file:`. The context module never learns the chat message schema, and the message-shaping policy stays in the one file that owns the loop.

**Injected context is permanent history.** The blocks are appended to `self.messages`, not to a per-call copy of the payload. That is a real choice with consequences: the file's contents survive into every later turn (ask a follow-up question without re-typing `@facts.txt` and it still works), re-referencing the same file injects a second copy, and the history holds a *snapshot* — if the file changes on disk afterward, the model keeps seeing the stale version. Chapter 6 is where accumulated history like this gets managed rather than merely accumulated.

**Raw and uncapped, on purpose.** `read_text()` slurps the whole file. A large file will blow past a local model's context window and degrade or break the call. The author flags this on camera and in the docstring rather than fixing it here — per-item clamping "at the door" is chapter 6's job (the README calls these door caps, in `harness/limits.py`). One primitive per chapter; don't smear it.

**Failures are silent.** A typo'd path fails `is_file()` and is skipped with no warning to the user or the model. The model then answers without the file — often by hallucinating confidently. The same goes for `@notes.txt,` with trailing punctuation: `\S+` greedily captures the comma, `notes.txt,` is not a file, nothing is injected. A production harness would surface "could not read X"; this one keeps the chapter's point uncluttered: the harness, not the model, opens the file.

**The loose regex is guarded by `is_file()`.** `@(\S+)` matches any `@`-prefixed run of non-space characters, including the tail of an email address mid-word. The reason this doesn't misfire constantly is that every candidate must pass `path.is_file()` before anything is read. The filesystem check, not the regex, is the real filter.

**No path scoping.** `deliver` will happily read `@/etc/passwd` or any absolute path the process can access — there is no workspace boundary on delivery, even though a `Workspace` class already exists in [harness/workspace.py](../stages/ch-04-context-delivery/harness/workspace.py). And whatever the file contains lands in the prompt as user-role content, so a file can carry instructions the model may follow — the classic prompt-injection surface every context-delivering harness inherits. Boundaries are built up in the tool and sandbox chapters; at this stage the trust model is simply "the user chose the file."

**Blocks ride the `user` role.** OpenAI-compatible chat endpoints offer no "context" role, so the harness labels its injections inside ordinary user messages. The instruction head from chapter 3 stays reserved for behavior; delivered artifacts are conversation, not policy.

**Text scanning is simpler than an explicit attachment API.** A typed call such as
`send(text, attachments=[Path(...)])` could support spaces, validate paths before constructing the
turn, and distinguish literal `@` text from files. The inline marker is convenient in a REPL and
requires no UI-specific object, but its loose grammar and silent failures become part of the user
interface. Chapter 14 can reuse it unchanged precisely because it is encoded in text.

## Study pointers

Read the stage in this order:

1. [harness/context.py](../stages/ch-04-context-delivery/harness/context.py) — the whole primitive, docstring first.
2. [harness/agent.py](../stages/ch-04-context-delivery/harness/agent.py) — where `deliver`'s blocks enter the loop, and what chapter 3 machinery is unchanged.
3. [tests/episodes/test_ch04.py](../stages/ch-04-context-delivery/tests/episodes/test_ch04.py) — how injection is proven offline through the patched seam.
4. [tasks/checks.py](../stages/ch-04-context-delivery/tasks/checks.py) — `_accept_ch04` and `_demo_ch04`, the live half of the two gates.

Things to try (the demo and `accept` need LM Studio serving a local model per [.env.example](../stages/ch-04-context-delivery/.env.example); `pytest` runs offline): run `uv run demo ch-04`, then in the REPL reference a file of your own and ask a follow-up *without* the `@` reference to see history permanence at work. Then trip the sharp edges deliberately — reference a path with a trailing comma, or point `@` at a file bigger than your model's window — and watch what silent skipping and uncapped delivery each do to the answer.

Previous: [Chapter 3 — instructions](ch-03-instructions.md) · Next: [Chapter 5 — tools](ch-05-tools.md), where the model stops waiting for files to be pushed and asks for them itself. Chapter 6 ([context management](ch-06-context-management.md)) adds the door caps and compaction this chapter deliberately postponed.
