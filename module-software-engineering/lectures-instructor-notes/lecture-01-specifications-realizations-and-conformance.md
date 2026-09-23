# Lecture 01 — Specifications, Realizations, and Conformance

> **Unit:** module-software-engineering · **Module week 1, meeting 1 of 2** · 75 minutes
>
> **Thesis:** A specification and a realization are two artifacts related by
> conformance; verification checks the relation; when the check fails, one
> side is changed by a recorded decision. The demo shows the specification
> changed first, before any realization exists, and then a realization
> changed with the specification held still.

## Learning objectives

After this lecture, students can:

1. Define specification, realization, conformance, and verification, and draw
   the relationships among them for a given pair of artifacts.
2. Assess a specification against the five quality properties by running the
   audit in `process/spec-audit.md` (AUD-1 through AUD-7), and produce a gap
   list in the form RPT-1.
3. Given a failed conformance check, decide whether the specification or the
   realization changes, and record the decision in the form the process
   requires (an amendment proposal, RPT-3; a ruling before any repair, RPT-4).
4. Compare the three kinds of verifier — human, agent, algorithmic — on cost,
   repeatability, and the clauses each can decide; name one way each can
   produce an invalid result; state the three scope lines a conformance report
   must carry (RPT-2).

## Before class

Assigned before the module's first meeting (see `../reading-list.md`):

- [required] The Lecture 01 handout,
  `../student-materials/handout-lecture-01-note-set-starter.md`: the
  specification `note-format-spec.md` 0.1, the loader `CLAUDE.md`, and the
  three process documents (`spec-audit.md`, `reporting.md`,
  `verification.md`). Ten minutes; class time is not spent reading them.
- [recommended] RFC 2119, key words for requirement levels.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–4 | Framing | `ls` the demo repository: one specification, a `CLAUDE.md`, a `process/` folder, no notes. The example: a set of study notes, one markdown file per article; the questions it raises (how is a note formatted; who checks). Why it is small: six rules fit on a screen, and every concept in the lecture can be pointed at in a file. Where the module goes: Lecture 02 adds the operations on the set and a concept of operations; Lectures 03–06 apply the same method to a program. |
| 4–14 | Four terms, on the specification | With `note-format-spec.md` on screen: specification, realization, conformance, verification, defined as in the notes and instantiated on R1–R6. One S, many R. RFC 2119 keywords; numbered rules; `Version: 0.1 (draft)`. Diagram 1. Read `CLAUDE.md`: one governing document, three process documents, two rules. |
| 14–20 | Evaluating a specification: the quality properties as an audit | Unambiguous, internally consistent, externally consistent and aligned, complete for its level, traceable — and where they live: `process/spec-audit.md`, as AUD-1 through AUD-5, with AUD-6 (the three places to search) and AUD-7 (the output is an RPT-1 list; then stop). The three process files: two always loaded (RPT, VER), one run on request (AUD). |
| 20–34 | Demo, Segment 2 — the audit | The prompt is typed; the room writes its own gap list for two minutes; the agent's RPT-1 list appears; compare. The three seeded findings (the scope sentence against R6; R2 against R3; the filename). Rulings; amendments per RPT-3; approval; version 1.0.0; `git diff`; `git log`. The specification moved before any realization existed. |
| 34–40 | Change S or change R | A failed check reports a fact about the pair. Two ways to find defects in S: realistic examples; analysis — which is what the audit is. The developer decides which side moves; the decision is recorded in the changelog when S moves and in the commit message when R moves. Diagram 2. |
| 40–52 | Demo, Segment 3 — the verification gate | The careless note pasted in; the index written by hand. "Check and report per RPT-2; change nothing." Four findings citing R2–R5, the rule text quoted; the three scope lines. The ruling; the repair; the passing re-check; the commit. The realization moved with the specification held still. The R3 finding exists only because of Segment 2. |
| 52–64 | Demo, Segment 4 — three kinds of verifier | `check_notes.py` written; `--all`; the sabotage run and the restore. The VER-1 table: human, agent, algorithmic — cost, repeatability, which clauses. VER-2: every clause of 1.0.0 is mechanical; judgment clauses come later. The verifier is itself a realization of the specification and can be wrong; the six ways a result can be invalid, and the RPT-2 scope lines as the response. Diagram 3. |
| 64–70 | What the process documents did today | AUD ran once, on request, before anything was built. RPT gave every report its form — the gap list, two conformance reports, an amendment proposal. VER named the kinds of verifier and classified the clauses. Not yet present: operations on the set, a concept of operations, the invariant — Lecture 02. |
| 70–72 | Exercise 1; before next meeting | Exercise 1 in three sentences. Readings. |

Blocks sum to 72 minutes; 3 minutes slack.

## Demos

### Demo 1 — The note-set demo, part 1

- **Artifacts:** `../demos/lecture-01-note-specs-demo/demo-script-lecture-01.md`
  (segments, prompts, expected outcomes, recoveries); `starter/`;
  `sample-inputs/royce-note-filled-nonconformant.md`;
  `starter-l02/check_notes.py` as the Segment 4 fallback.
- **Setup (before class):** the script's checklist in full: a fresh repository
  from `starter/` with an initial commit; `python3` confirmed; the fallback
  verifier copied outside the repository; the sample input open in a plain-text
  editor; Claude Code started in the repository with the always-on process files
  loaded; one rehearsal with captures at every `[fallback capture]` marker.
- **Script:** Segment 1 (the tour) is folded into the 4–14 and 14–20 blocks;
  Segment 2 in 20–34; Segment 3 in 40–52; Segment 4 in 52–64.
- **Expected outcome:** the class sees S change with no R present (Segment 2), R
  change with S still (Segment 3), and three kinds of verifier report the same
  rule identifiers on the same note (Segments 3 and 4).
- **Fallback:** the rehearsal captures, segment by segment; each segment's *If
  it goes differently* note in the script.

## Discussion prompts

1. The audit found three defects before any note existed. Which quality
   property did each violate, and would a realization have revealed it sooner?
2. The R3 finding on the careless note exists only because of an amendment made
   forty minutes earlier. What would a report against 0.1 have said, and would
   that report have been wrong?
3. `check_notes.py` returned exit 0 after the restore. List what that exit code
   establishes and what it does not, using VER-2 and the RPT-2 scope lines.

## Assigned after class

- Readings (for L02): [required] Royce (1970); [required] Meyer (1992) — the
  precondition and postcondition are the form Lecture 02 gives to an operation;
  [required] the Lecture 02 handout: `note-set-conops.md` 0.1 and the three
  process documents Lecture 02 adds (`process/README.md`,
  `development-rules.md`, `conops-audit.md`). See `../reading-list.md`.
- Exercise: `../exercises/exercise-01-conformance-three-ways.md`, due before
  Lecture 03.

## Instructor notes

- **Cut if running long:** the 14–20 block compresses to the AUD headings on
  screen and one sentence per property; Segment 4's sabotage run can be shown
  from captures. Never cut Segment 2.
- **Risks:** plan-mode UI differs across Claude Code versions (the script's
  recovery: the same prompt in normal mode with "do not create or modify any
  file until I approve"). A seeded finding missed — one nudge each, in the
  script. The paste in Segment 3 must be into a plain-text editor. Segment 2
  runs over when the list is long: rule on the three seeded findings, mark the
  rest deferred.
- **Variants:** with a strong room, have students write their own gap list for
  two minutes before the agent's appears, then compare. With laptops, students
  run Segment 3 on a note of their own in parallel.
