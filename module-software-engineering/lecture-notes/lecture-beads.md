# Beads: Managing Agent Work Across Sessions and Subsystems

> Companion reading for lecture slides 1–45, with the deck's command and source
> references available on slides 46–48. The notes explain the growing work
> graph, tool choices, setup and agent workflow, the recorded tic-tac-toe run,
> the brief parallel/distributed extension, and the accompanying exercise.
>
> Examples target Beads 1.3.2. The recorded implementation used Claude Code
> 2.1.310 and Sonnet 5.5. See the [slide source](../slides/lecture-beads.md) and
> [complete run record](../demos/lecture-beads/recorded-run/README.md).

This lecture uses coding agents to work on the familiar Spec Kit
five-in-a-row tic-tac-toe project. The game has a 9×9 board
where five or more marks in a line wins. Students already know its
specification, contracts, plan, and original task list, so we can concentrate
on organizing and continuing the execution work.

The central idea is a **persistent, queryable work graph**. As a project grows,
its tasks acquire dependencies, owners, progress, discoveries, and verification
evidence. An agent needs the relevant part of that graph and the governing
files for its current task. The same structure supports work divided across
subsystems, sessions, and agents. Work can proceed sequentially, or a
coordinator agent can orchestrate workers on independent tasks when the
interfaces and shared tracking environment permit that.

The recorded demonstration is sequential. Sonnet reviewed the plan, created
and refined the beads, implemented part of a parser task, and left a handoff.
A fresh session continued that task; later sessions implemented the remaining
work and closed the milestone after verification. The notes distinguish captured behavior,
proposed improvements, and the documented parallel/distributed extension.
The small seeded issue used to introduce fields is separate from that run.
Its progress text remains explicitly labeled as teaching data.

## What is Beads?

**Beads is an issue tracker designed for coding agents.** Its command-line
program is `bd`. A **bead**, also called an **issue**, is a tracked work item:
a task, feature, bug, investigation, or other bounded piece of work. Its fields
describe the work, governing context, acceptance criteria, status, ownership,
and progress. Relationships connect these items into a work graph.
([Beads 1.3.2](https://github.com/gastownhall/beads/tree/v1.3.2))

A blocking dependency identifies a prerequisite. An epic groups child issues
toward a larger goal. Labels and references can help select work for a
subsystem or concern. These structures answer different questions: which
deliverable a task belongs to, what it needs before it can proceed, and who
is working on it. They make independent work and integration points visible.
([Issues and relationships](https://beads.gascity.com/core-concepts/issues),
[queries](https://beads.gascity.com/cli-reference/list))

The records persist outside the conversation. An agent can query active or
ready work, read the selected issue, and follow its references to the
specification, contracts, code, and evidence. It need not load the entire
backlog into its context. The developer and agent can inspect the same
records; the agent normally creates and maintains the detailed items.
([Ready work](https://beads.gascity.com/cli-reference/ready))

GitHub Issues gives users and developers a shared place to discuss and track
project concerns. Beads emphasizes detailed agent execution: **what is ready,
who owns it, and what remains?** The distinction is audience and granularity.
GitHub also supports dependencies, APIs, CLI access, and agents. Beads can
complement that project tracker with a detailed operational work graph.
([GitHub dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies))

Session recovery is one benefit of the graph. The broader purpose includes
maintaining a growing collection of related work and coordinating its
execution across parts of a project. Actual parallel/distributed execution
also needs suitable code workspaces and access to the issue records; the
tracker does not launch workers or make coupled implementation independent.
([Agent coordination](https://beads.gascity.com/multi-agent/coordination))

## One bead, concretely

The opening bead is a prepared teaching illustration: its progress note is
example data, and the later recorded run uses a separate database and different
IDs. Consider the work item **“Parse player input for tic-tac-toe.”** The game needs
to recognize a move such as `4 7`, meaning row 4, column 7, and recognize a
choice from a menu. The work includes implementing those parsers and updating
the existing menu code that calls them. Its description should refer to the
game's input rules so that the implementation follows the specified formats.
In the Spec Kit project those rules are in the
[CLI contract](https://github.com/santoslab/agentic-software-engineering-public/blob/4d6a2cd/module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/specs/001-five-in-a-row/contracts/cli.md).

This example chooses one task for the CLI parsing changes. It follows the
original implementation task's scope: move parsing can be finished while
menu parsing and the caller refactor remain. The later recorded demonstration
uses that boundary for its planned interruption.
Beads does not require those parsers to share a bead; separate assignment
or verification needs can justify splitting them.

**The bead itself is the work item.** Its title names the work; its
description explains the scope and points to the information needed to do
it. The other fields help the developer and agent track the work and decide
whether it is complete.

| Beads field | Purpose in this example |
|---|---|
| **Title** | Names the task: parse player input for tic-tac-toe. |
| **Description** | Explains the changes to make and refers to the governing input rules. |
| **Acceptance criteria** | States the conditions for completion: the specified formats parse, menu behavior is preserved, and the required tests pass. |
| **Notes** | Records progress and the next action: move parsing is finished; menu tests and the menu refactor remain. |
| **ID** | Identifies this particular work item. The example's ID is `ttt-8fy`. |
| **Status** | Records its state. Here `in_progress` means the work has started and is unfinished. |

These are the fields used in our example; Beads supports additional fields
and metadata. The
[issue model](https://beads.gascity.com/core-concepts/issues) describes the
larger structure.

The slide uses three explanatory phrases: *context*, *done when*, and
*progress*. They describe what information to put in the fields above.
**Context** is the information needed to interpret the task, such as its
governing rules and relevant files; in this example, references belong in
the description. **Done when** explains the acceptance criteria. **Progress**
explains the notes. They are teaching labels, rather than three additional
field names in the JSON record shown next.

Acceptance criteria and progress notes answer different questions. The
criteria describe the result that must be established before the task is
complete. The notes describe what has happened so far and what to do next.
A note saying that move parsing is finished does not establish that menu
behavior is preserved or that all required tests pass. In a real work item,
the developer and agent should record the relevant verification results
alongside their progress claims.

The governing input rules still determine the required behavior. A short
description or acceptance summary points back to those rules; it does not
settle a new behavior merely by being entered in the tracker. For example,
the CLI contract specifies how move text is read, while the engine handles
whether the resulting square is in range and available. A parser task must
preserve that division.

## The same bead, as JSON

The command `bd show` retrieves a bead. Adding `--json` requests its
structured representation:

```sh
bd show ttt-8fy --json
```

Here `bd` names the installed Beads executable; the repo-local setup is
covered later in the lecture. The ID belongs to the example database used
for this capture. In your own project, use the ID assigned to your work item.
([Show command reference](https://beads.gascity.com/cli-reference/show))

The following excerpt preserves the values returned by Beads 1.3.2. The outer
array contains one issue object for this request:

```json
[
  {
    "id": "ttt-8fy",
    "title": "Parse player input for tic-tac-toe",
    "description": "Implement move/menu parsing. Update menu caller. Follow input rules.",
    "acceptance_criteria": "Required formats parse; menu behavior is preserved; tests pass.",
    "notes": "Move parser done; next: menu tests and refactor. (Example progress.)",
    "status": "in_progress"
  }
]
```

Read this against the preceding table. `title` and `description` identify and
describe the actual work. `acceptance_criteria` gives the completion
conditions. `notes` carries the progress update and next action. `id` and
`status` identify the record and its current state. There is no field named
`context`, `done_when`, or `progress` in this example.

The slide and this excerpt omit other metadata to keep the work item in
view. The [full captured response](../slides/examples/bead-show.json) also
contains the issue type, priority, assignee, timestamps, and other tracking
information. The excerpt is a selection of fields from that response, not a
separately invented JSON format.

The capture came from a real CLI call after creating an example issue in a
disposable repository. Its description, acceptance criteria, and progress
note were entered as teaching data. The output demonstrates how Beads stores
and returns a work item; the progress note is not evidence that an agent
implemented or tested the parser. Establishing those claims requires
examining the project changes and verification results.

## Motivation: resuming work from a previous session (in a clear context)

Suppose a previous session implemented part of the parser and ended before
the task was complete. A new session needs the active task and governing
rules, the changes already made, the checks performed, the remaining
acceptance criteria, and the next useful action. The stored claims need to
be checked against the actual files and results.

This is the problem addressed by **STATE.md** in *Other LLMs and Harnesses*. Its slide “Poor man's context management on a budget” proposed
a project-root state file, maintained with the agent's help at checkpoints
or before clearing/compacting context. Version control preserves the state
file alongside project changes. Ordinary text can carry that summary between
different harnesses and models.
([Earlier lecture, slide 15](https://github.com/santoslab/agentic-software-engineering-public/blob/main/weeks-01-03/slides/lecture-04-other-llms-and-harnesses.md#poor-mans-context-management-on-a-budget))

**A growing project needs more than a single saved summary or checklist.**
Work accumulates across subsystems. Tasks have different owners and
prerequisites, some can proceed independently, and discoveries create new
relationships. The agent needs to retrieve and update individual items
without repeatedly reconstructing the entire project's operational state
from one expanding narrative or task list.

Beads gives the work individually addressable records and queryable
relationships. A worker can select relevant issues, inspect what blocks
them, claim a task, and record its progress and evidence. Another session
can recover the same bounded item. Multiple workers can divide independent
items when the code and issue-sharing environment supports that execution.

The limitation here concerns a monolithic STATE.md/tasks.md used as the
operational tracker for a growing graph. It is not a claim that Markdown
cannot store structured records: Ticket, discussed later, uses separate
ticket files and tracking commands. STATE.md remains a useful summary and
the original tasks.md remains planning input. The execution graph supplies
the ongoing selection, ownership, dependency, and handoff machinery.

## SDD: from specifications to a growing work graph

In specification-driven development, the specification states required
behavior and guides planning, implementation, and verification. The plan
describes an approach; a work breakdown identifies tasks needed to realize
and verify the behavior. A document, an issue tracker, or another planning
tool can supply that initial breakdown.

We use **Spec Kit** because students have seen the tic-tac-toe specification
workflow. Two examples from its familiar tasks.md are writing tests for player
move input and implementing move/menu parsing with the existing menu-caller
refactor. The same plan also includes rendering, the game loop, and verification.
We explain those tasks by name. The original task labels are retained in the
records and the reference appendix for traceability, separately from Beads
issue IDs. No recall of those codes is needed to follow the example. Other
SDD workflows may use other labels and artifact formats.
([Original task list](https://github.com/santoslab/agentic-software-engineering-public/blob/4d6a2cd/module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/specs/001-five-in-a-row/tasks.md))

During execution, the work acquires live status, owners, discoveries,
evidence, and dependencies across parts of the system. The operational
question becomes: **what is ready in this part of the project, and how does
it connect to the rest?** A structured tracker maintains and queries those
changing records. Its dependency graph also exposes work that can be
assigned separately and integration work that must wait.

In this lecture's working copy, tasks.md stays as the original planning
input and Beads is authoritative for live execution status. The records
retain original IDs and governing references. Regrouping tasks into useful
execution units changes tracking granularity; it does not remove an
obligation or authorize changing specified behavior.

## What we want the work graph to answer

The graph should let an agent find the work relevant to a subsystem or goal,
identify its prerequisites, and distinguish ready work from active work.
Assignees identify ownership. Progress notes explain what has happened and
what remains. Discovery links explain where new work originated. Acceptance
criteria and evidence explain why completion is claimed.

Grouping and ordering are separate. A collection of tasks may belong to one
milestone or subsystem while having different prerequisites. Independent
branches can be assigned separately; integration waits for the necessary
results. A worker retrieves the selected issue and its linked governing
files, keeping its working context focused on that part of the graph.

These capabilities address the growing operational record, including
continuation across sessions. The agent maintains the detailed records
within the agreed plan; the developer can inspect the graph, redirect
priorities, and assess evidence. A closed status records a conclusion.
The linked files, tests, reports, and decisions establish whether that
conclusion is warranted.

## When is Beads useful?

Beads becomes useful as the work record grows in tasks, relationships,
subsystems, and workers. An agent can query a selected part of the backlog,
find ready work, inspect ownership, and follow dependencies beyond its
current subsystem. Independent tasks can be assigned separately while the
graph keeps integration prerequisites visible. Discoveries remain linked
to the work that exposed them.
([Queries](https://beads.gascity.com/cli-reference/list),
[coordination](https://beads.gascity.com/multi-agent/coordination))

The same record supports context recovery. Important information can be
lost **within a session** when compaction replaces a long conversation
with a shorter summary. The direction may survive while a constraint,
decision, partial change, or verification detail needed for the next action
is omitted.

In *Other LLMs and Harnesses*, the slide “Compaction: what happens when
context runs out” compared actual compaction output. We saw summaries
missing details needed to continue. Those observations describe the runs
examined in that lecture, not permanent rankings of current harnesses.
([Earlier lecture, slide 14](https://github.com/santoslab/agentic-software-engineering-public/blob/main/weeks-01-03/slides/lecture-04-other-llms-and-harnesses.md#compaction-what-happens-when-context-runs-out))

*Context, Cost, Verification, and the Road Ahead* also discusses how
managing the context window trades verbatim detail for a summary. The practical response is to preserve the particular
facts needed for implementation and verification, then retrieve them when
the working context changes.
([Managing the window in practice](https://github.com/santoslab/agentic-software-engineering-public/blob/main/weeks-01-03/lecture-notes/lecture-06-context-cost-verification-and-the-road-ahead.md#2-managing-the-window-in-practice))

Beads cannot recover information never recorded. The agent needs to write
the relevant context, progress, evidence, and next action before loss, then
read the issue and linked files when continuing. This preserves the useful
checkpoint practice from STATE.md while making the growing work collection
individually queryable.

A short immediate change may need little tracking. The motivating case for
Beads is an evolving graph of work across parts of a project, not merely a
longer saved conversation. Our lecture demonstrates the mechanism with a
small sequential run; it does not measure large-backlog or distributed
performance.

## Project issues and agent work items

**An SDD task document, GitHub Issues, and Beads can all be used together.**
They serve complementary roles: the document records the planned work derived
from specifications, GitHub tracks the broader project issue, and Beads
maintains the evolving detailed execution graph. Consider who reads each record and what
information that audience needs. An SDD task document can hold a detailed work
breakdown and use Git to preserve its changes. GitHub Issues and Projects
provide a shared place for reporting bugs, proposing features, discussing
work, and coordinating developers. Agent work items often need a smaller,
more specific scope, together with the context, prerequisites, checks, and
progress notes needed to execute and resume that work.

For example, a project issue might be **“Add two-player mode.”** One of the
agent work items supporting it could be **“Implement move/menu parsing;
preserve existing menu behavior; run parser/menu tests.”** Other work items
could cover rendering, the game loop, and milestone verification. The broader
issue communicates the feature being delivered; the detailed records guide
and preserve the implementation work.

GitHub can represent the detailed tasks too: it supports sub-issues,
dependencies, CLI access, and APIs. The concern is the effect on the issue
list's audience. Creating a project issue for every small agent task or
intermediate investigation can bury the bugs, features, and coordination
items that users and developers need to follow. Keeping the execution-level
backlog in Beads is one way to keep that detail available to the agent while
preserving the usefulness of the project issue list.
([GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues),
[Beads work graph](https://beads.gascity.com/core-concepts))

The records can be linked without duplicating their responsibilities. The
SDD task document provides the planning input and references to the governing
specification. A GitHub issue such as “Add two-player mode” can link to that
plan and to the Beads work items implementing it. Beads records the current
status, ownership, dependencies, verification evidence, and resumption notes
for each detailed task. The broader project's progress can be assessed from those
linked results.

Each work item should have one authoritative place for its current status.
When combining the tools this way, keep the original task IDs for traceability
and use Beads for live execution status, rather than independently maintaining
the same task's status in two places. The workflow needs that explicit policy;
linking the records does not automatically synchronize them.

As the project grows, the detailed graph may span several subsystems.
Agents can select the items relevant to their part while following shared
interfaces and dependencies to related work. The broader project issue
continues to communicate the deliverable, and the SDD artifacts continue
to govern its intended behavior. Those roles remain useful alongside the
operational graph.

Spec Kit's optional GitHub extension can convert a task list into issues.
Before using that route, decide which level of detail belongs in the shared
project tracker. Exporting every execution task is a workflow decision with
consequences for the people using the issue list.
([Spec Kit GitHub extension](https://github.com/github/spec-kit/blob/main/extensions/github/README.md))

## Alternatives: choosing an agent work tracker

The choice between agent work trackers depends on the work you need them to
do and the record format you want to maintain. Task Master, Ticket, and Beads
all persist tasks and support dependencies. The following preferences are
inferences from their documented designs, rather than a measured ranking.

**Task Master** provides AI commands that turn requirements into task
records and split selected tasks into subtasks. For example, `parse-prd`
asks its configured model to generate a task breakdown, and `expand` asks
it to break a selected task into smaller pieces. The commands supply the
prompts, model calls, task structure, and saving of the results. These AI
features require configuring a model provider or a supported agent CLI.
([Task Master](https://github.com/eyaltoledano/claude-task-master))

**There is no established evidence for the effectiveness of these AI planning
commands.** The examined expansion unit tests mock model output; the manual
generation benchmarks concern timing and progress reporting. They do not
establish improvements in plan quality or resulting software. An effectiveness
comparison would need the same specification, repository context, model, and
budget, with repeated runs measuring requirements coverage, dependency errors,
review effort, and implementation success.
([Expansion tests](https://github.com/eyaltoledano/claude-task-master/blob/1c7365cab1f1d8ee5b0ecc2292a9ba9cf5efea2e/tests/unit/scripts/modules/task-manager/expand-task.test.js),
[manual benchmarks](https://github.com/eyaltoledano/claude-task-master/blob/1c7365cab1f1d8ee5b0ecc2292a9ba9cf5efea2e/tests/manual/progress/TESTING_GUIDE.md#-benchmarks))

**Ticket (`tk`)** is a useful candidate when you want task records that you
can inspect as ordinary files and review with the rest of your Git changes.
It stores Markdown tickets with YAML metadata in `.tickets/`, and provides
commands for dependencies, ready work, status changes, and notes. The core
tool is a Bash script using standard command-line utilities; its JSON query
command also requires `jq`. Its file-based approach keeps the storage easy
to inspect. Collaboration follows the task files through Git, including any
merges needed when branches change those records.
([Ticket](https://github.com/wedow/ticket))

**Beads (`bd`) is designed for coding agents.** The agent can break down
work, create beads, link prerequisites, revise the breakdown as it learns,
select ready work, and record progress and verification. It can also capture
new discoveries and close tasks when their acceptance criteria are met. The
agent performs the planning and calls `bd` to preserve and maintain the work
record. An existing SDD plan is one possible input; an agent can also develop
a breakdown from the governing requirements and specifications.
([Beads 1.3.2](https://github.com/gastownhall/beads/tree/v1.3.2))

Task Master provides built-in model calls for requirements parsing and task
expansion.
A coding agent using Beads can perform that reasoning itself and maintain the
resulting work graph through the CLI. Both approaches support agent work.
Beads additionally provides workflow context through `bd prime`. The agent
still needs to follow the recovery procedure after compaction or a session
boundary.

The storage choice brings an operational tradeoff. Task Master's local
storage reads and parses the whole JSON file even for a single-task lookup,
and rewrites it for status updates. Those operations process data in proportion
to the backlog's file size. Tags group tasks within that file. Our measured
latency through 10,000 synthetic tasks establishes behavior within the tested
range; it does not establish scalability as the backlog or writer count grows.
([Task Master storage](https://github.com/eyaltoledano/claude-task-master/blob/1c7365cab1f1d8ee5b0ecc2292a9ba9cf5efea2e/packages/tm-core/src/modules/storage/adapters/file-storage/file-storage.ts))

Prefer Ticket when you want readable task files and ordinary Git review;
prefer Beads when agents need to maintain a growing work graph with ownership,
ready-work queries, dependencies across subsystems, discoveries, and handoffs.
The same structure can guide separate workers when the execution environment
supports that coordination.

The lecture starts from the existing SDD plan because students have seen it.
The agent turns that plan into beads and maintains them while implementing
and verifying the work. This makes the agent's role in planning, tracking,
and recovery concrete. That selection does not establish
that it is the best tracker for every project. Compare the planning help,
record inspection, recovery behavior, and maintenance effort you actually
need. The Beads workflow has been exercised locally. A separate
[Task Master 0.43.1 assessment](../demos/lecture-beads/assessment/task-master-assessment.md) tested
local backlog size and concurrent CLI updates; it found lost updates with
concurrent writers, despite successful command responses. The AI planning
features and hosted team mode were not evaluated. Ticket remains a comparison
based on its project documentation.

## Keep the roles of the documents clear

Specifications and contracts govern required behavior and subsystem interfaces.
The plan describes the implementation approach, and `tasks.md` supplies
the original work breakdown for this example. Beads maintains the evolving
work graph: current status, ownership, prerequisites, discoveries, evidence
summaries, and handoffs. The code implements the behavior; tests and reports
provide the detailed verification evidence.

This separation matters when agents work on different parts of a system.
Each worker needs the relevant contracts and issue context, while shared
dependencies identify what must be integrated and when. The work graph
coordinates execution within the agreed behavior.

**Store an evidence summary in the bead.** Record what was checked, the
command or procedure used, the outcome, the revision or working-tree state
checked, and references to the relevant reports and commits. Include failures
and acceptance criteria that remain unverified. A later session should be able
to read the summary, locate the full evidence, and establish what still needs
work. A status of `closed` alone does not establish that verification succeeded.

A work item can expose a gap or contradiction in a specification. Record the
question and the affected work, then obtain a developer ruling. Updating the
tracker does not change the governing requirements or grant the agent
authority to resolve a change in intended behavior.

## Install Beads; initialize the game project

The [Beads project download](https://downgit.github.io/#/home?url=https://github.com/santoslab/agentic-software-engineering-public/tree/main/module-software-engineering/demos/lecture-beads)
contains the pinned Beads **1.3.2** installer, reproduction starter,
self-contained exercise-beads/ folder, and sanitized recorded-run/ materials.
Slides and notes are distributed separately.

Choose the setup instructions for the activity you are doing:

- The [recorded-demo archive](../demos/lecture-beads/tictactoe-beads-sonnet-starter.tar.gz)
  supplies the exact prompts for reproducing the lecture's parsing run.
- The [exercise-beads handout](../demos/lecture-beads/exercise-beads/README.md) supplies the
  rendering exercise, for which students write their own prompts.

Both packages have a setup.sh that creates work/, installs the locked tools,
and initializes Git and Beads. Follow that package's README; initialization
is already complete after its setup script. Restored checkpoints also retain
their existing tracking state.

The following manual commands illustrate installation and initialization for
a separate game copy that has not yet been initialized. From the extracted
installer project folder, install the CLI and save its path:

```sh
npm ci
export PATH="$PWD/node_modules/.bin:$PATH"
export BD="$PWD/node_modules/.bin/bd"
"$BD" version
```

**Here, npm is the installer for the Beads CLI.** The downloaded project's
`package.json` lists `@beads/bd` version **1.3.2**. Its `package-lock.json`
records the dependency versions, and `npm ci` uses that lockfile to install
the tool under `node_modules/`, exposing `node_modules/.bin/bd`.

CI means continuous integration, where clean, repeatable installs are useful.
We use the command locally for the same reproducibility: students get the
Beads version used in the lecture. It requires the lockfile to match
`package.json`, replaces an existing `node_modules` directory, and leaves the
package manifests unchanged.
([npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/))

Next, enter the separate disposable game working copy and initialize tracking
there:

```sh
cd /path/to/tictactoe-work
"$BD" init --prefix ttt
```

`--prefix ttt` configures the project's issue-ID prefix. A later `bd create`
assigns the rest of each new issue's ID; initialization itself does not create
the milestone epic or its child tasks.

`BD` identifies the installed executable; the game's `.beads/` directory
contains that project's tracking records. Set `PATH` and `BD` in each terminal
used for the lecture, and start the agent from that configured terminal. The
`PATH` entry lets the generated integrations invoke `bd` by name. Inspect
initialization output and the generated files; initialization can also create
a Git commit for its setup files.
([Installation](https://beads.gascity.com/getting-started/installation),
[initialization](https://beads.gascity.com/cli-reference/init))

## Inspect the generated agent guidance

**`bd init` normally creates or updates `AGENTS.md` and `CLAUDE.md` and
installs project integrations.** This behavior was checked with Beads 1.3.2
in disposable repositories, both empty and with existing instruction files.
Existing policy text was preserved in those checks. The generated guidance
points the agent to `bd prime` and describes the core work-tracking workflow.
The `--skip-agents` option suppresses instruction and integration setup when
you deliberately want to manage it yourself.
([Beads 1.3.2 initialization and onboarding](https://github.com/gastownhall/beads/blob/v1.3.2/README.md#-quick-start))

**`bd init` sets up the project; `bd prime` supplies guidance for the current
agent session.** Run initialization when setting up tracking in a project.
Run `bd prime` at session start or after compaction when the agent needs the
Beads workflow again. Its output includes work-tracking commands and workflow
guidance, plus saved project memories when present. The agent must read the
output for it to become useful session context.
([bd prime](https://beads.gascity.com/cli-reference/prime))

**The course-specific policy belongs in `CLAUDE.md` or `AGENTS.md`, according
to which instruction file the harness reads.** Generated guidance in those
files tells the agent to run `bd prime`. That command prints Beads workflow
context; it does not simply print those instruction files or repeat project
initialization. The agent reads the project policy alongside the command's
output.

Inspect the instruction file and the project integrations. Keep the generated
guidance, preserve existing project policy, and add the lecture's policy
alongside it:

```markdown
Keep Spec Kit task IDs; tasks.md is the original plan.
Use Beads for live status, evidence summaries, and handoffs.
Read specifications/contracts before editing.
Ask the developer about changes to specified behavior.
```

These additions establish traceability to the familiar SDD artifacts and say
what evidence and handoff information to retain. They do not replace the
specification, contract, or constitution. The instruction file tells the agent
where to begin; `bd prime` supplies work-tracking guidance; the issue and its
linked project files provide the context for the actual task.

For each new session, make the instructions and executable available. Generated
hooks may provide workflow context automatically, but the agent still needs
to inspect the relevant work item and governing files. Run `bd prime` explicitly
when that workflow context is missing.

## What `bd prime` prints

The slide shows excerpts from actual Beads 1.3.2 workflow context supplied
by a SessionStart hook during the recorded Sonnet run. The
[full recorded output](../slides/examples/sonnet-run/prime-workflow.txt)
preserves the decoded hook text; ellipses on the slide mark omitted sections.
The [consolidated transcript](../demos/lecture-beads/recorded-run/transcript.md#call-03)
shows the hook's decoded workflow context and outcome.

The opening reminder tells the agent to reload workflow guidance after
compaction, clearing context, or starting a new session. The core rule says
to create the work record before coding and mark it in progress when work
starts. The query reminders distinguish available work, active work, and a
particular issue's details. Other sections cover creating and updating issues,
dependencies, verification tools, and persistent memory commands.

The closing checklist asks the agent to close completed issues, run the
relevant quality gates, inspect Git state, and report a handoff. Its
local-only/no-remote wording reflects the recorded demo's setup, which had
no Git remote. That wording is configuration-specific; it does not establish
a universal rule against sharing Beads records or pushing project code.

**The output is a workflow briefing that the agent must read.** The agent
still queries the actual work items and reads the governing files to recover
what has been done and what should happen next. Saved project memories can
also appear in prime's output when present. Running the command does not
restore the whole earlier conversation.
([bd prime](https://beads.gascity.com/cli-reference/prime))

## How the record reaches a fresh session

A session leaves two kinds of durable information. It updates the work record
in Beads with the task's state, evidence summary, remaining work, and next
action. It also changes project files: code, tests, reports, and any approved
specification amendments. A fresh session needs to read both to establish
where the work stands.

![A session records progress and changes project files; a fresh session reads both.](../slides/diagrams/session-recovery.svg)

**Saving information and bringing it into the agent's context are separate
actions.** The project instructions tell the agent how to begin. `bd prime`
provides the Beads workflow guidance. The agent then queries unfinished work,
reads the selected issue with `bd show`, and follows its references to the
specification, contract, code, and verification evidence. Those command
results and file contents enter the current session as the agent reads them.
([Beads concepts](https://beads.gascity.com/core-concepts),
[bd show](https://beads.gascity.com/cli-reference/show))

For example, a parser task might record that move parsing is implemented and
menu parsing remains. The next session should inspect the actual changes,
read the input contract, and check the recorded verification results before
continuing. The summary gives it a starting point; the project files and
evidence establish whether the summary still describes the current state.

This recovery procedure also applies after compaction within a session.
Retrieve the relevant issue and linked files as needed. The whole backlog
does not have to enter the context at once. Useful recovery depends on the
previous session having recorded enough information and the current session
actually reading it.

## The agent's daily loop

**The coding agent normally performs this loop.** It runs the CLI through its
shell tool, implements the selected task, runs verification, and updates the
work record within the agreed scope. Scope and specified behavior are
established during planning. The agent reviews and refines the work items and
dependencies against that plan as it proceeds. New specification gaps or
proposed scope changes return to planning for a developer ruling; the developer
also assesses the resulting evidence before accepting completion. The commands
below make the agent's actions explicit; the developer can also use the CLI
to inspect or correct the record.

At session start, the agent loads workflow guidance and checks both work
already started and available new work:

```sh
"$BD" prime
"$BD" list --status in_progress
"$BD" ready
```

The two task queries answer different questions. `list --status in_progress`
shows unfinished work that has already started. `ready` shows open work with
no active blockers and excludes work in progress. An empty ready list therefore
does not mean there is nothing to resume. **The agent resumes unfinished work
first; the developer can redirect priorities.**
([bd ready](https://beads.gascity.com/cli-reference/ready))

The agent selects a task and reads its full record before acting. In the
following commands, `<selected issue ID>` represents an actual ID returned by
the tracker. The agent assigns that value to the shell variable `task_id`;
listing issues does not set the variable automatically.

```sh
task_id="<selected issue ID>"
"$BD" show "$task_id"
"$BD" update "$task_id" --claim
```

The claim records the assignee and changes the status to `in_progress`.
Claiming an issue already owned by the same actor is idempotent. The issue's
scope and acceptance criteria, together with the governing specification and
contract, determine the work and verification required.
([bd update](https://beads.gascity.com/cli-reference/update))

The agent implements the task, inspects the diff, and runs the required
verification. It records progress and an evidence summary as the work proceeds.
The following template shows the information it should record from the actual
results:

```sh
"$BD" update "$task_id" --append-notes \
  "<checks, results, evidence references, remaining work, and next action>"
```

`--append-notes` retains earlier notes; `--notes` replaces the notes field.
If verification fails or acceptance criteria remain unchecked, the agent
records that state and leaves the task unfinished. When ending a session
partway through a task, it makes the next action specific enough that another
session can resume it.

After satisfying the acceptance criteria, the agent closes the task with
the actual verification summary and references in the close reason:

```sh
"$BD" close "$task_id" --reason "<verification summary and evidence references>"
```

Closing records a completion claim. Its reason and the linked evidence let
the developer or a later session assess that claim. The command does not run
the tests or establish conformance on its own.
([bd close](https://beads.gascity.com/cli-reference/close))

## The agent writes actionable beads

The agent drafts and refines work items from the specifications and plan.
Each bead should identify a bounded result, its governing context, and the
verification needed to establish completion. That makes the record useful
both to the agent doing the work and to a later session recovering it.

Consider the difference between **“Finish the CLI”** and **“Parse player
moves and preserve menu behavior.”** The latter names a result that can be
implemented and checked independently of the game loop. The original plan
includes move-parser tests, implementation of move/menu parsing, and the
existing menu-caller refactor. This run groups that work into one bead and
keeps the original task labels for lookup. The readable name carries the
meaning; the labels provide traceability.
([Original task list](https://github.com/santoslab/agentic-software-engineering-public/blob/4d6a2cd/module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/specs/001-five-in-a-row/tasks.md))

The description should point to the input rules in the CLI contract: C-7
covers move formats, and C-1/C-2 govern menu choices. The acceptance criteria
should cover the specified parsing behavior, preservation of menu behavior,
and the required tests. The work boundary also matters: implementing the
two-player game loop belongs to a different bead.
([CLI contract](https://github.com/santoslab/agentic-software-engineering-public/blob/4d6a2cd/module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/specs/001-five-in-a-row/contracts/cli.md))

These references preserve details that a short task title cannot carry. For
example, the move parser can recognize signed integers and return a square
whose coordinates are out of range; the engine decides whether the move is
legal. Moving range validation into the parser would change that agreed
division of responsibility. Likewise, omitting the menu-caller refactor would
leave part of the original parser/refactor task unfinished.

The agent chooses task granularity that supports implementation and
verification. A bead can include several related changes that establish one
result. Splitting every line of code into a separate issue would add tracking
work without necessarily improving recovery or verification.

## Issues, epics, and their relationships

An **issue**, also called a **bead**, is a tracked work item. An **epic** is
an issue for a larger goal, grouping related **child issues**. The recorded
example uses epic ttt-cik for the two-player milestone, with four children
covering rendering, parsing, the loop, and verification.
([Issue model](https://beads.gascity.com/core-concepts/issues))

| Relationship | Question answered | Example |
|---|---|---|
| Blocking dependency | What is a prerequisite? | Loop needs Parser and Renderer. |
| Parent / child | Which larger goal contains this work? | Parsing belongs to the two-player milestone. |
| Discovered from | Which work exposed this item? | A parser concern links back to the parsing task. |

Epics can organize milestones or subsystem goals; labels and references
can also select a subsystem's work. There need not be exactly one epic
per subsystem. Whatever grouping is chosen, dependencies across groups
still need to be explicit. Parent membership does not replace the intended
prerequisite edges.

**Priority expresses importance; dependencies express prerequisites.**
A high-priority task may still be blocked. A discovery link records origin;
if the new item is a prerequisite, the agent must also record the blocking
relationship. The agent maintains these links against the plan and actual
execution needs.

The demo's Parser and Renderer are independent tasks within the CLI
milestone, not two distinct architectural subsystems. Their graph shows
how independent work and integration points are represented. Larger
projects can use the same structure across subsystem boundaries when
interfaces and dependencies support that division.

## Dependency direction: read it as a sentence

The agent adds and inspects dependencies through the CLI. Before these
commands, it assigns `loop_id`, `parse_id`, and `render_id` the actual IDs of
the corresponding work items. These variable names describe their roles;
they are not literal Beads IDs.

```sh
"$BD" dep add "$loop_id" "$parse_id"
"$BD" dep add "$loop_id" "$render_id"
"$BD" dep tree "$loop_id"
```

Read the first command as **“The loop depends on the parser.”** The first
positional ID is the dependent work item; the second is its prerequisite.
The second command adds rendering as another prerequisite of the loop.
Without an explicit relationship type, `dep add` creates a blocking dependency.
The final command displays the dependencies rooted at the loop issue, letting
the agent inspect what blocks it.
([Dependency command reference](https://beads.gascity.com/cli-reference/dep))

The lecture's diagrams draw arrows from prerequisite to dependent: a parser
arrow points toward the loop because the parser enables that work. The
command's arguments read in the other order: first name the work that must
wait, then name what it needs. Reading the command aloud helps prevent
reversing that relationship.

When the parser and renderer are complete, those prerequisites are satisfied.
Other blockers, if present, still matter. The graph records the ordering;
verification of the parser and renderer establishes whether their completion
claims are warranted.

## Steve Yegge's advice: from plan to beads

Steve Yegge describes this workflow in **“Beads Best Practices,”** published
November 24, 2025, in the section **“Plan Outside Beads, Then Import.”** The
following is a paraphrase of his advice for a larger plan:

1. Develop the plan with a planning tool and have the model revise it.
2. Ask the agent to create detailed epics and issues, preserving design context,
   dependencies, and opportunities for independent work.
3. Ask the agent to review and refine those records so implementing agents can
   follow them effectively.
4. Iterate on both the plan and its Beads representation before implementation.

([Yegge's article](https://steve-yegge.medium.com/beads-best-practices-2db636b9760c))

Yegge suggests repeating plan and bead refinement, potentially up to five
times. That is guidance rather than a fixed required count. He does not
explicitly require a fresh session for each planning or bead-review pass.
His separate advice to restart agents frequently concerns moving on after a
task is finished.

The review is itself agent work. In this lecture, the familiar Spec Kit
specifications and plan supply the input; the agent creates and improves the
execution records. We use the article as practitioner guidance. Its
recommendations do not establish an experimentally measured benefit, a
required number of review passes, or a need for an epic in every small task set.

## The agent reviews beads against the plan

**Planning establishes the scope, required behavior, and acceptance criteria.**
The agent then checks whether its work records faithfully express that plan.
This review can change task wording, granularity, and relationships while
preserving the agreed result.

The agent checks coverage: does every planned obligation appear in a work
item, and has any work been duplicated or omitted? It checks whether each
item gives an implementing session enough context and a verifiable outcome.
It also checks the dependencies against the actual implementation needs and
splits or combines tasks where that improves execution. It repeats the review
before implementation and maintains the records as work progresses.

For the parser bead, a review should catch a missing menu-caller refactor
because that change is already required by the original parser/refactor
task. Adding the omitted work to the bead restores coverage of the existing
plan. The agent can make that
correction within the agreed scope. It does not need a new developer decision
for each routine improvement to the work record.

**A new specification gap or proposed scope change returns to planning for a
developer ruling.** For example, supporting an input format that the contract
currently rejects would change intended behavior. The agent records the
question and its references, obtains the ruling, and brings any approved
amendment into the governing artifacts and affected work items before
implementing that change.

The developer's role is to establish direction and rule on such changes,
then assess the resulting evidence before accepting completion. The agent
performs the detailed task review, implementation, verification, and tracker
maintenance within that agreed boundary. Beads preserves those decisions and
the progress made under them.

## Recorded run: six sessions, nine CLI calls

The [recorded transcript on GitHub](https://github.com/santoslab/agentic-software-engineering-public/blob/main/module-software-engineering/demos/lecture-beads/recorded-run/transcript.md)
combines all nine calls in one sanitized Markdown file, with session
boundaries, executed prompts, visible responses, and tool activity.

The following walkthrough uses an actual Sonnet run from the unfinished
course project. It follows the workflow introduced earlier: review the
plan outside Beads, file the epic and issues, review and refine those
records, then implement and verify one bounded item at a time. The parser
task is deliberately paused with useful work unfinished so that a fresh
conversation has something substantive to recover.

The [recorded-run materials](../demos/lecture-beads/recorded-run/README.md) include
the exact prompts, a single sanitized transcript, verification evidence,
and restorable project/Git/Beads snapshots after each stopped stage.
Original raw CLI captures remain in the authoring repository. The source
and tests were written by Sonnet. The orchestrator prepared the starter,
supplied recorded execution clarifications, captured state, and independently
checked the final result. It did not hand-edit the agent's realization.

**A session here means one conversation history.** A prompted CLI call can
start a new session or continue an existing one with `--resume`. The recorded
workflow used **nine successful prompted CLI calls across six sessions**:

| Session | Prompts / CLI calls | Work |
|---|---|---|
| 1 | 01–04 (four calls) | Review the execution plan; create beads; review and refine them twice |
| 2 | 05 | Implement move parsing; save the partial commit and handoff |
| 3 | 06 | Recover in a fresh session; finish menu parsing and the caller refactor |
| 4 | 07 | Implement and verify rendering |
| 5 | 08 | Implement and verify the two-player loop |
| 6 | 09 | Verify the milestone; close the verification bead and epic |

Slide 23 shows this map; the stage headings and later checkpoint table use
these same session numbers. Calls 02–04 resumed session 1. Each of the later
five calls started a fresh session. The [run index](../demos/lecture-beads/recorded-run/transcript.md#session-map)
links the exact prompts and consolidated transcript, including session IDs
and call boundaries. Diagnostic calls and the initial authentication failure
are outside this workflow count.

Work proceeded sequentially. The graph exposed independent tasks, but the
run did not execute them in parallel or across machines. The demo prompt
specified the parsing task and its stopping point; the process ended normally
after saving its handoff. The review count and mid-task pause are teaching
adaptations of Yegge's workflow, not a random-crash or compaction experiment.

## The recorded run starts from an unfinished project

The source repository is
**[santoslab/agentic-software-engineering-public](https://github.com/santoslab/agentic-software-engineering-public)**,
specifically its Spec Kit tic-tac-toe demo under
module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/.
The course repository was checked at the supplied revision
`b4bf5c1679093c0baa90c7105038868b651c50a3`, where that game is already
implemented.

The recorded starter instead comes from an earlier saved state,
`4d6a2cdc70cfd3fc4ffc5d117ad1078d69b206f8`, before the two-player milestone
was implemented. The engine, evidence tooling, and CLI shell already work.
Board rendering, move/menu parsing, the two-player loop, and milestone
verification remain. That is the starting state preserved by the archive;
the newer completed game would not reproduce the same experiment.
([Original checkpoint](https://github.com/santoslab/agentic-software-engineering-public/tree/4d6a2cd/module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe))

The independent starter check recorded **44 passing tests**. The specifications,
contracts, plan, tasks, and existing source/tests were exported unchanged.
Preparatory files added the tracking policy, pinned local Beads dependency,
and reproduction tools. The recorded runtime was Claude Code 2.1.310,
`claude-sonnet-5-5`, Beads 1.3.2, Python 3.12.13, and pytest 9.1.1 on macOS.
([Baseline test output](../demos/lecture-beads/recorded-run/verification/baseline-tests.txt))

The [recorded-demo reproduction archive](../demos/lecture-beads/tictactoe-beads-sonnet-starter.tar.gz)
contains the pristine starter, exact staged prompts, setup script, recorder,
and a file manifest. It excludes completed implementation, an issue database,
dependencies, and previous conversations. Extract it and follow its README.
Its setup.sh creates an independent working copy, installs the locked tools,
initializes Git and Beads, and leaves the source starter intact. Those are
the setup operations explained earlier; do not initialize tracking again
after that script or when restoring an already initialized checkpoint.

The first planning pass prompted recorded clarifications about test ordering,
the selected milestone boundary, and keeping the intended interruption inside
one parsing issue. They are included in prompt 02 of input revision 2. The
reproduction archive includes those clarifications, and the published prompt
copies preserve every executed request. New runs
can produce different issue IDs, decomposition, or output; the archives let
students inspect the particular run used in the lecture.

## Session 1: plan and review outside Beads

The first successful agent invocation was planning only. The
[exact prompt](../demos/lecture-beads/recorded-run/prompts/01-plan.txt)
asked Sonnet to read the project policy, existing specification, tasks,
contracts, and relevant code; write an execution plan outside Beads; and
review and revise that plan at least once. It required preservation of the
approved behavior, test-first obligations, public API boundaries, and the
separately verified menu-caller refactor. Unresolved questions had to be
reported. Creating issues and implementing code were deferred to later turns.
The slide presents an abridged paraphrase of that prompt.

Sonnet produced planning/beads-plan.md and planning/plan-review.md. Its
initial plan described nine internal work steps. The review found that
writing all future game-loop tests before the menu refactor would leave
the full suite failing when that refactor had to be verified. It therefore
put those tests after the refactor while retaining tests before the code
they cover. It also separated the new parser implementation from the
behavior-preserving menu refactor into distinct commits, and proposed
direct menu-parser tests missing from the original test-task description.
([Planning transcript](../demos/lecture-beads/recorded-run/transcript.md#call-01))

The first pass left questions about those tests, execution order, and the
boundary between this milestone and the later leave-game feature. The next
prompt supplied recorded clarifications from the existing starter authority:
add the menu-parser tests, verify the refactor before writing the future
loop tests, and retain the selected milestone's interim behavior. It also
explicitly required the move parser, menu parser, and menu-caller refactor
to remain in one bounded bead for the planned interruption. Sonnet chose
the remaining grouping and dependencies. This constraint is part of the
input to the recorded result, and should be visible when evaluating it.
([Exact creation prompt](../demos/lecture-beads/recorded-run/prompts/02-create-beads.txt))

The saved [execution plan](../demos/lecture-beads/recorded-run/planning/beads-plan.md)
and [written review](../demos/lecture-beads/recorded-run/planning/plan-review.md)
include the subsequent clarifications as revision 2. The first transcript
and after-planning archive preserve the earlier state. The transcript's
filename contains retry because an authentication failure was retried
before successful model work; it does not identify a second planning pass.
The plan review and revision occurred within the successful planning turn.

## Session 1: create four child beads

Sonnet created epic **ttt-cik** for the two-player milestone and four child
issues. The task-to-issue map preserves every original planning label:

| Original work, described by name | Recorded bead |
|---|---|
| Board-drawing tests; board and CLI message implementation | Render — ttt-cik.1 |
| Move-parser tests; move/menu parsing and the existing menu-caller refactor | Parse — ttt-cik.2 |
| Session helpers/tests; the two-player loop | Loop — ttt-cik.3 |
| Full-suite and two-player acceptance-evidence checks | Verify — ttt-cik.4 |

The [recorded map](../demos/lecture-beads/recorded-run/planning/beads-map.md)
and [creation transcript](../demos/lecture-beads/recorded-run/transcript.md#call-02)
show the actual records. These IDs belong to that database; they are not
identifiers to expect in a newly initialized reproduction.

The execution plan initially described nine internal steps. An internal step
need not become a separate issue. Related tests and implementation can form
one bounded outcome, while retaining their ordering obligations. The parsing
issue spans move parsing, menu parsing, and the existing menu-caller refactor,
so it remains unfinished at the intended pause. Its required II(c) and II(b)
commits are still distinct. Grouping does not erase that rule, the session-helper
requirements, or any other original obligation.

## Session 1: review and refine the beads

Prompts 01–04 all belonged to session 1. Prompt 01 planned and reviewed the
execution approach; prompt 02 created the actual epic and issues. Prompts
03 and 04 continued that same session using `--resume`. Creation and review
therefore implement steps 2 and 3 of the earlier Yegge workflow summary. They were two review requests to the same
agent that wrote the records. No implementation occurred during these calls.

[Prompt 03](../demos/lecture-beads/recorded-run/prompts/03-review-beads.txt)
asked Sonnet to inspect every full record against the execution plan,
original tasks, specifications, and contracts. It called for corrections to
omissions, duplication, ambiguity, missing evidence, and dependencies, with
concrete findings saved in planning/beads-review.md. Sonnet updated the
actual acceptance criteria and notes: it preserved the existing menu's
rejection of `01` and `+1`, clarified the separate parser/refactor commits
and passing-suite boundary, and recorded unresolved behavior questions.

[Prompt 04](../demos/lecture-beads/recorded-run/prompts/04-review-again.txt)
requested another pass for requirements lost during grouping, criteria that
conflict with contracts, and implicit prerequisites or verification duties.
It required useful corrections, an implementation-readiness report, and
unresolved developer decisions; it explicitly discouraged invented changes.
Sonnet added claim/progress/commit instructions to the epic and clarified
test-helper wiring and evidence details in the loop issue. It checked the
dependency graph and left its edges unchanged: Render and Parse remained
independently ready implementation work.

The slide abridges both prompts and summarizes observed changes from the
[written review](../demos/lecture-beads/recorded-run/planning/beads-review.md).
The later detailed review section gives concrete examples. Readiness was
the agent's reported result; several questions remained open. This record
shows what the two passes changed, and does not establish an optimal number
of reviews or the completeness of the result.

## The graph exposes independent work

![The captured work graph: Render and Parse both precede Loop, which precedes Verify.](../slides/diagrams/tictactoe-work.svg)

The arrows run from prerequisite to dependent. Loop needs both Render and
Parse; Verify needs Loop. The engine and contracts are already available,
so there is no prerequisite edge between Render and Parse. The epic groups
the milestone separately from these blocking relationships.

The diagram is drawn from the [captured issue relationships](../slides/examples/sonnet-run/dep-tree-after-creation.txt).
It is a presentation of real data, not a screenshot of a native CLI graph.
Both branches could be assigned separately when suitable workspaces and
coordination are in place. The recorded work proceeded sequentially.

These branches are independent CLI tasks, not different architectural
subsystems. Larger projects can use the same graph structure across subsystem
boundaries when the interfaces and prerequisites support that division.
Independent work can proceed separately; integration still needs evidence
that the required results exist and fit the contracts.

## The agent follows the project's tracking policy

The starter's CLAUDE.md and AGENTS.md tell the agent to read the constitution,
specifications, contracts, and original tasks. They select only the two-player milestone,
leave tasks.md unchanged as planning input, and make Beads authoritative for
live status, dependencies, evidence, discoveries, and handoffs. The later
computer-play and US3 menu features remain outside the selected milestone.

This is an explicit course adaptation. The original speckit-implement
instruction updates task checkboxes; the recorded workflow instead uses
Beads-directed prompts and the stated tracking policy. No automatic Spec
Kit-to-Beads synchronization is being claimed.

Sonnet wrote an [execution plan](../demos/lecture-beads/recorded-run/planning/beads-plan.md)
and [plan review](../demos/lecture-beads/recorded-run/planning/plan-review.md)
outside Beads, created the actual epic/issues, and reviewed/refined those
records twice in session 1. Partial implementation, recovery, rendering,
loop work, and final verification each started a fresh session, as shown in
the session map above. This is the recorded protocol, rather than a fixed
number of calls required for ordinary development. The agent normally performs the
reasoning, CLI operations, implementation, and updates. The developer sets
direction and judges genuine behavior changes and evidence.

## The agent files the epic and issues

**Beads assigned the epic ID `ttt-cik`.** The setup had selected the `ttt`
prefix with `bd init --prefix ttt`; `bd create` generated the suffix when
Sonnet filed the epic. Sonnet used the returned ID as the parent of its four
child issues.

The agent supplied the title, detailed description, and acceptance criteria.
The slide shortens the epic title by omitting its original task-label suffix;
the exact title remains in the linked transcript. The recorded command uses
`--body-file -` to read its description from standard input and `--silent` to
return the assigned ID. A heredoc supplied the long body. Child creation also recorded their
parent, labels, design references, and acceptance criteria.
([Actual command bodies](../demos/lecture-beads/recorded-run/transcript.md#call-02))

For comparison, the following is a short **generic syntax example**, not a
verbatim command or a new record from the captured run:

```sh
"$BD" create "Describe a bounded outcome" -t task -p 1 \
  --description "Work, governing references, and scope boundaries" \
  --acceptance "Observable conditions and required verification"
```

The agent must fill those fields with the actual task's information. In the
recorded run that included original task IDs, project-relative contract/spec
references, tests-first requirements, preservation obligations, evidence,
and boundaries. The tracker stores the result; the planning quality comes
from the agent's reasoning and subsequent review.
([Create reference](https://beads.gascity.com/cli-reference/create))

Sonnet used temporary /tmp ID files while creating the records, despite the
project-only instruction. The durable mapping is in Beads and
planning/beads-map.md. Fresh sessions recover IDs from
the tracker rather than relying on old shell variables or those temporary
files. The slide's epic command is explicitly an excerpt; its complete
standard-input body remains in the transcript.

## Review and refine the actual beads

The reviews inspected complete records against the original tasks, plan,
contracts, and existing code. They changed the beads' acceptance criteria
and notes. The table shows four concrete problems and the instructions
added to make the work verifiable.

First, the existing menu rejects `01` and `+1`, even though converting either
string with Python's `int()` would produce 1. A new menu parser could therefore
change which inputs the menu accepts. The review required tests that reject
both entries, so the later menu-caller refactor preserves the existing behavior.

Second, the parsing bead contains new parser implementation and a refactor
that makes the existing menu call the new parser. Those are distinct changes.
The review clarified that tests and the parser code they exercise are
committed together, with the initial failing-test evidence recorded in the
bead. The planned pause produced one partial move-parser commit and a later
menu-parser commit. The menu-caller refactor is a separate later commit,
with the full test suite passing before and after that refactor. The original
task notes label first implementation **II(c)** and behavior-preserving
refactoring **II(b)**. The slides retain those recorded change labels alongside
plain descriptions; they are project conventions, not Beads states.

Third, the rendering work includes prompts, error messages, and win/draw
messages, while its board-drawing unit tests check only the board. The review
made the game-loop tests responsible for checking the required messages.
That makes clear where their verification evidence will come from; a passing
board-drawing test alone does not verify the renderer's text output.

The rendering-only exercise changes that evidence boundary explicitly: it
requires unit tests of the prompt and rejection/result helpers so the rendering
bead can close while the loop remains planned work. Those tests establish helper
output, not correct loop integration or full-game conformance. The interim
rendering task defers the leave-game hint; the exercise preserves that scope.

Fourth, “keep existing files unchanged” requires a particular starting version
and a list of protected files. The review recorded the starting Git commit,
`f803ba7`, after the tracking setup, and identified the comparison paths.
The agent can then compare the governing specifications and existing menu/EOF
tests with that saved version during final verification.

The reviews also clarified session-helper wiring and the claim/progress/closure
protocol. These were changes to the work records before implementation.
([Written findings](../demos/lecture-beads/recorded-run/planning/beads-review.md))

These were observed changes to actual records. They do not establish that
two passes is optimal or that review automatically finds every problem.
The same agent wrote and reviewed the records, continuing its planning
conversation. Some corrections were appended beside superseded descriptions,
so implementing sessions needed to read the full issue. Questions also
survived both review passes; the later parser example illustrates why a
reviewed record still needs critical assessment.

## What happened to the behavior questions?

The slide previews the later implementation and final review before the
walkthrough returns to selecting and implementing ready work. The agent
recorded three interpretation questions during bead review. The final review
still listed all three as open while closing the milestone. No subsequent
developer ruling was recorded. The implementation nevertheless had concrete
behavior, which is distinct from establishing that every interpretation
question was settled.
([Review questions](../demos/lecture-beads/recorded-run/planning/beads-review.md),
[final disposition](../demos/lecture-beads/recorded-run/verification/milestone-review.md))

**Move syntax** (D2 in the archived review). The contract describes coordinates
as signed integers.
The reviewer asked whether that includes `+4 7` and non-ASCII digits. The
implemented regular expression accepts ASCII digits with an optional minus
sign, so it rejects both examples. The tests do not pin their intended
acceptance or rejection. This is the clearest remaining intent question:
the recorded choice and passing tests do not supply the missing decision.
The parser and milestone were closed with the question still listed.

**Output after a win or draw.** The reviewer flagged wording about a
transcript ending with the result line versus returning to the start menu.
For the selected interim milestone, the original implementation task already
requires the return to the start menu, and the test instructions already
say not to assert what happens after the result line. The archived code
prints the result and returns to the start-menu loop; tests avoid asserting
that the complete output ends with the result. The agent continued to list
the question as open, but that alone does not establish a specification
defect or a need for a new developer ruling.

**Board redraws.** The reviewer asked whether the winning move needs a
second drawing of the final board and whether rejected moves should redraw
the board. The archived code draws initially and after every accepted move.
The drawing after the winning move is the final board; there is no extra
drawing after result detection. Rejected moves produce a message and the
same player's prompt without another board drawing. Tests check ordering
and a minimum number of board drawings, and leave those exact redraw counts
open. The review recorded the behavior without a new developer ruling.

These observations come from the final app.py, parse.py, and game-loop tests
in the [milestone archive](../demos/lecture-beads/recorded-run/states/09-after-milestone.tar.gz).
They are agent-flagged questions rather than three proven defects. The later
parser example shows a proposed follow-up for the unresolved move-input
interpretation; that follow-up was not performed in the recorded run.

## Inspect prerequisites and ready work

The recorded graph can be inspected with the CLI, using IDs from that run:

```sh
"$BD" dep tree ttt-cik.4
```

The tree starts at Verify and follows its prerequisites. The slide shows
this abridged view, with titles and formatting shortened:

```text
ttt-cik.4  Verify [BLOCKED]
└── ttt-cik.3  Loop [blocks]
    ├── ttt-cik.2  Parse [blocks]
    │   └── ttt-cik  Milestone [parent-child]
    └── ttt-cik.1  Render [blocks]
```

Verify waits for Loop, and Loop waits for both Parse and Render. The
`[blocks]` labels identify those prerequisites. The `[parent-child]` row
records Parse's membership in the milestone epic. The tree includes that
grouping relationship alongside the blocking relationships.

`dep tree` prints a node reached through several paths only once. All four
children belong to the same epic; its position under Parse in this tree is
the first displayed path, rather than exclusive membership. The
[captured relationships](../slides/examples/sonnet-run/dep-tree-after-creation.txt)
preserve every parent-child link.

The [full tree output](../slides/examples/sonnet-run/dep-tree-after-creation.txt)
was captured by replaying this read-only command against a temporary
restoration of the creation archive. The original Sonnet creation call
queried the epic's tree; this verification-child query was added later for
the lecture. The saved output preserves the original titles and metadata,
with terminal styling removed.

Ready-work selection is a separate query:

```sh
"$BD" ready
```

The [captured ready query](../slides/examples/sonnet-run/ready-after-creation.json)
contains ttt-cik, ttt-cik.1, and ttt-cik.2. The first is the parent milestone,
while the latter two are the independently ready implementation children.
The epic groups the milestone; Render and Parse are the coding tasks to choose
from in this ready list. The next demo prompt explicitly directed Sonnet to
work on Parse and set its stopping point: implement and test move parsing, then end the session
with menu parsing and the menu-caller refactor unfinished. The task and pause
point were part of the demonstration setup. Sonnet followed those instructions;
a fresh session later completed the remaining work. Loop and Verify were
still blocked by their prerequisites.

All five records were priority 1 in this run. Their ready status follows
the graph, not a difference in priority. When reproducing from a new database,
use the IDs actually assigned there. Also distinguish selecting new ready
work from resuming an in-progress task: the latter is found through the
active-work query, not by expecting ready to return it.

The slide's ready list selects IDs and roles from actual JSON captured by
querying a restored archive. Its console excerpts abbreviate these query
results. The original agent stream and the archived database provide the
provenance for the issue state; the tree output was replayed later as
explained above.

## Session 2: interrupt useful unfinished work

The [first implementation prompt](../demos/lecture-beads/recorded-run/prompts/05-interrupted-implementation.txt)
asked Sonnet to read and claim the parsing bead, write move-parser tests,
record their intended failure, and implement only parse_move. It explicitly
required stopping before parse_menu, its tests, and the existing menu-caller
refactor. The agent had to save a partial commit and a concrete Beads handoff,
leaving the issue in progress.

The exact stopping point came from that implementation prompt. The bead
described the whole parsing task and included a general instruction to save
progress if interrupted. Its recorded work boundary did not independently
instruct the agent to stop after move parsing; the demo prompt supplied
that timing.

The agent wrote the tests first. Their initial run produced a collection
error because five_in_a_row.cli.parse did not exist. It recorded that result,
implemented parse_move, and then recorded 13 passing parser tests and 57
passing tests in the full suite. The partial II(c) commit was 701dc43.
([Implementation transcript](../demos/lecture-beads/recorded-run/transcript.md#call-05))

This is a planned interruption of the task. The process exited normally
after writing the handoff; there was no forced kill. A passing current suite
does not imply task completion when acceptance criteria include remaining
work. At this point the parser module had no parse_menu and the start-menu
caller was unchanged. Those facts were checked before recovery began.

## Session 2: the saved parsing handoff

The [actual issue view](../slides/examples/sonnet-run/parse-after-interruption.json)
preserves the full description, criteria, review notes, and handoff. Its
progress summary identifies move parsing as complete, 13 parser/57 full-suite
passes, partial commit 701dc43, and the remaining menu tests, menu parser,
and separate II(b) refactor. The next action is to add the menu-parser tests
while preserving the existing menu behavior.

The handoff also preserves boundaries: range checks stay in the engine,
the game loop belongs to another issue, and the parser interpretation
question D2 remains recorded. The issue's status is **in_progress**. The
slide abridges this real note into a table; it does not replace the actual
command results or pretend that every acceptance criterion is satisfied.

The [interrupted archive](../demos/lecture-beads/recorded-run/states/05-after-interruption.tar.gz)
preserves both the work record and the project at this moment, before the
fresh conversation. That timing matters: a handoff reconstructed after
resumption would not establish what the new session was given.

## Session 3: recover in a fresh session

The recorder starts Claude in the working project with the staged recovery
prompt and writes the output elsewhere. A portable invocation from the
bundled recorder directory is:

```sh
python3 run-session.py --project work \
  --prompt prompts/06-fresh-recovery.txt \
  --output recordings/recovery \
  --model claude-sonnet-5-5
```

Use this after the partial implementation or after restoring its checkpoint.
A pristine starter with no active issue is a different state. The displayed
paths are portable reproduction paths. The
[recorded recovery call](../demos/lecture-beads/recorded-run/transcript.md#call-06)
shows its executed prompt and session identity; private local metadata is omitted.

The [partial implementation call](../demos/lecture-beads/recorded-run/transcript.md#call-05)
and [recovery call](../demos/lecture-beads/recorded-run/transcript.md#call-06)
record distinct IDs for sessions 2 and 3. Recovery used neither `--resume`
nor `--continue`, automatic memory was disabled, and its prompt supplied no
previous transcript or selected issue ID. Project instructions, workflow
guidance, Beads, and working files were intentional durable context. A fresh
session still has its harness and project environment.

Here, work/ is the game project directory containing source, tests, Git
history, and .beads/. The --output value recordings/recovery is a filename
prefix relative to the bundled recorder directory. The recorder creates
recordings/ beside work/ and writes files such as recordings/recovery.jsonl,
recordings/recovery.md, recordings/recovery.prompt.txt,
recordings/recovery.metadata.json, and recordings/recovery.stderr.log there.
Thus “outside work/” describes the folder location of the recorded evidence.

Those files preserve the exact prompt, JSONL messages/tool events, stderr,
metadata, and a derived readable Markdown transcript for inspection. The
recorder does not reconstruct a transcript from the final answer. The fresh
agent is instructed to recover from the project instructions, Beads, and
working files without reading previous conversation logs. The reproduction
command writes new recordings. The published transcript combines the original
run's visible messages and tool activity; raw captures remain in the authoring
repository and are omitted from the student checkpoint archives.

## Session 3: what recovery actually did

The [recovery prompt](../demos/lecture-beads/recorded-run/prompts/06-fresh-recovery.txt)
asked the agent to find unfinished work, identify its contract, inspect the
working tree/evidence, and report its understanding and next action before
editing. The transcript shows it listing active work, reading ttt-cik.2,
inspecting the partial commit, and reading the parser, tests, app, and
relevant contract. Its first test edit added the remaining menu-parser tests.
([Full recovery transcript](../demos/lecture-beads/recorded-run/transcript.md#call-06))

The sequence supports saying that it found the right task and continued
the recorded remaining work. **It did not give the requested specific
recovered-understanding report before editing.** Its earlier assistant text
only said it would recover context. The [observation record](../slides/examples/sonnet-run/recovery-observations.md)
identifies the relevant raw events and marks that criterion unmet.

The agent also encountered a BSD sed error while adding an import. It noticed
the failed edit, corrected the import, and recorded the intended ImportError
before implementing parse_menu. The original failed attempt and corrected
red run remain in the stream. Successful continuation and perfect instruction
following are different claims; the captured result supports the former
with this explicit limitation.

For the exercise, ask the fresh session to read and report only in its first
turn, compare the Git-visible state and current revision before/after that turn,
and inspect its tool transcript for other writes. Then request continuation in
a further turn of that same new session. This makes recovery observable before
implementation. It is an improvement suggested by the miss, not a protocol
we claim the original recorded session already followed.

## Session 3: verify and close Parse

The agent finished parse_menu and its tests in II(c) commit 8cd08de. It then
made the existing caller refactor as separate II(b) commit 8a56f89, stating
that no specified behavior changed. The full suite passed before that
refactor commit and after the change. The existing start-menu and EOF tests
were unchanged.

The recorded results were **28 parser/menu tests** and **72 full-suite tests**,
all passing. Immediately before closure, the agent used
`bd update ttt-cik.2 --append-notes` to save a completion/evidence summary.
It described the menu-parser implementation and menu-caller refactor,
recorded the initial failing test and later passing commands/results,
listed implementation and refactor commits, and confirmed that the existing
menu/EOF tests were unchanged. It also repeated the unresolved question
about accepted signs and digits. Appending the summary retained the earlier
review notes and interrupted-session handoff in the same issue.

The agent then ran `bd close ttt-cik.2 --reason` with a shorter summary of
acceptance and evidence. The saved issue therefore contains the detailed
completion notes and a separate close_reason, alongside its closed status.
The [issue view after recovery](../slides/examples/sonnet-run/parse-after-recovery.json)
preserves those updates; the [recovery transcript](../demos/lecture-beads/recorded-run/transcript.md#call-06)
shows the update followed by the close command. This information was stored
in Beads as well as being reported in the agent's final chat response.

The raw note calls this “SESSION 2 EVIDENCE,” counting the two implementation
sessions. It is session 3 in the complete run map above, which also counts
the earlier planning session.

The loop still needed Renderer. Satisfying one prerequisite did not satisfy
the other, so the next implementation child was Render. The
[recovered checkpoint](../demos/lecture-beads/recorded-run/states/06-after-recovery.tar.gz)
lets students inspect this state separately from the earlier interruption.

The passing tests establish the cases checked. They do not settle every
interpretation of the governing input rule. The agent kept D2 in the record
while closing the parsing issue; the next sections assess that limitation.

## Recorded progress through the milestone

Work proceeded sequentially across Sonnet sessions. Session 1 planned and
reviewed the work without implementing game changes. Sessions 2–6 implemented
or verified their assigned work and updated Beads. Rendering, the loop, and
final verification were completed in that order. The actual full-suite
progression was:

| Session | Checkpoint | Tests passing | Next child work |
|---|---|---:|---|
| 1 | Planning/reviews complete; starter unchanged | 44 | Render or Parse |
| 2 | Partial parser | 57 | Resume Parse; Render independent |
| 3 | Parser complete | 72 | Render |
| 4 | Renderer complete | 73 | Loop |
| 5 | Loop complete | 83 | Verify |
| 6 | Milestone verification complete | 83 | Epic and four children closed |

An in-progress issue is resumed from the active-work query. The ready list
still contained the epic at intermediate states; the table names executable
child work rather than treating the parent as another coding task.
([Captured progression](../demos/lecture-beads/recorded-run/transcript.md#checkpoint-states))

The loop agent's final narrative said 72 tests before its issue. The preceding
rendering checkpoint actually had 73. We use the captured suite results in
the table. This is an example of checking a progress summary against the
evidence instead of treating the agent's final prose as authoritative.

The independent final check recorded **83 passing tests**, all seven US1
scenario rows passing, and no unknown requirement IDs. Protected specifications,
task artifacts, and existing menu/EOF/architecture tests were unchanged;
seven realization/test files changed. Computer play and later US3 features
were outside this milestone. The result is finite verification evidence,
including the parser limitation discussed below.
([Final output](../slides/examples/sonnet-run/final-tests.txt),
[conformance report](../slides/examples/sonnet-run/final-conformance.md))

## An unresolved question survives closure

The recorded signed-integer question concerns which signs and digits the
move-input rule allows. The archived review calls it **D2**; that is a review
label, not a Beads issue ID.
The implementation accepts an optional minus and ASCII digits. It rejects
`+4 7` and non-ASCII digits. The tests do not resolve the full intended
interpretation. The model recorded this as an open question while closing
the parsing issue and milestone.
([Preserved final review](../demos/lecture-beads/recorded-run/verification/milestone-review.md))

The tracking problem is observable even without deciding the intended format
here: a closed status does not establish that the question was answered.
Read the governing contract, determine whether it needs a developer ruling,
and obtain the decision and affected evidence before claiming that part of
the behavior fully resolved. An agent should distinguish a genuine intent
gap from a choice the specification deliberately leaves open.

For example, the following **proposed follow-up was not executed in the
recorded run**:

```sh
"$BD" create "Clarify accepted signs in move input" -t task \
  --description "Resolve accepted signs and digits against the move-input contract." \
  --deps "discovered-from:ttt-cik.2"
```

The discovery relationship records origin. If the decision is a prerequisite
of another item's completion, record the appropriate blocking relationship
as well. Keep proposed improvements separate from what the original run
actually did; do not retrospectively edit the archive to manufacture a
cleaner process.

Other model-reported questions concern result/menu ordering and redraw
details. The original session-test task already says not to assert what
happens after the result line. A review question is not automatically a
proven specification defect. The required rejection of `4;7` has explicit
test coverage; the signs/digits question was left open.

## What did this run demonstrate?

The fresh session retrieved the active issue and its governing files, inspected
the partial state, and began the recorded remaining menu work. The dependency
graph changed which child was ready as prerequisites closed. The agent
closed the selected milestone after its checked cases passed. These are
observations about the recorded workflow and can be assessed from the
transcripts, code, issue records, and test output.

The reporting instruction was missed, an implementation interpretation remained
unresolved through closure, and some execution attempts needed repair. The
loop session repaired its transcript-test helper after four failures; its
statement that no assertions were weakened is an agent claim to inspect,
separate from the final passing suite. The source stream preserves the
attempts, whereas final commits alone bundle tests and code.

The graph's queryable records, ownership, dependencies, and bounded task
contexts explain the architectural motivation for a growing project. The
small demonstration does not measure large-backlog throughput, parallel or
distributed execution, an optimal review-pass count, or comparative tool
effectiveness. Those limits do not erase the directly observed mechanisms.
([Independent checks](../demos/lecture-beads/recorded-run/verification/independent-check/summary.json))

## From sequential work to parallel subsystem work

One coordinator agent can orchestrate several worker agents assigned to
independent parts of a system. The coordinator delegates bounded work,
tracks progress, and arranges integration. Clear subsystem interfaces and
dependencies make that division possible. Beads records ready work,
ownership, and prerequisites; the coordinator supplies the orchestration.
The tracking graph itself does not launch workers or remove code coupling.
([Coordination patterns](https://beads.gascity.com/multi-agent/coordination))

Give workers separate code working copies/worktrees and branches, compatible
Beads versions, and configured access to shared or synchronized issue records.
Concurrent updates need a configuration that supports them. The workflow is
to select independent ready tasks, agree or claim ownership, implement and
verify, integrate when prerequisites are satisfied, then update and synchronize
the records. Ownership against one shared authority does not automatically
become a global reservation across disconnected replicas.
([Worktrees](https://beads.gascity.com/reference/worktrees),
[synchronization setup](https://beads.gascity.com/getting-started/sync-setup))

Code changes and issue state have separate synchronization procedures. Each
worker needs the relevant project and tracking state before starting. Follow
the pinned runtime's setup instructions for the chosen environment. This
lecture summarizes that extension; the recorded run and exercise remain
sequential and require no distributed infrastructure lab.

## Exercise: render and resume

**Due: November 8, 2026.**

The [exercise-beads starter folder](../demos/lecture-beads/exercise-beads/README.md)
contains a separate render-and-resume exercise. It starts from the same
unfinished course game with 44 passing baseline tests, an engine and menu
shell, and the existing specifications, contracts, and original plan/tasks.
Its setup creates a fresh Git repository and empty Beads workspace. The
student writes their own prompts; the lecture's recorded parsing prompts
remain separate reproduction materials.

Use two agent sessions, with work proceeding sequentially. A session can
contain multiple turns: the first includes planning outside Beads, graph
creation, review/refinement, and partial implementation. The graph should
show how rendering and parsing can proceed independently and what the loop
must wait for. Preserve original task references, contract paths, acceptance
criteria, and evidence requirements. Keep board drawing and the renderer's
message helpers in one bounded rendering bead.

In session 1, write board-drawing tests first, record their intended failure,
implement board drawing, and verify the result. Stop before the move-prompt,
rejection, and result helpers or their tests. Save a partial commit and append
a concrete handoff with completed work, commands/results, remaining criteria,
files/commits, boundaries, and the next action. The bead remains in_progress.
Save the interrupted project state before starting recovery.

Start session 2 with fresh history and no previous transcript. Its first turn
must read and report only: the active issue, governing references, completed
work and evidence, remaining criteria, unresolved questions, and next action.
The student checks that report against the saved checkpoint before requesting
edits. The handout captures Git status, including the current revision, and
a diff against HEAD before and after this report-only turn. Compare the
captures before continuing, and inspect the tool transcript for writes to
ignored Beads data or other files that Git does not show. These are observation
checks; the recorder still grants editing tools. Record any missed instruction
or incorrect recovery claim in the reflection. The student should not supply
the old issue ID or a recap of completed/remaining work in the recovery prompt.

In a subsequent turn of session 2, finish the message helpers and their tests.
This exercise explicitly requires focused unit tests of the existing prompt,
error, and win/draw behavior, so the rendering work can be verified without
implementing the game loop. Preserve the original interim scope: the later
leave-game command and hint remain deferred. Record the expected failing
tests before implementation and retain actual verification output. Before
closing, append a completion/evidence summary and supply a close reason.
Preserve genuine unresolved decisions and label proposed future work.

The required coding scope is rendering only. Parsing, the menu-caller
refactor, and the loop remain planned work, and the milestone is not complete.
This exercise has its own two-session protocol; the six-session map above
describes the separate recorded lecture demonstration.
Explain how the graph could support independent workers while executing this
exercise sequentially. The supplied recorder examples use five CLI calls
across two sessions; additional review turns are allowed. Resuming session 2
for its implementation turn continues the fresh session, rather than the old
session 1 history.

The recorder flags were checked against **Claude Code 2.1.310**, also used in
the recorded lecture. The recorder saves the installed CLI version and disables
skills/commands with `--disable-slash-commands`. Its default per-call budget flag
is 8 USD; adequacy for this new exercise has not been measured. A budget cutoff
is not a completed handoff. Inspect the saved result and continue the appropriate
session with a new output prefix until the required commit and Beads handoff
exist before taking the paused checkpoint.

The [exercise DownGit link](https://downgit.github.io/#/home?url=https://github.com/santoslab/agentic-software-engineering-public/tree/main/module-software-engineering/demos/lecture-beads/exercise-beads)
targets only exercise-beads/ in the lecture-beads demo folder. The exercise folder is self-contained, with the
handout, pristine starter, setup script, recorder, provenance, and checksums.

## Exercise: evidence to keep

The [handout](../demos/lecture-beads/exercise-beads/README.md#save-checkpoints-and-submit-evidence)
gives commands for before-recovery and after-rendering checkpoints and issue
exports. Save the full stopped project, including source/tests, local Git
history, and Beads state. An export makes issues easy to inspect but does not
replace the project and its tracking history. The before-recovery state must
be saved before session 2 starts.

Keep the student-authored prompts and recordings for both sessions, including
the first fresh recovery report, before/after Git comparisons, and later
continuation. Transcripts stay outside work/ and are retained for inspection
rather than supplied as recovery input. Include board/message test evidence, full-suite results, commit/report
references, final completion notes and close reason, and unresolved questions
or proposed follow-ups. Other planned work should remain open.

Write a short reflection on what the fresh session recovered or missed and
how its claims compared with the saved project. Explain independent tasks and
integration prerequisites. Assess the graph, recovery, and verified behavior
using the evidence; a closed status alone does not establish completion.
Review submitted recordings and files for credentials. Submit by
**November 8, 2026**, using the course's announced submission location.

## Questions to think about

What information did the work graph make retrievable that code and Git
history alone did not explain? Which tasks could agents work on separately,
and where must their results be integrated? How would you organize a much
larger backlog around subsystems while retaining dependencies across their
boundaries?

Finally, what follows when a bead is closed but a required behavior question
or its evidence remains unresolved? Use the recorded D2 question and the
missed report before editing to distinguish successful continuation from
complete compliance with the intended workflow. The developer still assesses
intent and evidence, while agents perform and maintain the detailed work.

## Command and source references

The deck's command reference on slide 46 collects the common operations:
prime, create, list, ready, show, claim, append progress, add dependencies,
and close with evidence. With the repo-local installation, either put its
bin directory on PATH or use the saved BD executable path. Set the environment
for each terminal and agent session. Generic examples and proposed commands
in these notes are labeled separately from the captured run.

The final reference slides link the pinned Beads release, issue/CLI and
coordination documentation, Yegge's article, the original course checkpoint,
and tracker alternatives. The [recorded run index](../demos/lecture-beads/recorded-run/README.md)
provides the primary evidence for the lecture's actual agent outcomes; its
[restore guide](../demos/lecture-beads/recorded-run/RESTORE.md) explains the state archives.
Use the pristine starter for a new run and the interrupted checkpoint to
inspect or repeat that specific handoff. Both preserve a concrete starting
point without requiring students to reconstruct the state from slide prose.

## Original plan task labels for reference

The lecture uses descriptive names for the work. These original Spec Kit
labels are lookup references when inspecting the archived plan and Beads
records; students are not expected to remember the numbers.

| Original label | Work it identifies |
|---|---|
| T018 | Write board-rendering tests |
| T019 | Write move-parser tests |
| T020 | Write session helpers and two-player interaction tests |
| T021 | Implement board rendering and CLI message text |
| T022 | Implement move/menu parsing; refactor the existing menu caller |
| T023 | Implement the two-player loop |
| T024 | Run the full suite and inspect two-player acceptance evidence |

The source [task list](https://github.com/santoslab/agentic-software-engineering-public/blob/4d6a2cd/module-software-engineering/demos/lecture-speckit-intro-tic-tac-toe/specs/001-five-in-a-row/tasks.md)
and [recorded mapping](../demos/lecture-beads/recorded-run/planning/beads-map.md)
preserve the formal correspondence. Beads issue IDs are separate identifiers
used to query particular records; read their titles and descriptions for
meaning, and look up the IDs when issuing commands.
