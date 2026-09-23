# Project 1 — Reversi, Specification-First

> **Assigned:** Lecture 05 (Part 1) and Lecture 06 (Part 2) · **Due:** Part 1 —
> end of the L05/L06 week; Part 2 — one week later *(dates: instructor to fix)* ·
> **Effort:** Part 1 ≈ 3–4 h, Part 2 ≈ 6–8 h *(unvalidated until the reference
> solution exists)*
>
> **Requires:** Claude Code, Python 3.11+, git, `pytest` with `pytest-cov`.
>
> **Status:** draft; instructor review required before assigning (dates,
> effort estimates).

## 0. What this project is

Someone wants a text-based Reversi and has written down their general idea as a
sketch of a concept of operations. That sketch, a `CLAUDE.md`, and a `process/`
folder are everything you receive. There is no specification, no code, no tests.

You will do to Reversi exactly what Lectures 03 and 04 did to five-in-a-row
tic-tac-toe: turn the sketch into a ConOps by elicitation, derive a family of
specifications from the ConOps, realize them through plan mode, and verify the
realization with a test suite that cites the specification and a coverage gate
that enforces it. The method is the same; the game is harder in ways that make each
kind of specification earn its place (§4).

Later stages of Project 1 — persistence, a web layer, a port to another language
proven equivalent by shared fixtures, an MCP server — build on what you produce
here. Read Stages B–E of the project unit's brief
(`../weeks-04-07/project-1-brief.md`) with "Reversi" in place of "tic-tac-toe";
they are otherwise unchanged.

## 1. What you get

| File | What it is |
|---|---|
| `student-materials/reversi-starter/CONOPS-sketch.md` | The client's general idea, in the Lecture 02 skeleton with sections 2, 3, and 6 omitted (no existing system). Incomplete on purpose; it contains at least one internal tension. |
| `student-materials/reversi-starter/CLAUDE.md` | The loader: the governing documents in authority order, the process files, two bootstrap rules, the commands. |
| `student-materials/reversi-starter/process/`, `…/BACKLOG.md` | How development proceeds with respect to the specifications — `development-rules.md` (DEV), `spec-audit.md` (AUD), `conops-audit.md` (AUDCON), `verification.md` (VER), `reporting.md` (RPT), and the invariant in `process/README.md` — identical to the in-class demo's. DEV-8 makes the audit a standing law; `BACKLOG.md` is where deferred questions go (DEV-6). |

Also available as a worked example: the in-class 9×9 demo repository, tag by tag
(`t0-conops-sketch` … `t5-fixtures`; `demos/lecture-03-game-demo/reference/` is
the `t5` state). Point your agent at its **specifications and tests as
patterns** if you like. Do not start from its code; your engine is derived
from your `SPECS.md`, and your git history has to show that.

**Where the sketch is silent, the client's intent is standard Reversi** (8×8; the
standard four-disc opening; dark moves first; a move must flip at least one disc; a
player with no legal move passes; the game ends when neither player can move; more
discs wins; equal counts tie). This does not let you skip the questions. Your job
is to *find* every place the sketch leaves a decision open, record the ruling, and
state it in the specification — a specification that leaves a standard rule
implicit fails the completeness check. Rulings that are genuinely yours (display
glyphs, hints, post-game options, side alternation, error wording, interface
shapes, module split) are yours to make and record.

## 2. Part 1 — Own the specifications *(assigned L05)*

1. **Sketch → `CONOPS.md`.** In plan mode: read the sketch; before anything
   else, run the audits on it as DEV-8 requires — `process/conops-audit.md`
   (AUDCON) and `process/spec-audit.md` (AUD) — and deliver the gap list in the
   form RPT-1, numbered, each item with a recommended resolution; rule on each;
   approve the amendments (RPT-3); write `CONOPS.md` 1.0 with a changelog. It
   must be in the third person and implementation-free (AUDCON-1, AUDCON-5), must
   fill every section the skeleton keeps (AUDCON-7), and must exercise every mode
   and policy in a scenario (AUDCON-3) — including solo play, two-player play, a
   pass, a game that ends before the board is full, and recovery from an entry
   the program rejects.
2. **`CONOPS.md` → `SPECS.md`.** Same moves, new target. One file, one section per
   kind, in this order: board and coordinates; rules of play; display format
   (byte-exact, with an empty-board and a mid-game example); input grammar;
   interaction flow (menus, per-game loop, pass handling, post-game); interface
   contract (each public operation with its pre- and postconditions — a move's
   postcondition names the discs that flip); an example session; verification
   obligations. Number every clause so tests can cite it (AUD-5). Audit it before
   planning anything (DEV-8): AUD-8 through AUD-14 apply section by section.
   Version 1.0.0, changelog. The kinds and their order are pre-picked for this
   assignment, as they were for the in-class demo, so that every submission has
   the same shape; in general, choosing the kinds of specification is a decision
   the developer or the organization makes, and the course catalog
   (`../specification-kinds.md`) is the menu.
3. **Verification obligations, not a testing contract.** The policy — 100%
   branch coverage, the single permitted pragma, citation discipline, fixtures
   never edited — is already in your `process/verification.md` (VER-4 through
   VER-8) and is not yours to weaken. Your `SPECS.md` §9 lists the
   *obligations*: what the tests must claim about Reversi, category by category,
   each traced to the clauses it verifies (AUD-14). The demo's `SPECS.md` §9.5
   (`demos/lecture-03-game-demo/reference/SPECS.md`) is the model; notice how
   much of it carries over — that is the point.
4. **Commit the elicitation.** Export the session(s) that produced the two
   documents to `transcripts/part-1-elicitation.md`. The RPT-1 gap lists, your
   rulings, and the RPT-3 amendments are the evidence that the specifications
   were *elicited*, not typed.
5. **`CLAUDE.md` and `process/`.** Keep them as shipped; a process rule changes
   only by a recorded amendment (DEV-3). Add to `CLAUDE.md` how to run the game
   and the tests once they exist.

**Required elements (all must be present):**

- [ ] `CONOPS.md` 1.0 — third person, implementation-free, all kept sections
      filled, five scenarios as above, glossary, changelog
- [ ] `SPECS.md` 1.0.0 — the eight sections above, every clause numbered, examples
      byte-exact, changelog
- [ ] Every decision in §4 of this brief is stated explicitly in one of the two
      documents (the ConOps for what a player observes, `SPECS.md` for the rest)
- [ ] `transcripts/part-1-elicitation.md` showing at least two RPT-1 gap lists
      (one per document), your rulings, and the RPT-3 amendments
- [ ] `CLAUDE.md` and `process/` as shipped, or amended only with a changelog entry
- [ ] Git history: the ConOps committed before the `SPECS.md` work begins

## 3. Part 2 — Realize and verify *(assigned L06)*

1. **Plan, then build.** Plan mode from `SPECS.md`; the approved plan committed
   under `plans/` before the implementing commits. Module split per your spec
   (pure engine with no I/O; computer strategies as static methods; all I/O in the
   entry point is the demo's split — yours may differ if your spec says so).
2. **Tests that cite (VER-6).** One test file per source module; every test's
   docstring cites the clause it verifies; tighter never looser; direct board
   assignment for *setup* only; no tautological tests. Every obligation in your
   `SPECS.md` §9 is claimed by at least one test.
3. **The gate (VER-4, VER-5).** `pytest --cov=. --cov-branch
   --cov-report=term-missing --cov-fail-under=100` passes; the only
   `# pragma: no cover` is the `__main__` guard.
4. **Fixtures (VER-7).** `fixtures/scenarios.json` in the shape of §3.1, with a
   loader in `tests/`. At least: an opening move with its flips; a move that flips in more
   than one direction; a rejected move that flips nothing; a rejected entry that
   is not a square; **a scenario containing a pass**; **a game that ends before
   the board is full**; a full-board game with its final count; a tie. The pass and
   early-end scenarios are hard to construct by hand — generate them with your
   engine if you must, but *verify them against your specification by hand* before
   trusting them, and say how you did it in the report.
5. **Spec amendments (DEV-2, DEV-3).** Implementation will find something the
   specification did not settle. Propose the amendment (RPT-3), get it approved,
   and commit it before the code that depends on the ruling — a change of
   specified behavior, DEV-2 (c). A question you cannot settle goes to
   `BACKLOG.md` (DEV-6).
6. **`PART-2-REPORT.md`,** half a page: the amendment(s) implementation forced;
   one thing 100% branch coverage did *not* tell you about conformance (VER-8);
   how the
   pass and early-end fixtures were constructed and checked; what you could not
   verify by reading.

### 3.1 Fixture shape

Moves are squares in the notation your input grammar defines (`d3`); the literal
`"pass"` means the player to move has no legal move and the engine must report
that before play continues. Colors are named `dark` and `light` regardless of the
glyphs your display uses, so the same file can later run against an engine in
another language.

```json
{
  "description": "Reversi engine fixtures. Standard rules: 8x8, standard opening, dark moves first.",
  "games": [
    {
      "name": "dark-opens-d3",
      "moves": ["d3"],
      "flips": [["d4"]],
      "expected": {"to_move": "light", "dark": 4, "light": 1, "over": false}
    }
  ],
  "rejections": [
    {"name": "flips-nothing", "setup_moves": [], "attempt": "a1"},
    {"name": "occupied",      "setup_moves": [], "attempt": "d4"}
  ]
}
```

Loader contract: from a fresh game, play `moves` in order; every listed move is
accepted; `flips[i]`, if present, is exactly the set of squares flipped by move
`i`; after the last move the engine's state matches `expected`. A `rejections`
entry plays `setup_moves`, submits `attempt`, and requires rejection with the board
and the player to move unchanged. The file is never edited to make a test pass — a
wrong expectation is a specification conversation (VER-7).

**Required elements:**

- [ ] Engine, computer strategy, and CLI per `SPECS.md`; the game runs
- [ ] `pytest` green; the gate command passes at 100% branch with the single
      permitted pragma
- [ ] Every test cites a `SPECS.md` clause (VER-6); every obligation in §9 is
      claimed by at least one test
- [ ] `fixtures/scenarios.json` with the eight scenario kinds above, and a loader
- [ ] At least one `SPECS.md` amendment committed **before** the code that
      depends on it; `BACKLOG.md` lists it
- [ ] `plans/` holds the approved plan (DEV-9); git history shows spec-before-code (DEV-2)
- [ ] `PART-2-REPORT.md` with the four sections

## 4. Decisions your specification must record

By kind — the kinds of the course catalog, `../specification-kinds.md`; *computer
opponent* below is a subject that spans three of them. Each is either observable by a player (state it in the ConOps and pin it
in `SPECS.md`) or internal (`SPECS.md` only). Finding them is the exercise; this
list is the floor, not the ceiling.

- **Rules of play.** The exact opening position and which color it gives the first
  move. Who moves first. That a move must flip at least one disc, and that *all*
  flanked runs in *all* directions flip. Whether a pass is forced or chosen. What
  happens after a pass (whose turn; is it announced). When the game ends — and
  that this is not "when the board is full." Who wins on equal counts. Whether a
  move can be taken back.
- **Display.** The glyphs for dark, light, and empty. Row and column labels.
  Whether legal-move hints are shown, when, and how. Whether the count is shown
  during play. Byte-exact format.
- **Input grammar.** The square notation; case; whitespace; length; what is
  rejected and with what effect on the turn. Whether a pass is typed or automatic.
- **Interaction flow.** Menus and their options; the per-game loop; how a pass is
  presented; post-game options; in solo play, which color the human has and
  whether it alternates on a rematch; in two-player play, whether anything
  alternates.
- **Interface contract.** How a square is named to the engine; what a move
  operation returns and what it changes (including the flipped set); how legality
  is queried; how "no legal move" is exposed; how game-over and the count are
  exposed; what an operation does after the game is over.
- **Computer opponent.** "Random among legal moves" — and how that is tested.
- **Verification obligations (`SPECS.md` §9).** The categories of behavior the
  tests must claim, each traced to clauses (AUD-14). The policy — target,
  pragma, citation discipline, fixtures — is fixed by VER-4 through VER-8 and is
  not a decision.

## 5. Process rules

1. **Spec before code (DEV-2).** A change of specified behavior trails a committed
   amendment; a repair follows a report and a ruling; a conformance-preserving
   change says so in its commit. Checked by reading your git history.
2. **Audit before plan; plan before build (DEV-8, DEV-9).** Approved plans under
   `plans/`.
3. **The process stands.** `CLAUDE.md` and `process/` are not edited to weaken a
   rule; a process document changes only by an amendment proposal (RPT-3) with
   a changelog entry (DEV-3).
4. **`CONOPS.md` never names an implementation (AUDCON-1).** A ConOps that says
   "Python," "class," or "list" is returned.
5. **Every operation ends the same way (DEV-7):** verified, reported (RPT-5),
   and committed under a message that names it (`conops: 0.1 sketch -> 1.0`,
   `specs: amend 4.3 pass handling`, `engine: legal_moves`).

## 6. Grading

Completion-based. Each part is **satisfactory** when every required element is
present and honest — a documented failure or a well-argued deviation counts, a
missing element does not. One resubmission pass per part.

## 7. What comes next

Stages B–E of the project unit's brief (`../weeks-04-07/project-1-brief.md`),
with Reversi as the subject. Your
`fixtures/scenarios.json` and the instructor's shared fixture set are what the
port stage will run against your engine and its counterpart in another language.
Your Part 2 engine — obvious, spec-traceable, tested — is the executable
specification a later stage will hold a faster implementation to.

## 8. Do / don't

- **Do** rule on gaps yourself and record the ruling; **don't** let the agent
  decide by default and discover the decision in the code later.
- **Do** reuse the demo's `SPECS.md` §9.5 as the model for your obligations —
  the `process/` set is already yours; **don't** start from its code.
- **Do** commit transcripts and plans; **don't** summarize them from memory.
- **Don't** edit a fixture to make a test pass.
