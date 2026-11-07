# Lecture 2 Notes — From LLM to Agent: the Loop, System Prompts, Tool Calls

> Agentic Software Engineering · Week 1, second meeting
>
> **The one idea:** an agent is an LLM in a while-loop with tools.  The difference between 
> a Chat Bot and a Coding Agent is the harness, not the model.  You will demonstrate 
> that yourself in Exercise 4 when you convert a toy chat bot into a toy coding agent.

## 1. Connecting to the previous lecture

Last time we established that an LLM is *stateless* -- it just takes in a string and outputs a string.  Given this, if we have a two-hour long chat session with a chat bot, where does bot's memory live?  The answer: in a **messages list** — an ordinary array,
maintained by ordinary software, replayed into the model on every call. That software
is the **harness**.  We can get different types of behavior from a model by changing the harness.  

- **A chat app** (ChatGPT, Claude.ai) maintains the messages list and displays the
  replies. The model *answers*.
- **A completion tool** (Copilot's original mode) stuffs surrounding code into the
  context and asks for the next few tokens. The model *completes*.
- **An agent** (Claude Code, Codex CLI, and the toy you will build in week 3) gives
  the model *tools* (e.g., for reading/writing files) and *user messages*, the model
  produces response messages and *sends tool requests*  (e.g., read this file, run this command), the harness executes the commands, and sends the results back to the model.
  Together, the harness and the model become an *actor*.

Same LLM-concept (just a predictor, a generator of plausible output text in response to input text) is used in all three. What changes is what the surrounding software (the harness)
-- the harness changes what the predictor can effectively do.

## 2. The agent loop

Here is the entire architecture of a coding agent, in pseudocode you will implement
nearly verbatim in Exercise 4:


```python
messages = [{"role": "user", "content": task}]
while True:
    # send to the model a string combining the system prompt, message history,
    #  ..and list of available tools
    response = model(system=SYSTEM_PROMPT, messages=messages, tools=TOOLS)
    # add the model's reponse to the message history
    messages.append(assistant_message(response))
    if response.stop_reason != "tool_use":
        break                                  # the model is done acting
    # carry out all tool calls that the model requests  
    results = [execute(call) for call in response.tool_calls]
    #  add the tool call results to the message history
    messages.append(tool_results(results))     # results go back INTO the context
```

**Message roles.** The conversation is a typed list. A **system** message carries
standing instructions (more below). **User** messages carry your requests — and, by
convention of the API, tool results too. **Assistant** messages carry the model's
replies, including its requests to use tools. The model sees the whole typed list
every call; the roles tell it who said what.

Here is what the list actually looks like a few turns into a real task (condensed):

```
system:     You are a coding agent. Work only inside the working directory. …
user:       "Fix the failing test in this project."
assistant:  [tool_use: list_dir(".")]
user:       [tool_result: "cart.py  discount.py  test_checkout.py"]
assistant:  [tool_use: read_file("test_checkout.py")]
user:       [tool_result: "def test_discount_applied_over_threshold(): …"]
assistant:  "The test expects a discount above the threshold. Let me check
             the implementation."  [tool_use: read_file("discount.py")]
```

Notice two things: the tool results ride in **user**-role messages (the harness is
"speaking" on your behalf), and the list only ever grows — every call re-sends all of
it, which is Lecture 1's statelessness in action.

**Termination.** The loop ends when the model responds *without* requesting a tool —
the model itself decides when it has enough to answer. (Your own agent will also want
a hard iteration cap. Unbounded autonomy is a bug, not a feature; you'll feel why by
Lecture 6.)

**Errors are just results.** If a tool fails — file not found, command rejected — the
error text goes back into the context like any other result, and the model reads it
and adjusts. In other words, the text you choose to include in the
error text is not a neutral log or debugging remark; it is
a control input -- it influences upcoming behaviors of the model and
impacts its ability to recover.   Typically, you need to abstract the
low-level (potentially voluminous) technical output of the failed tool
call into a crisp and informative diagnosis that enables the model to
be decisions about how to recover.

A well-built agent *recovers* from tool errors for the same reason it can
do anything else: the failure message became part of the prompt. Concretely:

```
assistant:  [tool_use: read_file("game.py")]
user:       [tool_result: "ERROR: file not found: game.py —
             directory contains: cart.py, discount.py, test_checkout.py"]
assistant:  "There is no game.py here; the logic must be in discount.py."
            [tool_use: read_file("discount.py")]
```

Nobody wrote recovery logic. The error message is just more context, and a helpful
error message (one that lists what *does* exist) is a prompt that steers the next
prediction. You will feel this personally in Exercise 4: agents with terse error
strings flail; agents with informative ones self-correct.

## 3. Tool calling, mechanically

How do we tell the model about available tools?  We give it some meta-data (in JSON format).There are various protocols for telling models about tools, but they all have 
the following commonalities.  Each tool is described by 
 - a unique name
 - a description, which the model gets as part of its text/context input to help it 
   understand the situations in which the tool could be applied
 - information about how the model should format the parameters when requesting 
   a tool use.  

Here is the meta-data for an example tool, using the Anthropic Messages API format:

```json
{
  "name": "read_file",
  "description": "Read a file from the working directory and return its contents as text. Use this before proposing any edit.",
  "input_schema": {
    "type": "object",
    "properties": {
      "path": {"type": "string", "description": "Path relative to the working directory"}
    },
    "required": ["path"]
  }
}
```

When the model decides it wants the tool to be called, in addition to any conventional text response that it sends the user, it also sends back a JSON formatted data requesting the tool call.   For example, the JSON below indicates that the message being exchanged between the model and the harness is coming from the model (the `assistant`).  The message has two parts:
 - the `text` part is a "conventional" text message back to the user
 - the `tool_use` part is the request for the tool call, formatted according to tool schemas like the one above.

```json
{
  "role": "assistant",
  "content": [
    {"type": "text", "text": "Let me look at the game logic first."},
    {"type": "tool_use", "id": "toolu_01A9...", "name": "read_file",
     "input": {"path": "game.py"}}
  ]
}
```

And the harness — *your code, not the model* — executes the read and sends back the following. This time, the `role` indicates that this is a message originating with the user (actually, the harness in this case).  The type of the message is a `tool_result` -- that 
output that a tool produced.

```json
{
  "role": "user",
  "content": [
    {"type": "tool_result", "tool_use_id": "toolu_01A9...",
     "content": "BOARD_SIZE = 9\nWIN_LENGTH = 5\n..."}
  ]
}
```

Here are some key points:

1. **The model never executes anything.** It emits a *request* for a tool use, 
   shaped by a tool use schema.
   The harness decides whether and how to honor it.  For example, based on the 
   configured security settings for the harness, the harness may decide not to execute 
   the tool call because it is an access a file that the user hasn't granted permission to.
   In general, every safety property an agent has
   — permission prompts, sandboxes, allowlists — lives on the harness side of that
   line. When Claude Code asks "may I run `pytest`?", that is the harness talking.
2. **The tool description is prompt text.** The model chooses tools by *reading their
   descriptions*. A vague or misleading description produces vague or misleading tool
   use, exactly as a vague instruction does. When you write tools in Exercise 4, write
   the descriptions like you're instructing a new colleague.
3. **The `id` matters.** Each `tool_result` answers a specific `tool_use` by id. Pair
   them, don't zip them — mismatched ids are the classic first bug in a hand-rolled
   agent.

## 4. System prompts: same model, different soul

The **system prompt** is the standing instruction block that rides at the front of
every call, before the conversation. It typically establishes identity ("you are a
coding assistant operating in a repository"), an inventory of behavioral rules (read
before editing; prefer small diffs; ask before destructive operations), conventions
for output, and safety boundaries.

Its power is hard to overstate. The *same model* and *same weights* 
behave like a cautious code reviewer, a chatty tutor, or a terse batch tool 
depending on this one block of text —
same model, different soul. Give the identical request — *"add save/load to this
game"* — to the same model under two different system prompts:

> **System prompt A:** "You are a meticulous code reviewer. Never modify files.
> Report risks and design questions as a numbered list with file:line references."
>
> → replies with a list: where game state lives, what serialization format questions
> need answering, which functions would need touching — and changes nothing.

> **System prompt B:** "You are a rapid prototyper. Prefer working code now over
> polish; stub what you must and mark every stub with TODO."
>
> → starts editing immediately and produces a working-but-rough `save_game()` with
> two TODOs.

Neither is wrong; they are different *tools* built from the same model. When your
Exercise 4 agent behaves oddly, the first place to look is the system prompt you
wrote — and in class we demonstrate this by running the toy agent with a strong and
then a deliberately weakened system prompt and watching the behavior visibly degrade.

One preview for Lecture 3: Claude Code lets *you* extend its standing instructions
per-project through a file called `CLAUDE.md`. Once you see the system prompt clearly,
CLAUDE.md is obvious: it is user-space system prompting.


## 5. The demo: watching the loop breathe

In class the instructor runs a ~200-line Python agent — the same one you will build —
on a trivial task, with every API request and response printed raw to the terminal.
You watch the messages list grow turn by turn: the user task; an assistant `tool_use`
block; a `tool_result`; another `tool_use`; and eventually an assistant message with
`stop_reason` of `end_turn`, at which point the loop exits and the task is done.

Two things to notice when you watch (or re-watch the recording):

- The whole conversation is re-sent on every call — you can *see* the request bodies
  getting longer. File that observation away; it becomes money in Lecture 6.
- Nothing arrives anywhere by a hidden channel. Everything the model "knows" scrolled
  past you in plain JSON. This transparency is what makes agents *debuggable*: the
  context is the complete explanation of the behavior.


## 6. Workflows, agents, and where Claude Code sits

Anthropic's essay *Building Effective Agents* (this week's core reading) draws a
distinction the industry has largely adopted:

- **Workflows** are systems where LLMs and tools are orchestrated through
  *predefined code paths* — a fixed chain of prompts, a router, a
  generate-then-critique pair. The developer decides the control flow.
- **Agents** are systems where the LLM *dynamically directs its own process and tool
  usage*. The loop above is the minimal agent: the model decides what to read, what
  to run, when to stop.

The same job can be built either way, and the contrast makes the definition concrete.
A commit-message helper as a **workflow**: step 1, always run `git diff`; step 2,
always ask the model to summarize the diff; step 3, always ask it to draft a message
in the team's format. The model fills in blanks, but the developer wrote the three
steps, and they run in that order every time. The same helper as an **agent**: "write
a commit message for the staged changes" plus tools — and the *model* decides to run
the diff, notices a failing pre-commit hook, reads the hook's config to understand
why, and only then writes the message. More capable, less predictable, harder to
bound — which is exactly the essay's point about choosing the simplest thing that
works.

The essay's central advice is worth quoting in spirit: *use the simplest thing that
works.* Workflows are more predictable and cheaper; agents are more flexible and
harder to bound. Claude Code sits firmly on the agent side — the model chooses its own
next action — but wrapped in strong harness guardrails: permission prompts, a plan
mode that separates thinking from doing, and configurable rules.

The academic lineage runs through **ReAct** (Yao et al., ICLR 2023), which
demonstrated that interleaving *reasoning* text with *actions* outperforms either
alone. Every "let me look at the game logic first" you saw in the demo is that idea in
production.

## 7. Exercise 1 launches

Your first exercise involves no installation and no API key: you will read the
complete transcript of a real multi-session Claude Code project (a small game built
over seven sessions) plus excerpts from two later attempts to scale it, and you will
critique the *human's* performance — where they steered well, where vagueness cost
rework, and how two different disciplines announce themselves in the very first prompt
of a session. The vocabulary from today — loop, roles, tool calls, system prompt — is
your reading lens. The spec is in the exercises folder; the transcripts are in the
handouts.

## Questions to think about

1. What can a tool-calling loop do that fine-tuning a model never could? (Consider:
   your codebase changed this morning.)
2. Where exactly should a harness refuse to do what the model asks? Name a tool call
   you would never auto-approve.
3. Tool descriptions are English the model reads. What happens if a description is
   subtly wrong — and who would notice?

## Before next lecture
- **Required:** The Carbon Layer - YouTube Channel - *[Harness Engineering Masterclass: Technical Deep Dive on how to build Agentic Systems](https://youtu.be/mQfTdNVCOB0?si=zZmykXWn-mVEo3Pk)* — up to timestamp 14:00 is good enough for preparing for L03.  This is Week 1-3 core reference (our toy agent will address the first several "primitives" (building blocks) for a coding agent that are introduced in the video. 
- **Required:** Anthropic API docs, [*Tool use*](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — a skim now to recognize the shapes;
  you will return for depth before Exercise 4.
- **Recommended:** Yao et al., *ReAct*, §1–3.
- **Logistics:** install Claude Code and authenticate with your Claude Pro account
  before next lecture; the install handout has the steps.
- **Exercise 1** (transcript critique) is due before Lecture 4.
