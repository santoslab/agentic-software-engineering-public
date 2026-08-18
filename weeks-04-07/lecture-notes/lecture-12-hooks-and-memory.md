# Lecture 12 — Hooks and Memory: Automating the Environment

> Week 6, meeting 2 of 2. Companion reading for the lecture; self-contained.
> Assigns the **Stage C cost-hook port** (a required element of the stage).

## What must happen every time cannot depend on remembering

The pass-4 retrospective handed this course its sharpest sentence, back in
Lecture 06: *"I should have interrupted the model as soon as it skipped a
verification step I intended."* The step was intended. It was even understood.
It depended on someone remembering to care at the right moment, and at
production prices, it got skipped.

You have spent two weeks building the answer for *checks*: gates, named in a
file, run as a unit. Today is the answer for *actions*: a **hook** is code that
runs at a lifecycle event of your Claude Code session — automatically, every
time, whether or not anyone is thinking about it. Yesterday's gate table is
discipline you execute; a hook is discipline that executes itself.

## Hook anatomy

A hook is a program registered in `.claude/settings.json` against a lifecycle
event. The events you will actually use, and what each is for:

| Event | Fires | Canonical use |
|---|---|---|
| `SessionStart` | New session begins | Prime context: surface the backlog, warm state |
| `SessionEnd` | Session exits | Logging, transcription, cost accounting |
| `PreCompact` | Before compaction | Preserve what summarization would lose |
| `PreToolUse` / `PostToolUse` | Around each tool call | Guard or audit specific actions |

The contract is deliberately boring: the hook receives JSON on stdin (session
id, transcript path, exit reason, working directory) and communicates by exit
code. It is a filter in the oldest Unix sense. Anything that can read stdin can
be a hook — which is why yours will be Python and the one you are porting is
PowerShell.

Now the iron rule. Open the original cost hook and read its skeleton:

```
try {
    # ... the entire program ...
} catch {
    # Never block session exit on a logging failure.
}
exit 0
```

**A logging hook must never block the session.** Whatever goes wrong — missing
transcript, malformed JSON, locked file — it swallows the failure and exits
zero. A cost log that occasionally misses a row is a minor annoyance; a cost
log that can prevent your session from ending is a booby trap wired to an
event you cannot avoid triggering. When you port this hook, that try/except
envelope is the first behavior to preserve and the easiest to forget.

## Worked example: reading the cost hook as a spec

Stage C's Claude-feature requirement: port `log-cost-on-end.ps1` (shipped in
`student-materials/hooks/`) to cross-platform Python. **The .ps1 is the spec.**
You do not need to know PowerShell to read it as one — you need to extract the
behaviors that must survive the trip. Walk it block by block and list them:

1. **The pricing table.** Rates per million tokens, per model, four rate types —
   input, output, cache write, cache read — editable in one obvious place, with
   a priced fallback for unknown model ids. (Why a fallback instead of skipping
   unknown models? Because a cost log that silently drops the expensive new
   model is a cost log that lies in the direction you least want.)
2. **Transcript collection.** The session's main transcript, plus any subagent
   transcripts in the conventional subdirectory. Miss the subagents and every
   session that used one under-reports.
3. **The walk.** Each transcript is JSONL; each line may carry a message with a
   `usage` block; malformed lines are skipped without ceremony.
4. **Dedupe by message id.** The subtle one. The same message can appear in
   more than one transcript file; the hook keeps a seen-set of message ids and
   counts each exactly once. Drop this and your numbers inflate quietly — the
   kind of bug no test notices because the CSV still *looks* right. When your
   port is done, this is the behavior to test first: feed it two files sharing
   a message, assert the tokens count once.
5. **The output contract.** Append one row to `Documentation/session-costs.csv`
   — same columns, same order: timestamp, session id, reason, models, four
   token totals, estimated cost. Create the directory and header if missing.
   Your Project 2 team will *merge* these CSVs across machines; the column
   contract is what makes that possible.

Notice what you just did: extracted a behavioral contract from working code in
a language you may not know. That is Stage A's exercise again — and Tuesday you
do it across Python and TypeScript at full scale. The course keeps handing you
the same move because it *is* the move.

Cross-platform notes for the port, learned the annoying way so you don't have
to: build paths with `pathlib`, never string concatenation; open the CSV with
`newline=""` (Windows will double-space it otherwise); and document the
registration command for both worlds — the interpreter is `python3` on
macOS/Linux and typically `python` on Windows, and your README-hook note must
say so because `settings.json` is checked in and your grader's OS is not yours.

## Memory, the complete picture

Lecture 06 gave you three kinds of memory: the conversation (volatile,
re-billed, rots), CLAUDE.md (durable, per-project), your PKB (durable, yours,
cross-project). Today the middle layer unfolds into a hierarchy:

| Layer | File | Scope | What lives there |
|---|---|---|---|
| User | `~/.claude/CLAUDE.md` | You, every project | Your standing preferences: tools, style, "ask before X" |
| Project | `<repo>/CLAUDE.md` | Every session in this repo | The laws: coverage gate, layering rule, build commands |
| Directory | `web/CLAUDE.md` | Sessions working in that area | That layer's rules and commands — loaded when relevant, free when not |

The economic logic is the same one prompt caching taught you: pay for context
in proportion to how often it is needed. The engine coverage law is needed by
every session — project level. The template conventions are needed only when
touching templates — directory level. Your preference for `uv` over `pip` is
needed in every repo you ever touch — user level.

Two additions complete the picture. **Auto-memory**: Claude Code can maintain
its own notes across sessions — facts it decides are worth keeping. Treat it
like a junior engineer's notebook: genuinely useful, occasionally wrong, and
*reviewable* — you read what it writes, you delete what is stale. It does not
replace CLAUDE.md (curated law) and it does not replace your PKB, for a reason
worth stating: auto-memory is the agent's lessons about *this project*; your
PKB is *your* lessons about *every project*. "Migration 7 fought back for two
days because the seed data assumed the old column" belongs in your PKB the
moment you can phrase the general rule; no tool writes that file for you.

## Isolation: permissions as context engineering

One more `settings.json` capability, shown by the course's own experiments.
The fifth NautilusTRX pass was a rebuild-from-scratch exercise; its value as an
experiment depended on *not* seeing the four earlier attempts. Its settings
file deny-lists Read, Edit, and Write for every sibling pass and the course
materials — sixty lines of "do not look."

Read that file as a design statement: **permissions are not only safety; they
are context engineering.** An agent cannot be steered by what it cannot see.
Contamination — the stray Read of a previous solution that quietly becomes
*the* solution — is invisible in the output and fatal to the experiment. Your
version is smaller but real: the brief prohibits consulting the course repo's
finished solutions, and a three-line deny-list makes the prohibition mechanical
instead of aspirational. You now know all three enforcement grades: aspiration
(the brief's sentence), discipline (you remembering), mechanism (the
deny-list). Prefer mechanism. That preference is most of this course.

## Stage C hook assignment, concretely

From the brief: `.claude/hooks/log_cost_on_end.py`, behavior-preserving per the
five contract points above; never-block; registered in `settings.json`; at
least five real rows of your own sessions committed in `session-costs.csv`.
When it works, look at your own numbers — the cache-read column dwarfing input
is Lecture 06's economics, now self-collected. From here to semester's end, you
have per-session cost data on everything you do; Lecture 22 will ask you to
read it like an engineer.

## Questions to think about

1. Sort into hook / skill / CLAUDE.md line / gate: (a) "run the gates before
   every commit"; (b) "transcribe the session at exit"; (c) "never edit
   migration functions"; (d) "surface BACKLOG.md at session start." One of
   these defensibly lives in two homes — which, and what decides it?
2. The hook recomputes cost from the transcript instead of reading a cost
   field. The .ps1's header comment says why. What general lesson about
   reading-before-assuming does that comment teach, and where else did you
   meet it this week?
3. Auto-memory records "tests live in tests/unit and tests/integration."
   Your PKB records — what, exactly, from the same fact? Write the PKB
   sentence; notice what had to change for it to be worth keeping.
