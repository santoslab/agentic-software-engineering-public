# Repository Organization

## Motivation

A specific repository organization for your project is not mandated,
but it will be helpful for several reasons if every team aims to
follow the structure given in this file.

- This will enable us to use the same vocabulary across projects to
  refer to the location of specifications, documentation,
  background/reference material, process guidelines, etc.
- It will facilitate potential sharing of agent skills and development
  process guidelines across projects.
- It will facilitate agent-based review and evaluation of your
  projects.


## Canonical Example

The structure that we suggest is illustrated in the development of the
[message guard
example](../module-ase-principles/demos/running-example-message-guard/)
used in our lectures (the Python sibling of the HAMR Simple Network
Guard). Version
[A0](../module-ase-principles/demos/running-example-message-guard/a0/)
is the smallest instance of the structure; version
[A1](../module-ase-principles/demos/running-example-message-guard/a1/)
is the fullest so far, and is the one the folder list below follows.
Each version's README has a table, "The artifacts, by category", that
says what every file in that version is for; read it alongside this
note.

The example keeps its versions as side-by-side snapshot directories
(`a0/`, `a1/`) so that a lecture can point at one and you can compare
two with `diff -r`. Your project is one repository tree. Its versions
are commits and tags (one tag per project milestone, for example), not
copies of the tree.


## Folder Structure

```
your-project/
├── README.md          the map: what the system is, the role of every folder, how to run it
├── CLAUDE.md          what an agent reads first, and the roles it plays here
├── pyproject.toml     technology configuration: dependencies, tool settings
├── uv.lock              (your stack's equivalents), with the lock file committed
├── .gitignore
├── specs/             specifications: what the system must do
├── guard/             the realization: the product code (name it for your system)
├── tests/             the suite; each test cites the clauses it is evidence for
│   └── tooling/       tests of the assurance tools themselves
├── tools/             programs that evaluate the project or help a person work with it
├── tooling/           the tool catalog: one page per tool, how it was specified and checked
├── process/           judgments, procedures, and templates: how claims are defined and evaluated
├── records/           what people, and agents, decided and did
├── reports/           the development state, readable without reading the code
├── reference/         material that informs the specifications but is not one
└── .claude/skills/    the project's skills, each packaging a procedure
```

Two folders arrive in later versions of the example or are not in it
at all, and most projects will want them: `plans/` (from A2) and
`docs/` with `examples/` (not in the guard). Both are described at the
end of this section.

### `README.md` and `CLAUDE.md`

**`README.md`** is the map of the repository. The guard's README says
what the system is, lists the artifacts by category (one row per
folder, with its files and their role), lists the judgments and what
evaluates each, gives the commands that run everything, and says which
files are generated and which are written by hand.

- Keep a category table like the guard's, and update it in the same
  change that adds a folder. It is what an instructor, a reviewer, or
  an agent reads to find things.
- The commands under "Running it" should work from a fresh clone:
  install, run every evaluation, run the system on one example. A
  reader who cannot run your project from the README alone cannot
  evaluate it.

**`CLAUDE.md`** is the agent instruction file. The guard's is under
fifty lines: which files to read first, and three roles. As *author*,
everything the agent writes is held to the judgment clauses, and it
reads the clause that applies before writing. As *assessor, when
asked*, it compiles the assurance report by the written procedure and
reports only results it obtained in that session. It is *not a decider
of human judgments*: it does not sign off, rule on an audit gap, or
write a record for an activity that did not happen.

- Point to the process files instead of restating them. An instruction
  file that repeats the judgments drifts away from them.
- Say what the agent must not change without being asked. In the
  guard, that is the specifications, the records, the elicitation
  record, and the scenarios.
- If your team also uses an agent that reads a different instruction
  file (`AGENTS.md`), keep one file as the source and have the other
  point to it.

### Technology files at the root

In the guard: `pyproject.toml` (the Python version, the dependencies,
the pytest marker and coverage settings, the ruff settings), `uv.lock`,
and `.gitignore` (the virtual environment, the caches, `.coverage`).

- Use your stack's standard files in their standard places
  (`package.json` with its lock file, `build.gradle`,
  `docker-compose.yml`, and so on), and commit the lock files, so that
  a reviewer's run uses the versions yours did.
- Keep evaluation thresholds in configuration rather than in someone's
  memory. The guard's `--cov-fail-under=100` and `--strict-markers` are
  in `pyproject.toml`.
- The written description of the stack (each choice, its version, why
  it was chosen, its license, how it is installed) is
  `specs/technology.md`, as `brainstorming.md` suggests. The
  configuration files are its realization.

### `specs/`: specifications

What the system must do, written so that it can be built from and
checked against. In the guard (A1):

- `conops.md`: the concept of operations (the agreed purpose; scope,
  with assumptions; user categories; user stories US-1 to US-3, each
  with an example; deferred wants D-1 to D-3);
- `glossary.md`: every domain term, defined once;
- `requirements.md`: REQ-0 to REQ-3, in EARS form;
- `scenarios.json`: SC-1 to SC-6, the stories' examples as data that
  any realization must reproduce.

Guidance:

- One file per form of specification. The forms the guard has not
  reached yet (architecture, data format, interface contracts, in A2)
  go here too, as `specs/architecture.md` and so on.
  [`specification-kinds.md`](../specification-kinds.md) catalogs the
  forms.
- Every clause that is to be verified carries an identifier and a
  verification method, in a header line a program can parse:

  ```
  **REQ-1** · Method: test · Pattern: event-driven · Derived from: US-3
  ```

  Use one identifier prefix per form (`US-`, `REQ-`, `SC-`; later
  `ARCH-`, `DATA-`, `IF-`), and do not reuse an identifier once it is
  retired.
- Declare the links between specifications as fields (`Derived from`,
  `Scenarios`, `Source`), so that a trace tool can resolve them in both
  directions.
- Examples that the stakeholders gave are specifications, not test
  data. Never edit `scenarios.json` (or its equivalent) to make a test
  pass; a scenario that looks wrong is a gap for the audit.
- Only what has been agreed belongs here. Drafts, brainstorming notes,
  and transcripts go to `reference/`. Wants not chosen for this version
  go to `reference/` too, or to a deferred-wants section of the concept
  of operations, as in the guard.

### `guard/`: the realization

The product code. In the guard, one Python package: `message.py` (the
message type) and `filter.py` (the one stage).

- Name the folder for your system, and follow the layout your language
  expects (`src/<package>/`, a Maven tree, and so on). A project with
  several components (a backend, a frontend, a database schema) uses
  one folder per component; the architecture specification names the
  components and the folder that realizes each.
- Only product code goes here. The programs that evaluate the product
  are in `tools/`, and generated reports are in `reports/`.

### `tests/`: the suite

The tests, and the executable evidence for every clause whose method
is *test*. In the guard (A1):

- `test_filter.py`, `test_message.py`: unit tests. A test that is
  evidence for a clause cites it with a marker,
  `@pytest.mark.req("REQ-1")`.
- `test_scenarios.py`: the scenario loader, which runs every scenario
  in `specs/scenarios.json` as a test that cites its story.
- `conformance.py` (the clause reader) and `conftest.py` (a pytest
  plugin): together they turn citations and outcomes into requirements
  coverage, write `reports/conformance.md`, and fail the run when a
  clause has no passing evidence.
- `tooling/`: tests of the assurance tools, with `cases/` holding one
  directory per kind of finding a tool must report.

Guidance:

- Cite clauses from tests in a form a program can read (a marker, an
  annotation, a naming convention), and register it strictly, so that
  a misspelled citation is an error rather than a silent miss. In a
  project with several languages, choose a citation form for each test
  framework and feed all of them into one conformance report.
- Keep the tests of your tools apart from the tests of your product.
  Every kind of finding a tool can report needs a case on which it must
  report it; a tool nobody has seen fail is not yet trusted.

### `tools/`: programs that evaluate the project

Programs that evaluate the project or help a person work with it. None
of them is part of the product. In the guard (A1):

- `evaluate.sh`: every mechanical evaluation in one command (ruff;
  pytest with coverage and the plugin; the trace tool). It prints a
  header saying what it checked and exits non-zero at the first
  failure.
- `trace.py`: resolves every declared link in both directions and
  writes `reports/trace-matrix.md`.
- `walk.py`: a walkthrough helper. A person gives it one message and
  sees what the guard does with it.

Guidance:

- Write the evaluation command on the first day, and extend it as the
  project grows. One command with one exit code is what you, your
  agent, and an instructor all run.
- Add a tool the second time you do a check by hand.
- Give each new tool a page in `tooling/` and its failure cases in
  `tests/tooling/`.
- In A0 and A1 nothing runs these programs unasked. Running
  `evaluate.sh` from a pre-commit hook is the control layer, which the
  example adds in A2.

### `tooling/`: the tool catalog

Prose about the assurance tools, wherever their code lives (`tools/`,
`tests/`, `.claude/skills/`). In the guard (A1), `tooling/README.md`
has one row per tool (its kind, its goal, the clause or procedure it
serves, what it reads and writes), and each tool has a page under the
same seven headings: goal; requirements; the prompt; review points;
deliberate-failure checks; adapting it to your project; making it
shared infrastructure.

- Do not confuse the two folders: `tools/` holds programs, `tooling/`
  holds the pages that say how each was specified, prompted for,
  reviewed, and checked.
- Write a tool's page when you build the tool, while the prompt and
  the reviewed design are at hand. The sidebar [*Tooling as
  engineering*](../module-ase-principles/lecture-notes/sidebar-tooling-as-engineering.md)
  gives the reasons.

### `process/`: judgments, procedures, templates

How claims about the project are defined and evaluated. In the guard
(A1):

- `judgments.md`: the five judgments (SQ, specification quality; RQ,
  realization quality; CONF, conformance; VAL, validated; TR,
  traceable) and the clauses that make them up, filed by the form of
  specification each is about. Every clause has four fields: *Holds
  when*, *Evaluated by*, *Evidence*, and *In this project*. The file
  ends with the steps for compiling the assurance report.
- `procedures.md`: the activities that have fixed steps and a stated
  stop: Audit and Elicit.
- `templates/`: the forms of the report and of the records
  (`assurance-report.md`, `gap-list.md`).

Guidance:

- Start from the guard's judgments file. A clause's first three fields
  depend only on the form and can be kept; rewrite *In this project*
  for your files and commands.
- When you add a form of specification, add its clauses here in the
  same change.
- Add a template when the same record or report is written more than
  once, so that the agent fills a form instead of inventing one each
  time.
- Process rules, which say when a claim must hold (a gate before a
  commit, a stale result), arrive in A2 as `process/rules.md`. Write a
  rule for a practice you already follow, not ahead of it.

### `records/`: what was decided and done

The evidence of what people, and agents, decided and did. The rows of
the assurance report that a person establishes rest on these files. In
the guard (A1):

- `dev-log.md`: append-only, one entry per task, naming the files
  touched, the judgments touched, the evaluations run, and, for a task
  that ended in a commit, the commit;
- `reviews.md`: one entry per review, a person reading an artifact
  against a judgment clause, with who read, when, against which state,
  and what they found;
- `audit-NN-*.md`: one file per audit of the specifications, each a
  gap list with a person's ruling on every gap;
- `validation.md`: the walkthroughs of the stories by a stakeholder of
  each user category, and the sign-offs (A0's version of this file is
  `walkthrough.md`).

Guidance:

- A record says who decided, in which role, when, against which state
  of the repository (a commit), and what they decided. Without the
  state, a reader cannot tell whether the record still applies.
- Append; do not rewrite. A new audit is a new numbered file, and a
  correction is a new dev-log entry.
- An agent may draft a record (the guard's agent-run audits are agent
  drafts), but a ruling or a sign-off is a person's, and no record is
  written for an activity that did not happen.

### `reports/`: the development state

The state of the project, readable without reading the code. In the
guard (A1):

- `assurance-report.md`: one row per clause, saying whether it holds,
  its evidence, and the provenance of that evidence. The agent
  compiles it on request, from evaluations it runs then and records it
  reads.
- `conformance.md`: generated by every test run; each clause, the tests
  that cite it, and its status.
- `trace-matrix.md`: generated by `tools/trace.py`.

Guidance:

- Commit the reports, generated ones included, so that the report for
  a commit is in that commit's tree. In the guard's replayed history,
  `git show a1-specs:reports/assurance-report.md` shows the report as
  it stood at that commit.
- Never edit a generated report by hand: change the input or the tool,
  and run it again. The assurance report is recompiled, not patched.
- Say in the README which reports are generated, which are compiled by
  the agent, and which files are written by hand. The guard's A1
  README has that table.
- From A2, `reports/ledger.md` keeps the report between requests: it
  is generated from exit codes and records, with stale rows marked.

### `reference/`: what informs the specifications

Material that informs the specifications but is not one. Nothing in it
is audited, and no judgment is about it. In the guard (A1):

- `elicitation.md`: the questions put to the stakeholders and their
  answers, in their words; the stories cite these as their `Source`;
- `drafts/`: the specifications as they stood before the audit, kept
  so the audit can be replayed;
- `prompts/`: the prompts that produced artifacts;
- `history/`: the patches that replay the build.

Guidance:

- In your project, this is where the brainstorming goes: transcripts
  of conversations with agents, technology comparisons, decision notes,
  deferred features, notes on an existing codebase, and external
  standards or papers you are allowed to redistribute.
- Keep the prompts that produced important artifacts, with the date
  and the agent that ran them.
- When something here becomes binding, move it into `specs/` and give
  it identifiers. A specification may cite a reference file, as a
  story's `Source` does, but citing it does not make it a
  specification.

### `.claude/`: skills and agent configuration

The project's Claude Code configuration. In the guard (A1),
`.claude/skills/elicit/` and `.claude/skills/audit-spec/`: each is a
`SKILL.md` with its supporting files (per-form `forms/`, a checklist, a
record template), and each packages a procedure of
`process/procedures.md`. Both are started by the developer only:
`disable-model-invocation: true` in `SKILL.md`, with
`agents/openai.yaml` as the equivalent setting for Codex.

- The procedure in `process/procedures.md` is the definition; the
  skill is its packaging. Change the procedure first.
- Give a skill a version (the guard's audit skill is at 1.2), and rerun
  it on its known-violation set after every change. The guard's set is
  `reference/drafts/`, which carries seven seeded gaps.
- Commit `.claude/` (skills, the project `settings.json`); personal
  settings belong in `settings.local.json`, which is not committed. The
  course's [`.claude-template/`](../.claude-template/) is a minimal
  starting point.
- In A2 the guard adds a hook here, the pre-commit run of
  `tools/evaluate.sh`.

### Later in the example: `plans/`

Not in A0 or A1. From A2 the guard has `plans/NNN-*.md`, build plans:
tasks grouped into waves, a gate at the end of each wave, and each task
citing the clauses it realizes. A verification plan,
`plans/verification-plan.md`, comes later still.

- The development plan from your proposal belongs here, one file per
  phase. Have each task cite the clauses (`US-n`, `REQ-n`) it realizes,
  so that a reader can tell which part of the plan a commit belongs to.

### Not in the example: `docs/` and `examples/`

The guard is a library with one function, and its README is its
documentation. Your project's deliverables include documentation and
examples that the instructors and our agents can run, so most projects
will add two folders.

- **`docs/`**: documentation that describes. User and developer
  guides, how to run the system, design notes, and for a brownfield
  project the `docs/orientation.md` and `docs/running.md` of the
  brainstorming prompts. Documents describe; specifications prescribe.
  A description of an existing architecture in `docs/architecture.md`
  becomes `specs/architecture.md` once its claims carry identifiers and
  methods and are evaluated.
- **`examples/`**: runnable example inputs, each with the command that
  runs it and the output to expect, listed in `examples/README.md`.
  Examples that the stakeholders gave as part of a story are
  scenarios, and belong in `specs/`; the examples here demonstrate the
  system, and a test that runs each one keeps them working.


## Growing into the Structure

You do not need every folder on the first day; the guard did not have
them either. A0 started with the README, `CLAUDE.md`, the technology
files, `specs/` (the concept of operations and the requirements), the
realization, `tests/`, `tools/evaluate.sh`, `process/judgments.md` with
the report template, `records/`, and `reports/`. A1 added `reference/`,
the glossary and the scenarios, the procedures and their skills, the
trace tool, and `tooling/`. A2 adds `plans/`, the rules, the ledger,
and the hook.

A reasonable order for your project, against the
[timeline](general-guidance-timeline.md):

1. **Proposal and initial presentation.** `README.md`, `CLAUDE.md`,
   `specs/conops.md`, `specs/technology.md`, `reference/` with the
   brainstorming transcripts and decisions, and `plans/` with the
   development plan.
2. **First part of the system running.** The realization, `tests/` with
   clause citations, `tools/evaluate.sh`, a generated
   `reports/conformance.md`, and `records/dev-log.md`.
3. **Final submission.** The remaining forms of specification you
   chose, `process/judgments.md` adapted to them, the records of your
   reviews, audits, and validation, an assurance report, a catalog page
   for each tool you built, and `docs/` and `examples/`.
