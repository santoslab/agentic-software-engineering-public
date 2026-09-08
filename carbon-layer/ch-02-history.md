# Chapter 2 — History: the harness owns the conversation

The ch-01 agent answers one request and retains no data from it. This is a property of the client implemented in chapter 1: every request contains a newly created message list, and neither the client nor the configured chat-completions endpoint is given a conversation identifier. This chapter adds a message list that the harness keeps and resends on every call. The code change is one new attribute and two `append` calls, but the resulting list becomes the input that later chapters prepend, append, compact, and persist.

## The primitive

The OpenAI-compatible request used in this repository supplies the conversation as a list of messages. The client does not use a server-managed conversation or session: it sends a list and receives one reply. Therefore, any earlier turn that should influence a response must be included again by the client. The module docstring of [harness/agent.py](../stages/ch-02-history/harness/agent.py) summarizes this division of responsibility:

> The model isn't stateful. The harness is.

The primitive is conversation history: the harness owns a `messages` list, appends each user turn, sends the *entire* list on every model call, and appends the reply so the next call sees it too. The capability it unlocks is multi-turn behavior — the model can now use facts stated on earlier turns, because those turns are physically present in its input. "Remembering" is an illusion produced by replay: the model rereads the whole conversation from scratch each time and simply continues it.

This state belongs in the harness because the harness constructs the request. The same list also becomes the shared representation used by later features: instructions are prepended in chapter 3, tool calls and tool results are appended in chapter 5, compaction rewrites older entries in chapter 6, and durable state serializes the list in chapter 9. The design is simple, although storing raw provider-format dictionaries also creates typing and consistency tradeoffs discussed below.

## From the video

The walkthrough introduces this stage at [6:49](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=409s) as the fix for ch-01's amnesia, and immediately raises the stakes: the speaker calls it "the single most important idea in the whole build" ([6:55](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=415s)). The formulation that follows is worth memorizing verbatim: "The model is stateless, so the harness keeps the conversation and replays it on every call" ([6:59](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=419s)). He then deflates any expectation of machinery — it is "just a list," and in the diff the change amounts to three lines: the list in the init and the two appends.

The demo at [7:40](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=460s) deliberately reruns the exact two-turn exchange that failed in chapter 1 — "Your name is Gemma," then "What is your name?" — and this time turn two succeeds: "It remembers." The point the speaker underlines is that nothing about the model changed: "Same stateless model, but now with the history living in the harness" ([7:53](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=473s)). The segment closes by naming the next gap: the agent recalls what you told it, but it has no standing personality — "Every turn it starts blank" ([8:04](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=484s)) — which is what instructions fix in chapter 3.

## The code

The stage snapshot is [stages/ch-02-history/](../stages/ch-02-history/). Relative to ch-01, the diff touches exactly four files: the agent, the acceptance registry, a new episode test, and a new seam test.

### The stateful `Agent` interface

The core change is in [harness/agent.py](../stages/ch-02-history/harness/agent.py). In chapter 1,
`send()` passed a newly created one-message list directly to `chat()` and retained nothing. At
ch-02 the class gains one attribute, and `send` becomes append/replay/append:

```python
class Agent:
    """A model wrapped in conversation memory the harness owns."""

    def __init__(self, model: str | None = None, provider: Provider | None = None) -> None:
        self.model = model
        self.provider = provider
        self.messages: list[dict] = []  # <-- the ONLY new attribute over ch-01

    def send(self, user_text: str) -> str:
        """Append the turn, replay the whole history, keep the reply."""
        self.messages.append({"role": "user", "content": user_text})
        resp = chat(self.messages, model=self.model, provider=self.provider)
        self.messages.append({"role": "assistant", "content": resp.content})
        return resp.content
```

The public interface is deliberately almost unchanged from chapter 1:

| Interface | Inputs and defaults | Return value | State and failure behavior |
|---|---|---|---|
| `Agent(model=None, provider=None)` | Optional model id and provider, both forwarded later to `chat()`. | A new agent object. | Creates a fresh empty `messages` list for that object. Construction performs no model call. |
| `send(user_text)` | One required string. Empty text is permitted; there is no validation. | The response's `content` string. | Appends the user before calling; appends the assistant only after success. A raised model error leaves the unmatched user message in history and propagates. |
| `messages` | Public mutable `list[dict]`, initially empty. | Callers may inspect or mutate it directly. | Every element is expected, but not type-validated, to follow the provider message shape. |

`self.messages: list[dict] = []` is an **instance attribute**: every call to `Agent()` evaluates a
new list expression, so two agents do not share history. This differs from a class attribute such
as `messages = []` in the class body, which would be shared by all instances.

At runtime, the REPL in `main()` (unchanged in shape since ch-01) constructs a single `Agent` and
calls `send` once per line of input, so the history accumulates for the life of the process — the
banner now reads “it remembers within this session.” Note that history is stored directly in the
provider wire format, a list of `{"role": ..., "content": ...}` dictionaries: there is no
`Message` class, so “replay the conversation” is literally “pass the list to `chat`.” The model
call still goes through the `model/` seam, so nothing in this file knows which provider is on the
other end.

`chat(self.messages, ...)` receives a reference to that same list, not an automatic copy. The real
client only reads it, and the tests' fakes copy the contents they want to retain. A responder that
mutated the list would mutate the agent's history as well. The stage does not defend against that
because the model boundary is treated as trusted Python code even though the remote model output
is not.

### History execution trace

For two calls on the same `Agent`, the list changes as follows:

1. Construction sets `self.messages` to an empty list.
2. `send("Your name is Gemma.")` appends the first user dictionary. `chat()` receives a list of
   length one and returns, for example, `"ok"`; `send()` appends that assistant dictionary.
3. `send("What is your name?")` appends a second user dictionary to the existing list.
4. The second `chat()` call receives three messages in order: the first user statement, the first
   assistant response, and the second user question.
5. The second assistant response is appended, leaving four messages for a possible third turn.

The model does not retrieve a hidden memory in step 4. It can use the name because the harness
places the earlier statement back in the request.

### Exact-payload episode tests

[tests/episodes/test_ch02.py](../stages/ch-02-history/tests/episodes/test_ch02.py) checks the new capability offline in two parts. The first test verifies that the second call carries the full history:

```python
def test_history_is_replayed():
    captured: list[list[str]] = []

    def fake_chat(messages, **kwargs):
        captured.append([m["content"] for m in messages])
        return LLMResponse(content="ok")

    with patch.object(agent_mod, "chat", side_effect=fake_chat):
        a = agent_mod.Agent()
        a.send("Your name is Gemma.")
        a.send("What is your name?")

    # The second call sees the full history: user1, assistant1, user2.
    assert captured[1] == ["Your name is Gemma.", "ok", "What is your name?"]
```

The nested `fake_chat` is a local function that can still access `captured` from the enclosing test.
This is a **closure**: the function retains access to names from the scope where it was created.
Here the closure is a lightweight recording test double—each call appends a snapshot to the outer
list, which the assertion reads afterward.

That `captured[1]` assertion is the primitive in one line: user turn one, the assistant's reply,
user turn two — all present in the second request. The second test, `test_model_can_use_history`,
simulates the model's side: a fake `chat` that answers “Gemma” only if the name appears somewhere in
the messages it was given. Together they encode the division of labor — the harness supplies the
context, the model merely uses whatever it is handed. The patching trick they rely on is deliberate
ch-01 groundwork: [model/client.py](../stages/ch-02-history/model/client.py) keeps `chat` a free,
module-level function, giving tests a straightforward name to replace with
`patch.object(agent_mod, "chat")`.

### Provider-seam test

[tests/test_model_seam.py](../stages/ch-02-history/tests/test_model_seam.py) is new here and, per the commit message, held forever after:

```python
def test_agent_runs_offline_through_fake_provider():
    a = Agent(provider=fake(scripted=lambda msgs: "PONG"))
    assert a.send("ping") == "PONG"
```

The fake provider itself ([model/fake.py](../stages/ch-02-history/model/fake.py)) already existed at ch-01, but chapter 1 did not drive a real `Agent` through it. Unlike the episode tests, this test performs no monkeypatching: the call reaches the real `chat()`, which dispatches to the provider's `responder` instead of HTTP (see [model/client.py](../stages/ch-02-history/model/client.py)). It therefore checks that the same agent interface operates through a second response implementation while remaining offline.

### Offline and live gates

[tasks/checks.py](../stages/ch-02-history/tasks/checks.py) registers this chapter's live acceptance and demo. `uv run verify` runs ruff, mypy, pytest, and imports offline; `uv run accept ch-02` evaluates the behavior with the configured live model:

```python
def _accept_ch02() -> bool:
    """The real agent recalls a fact stated on an earlier turn."""
    from harness import agent

    a = agent.Agent()
    a.send("Your name is Gemma. Please remember it.")
    reply = a.send("What is your name? Reply with just the name.")
    print("model replied:", repr(reply))
    return "gemma" in reply.lower()
```

This is the video's demo turned into an assertion: state a fact on turn one, require it back on turn two, on one live `Agent` whose only memory is the list.

The evidence has useful boundaries. The first episode test checks exact payload ordering but
replaces the whole model client. The seam test exercises real client dispatch but its scripted
provider does not interpret history. The live check establishes that a configured model can use
replayed context, but its substring assertion is tolerant rather than exact. None of the three
checks persistence across a process restart; chapter 9 adds that separate claim.

## Design decisions & gotchas

- **Replay is O(conversation), on purpose.** Every turn resends the entire history, so tokens and latency grow with every exchange, and the total cost of a session grows roughly quadratically. There is no trimming, no budget, no cap. That is a real problem — and it is deliberately not this chapter's problem. The finite context window is the subject of chapter 6 (context management), and it is worth noticing that compaction only *can* be a harness feature because the harness owns the list being compacted.
- **Memory is object-lifetime only.** `self.messages` lives in RAM and dies with the process; restart the REPL and the agent is blank again. Persistence (sessions on disk, recall across runs) is deferred to chapter 9 (durable state). The banner's phrasing — "within this session" — is precise.
- **Append order has a failure mode.** The user message is appended *before* the `chat` call, so the model can see it; the reply is appended after. If `chat` raises (network error, timeout), the exception propagates but the user message stays in the list — the next successful `send` will replay a conversation containing a user turn with no reply. Harmless at this scale, but it is the first appearance of a recurring harness theme: once you own state, you own its consistency under failure.
- **Wire-format dicts, no abstraction.** Storing history as raw `{"role", "content"}` dicts keeps replay trivially honest and matches what later chapters need, when tool-call and tool-result messages join the same list. The trade-off is that nothing type-checks the shape of a message; the harness is trusted to append well-formed entries.
- **Typed messages are a credible alternative.** A `Message` dataclass or `TypedDict` could restrict
  roles and make required fields visible to mypy. Conversion to provider dictionaries would then
  happen at the model boundary. The current dictionaries remove that conversion layer and make
  traces correspond directly to the HTTP payload, at the cost of allowing malformed state and
  provider-specific fields to spread through the harness.
- **Tests preserve capabilities, not temporary limitations.** Nothing had to be deleted at this tag because ch-01 did not assert that the agent forgets. Its tests assert behaviors that should remain true—one `send()` returns model content and forwards its provider—even after history is added. A test requiring the agent to forget would encode behavior that the next stage intentionally removes.
- **The acceptance probe is weaker than it looks.** `_accept_ch02` asks the agent to remember that its name is "Gemma" — but the live model *is* Gemma (`google/gemma-4-26b-a4b`), which may well volunteer that name with no history at all. The upstream commit message says the original live run recalled the author's name, "Ankit," which a model cannot guess; the code at the tag uses the weaker fact. A good exercise is to re-run `accept` with an arbitrary name and confirm the primitive, not the model's self-knowledge, is doing the work.

## Study pointers

Read the stage in this order:

1. [harness/agent.py](../stages/ch-02-history/harness/agent.py) — the whole primitive: one attribute, append/replay/append.
2. [tests/episodes/test_ch02.py](../stages/ch-02-history/tests/episodes/test_ch02.py) — the harness half and the simulated-model half of remembering, checked offline.
3. [tests/test_model_seam.py](../stages/ch-02-history/tests/test_model_seam.py) — the seam's second implementation, exercised end to end.
4. [model/client.py](../stages/ch-02-history/model/client.py) and [model/fake.py](../stages/ch-02-history/model/fake.py) — how `chat` dispatches to a `responder` instead of HTTP.
5. [tasks/checks.py](../stages/ch-02-history/tasks/checks.py) — the ch-02 acceptance and demo registrations.

Things to try: `uv run verify` is fully offline and should be green as-is. The demo and acceptance (`uv run demo ch-02`, `uv run accept ch-02`) need LM Studio serving a local model, configured via `.env`. Then run the REPL (`uv run agent`), teach it a fact, ask for it back, quit, restart, and ask again — feeling the boundary between in-session memory and no persistence is the fastest way to internalize what this chapter did and did not build. As a follow-up, add `print(len(agent.messages))` to `send` and watch the replayed payload grow turn by turn.

Previous: [Chapter 1 — model only](ch-01-model-only.md). Next: [Chapter 3 — instructions](ch-03-instructions.md). Later chapters that build directly on this list: [chapter 5 (tools)](ch-05-tools.md) appends tool calls and results to it, [chapter 6 (context management)](ch-06-context-management.md) budgets and compacts it, and [chapter 9 (durable state)](ch-09-durable-state.md) writes it to disk so it survives the process.
