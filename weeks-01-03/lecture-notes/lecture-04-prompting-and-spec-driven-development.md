# Lecture 4 Notes — Prompting + Spec-Driven Development

> Agentic Software Engineering · Week 2, second meeting
>
> **The one idea:** the two 9×9 attempts in the course archive are the same task with
> different discipline — requirements and specifications, not prompt cleverness,
> separate the outcomes.

## 1. A tale of two attempts

The course archive contains two attempts at the same job: scale a working 3×3
tic-tac-toe game to a 9×9 board with a five-in-a-row win rule. You read excerpts of
both for Exercise 1. Put their opening prompts side by side.

**Attempt 1** opens with everything in one paragraph:

> *"I have a tic tac toe game with a standard 3 by 3 board that I want to adapt to a
> larger game. Scale the game up for a 9 by 9 board where you need to get 5 in a row
> to win. Before changing the code, revise the @SPECS.md and @CLAUDE.md files to
> reflect the adaptations. Picking a move should now be a two step process where a
> player first picks a column then a row to play in…"*

Notice what this prompt is *not*: it is not careless. It asks for documentation
updates before code — a good instinct. But every requirement the project will have is
compressed into one breath, delivered once, never systematically examined. And here is
the forensic detail worth the price of admission: that prompt asks for **column, then
row**. The specification the project shipped with says, in its input-handling section,
that the player enters the **row first, then the column**. Somewhere between the
opening paragraph and the final product, a requirement quietly flipped. Nobody decided
that in a design conversation; it drifted. That is what requirements-as-a-paragraph
buys you: whatever survives the session.

**Attempt 2** is a do-over, and its opening move is diagnosis:

> *"This is a 3x3 tic tac toe game. @SPECS.md gives a good intro to what is developed,
> but it is sub-par for what a SPECS file should contain. I want to change the board
> to a 9x9 board where you need to get 5 in a row to win. Help me fully describe the
> specs of the program by re-writing @SPECS.md. … Use /grill-me to fully flush out the
> SPECS file so we don't have to change it in the future."*

Read the ambition in that last clause: *so we don't have to change it in the future.*
The spec is being written as a **contract**, before any code, by interrogation rather
than by recollection. The conversation that follows has a completely different shape
from Attempt 1's: the *agent* asks the questions, the human makes decisions, and each
decision closes a branch of the design tree. Later, the same discipline produces a
Concept of Operations by the same method — and that document goes on to outlive the
codebase entirely (section 4).

Neither attempt "failed." Attempt 1 produced a working game. But one of these
processes produces requirements that hold their shape, and the other produces a second
attempt.

## 2. The five principles

The course cheat sheet distills prompting-for-development into five principles. You
have read it; here is each principle with the reasoning that makes it stick.

**1. Provide specific instructions.** The model cannot read your mind, and — Lecture
1 — it fills every unspecified gap with the *plausible*, not the intended. "Fix the
bug with the new login UI" invites a guess. "When using the new login UI, the submit
request does not seem to go through; check that the submit request is handled properly
so the page reacts correctly" aims the same capability at the actual problem.
Specificity is not verbosity: one precise sentence beats three vague ones.

**2. Spec-driven development.** For anything beyond a small task, move the details
out of the prompt and into a document, then point the prompt at the document: "Use the
login section in @website-spec to implement the login page." The prompt names the
work; the spec carries the truth. Sections 3 and 4 are about why this scales the way
nothing else does.

**3. Give the agent the tools to check itself — and encourage their use.** "Add a
login page. Use the unit tests to check your implementation; verify the UI with the
browser tools at your disposal." An agent that can run the tests catches its own
plausible-but-wrong output before you ever see it. This principle returns at full
strength in Lecture 6 (verification) — and note that it presumes the tests exist and
are trustworthy, which is your job.

**4. Promote positive behaviors instead of only restricting.** "Don't use bulleted
lists in the report" leaves the model steering around a wall. "Strive for complete
paragraphs that flow together" gives it a direction. Prohibitions have their place —
safety rules are prohibitions — but a prompt that is mostly "don't" produces cramped,
evasive output. Say what good looks like.

**5. Point the agent at existing patterns.** "Look at how the existing widgets on
the dashboard are built (@HotDogWidget is a good example); follow that same pattern to
add a calendar widget, using only libraries already in the project." This is the
cheapest specification you will ever write: the pattern *is* the spec. It keeps new
code consistent with the codebase and biases the agent toward reuse over reinvention.
You saw the instructor use exactly this move in the plan-mode demo last lecture
("like `random_move`, static method, registered in the dispatch").

Three useful moves follow from these principles:

- If you do not know the implementation path, describe the outcome you want and ask
  the agent to recommend a route before it edits.
- Ask how the result can be tested and request representative inputs, boundaries, and
  failure cases.
- Ask the agent to draft documentation, then review that prose against the behavior
  and the intended reader.


Last lecture's failure demo — *"fix the AI, it plays bad"* — violated principle 1 and,
depending on your reading, principles 3 and 5. It's worth a minute to rewrite it
yourself using at least two principles before reading on; Exercise 1's question 2 asks
you to do this on a real transcript excerpt.

## 3. Requirement elicitation: make the agent interview you

The deepest habit shift this course asks of you is this: **before building, make the
agent ask *you* the questions.**

The mechanism could not be simpler. The `grill-me` skill you saw in Lecture 3 is a
thirteen-line prompt file — "interview me relentlessly… walk down each branch of the
design tree… for each question, provide your recommended answer." Invoked before work
begins, it inverts the flow of the conversation: instead of you trying to remember
every requirement (Attempt 1), the model — which has read the codebase and has seen
ten thousand projects like yours — probes for the decisions you haven't made yet.

Watch it work in Attempt 2's ConOps session. The rhythm of a grilling round looks
like this (condensed from the real transcript — note that the skill's last line makes
the agent *recommend* an answer to every question it asks):

> **Agent:** Who is this ConOps for — a grader, future developers, a non-technical
> stakeholder? What structure should it follow? *Recommendation: treat it as a formal
> learning artifact with standard ConOps sections.*
>
> **Human:** Formal learning artifact; IEEE/AIAA ConOps sections; new `CONOPS.md` at
> the project root.
>
> **Agent:** What is its relationship to the existing SPECS.md — may it reference it?
> Which operational scenarios should it narrate, and which actors exist?
>
> **Human:** Restate whatever is needed but *do not reference SPECS* — the ConOps is
> implementation-independent. Scenarios: solo-vs-computer win, hot-seat two-player,
> tie, invalid-input recovery. Actors: solo player, hot-seat pair, computer opponent.

Each answer closes a branch of the design tree — and one of them turns out to be
load-bearing:

> *"SPECS.md is meant to provide useful information that might need to be re-stated in
> the ConOps. Do not reference SPECS in the ConOps as ConOps is implementation
> independent."*

That single decision — the ConOps must stand alone, implementation-free — is what
makes section 4's punchline possible. It would never have been *stated* if no one had
asked. The economics of this are absurdly favorable, as the course's medium-project
retrospective puts it: for the cost of a few hundred tokens of questioning, you avoid
tens of thousands of tokens of redevelopment. Elicitation converts unknown-unknowns
into decisions *before* they become rework.

(And when is grilling a waste of time? Small, reversible, well-understood tasks.
Discipline scales with stakes — a theme Lecture 6 makes explicit.)

## 4. ConOps vs. SPECS — and the punchline

Two document kinds recur throughout this course, and they answer different questions:

- A **Concept of Operations (ConOps)** describes the system from the *user's*
  perspective: what it is for, who uses it, what the scenarios of use look like. It is
  implementation-independent by design — a good test is whether a non-programmer could
  read it and confirm "yes, that is the game I want."
- A **specification (SPECS)** is the *behavioral contract*: module responsibilities,
  input handling rule by rule, rendering conventions, testing requirements. The 9×9
  spec even legislates its own authority — it is "the single source of truth," and
  tests may assert *tighter* than the spec but never looser.

The hierarchy is ConOps → spec → code and tests, each level more concrete, each
derivable-from and answerable-to the one above. See the difference by putting the
*same behavior* — entering a move — at both altitudes:

> **ConOps altitude:** "The player chooses a row and then a column; while the column
> is being chosen, the display marks the selected row."
>
> **SPECS altitude:** "Validate row input: must be a digit 1–9, and `row_has_space(row)`
> must return `True`; on failure, re-prompt. … The row choice **sticks** once
> accepted. There is no back-out from the column prompt to the row prompt within the
> same turn."

The first tells you what the experience *is* — a user could confirm it. The second
legislates behavior precisely enough to write a failing test against — including the
edge nobody would think to ask about (can you back out of a chosen row? no). Both
sentences describe one feature; neither can do the other's job.

Now the punchline. The course archive contains a **Java** implementation of the 9×9
game — Maven build, JaCoCo coverage enforcement, 100% branch coverage — built from
*the same ConOps* that Attempt 2 produced for the Python version. The ConOps never
mentions Python, so nothing in it had to change. Requirements elicited once, specified
once, implemented twice.

> **Specs are portable; prompts are not.** The ConOps outlived the codebase.

If you remember one sentence from this lecture, that is the one.

## 5. Prompts shrink as artifacts grow

Here is the trajectory this all points to, visible in the course's medium-size project
(a personal-finance tracker built five times over). Watch the *development prompt* —
the thing typed to start each unit of work — evolve across passes:

First pass:

> *"Milestone 0 is complete, now implement milestone 1. /grill-me. When complete,
> allow me to review the code before transcribing and committing."*

Fifth pass:

> *"Implement Wave 2. /grill-me"*

The prompt got *shorter* while the results got *better* — personal satisfaction 8/10
on the final pass, "best end product and best understanding of the end product so
far." How? Everything the first-pass prompt carried inline had migrated into durable
artifacts: the ConOps holds the requirements; the development plan holds the wave
structure and the locked decisions; CLAUDE.md holds the conventions and the
development cycle. The prompt no longer *specifies* anything. It just names which
piece of the standing specification to execute next and invokes the elicitation
habit.

That is the course's central trajectory in miniature: **move context out of the
conversation and into artifacts.** The conversation is ephemeral and re-billed every
turn; artifacts persist, port across sessions — and, as the Java game shows, across
languages. Lecture 6 completes this picture with the memory taxonomy and the cost
data.

## 6. Project 0 launches: spec-driven development, on yourself

Everything above applies to a project with no compiler at all — and today you start
it. **Project 0** is a personal knowledge base (PKB) on agentic software engineering,
organized around your own interests, that you will maintain all semester.

The format is Google's **Open Knowledge Format (OKF)**: plain markdown files with a
YAML frontmatter block (one required field — `type` — plus recommended
title/description/tags/timestamp), two reserved files (`index.md`, a directory
listing; `log.md`, a chronological change history), and ordinary links, with a rule
you should savor: *broken links are legal* — they mark knowledge you haven't written
yet. Conformance is deliberately light, the format is Obsidian-viewable, and the spec
explicitly targets knowledge "authored by humans, generated by AI agents." A complete,
conformant concept note is nothing more than this:

```markdown
---
type: Concept
title: The agent loop
description: The while-loop-with-tools that turns a predictor into an actor.
tags:
  - agents
---

An agent is a language model called in a loop by a harness…
See also [context windows](/concepts/context-window.md).
```

One required field (`type`), a few recommended ones, ordinary markdown below. A tiny
worked example bundle ships in your starter repo; open it in Obsidian before
designing your own.

The kickoff *is* this lecture applied to a markdown stack: run a grill-me elicitation
about your KB's purpose and organization *before creating any files*; write a
one-page spec (folder taxonomy, your `type` vocabulary, note granularity, linking
conventions); have Claude scaffold the bundle from the spec; seed it with five notes
from the weeks 1–3 material in your own words. The stretch goal — a conformance
checker the agent can run — is principle 3 pointed at knowledge work.

The full spec is `project-0-pkb-kickoff.md`; kickoff is due at the end of week 3,
and the PKB has checkpoints in weeks 6, 10, and 15.

## Questions to think about

1. The ConOps never mentions Python — what exactly did that buy? Name something else
   a team could buy with the same property.
2. When is `/grill-me` a waste of time? Construct the smallest task for which you'd
   still use it.
3. Why did the development prompt *shrink* pass over pass? What, specifically, was
   each deleted clause replaced by?

## Before next lecture

- **Required:** Anthropic API docs — *Messages API* and *Tool use*, in depth this
  time. Exercise 4 is built directly on these pages.
- **Required:** Thorsten Ball, *How to Build an Agent* (ampcode.com) — a working
  code-editing agent in ~300 lines of Go. You will build the Python equivalent.
- **Recommended:** re-read the "agents" section of *Building Effective Agents*;
  Anthropic's *Writing effective tools for agents — with agents*.
- **Project 0** is now open (kickoff due end of week 3). **Exercise 2** is due before
  next lecture.
