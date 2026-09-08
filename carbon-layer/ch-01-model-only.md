# Chapter 1 — Model only: one call through a configurable model interface

Chapter 0 created the project structure and its offline and live checks, but it did not contain an
agent. This chapter adds an `Agent` whose only behavior is to send one user message to a model and
return the model's text. It also adds the `model/` package responsible for choosing an endpoint,
making the HTTP request, and converting the provider's JSON response into a Python object used by
the harness.

This is intentionally not yet a conversational agent. Each call is independent. The important
engineering result is a stable boundary between `harness/agent.py` and the code that communicates
with a model provider. In this book that kind of boundary is called a **seam**: callers use one
interface while the implementation behind the interface can vary. Here, `Agent` always calls
`chat()`. The `chat()` function can use an OpenAI-compatible HTTP service or a deterministic fake
without requiring changes to `Agent.send()`.

## The primitive

The primitive is one model call together with the interface around it. Chapter 1 introduces four
responsibilities that are worth keeping separate:

1. `Agent.send()` converts a user's string into a chat message and returns visible response text.
2. `chat()` is the single entry point used by the harness for a model request.
3. `Provider` records which endpoint, model identifier, and credential should be used. Its optional
   `responder` field also permits a caller to supply non-HTTP behavior for tests.
4. `complete_openai()` implements the actual OpenAI-compatible HTTP exchange and normalizes the
   response into `LLMResponse`.

Calling `chat()` a *free function* means that it is defined directly in a module, rather than as a
method belonging to an object. A more familiar Python description is simply “a module-level
function.” Code imports it with `from model import chat` and calls `chat(...)`; there is no client
object to construct first.

This separation is useful because the rest of the harness should not have to know whether a model
is local or hosted, which URL convention it uses, or what raw JSON it returns. Those details can
change more often than the agent loop. The separation is not complete provider independence,
however: the only network implementation in this stage is OpenAI-compatible. Supporting a
different native protocol would require a new implementation *and* a change to `chat()` (or another
dispatch mechanism) so that it can select that implementation.

The chapter also demonstrates the limitation that motivates chapter 2. A chat-completions request
contains all of the messages the model may use for that response. Chapter 1 sends a newly created,
one-element list on every call and retains no conversation state. Consequently, the second call
does not contain the first call's message or response. Chapter 2 adds that state to the harness.

## From the video

The walkthrough introduces the development method as finding the first missing capability, then
adding the smallest harness feature that supplies it. At
[5:15](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=315s), the speaker describes the request style
used here: “One request in, an answer out, nothing is carried between the calls.” More precisely,
the chapter's client sends no conversation identifier and the program retains no message history;
each generated response depends only on the messages in that request.

At [5:31](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=331s), the video shows the new `Agent`, its
small read-evaluate-print loop (REPL), and the provider choices. A REPL is a loop that reads input,
evaluates it by calling the program, prints the result, and waits for another input. Reusing the
same `Agent` object makes the command-line interaction look continuous, but in this stage the
object stores only model configuration, not prior turns.

The demonstration at [6:28](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=388s) makes the missing
history visible. The first request tells the model that its name is Gemma. The next request asks its
name, but that second request contains only the question. The model is not being asked to retrieve
stored state; it is receiving a new list that omits the earlier fact. Chapter 2 changes the list
that the harness sends while leaving the model interface unchanged.

## The code

Nine files change at this tag. The runtime path is concentrated in `harness/agent.py` and four
`model/` modules; the other changes package those modules, add tests, and register the offline and
live checks.

### The `Agent` interface

[harness/agent.py](../stages/ch-01-model-only/harness/agent.py) defines the class used by the REPL:

```python
class Agent:
    """A thin, stateless wrapper around a single model call. No memory (yet)."""

    def __init__(self, model: str | None = None, provider: Provider | None = None) -> None:
        self.model = model
        self.provider = provider
        # NO self.messages — ch-01 is stateless; the demo's "watch it forget" depends on this.

    def send(self, user_text: str) -> str:
        """Send one message, return the model's reply. Nothing is carried over."""
        resp = chat(
            [{"role": "user", "content": user_text}],
            model=self.model,
            provider=self.provider,
        )
        return resp.content
```

Python passes the object being operated on as the first method parameter, conventionally named
`self`. The constructor name `__init__` is special: Python calls it after creating an object such as
`Agent()`. The annotation `model: str | None` says that `model` may be either a string or `None`;
`= None` supplies the value used when the caller omits the argument. `provider` works the same way.
The final `-> None` says the constructor does not return a useful value. In contrast,
`send(...)-> str` promises a string result.

The message passed to `chat()` is a list containing one dictionary. `role` identifies who supplied
the message, and `content` contains the text. A call such as `Agent().send("What is 2 + 2?")`
therefore sends one user-role message whose content is that question. The list is a local value in
`send`; it is not assigned to `self`, so it is discarded after the call.

The `main()` function below the class constructs one agent and repeatedly calls `input("you> ")`.
`while True` continues until input raises `EOFError`, normally after Ctrl-D. This is persistence of
the Python process, not persistence of conversation data.

### The package interface and file responsibilities

[model/__init__.py](../stages/ch-01-model-only/model/__init__.py) imports selected names from the
other model modules and lists them in `__all__`. This lets the agent write
`from model import Provider, chat` without knowing which internal files define those names.

The package is divided as follows:

| File | Responsibility |
|---|---|
| `client.py` | Defines the stable `chat()` entry point and selects the fake or HTTP path. |
| `provider.py` | Defines configuration, response data, environment loading, and provider presets. |
| `openai_compatible.py` | Builds an HTTP request and translates its JSON response. |
| `fake.py` | Supplies deterministic responses without HTTP. |
| `__init__.py` | Presents the package's public import surface. |

[pyproject.toml](../stages/ch-01-model-only/pyproject.toml) adds the `agent` console command and
includes `model`, `harness`, and `tasks` in the built wheel. The project is still named `gemma` at
these tags; the upstream rename to Carbon occurred later.

### The `chat()` entry point

[model/client.py](../stages/ch-01-model-only/model/client.py) defines the interface every model call
uses:

```python
def chat(
    messages: list[dict],
    *,
    model: str | None = None,
    tools: list | None = None,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    timeout: float = 180.0,
    provider: Provider | None = None,
) -> LLMResponse:
```

The bare `*` makes every following parameter keyword-only. A caller may write
`chat(messages, max_tokens=200)`, but not `chat(messages, 200)`. Keyword-only parameters make a
call with several numeric and optional settings easier to read and less vulnerable to accidental
argument reordering.

| Parameter | Meaning in this stage | Later use |
|---|---|---|
| `messages` | Ordered dictionaries sent as the conversation input. Chapter 1 supplies one user message. | History grows in chapter 2; instructions and tool messages add more roles later. |
| `model` | Optional per-call model identifier. `None` means to use `provider.model`. | Subagents can select worker models in chapter 11. |
| `tools` | Optional list of tool schemas advertised to the model. It is unused by `Agent` here. | Chapter 5 supplies tool schemas and handles returned calls. |
| `temperature` | A provider decoding setting; lower values generally reduce sampling variation. Zero improves repeatability but does not guarantee identical output on every backend. | Remains a model-call control. |
| `max_tokens` | Upper bound requested for generated tokens, including reasoning tokens on the configured Gemma service. | Compaction requests a smaller bound in chapter 6. |
| `timeout` | Maximum number of seconds the HTTP client waits for this request. | Applies only to the HTTP branch. |
| `provider` | Endpoint configuration or an explicitly supplied responder. `None` loads environment configuration. | The same dependency is passed throughout the later harness. |

The body first evaluates `provider or Provider.from_env()`. If the caller supplied a `Provider`,
that object is used. Otherwise, the environment-based default is created. It then tests
`provider.responder is not None`. A responder takes the fake path; the absence of a responder takes
the HTTP path through `complete_openai()`.

This is *dispatch*: selecting which implementation receives a call. It is a simple two-branch
conditional, not a general plugin system.

### Provider and normalized response data

[model/provider.py](../stages/ch-01-model-only/model/provider.py) defines two dataclasses. A
`@dataclass` decorator asks Python to generate routine methods such as a constructor from the listed
fields. `LLMResponse` is the internal response format:

```python
@dataclass
class LLMResponse:
    content: str
    reasoning: str | None = None
    tool_calls: list = field(default_factory=list)
    usage: dict = field(default_factory=dict)
    finish_reason: str | None = None
    raw: dict = field(default_factory=dict)
```

`content` is required visible text. `reasoning` can hold provider-specific reasoning text.
`tool_calls` is initially an empty list and becomes important in chapter 5. `usage` holds token
counts used by observability in chapter 13. `finish_reason` records why generation stopped, and
`raw` preserves the complete provider JSON for diagnostics. `default_factory` creates a new empty
list or dictionary for every response, avoiding unintended sharing between instances.

`Provider` contains `base_url`, `model`, `api_key`, and an optional callable named `responder`.
Because `responder` is executable behavior, the object is mostly configuration but is not strictly
configuration-only. `Provider.from_env()` reads `.env` and then uses `LLM_BASE_URL`, `LLM_MODEL`,
and `LLM_API_KEY`, falling back to constants in the file. `_load_dotenv()` uses
`os.environ.setdefault`, which preserves a value already present in the process environment.

The preset functions `lmstudio()`, `openrouter()`, `ollama()`, and `openai()` return `Provider`
objects with suitable base URLs and credentials. They do not contact a service. Passing one of
these objects changes the configuration used by `chat()`; all four presets still use the same
OpenAI-compatible HTTP implementation.

### Real HTTP execution trace

[model/openai_compatible.py](../stages/ch-01-model-only/model/openai_compatible.py) implements the
network branch. For `Agent().send("What is 2 + 2?")`, the control and data flow is:

1. `Agent.send()` creates one message: role `user`, content `What is 2 + 2?`.
2. `chat()` receives no explicit provider, so `Provider.from_env()` selects the configured base
   URL, model, and API key.
3. Because that provider's `responder` is `None`, `chat()` calls `complete_openai()`.
4. `complete_openai()` builds a payload containing `model`, `messages`, `temperature`, and
   `max_tokens`. It adds `tools` only when the list is non-empty.
5. `httpx.post()` sends the payload to `{base_url}/chat/completions` with a bearer-token header and
   the configured timeout. `raise_for_status()` turns an unsuccessful HTTP status into an
   exception; this stage does not retry or translate that exception.
6. The function reads `choices[0].message` from the returned JSON and constructs `LLMResponse`.
   Missing visible content becomes an empty string; missing tool calls and usage become empty
   collections.
7. `Agent.send()` returns only `resp.content`, so the REPL prints the visible text and discards the
   remaining response metadata.

This normalization prevents the harness from repeatedly indexing provider JSON. Later harness code
can use named fields on `LLMResponse` instead.

### Fake execution trace

[model/fake.py](../stages/ch-01-model-only/model/fake.py) provides the non-network branch:

```python
def fake(
    *,
    scripted: Callable[[list[dict]], str] | list[str] | None = None,
    default: str = "ok",
) -> Provider:
    """Build a ``Provider`` backed by a deterministic, offline responder."""
    return Provider(
        base_url="fake://local",
        model="fake",
        api_key="x",
        responder=FakeProvider(scripted=scripted, default=default),
    )
```

`Callable[[list[dict]], str]` means a callable that accepts a message list and returns a string.
The vertical bars permit three alternatives: such a callable, a list of strings, or `None`.

For `fake(scripted=["first", "second"])`, `fake()` constructs a normal `Provider` whose
`responder` refers to a `FakeProvider` object. On the first `chat()` call, the responder branch calls
that object. Python invokes its `__call__` method, obtains call index zero from `itertools.count`,
and selects `"first"`. The second call selects `"second"`; later calls use the last list element
again. A callable script instead computes content from the messages, and no script returns the
`default` value. Every path produces `LLMResponse(content=content, finish_reason="stop")`; the
dataclass defaults fill the other fields.

The fake is a **test double**, the general term for code substituted for a production dependency
during testing. More specifically, it is a stateful fake implementation. The episode tests also
use `unittest.mock.patch`, which replaces the name `chat` temporarily and can record how it was
called. Both techniques are useful, but they test different portions of the call path.

### Testing strategy

[tests/episodes/test_ch01.py](../stages/ch-01-model-only/tests/episodes/test_ch01.py) contains three
offline tests:

- `test_send_returns_model_content` replaces `harness.agent.chat` with a controlled test double. It
  checks that `send()` calls it once and returns its `LLMResponse.content`. It does not execute
  `model.client.chat` or either provider branch.
- `test_presets_configure_endpoints` checks the values returned by three preset functions. It does
  not contact those endpoints.
- `test_agent_routes_through_provider` replaces `harness.agent.chat` with a function that records
  the `provider` keyword argument. `seen["provider"] is p` uses Python's identity operator to check
  that the exact object passed to `Agent(provider=p)` reaches `chat()`. This verifies argument
  forwarding; it does not prove that the real `chat()` dispatches or that the endpoint is usable.

Chapter 2 adds `test_agent_runs_offline_through_fake_provider`, which does not patch `chat()` and
therefore exercises the complete agent → client → responder path. Taken together, the tests isolate
small behavior when useful and exercise the integration boundary when it becomes available.

[tasks/verify.py](../stages/ch-01-model-only/tasks/verify.py) is the deterministic gate. It checks
formatting, lint, types, tests, and imports without contacting a model service. The widened mypy
arguments and smoke imports confirm that the new packages can be analyzed and loaded.

[tasks/checks.py](../stages/ch-01-model-only/tasks/checks.py) registers live acceptance checks. One
asks the configured model for `2 + 2`; the other constructs an explicit environment-based
`Provider` and asks for a constrained word. These checks demonstrate a functioning endpoint and
explicit provider forwarding. They do not compare two network protocols or prove that changing
providers can never require adapter work.

## Design decisions & gotchas

**A module-level function is convenient, not uniquely testable.** Importing `chat` into
`harness.agent` gives tests a simple replacement point: patch the name used by the code under test.
An injected client object could also be tested by passing a fake client explicitly. The current
choice minimizes objects and constructor parameters in an educational implementation; its cost is
that each module importing `chat` holds a separate name that must be patched separately.

**The provider object combines configuration and a test strategy.** An alternative would define a
formal provider protocol with separate HTTP and fake implementation classes. This stage instead
uses one optional `responder` field and one conditional. That is compact, but it makes `Provider`
broader than a pure data object and does not yet support selecting among multiple native protocols.

**The interface anticipates later chapters.** `tools`, `tool_calls`, `usage`, `reasoning`, and
`raw` are present before the harness uses them. This avoids changing the call signature when tools
and observability arrive, but it also asks chapter-1 readers to understand fields with no current
behavior. The table above makes those deferred uses explicit rather than treating them as implicit
evidence of a universally “mature” interface.

**Environment defaults are machine-specific.** `DEFAULT_BASE_URL` is a private LAN address. Copy
[.env.example](../stages/ch-01-model-only/.env.example) to `.env` and configure your own endpoint.
The minimal loader does not implement quoting, interpolation, `export` syntax, or searches through
parent directories; it accepts simple `KEY=VALUE` lines from the current directory.

**Failure handling is deliberately minimal.** Network errors, timeouts, unsuccessful status codes,
unexpected JSON, and an empty `choices` list propagate as exceptions. There are no retries or
provider-specific error translations. This keeps the first call path visible but would require
hardening in a production harness.

**Tests preserve capabilities that later stages retain.** The chapter does not assert that the
agent forgets, because chapter 2 intentionally changes that behavior. It does assert that one
`send()` returns model content and forwards configuration—behaviors expected to remain true after
history is added. This is the concrete meaning behind the source comment that tests guard
capabilities rather than temporary limitations.

**Live assertions are intentionally tolerant.** The prompts request constrained output, while the
checks use substring matching. This accommodates model variation, but it can admit false positives.
Live-model acceptance provides different evidence from deterministic tests and should not replace
exact offline assertions.

## Study pointers

Read the stage in this order:

1. [harness/agent.py](../stages/ch-01-model-only/harness/agent.py) — trace the one message created by
   `send()` and notice which values are stored on `self`.
2. [model/client.py](../stages/ch-01-model-only/model/client.py) — identify the defaulting expression
   and the two dispatch branches.
3. [model/provider.py](../stages/ch-01-model-only/model/provider.py) — separate response fields,
   provider fields, environment loading, and presets.
4. [model/openai_compatible.py](../stages/ch-01-model-only/model/openai_compatible.py) — follow the
   transformation from Python arguments to HTTP JSON and back to `LLMResponse`.
5. [model/fake.py](../stages/ch-01-model-only/model/fake.py) — compare callable, list, and default
   response selection.
6. [tests/episodes/test_ch01.py](../stages/ch-01-model-only/tests/episodes/test_ch01.py) — for each
   test, state which production functions run and which are replaced.
7. [tasks/verify.py](../stages/ch-01-model-only/tasks/verify.py) and
   [tasks/checks.py](../stages/ch-01-model-only/tasks/checks.py) — compare deterministic evidence
   with live-model evidence.

For a fully offline exercise, construct `Agent(provider=fake(scripted=["first", "second"]))` in a
Python shell and call `send()` three times. Predict each result before running it, then explain why
the messages do not affect list-script selection. Next use a callable script that returns
`messages[0]["content"]` and observe that the fake can inspect the same message structure an HTTP
provider would receive.

The REPL, demo, and live acceptance require an OpenAI-compatible endpoint. After configuring
`.env`, run `uv run agent` and repeat the two-turn forgetting demonstration, then compare `uv run
verify` with `uv run accept ch-01` and identify which commands contact the endpoint.

Previous: [Chapter 0 — What is an agent?](ch-00-what-is-an-agent.md) · Next:
[Chapter 2 — History](ch-02-history.md), where the harness retains and resends conversation data.
