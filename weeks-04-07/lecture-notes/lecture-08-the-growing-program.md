# Lecture 08 — The Growing Program: Elicitation, Change, and the Backlog

> Week 4, meeting 2 of 2. Companion reading for the lecture; self-contained.
> Stage A is in flight; this lecture governs how it (and every later stage) changes
> the program.

## The drift bug, one more time

The first 9x9 attempt asked for a two-step move — *pick a column, then a row* — in
its opening prompt. The spec that shipped says *row, then column*. The code follows
the spec. Nobody ever decided; two artifacts disagreed, and the one that won, won
by accident.

Here is the thing to notice: this was not a green-field failure. The prompt, the
spec, and the code all existed already. The drift happened at a *change* — when
requirements moved and only some of the artifacts moved with them. Change requests
are where drift breeds, because change is when someone edits one thing and forgets
it has siblings.

Programs grow by requests, not rewrites. Your tic-tac-toe will take on a database,
a web interface, a second implementation language, and a tool server in the next
three weeks — every one of them a change to a working system. So today is about the
discipline that keeps a growing program's artifacts telling the same story: a
pipeline (elicit, amend, plan, build, verify) and a place for everything the
pipeline decides *not* to do (the backlog).

## Change control: the classical shape, the agentic price drop

Classical software engineering has had an answer to "how do you change a working
system?" for fifty years, and it reads like bureaucracy until the day it saves you:

1. A **change request** states what should be different and why.
2. **Impact analysis** finds everything the change touches.
3. Someone **approves** — scope, cost, risk.
4. The change is **implemented**, then **verified**, and the artifacts are updated.

Heavyweight process died in most places because steps 1, 2, and the artifact
updates cost more than the changes themselves. Here is what has changed: an agent
makes the artifacts cheap to maintain, which makes the discipline affordable at
toy scale — and the same agent makes *undisciplined* change fast enough to drift
the moment you stop paying attention. The process is newly affordable exactly when
it became newly necessary.

The agentic translation is compact:

| Classical step | Your version |
|---|---|
| Change request | The **spec amendment**, as a commit — the request and the decision record in one |
| Impact analysis | The elicitation session + **plan mode** — the plan you approve *is* the impact statement |
| Approval | You, approving the plan (committed under `plans/`) |
| Implement + verify | The build, then your gates (`pytest --cov` now; GATES.md from Stage C) |
| Update artifacts | Already done — the amendment came *first* |

That last row is the point of the whole table. Amendment-first is not ceremony; it
reorders the work so the artifact update cannot be forgotten, because it already
happened.

## Worked example: the ripple hunt

Stage A's recommended extension — configurable board size and win length — looks
like a two-line change. `game.py` starts with:

```python
BOARD_SIZE = 9
WIN_LENGTH = 5
```

Make them parameters, done? Run the impact analysis — grill the change the way
grill-me would grill you — and watch the ripple spread:

- **`main.py` hard-codes the board size in prose.** Every input prompt says
  "Enter a row (1-9)" and every digit check tests `1 <= value <= 9` with its own
  literal. A 19x19 game built on today's `main.py` would *say* "1-9" while
  accepting 1-19 — or worse, enforce 1-9 on a 19-wide board. The user-facing
  strings are part of the behavior; your spec amendment has to say so.
- **`render()` hard-codes its geometry.** The header line is the literal string
  `"     1 2 3 4 5 6 7 8 9"` and the border is `"-" * 18`. Change the board size
  and the header lies and the border is the wrong width. Nothing in the type
  system, nothing in the tests, will tell you — only the ripple hunt does.
- **The win-length interaction.** A 3x3 board with win length 5 is unwinnable.
  Does the spec forbid the combination, clamp it, or allow absurd configurations?
  A decision, and therefore a clause.
- **The tests assume 9x9.** Fixtures place marks at row 9; a configurable engine
  needs its tests told what configuration they run under. (And in week 7, the
  *shared* fixtures pin the baseline 9x9/5 contract for the port — one more
  artifact with an opinion.)
- **The AI's contract.** `random_move` picks from `available_moves()` — it
  survives any size unchanged. Knowing *that this is true, and why* (it never
  mentions geometry) is also impact analysis; "unaffected, because..." is a
  finding, not a shrug.

One "two-constant change": four files, the spec, and one genuinely new rule
(the size/win-length compatibility clause) that did not exist anywhere until you
hunted. **This is why the amendment comes first — the amendment is where the
ripple gets found, while finding it is cheap.** The amendment you commit after
this hunt is a different, better document than the one you would have written
before it.

In class, the demo runs this exact change end to end: grill-me, the amendment
commit, the approved plan into `plans/`, the implementation, the gates, and a
commit message that cites the amendment. Twenty minutes. That is the full cost of
the discipline at this scale — and it is the exact workflow Stage A grades.

## The backlog: where deferred things go to stay alive

The ripple hunt found more than you are going to do this week. The compatibility
clause, maybe. A niggle about `render()` deserving its own tests. The pipeline's
output is not just "do this" — it is also "not this, not now." Deferred work needs
a home, and there are only three candidates:

- **A TODO comment.** Dies in the file. Nobody reads a codebase's TODOs as a
  work queue; they are archaeology.
- **Your head.** Dies tonight. (Lecture 06 told you what session memory is worth
  across weeks — yours is not better.)
- **`BACKLOG.md`.** A file, in the repo, with a *reader*: you, at the start of
  every next stage — mandatorily.

The course's large-scale case study (lost-communities, which Project 2 builds on)
runs its backlog with two rules worth stealing verbatim. First, its header states
who reads it and when:

> Written by the Report phase. Read by the Gather phase of the next milestone —
> this is mandatory, and it is what stops the Report from being write-only.

A backlog nobody is *required* to read is a diary. The reading rule is what makes
it infrastructure — and yours starts in Stage B: before you begin any stage, you
read your backlog, and your stage plan says which entries it closes.

Second, look at the shape of a real entry and how entries die:

> **The fake-data notice must reach the UI at M5.** Every community, document,
> and metadata record in the repo is invented... a plausible-looking archive is
> exactly the thing someone might one day cite.

One bold line, then *why it matters*, then which milestone should absorb it. And
when an entry closes, it is struck through with a pointer to the milestone report
that closed it — never silently deleted. The backlog is an honest ledger: you can
read the whole history of deferred-then-done in one file.

Yours will be smaller. It should never be *empty* — an empty backlog after a week
of real work does not mean you finished everything; it means you stopped writing
things down. Expect your grader to believe exactly that.

## When to skip all this

The pipeline is for *behavioral* change. A refactor that provably preserves
behavior, a typo, a comment — commit them; no amendment, no plan file. The
boundary question that decides it: **would any test's expected value change?** If
yes, it is a spec matter. If no, it is housekeeping. When you are not sure, notice
that uncertainty is itself the answer: you do not know what the change touches,
which is precisely the condition impact analysis exists for.

## Questions to think about

1. Sort these into backlog / TODO comment / do-it-now: (a) "render() header will
   break for size != 9" discovered mid-Stage-A; (b) "the win-check scans all 81
   cells every move; fine for now"; (c) "seed.py should eventually take a player
   count argument." Defend each placement — and say who would ever read it there.
2. Your backlog has an entry three stages old that no stage has absorbed. What
   are the three honest things you can do with it, and which is worst?
3. The demo's change cost twenty minutes with full discipline. Estimate the cost
   of the *undisciplined* version going wrong in week 7 — be concrete about what
   the TypeScript port does with an undocumented render-geometry assumption.
