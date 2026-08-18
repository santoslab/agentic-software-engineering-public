---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
  }
  section.lead {
    background: #310066;
    color: #ffffff;
  }
  section.lead h1, section.lead h2 {
    color: #ffffff;
  }
  section.standout {
    background: #beaefc;
    color: #310066;
    text-align: center;
    font-size: 36px;
  }
  h1, h2 {
    color: #310066;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->

# Anatomy of a Coding Agent: Building the Toy Agent

**Agentic Software Engineering — Lecture 5**
Week 3 · Meeting 1 of 2

---

## The one idea

In **~200 lines of Python** against the raw API, you can build a working coding agent.

After today, no part of Claude Code is magic — it is *your loop, plus engineering*.

> "an LLM, a loop, and enough tokens" — Thorsten Ball,
> *How to Build an Agent, or: The Emperor Has No Clothes*

<!-- 0–5 min. Today we walk the file; this week you build it (Ex. 4). -->

---

<!-- _class: lead -->

# The conversation is the only state

---

## One API call

```python
response = client.messages.create(
    model="claude-haiku-4-5-20251001",   # cheap and fast: right for a toy
    max_tokens=2000,                     # a per-call spend cap YOU control
    system=SYSTEM,                       # standing instructions
    messages=messages,                   # THE ENTIRE STATE OF THE AGENT
    tools=TOOLS,                         # what it may request
)
```

`messages=messages` is Lecture 1's statelessness, made visible —
and (Lecture 6) it is the line that costs money.

<!-- 5–20 min block. -->

---

## A workable system prompt, in full

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

Twelve lines, nothing clever. **Prove each line by deletion:**
remove "read a file before you edit it" → the agent overwrites files it has never seen. Plausibly, of course.

---

<!-- _class: lead -->

# Tools and the dispatch loop

---

## Tool descriptions are load-bearing

> **Weak:** `"description": "Reads a file."`
> Which paths are legal? Relative to what? When?
> The model fills the gaps with guesses.

> **Strong:** `"description": "Read a file from the working directory and return its contents as text. Paths are relative to the working directory. Use this before proposing any edit to a file."`
> The *when* and *how* now ride in **every API call.**

A misbehaving agent very often has a mis-*described* tool.

<!-- 20–40 min block. Write descriptions like instructions to a colleague — that is literally how they are consumed. -->

---

## The loop, in full

```python
def run(task, max_turns=25):                        # hard cap: no unbounded autonomy
    messages = [{"role": "user", "content": task}]
    for _ in range(max_turns):
        resp = client.messages.create(model=MODEL, max_tokens=2000,
                                      system=SYSTEM, messages=messages, tools=TOOLS)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            return resp                             # the model decided it is done
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                results.append({"type": "tool_result",
                                "tool_use_id": block.id,      # pair by id!
                                "content": execute(block.name, block.input)})
        messages.append({"role": "user", "content": results})
```

---

## The dispatcher — where every safety decision lives

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

---

## Three decisions with names

1. **Path jailing** — resolve, then prefix-check, *before* touching disk. The model *will* emit escaping paths — not malice, plausibility. **You are now the permission system from Lecture 3.**
2. **Command allowlisting** (optional `run_command`) — exact-match list, argument *list* not shell string. Interpolating model output into a shell is *the* classic agent-security mistake.
3. **Errors as feedback** — return, don't raise. "file not found: game.py — sandbox contains: cart.py, discount.py, test_checkout.py" is a *prompt* that steers the next turn.

Plus the caps: `max_turns`, `max_tokens`, model choice = **your spend cap.**

---

<!-- _class: standout -->

## Demo: fix the failing test

Three files. One inverted comparison.
Raw API traffic on screen.

<!-- 40–57 min — the lecture's spine. Same seeded mini-project that ships with Ex. 4. Recorded fallback mandatory; two seed variants prepared in case it one-shots. If time: rerun with gutted system prompt. -->

---

## The seeded bug

```python
# discount.py
def apply_discount(total_amount, threshold, rate):
    """Apply rate discount if total exceeds threshold."""
    if total_amount < threshold:          # BUG: should be >
        return total_amount * (1 - rate)
    return total_amount
```

What you watch: `list_dir` → read the test → read `discount.py` → edit `<` to `>` → run tests → `stop_reason: "end_turn"`.

Five or six turns. And **every one of them has an address** in ~200 lines you now understand completely.

*When your agent misbehaves this week: read the traffic. The context is the complete explanation of the behavior.*

---

<!-- _class: lead -->

# Toy vs Claude Code

---

## What the production harness adds

| Your toy lacks… | You met it in… |
|-----------------|----------------|
| permission system with a UI | every Ex. 2 prompt |
| context management (`/compact`, `/context`) | the survival kit |
| CLAUDE.md injection | Demo 1, L3 |
| plan mode | Demo 2, L3 |
| subagents, hooks, skills, MCP | deferred to later units |
| battle-tested system prompt + tools | you hand-rolled yours tonight |

Every one: **legible engineering on a loop you have now built.**

That reframing — magic → engineering — is the deliverable of weeks 1–3.

<!-- 57–67 min. Compressible: the Ex. 4 reflection asks the same question. -->

---

<!-- _class: standout -->

## Exercise 4 launches

Build it. Run it on two micro-tasks. Capture the logs.
Name two things Claude Code does that your toy doesn't —
**and point to the line in your code where each would go.**

Due start of week 4.

<!-- 67–75 min. Spec walkthrough; shared key pool. -->

---

## Spend and safety rules are graded elements

- **Haiku** while iterating · `max_tokens` capped at 2000 · turn cap 25
- Expected total: **well under $5** — past that, stop and read your transcript; something is looping
- Key from the shared pool: environment variable, never committed
- Jail all file ops · allowlist any `run_command` · no shell interpolation

---

## Questions to think about

1. Which single tool would you add next — and what's the *worst* thing it could do? Where in your code would you contain that?
2. Where in the loop would you insert a human checkpoint, and what would it cost in autonomy? (Lecture 6 shows a $25–50 answer.)
3. Your agent re-sends the whole conversation every call. What does that predict about turn 30 — in latency, cost, and attention?

---

## Before next lecture

- **Required:** Anthropic engineering, *Effective context engineering for AI agents*
- **Required:** the *Agentic Development Principles* handout — L6 makes them the semester's rubric
- **Required:** NautilusTRX pass-retrospectives handout (~10 min) — including the expensive failure we dissect
- **Project 0 kickoff due end of this week**

*Next: when can you trust the output — and at what price?*
