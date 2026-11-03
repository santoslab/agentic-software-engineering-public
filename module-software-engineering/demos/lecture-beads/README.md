# Beads lecture project

This folder installs the lecture's pinned Beads **1.3.2** CLI locally. It is
separate from the game project whose work you will track. You need Node.js,
npm, and Git.

From this extracted folder:

```sh
npm ci
export PATH="$PWD/node_modules/.bin:$PATH"
export BD="$PWD/node_modules/.bin/bd"
"$BD" version
```

Here, npm installs the Beads CLI. This project's `package.json` lists
`@beads/bd` **1.3.2**, and `npm ci` installs the versions recorded in
`package-lock.json`, exposing `node_modules/.bin/bd`. CI means continuous
integration; we use its clean-install command locally for reproducible tool
setup. Adding the local executable to `PATH` also lets generated agent hooks
invoke `bd` by name.

Next, enter your separate disposable tic-tac-toe working copy:

```sh
cd /path/to/tictactoe-work
"$BD" init --prefix ttt
```

Initialize the game copy. This installer folder does not need its own Beads
workspace. Set `PATH` and `BD` in every terminal used for the lecture; start
your coding agent from that configured terminal.

`bd init` sets up the project. At session start or after compaction, `bd prime`
prints Beads workflow guidance for the agent to read. Project-specific policy
stays in the instruction file the harness reads, alongside the generated
instructions to run `bd prime`.

Beads 1.3.2 creates or updates `AGENTS.md` and `CLAUDE.md` and installs project
integrations. Inspect the generated instructions and hooks, retain the
project's existing policies, and add the lecture's task-tracking policy to
the instruction file your harness reads. `bd init` can also create a Git
commit for the setup files; inspect its output and the resulting commit.

The walkthrough uses the familiar Spec Kit five-in-a-row tic-tac-toe example.
The lecture slides and course notes are distributed separately from this
project folder.

## Student exercise: render and resume

The self-contained [exercise-beads starter folder](exercise-beads/README.md)
contains the unfinished 44-test game, setup script, recorder, and handout.
Follow its README from inside that folder. Students write their own prompts,
pause after board rendering, and finish the message helpers in a fresh session.

The [exercise-only DownGit link](https://downgit.github.io/#/home?url=https://github.com/santoslab/agentic-software-engineering-public/tree/main/module-software-engineering/demos/lecture-beads/exercise-beads)
downloads only that starter folder.

## Reproduce the Sonnet demonstration

The [starter archive](tictactoe-beads-sonnet-starter.tar.gz) includes the unfinished
tic-tac-toe project, exact staged Sonnet prompts, setup script, and transcript
recorder. Its [SHA256 file](tictactoe-beads-sonnet-starter.tar.gz.sha256) identifies
the archived input. Extract it into a separate folder and follow its README.

The prompts have Sonnet review the plan, create and refine the beads, then
perform a deliberately interrupted task and recover in a fresh session.
The archive contains inputs; it does not contain completed agent-run results.
Claude Code with Sonnet access, uv/Python, Node.js/npm, and Git are required.

The starter's archive ownership metadata is normalized for publication.
Its source files, prompts, and file modes match the original reproduction
input; the accompanying SHA256 file identifies this distributed copy.

## Read the recorded demonstration

The [consolidated transcript](recorded-run/transcript.md) shows all nine calls
across six sessions in one GitHub-readable Markdown file, with executed
prompts, visible responses, and tool activity. The
[recorded-run folder](recorded-run/README.md) also includes sanitized,
restorable checkpoints and selected verification evidence. Raw CLI recordings
and private authentication diagnostics are excluded from the download.

## Task Master assessment

The [local-storage assessment](assessment/task-master-assessment.md) and its
[reproducer](assessment/task-master-evaluate.py) support the lecture's
comparison. They use synthetic tasks and make no model calls.

Instructional prose follows [CC BY 4.0](LICENSE-CC-BY-4.0); configuration
follows [MIT](LICENSE-MIT). The installed Beads package retains its own license.
