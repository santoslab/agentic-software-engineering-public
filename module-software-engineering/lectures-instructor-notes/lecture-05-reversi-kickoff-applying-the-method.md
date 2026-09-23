# Lecture 05 — Reversi Kickoff: Applying the Method

> **Unit:** module-software-engineering · **Module week 3, meeting 1 of 2** · 75 minutes
>
> **Thesis:** The method is the same moves on a game you were just handed; the
> first move is an audit you can watch, and everything after it is yours.

## Learning objectives

After this lecture, students can:

1. Learn a game's rules from a ConOps sketch and sort its observable policies
   into stated, implied, and missing (AUDCON-2, AUD-4).
2. Produce an RPT-1 gap list on the Reversi sketch and rule on at least three
   items — the end condition, the opening position, the consequences of a pass.
3. Map each Project 1 deliverable onto the process rule that governs it.
4. State the convergence rule: where the sketch is silent the client's intent is
   standard Reversi, but every such rule must be *stated*, and the choices that
   are genuinely the student's are recorded as rulings.

## Before class

Assigned at Lecture 04:

- [required] The Project 1 brief, `../project-1-reversi-brief.md`, in full.
- [required] `../student-materials/reversi-starter/CONOPS-sketch.md`, read as a
  player.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–8 | Where we are: one method, applied twice | The specification-family table as a checklist, one row per kind, each with the AUD rule that audits it and the VER row that verifies it. Buffer: anything L03 or L04 dropped is picked up here (the overline chain; DEV-2's three kinds; the fixtures run). |
| 8–22 | Learn Reversi from its ConOps sketch | Read §1.2 and §4.2 aloud. The rules as observable policies: place, flank, flip, forfeit, count. Stated: two colors; a move must trap; forfeit when no move; count when full. Implied: an opening position exists ("a few discs in the middle"). Missing: who moves first; equal counts; what happens after a forfeit. The tension students should find themselves: "the board is full" as the end, alongside forced forfeits that mean it may never fill. Reading a ConOps to learn a game *is* validation. |
| 22–48 | Demo 1 — the round-1 audit on the Reversi sketch | The room writes its gap list for three minutes; type the round-1 prompt; the agent's RPT-1 list; compare against the key. Rule live on four scripted gaps — the end condition (neither player can move), the opening (d4/e5 light, d5/e4 dark, dark first), the consequences of a pass (forced, announced, opponent moves, two in a row ends the game), all runs in all eight directions flip. Defer one live (DEV-6). Show one ruling becoming an RPT-3 amendment. **Stop before `CONOPS.md` is written** — that is Part 1. |
| 48–62 | The Project 1 deliverables, and the rule behind each | Part 1: `CONOPS.md` (AUDCON-1…8), `SPECS.md` with numbered clauses and §9 as obligations (AUD-8…14), the transcript with RPT-1 lists and RPT-3 amendments, `CLAUDE.md` and `process/` as shipped. Part 2: the plan (DEV-9), tests that cite (VER-6), the gate (VER-4, VER-5), fixtures with a pass and an early-end scenario (VER-7), at least one amendment committed before the code that needs it (DEV-2 (c), DEV-3), the report with what coverage did not tell you (VER-8). The convergence rule. Effort and dates. |
| 62–72 | Logistics, Q&A | The `process/` set is adopted, not authored — a rule changes only by DEV-3 with a changelog entry. `d3` notation and the letter→index decision. What *student's choice* means and how it is graded (recorded, consistent, stated in the right document). Where to ask. |

Blocks sum to 72 minutes; 3 minutes slack.

## Demos

### Demo 1 — The audit on the Reversi sketch

- **Artifacts:** `../demos/lecture-05-reversi-audit/demo-script-lecture-05.md`;
  `../student-materials/reversi-starter/` (the sketch, the loader, the L04
  `process/`, `BACKLOG.md`); `../demos/lecture-05-reversi-audit/expected-gaps.md`
  (the key: 26 decisions, standard rulings, *student's choice* marks, nudges).
- **Setup (before class):** fresh clone of the starter with an initial commit;
  Claude Code open; the prompt in a text file; rehearsal captures.
- **Script:** (1) three minutes for the room's list; (2) the prompt — *"Read
  `CONOPS-sketch.md` and the process documents. Before proposing anything, run
  the audits in `process/conops-audit.md` and `process/spec-audit.md` on the
  sketch (DEV-8) and report the gap list per RPT-1 — numbered, each with your
  recommended resolution. Then stop and wait for my rulings."*; (3) compare; rule
  on the four scripted gaps (the end condition, the opening, the pass, the
  flips), deferring the hints item; (4) *"Propose the amendment for gap 1 per
  RPT-3 and wait"* — show the form, approve nothing further; (5) stop, and say
  why: the rest is the homework.
- **Expected outcome:** students have seen the exact first move of Part 1
  performed on their own starter, and have a list of their own to compare with
  the agent's.
- **Fallback:** captures; the key stands in for the agent's list.

## Discussion prompts

1. The sketch says the game ends when the board is full, and that a player with
   no move forfeits the turn. Which statement is wrong? (Neither — one is
   incomplete. Which, and how do you know?)
2. Which rulings in your gap list are yours to make, and which are the client's?
   Where does the brief draw that line, and why does it draw it there?
3. Part 2 requires a scenario containing a pass. Before you trust a scenario your
   own engine generated, what do you check it against, and how?

## Assigned after class

- Readings (for L06): [required] MCP documentation, core concepts and the
  FastMCP quickstart; [required] the dice-server README
  (`../../weeks-04-07/student-materials/mcp-example/README.md`).
- Project: **Project 1, Part 1** launched today; due at the end of this week
  (date per the brief).

## Instructor notes

- **Cut if running long:** the deliverables block (48–62) compresses to the
  required-elements checklist on one slide — the brief is the reading. Never
  cut the audit demo or the stop before the ConOps is written.
- **Risks:** students who know Reversi supply rules the sketch does not state and
  call them obvious. Say once that a rule the sketch does not state is a finding,
  whatever the reader already knows, and that the convergence rule says how such
  findings are resolved. The
  agent's list will be longer than the key; rule on four and defer the rest. This
  lecture is deliberately lighter; if L03/L04 ran on time, the buffer block
  becomes Q&A on the brief.
- **Variants:** pairs rule on two gaps each and read the rulings aloud; the class
  audits each against AUDCON-2 and AUD-1.
