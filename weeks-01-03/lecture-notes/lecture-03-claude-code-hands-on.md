# Lecture 3 Notes — Claude Code Hands-On: Permissions, CLAUDE.md, Plan Mode

> Agentic Software Engineering · Week 2, first meeting
>
> **The one idea:** Claude Code is Lecture 2's loop productionized. Today you learn to
> drive it deliberately — knowing what each feature does to the context and what each
> permission prompt is protecting — instead of vibing.

## 1. Mapping the UI onto the loop

Open Claude Code and you are looking at the agent loop wearing a user interface. The
transcript scrolling up your terminal is the messages list. The spinner is a model
call in flight. The diff it shows you before touching a file is a `tool_use` request
*paused at the harness*, waiting for your approval. Nothing in this tool is a new
concept; it is Lecture 2 with engineering around it. Keep that mapping in your head
and the rest of this lecture is easy.

## 2. Permissions: the harness's refusal point

Last lecture we asked where the harness should refuse what the model asks. Claude
Code's answer is its **permission system**. Reading a file inside the workspace is
cheap and reversible, so it flows. Writing a file, running a shell command, touching
anything outside the workspace — these stop and ask you.

Two things to internalize about those prompts:

- **They are the safety layer.** The model cannot run anything; it can only request.
  The permission prompt is the moment the request crosses from model-space into
  your-filesystem-space. Treat each one as a question: *do I understand what this
  will do?* A typical prompt looks like (stylized):

  ```
  Claude wants to run:  pytest -q
    (y) allow once   (a) always allow pytest in this project   (n) deny
  ```

  Before pressing anything, practice the two-second habit: what does this command
  touch, and is it reversible? `pytest -q` reads code and runs tests — cheap, yes.
  `rm -rf build/` or `git push` deserve an actual pause. The `(a)` option is how
  permissions accumulate into project settings — convenient, and exactly how an
  over-permissive setup happens one keystroke at a time.
- **Auto-accept is a loaded gun in week 2.** Claude Code offers permission modes,
  from prompt-on-everything to broad auto-acceptance. Experienced operators loosen
  permissions deliberately, for bounded tasks, with version control as the backstop.
  You will get there. Start conservative: the discipline of *reading* what the agent
  wants to do is exactly the skill this unit builds.

Permissions and other per-project configuration live under the project's `.claude/`
directory (`settings.json`). Your starter repo includes a commented template.

## 3. CLAUDE.md: memory that carries intent

Claude Code automatically injects a file named `CLAUDE.md` from your project root into
the context of every session. It is, precisely, user-space extension of the system
prompt — standing instructions that survive across sessions. The command `/init` asks
the agent to *generate* one by reading your codebase.


In class we run `/init` on a copy of the course's tic-tac-toe project with its curated
CLAUDE.md temporarily removed, then diff what the generator produced against what the
instructor's file actually says. The generated file is respectable: it names the
modules, the commands, the test setup — everything derivable from the code. Now look
at what the *curated* file contains that the generated one cannot:


> *"The 1-based-to-0-based translation lives inside `Game` and never escapes its
> boundary."*
>
> *"`computer_ai.py` — `ComputerAI` exposes strategies as **static methods** only (no
> instances). … future strategies plug in by adding another static method and a
> dispatch entry in `main.py`."*

These are not facts *about* the code; they are **decisions** — boundaries the
maintainer wants preserved, extension patterns future work should follow. `/init` can
describe what is; only a human can say what must remain true. That is the working
definition of a good CLAUDE.md: *the intent that code cannot carry.* You will practice
exactly this judgment in Exercise 2, where improving a generated CLAUDE.md is a
graded deliverable.

A rule of thumb you will refine over the semester: if you find yourself typing the
same instruction into prompts twice, it belongs in CLAUDE.md. (The course's
medium-project retrospectives elevate this to a principle — "unique practices,
atypical conventions and project preferences should not have to be part of your
prompt" — and we will meet it again in Lecture 6.)

## 4. @-mentions and slash commands

Two pieces of context plumbing you will use constantly:

- **`@path/to/file`** in a prompt forces that file into the context before the model
  answers. It is the surgical alternative to hoping the agent reads the right thing.
  Use it when you know; let the agent explore when you don't. Resist the urge to @
  half the repository — every token competes for the window, and Lecture 6 will show
  you the bill.
- **`/command`** invokes a *skill*: a reusable prompt stored as a file. This is worth
  seeing once to be permanently demystified. The course repo's `grill-me` skill —
  which you will use for real in Project 0 — is thirteen lines, and its entire body
  is adapted from [Matt Pocock's public skills repository](https://github.com/mattpocock/skills):

> Interview me relentlessly about every aspect of this plan until we reach a shared
  > understanding. Walk down each branch of the design tree resolving dependencies
  > between decisions one by one.
  >
  > If a question can be answered by exploring the codebase, explore the codebase
  > instead.
  >
  > For each question, provide your recommended answer.

  That's it. A slash command is a prompt file. An entire elicitation methodology fits
  in a paragraph, versioned in the repo, identical every time it's invoked. When
  Lecture 4 leans hard on `/grill-me`, remember there is no machinery behind it —
  just these words, injected on demand.

## 5. Plan mode: cheap words before expensive edits

For any change bigger than trivial, Claude Code offers **plan mode**: the agent
explores and *proposes* — reading files, thinking out loud, producing a step-by-step
plan — but cannot edit until you approve. The workflow is: explore, plan, you read
the plan, approve (or push back), execute — and you can interrupt and steer at any
point during execution.


In class we do this live on the tic-tac-toe project with a real feature: adding a
`blocking_move` strategy alongside `random_move` in `computer_ai.py` (block the
opponent's imminent five-in-a-row if one exists, else fall back to random). A plan the
agent might propose looks like this:


> 1. Read `computer_ai.py` and its tests to match the existing strategy pattern
>    (static method taking a `Game`, returning a `(row, col)` tuple).
> 2. Add `blocking_move(game)`: scan for any cell that completes an opponent
>    five-in-a-row next turn; return it, else fall back to `random_move`.
> 3. Register the new strategy in `main.py`'s dispatch.
> 4. Add tests: blocks an imminent win in each direction; falls back cleanly when no
>    threat exists.
> 5. Run the test suite.

Now read it the way you would review a colleague's plan, because that is the skill:
step 2 hides a real design question — does "imminent" mean only four-in-a-row with the
fifth cell open, or also broken patterns like `X X . X X`? The plan is where you catch
that ambiguity for the price of a sentence; the diff is where it costs a rewrite.
Watch what plan mode buys:

- The plan surfaces the agent's *understanding* before any file changes. If it
  misread the strategy-dispatch pattern, you catch it in prose, not in a diff.
- The plan is a natural checkpoint for *you* to inject constraints ("static method,
  like the CLAUDE.md says"; "tests first, please") while they are still cheap.
- Approval converts the plan into the working contract for the execution phase.

The alternative — prompt-and-pray, straight to edits — sometimes works and is always
faster *when it works*. The course's transcripts contain both styles, and Exercise 1
has you watch what each costs. As a default posture for non-trivial work: plan first.
Words are cheaper than edits, and both are cheaper than rework.

## 6. The survival kit: watching your context

You now know the context window is finite, replayed, and billed. Claude Code gives
you four controls; learn them this week, understand them deeply in Lecture 6:

- **`/context`** — what is currently in the window, and how full it is.
- **`/cost`** — what this session has spent so far.
- **`/compact`** — summarize the conversation to reclaim space (lossy — a summary
  replaces the verbatim history).
- **`/clear`** — wipe the conversation and start fresh (CLAUDE.md is re-injected;
  everything else is gone).

A `/context` readout looks roughly like this (illustrative numbers):

```
CLAUDE.md + settings        1.4k tokens
conversation               17.9k
file reads (9 files)       31.2k
tool output                 6.8k
---------------------------------
total                      57.3k of 200k
```

Reading it is the skill: here, file reads dominate — nine files are being re-sent
with every single turn, including, probably, several the session no longer needs.
That is the moment `/compact` (or a fresh session) starts paying for itself.

Rule of thumb for now: when a long session starts feeling sluggish or the agent seems
to "forget" things it knew an hour ago, check `/context` before you blame the model.
You will be running Exercise 2 sessions this week; glance at `/context` occasionally
just to build the habit of knowing what your agent is carrying.

## 7. What we are deliberately NOT teaching yet

Claude Code has more machinery: sandboxes, hooks (run a command on events), subagents
(parallel agents with separate contexts), deeper skill patterns, MCP servers
(connecting external tools), plugins. They are real, they are useful, and they are
*deferred*. Each arrives in the semester when a project genuinely demands it — hooks
and subagents around week 9 with Project 2, MCP around week 12 with Project 3. The
`technical-concepts.md` reference in the course materials maps every one of these to
curated documentation when you get curious early. Curiosity is fine; just don't
mistake feature tourism for skill. The core loop, context discipline, and
verification carry you through Project 1 entirely.

## 8. A cautionary demo, and Exercise 2


We close with a deliberately bad prompt on the same tic-tac-toe project: *"fix the AI,
it plays bad."* The agent — obligingly, plausibly — guesses at what "bad" means and
produces a confident change that may or may not be what anyone wanted. One sentence of
specificity ("the AI should block an opponent's immediate win; add that as a new
strategy, keep random_move as the fallback") transforms the outcome. Hold that
contrast; Lecture 4 is entirely about it.


**Exercise 2** launches today: on an unfamiliar open-source codebase (announced with
the exercise spec), you will use Claude Code in *comprehension* mode — explore it,
improve its generated CLAUDE.md with intent the generator couldn't know, answer an
architecture question set with file-path citations, and **catch the agent being wrong
at least once**, with evidence. No code modifications; the first agentic build is
Project 1. Due before Lecture 5.

## Questions to think about

1. What belongs in CLAUDE.md vs. in the prompt vs. in a spec file? (Lecture 4 gives
   this a principled answer; sketch your own first.)
2. Which permission would you *never* auto-accept, even in week 15? Why that one?
3. `/init` read every line of the code and still missed things. What *category* of
   knowledge did it miss, and why can't any amount of code-reading recover it?

## Before next lecture

- **Required:** the course *Prompting Cheat Sheet* (in your handouts) — Lecture 4
  walks it principle by principle; arrive having read it.
- **Required:** *Claude Code Best Practices* (code.claude.com/docs/en/best-practices).
- **Recommended:** Claude Code docs on permission modes, memory/CLAUDE.md, and plan
  mode — the curated links are in the course's `technical-concepts.md`.
- **Exercise 1** is due before next lecture. **Exercise 2** is now open.
