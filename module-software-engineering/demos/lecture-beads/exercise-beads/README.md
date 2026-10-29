# Beads exercise: render and resume

**Due: November 8, 2026.**

Use the familiar 9×9, five-in-a-row tic-tac-toe project to practice planning,
maintaining a Beads work graph, and continuing unfinished work in a fresh
agent session. The required implementation is **rendering only**.

Write your own prompts. Use two agent sessions, with as many turns in each
as you need. Work proceeds sequentially. Your second session must recover
from the project and Beads without receiving the first session's transcript.

## Starting state

The pristine `starter/` contains the existing engine, menu shell,
specifications, contracts, original task list, and **44 passing baseline
tests**. Board rendering, parsing, and the two-player loop are unfinished.
The setup creates a separate `work/` copy with a fresh Git repository and an
empty Beads workspace. Your agent creates and reviews the work records.

The game source, tests, and governing artifacts come from the public course
project's [unfinished checkpoint](https://github.com/santoslab/agentic-software-engineering-public/tree/4d6a2cdc70cfd3fc4ffc5d117ad1078d69b206f8/module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe).
`source.json` records provenance; `starter-sha256.txt` identifies these inputs.
The exercise-specific agent policy and setup tools are added teaching material.

## Setup

You need Git with your author name/email configured, Node.js/npm, uv, Python
3.12 or newer, and an authenticated coding agent. The supplied recorder uses
Claude Code. Installing the locked dependencies needs network access; agent
calls use your own account's allowance. Beads **1.3.2** is installed locally.

From this folder:

```sh
sh setup.sh
cd work
export PATH="$PWD/node_modules/.bin:$PATH"
bd version
bd list --all
cd ..
```

Setup runs the baseline tests before initializing Beads. Expect **44 passed**
and an empty issue list. It refuses to overwrite an existing `work/` folder.
Keep `starter/` unchanged; all implementation happens in `work/`.
The setup makes local commits and configures no Git remote.

The folder layout after setup and recording is:

```text
exercise-beads/
├── starter/       pristine game and exercise policy
├── work/          your game copy, Git history, and .beads/
├── prompts/       prompt files you write
├── recordings/    CLI transcripts, metadata, and readable transcripts
└── checkpoints/   saved project states and issue exports
```

## Scope and completion conditions

Have your agent review the existing plan and create a graph for the
two-player milestone. Preserve readable task descriptions, original task
references, governing contract paths, acceptance criteria, evidence needs,
and blocking relationships. Identify the independent rendering and parsing
work and the game loop's integration prerequisites. Choose useful issue
boundaries; keep board drawing and the rendering message helpers in **one
rendering bead** so there is meaningful unfinished work to hand off.

Implement the board renderer, move prompt, rejection messages, and two-player
win/draw messages specified by the original rendering work. The governing
references are `specs/001-five-in-a-row/tasks.md` (board-drawing tests and
rendering implementation, originally T018/T021) and its `contracts/cli.md`.
Follow that interim milestone: the later leave-game command and its prompt
hint remain deferred. Function names for message helpers can be chosen by
the agent and must be recorded for later callers.

**This exercise also requires focused unit tests of the prompt and message
helpers.** They verify the existing specified behavior; tag evidence with
the relevant existing requirement IDs. Write each set of tests before its
implementation and retain the expected initial failing result. A passing
board-drawing test alone does not verify the messages. This is a deliberate
adaptation of the recorded lecture run, where loop tests supplied the message
evidence. Here the criteria concern helper output; the board's display timing
and loop integration remain work for the unimplemented loop. Requirement-level
conformance rows must not be read as completion of the full game.

Rendering is complete when the board and all required messages have evidence,
the full test suite passes, existing engine/menu/EOF/architecture tests and
governing artifacts remain unchanged, and the bead contains a completion
summary and verification references. Record the applicable change type in
implementation commits, following the project constitution and task notes.

Keep parsing, the menu-caller refactor, and the game loop as planned work.
Their implementation is outside this exercise. Do not close the whole
two-player milestone or claim full-game conformance after finishing rendering.
Report genuine behavior disagreements for a developer decision and preserve
that decision before implementing affected behavior.

## Session 1: plan, review, draw the board, and stop

Write prompts that have your agent:

1. Review the existing specifications, contracts, tasks, and code; prepare
   and revise a concise execution plan outside Beads.
2. Create detailed Beads records, inspect dependencies/readiness, and review
   and refine the actual records before implementation.
3. Claim the rendering bead. Write the board-drawing tests first, record
   their intended failure, implement board drawing, and run verification.
4. **Stop before implementing the prompt, rejection, and result helpers or
   their tests.** Commit the partial work and keep the rendering bead
   `in_progress`.
5. Append a handoff to that bead: completed work, actual commands/results,
   remaining acceptance criteria, relevant files and commits, boundaries,
   and the next action.

The board tests can pass while the rendering bead is still unfinished.
End the session after the saved handoff. Save the interrupted project state
**before** starting session 2, using the checkpoint procedure below.

## Session 2: recover first, then finish

Start a new session without `--resume`/`--continue`, previous transcripts,
automatic memory, or a pasted explanation of the previous work. Your recovery
prompt should ask the agent to find the unfinished work from project guidance,
Beads, Git, and source/tests. Do not supply its issue ID or the completed and
remaining implementation details.

**The first turn is read/report only.** Require a report identifying the
active issue, governing references, completed work and evidence, remaining
criteria, unresolved questions, and proposed next action. Check that report
against the saved checkpoint before requesting edits. Capture and compare the
Git-visible working-tree state and current revision before and after this
turn, using the commands below. Inspect the tool transcript for other writes,
including changes to ignored Beads data. The recorder grants editing tools, so
read/report-only is an instruction whose adherence you must check. Record any
missed instruction or inaccurate recovery claim.

In a later turn of this same new session, ask the agent to finish only the
active rendering bead. It should write message-helper tests before code,
record the initial failure, implement and verify the remaining work, append
a completion/evidence summary, and close the bead with a reason when its
criteria are met. Preserve unresolved questions and record genuine discoveries
or clearly labeled proposed follow-ups; do not invent a bug to satisfy this
instruction. Save the final project state too.

## Record the sessions

Create `prompts/` and write your own prompt files. These example filenames
describe their purpose; the bundle does not supply the completed prompts.
You can add review turns using additional files and unique output prefixes.
Run these commands from the folder containing `run-session.py`.

```sh
mkdir -p prompts
# Write prompts/01-plan.txt, 02-beads-and-review.txt, and 03-board-and-handoff.txt.
python3 run-session.py --project work --prompt prompts/01-plan.txt --output recordings/01-plan
session1_id=$(python3 -c 'import json; print(json.load(open("recordings/01-plan.metadata.json"))["session_id"])')
python3 run-session.py --project work --prompt prompts/02-beads-and-review.txt --output recordings/02-beads-and-review --resume "$session1_id"
python3 run-session.py --project work --prompt prompts/03-board-and-handoff.txt --output recordings/03-board-and-handoff --resume "$session1_id"
```

Save the pre-recovery checkpoint, then write your recovery and continuation
prompts and start the fresh session:

```sh
# Capture the current revision, tracked-file state, and untracked paths.
git -C work status --porcelain=v2 --branch --untracked-files=all > recordings/04-before.status.txt
git -C work diff HEAD > recordings/04-before.diff
python3 run-session.py --project work --prompt prompts/04-recover-report.txt --output recordings/04-recover-report
git -C work status --porcelain=v2 --branch --untracked-files=all > recordings/04-after.status.txt
git -C work diff HEAD > recordings/04-after.diff
diff -u recordings/04-before.status.txt recordings/04-after.status.txt
diff -u recordings/04-before.diff recordings/04-after.diff
```

The status capture includes the current commit; the diff includes staged and
unstaged tracked-file changes. Both comparisons should be empty. Git does not
capture every possible write, so also inspect the agent's tool transcript.
If anything changed, preserve the evidence and assess the missed instruction
before proceeding. Check the recovered-understanding report against the saved
checkpoint, then request implementation in the same new session:

```sh
session2_id=$(python3 -c 'import json; print(json.load(open("recordings/04-recover-report.metadata.json"))["session_id"])')
python3 run-session.py --project work --prompt prompts/05-finish-rendering.txt --output recordings/05-finish-rendering --resume "$session2_id"
```

Each call records its exact prompt, raw JSONL messages/tool events, readable
Markdown, stderr, and session/model metadata. `--output` is a filename prefix:
`recordings/04-recover-report` creates files such as
`recordings/04-recover-report.jsonl` and `.md`. Use a new prefix for every call.
The first call in each session creates its ID; `--resume` continues that
session's history. The five example CLI calls span **two sessions**.

The recorder flags were checked against **Claude Code 2.1.310**, also used in
the recorded lecture. Check your installation with `claude --version`; the
metadata retains the actual version. The recorder disables skills/commands
with `--disable-slash-commands`, disables automatic Claude memory, and keeps
recordings outside the agent's project. Its default model is `sonnet`; use
`--model` to select an available model and retain the observed model in your evidence. Its default
per-call budget flag is 8 USD, a CLI estimate rather than an account-billing
guarantee. The `--budget-usd` option changes that limit; adequacy for this new
exercise has not been measured. A budget cutoff is not a completed handoff.
Inspect the saved result and continue the appropriate session with a new
output prefix until the required partial commit and Beads handoff exist
before saving the paused checkpoint. Do not give previous recordings to the
recovery agent.

You may use another course-approved harness if you can retain equivalent
prompts, tool transcripts, session boundaries, and project-state evidence.

## Save checkpoints and submit evidence

After session 1 has ended, run these commands from this exercise folder:

```sh
mkdir -p checkpoints
work/node_modules/.bin/bd -C work export > checkpoints/before-recovery.issues.jsonl
tar --exclude='work/node_modules' --exclude='work/.venv' --exclude='work/.pytest_cache' --exclude='__pycache__' -czf checkpoints/before-recovery.tar.gz work
```

After completing rendering, save a separate final checkpoint:

```sh
work/node_modules/.bin/bd -C work export > checkpoints/after-rendering.issues.jsonl
tar --exclude='work/node_modules' --exclude='work/.venv' --exclude='work/.pytest_cache' --exclude='__pycache__' -czf checkpoints/after-rendering.tar.gz work
```

The project archives retain source, tests, local Git history, and `.beads/`.
The issue exports make records easy to inspect; an export alone is not a full
replacement for the saved project and tracking history. Restore a checkpoint
into a new folder and reinstall its locked dependencies; its Git and Beads
state are already initialized.

Submit your prompt files, both sessions' recordings, the before/after Git
captures and comparisons, both checkpoints and issue exports, verification
output, and a short reflection. Explain what the fresh session recovered or
missed, how you checked it before edits, and how
the graph represents independent work and integration. Compare closure claims
with their supporting evidence. Review the submitted files for credentials.
Submit by **November 8, 2026**, using the course's announced submission location.

## Distribution and licensing

The planned public location is
`module-software-engineering/demos/lecture-beads/exercise-beads/`.
The [planned DownGit link](https://downgit.github.io/#/home?url=https://github.com/santoslab/agentic-software-engineering-public/tree/main/module-software-engineering/demos/lecture-beads/exercise-beads)
downloads this exercise folder after publication. The lecture's recorded-demo
archive is distributed separately for reproducing its parsing example.

Instructional prose follows [CC BY 4.0](starter/LICENSE-CC-BY-4.0);
scripts and configuration follow [MIT](starter/LICENSE-MIT). External tools
retain their own licenses.
