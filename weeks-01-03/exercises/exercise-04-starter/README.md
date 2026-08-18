# Exercise 4 starter

Read [`../exercise-04-toy-agent.md`](../exercise-04-toy-agent.md) first. Part 1 of the
exercise is a nine-step build that turns the chat bot in this folder into an agent;
every piece of code you need is in the step that introduces it.

| Path | What it is |
|------|-----------|
| `toy_agent.py` | A ~50-line chat bot: config, one HTTP call, a REPL. No tools, no loop, no sandbox — those are steps 3–8. |
| `micro-task-b-seed/` | The 3-file mini-project for micro-task B. Its tests fail. |
| `sandbox/` | You create this in step 3. Everything your agent can touch lives here. |

The starter has **no comments**. That is deliberate — the explanations live in the
exercise, next to the code they explain, so read the step before you paste the snippet.

## Quick start

```
pip install requests
python toy_agent.py
```

No API key is required — see the "Model access" section of the exercise before you add
one, and note that sending a *placeholder* key is worse than sending none.

## Micro-task B

Copy `micro-task-b-seed/` into `sandbox/` — **copy, don't move**. You will want to
reset and re-run, and a flaky free route makes that likelier than you'd think.

```
cp micro-task-b-seed/* sandbox/          # PowerShell: copy micro-task-b-seed\* sandbox\
pytest sandbox                           # confirm both tests fail before you start
```

Then give your agent: *"The tests in this project fail. Find the bug and fix it —
change the code, not the tests."* It is one inverted comparison, and it breaks both
tests. The fix belongs in the code; if your agent edits `test_checkout.py`, that run
doesn't count.
