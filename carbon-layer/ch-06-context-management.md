# Chapter 6 — Context management: the harness manages a finite window

Chapter 5 gave the model hands, and the price arrives immediately: every tool call, every tool result, and every `@file` block now lands in the conversation history, and the history rides along on every model call. The context window is finite, so a harness that keeps appending forever is a harness that eventually fails — not with an error, but with an agent that drifts, repeats itself, and forgets its own goal. This stage adds the first window-management primitives: compaction (summarize the middle of an overgrown history, keep the head and tail) and door control (clamp every item to a maximum size before it enters the prompt).

## The primitive

The primitive is context management: the harness takes explicit ownership of what fits in the window, instead of letting the window fill by accident. The stage's own framing, in the [agent docstring](../stages/ch-06-context-management/harness/agent.py), is the sharpest statement of why this matters: "The model didn't get worse — what's in front of it changed." When an agent gets dumb mid-task, the first suspect is the prompt the harness assembled, not the weights.

The masterclass taxonomy names four moves for managing context — select, compress, write, and isolate. This chapter builds **compress**, in two complementary forms:

- **Compaction** operates on the whole history. Before each model call, if the estimated size of `self.messages` exceeds a `context_limit` budget, the harness replaces the middle of the conversation with a single model-written summary note, keeping the first and last few messages intact.
- **Door control** operates on individual items. Every block that enters the prompt — an `@file` context block, a tool result — is truncated to `MAX_ITEM_CHARS` first, so one oversized item can never flood the window on its own.

The two moves cover each other's blind spots. Compaction bounds how long the accumulated conversation can get, but it cannot shrink a single enormous message; door control caps every message at the door, but cannot stop a hundred small turns from piling up. Either alone leaks; together they bound the window from both directions.

This job can only live in the harness. The model has no lever over prompt assembly and no view of what was dropped — it sees whatever payload arrives and nothing else. Only the component that composes the payload each turn (the harness, in `_payload()`) can decide what deserves the finite space, and only the harness can spend an extra model call to write the summary that stands in for what it evicted.

## From the video

The walkthrough introduces this chapter as "a direct consequence of the last one": the moment the agent got tools, "everything started piling up into the conversation" — every tool call, every result, every file it reads — and at [14:38](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=878s) the harness "picks up a new job that manages what actually fits into that window." The author then lays out the full taxonomy from the masterclass video — "select, compress, write, and isolate" ([14:50](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=890s)) — and is explicit that this stage builds only compress: summarize the middle, protect the head and the tail, "because models read the start and the end most reliably" ([15:04](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=904s)). The stated goal: "make it shorter without losing the thread" — the goal, the decisions, and the facts.

The code tour points at the two new modules — `maybe compact` estimating tokens before deciding whether to compact, and `limits.py` deciding "the maximum item characters that we want" and clamping every file and tool output to that size. Then the on-camera demo makes the primitive visible: the author starts the REPL with a tiny context limit, buries a codename under enough turns of filler chatter to blow the budget, and watches the REPL print its compaction notice. Asked for the codename afterward, the agent still answers — Crime Master Gogo — because, as the author puts it at [16:43](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1003s), "the middle got compressed, but the thing that actually mattered survived." The closing beat is a deliberate cliffhanger: the window is handled, but the agent "still works all of this from scratch, every single time it runs" — persistence across runs is a later primitive (durable state, ch-09).

## The code

The diff touches two existing files and adds two modules plus a test episode:
[harness/agent.py](../stages/ch-06-context-management/harness/agent.py) wires the new moves into the
loop, [harness/compaction.py](../stages/ch-06-context-management/harness/compaction.py) and
[harness/limits.py](../stages/ch-06-context-management/harness/limits.py) implement them, and
[harness/context.py](../stages/ch-06-context-management/harness/context.py) picks up clamping for
`@file` blocks.

### Agent budget state and turn-boundary integration

Start at the loop. `Agent` gains a `context_limit` constructor parameter (default `DEFAULT_CONTEXT_LIMIT = 4000`, in ~tokens) and a `just_compacted` flag, and `_run` — the tool loop from ch-05 — now opens with a budget check:

```python
    def _maybe_compact(self) -> None:
        # Estimate the window cheaply; compact only when it overruns the budget.
        self.just_compacted = False
        if estimate_tokens(self.messages) > self.context_limit:
            self.messages = compact(self.messages, model=self.model)
            self.just_compacted = True
```

```python
    def _run(self) -> str:
        """Drive the model, executing tool calls until it produces a final answer."""
        self._maybe_compact()
        specs = self.tools.specs() if self.tools else None
```

The new `context_limit` constructor argument defaults to 4,000 approximate tokens and is stored
without validation. Zero requests compaction whenever the crude estimate is positive; a negative
value makes even a zero estimate exceed the threshold.
`just_compacted` is public observation state. `_maybe_compact()` resets it to `False` at the start
of every `_run()` and sets it after taking the over-limit branch, so it describes the current turn,
not whether compaction has ever happened. It reports that the branch ran, not necessarily that the
list became shorter: `compact()` returns the original list when it has at most the configured head
plus tail count, but `_maybe_compact()` still sets the flag to `True`.

The other loop change wraps each tool result in `clamp(...)` as it is appended, so the door check
happens at the exact point where a tool's output becomes a message.

```python
                    self.messages.append(
                        {"role": "tool", "tool_call_id": tc.get("id", ""), "content": clamp(result)}
                    )
```

### `estimate_tokens()` and `compact()`

[harness/compaction.py](../stages/ch-06-context-management/harness/compaction.py) is the core of the
chapter. Its public interfaces are:

| Interface | Inputs and defaults | Return/state | Failure behavior |
|---|---|---|---|
| `estimate_tokens(messages)` | Provider-shaped message list. | Integer sum of content-character counts divided by four. | Missing/false content counts as empty; non-string content is stringified. |
| `compact(messages, keep_head=2, keep_tail=4, model=None)` | History, two message counts, optional model id. | The original list unchanged when short enough; otherwise a new head + summary + tail list. | Model-call failures propagate; counts are unvalidated and follow ordinary Python slicing; no retry. |

`estimate_tokens` is deliberately crude — “Cheap ~4-chars-per-token estimate over message
contents”:

```python
def estimate_tokens(messages: list[dict]) -> int:
    """Cheap ~4-chars-per-token estimate over message contents."""
    return sum(len(str(m.get("content", "") or "")) for m in messages) // 4
```

`compact` does the head-and-tail surgery. It keeps the first `keep_head=2` and last `keep_tail=4` messages, flattens the middle into a role-labeled transcript, and asks the model — through the same `chat` seam every other call uses — to compress it into a checkpoint:

```python
    head = messages[:keep_head]
    tail = messages[-keep_tail:]
    middle = messages[keep_head:-keep_tail]

    transcript = "\n".join(f"{m.get('role')}: {m.get('content', '')}" for m in middle)
    summary = chat(
        [
            {"role": "system", "content": COMPACTION_PROMPT},
            {"role": "user", "content": transcript},
        ],
        model=model,
        max_tokens=512,
    ).content

    note = {"role": "system", "content": f"[summary of earlier conversation]\n{summary}"}
    return head + [note] + tail
```

The bracket notation is Python **slicing**. `messages[:2]` selects indices before 2; `messages[-4:]`
selects the last four; `messages[2:-4]` selects what lies between. Slicing produces shallow lists:
the lists are new, but their message dictionaries are the same objects. The final concatenation
also produces a new list and retains the original head/tail dictionary objects exactly, which is
why identity-insensitive equality tests can assert they are unchanged.

The defaults assume positive counts. In particular, `keep_tail=0` makes `-keep_tail` equal zero,
so `messages[keep_head:-keep_tail]` becomes `messages[keep_head:0]`, not “through the end.” The
public function does not validate that edge; its callers use the defaults or positive test values.

The summary call forwards `model` and sets `max_tokens=512`, but does **not** forward the agent's
explicit `provider`. An agent using an injected fake or non-default provider can therefore take
the environment-configured HTTP path during compaction. The offline test patches
`harness.compaction.chat` separately, and later hardening would need dependency forwarding if
compaction must honor the same provider seam.

`COMPACTION_PROMPT` is worth reading in full, because it encodes the chapter's real insight: a good summary is defined by what the *next* turn needs, not by brevity. It instructs the summarizer to "Preserve, verbatim, every concrete fact, code, name, decision, file path, and the current goal and next step. Drop chit-chat."

### `clamp()` at the two input doors

[harness/limits.py](../stages/ch-06-context-management/harness/limits.py) is the entire door-control
mechanism — eighteen lines:

```python
MAX_ITEM_CHARS = 4000


def clamp(text: str, max_chars: int = MAX_ITEM_CHARS) -> str:
    """Truncate an item to ``max_chars``, with a marker noting what was dropped."""
    if len(text) <= max_chars:
        return text
    dropped = len(text) - max_chars
    return f"{text[:max_chars]}\n…[truncated {dropped} chars]"
```

`clamp(text, max_chars=4000)` returns the original string when it fits. Otherwise it keeps exactly
the first `max_chars` characters and appends a marker reporting `len(text) - max_chars`. The final
returned string is therefore *longer* than `max_chars` by the marker length; the setting bounds
retained source content, not total message length. Values below zero are accepted and have Python's
negative-slice behavior, another reason this teaching implementation expects ordinary positive
configuration.

The marker matters: the model is told that content was dropped and how much, rather than being
handed a silently amputated file.
[harness/context.py](../stages/ch-06-context-management/harness/context.py) applies the same clamp to
`@file` delivery — the ch-04 code is unchanged except that the block is clamped before it is
returned (`blocks.append(clamp(f"--- {path} ---\n{body}"))`), and its docstring is rewritten to
retire ch-04's admission that blocks were “raw and uncapped”: now “the harness, not the model, opens
the file — and decides how much fits.”

The two doors are not exhaustive: ordinary user messages, assistant text, and model-generated
compaction summaries are not clamped. “Every item” in the chapter's framing refers to externally
loaded file blocks and tool results, the two newly unbounded inputs the harness controls here.

### REPL visibility

The REPL in `main()` makes the primitive demoable. A new `--context-limit` flag ("Set it low, e.g. 400, to watch compaction fire live"), and after each reply the REPL reads the `just_compacted` flag:

```python
        reply = agent.send(user)
        if agent.just_compacted:
            print("[context compacted — kept the start and end, summarized the middle]")
        print("bot>", reply)
```

### Offline tests and live acceptance evidence

The offline gate in
[tests/episodes/test_ch06.py](../stages/ch-06-context-management/tests/episodes/test_ch06.py)
replaces `chat` for deterministic checks. It tests the arithmetic of `estimate_tokens`, verifies
that `compact` preserves exact head and tail messages while shortening the list, drives an agent
over the limit and checks for a summary note, and covers both clamp sites. Oversized `@file` and
tool-result inputs must be shortened and marked `truncated`:

```python
def test_compact_keeps_head_and_tail_and_summarizes_middle():
    msgs = [{"role": "user", "content": f"m{i}"} for i in range(10)]
    with patch.object(compaction, "chat", return_value=LLMResponse(content="SUMMARY")):
        out = compact(msgs, keep_head=2, keep_tail=2)
    assert out[0] == msgs[0] and out[1] == msgs[1]
    assert out[-1] == msgs[-1] and out[-2] == msgs[-2]
    assert any("SUMMARY" in m["content"] for m in out)
```

The live acceptance in
[tasks/checks.py](../stages/ch-06-context-management/tasks/checks.py) combines two checks against a
real model. `_accept_ch06_compaction` uses `context_limit=80`, introduces the fact “the deploy key is
GRIFFIN-7,” adds eight filler turns, and then checks both that compaction occurred and that the reply
still contains the key. This supplies evidence that the generated summary retained the fact needed
by the later question; it does not establish that arbitrary facts survive. `_accept_ch06_doorcontrol`
registers a `dump` tool that returns a value four times the configured cap and checks the tool
message stored in history. This branch is deterministic except for the live model choosing the
tool. The demo uses the same mechanisms with a different codename and a 20,000-line log file.

### Compaction execution trace

When `_maybe_compact()` estimates that the next request exceeds `context_limit`:

1. `compact()` retains the configured messages at the head and tail of `self.messages` exactly.
2. It converts the middle messages into a role-labeled transcript and asks `chat()` for a bounded
   summary. This is an additional model request, separate from the user's pending turn.
3. It replaces the removed middle with one system-role checkpoint containing the generated summary.
4. `Agent` assigns the shorter list back to `self.messages` and marks `just_compacted=True`.
5. The ordinary model call proceeds with the preserved head, summary checkpoint, and recent tail.

If the summary omits a fact, later turns cannot recover that fact from the removed messages. The
live check therefore verifies both that compaction occurred and that one planted fact survived.

## Design decisions & gotchas

**Compaction runs at turn boundaries, not inside the tool loop.** `_maybe_compact` is called once at the top of `_run`, so a single turn's tool storm can still push the history past the budget until the next `send`. That overshoot is bounded, though: at most `MAX_TOOL_STEPS` results per turn, each clamped to `MAX_ITEM_CHARS` — the two limits from ch-05 and ch-06 compose into a worst-case per-turn growth cap.

**Two limits, two units.** `context_limit` is in approximate tokens (4 chars each); `MAX_ITEM_CHARS` is in characters. The defaults line up sensibly — a 4,000-token budget is ~16,000 chars, and each item is capped at 4,000 chars (~1,000 tokens) — but read the units carefully before tuning either.

**The estimate is deliberately approximate.** `estimate_tokens` counts only `content` fields. The system prompt and AGENTS.md live outside `self.messages`, and the JSON of `tool_calls` on assistant messages is omitted. The value can trigger compaction near the configured limit, but it should not be interpreted as a provider token count.

**Compaction requires an additional model call.** The summary uses `chat()` with `max_tokens=512`. This adds latency and token usage to the turn, so the harness invokes it only after the estimated history exceeds the configured budget rather than on every turn.

**The splice is index-based, not structure-aware.** `compact` cuts at message positions 2 and −4 with no regard for tool-call pairing, so the kept tail can begin with a `tool` message whose `assistant` partner (the one carrying `tool_calls`) was summarized away. Lenient local servers accept this; strict OpenAI-style APIs reject orphaned tool messages. A production harness compacts at structurally safe cut points — a refinement this chapter deliberately skips. The summary note also re-enters the history as a mid-conversation `system` message, another liberty a strict endpoint may not extend.

**Compaction is lossy and irreversible.** Whatever the summarizer drops is gone from the window for good — there is no store to fetch it back from yet. The `COMPACTION_PROMPT`'s "verbatim" demand is the only defense. The compaction docstring flags the deeper principle — "present is not the same as used": keeping the head and tail intact is not sentiment but an accommodation of how models actually attend to long prompts.

**Clamp keeps the head of an item.** `clamp` truncates from the front, so for a log file whose interesting lines are at the end (the demo's `log.txt`, say), the marker survives but the recent errors don't. Keeping an item's own head *and* tail is a natural exercise; the chapter keeps the mechanism minimal.

**The flag exists for visibility.** `just_compacted` does nothing for correctness — it exists so the REPL can announce that the window was managed. Making invisible harness events visible is a running theme that becomes its own primitive in ch-13 (observability).

**Three of the four moves are deferred.** This chapter builds compress. *Write* (persist context outside the window) arrives with durable state in ch-09, *isolate* (give work its own window) with subagents in ch-11, and *select* shows up as skills' load-on-demand disclosure in ch-07 and memory search in ch-09. The agent also still forgets everything between runs — compaction manages the window within a session; it is not memory.

## Study pointers

Read the stage in this order:

1. [harness/limits.py](../stages/ch-06-context-management/harness/limits.py) — the smallest possible door control; read the docstring's threat list (distraction / confusion / poisoning).
2. [harness/compaction.py](../stages/ch-06-context-management/harness/compaction.py) — the estimate, the head/tail splice, and the summarizer prompt.
3. [harness/agent.py](../stages/ch-06-context-management/harness/agent.py) — the ch-06 docstring, `_maybe_compact`, the `clamp(result)` call site, and the REPL's `--context-limit` flag.
4. [harness/context.py](../stages/ch-06-context-management/harness/context.py) — how the ch-04 primitive absorbed door control with a one-line change.
5. [tests/episodes/test_ch06.py](../stages/ch-06-context-management/tests/episodes/test_ch06.py) — how both moves are tested offline with a patched `chat`.
6. [tasks/checks.py](../stages/ch-06-context-management/tasks/checks.py) — the ch-06 section: the GRIFFIN-7 recall check and the `dump`-tool clamp check that make up the live gate.

Things to try (running the REPL, demo, or `accept` needs a live model — by default LM Studio serving a local model, per the repo's `.env`; `uv run verify` is fully offline):

- `uv run agent --context-limit 400`, then recreate the video's demo: state a codename, bury it under filler turns, and watch for `[context compacted — kept the start and end, summarized the middle]` before asking for it back. Then retry with `keep_head=0` (edit the `compact` call) and see what dies.
- `uv run demo ch-06` prints the whole arc — message counts, token estimate, compaction flag, recall, and a 20,000-line file arriving as a ~4,000-char clamped block.

Previous: [ch-05 — tools](ch-05-tools.md) · Next: [ch-07 — skills](ch-07-skills.md)

Later chapters that build on this primitive: [ch-09 — durable state](ch-09-durable-state.md) (the *write* move: context that survives the window and the process), [ch-11 — subagents](ch-11-subagents.md) (the *isolate* move: separate windows that return answers, not transcripts), and [ch-13 — observability](ch-13-observability.md) (events like `just_compacted` graduate into a real trace).
