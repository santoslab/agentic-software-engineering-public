# Exercise — Create a Skill: SPECS from a CONOPS

> **Assigned:** the skills lecture (Thursday 2026-10-01) · **Due:** Tuesday,
> October 13, 11:55 pm · **Effort:** about 3–5 hours, at least 2 of them runs, mostly
> unattended (three runs that stop for rulings take 10–15 minutes; a run that
> writes the whole document can take 17 minutes or more by itself)
>
> **Requires:** Claude Code; git; `jq` (for reading transcripts). Uses the
> tic-tac-toe demo in `module-software-engineering/demos/lecture-03-game-demo/`
> and the skills lecture's worked example (the `conops-from-sketch` skill).
>
> **Feedback, not points.** This exercise earns no grade points. You get a
> written feedback note; what it covers is at the end.


## Goal

Create an agent skill that packages the second move of the method — from a
concept of operations to the decisions `SPECS.md` must settle — and find out,
with evidence, whether it works. The lecture's skill audits a sketch and stops
for rulings; yours audits a finished `CONOPS.md` for everything a technical
specification must decide, grouped by kind of specification, and stops for
rulings. The subject is tic-tac-toe, whose concept of operations you know from earlier in the course (*Specifying a Game*). Most of the exercise is the evaluation, not the writing.

## Setup

1. **The repository.** The quickest start: [download the starter](https://downgit.github.io/#/home?url=https://github.com/santoslab/agentic-software-engineering-public/tree/main/module-software-engineering/student-materials/specs-skill-starter)
   (`student-materials/specs-skill-starter/`: the tic-tac-toe starter with the
   reference `CONOPS.md` in place of the sketch), unzip it as `~/specs-skill`, and
   make it a git repository (`git init && git add -A && git commit -m "start:
   CONOPS 1.0 and process"`). Or build the same thing from your clone:
   in every terminal you use, set `MOD` to your clone's
   `module-software-engineering` folder (a spare terminal does not see a
   variable set in another one). Then copy the demo's starter somewhere
   outside the course repository, add the reference concept of operations,
   remove the sketch, and make it a git repository:

   ```sh
   export MOD=<your clone>/module-software-engineering
   cp -R $MOD/demos/lecture-03-game-demo/starter ~/specs-skill
   cp $MOD/demos/lecture-03-game-demo/reference/CONOPS.md ~/specs-skill/
   cd ~/specs-skill && rm CONOPS-sketch.md
   git init && git add -A && git commit -m "start: CONOPS 1.0 and process"
   ```

   Do **not** copy the reference `SPECS.md`; it would give the answers away.

2. **The key, committed first.** Your key is the round-2 table in
   `$MOD/demos/lecture-03-game-demo/demo-script-lecture-03.md` (gaps 15–22).
   Before any run, copy it into `key.md` and add a *Hinted in* column, as the
   lecture's evaluation did: for each gap, does anything in `process/` (the
   per-kind checks AUD-8 to AUD-14) or `CLAUDE.md` give the gap away? A gap the
   repository hints at is weak evidence for your skill. **Commit `key.md`
   before your first run**; the history is how a reader knows it came first.

3. **What a run sees.** A run must see the repository and your skill, and
   nothing else: not `key.md`, not `runs/`, not another run's output. So every
   run works in a fresh directory exported from your latest commit, with only
   the files the run needs:

   ```sh
   rm -rf ~/specs-run && mkdir ~/specs-run
   git -C ~/specs-skill archive HEAD CLAUDE.md BACKLOG.md CONOPS.md process .claude \
     | tar -x -C ~/specs-run
   cd ~/specs-run
   ```

   Commit the skill before each set of runs, so the export contains the
   version you mean to test. Keep `runs/` in `~/specs-skill` and commit it
   afterwards.

4. Read the lecture's worked example: the `conops-from-sketch` folder shown in
   the lecture notes (its `SKILL.md`, `probes.md`, and
   `gap-report-template.md`), and the notes' sections on what makes a skill
   good and on evaluating a skill.

## Task

1. **Create the skill.** A project skill at
   `.claude/skills/specs-from-conops/SKILL.md`, with at least one bundled file.
   It must:
   - have a description that says when to use it *and when not*;
   - be user-invoked only (`disable-model-invocation: true`), with a one-line
     justification in `DESIGN.md`;
   - run in phases that each end in a **stop**: audit `CONOPS.md` and the
     process documents and report the open decisions per RPT-1, **grouped by
     the kind of specification that must settle each** (the AUD-8 to AUD-14
     kinds), then stop; record rulings and propose amendments (RPT-3), then
     stop; write `SPECS.md` 1.0.0 and re-audit;
   - defer to the repository's own audits where they exist;
   - contain no tic-tac-toe answers. A probe is a question; it never carries
     its answer. Your key is the answer; if a line of the key appears in the
     skill, the evaluation measures nothing.

   Write `DESIGN.md` (half a page): what each phase is for, what each bundled
   file is for and when the body sends the model to it, and which sentence in
   the body you expect to matter most.

2. **Trigger tests.** Four prompts, each run headless in a fresh export
   (setup step 3), with the isolation the lecture's evaluation used:

   ```sh
   rm -rf ~/specs-run && mkdir ~/specs-run
   git -C ~/specs-skill archive HEAD CLAUDE.md BACKLOG.md CONOPS.md process .claude \
     | tar -x -C ~/specs-run
   cd ~/specs-run
   claude -p "<prompt>" --output-format stream-json --verbose \
     --setting-sources project --permission-mode acceptEdits \
     --permission-prompts none --no-session-persistence \
     > ~/specs-skill/runs/<name>.jsonl
   jq -c 'select(.subtype=="init")|{model,claude_code_version,skills}' ~/specs-skill/runs/<name>.jsonl
   jq -c 'select(.type=="assistant")|.message.content[]?
          |select(.type=="tool_use")|{name,input}' ~/specs-skill/runs/<name>.jsonl
   ```

   `--setting-sources project` keeps your personal skills and plugins out of
   the run; your personal `~/.claude/CLAUDE.md` still loads, so say so if a run
   quotes it. The `init` line should list `specs-from-conops`; if it does not,
   the export did not contain the skill.

   Prompts: (a) "What is a technical specification?"; (b) "Summarize
   CONOPS.md"; (c) "Write SPECS.md from CONOPS.md"; (d) `/specs-from-conops`.
   (a), (b) and (c) are the **negative** tests: the skill should not fire. For
   each, record whether the Skill tool was called and whether any file was
   written. For (c), report what happened *without* your skill, and say what —
   outside the skill — would stop it.

3. **Tuning runs.** Run `/specs-from-conops` **at least three times**, each in a
   fresh export. Evaluate each run in three passes, in this order.

   **Behavior first.** Did it stop for rulings? Did it write anything before
   rulings (any Write or Edit call, or a new file)? Did it invent a rule —
   state as settled something neither `CONOPS.md` nor `process/` states? A run
   that fails one of these has failed at the skill's job, whatever else it
   asked.

   **Precision second.** Count the questions in its report, and how many of
   them are *trivial* (you would answer "obviously" in one word) or *already
   settled by the repository* (it asked instead of citing the rule). Recall
   alone rewards volume: a skill that asks everything "finds" most of any key,
   and a developer handed forty questions answers none of them well — the
   grill-me issue "Codex just asked me 200 questions" is that failure.

   **Recall third.** Score each gap in the key for each run with this legend:

   | Mark | Meaning | Counts |
   |---|---|---|
   | **A** | asked: open, with a recommendation | 1 |
   | **R** | answered from the repository: the gap is already settled by a rule the repository states, and the run cites that rule instead of asking | 1 |
   | **~** | partly asked; or asked the developer to rule on something the repository already settles | ½ |
   | **D** | deferred by the agent to the backlog | 0 |
   | **S** | silently decided, or written into `SPECS.md` differently from what the repository settles | 0 |
   | **–** | absent | 0 |

   Some gaps in the key are not questions for the developer at all: the
   repository already answers them. A skill that reads the repository and
   says so, citing the rule, earns **R**; your *Hinted in* column is where you
   will notice these. Also record the cost and which bundled files were
   read. The Read tool calls
   show most of these, but a model can also open a file with `cat` through
   Bash; check both.

4. **Iterate, and say why you stopped.** Change the skill to fix what the runs
   missed — by improving a *question*, never by adding an answer — and rerun
   step 3. Keep each version as a folder (`iterations/iter1/`, `iter2/`, …)
   and, when there are two or more, a diff between consecutive ones. Stopping
   after the first version is allowed, with a reason. Stop when the remaining
   misses are within run-to-run noise, and say so. Report every miss,
   including the ones you could not fix.

5. **Reflect** (one page). Put your first and last scores side by side. Then
   answer: **what would you need before trusting this skill beyond
   tic-tac-toe?** The lecture's skill scored 92% on the sketch it was tuned on
   and 54% on new kinds of gap in a Reversi sketch it had never seen, while
   still stopping and writing nothing in every run. Which parts of your skill
   do you expect to transfer the way its stops did, which the way its probes
   did not, and what measurement would tell you? Name one kind of gap no probe
   of yours asks, and one thing your skill cannot enforce, with the mechanism
   (hook, permission, gate, process rule) that could.



## What you hand in

A repository link, or a zip **that includes `.git`** (without the history,
nobody can see that the key was committed first), containing:

- `.claude/skills/specs-from-conops/` — the final skill, with its bundled files
- `iterations/` — each version, and the diffs between them if there are two
  or more
- `DESIGN.md` — from task 1
- `key.md` — committed before the first run
- `runs/` — every transcript (`.jsonl`)
- `EVAL.md` — the trigger table; per run, the behavior checks, the precision
  count, and the recall scoring; the iteration log with your reason to stop;
  and every miss
- `reflection.md` — from task 5

## Completion checklist

- [ ] A skill with a when/when-not description, `disable-model-invocation`,
      phases ending in stops, output grouped by kind, and at least one bundled
      file the body sends the model to
- [ ] No tic-tac-toe answers in the skill
- [ ] Four trigger tests with transcripts, three of them negative, and the (c)
      question answered
- [ ] At least three runs per version, each with behavior checks, a precision
      count, and recall scored against a key committed before the first run
- [ ] Every version kept, each change with a stated reason; a reason to stop
- [ ] A reflection that answers the transfer question

## The feedback you will get

There are no points. You get a short written note on five things:

- **Your skill's design** — the description, the stops, the bundled files, and
  whether any line of it is an answer rather than a question.
- **Your own evaluation** — whether the key was committed before the runs,
  whether there were at least three runs per version, whether behavior and
  precision were checked and not only recall, whether the negative trigger
  tests are there, whether the misses are reported honestly, and
  whether you gave a reason to stop.
- **How the skill behaves when the instructor runs it** — your skill, run again
  on the same tic-tac-toe repository with a fixed model: where it asks and
  where it decides, and any rule it invents, quoted from the transcript.
- **How it generalizes** — one run (sometimes three) on a concept of
  operations you haven't worked with in this exercise: first how it behaved
  (stopped? wrote? invented?), then how many of its questions were worth
  asking, then one or two notable catches or misses. No score: a count of
  gaps found would reward a skill that asks everything.
- **Your reflection** — mainly your answer to the transfer question.

The note names one thing that works and one or two things to fix, each with
the transcript lines that show it.
