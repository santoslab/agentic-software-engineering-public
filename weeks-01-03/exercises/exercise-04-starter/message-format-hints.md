# Message JSON format used by `toy_agent.py`

`toy_agent.py` uses the **OpenAI-compatible Chat Completions format**. Its URL
ends in `/v1/chat/completions`, and its request and response structures match
the OpenAI Chat Completions API.

The endpoint in this exercise is hosted by **OpenCode Zen**, and the selected
model is `mimo-v2.5-free`. Thus, it uses OpenAI's *format*, but it is not calling
an OpenAI-hosted model.

This exercise does **not** use OpenAI's newer Responses API. The two APIs use
different structures; do not mix Responses API `input`/`output` items into the
`messages` list described here.

## Overall request body

Each call sends one JSON object containing a model name, the conversation so
far, and the available tools:

```json
{
  "model": "mimo-v2.5-free",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful coding assistant."
    },
    {
      "role": "user",
      "content": "Read checkout.py"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "read_file",
        "description": "Get the full contents of a file",
        "parameters": {
          "type": "object",
          "properties": {
            "file_name": {
              "type": "string",
              "description": "The path of the file to read"
            }
          },
          "required": ["file_name"]
        }
      }
    }
  ]
}
```

`messages` is the history of all messages exchanged with the model.  Each message is labelled according to its `role` as follows:
- `system` - the system prompt
- `user` - messages created by the user (`user`) as part of the conversation, 
- `assistant` (not illustrated) - previous messages received from model. The model has no history itself so we have to remind it what it said earlier. `assistant` messages also include what tool requests the model made.
- `tool` (not illustrated) - the result of one tool call that the harness made in response to a request by the model.  Each tool call as an individual response entry in the message list.

`tools` -  also tells the model what tools are currently available for the harness to call.  
The real program includes all three entries from `TOOLS_SCHEMA`, not just the
one representative tool shown above. Python dictionaries and lists are
converted to JSON by `requests.post(..., json=...)`.

## Objects in the `messages` array

Here's a table-based summary of the concepts above.

`messages` is the ordered conversation history. Each object has a `role` that
determines its remaining fields.

| Role | Created by | Purpose | Fields used here |
|---|---|---|---|
| `system` | Harness | Instructions that govern the assistant | `role`, `content` |
| `user` | Harness | A user's request | `role`, `content` |
| `assistant` | Model | Text and/or requests to call tools | `role`, `content`, optionally `tool_calls` |
| `tool` | Harness | The result of one requested tool call | `role`, `tool_call_id`, `content` |

Examples of ordinary messages are:

```json
{"role": "system", "content": "You are a helpful coding assistant."}
```

```json
{"role": "user", "content": "Which files are available?"}
```

```json
{"role": "assistant", "content": "The sandbox contains checkout.py."}
```

The complete history is sent again on every model call. The service does not
otherwise know what happened in earlier iterations of this program.

## Tool definitions

The top-level `tools` array describes functions the model is allowed to
request. It does not give the model direct access to the Python functions; it only tells the model what tools are available for the harness to call and report back on.

Each definition has this shape:

```json
{
  "type": "function",
  "function": {
    "name": "function_name",
    "description": "When and why to use this function",
    "parameters": {
      "type": "object",
      "properties": {
        "argument_name": {
          "type": "string",
          "description": "What this argument means"
        }
      },
      "required": ["argument_name"]
    }
  }
}
```

`parameters` is a [JSON Schema](https://json-schema.org/) describing the
argument object. Names and descriptions are prompt text: they help the model
decide which function to request and which arguments to supply.

The Python program separately maps each advertised name to executable code in
`TOOLS_DICTIONARY`. A schema alone never runs a function.

## HTTP response and the assistant message

The service returns a Chat Completion response envelope resembling:

```json
{
  "id": "chatcmpl-example",
  "object": "chat.completion",
  "created": 1770000000,
  "model": "mimo-v2.5-free",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "How can I help?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 5,
    "total_tokens": 30
  }
}
```

Providers may include additional fields. The toy agent ignores almost all of the envelope: `call_zen` returns the `messages` portion of the response which we can access in Python code as follows.

```python
payload["choices"][0]["message"]
```

That inner message is appended to `messages`.

## Tool-call round trip

Tool use is a conversation between the model and the harness:

1. The harness sends the message history and tool definitions.
2. The model returns an assistant message containing `tool_calls` (0 or more tool calls it wants the harness to make for it - each has a unique ID).
3. The harness parses the arguments and runs the corresponding Python code.
4. The harness appends a `tool` result message with an ID that matching call ID.
5. The enlarged history is sent to the model again.
6. The model may request more tools or return its final text.

For example, the model may return this inner assistant message:

```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_123",
      "type": "function",
      "function": {
        "name": "read_file",
        "arguments": "{\"file_name\":\"checkout.py\"}"
      }
    }
  ]
}
```

Important: `function.arguments` is a **string containing JSON**, rather than a
JSON object nested directly at that position. The program turns it into a
Python dictionary with:

```python
arguments = json.loads(tool_call["function"]["arguments"])
```

It then invokes the selected function using `**arguments`.

After executing the function, the harness appends a matching result:

```json
{
  "role": "tool",
  "tool_call_id": "call_123",
  "content": "def calculate_total(...):\n    ..."
}
```

`tool_call_id` must equal the `id` in the model's request. This association is
especially important because one assistant message may request multiple tools.
The harness adds one `tool` message for each call.

The next request therefore contains this order inside `messages`:

```json
[
  {"role": "system", "content": "You are a helpful coding assistant."},
  {"role": "user", "content": "Read checkout.py"},
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_123",
        "type": "function",
        "function": {
          "name": "read_file",
          "arguments": "{\"file_name\":\"checkout.py\"}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "tool_call_id": "call_123",
    "content": "def calculate_total(...):\n    ..."
  }
]
```

The assistant tool-call message must remain in the history; sending only the
tool result would lose the request that the result answers.

## Details worth remembering

- `content` is ordinary text in this exercise, including for tool results.
- An assistant message may have text, tool calls, or both. Its `content` is
  commonly `null` when it only requests tools.
- A model proposes tool calls; the harness validates and executes them.
- Tool names and arguments are model output and must be treated as untrusted.
  This program checks known names, catches exceptions, and confines file paths
  to `sandbox/`.
- The agentic loop stops when an assistant message has no `tool_calls`.
- The exercise uses non-streaming responses, so it receives complete message
  objects instead of partial streaming chunks.

## Official references

- [Create a Chat Completion](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling)

