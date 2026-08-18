# Lecture 08 — The Growing Program: Elicitation, Change, and the Backlog

> **Unit:** weeks-04-07 · **Week 4, meeting 2 of 2** · 75 minutes
>
> **Thesis:** Programs grow by requests, not rewrites — the discipline is a governed
> pipeline (elicit → amend the spec → plan → build → verify), and what you decide
> *not* to do now goes in the backlog, not in your head.

## Learning objectives

After this lecture, students can:

1. Run a requirement-elicitation session for a *change* to an existing system, not
   just a green-field build.
2. Write a spec amendment and explain why it precedes the implementing commit.
3. Perform an informal impact analysis and predict a change's ripple beyond the
   obvious files.
4. Maintain a credible BACKLOG.md: what goes in, how entries close, and why an
   empty backlog is a red flag.

## Before class

- [required] `project-1-brief.md` — in full.
- [required] The Spec-Driven Development section of `prompt-cheat-sheet.md` (re-read).

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–10 | Cold open: the drift bug | Attempt1, Session 12 (from L04): the prompt said column-then-row; the shipped SPECS said row-then-column. Nobody decided — two artifacts quietly disagreed. Change requests are where drift breeds, because change is when someone edits *one* artifact and forgets the others. Today's pipeline exists to make that structurally hard. |
| 10–24 | Change control, classical → agentic | Classical: change request → impact analysis → approve → implement → verify. Agentic translation: the *spec amendment commit* is the change request and the decision record in one; plan mode is the impact analysis you approve; the gate run is the verification. Nothing was invented — the artifacts got cheaper to maintain, so the discipline became affordable at toy scale. |
| 24–40 | Worked example: impact analysis on the Stage A extension | "Make board size configurable" looks like editing two constants. Grill the change: `main.py` hard-codes "1-9" in every prompt string and digit check; `render()` hard-codes its header row and border width; the AI's contract (does random need to know?); test fixtures assume 9x9; the spec's win-length interactions (3x3 needs win length 3). One two-constant change touches four files and the spec. **The ripple is why amendments come first: the amendment is where you *find* the ripple while it's cheap.** |
| 40–54 | Demo 1 — a governed change, end to end | Live on the instructor's starter copy: grill-me on the extension → SPEC.md amendment (committed) → plan mode (approve, export to `plans/`) → implement → `pytest --cov` green → commit referencing the amendment. Twenty minutes of the exact workflow Stage A grades. |
| 54–66 | The backlog | What the pipeline defers needs a home. Read real `BACKLOG.md` entries from the lost-communities case study (structure: one-line item + *why it matters* + which milestone absorbs it; entries close by strikethrough with a pointer to the closing milestone report — never silently deleted). Three homes for a loose end: TODO comment (dies in the file), your head (dies tonight), BACKLOG.md (read at the start of every next stage — the only one with a *reader*). P2 preview: the Gather phase is *required* to read the backlog; that rule starts now, solo. |
| 66–75 | Stage A workshop | Students start grill-me on their chosen extension in-seat; instructor circulates. Target before leaving: three ripple items your amendment must cover. |

## Demos

### Demo 1 — A governed change, end to end

- **Artifacts:** instructor's copy of `tictactoe-starter` with Stage A's SPEC.md
  already present (from the L07 demo, cleaned up); the grill-me skill installed.
- **Setup (before class):** SPEC.md committed; venv ready; `pytest --cov` green at
  100% branch on `game.py`; rehearse the timing — the implement step must be
  allowed to run while narrating the plan.
- **Script:** (1) `/grill-me` the configurable-size change — answer its questions
  from the 24–40 block's analysis; (2) amend SPEC.md, commit *just that*;
  (3) plan mode → approve → save plan under `plans/`; (4) let it implement;
  (5) run gates; commit with a message citing the amendment commit.
- **Expected outcome:** the full Stage A workflow, timed proof that discipline at
  this scale costs minutes, not days.
- **Fallback:** pre-recorded run of the same session; the two commits shown as
  static diffs (amendment first, implementation second) preserve the core point.

## Discussion prompts

1. What belongs in BACKLOG.md vs a TODO comment vs an issue tracker? (Scale — and
   who reads each one, and when.)
2. An empty backlog after a stage of real work: what does it actually tell you?
3. When is it *right* to skip the amendment and just fix the code? (Behavior-
   preserving refactors; typos. The boundary is "would a test's expectation
   change?")

## Assigned after class

- Readings (for L09):
  - [recommended] Python `sqlite3` module docs — the tutorial section.
  - [recommended] Skim your Ex. 2 target repo's migration folder if it had one —
    now you know what you were looking at.
- Stage A checkpoint: end of this week.

## Instructor notes

- **Cut if running long:** the workshop block (66–75) is the shock absorber; the
  demo is not cuttable — it is the stage's workflow made visible.
- **Risks:** the demo's implement step can wander; keep the plan tight (two
  files + tests) and let anything else become a live BACKLOG.md entry — which is
  itself a teaching moment. Students will ask if every one-line change needs this;
  answer with prompt 3's boundary rather than a blanket yes.
- **Variants:** if the L07 demo already produced a strong SPEC.md, diff the
  instructor's against the best student attempt from the room for two minutes
  before the demo.
