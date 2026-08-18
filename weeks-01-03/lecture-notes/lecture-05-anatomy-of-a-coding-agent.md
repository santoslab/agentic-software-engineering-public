# Lecture 5 Notes — Anatomy of a Coding Agent: Building the Toy Agent

> Agentic Software Engineering · Week 3, first meeting
>
> **The one idea:** in about 200 lines of Python against the raw API, you can build a
> working coding agent. After today, no part of Claude Code is magic — it is your
> loop, plus engineering.

## 1. The emperor has no clothes


Thorsten Ball subtitled this week's required reading "The Emperor Has No Clothes,"
and his thesis is the one this lecture demonstrates end to end: a functional
code-editing agent is *an LLM, a loop, and enough tokens*. Everything we have built up
across four lectures — the stateless model, the messages list, tool schemas, the
dispatch loop, the system prompt — assembles today into one file you can read in a
sitting. In class we walk that file top to bottom and then watch it fix a real failing
test. This week, you build it (Exercise 4).

The point is not that Claude Code is trivial — section 5 is precisely about what it
adds. The point is that the *architecture* is legible, so every behavior you observe
in any agent, and every safety property you rely on, has an address you can point to.

## 2. The conversation is the only state

Strip the agent to its API call. One request looks like this:

```python
response = client.messages.create(
    model="claude-haiku-4-5-20251001",   # cheap and fast: right for a toy
    max_tokens=2000,                     # a per-call spend cap you control
    system=SYSTEM,                       # standing instructions
    messages=messages,                   # THE ENTIRE STATE OF THE AGENT
    tools=TOOLS,                         # what it may request
)
```

Look at `messages=messages` and connect it to Lecture 1: the model is a pure function.
Your `messages` list *is* the agent — its perceptions, its history, its partial
progress, everything. The line in your loop that re-sends the whole list every
iteration is statelessness made visible, and it is also (Lecture 6) the line that
costs money.

The **system prompt** for a toy coding agent is yours to author, and authoring it is
where Exercise 4 starts feeling real. A workable one, in full — identity and scope,
operating rules, how to finish:

```python
SYSTEM = """You are a coding agent. You work ONLY inside the scratch
directory; never reference paths outside it.

Rules:
- Read a file before you edit it.
- Prefer the smallest change that completes the task.
- If a tool returns an error, read it carefully and adjust your approach.
- Run the tests after changing code, if a test tool is available.

When the task is complete, stop requesting tools and summarize what you
changed in two or three sentences."""
```

Twelve lines, nothing clever — and every line earns its place, which you can prove by
deletion: remove "read a file before you edit it" and the agent will occasionally
overwrite files it has never seen, guessing at their contents (plausibly, of course).
In class we run the same agent twice, once with a considered system prompt and once
with a gutted one — same model, same tools, same task, visibly worse behavior. You
built the soul; you can also lobotomize it.

## 3. Tools and the dispatch loop

Your agent needs at least three tools — `read_file`, `list_dir`, and `write_file` or
`edit_file` — each defined exactly as in Lecture 2: name, English description, JSON
schema. Write the descriptions like instructions to a colleague, because that is
literally how they are consumed. The difference is not cosmetic:

> **Weak:** `"description": "Reads a file."`
> — Which paths are legal? Relative to what? When should it be used? The model fills
> the gaps with guesses: absolute paths, files outside the sandbox, editing before
> reading.
>
> **Strong:** `"description": "Read a file from the working directory and return its
> contents as text. Paths are relative to the working directory. Use this before
> proposing any edit to a file."`
> — The same schema, but the *when* and the *how* are now in every single API call,
> steering tool choice on every turn.

A misbehaving agent very often has a mis-*described* tool; check the descriptions
before you blame the loop.

The loop that animates them, in full:


```python
def run(task, max_turns=25):
    messages = [{"role": "user", "content": task}]
    for _ in range(max_turns):                      # hard cap: no unbounded autonomy
        resp = client.messages.create(model=MODEL, max_tokens=2000,
                                      system=SYSTEM, messages=messages, tools=TOOLS)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            return resp                             # the model decided it is done
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,        # pair by id — never zip by index
                    "content": execute(block.name, block.input),
                })
        messages.append({"role": "user", "content": results})
```

And the dispatcher, where every safety decision in your agent lives:


```python
SANDBOX = Path("scratch").resolve()

def safe_path(p):
    full = (SANDBOX / p).resolve()
    if not full.is_relative_to(SANDBOX):            # the jail check
        raise ValueError(f"path escapes sandbox: {p}")
    return full

def execute(name, args):
    try:
        if name == "read_file":
            return safe_path(args["path"]).read_text()
        ...
    except Exception as e:
        return f"ERROR: {e}"                        # errors go back as results
```


Three design decisions in that code deserve names, because in Exercise 4 they are
graded elements and in your career they are the difference between a tool and an
incident:

- **Path jailing.** Resolve every path and verify it is under the sandbox root
  *before* touching the filesystem. The model will occasionally produce a path
  outside the sandbox — not malice, just next-token plausibility. Your jail check is
  the harness refusing. You are now, personally, the permission system from Lecture 3.
- **Command allowlisting.** If you implement the optional `run_command` tool, it
  takes an exact-match allowlist (`python`, `pytest`) and passes an *argument list* —
  never a string through a shell. Interpolating model output into a shell string is
  the classic agent-security mistake; do not make it in week 3 and you likely never
  will.
- **Errors as feedback.** `execute` returns error text instead of raising. A
  well-described error ("file not found: game.py — sandbox contains: cart.py,
  discount.py, test_checkout.py") is a *prompt* that lets the model self-correct on
  the next turn. In class you get to watch this: the agent misreads a filename, eats
  the error, lists the directory, and recovers. Nobody wrote recovery logic. The loop
  plus informative errors *is* the recovery logic.

Two smaller caps complete the safety story: the `max_turns` bound (an agent that
cannot stop is a bug with a billing rate) and your model/`max_tokens` choices, which
are the spend cap. Exercise 4's rules — Haiku while iterating, `max_tokens` capped
at 2000,
turn cap 25 — are these decisions made explicit.

## 4. Watching it work

The in-class run uses the same seeded mini-project that ships with Exercise 4: three
small files — a cart, a discount function, a test — where the test fails because a
comparison in `apply_discount` is inverted. The task prompt: *"The test in this
project fails. Find the bug and fix it — change the code, not the test."*

With verbose mode printing every request and response, you see the whole cognition in
plain JSON: it lists the directory; reads the test; reads `discount.py`; emits an edit
flipping `<` to `>`; runs the tests (or asks you to); and returns a summary with
`stop_reason: "end_turn"`. Five or six turns, a few thousand tokens, one fixed bug —
and at no point did anything happen that you cannot point to in the ~200 lines you
now understand completely.

When your own agent misbehaves this week, debug it the same way you just watched it
succeed: **read the traffic.** The context is the complete explanation of the
behavior. Uninformative error strings, a misleading tool description, a missing rule
in the system prompt — the transcript will show you which.


## 5. What Claude Code adds (or: the toy, grown up)

Now run the comparison that makes the whole unit click. Your toy has the same
skeleton as Claude Code. What does the production harness add?

- **A permission system with a UI** — your jail check, generalized to interactive,
  configurable consent over reads/writes/commands.
- **Context management** — compaction, the `/context` accounting, careful curation of
  what enters the window. Your toy just grows until it hits the wall.
- **CLAUDE.md injection** — durable per-project instructions loaded every session.
  Your toy's system prompt is hardcoded.
- **Plan mode** — a harness-enforced separation between proposing and doing. Your toy
  goes straight to edits.
- **Subagents, hooks, skills, MCP** — the extensibility surface from Lecture 3's
  preview, all deferred to later units.
- **A battle-tested system prompt and toolset** — thousands of engineering hours on
  the exact text and schemas you hand-rolled in an evening.

Every one of these is *legible engineering on a loop you have now built*. That
reframing — from magic to engineering — is the deliverable of weeks 1–3.

## 6. Exercise 4 launches

The full spec is `exercise-04-toy-agent.md`. In brief: build the agent (3+ tools,
system prompt of your own authorship, dispatch loop, path jail, turn cap; optional
allowlisted `run_command`); run it on two micro-tasks (a green-field fizzbuzz-with-
tests task, and the seeded bug fix above) capturing verbose session logs; and write a
half-page reflection naming two things Claude Code does that your toy doesn't — *and
pointing to the exact place in your code where each would have to go.*


You will receive a shared-pool API key; the spend rules in the spec are graded
elements. Expected total cost is well under $5 — and if you find yourself past that,
stop and read your transcript, because something is looping.


Due at the start of week 4.

## Questions to think about

1. Which single tool would you add to your agent next, and what is the worst thing it
   could do? Where in your code would you contain that?
2. Where in the loop would you insert a human checkpoint, and what would it cost you
   in autonomy? (Lecture 6 shows a $25–50 answer to this question.)
3. Your agent re-sends the entire conversation every call. What does that predict
   about turn 30 of a long session — in latency, in cost, in the model's attention?

## Before next lecture

- **Required:** Anthropic engineering, *Effective context engineering for AI agents*.
- **Required:** the *Agentic Development Principles* handout — five principles, one
  page; Lecture 6 makes them the semester's rubric.
- **Required:** the NautilusTRX pass-retrospectives handout (~10 minutes) — five
  builds of the same project, including the expensive failure we dissect in class.
- **Project 0** kickoff is due at the end of this week.

