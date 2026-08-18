
# Not quite node yet, just a draft

# Exercise 4 — Build a Toy Coding Agent

> **Assigned:** Lecture 05 · **Due:** start of week 4 · **Effort:** 3–4 hours
>
> **Requires:** Python 3.11+ and the `requests` package. — see "Model access" below.
>
> **Starter code:** [`exercise-04-starter/`](./exercise-04-starter/) — a bare chat bot
> (`toy_agent.py`) that Part 1 walks you through turning into an agent, plus the
> micro-task B seed project.

## Goal

Demystify the harness by building one: a working coding agent in roughly 200 lines of
Python against a hosted LLM API. When you're done, you will be able understand most
Claude Code features as "what I did in my toy implementation, but with more engineering".
That is, your toy example will help you understand each of the core features in Claude Code.
You'll also be able to understand, even with your simple toy agent, how coding agents
enforce basic safety features. 

Note that part of the exercise is to reflect on your observations of how your agent behaves and to note
"interesting things" that you observed.  So be thinking about this as you work.

## Overview of Different Parts

- Part 1: The exercise description will walk you through how to take the given code
that implements a chat bot and turn it into a simple coding agent.
- Part 2: You'll apply your agent to some very simple development "micro-tasks"
- Part 3: You'll write up a summary of your experiences in the exercise 

## Model access (read first)

Here is some technical background on the backend models that we will use.
You don't need to understand the details of all of this, but you need to be 
somewhat aware of this issues (which you can research more about yourself).
Bottom line: for this assignmnet, if you just start with the code we give you
and don't make any adjustments on your own, you don't have to worry about the 
issues below.

Your toy agent will use a free model on **OpenCode Zen** (<https://opencode.ai/docs/zen>),
an OpenAI-compatible endpoint at `https://opencode.ai/zen/v1/chat/completions`.

- **No key required.**  You won't need an authorization key to use OpenCode Zen, 
  and trying to use one (even a "placeholder" key) will actually cause problems.
  If you just use the code as we have supplied, everything will work fine.
  The free tier accepts a request with no `Authorization` header at
  all. Counter-intuitively, sending a *placeholder* key is worse than sending none — a
  fake value earns a `401 Invalid API key`. If you happen to already have a key, 
  only then should you a header with the real key.
  Moreover, if you use a key, read it from an environment variable. **Never commit a key.**
- **The free lineup rotates**, roughly monthly. List the current one with:
  ```
  curl -s https://opencode.ai/zen/v1/models | python -m json.tool
  ```
  Known-good at the time of writing of this assignment are: 
  `mimo-v2.5-free`, `north-mini-code-free`,
  `ling-3.0-flash-free`, `nemotron-3-ultra-free`, `laguna-s-2.1-free`.
- **Avoid the DeepSeek-family *thinking* models** (e.g. `big-pickle`,
  `deepseek-v4-flash-free`) for this exercise. They require each assistant message's
  `reasoning_content` field to be echoed back verbatim, and will 400 if you rebuild a
  "clean" message dict.
- **Free tiers are best-effort infrastructure.** Some routes fail a large fraction of
  calls with a 5xx, and in an agentic loop a *single* failure kills the whole run. If a
  run dies, switch models before you start debugging your payload.
- **Caps in code, not intentions:** nothing here bills you, so there's no spend to cap —
  but a runaway loop still costs wall-clock time and produces an unreadable log. Set a
  hard iteration limit (e.g., 25 loop turns). If your agent is still going after 25
  turns, stop and ask what's looping. On a paid API this same limit is what stands
  between a bug and a bill.

## Format of Messages between Harness and Model

There are different standards for exchanging information between the harness (i.e., your 
toy agent) and a model.  This exercise uses an older API format from OpenAI called the 
"Chat Completions" format.  Although the concepts are similar, this is slightly different
that the format used by Claude or the most recent Open AI models.

The starter files for the exercise provide a summary of the message formats in the file
`message-format-hints.md`.

## Safety rules (graded elements, not suggestions)

Here are some safety rules that you need to enforce as you build your agent.

1. **Jail all file operations** to a scratch directory: resolve every path and verify
   it's under the sandbox root *before* touching the filesystem (the provided code will give
   you some direction about how to do that).
2. If you implement `run_command`: **hard allowlist** (e.g., `["python", "pytest"]`,
   exact-match on the executable), no shell interpolation of model output — pass an
   argument list, never a string through a shell.
3. Hard iteration limit on the loop (no unbounded autonomy) -- we'll also show you
   how to do that.

## Task

### Part 1 — chat bot to agent, in nine steps

You are given a **chat bot**, not an agent:
[`exercise-04-starter/toy_agent.py`](./exercise-04-starter/toy_agent.py) is ~50 lines
that POST your messages to a model and print the reply. It has no tools, no loop, and no
safety properties. You will add those, one step at a time, until it is an agent of
roughly 200 lines.

The starter carries **no comments** on purpose. The explanation of each piece lives in
the step below that gives it to you — read the step, then write the code.

| # | Step | Who writes it |
|---|------|---------------|
| 1 | Run the chat bot you were given | — |
| 2 | Play with, then write, the system prompt | you |
| 3 | Add the sandbox jail | given |
| 4 | Add your first tool | given |
| 5 | Declare the tool to the model | given |
| 6 | Grow the single call into the agentic loop | given |
| 7 | Bound the loop (`MAX_TURNS`) | you (**graded**) |
| 8 | Add the rest of your tools (≥3 total, `run_command` optional) | you |
| 9 | Add `--verbose` | you |

Steps 3–6 are given in full because a subtly wrong jail or a half-answered tool call
fails in ways that are miserable to debug and easy to not notice. What is left to you is
the part the exercise is actually about: the prompt, the tools, the ceiling on autonomy,
and the evidence that the jail holds.

---

#### Step 1 — Run the chat bot you were given

```
pip install requests
python toy_agent.py
```

Talk to it. Confirm you get replies before you change anything — if the route is having a
bad day (see *Model access* above), you want to know that now and not after five edits.

One thing to notice while you chat: `messages` is the *entire* state of the program, and
the whole list is re-sent on every call. Nothing is remembered on the server. Each turn
therefore costs more than the last, and that growth is what you'll be asked about in
Part 3.

#### Step 2 — Write the system prompt

**First, experiment with different styles.** Sometimes it can be difficult to see how
the system prompt effects the model's output. Try adding lines or phrases that are
stylistic and fun instead of strictly productive. Here are some ideas to start:

- End all of your responses with 'Go Cats!'
- Always output in Rhymed Couplets
- Talk like a 17th century Pirate
- reference as many facts about australia or it's wildlife as possible

**Now write the real one.** Now write a real system prompt that determines
how you want the agent to behave (you can adapt this as you continue the exercise).
At minimum it should establish who the agent is, that it only ever touches its
working directory, that it reads a file before editing it, that it keeps calling tools
until the task is done, and what it should say when it stops.

```python
SYSTEM = """You are ...

Follow these rules while working.
- Always read a file before you write or edit it.
- ...
"""
```

#### Step 3 — Add the sandbox jail (code given)

We'll now add a sandbox jail (and in the following step, our first tools).  You won't be 
able to test the sandbox mechanism until the tools are added.

Here is the main point, in our simple notion of a sandbox, everything your agent 
can touch has to live in one directory.   A real coding agent has a much more 
sophisticated approach, but from this addition to our toy agent, we can understand 
the principle. 

To provide the basic infrastructure for the "one directory sandboxing", 
add this code after the declaration of your system prompt.

```python
# ------ Sandboxing --------

from pathlib import Path

# Create a `sandbox` sub-directory (if it does not already exist) 
# in the directory from which the agent code was launched

SANDBOX_DIR = (Path(__file__).resolve().parent / "sandbox").resolve()
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)

# Helper function to make sure that paths to be used in tool calls
# lie within the sandbox.

def resolve_in_sandbox(file_name: str) -> Path:
    resolved = (SANDBOX_DIR / file_name).resolve()
    if not resolved.is_relative_to(SANDBOX_DIR):
        raise ValueError(f"path escapes the sandbox: {file_name}")
    return resolved
```

[TODO: Clarify and expand this explanation.  First explain the Python code.
Then, expand the three bulleted below (that give the implications of the code)
and explain things more simply and in greater detail.]

Three things this code is doing, none of them obvious:

- **It anchors to the file, not the working directory.** A CWD-relative sandbox plus
  `mkdir(parents=True)` fails *silently*: run the script from the wrong place and it
  quietly creates a second, empty sandbox there instead of erroring.
- **It resolves first and prefix-checks second.** A raw join confines nothing —
  `SANDBOX_DIR / "../../x"` walks straight out, and on Windows an absolute component
  like `"C:/Windows/Temp/x"` discards `SANDBOX_DIR` entirely. Resolving before checking
  is what makes both fail closed.
- **It raises, and that's fine.** The `ValueError` needs no handler of its own; step 6's
  blanket `except` turns it into a string the model reads and recovers from.

When we add the capability for our agent to use tools to interact with the file system,
we will want to always uses the helper function above to make sure that *every* such 
uses the helper function above to enforce that all reads/writes only happen within the 
sandbox.  We are in some sense "jailing" the agent.  However, a jail with a single unguarded
path is not a jail — we need to make sure that every file system tool call is confined to the jail.
That is what the concluding exercise checklist means by "demonstrably present."

With the addition above, re-run the toy agent to see that it creates the sandbox subdirectory.

#### Step 4 — Add your first tool (code given)

A tool is an ordinary Python function. This one is the worked example; the rest are
yours in step 8.

```python
# ------ Tools --------

def read_file(file_name: str) -> str:
    path = resolve_in_sandbox(file_name)
    if not path.is_file():
        return f"ERROR: file not found: {file_name}"
    return path.read_text()
```

Two things to copy from it into every tool you write later.

**It goes through the jail, first line.** No filesystem tool touches a path that
`resolve_in_sandbox` hasn't cleared.

**It fails with words, not silence.** Returning `""` for a missing file would make a
missing file and an empty file indistinguishable to the model, which is how tool-retry
loops start. Even this error string is thin.  The concept to start learning here is that, 
when incorporating tools into your agent harness, having the tool provide informative 
responses (on both success and failure) can help the harness performance.

Often, you want to improve your tool call information as you are building out a harness.
To simulate that activity, once you have a `list_files` tool in
step 8, come back and append the directory contents to it:

```python
        return f"ERROR: file not found: {file_name} - directory contains: {list_files()}"
```

That is the difference between the model recovering in one turn and guessing at
filenames for three. Write every error string as though a colleague has to act on it
with no other context — because that is exactly the situation the model is in.

Once your agent has tools and a loop, prove it holds: ask it, in plain English, to read
`../../secrets.txt` and to write `C:/Windows/Temp/pwned.txt`. Both must come back as the
`path escapes the sandbox` error, and the model should shrug and carry on rather than
the program crashing. Keep that exchange in a verbose log — it's the easiest way to
satisfy the checklist.


#### Step 5 — Declare the tool to the model (given)

Remember, the model can't execute tools directly -- it can only return text.
And the model can't see your Python, so not only does it not have the ability 
to call `read_file` tool directly, it doesn't even know that tool capability is 
there.

You need to provide meta data to the model in a some format (the formal varies based
on the protocol being used to speak to the model) so that it knows
 - the tool exists
 - what the purpose of the tool is (what it does)
 - how to format text output back to the harness to indicate that the tool
   should be called (and with what parameters, etc.)

Zen speaks the OpenAI `chat.completions` format, so we need to inform it about our
`read_file` tool by declaring metadata (specifically, a schema written in JSON 
that describes the format of interactions with `read_file`).  
We'll also set up a data structure (the `TOOLS_DICTIONARY`) to hold
all the tool schemas that our harness supports, and that dictionary 
will name the string name of the tool in the schema to the actual python
function that implements the tool. 

```python
READ_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Get the full contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string", "description": "The path of the file to read"},
            },
            "required": ["file_name"],
        },
    },
}

TOOLS_DICTIONARY = {"read_file": read_file}     # name -> function, for the loop to dispatch
TOOLS_SCHEMA = [READ_FILE_SCHEMA]               # what actually gets sent to the model
```

[TODO: The following paragraph is unclear.  Explain it better.  What are the "two halves"?]
Two registries, because the two halves travel separately: the schema list goes over the
wire, the dictionary stays home and executes. Every tool you add in step 8 goes in
**both** — forgetting the second is the most common way a new tool silently never gets
called.

Recognize something important: the `description` field is **prompt text, not documentation** — 
it provides info to enable the model to decide which tool to reach for. 
Remember Lecture 02 and write `description fields` like you're instructing a colleague.

Now, we need to extend the call to the model to pass along information about our tools
(as specified in the `TOOLS_SCHEMA`).  Note that you need to both add the `tools` parameter
to the arguments and then also add a new JSON key "tools" and the associated tool list
in the message that gets sent to the model.

```python
def call_zen(messages: list, tools: list) -> dict:
    ...
        json={"model": MODEL, "messages": messages, "tools": tools},
```

Now, toward the end of the code where `call_zen` is called, add the tool schema as an 
argument to the call

```python
message = call_zen(messages,TOOLS_SCHEMA)
```

Now test this new addition.  Put a file, e.g., `test_file.txt` in `sandbox/` with some simple content.
Run your agent, and ask the agent to read it, e.g, say "Read the file test_file.txt"

The reply will come back *empty*, because the model asked for a tool call and nobody executed it.
That is, the model probably realized that our registered `read_file` tool should be called, and sent 
back info on how to make the tool call, but requested tool call info is stored in a different field in `message` (the only field that we are utilizing now to echo back to the user is the `content` field).
And, there is nothing in the harness to look at the model's requests for tool actions and execute them.

In the following step, will add the necessary machinery to process tool calls coming back from 
the model.

#### Step 6 — Grow the single call into the agentic loop (given)

This step is the heart of the exercise. 

Add the following code to your agent.   That that the model call gets moved out of the REPL and into a
this new `agentic_loop` function that keeps going while the model keeps asking for tools:

```python
# -----  Agentic loop -----
import json


def agentic_loop(messages: list) -> None:
    while True:
        # given the current message history and tool list to the model
        message = call_zen(messages, TOOLS_SCHEMA)
        # add the message returned from the model to the message history
        messages.append(message)
        # if the returned message contain a user message, then print it
        if message.get("content"):
            print(message["content"])

        # get the tool calls proposed by the model
        tool_calls = message.get("tool_calls")
        if not tool_calls:
            break # exit the loop if there are no tool calls

        # for each tool call
        for tc in tool_calls:
            # look up the name of the function representing the tool call
            name = tc["function"]["name"]
            # get the argument the model has proposed for the tool call
            raw_arguments = tc["function"].get("arguments") or "{}"

            # if the model has proposed a tool that is not in our available tools, then
            # prepare an informative error message indicate what tools are available
            if name not in TOOLS_DICTIONARY:
                result = f"ERROR: unknown tool: {name} - available: {list(TOOLS_DICTIONARY)}"
            else:
                try:
                    # make the tool call
                    result = TOOLS_DICTIONARY[name](**json.loads(raw_arguments))
                except Exception as e:
                    result = f"ERROR: {name} failed: {type(e).__name__}: {e}"
            # add the result of the tool call (or the constructed error message) to the message history
            # to become part of the context for future calls.
            messages.append({"role": "tool", "tool_call_id": tc["id"], "content": str(result)})
```

Now update the model interaction portion of the REPL body -- it shrinks to one call 
of the agentic loop defined above. 

```python
        # model interaction
        agentic_loop(messages)
```

Here are four key rules about using the model API that that we need to be careful about.
These are reflected in the code above.  If we didn't following these rules, we would end
up with a bug somewhere.

[TODO: explain these bullet points in greater detail and use simple and direct language.]
- **Append the response dict unmodified.** Don't rebuild a "clean" message — thinking
  models require their `reasoning_content` echoed back verbatim and will 400 if it's gone.
- **Nothing in the dispatch block may raise.** Bad JSON, wrong keyword arguments, a jail
  violation, a hallucinated tool name — each becomes a string the model can read and act
  on. An exception escaping here kills the session.
- **Every `tool_call` gets answered** — including calls to tool names you don't
  recognize. A dangling call in the history 400s the next request.
- **Pair results by `tool_call_id`, never by index.** A model may request several tools
  in one turn, and the results are matched by id.

The agent loop exits when the model returns a message with no `tool_calls` — that is the model
deciding it's finished.  Note: sometimes the model might not do this, and we'll need to guard
against this problem (i.e., the model continuing to interact with tools too long) in the next step.

Now run the updated agent, and try to get the agent to read your test file again..
e.g., say "Read the file test_file.txt"

You should get some response back from the model now indicating that the contents of the file
have been read.

Try making the agent do something that it doesn't have the tool to do, e.g., tell the agent to 
add a line to test_file.txt with the text "File edit works!".  It should come back with some
message saying that it doesn't have the tools to do that.  Ask it what tools it has, and see
how it responds.  Think about how it knows how to answer these questions.

#### Step 7 — Bound the loop (graded)

`while True` is unbounded autonomy.  We need some way of stopping the interactions
with the model if it is going crazy with repeated tool calls.

Introduce a python "constant" `MAX_TURNS` and give it a value (25 is plenty).

Now, in the agent loop, add a counter variable to count the number of times that
we have called the model (i.e., the number of "turns").  

[TODO: Need to specify exactly where this occurs.  I'm thinking this should 
occur at the `break` used in the loop -- not at the loop condition.]
Replace it with a counted loop capped at
`MAX_TURNS` (25 is plenty), and **print something when the cap is hit** — a silent stop
looks exactly like a finished task, and you will misread your own logs otherwise.

[TODO: Is there any way to test the effectivess of this new feature?  If not, we should
clarify that for the students and comment on how one might want to improve the infrastructure
in the future to allow for the concept to be tested.]

#### Step 8 — Add the rest of your tools

An agent with one read-only tool can't do either micro-task in Part 2. You need **at least three
tools total**, so set up the following two additional tools (`list_files`, and `write_file`), each with its schema, and register them in *both* `TOOLS_DICTIONARY` and `TOOLS_SCHEMA`.  Some hints are given 
below.

##### - List Files tool

`list_files` — the agent's only way to discover what exists. No parameters, so its
schema takes an empty `properties` object.  You need to fill in the body of the `list_files` 
function and the `description` in the schema (and then don't forget to register them).

```python
def list_files() -> list[str]:
    ...                                       # the names of the files in SANDBOX_DIR

LIST_FILES_SCHEMA = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "...(fill in)...",      # remember: this is prompt text
        "parameters": {"type": "object", "properties": {}},
    },
}
```

Hint:  for your function body above, you can use the following Python code to return a 
sorted list of file names in the sandbox directory.

```python
   return sorted(p.name for p in SANDBOX_DIR.iterdir() if p.is_file())
```

Now test this new tool addition by running the agent and asking it to list the files in the sandbox directory (see if it can list your `test_file.txt` file).

[TODO: what does this mean??]
Once it exists, go back to `read_file` and fold it into that error string, as step 4
described.

##### - Write File tool

`write_file` (or `edit_file`) 

```python
def write_file(file_name: str, contents: str) -> str:
    path = resolve_in_sandbox(file_name)      # required: the jail, same as read_file
    ...                                       # return something actionable:
                                              # "wrote N bytes to X", not True or -1
```

In this case, you may be wondering what the return `str` should be.  In general, 
it's helpful for the model to get some explicit indication that the tool action succeeded or failed.
If nothing is returned (e.g., an empty string), the model will start guessing or try so to some
other action to figure out what happened.

Hint: here is some compact code that you can use to actually write to the file while 
give information about what happened the model.  

```python
   return f"wrote {path.write_text(contents)} bytes to {file_name}"
```

Try to write the `WRITE_FILE_SCHEMA` on your own.  

Hints:
  - use the `READ_FILE_SCHEMA` as a starting point
  - your `description` should indicate that a file will be written or overwritten
  - you will have two `required` `properties` - one for the `file_name` and one for the file `contents`

Once you have completed the addition of the `write_file` tool, test it by..
  - requesting an update (like a simple word or line insertion) into the existing test file
  - requesting that a new file with some simple content be created.


##### - (Optional) Run Command tool

Optional fourth tool, `run_command`, which lets the agent run its own tests. If you add
it, safety rule 2 applies and is graded:

```python
ALLOWED_COMMANDS = {"python", "pytest"}       # exact match on the executable

def run_command(command: list[str]) -> str:   # a LIST, never a string
    if command[0] not in ALLOWED_COMMANDS:
        return f"ERROR: command not allowed: {command[0]} - allowed: {sorted(ALLOWED_COMMANDS)}"
    ...                                       # subprocess.run(command, cwd=SANDBOX_DIR,
                                              # capture_output=True, text=True, timeout=...)
```

[TODO: What does this mean?]
Never join the model's arguments into a string and hand it to a shell. `subprocess.run`
with a list and the default `shell=False` is the whole defense.

#### Step 9 — Add a "Verbose" mode

Towards the top of your file, e.g., after the `import requests` define a constant `VERBOSE` to 
control a "Verbose" mode for your agent.

``` python
# control VERBOSE mode
VERBOSE = True
# VERBOSE = False
```

Before the tool call (right after the `raw_arguments` structure is built, 
add the following to print the details of the call.

```python
if VERBOSE:
    print(f"---\nCalling {name} with arguments {raw_arguments}")
```

After the completion of the `if` structure that defines `result` with either an actual
result or an error (right before we append the `result` to the messages list, add the 
following to print out the result contents that will be added to the converation history.

```python
if VERBOSE:
    print(f"Result: {result}\n---\n")
```

Repeat some of your interactions above to now see the effects of adding the VERBOSE mode.

You will use this mode in Part 2 -- for our toy agent, it's the best debugger you have —
almost every "why did it do that?" is answered by looking at what the tool actually
returned.


### Part 2 — the micro-tasks

Use your agent to complete both the tasks below.  Use the verbose mode and 
create a session log (by copying the contents of the terminal window) for each session.
You will can add your own personal notes or observations to the log. 
Add these log files as `micro-task-A-log.txt` and `micro-task-B-log.txt` to your
exercise solution folder.

- **Micro-task A (green-field):** "Create `fizzbuzz.py` with a `fizzbuzz(n)` function and a `test_fizzbuzz.py` with at least 4 pytest cases, then run the tests." (If you
  skipped `run_command`, have the agent write both files and run pytest yourself —
  note this in the log.)
- **Micro-task B (bug fix):** **copy** `exercise-04-starter/micro-task-b-seed/` (three
  files: `cart.py`, `discount.py`, `test_checkout.py`) into your `sandbox/`, then:
  "The tests in this project fail. Find the bug and fix it — change the code, not the
  tests." The bug is a single inverted comparison in the discount calculation, and it
  breaks both tests; `pytest sandbox` should show two failures before you start.

Copy, don't move — keep the pristine seed where your agent can't reach it. You will want
to reset and re-run, and a flaky free route makes that likelier than you'd think.

### Part 3 — reflection (half a page)

Create a file `reflections.md` in your exercise solution folder.  In this folder, 
record some of your thoughts about this exercise.  
- What did you learn?
- What surprised you? 
- Name **two things Claude Code does that your toy doesn't**, and
point to the place in *your* code where each would have to go. Where did your agent
waste tokens, and what (system prompt? tool description? loop change?) would fix it?

## Deliverable

Repo or zip: agent source · both session logs · the (agent-fixed) micro-task B files ·
`reflection.md`.

## Completion checklist (all required for satisfactory)

- [ ] ≥3 tools with schemas; loop terminates on its own AND via the turn cap (steps 4–8)
- [ ] Path jailing demonstrably present (point to the lines in your source) (step 3)
- [ ] If `run_command` exists: allowlist + no shell-string execution (step 8)
- [ ] Micro-task A log shows multi-turn tool use ending in success (`micro-task-A-log.txt`)
- [ ] Micro-task B log shows the bug found and fixed in code (tests untouched) (`micro-task-B-log.txt`)
- [ ] Reflection file completed (`reflections.md`)
- [ ] No API key committed; the turn cap is set in code (step 7)

## Troubleshooting

- **`500` mid-run, with the first call fine:** almost certainly the free route, not your
  payload — the body will say `{"type":"Router.Unavailable", ...}`. `raise_for_status()`
  throws that body away, so print it before raising. **A 5xx is the server's problem; a
  4xx is yours** — retry the first, fix the second. And repeat before concluding:
  against a route that fails a large fraction of calls, a single A/B test tells you
  almost nothing.
- **`400 The reasoning_content ... must be passed back`:** you're on a thinking model
  and you rebuilt the assistant message. Append the response dict unmodified, or switch
  models.
- **`401 Invalid API key` when you don't have one:** you're sending a placeholder. Omit
  the `Authorization` header entirely.
- **Model loops on a failing tool:** your error strings may be uninformative — return
  what a colleague would need ("file not found: X; sandbox contains: [...]").
- **Model "edits" files that don't exist:** strengthen "read before edit" in the system
  prompt, or make `write_file` fail loudly on suspicious paths.
- **Second request 400s, or the model stalls waiting:** every `tool_call` must be
  answered by a `role: "tool"` message carrying that call's `tool_call_id` — including
  calls to tool names you don't recognize. Pair them by id, not by index, and never skip
  one.
