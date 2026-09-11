# Exercise 4 — Build a Toy Coding Agent

Note: *Do this exercise without any assistance from Claude or any other coding agent*.  
If you don't do this exercise manually, you won't learn the concepts.

> **Effort:** 3–4 hours
>
> **Requires:** Python 3.11+ and the `requests`, `python-dotenv`, and `pytest` packages (see Files setup)

>
> **Starter code:** [`exercise-04-starter/`](./exercise-04-starter/) — a bare chat bot
> (`toy_agent.py`) that Part 1 walks you through turning into an agent, plus the
> micro-task B seed project.

## Goal

Demystify the harness by building one: a working coding agent in roughly 200 lines of
Python using a hosted LLM API. When you're done, you will be able understand most
Claude Code features as "what I did in my toy implementation, but with more engineering".
That is, your toy example will help you understand each of the core features in Claude Code.
You'll also be able to understand, even with your simple toy agent, how coding agents
enforce basic safety features. 

Note that part of the exercise is to reflect on your observations of how your agent behaves and to note "interesting things" that you observed.  So be thinking about this as you work.

## Overview of Different Parts

- Part 1: The exercise description will walk you through how to take the given code
that implements a chat bot and turn it into a simple coding agent.
- Part 2: You'll apply your agent to some very simple development "micro-tasks"
- Part 3: You'll write up a summary of your experiences in the exercise 

## Model access setup

Here is some technical background on the backend models that we will use.
You don't need to understand the details of all of this, but you need to be 
somewhat aware of this issues (which you can research more about yourself).
Bottom line: for this assignmnet, if you just start with the code we give you
and don't make any adjustments on your own, you don't have to worry about the 
issues below.

Your toy agent will by default use a free model on **OpenCode Zen** (<https://opencode.ai/docs/zen>), an OpenAI-compatible endpoint at `https://opencode.ai/zen/v1/chat/completions`.

- **No key required (at first).**  To initially run the starter code, you won't need an authorization key to use OpenCode Zen.  However, we found that in building the model solution, we eventually needed to have a subscription from the [OpenCode Go](https://opencode.ai/go) plan.  The free tier also rate-limits aggressively per address (see the `429` entry in Troubleshooting), which is another reason to expect to need a key for the full exercise.  

- **Adding an API key in an environment variable**  If the code at the top of the toy agent finds that the environment variable `OPENCODE_API_KEY`, it will set the agent/model interactions up to use non-free models.  So if you get an Open Code Go subscription, follow the instructions to get an API key, then set the environment variable `OPENCODE_API_KEY` appropriately for your shell (e.g., in your `.bashrc`) 
- follow the [hints given here](./exercise-04-starter/OPENCODE_GO_API_KEY_SETUP.md) 

- **Avoid the DeepSeek-family *thinking* models** (e.g. `big-pickle`,
  `deepseek-v4-flash-free`) for this exercise. They require each assistant message's
  `reasoning_content` field to be echoed back verbatim, and will 400 if you rebuild a
  "clean" message dict.

- **Free tiers are best-effort infrastructure.** Some routes fail a large fraction of
  calls with a 5xx, and in an agentic loop a *single* failure kills the whole run. If a
  run dies, switch models before you start debugging your payload.

- **Caps in code:** to avoid a situation where a bug in the harness uses up your
  token budget, part of the exercise will including coding a bound on the number of 
  calls to the mode for each user interaction (e.g., 25 loop turns). 


## Files set up and Python environment set up

Copy the `exercise-04-starter` folder from the course material repo into your student
repo, e.g., `exercises/exercise-04` (removing the `-starter`).  

In your terminal window, `cd` to the `exercise-04` folder.

We need three Python packages beyond the standard library:

- `requests` — makes the HTTP calls to the model endpoint
- `python-dotenv` — reads an optional `.env` file holding your API key (the starter
  imports it, so it must be installed even if you never create a `.env`)
- `pytest` — runs the tests in the Part 2 micro-tasks

You can install them globally as shown below..
```
pip install requests python-dotenv pytest
```
BUT it is best practice to use a python "virtual environment" that installs the packages locally for your project (instead of installing them system wide).  If you pursue that route, do
the following.

```
python -m venv .venv                        # create the virtual environment in .venv
source .venv/bin/activate                   # activate the virtual environment
pip install requests python-dotenv pytest   # install the needed packages locally
pip freeze > required-packages.txt          # record the required packages
```

Make sure `.venv` is listed in your solution repo's `.gitignore` (the starter folder ships a `.gitignore` that already covers this).  When others use your code (e.g., in a check-out of your repo), the local environment can be set up as follows...

```
python -m venv .venv
source .venv/bin/activate
pip install -r required-packages.txt
```

If you close the terminal or otherwise leave the virtual environment, you will need to activate it again in your `exercise-04` directory as follows...


```
source .venv/bin/activate
```

Now check to see if the initial version of the toy agent runs..
```
python toy_agent.py
```

## Format of Messages between Harness and Model

There are different standards for exchanging information between the harness (i.e., your 
toy agent) and a model.  This exercise uses an older API format from OpenAI called the 
"Chat Completions" format.  Although the concepts are similar, this is slightly different
that the format used by Claude or the most recent Open AI models.

The starter files for the exercise provide a summary of the message formats in the file
[`exercise-04-starter/message-format-hints.md`](./exercise-04-starter/message-format-hints.md).

## Safety rules (graded elements, not suggestions)

Here are some safety rules that you need to enforce as you build your agent (we help you do these things by giving clear instructions in the exercise description).

1. **Jail all file operations** to a scratch directory: resolve every path and verify
   it's under the sandbox root *before* touching the filesystem (the provided code will give
   you some direction about how to do that).
2. Hard iteration limit on the loop (no unbounded autonomy) -- we'll also show you
   how to do that.

## Task

### Part 1 — chat bot to agent, in nine steps

You are given a **chat bot**, not an agent:
[`exercise-04-starter/toy_agent.py`](./exercise-04-starter/toy_agent.py) is ~90 lines
that POST your messages to a model and print the reply. It has no tools, no loop, and no
safety properties. You will add those, one step at a time, until it is an agent of
roughly 200 lines.

Here is a summary of the steps that you will follow.

| # | Step | Who writes it |
|---|------|---------------|
| 1 | Run the chat bot you were given | — |
| 2 | Play with, then write, the system prompt | you |
| 3 | Add the sandbox jail | given |
| 4 | Add your first tool | given |
| 5 | Declare the tool to the model | given |
| 6 | Grow the single call into the agentic loop | given |
| 7 | Bound the loop (`MAX_TURNS`) | given |
| 8 | Add the rest of your tools (≥3 total, `run_command` optional) | you |
| 9 | Add `--verbose` | you |

Steps 3–6 are given in full because a subtly wrong jail or a half-answered tool call
fails in ways that are miserable to debug and easy to not notice. What is left to you is
the part the exercise is actually about: the prompt, the tools, the ceiling on autonomy,
and the evidence that the jail holds.

---

#### Step 1 — Run the chat bot you were given

```
python toy_agent.py
```

Talk to it. Confirm you get replies before you change anything.

One thing to notice while you chat: `messages` is the *entire* state of the program, and
the whole list is re-sent on every call. Nothing is remembered on the server. Each turn
therefore costs more than the last, and that growth is what you'll be asked about in
Part 3.

#### Step 2 — Write the system prompt

**First, experiment with different styles system prompt styles.**  Change the system 
prompt by changing the string assigned to the python `SYSTEM` variable.
Sometimes it can be difficult to see how the system prompt effects the model's output. Try adding lines or phrases that are stylistic and fun instead of strictly productive. Here are some ideas to start:

- End all of your responses with 'Go Cats!'
- Always output in Rhymed Couplets
- Talk like a 17th century Pirate
- reference as many facts about australia or it's wildlife as possible

**Now write the real one.** Now write a real system prompt that determines
how you want the agent to behave (you can adapt this as you continue the exercise).
For example, start with the string below and replace the `...` with something meaningful.
At minimum it should establish who the agent is, that it only ever touches its
working directory (the sandbox directory), that it reads a file before editing it, 
that it keeps calling tools until the task is done, and what it should say when it stops.

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

**What the Python code does**

`pathlib` is Python's standard library for working with filesystem paths as objects
rather than strings. Two of its features are used here: the `/` operator joins path
components (`SANDBOX_DIR / "notes.txt"`), and `.resolve()` converts a path to its
canonical absolute form — it makes the path absolute, collapses any `.` and `..`
components, and follows symbolic links.

The two setup lines create the sandbox directory:

- `__file__` is the path of the Python file that is currently running — in this
  program, `toy_agent.py` itself. So `Path(__file__).resolve().parent` is the absolute
  path of the directory containing `toy_agent.py`, and appending `/ "sandbox"` names a
  `sandbox` subdirectory next to the script.
- `SANDBOX_DIR.mkdir(parents=True, exist_ok=True)` creates that directory on disk.
  `exist_ok=True` means it is not an error if the directory already exists, so
  re-running the agent works. `parents=True` would also create any missing intermediate
  directories (not needed here, but harmless).

`resolve_in_sandbox(file_name)` is the function that every filesystem tool will call
before touching a path. It performs three steps:

1. **Join.** `SANDBOX_DIR / file_name` appends the model-supplied file name to the
   sandbox path. One `pathlib` rule matters here: if `file_name` is itself an absolute
   path (`/etc/passwd`, or `C:/Windows/Temp/x` on Windows), the `/` operator discards
   the left-hand side entirely and the result is just `file_name`. So the join by
   itself guarantees nothing about where the path points.
2. **Normalize.** `.resolve()` turns the joined path into canonical absolute form. This
   is the step where `sandbox/../../secrets.txt` stops *looking like* a path under
   `sandbox/` and becomes what it actually is: a path two levels above it.
3. **Check.** `resolved.is_relative_to(SANDBOX_DIR)` returns `True` only if the
   canonical path is `SANDBOX_DIR` itself or lies somewhere beneath it. If the check
   fails, the function raises a `ValueError` instead of returning, so the caller never
   receives an out-of-sandbox path.

**Why the code is written this way**

Three design decisions in this code each close a specific hole. None of them is
obvious from reading the code once.

- **The sandbox location is anchored to the script file, not the current working
  directory.** Suppose we had written `SANDBOX_DIR = Path("sandbox").resolve()`
  instead. That path is relative to wherever you happen to run `python` from. Launch
  the agent from some other directory and `mkdir` silently creates a second, empty
  `sandbox/` there — no error is raised, the agent appears to work, but it is reading
  and writing files in the wrong place, and the test files you put in the real sandbox
  "don't exist" as far as the model can tell. Anchoring to `__file__` makes the sandbox
  location a fixed property of the code rather than of how the program was launched,
  so this failure cannot occur.

- **The path is normalized before it is checked.** Consider what happens without
  `.resolve()`. The name `../../secrets.txt` joined onto the sandbox produces a path
  that *textually* begins with `SANDBOX_DIR` but *actually* points two directories
  above it — a prefix check on the unresolved path would incorrectly pass it. And, as
  noted above, an absolute `file_name` makes the join discard `SANDBOX_DIR` entirely,
  so there would not even be a prefix to check. Resolving first puts every path into a
  canonical form in which the containment check gives the correct answer. (Resolution
  also follows symlinks, so a link inside the sandbox pointing outside is caught as
  well.) A check structured this way is said to *fail closed*: any path that cannot be
  positively confirmed to be inside the sandbox is rejected.

- **A violation raises an exception rather than returning an error value.**
  `resolve_in_sandbox` does not print a warning or return `None`; it raises
  `ValueError`. This has two consequences. First, a tool author cannot forget to check
  a return code — a bad path never produces a usable `Path` object at all. Second, no
  dedicated error handling is needed: the tool-dispatch code you will add in step 6
  wraps every tool call in a `try/except` that converts any exception into an error
  string, so a jail violation comes back to the model as
  `ERROR: read_file failed: ValueError: path escapes the sandbox: ...`. The model
  reads that message, understands the request was refused, and continues; the program
  does not crash.

When we add filesystem tools starting in the next step, every one of them must obtain
its path from `resolve_in_sandbox` — never directly from the string the model supplied.
Note that the restriction only holds if *every* tool does this: if even one tool
bypasses the helper, the model can route any path it wants through that tool, and the
sandbox no longer confines anything. That is what the concluding exercise checklist
means by the path jailing being "demonstrably present" — you should be able to point
at each tool in your source and show that its first path operation goes through this
function.

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

Once your agent has tools and a loop — that is, after step 8, when it can also write —
prove the jail holds: ask it, in plain English, to read `../../secrets.txt` and to
write to an absolute path outside the sandbox: `/tmp/pwned.txt` on macOS/Linux,
`C:/Windows/Temp/pwned.txt` on Windows. Both requests must come back as the
`path escapes the sandbox` error, and the model should shrug and carry on rather than
the program crashing. Use the example that matches your operating system: a Windows
drive path is not an absolute path on macOS/Linux — there it simply joins onto the
sandbox as an oddly named subdirectory, so it produces a different error and proves
nothing about the jail. Keep that exchange in a verbose log — it's the easiest way to
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

**Why two registries?** A tool has two halves that live in different places:

- The **schema** (`READ_FILE_SCHEMA`) is the half the *model* sees. It travels over
  the network: every call to the model will include the `TOOLS_SCHEMA` list in the
  request body, and that list is the model's only knowledge that the tool exists. The
  model never sees your Python code.
- The **function** (`read_file`) is the half the *harness* executes. It never leaves
  your program: when the model's reply requests a tool by name, the loop you will
  write in step 6 looks that name up in `TOOLS_DICTIONARY` and calls the Python
  function it maps to.

Because the two halves are stored separately, every tool you add in step 8 must be
registered in **both** places — and forgetting one produces two different failure
modes:

- **Forget the schema entry** and the model never learns the tool exists, so it never
  asks for it. Nothing errors; the function is simply dead code. Because this failure
  is completely silent, it is the most common way a new tool never gets called.
- **Forget the dictionary entry** and the model *will* ask for the tool (it saw the
  schema), but the loop finds no function to run and answers with the `unknown tool`
  error string instead. This failure is at least visible in the conversation.

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

The code above is careful to follow four rules about the chat-completions API. Each
rule, if broken, produces a bug — and usually a confusing one, because the failure
often shows up one request *later* than the mistake that caused it.

- **Append the model's response to the history exactly as it was received.** The loop
  does `messages.append(message)` with the dict just as the API returned it. It might
  be tempting to build a tidier dict containing only the fields you care about
  (`role`, `content`, `tool_calls`). Don't. The response can carry fields you did not
  expect, and some models require them back: thinking models, for example, include a
  `reasoning_content` field and reject the next request with a 400 error if that field
  is missing from the history. Remember that the entire message list is re-sent on
  every call, so whatever you append now is exactly what the server sees later.

- **No exception may escape the tool-dispatch block.** Many things can go wrong while
  executing a tool call: the model may send arguments that are not valid JSON
  (`json.loads` raises), it may pass a wrong or missing keyword argument (the function
  call raises `TypeError`), the path may violate the sandbox (`resolve_in_sandbox`
  raises `ValueError`), or the model may name a tool that does not exist. The code
  turns every one of these into an error *string* and keeps going — the
  `try/except Exception` converts any raised exception into an `ERROR: ...` message,
  and the unknown-tool case is caught by the `if` before the call is even attempted.
  The reason: an error string appended to the history is information the model can
  read and react to on its next turn (fix the arguments, choose a different tool). An
  uncaught exception, by contrast, terminates the whole program mid-task.

- **Every requested tool call must receive a reply.** The API keeps strict
  bookkeeping: if an assistant message contains three entries in `tool_calls`, the
  history must contain three `role: "tool"` messages answering them before the model
  can be called again. This includes calls you could not execute — a hallucinated
  tool name still gets a `role: "tool"` reply, carrying the error string. If even one
  call is left unanswered, the next request is rejected with a 400 error. This is why
  the unknown-tool branch constructs an error message rather than simply skipping the
  call.

- **Replies are matched to requests by `tool_call_id`, not by position.** A model may
  request several tool calls in a single message. Each request carries a unique `id`,
  and each reply must carry that same value in its `tool_call_id` field — that is how
  the server pairs results with requests. Never assume "the first reply answers the
  first call"; copy the id from the specific tool call you are answering, as the loop
  does with `tc["id"]`.

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

`while True` is unbounded autonomy: as long as the model keeps requesting tools, your
harness keeps calling the model. Usually the model stops on its own, but "usually"
should not be the only protection — a confused model can keep requesting tool calls
indefinitely, and every extra iteration is another API call, re-sending the
ever-growing history, billed against your token budget. We will cap the number of
model calls a single user request is allowed to consume.

This takes four small edits to the loop you built in step 6.

1. **Introduce the constant.** Just above `agentic_loop`, define the cap:

   ```python
   # Cap on the number of model calls made for a single user request.
   MAX_TURNS = 25
   ```

2. **Count model calls in the loop condition.** Initialize a counter before the loop,
   replace `while True` with a condition on the counter, and increment the counter at
   the top of the loop body, so each pass through the loop counts one model call:

   ```python
   def agentic_loop(messages: list) -> None:
       turns = 0
       while turns < MAX_TURNS:
           turns += 1
           message = call_zen(messages, TOOLS_SCHEMA)
           ...
   ```

3. **Change the `break` to `return`.** The existing `break` — taken when the model
   returns no tool calls — is the model deciding it is finished. That is the normal
   exit, and we want it to leave the function entirely:

   ```python
           if not tool_calls:
               return  # the model decided it is finished -- the normal exit
   ```

4. **Print a warning after the loop.** Because the normal exit is now a `return`, the
   only way execution can reach a statement *after* the `while` loop is for the loop
   condition to fail — that is, the cap was hit. So place the warning there (indented
   at function level, outside the loop):

   ```python
       print(f"\n[toy-agent] Stopped: hit the MAX_TURNS = {MAX_TURNS} cap for this request. "
             "The task may be unfinished.")
   ```

   Do not skip the print. A silent stop looks exactly like a finished task, and you
   will misread your own session logs in Part 2.

Two remarks on the design. First, putting the cap in the loop *condition* (rather than
an `if ... break` somewhere in the body) makes the bound visible in the structure of
the code: you can point at `while turns < MAX_TURNS` and see that the loop terminates.
Second, note what the cap counts: model calls, not tool calls. A single model call may
request several tools, and all of them still execute; what the cap bounds is the
number of round trips to the model, which is what actually costs tokens.

**Testing the cap.** You cannot make a live model run away on demand, so how do you
know this works? Test the mechanism by lowering the cap: temporarily set
`MAX_TURNS = 2` and give the agent a task that needs more than two model calls. At
this point your agent's only tool is `read_file` (writing arrives in step 8), so use
a reading task: put a second file next to `test_file.txt` (say `notes.txt`, with any
short content) and ask:

```
One at a time: read test_file.txt, then read notes.txt, then tell me what
they have in common. Use exactly one tool call per turn.
```

Each read costs one model call, so the agent spends its two allowed calls on the two
reads and the cap fires before it can deliver the comparison. You should see the cap
warning print instead of an answer. Restore `MAX_TURNS = 25` afterward.

Be clear about what this test does and does not establish. It shows the counting and
the stop work. It does *not* exercise the scenario the cap exists for — a model stuck
requesting tools forever — because a real model cannot be made to misbehave on cue. An
automated test of that scenario would replace the model with a fake: a substitute for
`call_zen` that always returns a tool call, so that the loop could never exit
naturally. Our code has no place to plug such a fake in, because `agentic_loop` calls
`call_zen` directly. Making the model-call function a *parameter* of the loop, so a
test can pass in a fake, is precisely how production harnesses make their loops
testable. You are not asked to do that here, but it is worth recognizing as a
limitation of the current design — and it is the kind of observation that belongs in
your Part 3 reflection.

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

Now that `list_files` exists, make the improvement that step 4 promised: upgrade the
error message in `read_file`. Replace its file-not-found return with

```python
        return f"ERROR: file not found: {file_name} - directory contains: {list_files()}"
```

Notice that the tool functions are ordinary Python functions, so one tool can simply
call another — here `read_file`'s error path reuses `list_files` to tell the model
what *does* exist. A model that asks for a file that isn't there now learns the
actual sandbox contents in the same tool result, and can correct itself on the next
request instead of guessing at file names.

Test it: ask the agent to read a file that does not exist (say, `missing.txt`) and
watch how it responds. It will typically report that the file is absent and name the
files that are actually there — evidence that it read and used your improved error
string.

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

- **Micro-task A (green-field):** With an empty sandbox, give the agent this prompt: 

```
Create `fizzbuzz.py` with a `fizzbuzz(n)` function that implements 
the classic fizzbuzz behavior.  Write a `test_fizzbuzz.py` with at least 4 pytest cases
```

Record the output in your log.

In a terminal window opened in the `sandbox` folder, run `pytest` on the text file.

```
pytest test_fizzbuzz.py
```
Record the command given above and the output of the test run in your log.


- **Micro-task B (bug fix):** **copy** `exercise-04-starter/micro-task-b-seed/` (three
files: `cart.py`, `discount.py`, `test_checkout.py`) into a clean `sandbox/` — copy,
don't move, so that you can reset and start over if a run goes wrong:

```
cp micro-task-b-seed/* sandbox/       # PowerShell: copy micro-task-b-seed\* sandbox\
```
  
This code base has a bug caused by a single inverted comparison in the 
discount calculation, and it breaks both tests; 
  
Run `pytest sandbox` to see two failures before you start, and record the output 
indicating the failing tests in your log.

Start your agent and give it the following prompt:
```
The tests in this project fail. Find the bug and fix it — change the code, not the
tests.
```
You should see the agent read the files, discover the bug, and write to files to fix the bug.  Record this output in your log.

Exit your agent and run `pytest sandbox` to show the test pass.  Record your test command and the output in your log.


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
- **`429 Too Many Requests`:** the keyless free route rate-limits aggressively per
  address — a handful of quick runs (or a whole class on one campus network) can
  trigger it, and the throttle can persist for a while. Wait, or switch to an API
  key; the Go route has much higher limits.
- **`requests.exceptions.ReadTimeout` kills the session:** the model exceeded the
  `timeout=` value in `call_zen` before finishing its reply. Thinking models can
  deliberate for several minutes on a request that conflicts with their instructions —
  the step 4 jail probes are exactly that kind of request. Raise the timeout
  (300 seconds is generous) and rerun; this is slowness, not failure.
- **Model loops on a failing tool:** your error strings may be uninformative — return
  what a colleague would need ("file not found: X; sandbox contains: [...]").
- **Model "edits" files that don't exist:** strengthen "read before edit" in the system
  prompt, or make `write_file` fail loudly on suspicious paths.
- **Second request 400s, or the model stalls waiting:** every `tool_call` must be
  answered by a `role: "tool"` message carrying that call's `tool_call_id` — including
  calls to tool names you don't recognize. Pair them by id, not by index, and never skip
  one.
