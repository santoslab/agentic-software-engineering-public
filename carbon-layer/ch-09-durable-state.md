# Chapter 9 — Durable state: the harness writes the session down so it survives

Every primitive so far — history, instructions, tools, compaction, skills, the sandbox — lives and dies inside one process. Kill the REPL and the agent forgets everything, because the conversation only ever existed as a Python list. This chapter makes state durable: the harness serializes the session to disk after every turn and reloads it on startup, so a restarted agent picks up exactly where it left off. The same module then turns that pile of session files into something the model can *query* — a `search_memory` tool that does plain keyword search across past sessions and pulls matching facts back into the current context.

## The primitive

The primitive is **durable state**: the rule that nothing survives unless the harness writes it down. Concretely, an `Agent` can now be given a session id. On construction it loads any prior conversation for that id from a JSON-L file (one message per line); after every `send()` it writes the full history back. The process is no longer the unit of survival — the session file is. The module docstring in [harness/memory.py](../stages/ch-09-durable-state/harness/memory.py) states the invariant crisply: "The session boundary is the kill point — nothing survives unless it's written."

The second half of the primitive is **episodic memory**. A log is not memory until you can recover the right slice of it, so the module also ships `search_sessions` — keyword text search across *all* stored sessions, no embeddings — and wraps it as `search_memory_tool`, a regular `Tool` the model can call. That gives the agent recall beyond its context window: facts from sessions that are not loaded at all can be searched for and re-injected on demand.

Both halves must live in the harness, not the model. The model is stateless per call — its only "memory" is whatever the harness assembles into the payload, and that assembly evaporates with the process. Persistence is an environment concern: something has to decide *what* is written (the raw message list), *when* (after every turn, so the kill point is the only loss boundary), and *where* (a directory the next process can find). And retrieval is a context decision — choosing which five old messages re-enter a finite window is exactly the kind of selection the harness has owned since [ch-06](ch-06-context-management.md). The model participates only through the tool interface it already knows.

## From the video

The walkthrough introduces the chapter at [22:11](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1331s): "the harness writes the session down to a disk as a JSON L file, one message per line in a new module called memory.py." The agent gets a session, loads history on startup, and saves after every turn — "so you kill the process, restart, and we pick right up where we left off."

The author is careful to split the primitive in two. Persisting alone is not enough — a log isn't memory until you can recall the right slice — so the chapter also adds episodic search: at [22:52](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1372s) he stresses it is "a plain keyword search across all stored sessions, no embeddings," notes the design is borrowed from the Hermes agent, and frames it in the context-management vocabulary from ch-06: "That's the select move applied to history."

Then the proof, live: he tells the agent an amount, kills the process, starts a fresh agent on the same session, and asks what the amount was. At [23:18](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1398s) it answers, and he lands the chapter's one-line thesis: "The fact outlived the process that held it." He also flags a shortcut in passing — the REPL session name is "hard coded name for now but you can also pass in a parameter to load any specific session."

The segment closes by setting up the next chapter: the agent now survives a restart, "but look at what a turn still is. It's one loop, one shot" ([23:54](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1434s)). A real task needs planning, and buried inside a single loop there is nothing to hook, gate, or see — that is ch-10's problem.

## The code

The diff from ch-08 touches one existing file and adds two: the loop in
[harness/agent.py](../stages/ch-09-durable-state/harness/agent.py) grows session awareness,
[harness/memory.py](../stages/ch-09-durable-state/harness/memory.py) is the new module, and
[tests/episodes/test_ch09.py](../stages/ch-09-durable-state/tests/episodes/test_ch09.py) plus a ch-09
block in [tasks/checks.py](../stages/ch-09-durable-state/tasks/checks.py) are the gates.

### Session-aware `Agent` construction and save timing

Start with the loop, because the delta there is deliberately tiny. `Agent.__init__` takes two new parameters, `session: str | None = None` and `sessions_dir: str = DEFAULT_DIR`, and the line that used to read `self.messages: list[dict] = []` becomes a resume:

```python
        self.session = session
        self.sessions_dir = sessions_dir
        # Resume: load prior conversation from disk if this session exists (ch-09).
        self.messages: list[dict] = load_session(session, sessions_dir) if session else []
```

Writing is symmetric — a private `_save` that is a no-op for sessionless agents, called once per turn at the end of `send()`:

```python
    def _save(self) -> None:
        # Durable state: persist the full history so a restart can resume it.
        if self.session:
            save_session(self.session, self.messages, self.sessions_dir)

    # ... elided ...

    def send(self, user_text: str) -> str:
        """Inject any @path files, append the turn, drive the loop, then persist."""
        for block in deliver(user_text):  # @file references → injected context
            self.messages.append({"role": "user", "content": f"Context file:\n{block}"})
        self.messages.append({"role": "user", "content": user_text})
        reply = self._run()
        self._save()  # durable state: persist after every turn
        return reply
```

`session=None` and `session=""` both disable loading and saving because the code tests truthiness.
Any other string becomes a filename stem without validation at this tag. `sessions_dir` defaults to
the relative `.sessions` directory and is stored as supplied; relative roots are interpreted
against the process cwd when a memory function performs I/O. The directory is not created merely
by constructing a sessionless agent.

That is the entire loop change. `_run`, compaction, the approval gate, and the payload assembly are
untouched — durable state wraps the turn, it does not reach inside it. Save happens after `_run()`
returns. A model or approval exception therefore prevents the write, while a returned string such
as the tool-budget error is saved. There is no `finally` block or transaction joining model state
to disk state.

### JSONL storage interfaces

The mechanics live in `memory.py`. A session is a `<id>.jsonl` file under `.sessions/` (the `DEFAULT_DIR`), and save/load are as plain as the format suggests:

```python
def save_session(session_id: str, messages: list[dict], base: str | Path = DEFAULT_DIR) -> None:
    path = _path(session_id, base)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for m in messages:
            f.write(json.dumps(m) + "\n")


def load_session(session_id: str, base: str | Path = DEFAULT_DIR) -> list[dict]:
    path = _path(session_id, base)
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
```

**JSONL** (JSON Lines, written “JSON-L” in the upstream docstring) stores one complete JSON value per
line. It is not one large JSON array: each message dictionary is independently converted by
`json.dumps()`, followed by a newline. `json.loads(line)` performs the reverse parse. This makes the
file readable and line-oriented, but no schema validation confirms that a parsed value is a
message dictionary.

| Interface | Inputs/defaults | Return/state | Failure behavior |
|---|---|---|---|
| `save_session(session_id, messages, base=".sessions")` | Identifier, full list, storage root. | Creates parents, truncates/replaces `<id>.jsonl`, returns `None`. | Serialization and filesystem errors propagate; write is non-atomic. |
| `load_session(session_id, base=".sessions")` | Identifier and root. | Parsed nonblank lines in file order; missing file gives `[]`. | One malformed JSON line or a read error aborts the whole load. |
| `save_trace(session_id, rows, base=".sessions")` | Identifier, JSON-compatible flat-event rows, root. | Replaces `traces/<id>.jsonl`; creates parents; returns `None`. | Serialization and filesystem errors propagate; write is non-atomic. |
| `load_trace(session_id, base=".sessions")` | Identifier and root. | Parsed nonblank trace rows; missing file gives `[]`. | One malformed line or read error aborts the whole load. |
| `delete_session(session_id, base=".sessions")` | Identifier and root. | Removes message and trace files; returns `None`. | Missing files are ignored; other unlink errors propagate. |
| `list_sessions(base=".sessions")` | Root. | Metadata dictionaries sorted newest first. | Missing root gives `[]`; `OSError` while reading a file skips it, while decoding errors or a later `stat()` race propagate. |
| `search_sessions(query, base=".sessions", limit=5)` | Search text, root, result cap. | Ranked `{session, role, content}` dictionaries; blank query or missing root gives `[]`. | A malformed stored line or read error aborts the search; `limit` is not validated. |
| `search_memory_tool(base=".sessions")` | Storage root captured by a closure. | A `search_memory` `Tool`; no filesystem work yet. | Search failures become `error:` strings when invoked through `ToolRegistry`. |

The trace and session-management interfaces are present but deferred: chapter 13 activates
`save_trace()`/`load_trace()`, and chapter 14 consumes deletion and listing. At ch-09 no trace has
yet been produced, and the REPL does not list or delete sessions. Listing the interfaces here
prevents source presence from being mistaken for active behavior.

What gets written is the raw message list in provider format — user turns, assistant turns with
their `tool_calls`, and `role: "tool"` results. Loading it back therefore reconstructs the current
in-memory payload state, not an append-only audit history. If compaction already replaced older
messages with a summary, the file contains that summary and no longer contains the removed turns.
A missing file loads as `[]`, which is what makes “resume if it exists, start fresh if it doesn't”
a single expression in the constructor.

### Keyword search and the `search_memory` tool

Retrieval is `search_sessions`: split the query into lowercase terms, scan every message of every `*.jsonl` file in the directory, and score each message by how many terms appear in its content:

```python
    scored: list[tuple[int, dict]] = []
    for path in sorted(base_dir.glob("*.jsonl")):
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            msg = json.loads(line)
            content = str(msg.get("content", "") or "").lower()
            score = sum(term in content for term in terms)
```

`query.lower().split()` performs whitespace tokenization only: punctuation remains attached, and
there is no stemming. `term in content` is substring matching, so `cat` also matches `concatenate`.
In Python, `True` behaves as integer 1 and `False` as 0, so `sum(...)` counts how many query-list
entries are present at least once. The code does not deduplicate the query, so `cat cat` can
score two points; repeated occurrences of `cat` in the stored content do not raise the score.

Matching messages are sorted by descending score and the first `limit` entries (default 5) are
returned as `{session, role, content}` dictionaries. Python's sort is stable, so equal scores retain
the order produced by sorted filenames and then file lines. `limit=0` returns no hits; negative
values use ordinary negative slicing and unexpectedly return all but the last few, because the
interface does not validate the setting. There is no index or embedding model; the linear scan is
sufficient for the small teaching dataset and its ranking is easy to inspect.

`search_memory_tool` wraps that function in the `Tool` dataclass from [harness/tools.py](../stages/ch-09-durable-state/harness/tools.py), formatting hits with their session of origin:

```python
    def search_memory(query: str) -> str:
        hits = search_sessions(query, base=base)
        if not hits:
            return "no matching memory found"
        return "\n".join(f"[{h['session']}] {h['role']}: {h['content']}" for h in hits)
```

`search_memory_tool(base)` is a factory. Its nested `search_memory(query)` closure retains the
selected storage root; the model's schema therefore exposes only `query`, not the filesystem path.
No hits returns the non-error string `no matching memory found`, allowing the model to distinguish
an empty search from a tool failure.

Because memory search is exposed as an ordinary tool, the existing `_run` loop needs no special
branch. `main()` registers `search_memory_tool()` beside the sandbox and workspace tools and
constructs the agent with the session id `repl`. Retrieved text returns as a normal tool result and
is passed through chapter 6's `clamp`, limiting how much old session content enters the active
window at once.

### Offline tests and live acceptance evidence

The gates follow the repo's two-gate rule. The pytest side ([tests/episodes/test_ch09.py](../stages/ch-09-durable-state/tests/episodes/test_ch09.py)) is deterministic and offline — the resume test patches `chat` with a canned `LLMResponse` so no model is involved:

```python
def test_agent_resumes_from_disk(tmp_path):
    with patch.object(agent_mod, "chat", return_value=LLMResponse(content="ok")):
        a = agent_mod.Agent(session="demo", sessions_dir=str(tmp_path))
        a.send("remember: the one with the mark is Teja")

    # A brand-new agent (simulating a restart) reloads the prior conversation.
    b = agent_mod.Agent(session="demo", sessions_dir=str(tmp_path))
    assert b.messages  # resumed, not empty
    assert any("Teja" in m["content"] for m in b.messages)
```

Other tests cover the JSONL round trip, ranking (“warehouse passcode” must find GOGO-77 in the
right session), empty and no-match queries, and the tool running through a real `ToolRegistry`.
They use `tmp_path`, so no test reads or overwrites the developer's `.sessions` directory.

The acceptance gate (`uv run accept ch-09`, in
[tasks/checks.py](../stages/ch-09-durable-state/tasks/checks.py)) asserts both halves against a live
model. `_accept_ch09_state` tells one agent a fact, constructs a *second* agent on the same session
id, and requires the resumed agent to answer from disk. `_accept_ch09_episodic` seeds an
`old-session` file containing “the warehouse passcode is GOGO-77”, registers the memory tool on a
*sessionless* agent, and checks not only the answer but that the tool was actually exercised:

```python
    used = any(m.get("role") == "tool" for m in a.messages)
    print("used search_memory:", used, "| reply:", repr(reply))
    return "gogo-77" in reply.lower() and used
```

Since GOGO-77 exists only on disk, a correct reply plus a `tool` message in the history is evidence
for cross-session retrieval rather than in-context recall. The check does not inspect the tool name,
so the planted value is what makes the result discriminating.

### Save-and-resume execution trace

For two `Agent` objects constructed with the same session id:

1. The first constructor calls `load_session()`; a missing file yields an empty history.
2. After `send()` completes, `_save()` serializes each message as one JSON object per line in the
   session file.
3. The first object can be discarded, simulating process termination.
4. The second constructor resolves the same session path, parses each JSON line, and restores the
   message dictionaries in their original order.
5. Its next `send()` appends a new user turn and sends the restored history plus that turn to the
   model.

`search_memory` follows a different path: it scans other saved session files, ranks matching text,
and returns excerpts through a tool result. Resumption restores one named transcript; episodic
search retrieves selected material across transcripts.

## Design decisions & gotchas

**Rewrite, don't append.** JSON-L is pitched as "one message per line, easy to append," yet `save_session` opens the file in `"w"` mode and rewrites the whole history every turn. That is deliberate: compaction (ch-06) *mutates the middle* of `self.messages`, so an append-only log would drift from the in-memory state the moment the window is compacted. Full rewrite keeps the invariant simple — disk always equals memory as of the last completed turn.

**The write is not atomic.** A kill in the middle of `save_session` can leave a truncated file; there is no write-to-temp-then-rename. For a teaching chapter the window is tiny (the write happens between turns, not during them), but it is a real gap — the upstream repo hardens exactly this in a post-course fix commit ("atomic saves"). Note also that `load_session` does `json.loads` per line with no error handling, so a corrupt line raises rather than degrades.

**Sessions are plaintext on disk.** Whatever passed through the conversation — including tool output, which after ch-08 can be command results — is now written under `.sessions/` verbatim. The stage's [.gitignore](../stages/ch-09-durable-state/.gitignore) excludes `.sessions/` so state never lands in version control, but anything secret the agent saw in a turn is now a file. Relatedly, the session id is interpolated straight into a filename (`Path(base) / f"{session_id}.jsonl"`) with no sanitization; that is fine while ids come from the developer (`"repl"`, `"demo"`, `"acc"`), and it is why they should not come from anywhere else.

**Search is deliberately dumb.** Term-presence counting (each query term scores 0 or 1 per message, regardless of frequency), top five results, ties broken by scan order. No embeddings, no index — the author frames this as the *select* move applied to history, and the simplest thing that demonstrates it. Note the scan covers every `*.jsonl` in the directory, so the current session's own on-disk copy is searchable too, not just past ones.

**JSONL offers observability, not safety by itself.** A relational or embedded database could add
transactions, indexes, and schema constraints; an append-only event log could preserve every
pre-compaction turn. Full-file JSONL rewrite is easier to inspect and keeps disk equal to current
memory, but it scales linearly per save and provides no atomicity or validation at this tag.

**The file is ahead of the chapter.** `memory.py` also contains `save_trace`/`load_trace`, `delete_session`, and `list_sessions` — helpers nothing at this tag calls. They serve trace persistence and the sessions pane in later chapters (observability, [ch-13](ch-13-observability.md), and the TUI, [ch-14](ch-14-ui.md)); their docstrings cite "ch-16" and "ch-24", numbering from an earlier, longer cut of the course before it was consolidated to fifteen chapters. One detail is worth noticing now: traces go in a `traces/` *subdirectory* precisely so the `*.jsonl` globs used by `list_sessions` and `search_sessions` never mistake a trace file for a conversation.

**Deferred.** Semantic retrieval (embeddings), incremental appends, session management UX (list, switch, delete from the REPL), and any notion of *structured* memory beyond the transcript are all left out. Sessions become visible, listable, and deletable objects only when the TUI arrives in ch-14.

## Study pointers

Read the stage in this order:

1. [harness/memory.py](../stages/ch-09-durable-state/harness/memory.py) — the whole primitive in one file: JSON-L save/load, keyword search, the tool wrapper (and the forward-looking trace/list helpers you can skim for now).
2. [harness/agent.py](../stages/ch-09-durable-state/harness/agent.py) — how small the loop delta is: two constructor parameters, a resume expression, `_save()` at the end of `send()`, and two lines in `main()`.
3. [tests/episodes/test_ch09.py](../stages/ch-09-durable-state/tests/episodes/test_ch09.py) — the offline gate: round trip, restart, ranking, and the tool through the registry.
4. [tasks/checks.py](../stages/ch-09-durable-state/tasks/checks.py) (the ch-09 block at the bottom) — the live gate and the demo, mirroring the video's kill-and-restart experiment.

Things to try (running the demo, REPL, or `accept` needs LM Studio serving a local model per the stage's [README](../stages/ch-09-durable-state/README.md); the pytest gate runs offline): run `uv run agent`, tell it a fact, Ctrl-D, rerun, and ask for the fact back — then open `.sessions/repl.jsonl` and read the conversation as the model sees it, tool calls included. Run `uv run demo ch-09` for the scripted version of both halves. Then break something on purpose: hand-edit a line of the session file into invalid JSON and watch where the resume fails — it makes the "no validation on load" gotcha concrete.

Previous: [ch-08 — execution environment](ch-08-execution-environment.md). Next: [ch-10 — orchestration](ch-10-orchestration.md). This primitive resurfaces later: [ch-13 — observability](ch-13-observability.md) persists trace events beside the session files, and [ch-14 — UI](ch-14-ui.md) builds its sessions pane on `list_sessions` and `delete_session` from this very module.
