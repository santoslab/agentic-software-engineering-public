# Agent Skills: Packaging a Method So an Agent Can Follow It

> Software-engineering module. Companion reading for the lecture; self-contained.
> Assigns the skills exercise ([`../exercises/exercise-03-a-skill-for-specs-from-conops.md`](../exercises/exercise-03-a-skill-for-specs-from-conops.md)). The skills
> it uses are in [`../demos/lecture-06-skills/`](../demos/lecture-06-skills/).
> The readings for the next meeting are at the end.

## Where we are: a prompt we keep typing

Five lectures have built one method. We audit a document before we build from
it, report the gaps as a numbered list with a recommendation for each, let the
developer rule, propose amendments, and only then write. Here is the reference prompt for its first step, taking a sketch to a
concept of operations:

> Read `CONOPS-sketch.md` and the process documents. I want a `CONOPS.md` 1.0
> that realizes this sketch as a full-skeleton concept of operations. Before
> proposing anything, run the audits in `process/conops-audit.md` and
> `process/spec-audit.md` on the sketch (DEV-8) and report the gap list per
> RPT-1 — numbered, each with your recommended resolution. Then stop and wait
> for my rulings.

Two things about that prompt are worth noticing. First, it has already been
used twice, word for word: on tic-tac-toe earlier in the course (*Specifying a Game*), and on
Reversi in Project 1. It works on any sketch, because nothing in it
is specific to either game; and step 2's prompt, for `SPECS.md`, is its twin.
Second, most of the method is not in the prompt at all: it is in the files the
prompt names — what the audits check, and what a gap list must contain. Package the prompt and those files together and you have exactly the
shape of an **agent skill**. Today is about that shape: what a skill is, how a
harness loads one, when a skill is the right tool and when it is not, how to
write one, and — the part the rest of the course cares most about — how to tell
whether it works.

The worked example is a skill we built before this lecture and evaluated the
way we evaluated a program earlier in the course (*Verifying a Game*): against a key written before
the runs were read. It takes a concept-of-operations sketch to a gap list and
stops. Its first version failed in instructive ways, and its second version
works on the sketch it was tuned on and only partly works on one it had never
seen. Both results matter.

## What a skill is

An **agent skill** is a folder of instructions that teaches an agent how to do
one kind of task, and that the agent loads only when that task comes up. The
agent sees every installed skill's description all the time; it reads the
skill's body only when a task matches the description, or when you type the
skill's name as a command (`/name`). The rest of this section looks at the
folder; the loading is the subject of "How it works" below.

A skill is a folder. Its one required file is `SKILL.md`: a short block of
YAML front matter, then Markdown instructions.

```markdown
---
name: conops-from-sketch
description: Turns a concept-of-operations sketch into a governed CONOPS.md
  by the audit-first method … Use only when the developer explicitly asks to
  turn a sketch into a CONOPS. Not for explaining what a ConOps is,
  summarizing a sketch, or editing an existing CONOPS.md.
---

# CONOPS from a sketch
…instructions…
```

The front matter carries two fields every harness reads: a `name` (lowercase,
hyphens; it is also the folder's name) and a `description` (what the skill does
and when to use it). The body is the procedure. Anything else in the folder — a
template, a checklist, a script, reference data — is **bundled** with the
skill, and the body refers to it by relative path. Our skill's folder is:

```
conops-from-sketch/
├── SKILL.md                  the procedure: three phases (audit, apply rulings, write), each ending in a stop
├── probes.md                 questions to ask of any sketch, opened during phase 1
├── gap-report-template.md    the report's shape, opened when reporting
├── checklist.md              a fallback audit, opened only if the repo has none
└── agents/openai.yaml        Codex setting: only you may start it
```

This lecture follows two versions of one skill throughout. **v1** (`conops`) is
the obvious skill: a one-line description, "Helps with CONOPS documents.", and a
body that says to write the document and fill any missing details with sensible
defaults; the model may start it on its own. **v2** (`conops-from-sketch`, the
folder above) is our method, packaged: audit the sketch, list the gaps, stop for
the developer's rulings, then write; only the developer can start it. v2's
first draft (iter1) was tested and improved once; the second draft (iter2) is
the final version. "Creating a skill" below shows both in
full.

The idea is older than the name. Coding agents first had **custom
instructions**: one always-loaded file per project (`CLAUDE.md`, and in other
tools `AGENTS.md`). Then came **custom slash
commands**: saved prompts. A Markdown file in `.claude/commands/x.md` became
the command `/x`; typing it made the file's text your prompt. Only the user
could start one. In October 2025 Anthropic introduced **Agent
Skills**, which added two things to the saved prompt: a folder of supporting
files, and a description the *model* reads, so that the agent can decide on its
own that a skill applies. Anthropic then published the format as an **open
standard** ([agentskills.io](https://agentskills.io)), and many other agents —
Codex, Gemini CLI, GitHub Copilot, Cursor, and more — now read the same
`SKILL.md` folders. In current Claude Code, commands have merged into
skills. The Claude Code skills documentation
(`code.claude.com/docs/en/skills`, fetched 2026-09-27) puts it plainly: "Custom
commands have been merged into skills. A file at `.claude/commands/deploy.md`
and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work
the same way." Old command files keep working; when a skill and a command share
a name, the skill wins. A command file now accepts the same front matter as a
skill (all but `name` and `paths`), so the model can start it too: it is a skill
without a folder. The docs prefer a skill for new work, because only a skill can
bundle supporting files.

A useful way to think about the difference between these files is the
psychologist's split between kinds of memory. `CLAUDE.md` is closer to
*declarative* memory: facts about this project that should always be in mind. A
skill is closer to *procedural* memory: how to do a particular thing, recalled
when that thing comes up. That is also why a skill costs so little when it is
not in use, as we will see.

## Skills and their neighbours

A harness offers several ways to shape what an agent does. They overlap, and
choosing the wrong one is the most common mistake people make with skills.

| Mechanism | What it is | Loaded | Who triggers it | Use it for |
|---|---|---|---|---|
| `CLAUDE.md` / `AGENTS.md` | project memory: facts and standing rules | always, at session start | nobody; it is always there | what every session needs: how to build and test, where the specifications are, the two rules |
| slash command (now a skill) | a saved prompt | when typed | the user | a procedure the user starts on purpose |
| **skill** | a procedure plus its files | description always; body on use | the user (`/name`) or the model (by description) | a recurring, multi-step procedure with its own materials |
| subagent | a separate agent with its own context, prompt, and tools | when delegated to | the model, or the user | work whose *intermediate* output would clutter the main context: a search, a review |
| MCP server | a tool contract to another program | tool descriptions at start | the model, when it calls a tool | *capabilities* the agent lacks: a database, an issue tracker, a browser |
| hook | a shell command the harness runs on an event | on the event | the harness, deterministically | what must happen every time, whatever the model decides |
| plugin | a package of any of the above | when installed and enabled | — | distributing a set of these to other people |

Three distinctions do most of the work.

- **Skill or `CLAUDE.md`?** If every session needs it, it belongs in
  `CLAUDE.md`. If only some sessions need it, and it is more than a line or
  two, a skill keeps it out of the context until it is wanted. The tic-tac-toe starter's `CLAUDE.md` is short: two standing rules and a map of `process/`, which holds the rules. It imports three of them with `@path` (loaded every session) and only points to the two audits, which the agent reads when needed — so a `CLAUDE.md` line pointing to a procedure file costs about as little as a skill's description. The main gain of a skill is structure: each procedure lives in its own named folder, with its templates and checklists beside it, instead of in a `CLAUDE.md` that keeps growing. Along with that come a name you can type (with arguments), a description in a standard place that the agent matches tasks against, its own controls (who may start it, which tools run without prompts), and a folder you can reuse in another repository or share.
- **Skill or MCP?** A skill tells the agent *how* to do something with the
  tools it already has. An MCP server gives it a tool it does not have. The two
  combine well: a skill can say "use the tracker's tools in this order".
- **Skill or hook?** A skill is text the model reads, so following it is a
  probability, not a guarantee. A hook is a program the harness runs. If
  something *must* happen — the tests run before every commit, a file is never
  edited — make it a hook or a permission rule, not a sentence in a skill.

## When to write a skill, and when not to

Write one when all three of these hold:

1. **You do it more than once.** A procedure you have typed out three times is
   a candidate; a one-off request is not. Write the one-off request as a
   prompt.
2. **The model does not already do it the way you need.** Asking an agent to
   "summarize this file" needs no skill. A skill earns its place by encoding
   something the model would *not* do by default: our method's rule that a
   recommendation is not a ruling, a house report form, a set of probes that
   find what a first reading misses.
3. **It is procedural and has materials.** Steps, stops, a template, a
   checklist, a script. If it is a single fact, it belongs in `CLAUDE.md`.

And do not write one when the requirement is that something *always* or *never*
happens. That is enforcement, and enforcement belongs to hooks, permission
rules, and tests. We will see today that a skill governs only the requests that
invoke it.

## Two skills in the wild

Before we build one, look at two published skills, how they changed, and how
their authors knew whether a change helped. Both are widely installed; they are
almost opposite in purpose and in how they were evaluated.

### grill-me: make the agent question you about your plan

Matt Pocock's `grill-me` (in `mattpocock/skills`) makes the agent interview the
developer about a plan until they share an understanding. Its lineage runs
through a post by Thariq Shihipar of the Claude Code team (December 2025),
recommending that you ask Claude to interview you before it writes a
specification. The skill's first version, in February 2026, was two sentences with no front matter:

> Interview me relentlessly about every aspect of this plan until we reach a
> shared understanding. Walk down each branch of the design tree, resolving
> dependencies between decisions one-by-one.

Its history since then is a short course in skill writing:

| When | Change | Stated reason |
|---|---|---|
| Mar 2026 | front matter added, with a description listing triggers ("…or mentions 'grill me'"); "If a question can be answered by exploring the codebase, explore the codebase instead." | "add missing frontmatter" |
| Mar 2026 | "For each question, provide your recommended answer." "Ask the questions one at a time." | none measured |
| May 2026 | **split**: `grill-me` becomes a one-line, user-invoked wrapper (`disable-model-invocation: true`) around a new model-invoked skill, `grilling`, that other skills can call | consolidation |
| Jul 2026 | "Interview the user" becomes "**Grill** the user"; "Do not enact the plan until I confirm…" | "grill" already means relentless questioning to the model; a hard stop |
| Jul 2026 | "explore the codebase instead" becomes a split: *facts* you look up, *decisions* you ask me | inside another skill, the old line "reads as license to answer questions autonomously" |
| Jul 2026 | one question at a time becomes **rounds**: every question whose prerequisites are settled, asked at once | "Same 13 questions land in ~3 rounds instead of 13" — not measured |
| Aug 2026 | "Run the `/grilling` skill" becomes "Call the Skill tool with \"grilling\"" | "Naming the tool directly gets a higher hit rate" — not measured |

Three of those changes are worth a second look. The facts-versus-decisions
rewrite is our method's rule in other words: *a question the repository answers
is answered by reading it; a decision is the developer's*. The switch to rounds
overturned the skill's own rule, "ask one question at a time", whose reason had been added in June ("Asking multiple questions at once is bewildering"); the switch rested on a claim nobody measured. After the change a user filed an
issue asking "Can we get the old grill-me back?": a user caught the regression;
no test did. Rounds stayed; the skill's docs now tell anyone who prefers the
old behavior to add "When grilling, ask one question at a time." to their
`CLAUDE.md`, and the issue (#831) is still open. And the
"Skill tool" wording broke portability twice: in harnesses with no tool of that
name, such as Codex, it has nothing to bind to, and in Claude Code an open
issue (#1052) reports that the wrapper's own `disable-model-invocation: true`
forbids the Skill-tool call its body asks for: "Skill grill-me cannot be used
with Skill tool due to disable-model-invocation." The wrapper blocks itself. As of 2026-09-30 both reports (#1052, and #1123 for
Codex) are open and the line is unchanged. (The Skill
tool and `disable-model-invocation` are explained in "How it works" and
"Automatic invocation" below.)

How did the author know any of it worked? He says so directly. His guidance on
writing for agents — the human-facing page for his own skill-writing skill, in
`docs/productivity/writing-for-agents.md`, general advice rather than a
statement about `grill-me` — reads:

> There is no automated eval here; the check is a manual run plus the
> failure-mode vocabulary as a diagnostic.

We found no systematic evaluation of `grill-me` anywhere: not in the
repository, its history, its issues, or its author's posts. The evidence is the
author's own use (on his blog: "These grilling sessions often last about 45 minutes"), the
skill's popularity, and a large volume of user feedback, some of which changed
it.

Read the current version for yourself (the slides show it in full, except one repeated example, as of commit
`d81f3a1`, 2026-09-29): `skills/productivity/grill-me/SKILL.md` is the one-line
wrapper, and `skills/productivity/grilling/SKILL.md` is the procedure — design
tree, rounds, facts versus decisions, and the final "do not act on it until the
user confirms". Each skill also ships an `agents/openai.yaml` for Codex, and the wrapper's file sets `allow_implicit_invocation: false`: the same switch our v2 needed
(see "Where skills live across harnesses").

### ponytail: make the agent write less code

`ponytail` (DietrichGebert/ponytail) exists because coding agents over-build.
Its README's example: asked for a date picker, an agent "installs flatpickr,
writes a wrapper component, adds a stylesheet, and starts a discussion about
timezones"; with ponytail, the answer is `<input type="date">` — the browser
has one. The skill tells the agent to be "a lazy senior developer": question whether code needs to exist, reuse what is there, prefer
the standard library, write the shortest diff that works. It is packaged as a
**plugin**: the skill, five helper skills, hooks, a status line, and an MCP
server.

Its history is driven by measurement. The first version said "Say less", and it
did produce less code than its rivals. But its authors' own benchmark showed it
losing on total tokens to a competing skill: the model wrote short code and
then, in its reply to the user, long essays defending each simplification, and the prose ate the savings.
The fix was not a stronger adjective but a quantified cap. Today's file reads:

> Code first. Then at most three short lines: what was skipped, when to add it.
> No essays, no feature tours, no design notes. If the explanation is longer
> than the code, delete the explanation …

Its description was rewritten for triggering and tested on twelve labelled
prompts: it started on 2 of 6 coding prompts before and 6 of 6 after, with its behavior on the 6 non-coding prompts
unchanged, after adding "Use on ANY coding task … Do NOT use for non-coding
requests" (the commit reports the numbers; the test harness itself is not in
the repository). A laziness bug ("Dangerously lazy", filed by a user: asked to fix
a bug, the agent patched only the caller the report named and left the same bug
in every other caller) became a rule that makes the root-cause fix the *lazier*
one ("one guard in the shared
function is a smaller diff than a guard in every caller"), and ponytail's published benchmark results
reports that a plain-prose version of the same advice did not move the score.

Ponytail also shows what a skill alone cannot do. Ponytail must hold on every
coding turn, but a skill applies only if the model starts it, and after compaction (summarizing a long conversation to free space) Claude Code re-adds used skills only within a budget, so older ones
can drop out (both are explained in "How it works" below); other agents ponytail
supports may not re-add skills at all. Ponytail does not rely on the skill being started: a
`SessionStart` hook injects the rules at startup and again after every
compaction, a `UserPromptSubmit` hook tracks the mode — how strict ponytail is set to be: *lite* names the lazier option and lets you pick, *full* (the default) enforces it, *ultra* deletes before adding and challenges the requirement — and a `SubagentStart`
hook injects the rules into every subagent, because, as its source says,
session-start context "is parent-thread only and never reaches subagents". (The research agent that wrote our research notes received that injection, because the
instructor has the plugin installed — on a task that was not coding at all.)

The two skills pull in opposite directions — `grill-me` stalls until the human
decides; `ponytail` says "ship the lazy version and question it in the same
response" — and each is right for its job. We will come back to how differently
they were evaluated.

## Using skills

**Where they live.** According to the documentation, Claude Code finds skills
in these places:

| Location | Scope | Invoked as |
|---|---|---|
| `~/.claude/skills/<name>/SKILL.md` | you, in every project | `/<name>` |
| `.claude/skills/<name>/SKILL.md` in a repository | everyone who clones it | `/<name>` |
| `<subdir>/.claude/skills/<name>/SKILL.md` | work in that part of a monorepo | `/<name>` |
| a plugin's `skills/<name>/SKILL.md` | everyone who installs the plugin | `/<plugin>:<name>` |
| `.claude/skills/` in a system folder only an administrator can write (`/Library/Application Support/ClaudeCode/` on macOS, `/etc/claude-code/` on Linux, `C:\Program Files\ClaudeCode\` on Windows), usually pushed out by device management | every user on the organization's machines | `/<name>` |

A project skill is committed with the code, so a team shares it the way it
shares `CLAUDE.md`. When two locations hold the same name, the organization's
beats yours and yours beats the project's. A plugin skill carries its plugin's
name as a namespace, so two plugins can each have a `review` skill without
colliding. The documentation also says Claude Code watches the skill folders,
so an edited `SKILL.md` takes effect in the running session without a restart.

**Invoking.** Type `/` and the skill's name. (Our runs used `/name` as the whole prompt of a non-interactive run (`claude -p`), and it worked.) Text after the name is passed
as the skill's **arguments**. Per the documentation, the body can place them
with `$ARGUMENTS` (all of them) or by position (`$ARGUMENTS[0]`, or the
shorthand `$0`, `$1`). If the body has no placeholder, Claude Code appends
`ARGUMENTS: <what you typed>` to the end, so the model still sees it. Our skill
takes an optional path, `/conops-from-sketch drafts/CONOPS-sketch.md`, and its
front-matter field `argument-hint` shows the user what to type. A skill can
also be invoked by the model on its own, which is the next section's subject.

**Listing and inspecting.** Typing `/` opens the menu of commands and skills;
asking the agent "What skills are available?" works too, because the model can
see their descriptions (the documentation's own troubleshooting step). The
`/context` command shows how much of the context the skill listing takes, and
`/skill-doctor` reports what each skill costs and how often it is used. To
inspect one, read its folder: it is plain text, and reading it is the only way
to know what it will tell your agent to do.

## How it works: what the harness actually does

This is the part most introductions skip, and it explains nearly everything
else — why a skill is cheap, why it sometimes is not started, why it fades in a
long session.

Two kinds of evidence appear in this section, and they are marked. Some of it
is **what our transcripts show** (Claude Code 2.1.281): the `init` event, the
`Skill` tool call, the injected body, the files each run read. The rest is
**what the documentation says**: the Claude Code skills page,
`code.claude.com/docs/en/skills`, fetched on 2026-09-27. The documentation's
numbers and field lists change between versions; check them against the current
page before relying on them.

**At session start, only the metadata.** The harness scans the skill folders
and puts each skill's `name` and `description` into the model's context — not
the body, not the bundled files. You can see this in a headless run. With
`claude -p … --output-format stream-json --verbose`, the first event of every
run is an `init` event, and ours listed:

```json
{"type":"system","subtype":"init","model":"claude-sonnet-5",
 "claude_code_version":"2.1.281",
 "skills":["conops","deep-research","design", … ,"run-skill-generator"],
 "slash_commands":["conops", … ,"clear","compact","context","init", …], …}
```

`conops` is our skill, installed in the run's `.claude/skills/`; the rest are
skills that ship with the harness. (The headless documentation describes the
`init` event as reporting the model, tools, MCP servers and plugins; the
`skills` field is what we observed in version 2.1.281.) The event lists names
only; the descriptions reach the model in its context, which the transcript
does not record. According to the documentation, the descriptions share a
budget: each entry's description is cut at 1,536 characters, and the whole
listing is held to about 1% of the model's context window; when it overflows,
Claude Code drops the descriptions of the skills you use least, and a skill
without its description cannot be matched to a request. (The documentation does
not say how use is counted. Observed on one machine: Claude Code keeps a
per-user count of each skill's invocations, with the time of its last use, in
`~/.claude.json` under `skillUsage`.)

**On use, the body.** When the model decides a skill applies, it calls a tool
named `Skill`. From the transcript of one of our trigger tests, where the
prompt was the ordinary sentence "Turn CONOPS-sketch.md into CONOPS.md":

```json
{"type":"tool_use","name":"Skill","input":{"skill":"conops"}}
{"type":"tool_result","content":"Launching skill: conops"}
{"type":"user","isSynthetic":true,"message":{"content":[{"type":"text",
  "text":"Base directory for this skill: …/.claude/skills/conops\n\n
          Turn the CONOPS sketch into CONOPS.md. Use the standard ConOps
          sections and write it professionally. Fill in any missing details
          with sensible defaults so the document is complete.\n"}]}}
```

The body arrives as a message in the conversation, prefixed with the skill's
directory so that relative paths resolve. When the *user* types `/conops`, the
same body is injected without the model having to choose it.

**Bundled files, on demand.** The body says "work through
[probes.md](probes.md)"; the model then reads `probes.md` with its ordinary
Read tool, when it reaches that step. This three-level loading — metadata
always, body on use, files when the body sends the model to them — is called
**progressive disclosure**, and our transcripts show it: our second version's
runs opened `probes.md` and `gap-report-template.md` by path, after the phase-1
instructions sent them there, and in its first iteration two of three runs also
opened `checklist.md`, which they did not need. One sentence in the body
("leave the bundled checklist unopened" when the repository has its own audit)
brought that to zero of three. The agent knows the repository has an audit
because the same step tells it to look in `process/` for audit files; here it
finds `process/conops-audit.md` and `process/spec-audit.md` and uses those. A bundled file you tell the model not to open
costs nothing.

**The cost model.** Three costs, paid at different times:

| What | When it is paid | How much |
|---|---|---|
| name + description | every turn of every session where the skill is installed | a few lines per skill |
| body | from the moment of invocation, for the rest of the session | the length of `SKILL.md` |
| bundled files | only when read | their length |

This is why a long reference belongs in a bundled file, not in the body, and
why a description should be short and specific. Ponytail's authors cut their
file from 115 to 95 lines partly for this reason: "Smaller file cuts per-read
and per-session-injection cost."

**Persistence and compaction.** Once injected, the body is part of the
conversation. The documentation: "the rendered `SKILL.md` content enters the
conversation as a single message and stays there across later turns. … Claude
Code does not re-read the skill file on later turns, so write guidance that
should apply throughout a task as standing instructions rather than one-time
steps." In a long session it competes for the model's attention with everything
that came after it. When the context fills and the conversation is summarized,
the documentation says Claude Code re-attaches the most recent invocation of
each skill, but only its first 5,000 tokens, and all re-attached skills share
25,000 tokens, most recent first; in a session that invoked many skills, the
older ones can drop out entirely. The documentation's advice for a skill that
seems to stop working is to strengthen it, re-invoke it, or "use hooks to
enforce behavior deterministically". That is ponytail's choice: its
`SessionStart` hook fires on `startup`, `resume`, `clear` and `compact`, and
puts the full rules back every time.

**Dynamic context: `` !`command` ``.** A line in the body of the form `` !`git
log --oneline -5` `` is run by the harness *before* the body reaches the model,
every time the skill starts, and its output replaces the line. The model does not ask for it and never sees
the command, only the result.
It is a cheap way to give a skill live context (the current branch, the files
in `process/`), and — because it runs a shell command — it is also the first
thing to read when you inspect someone else's skill. (This is the
documentation's description; our evaluation did not use `!`. According to the
same page, you or an administrator can turn the feature off with the
`disableSkillShellExecution` setting, and each command is still checked against
your permission rules: if a rule does not allow it, or the command fails, the
whole skill does not start.)

**Other Claude Code extensions in the front matter.** The documentation lists
these fields as Claude Code's, beyond the portable standard:

| Field | Effect |
|---|---|
| `disable-model-invocation: true` | only the user can invoke it (`/name`); the documentation says this "removes the skill from Claude's context entirely" — though the name still appears in the `init` event's list |
| `user-invocable: false` | the model can invoke it; it is hidden from the `/` menu |
| `allowed-tools` | tools the model may use without asking permission during the turn that invokes the skill; the grant clears at your next message (our skill: `Read Grep Glob`) |
| `disallowed-tools` | tools removed while the skill is active |
| `argument-hint`, `arguments` | the hint shown when the user types `/name`; named arguments |
| `when_to_use` | more trigger text, appended to the description |
| `paths` | glob patterns: the model loads the skill automatically only when working with matching files |
| `model`, `effort` | a different model or effort level, for the rest of the current turn |
| `context: fork` (with `agent`) | run the skill in a subagent with its own context, instead of inline in the conversation |

(`allowed-tools` is also in the open standard, marked experimental there.)

A forked skill is worth a note. Inline, the skill's work fills your
conversation; forked, a subagent receives the skill's body as its prompt,
without your conversation history, and only its result comes back. That suits a
skill whose intermediate steps you do not need to see — a search, a review —
and does not suit ours, whose whole point is a conversation with stops in it.

## Automatic invocation, and how to prevent it

The model decides to invoke a skill the way it decides to call any tool: it
reads the description and judges whether the request matches. So the
description is a retrieval problem, with recall (does it fire when it should?)
and precision (does it stay quiet when it should?).

We tested this directly. Each of our two versions was installed alone in a
fresh copy of the tic-tac-toe starter, and given three prompts with no slash
command:

| Prompt | v1 (description "Helps with CONOPS documents.") | v2 (`disable-model-invocation: true`) |
|---|---|---|
| "What is a concept of operations?" | did not fire; read no file, and tied its answer to "this repository" from the always-loaded `CLAUDE.md` | did not fire; the same |
| "Summarize CONOPS-sketch.md" | did not fire; read the sketch and summarized it | did not fire; the same |
| "Turn CONOPS-sketch.md into CONOPS.md" | **fired** (`Skill: conops`) and wrote the file | **did not fire** — and wrote the file anyway |

Two lessons. v1's description is as vague as a description can be, and it still
fired only on the request where it mattered (and the first answer shows the
neighbour at work: `CLAUDE.md` is always there, skill or no skill); the model
judged relevance better than the description deserved. But it fired on exactly
the request with side effects, and v1's body told it to fill every gap with
"sensible defaults".

The second lesson is the more important. v2 is marked user-invoked only. Its
name was still in the `init` event's list, but the model could not invoke it,
and on the third prompt it did not: the transcript has no Skill call, and the
model did the naive rewrite with no skill at all. It wrote `CONOPS.md` in one
pass and reported:

> **Changes made converting the sketch** (mechanical, no new policy invented):

— while silently settling the sketch's inconsistent post-game options and
skipping several gaps. **Blocking automatic start stops the skill, not the
task:** `disable-model-invocation` protects the command, and the agent simply
does the job without it. A skill governs only the requests that invoke it. If a task must
*never* be done without the method, the skill is the wrong mechanism; that is a
job for a hook, a permission rule, or a test.

The ways to control automatic invocation, from gentlest to strongest:

- **A tighter description.** Say what it is for *and what it is not for*: ours
  ends "Not for explaining what a ConOps is, summarizing a sketch, or editing
  an existing CONOPS.md." Ponytail's ends "Do NOT use for non-coding requests".
- **Scoping.** Install a skill only where it applies: a project skill in the
  one repository that uses the method, not a personal skill in every session.
- **`disable-model-invocation: true`.** The model cannot invoke it; only
  `/name` can. Use it for anything with side effects you want to start
  yourself.
- **Permission rules.** According to the documentation, Claude Code's
  permission settings accept rules for the Skill tool: `Skill(deploy)` matches
  one skill exactly, `Skill(deploy *)` with any arguments, and denying the
  Skill tool altogether disables every skill. A user or an organization can
  block a skill without editing it.

And the interaction to watch for: `disable-model-invocation` also blocks *other
skills* from calling the protected one through the Skill tool, which is exactly
grill-me's issue #1052. A skill only you may start cannot be started by
another skill either.

The vendors disagree about this control. Claude Code's documentation recommends
`disable-model-invocation` for workflows you want to start by hand. Codex's
`skill-creator` says the opposite: "Keep automatic skill selection enabled
unless the user explicitly requests an explicit-only skill … Do not infer
explicit-only invocation from sensitive operations or required approvals: keep
the skill discoverable and require authorization immediately before the actual
mutation." Our v2 follows Claude Code's advice; under Codex's, it would stay
discoverable and stop for approval before writing `CONOPS.md` — which its
phases already do.

## Where skills live across harnesses

Claude Code reads skills from `.claude/skills/`. Many other harnesses that
adopted the open standard read `.agents/skills/`, which the standard's site
describes as "a widely-adopted convention for cross-client skill sharing"
(check each tool's current documentation; the list and the paths move). One
copy can serve both with a symbolic link, which is what our v2 folder does:

```
v2/.claude/skills/conops-from-sketch/     the one copy
v2/.agents/skills -> ../.claude/skills    a link, for other harnesses
```

The same split exists for project memory: Claude Code reads `CLAUDE.md`, many
other tools read `AGENTS.md`. A `CLAUDE.md` whose only line is `@AGENTS.md`
imports the other file, so one text serves both. According to the documentation
(`code.claude.com/docs/en/memory`, fetched 2026-09-27), Claude Code 2.1.277 and
later also reads `AGENTS.md` by itself, but only when the repository has no
`CLAUDE.md`; with both present, only `CLAUDE.md` is read unless it imports the
other. A symlink (`CLAUDE.md -> AGENTS.md`) also works; the import avoids the
Windows problem below and leaves room for lines only Claude should read, so it
is the arrangement that behaves the same everywhere. Note too
that Claude Code reads nothing under `.agents/`, which is why our v2 needs both
paths — ironic, since Anthropic published [agentskills.io](https://agentskills.io)
as an open standard. (The Claude Code memory documentation, fetched 2026-10-01,
lists "anything under a `.agents/` directory" as not read.)

Two cautions. Symbolic links on Windows need Developer Mode or administrator
rights, and git may check them out as plain text files; test on the machines
your team uses, or copy instead of linking. And portability stops at the front
matter. The open standard defines six fields: `name` and `description`
(required), and `license`, `compatibility`, `metadata` and `allowed-tools`
(optional; `allowed-tools` marked experimental). Claude Code's documentation
lists the same six as the only ones usable outside Claude Code. Everything else
— `disable-model-invocation`, `context: fork`, `model`, `argument-hint` — is a
Claude Code extension that other harnesses may ignore or treat differently. Our
v2 relies on `disable-model-invocation`; under a harness that ignores it, v2
would be model-invocable. Grill-me's "Call the Skill tool" line is the same
lesson in the body: the text is portable, the tool it names is not.

We checked the "would be" for three other harnesses. Codex and OpenCode have
their own switches and ignore Claude Code's; Grok honors Claude Code's field
(per its bundled user guide, Grok 1.0.41; we did not run it):

| Harness | Finds v2 in | Keeps the model from starting it | You start it with |
|---|---|---|---|
| Claude Code | `.claude/skills/` | `disable-model-invocation: true` in `SKILL.md` | `/conops-from-sketch` |
| Codex | `.agents/skills/` | `policy: allow_implicit_invocation: false` in the skill's `agents/openai.yaml` | `$conops-from-sketch` |
| OpenCode | `.claude/skills/` or `.agents/skills/` | nothing in the skill folder; the project's `opencode.json` sets `"permission": {"skill": {"conops-from-sketch": "ask"}}` (or `"deny"`) | asking for it |
| Grok (xAI) | `.claude/skills/`, `.agents/skills/`, or `.grok/skills/` | `disable-model-invocation: true` in `SKILL.md`, the same field as Claude Code | `/conops-from-sketch` |

Codex's documentation (`learn.chatgpt.com/docs/build-skills`, fetched
2026-09-30) does not mention `disable-model-invocation`; OpenCode's
(`opencode.ai/docs/skills`, same date) says "unknown frontmatter fields are
ignored." We tested Codex once each way, in a fresh copy of the tic-tac-toe
starter, with the prompt "Turn CONOPS-sketch.md into CONOPS.md" and no `$`.
Without `agents/openai.yaml`, Codex announced "I'll use the
`conops-from-sketch` workflow" and read the skill; with the file, it never
opened the skill. So v2 now ships that file too. It sits beside `SKILL.md`,
which the standard allows and Claude Code ignores; `SKILL.md` and the bundled
files are unchanged, so the evaluation below still describes this skill.

The standard's own checker says the same thing from the other side.
`skills-ref validate` checks the front matter against the six fields and the
naming rules, and v2 fails it: `argument-hint` and `disable-model-invocation`
are not among the six. The standard makes a skill *load* in every conforming
harness; who may *start* it is still each harness's own business, and passing
the checker says nothing about whether the skill works.

## Creating a skill: the worked example

The worked example is a skill that performs the first move of our method on a
concept-of-operations sketch: audit it, report the gaps, stop. The evaluation
used the tic-tac-toe starter from earlier in the course (*Specifying a Game*) — the sketch and the
process documents — and the fourteen gaps that lecture's first audit found as
the key.

### Version 1: the obvious skill

```markdown
---
name: conops
description: Helps with CONOPS documents.
---

Turn the CONOPS sketch into CONOPS.md. Use the standard ConOps sections and
write it professionally. Fill in any missing details with sensible defaults so
the document is complete.
```

This is what most first skills look like, and it is worth reading the way we
read a specification. The description does not say when to use it. The body has
no stop. And one phrase — "fill in any missing details with sensible defaults"
— is a policy, and it is the opposite of ours. Even "the standard ConOps
sections" names nothing: v1 ships no template, and the runs took the nine
sections from the sketch, which already uses them, and from the repository's
`process/conops-audit.md`, which describes the full skeleton.

In three runs, v1 never stopped for a ruling. Every run wrote a finished
`CONOPS.md`, and in doing so it *decided* nearly every one of the fourteen
gaps: five or more in a row wins, five in a row made on the board's last square is a win, not a draw, the
post-game options are "play again or return to the start menu" (silently
dropping the other version). The repository's process documents pulled it
halfway toward the method — it read the audits and produced numbered gap lists
— and then it marked its own items *ruled*, the first of them "already recorded
as settled in `reporting.md` RPT-1 and `spec-audit.md` AUD-1; applied
directly". It treated worked examples in the rules as rulings. It also invented
rules. One run wrote into `CONOPS.md`: `A mark, once placed, cannot
be retracted; there is no "undo."` The sketch never says anything about taking
a move back. An audit rule's worked example does — "'no taking a move back'
stated only under Limitations is a policy" — and the run treated that example
as a finding about this sketch, and "moved" a limitation the sketch never
stated into the policies. Another run put "which side is the human" in the
backlog, and in the same run wrote into `CONOPS.md` "the player is assigned X
and moves first". **The body of a skill is policy**, and "sensible defaults" is
a policy of inventing facts.

### Version 2: the method, packaged

The second version is the method from the lectures so far, turned into a procedure
an agent can follow without us repeating it:

- **A description that says when, and when not.** "Use only when the developer
  explicitly asks to turn a sketch into a CONOPS. Not for explaining what a
  ConOps is, summarizing a sketch, or editing an existing CONOPS.md."
- **`disable-model-invocation: true`.** The skill writes the project's
  governing document; the developer starts it.
- **`allowed-tools: Read Grep Glob`.** Phase 1 only reads.
- **Three phases, each ending in a stop.** Audit and report, then stop. Record
  the rulings and propose amendments, then stop. Write, re-audit, report. The
  body tells the model how to know which phase it is in from the conversation.
- **The reasons, stated.** "A concept of operations is a governing document … a
  guess written into it … becomes a requirement nobody decided." A model that
  knows why a rule exists applies it to cases the rule did not list.
- **Deference to the repository.** If the repository has its own audits, they
  are the authority and their rule identifiers are cited; the bundled checklist
  is a fallback.
- **Bundled files, opened when needed.** `probes.md` holds reading probes — a
  question to ask of any sketch: *counts and thresholds* (exactly N, or at
  least N?), *simultaneous conditions*, *who acts first, and on repeat*, *say
  it twice* (compare two sections' option lists word for word), *facts in the
  wrong place*. `gap-report-template.md` fixes the report's shape.
  `checklist.md` is the fallback audit.

In three runs, v2 stopped every time, wrote no file, invented nothing, and
ended with a request for rulings; one run's last line:

> **Rulings needed on 1–16.** Reply per number: accept the recommendation,
> give another ruling, or defer to the backlog.

**v2's stops are the feature.** v2 did not write a better `CONOPS.md` than v1;
in these runs it wrote none yet. Its value is that the document waits for the
developer, who decides every gap.

### Iterating: better questions, not answers

The first iteration of v2 asked every *hinted* gap — the process documents' own
examples give away nine of the fourteen, and the sketch itself flags a tenth —
but only six of twelve chances
(counting a partial ask as ½) on the four gaps nothing in the repository hints
at: the sketch asks whether, in solo play, who goes first changes on a rematch (asked in every run), but not whether that choice survives a return to the main menu; who starts a
two-player rematch; the post-game options that differ between two sections of the sketch;
whether a draw is realistic and final. It missed the first of those in three
runs out of three.

The fix could have been "ask whether the alternation survives a return to the
menu". That would have passed this evaluation and taught the skill nothing: the
answer key would have leaked into the skill. The second iteration changed the
*questions* instead:

- *who acts first* became a **grid**: one row per mode, one column per entry
  point (first time, repeat right after, after going back to a menu), and every
  empty cell is a gap;
- a new probe, **state carried across repeats**: what resets an alternation, a
  score, a setting?
- *say it twice* now says to copy both wordings side by side and compare the
  *sets* of options, not the gist;
- a doubted end state is **its own gap**, not a note on a missing scenario;
- the body: **one open question per gap**, because two questions in one item get one
  ruling and the other half is lost;
- three phrases that had been copied from the sketch itself were removed from
  the probes as overfitting.
The probes are worded for any sketch, but several are still shaped by the case
they were tuned on: turns, rounds, repeats, and menus fit an interactive game
better than, say, a billing system. Both sketches we tested on were board games,
so how far the probes carry beyond games is untested.

The runs quoted the new probes back ("probes 'who acts first, and on repeat —
as a grid' (grid cells: two-player × repeat, two-player × back-to-menu,
vs-computer × back-to-menu are all unaddressed)"), and the unhinted gaps went
from 6 of 12 to 11 of 12, for about two cents more per run.

## What makes a skill good

What the worked example, grill-me and ponytail have in common:

- **A description that says when and when not.** It is read on every turn by
  something deciding whether to act. Name the trigger *and* the near misses.
- **Policy you would sign.** Read the body as a specification of behavior.
  Every sentence is a rule the agent will try to follow, including the ones you
  meant as filler.
- **Stops where a human decides.** Name the stop, say what to hand over, say
  what not to do until then.
- **Reasons with the rules.** "Do X, because Y" transfers to cases "do X" did
  not list.
- **Concrete over adjectival.** Ponytail's "Say less" did not stop the essays;
  "at most three short lines" did. Our "compare the sets of options word for
  word" caught the post-game inconsistency in three runs of three; "read them
  side by side" had missed it once.
- **Short body, bundled detail.** The body is paid for the rest of the session;
  a bundled file only when read.
- **Deference to the repository.** A skill used in many repositories should use
  each one's rules where they exist, and bring its own only as a fallback.

**Checked against the vendors' guidance.** Both vendors publish advice on
writing skills: Anthropic's [*Skill authoring best practices*](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and
OpenAI's [*Build skills*](https://learn.chatgpt.com/docs/build-skills) together with Codex's built-in `skill-creator`
skill (quoted here as bundled with Codex CLI 0.159.2; an older version is
public in [`openai/skills`](https://github.com/openai/skills/tree/main/skills/.system/skill-creator)). Read against them, the list above holds up,
with three adjustments:

- **Both vendors agree** on the description (what the skill does *and* when to
  use it — Anthropic's own bad example is "Helps with documents", nearly our
  v1), on cutting what the model already knows ("Claude is already very
  smart"; "Assume Codex is already capable"), on concrete examples, and on a
  short body with detail in bundled files (Anthropic: under 500 lines,
  references one level deep).
- **Both add one we lacked: match the instructions to the risk.** Anthropic
  calls it "degrees of freedom": exact steps on a "narrow bridge with cliffs
  on both sides", general direction in an "open field". That is why v2 has
  three phases with stops: a guess written into a governing document becomes
  a requirement nobody decided. OpenAI puts stops the same way — "define a
  stopping condition proportional to the risk" — and its "prefer a narrow
  correction to accumulating universal rules for every observed example" is
  our "fix the questions, not the answers".
- **"Reasons with the rules" is Anthropic's too.** Its `skill-creator` skill
  ([`anthropics/skills`](https://github.com/anthropics/skills/tree/main/skills/skill-creator),
  installed in Claude Code as the `skill-creator` plugin) says: "Try hard to
  explain the why behind everything you're asking the model to do … in lieu of
  heavy-handed musty MUSTs."
- **One tension.** The same `skill-creator` warns that "Claude has a tendency
  to 'undertrigger' skills" and asks for descriptions that are "a little bit
  'pushy'". Our v2 went the other way — a narrow description, and only the
  developer may start it — because a wrong start writes a governing document.
  Which way to lean depends on what a wrong start costs.
- **xAI agrees on the rest.** Grok ships a bundled `skill-design-principles`
  skill: "One home per fact; maintain a single source of truth" (our deference
  to the repository); "If a statement is not required for the skill to
  function, remove it"; and "Solve the underlying class of problem, not the
  single instance you were shown … avoid overgeneralizations" (our "fix the
  questions, not the answers").
- **Their evaluation advice matches ours:** run each test with and without the
  skill, generalize from feedback rather than fitting the examples, and, when
  tuning a description, keep a held-out set (60% to tune on, 40% to test).

The anti-patterns are the mirror image, each with its case from this lecture:
a vague description (v1's "Helps with CONOPS documents.", close to Anthropic's
own bad example, "Helps with documents"); "sensible defaults" or any licence to
fill gaps (v1 invented rules in every run; it is the most freedom on the riskiest
part of the task, which both Anthropic's "degrees of freedom" and OpenAI's
"match specificity to the risk" warn against); the answer key copied into the skill
(the tempting fix for the side-switching gap; OpenAI and xAI both say to fix the
class of problem, not the one instance); a rule that must hold always,
written as a sentence (v2 was installed and `CONOPS.md` was written anyway; Claude Code's docs: "use
hooks to enforce behavior deterministically"); a
bundled copy of rules the repository already has (iter1 opened its own
checklist; xAI's "one home per fact"); and instructions that name one harness's
tools in a skill meant to be portable (grill-me's "Call the Skill tool", which broke on Codex; OpenAI: "refer to
another skill or tool only when … it is available in the target environment").

Two further lessons are less obvious.

**Compliance is probabilistic.** One of v2's three iter2 runs did
not ask what happens when the move that fills the board's last square also makes
five in a row — a win or a draw? It wrote it into its summary
instead, under the template's "Implies" heading: "a win is checked before a
full board is called a draw". That is a correct inference from the text, and it
is also a decision taken without asking — exactly what the skill exists to
prevent. Across runs, a skill raises the probability of the behavior; it does
not make it certain.

**Templates shape behavior.** The template's *States / Implies / Leaves out*
summary was meant to orient the reader. The model used "Implies" as a place to
settle things. On the held-out sketch below, the same move happened again, on a
different gap, in a sketch the template was not written for. Every heading in a
template is an instruction about where things may go. The proposed fix is
structural: anything implied but not stated is *also* listed as a numbered gap,
with the implication as its recommendation.

## Evaluating a skill

A skill is a program whose interpreter is a model, and it is evaluated the way
we evaluated a program earlier in the course (*Verifying a Game*): against claims fixed in advance, with the
verifier's own weaknesses in view.

### Our evaluation

The protocol:

- **A key written before the runs were read.** The fourteen gaps *Specifying a
  Game* found, with
  one column added after the first runs: *Hinted in*, which records where the
  repository gives a gap away. It showed that nine of the fourteen are
  described almost verbatim in the process documents' examples, so any run that
  reads `process/` gets them nearly free, and the sketch itself flags a tenth.
  Only the other four test the skill. **Check the key before the skill.**
- **A scoring legend.** Each gap in each run is *asked* (open, with a
  recommendation; counts 1), *partly asked* (counts ½), *deferred by the agent*
  (still a decision taken for the developer), *silently decided*, or *absent*
  (these three count 0).
- **Repeated runs, same model, clean environment.** Three runs per version in a
  fresh copy of the starter, run non-interactively, with a full transcript kept for each.
  The harness loaded only the project's settings, so the instructor's personal
  skills and plugins did not leak in (his personal `CLAUDE.md` still did; the
  runs cited it).
- **Trigger tests.** Three prompts with no slash command, plus one run that is only `/name`.

The results on the sketch the skill was tuned on:

| | v1 | v2 iter1 | v2 iter2 |
|---|---|---|---|
| stopped for rulings | 0 / 3 | 3 / 3 | 3 / 3 |
| any file written before rulings | 3 / 3 | 0 / 3 | 0 / 3 |
| invented rules | in every run | none | none |
| unhinted gaps asked (of 12; a partial ask counts ½) | 0 | 6 | **11** |
| hinted gaps asked (of 30) | none; decided or left open | 30 | 29 |
| mean cost per run (not one for one: v2 stopped after phase 1; v1 had already finished, wrongly) | $0.60 | $0.32 | $0.34 |

Then the recommendation, in the evaluation's own words: *stop iterating on this
sketch.* One miss in twelve unhinted chances is inside run-to-run noise at three
runs per version, and every further change would have been tuned against the
same three transcripts. That is **training on the test set**, and even the
generic probes of iter2, written after seeing the misses, are already
tuned to this sketch.

So the frozen skill (its files' hashes recorded) was run on a **held-out**
sketch it had never seen: a Reversi sketch, scored against the instructor's key that
existed before any run. The Reversi gaps were sorted in advance into kinds:
*new kinds* unlike anything the probes were tuned on, *transfer* gaps of the
same kinds as tic-tac-toe's, and gaps the starter's documents hint at. (The
gaps themselves are not listed here: that sketch is close to the one you audit
in Project 1, and finding its gaps is your work. As in Project 1, "standard
Reversi" settles the *answer*, not the question: a standard rule the sketch
leaves unstated still counted as a gap to raise.)

| Measure | tic-tac-toe (tuned on) | Reversi (held out) |
|---|---|---|
| unhinted gaps asked (a partial ask counts ½) | 11 / 12 (92%) | new kinds 13 / 24 (**54%**); transfer 6.5 / 9 (72%) |
| hinted gaps asked | 29 / 30 | 16 / 18 |
| stopped, no file written | 3 / 3 | **3 / 3** |
| invented rules | none | none |
| silently decided | 1 | 2 (both in one run) |

**The process generalized; the coverage did not.** On a sketch it was never
tuned on, v2 still stopped and wrote nothing in three runs of three. It did not
keep every decision open: one run settled two questions without asking, one of
them under its "Implies" heading again. And it asked only about half of the
new kinds of gap. The misses were of kinds no probe asks about: how something
is shown on screen (a *representation* question); whether a rule means every
case or just one (a *quantifier* question); what happens next after an event;
and what the sketch never mentions at all. The probes that do exist were built
on tic-tac-toe. v1, run once on Reversi, wrote the document without asking
anything and settled every open question on its own.

The candidates for the next iteration are generic questions — for every thing
the user sees, how is it shown? when a rule says "the" or "everything", does it
mean one or all? after each event, what happens next, and after that? what
would a user expect to know that the sketch never mentions? — and they must be
measured on a *third* sketch. Reversi is now part of the tuning set.

### Three levels of evidence

Set our evaluation beside the two published skills.

| Question | grill-me | ponytail | our conops skill |
|---|---|---|---|
| What was measured? | nothing systematic | lines of code, cost, latency, safety on adversarial inputs, trigger recall and precision, behavior probes | gaps asked vs. decided, stops, writes, inventions, triggers |
| Compared with what? | the author's own use | no skill (the baseline), a competing skill, a one-line prompt after a critic's suggestion | a key fixed before the runs; a held-out sketch |
| evidence | anecdote ("45 minutes"), adoption, user issues | public benchmark results, including the ones that went against it | transcripts, a scoring table, an iteration log |
| What went wrong, and who found it? | regressions in the skill, found by users (#831, #1052) | flaws in its own evaluation — an inflated headline number, a contaminated baseline — found by a critic and the author | v1 invents; iter2 overfits; held out, 54% against 92% tuned |

Ponytail's record is the instructive one, because much of it is a record of its
own mistakes, published. Its first headline — "80–94% less code" — came from
single prompts with no system prompt, and a critic (Colin Eberhardt, issue #126) showed that adding a one-line system prompt took the no-skill baseline from 108 lines of code to 16, against ponytail's 8.25; the benchmark README now says "Read this number
honestly … it counts prose, not just code, and overstates the win." The authors
rebuilt the benchmark around real agent sessions, and its first run went wrong
the other way: it showed only about 4% less code, because the plugin's
session-start hook had fired in *every* test condition, so, in its author's
words, "the 'baseline' was secretly running ponytail" ("We nearly published
it"). They marked that result superseded, isolated each condition (only its own
plugin loaded), and reran: about 54% less code on average, 0 to 94% depending
on the task (12 feature tasks, Haiku 4.5, four runs each). And they report what skill text could not fix: OpenAI models kept
validating email addresses with the wrong library function
(`email.utils.parseaddr`). The author tried eight different rewrites of the
skill, one compared against the current skill over 100 runs (96% → 95%); none
did better, so none was released — "Nothing was shipped."

Claude Code's own documentation (the skills page, fetched 2026-09-27) gives the
same starting point: "Seeing a skill trigger tells you Claude found it, not
that it did what you intended." It recommends measuring triggering and output
separately, against a baseline run with the skill disabled, each in a fresh
session, "because leftover context from authoring the skill will mask gaps in
the written instructions", and it points to two tools that automate the loop
(the `skill-creator` plugin and `claude plugin eval`). Neither replaces a key
you wrote before looking.

Anthropic's [*Skill authoring best practices*](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
go further: "Create evaluations BEFORE writing extensive documentation",
establish a baseline "without the Skill", and test with every model you plan to
use ("Tested with Haiku, Sonnet, and Opus"). Our evaluation used one model, so
its numbers say nothing about how the skill behaves on the others.
OpenAI's `skill-creator` asks for the same discipline from the other side:
"verify observable behavior or meaningful invariants. Avoid tests that merely
match generated wording", and, when another agent tests the skill, do not give
it "the intended answer, suspected bug, proposed fix, or prior conclusions".
xAI's bundled guidance has no advice on evaluating skills.

That gives three levels of evidence, in increasing strength:

1. **Anecdote and adoption** — the author's own use, stars, installs. It tells
   you people like it, not that it does what it says.
2. **Measurement on the cases you tuned on** — necessary, and optimistic. Our
   92% is this kind of number.
3. **Measurement on held-out cases, with the instrument checked** — a key fixed
   before the runs, a fair comparison (e.g. no skill at all), a clean environment, and
   a case the skill has never seen. Our 54% is this kind of number, and it is
   the one to believe.

One caution applies to every level that counts gaps. **Scoring only which of the key's questions
got asked rewards asking everything.** A skill that asks about everything "finds" most of any list,
and our numbers count gaps asked, not whether the rest of the report was worth
reading. Grill-me's issue tracker has the extreme case: "Codex just asked me
200 questions". The key is also one author's incomplete list, so a valid
question it lacks looks like noise, and one run is noise too (the unchanged
iter2 scored 3, 4.5 and 5.5 of 8 new-kind gaps on the same sketch). So pair
recall with **behavior** — did it stop, did it write, did it invent — and with
**precision**: of the questions it asked, how many were trivial, or already
settled by the repository? Our evaluation checked behavior first; it did not
measure precision, and the gap lists grew by about three items from iter1 to
iter2. The exercise asks you to measure all three.

## Security and trust

A skill is instructions your agent will follow, plus files it will read and
possibly scripts it will run. Installing one is closer to installing a package
than to reading a blog post.

- **Supply chain.** A popular skill repository can change under you; a plugin
  from a marketplace updates. Pin versions you depend on, and read the diff.
- **Injection in bundled files.** A bundled reference file is read by your
  agent with your permissions. Text in it that says "also run …" is an
  instruction, whatever it looks like to you.
- **`` !`command` `` runs before the model sees anything.** It runs on your
  machine, as you. Read every one.
- **`allowed-tools` widens what runs without asking.** The documentation is
  explicit that workspace trust does not gate it: a project skill's grant
  applies "including in a `-p` run in a folder you've never trusted", so
  "review the `allowed-tools` of skills checked into a repository before you
  run Claude Code there." Treat it like a permission grant, because it is one.
- **Read before installing.** The whole skill is text. Reading it takes
  minutes, and nothing else tells you what it will do. Anthropic's own advice
  for skills in its API is to use them "only from trusted sources", and
  otherwise to "thoroughly audit it before use".

## Sharing, debugging, and skills beyond coding

**Sharing.** Commit a project skill in `.claude/skills/` and everyone who
clones the repository has it. For a wider audience, package skills (and any
hooks and MCP servers they need) as a **plugin**, published through a
**marketplace** — a repository that lists plugins, which users add with the
`/plugin` command. Ponytail is distributed as a plugin; grill-me's repository
is packaged as a Claude Code plugin and also installs through `npx skills add`
for other harnesses.

**Debugging.** Four questions, in order:

1. *Is it loaded?* Is it in the `/` menu? In a headless run, is its name in the
   `init` event's `skills` list? If not: wrong folder or file name. Malformed
   front matter is subtler: the skill still loads and `/name` still works, but
   with empty metadata, so the model has no description to match. Two commands
   catch it: `claude --debug` starts a session that logs what it loaded and
   shows the parse error, and `claude plugin validate .claude/skills` checks
   every skill's front matter and files in the folder without starting a
   session (`--strict` also fails on warnings; our v2 passes both).
2. *Did it trigger?* Look for a `Skill` tool call in the transcript. If the
   model did not call it, the description did not match the request — or
   `disable-model-invocation` is set.
3. *Did it do what it says?* Read the transcript step by step: which bundled
   files were read (Read calls, but also `cat` through Bash), when, and what
   the model did at each stop. Our v2 finding about `checklist.md` came from
   exactly this reading.
4. *Did it abort?* A skill with a `` !`command` `` line can load and trigger
   and still fail: according to the documentation, an injected command that
   does not pass the permission check aborts the invocation with a "Shell
   command permission check failed" error. Allow the command in
   `allowed-tools`, or remove the line.

**Beyond coding.** The same format carries any procedure. Anthropic ships
pre-built document skills (PowerPoint, Excel, Word, PDF) that run in the Claude
apps and through the Claude API, and the open standard is read by harnesses
that have nothing to do with code. Grill-me's author, on his blog, uses it "for figuring out
what course to build next".

## The exercise: create the counterpart skill

The exercise assigned today asks you to create the other half: a skill that
takes a concept of operations to `SPECS.md` the way ours takes a sketch to a
gap list — audit for the decisions a technical specification must settle,
grouped by the kind of specification that must settle each, report a numbered
gap list with a recommendation for each, stop for rulings — and to
evaluate it the way this lecture evaluated ours. The subject is tic-tac-toe:
tic-tac-toe's reference `CONOPS.md` from earlier in the course (*Specifying a Game*), with that lecture's second
gap table (gaps 15–22) as the key, committed before your first run. You run four trigger tests (one where it should start, three where it shouldn't), score at least three runs per version, and say why you
stopped iterating. The reflection asks what you would need before trusting the
skill beyond tic-tac-toe — the question our Reversi result answers for our
skill. The exercise earns feedback, not points. The details are in
[`../exercises/exercise-03-a-skill-for-specs-from-conops.md`](../exercises/exercise-03-a-skill-for-specs-from-conops.md).

## Questions to think about

Not graded and not handed in; worth a short answer of your own.

1. With v2 installed but not started, the agent wrote `CONOPS.md` in one go
   when the request did not name the skill, and called its work "mechanical,
   no new policy invented". What would you have to add to the repository — not to the skill —
   so that `CONOPS.md` cannot be written before a gap list has been ruled on?
   Which of hooks, permissions, tests, or process rules does it use?
2. Our skill scored 92% on the sketch it was tuned on and 54% on new kinds of
   gap in a sketch it had never seen. Which number would you report, and what
   would you have to do before you could report a third?
3. Grill-me's switch from one question at a time to rounds was justified, in the change's changelog entry, by
   "Same 13 questions land in ~3 rounds instead of 13". Design the smallest
   evaluation that would have tested that claim before it shipped. What is the
   key, what is the baseline, and what would count as a regression?

## Before next meeting

- The exercise is assigned today, due Tuesday, October 13, 11:55 pm: [`../exercises/exercise-03-a-skill-for-specs-from-conops.md`](../exercises/exercise-03-a-skill-for-specs-from-conops.md).
- Project 1 continues; it is due Thursday, October 8.
- The next lecture is on MCP. Before it, read the Model Context
  Protocol documentation's core concepts, the FastMCP quickstart, and the dice-server README. Read them with today in mind: a skill
  tells an agent how to use the tools it has; MCP gives it new ones.
- Optional: the open standard's specification ([agentskills.io](https://agentskills.io/specification)) and the Claude
  Code skills documentation, and one published skill of your choice, read as a
  specification — what policy does its body set?