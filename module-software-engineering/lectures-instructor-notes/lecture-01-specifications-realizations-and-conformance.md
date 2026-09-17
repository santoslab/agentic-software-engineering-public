# Lecture 01 — Specifications, Realizations, and Conformance

> **Unit:** module-software-engineering · **Module week 1, meeting 1 of 2** · 75 minutes
>
> **Thesis:** A specification and a realization are two artifacts related by
> conformance; verification is the activity that checks the relation; when the check
> fails, one side is changed by a recorded decision, and the demo shows this
> happening in both directions.

## Learning objectives

After this lecture, students can:

1. Define specification, realization, conformance, and verification, and draw the
   relationships among them for a given pair of artifacts.
2. Given a failed conformance check, decide whether to change the specification or
   the realization, and justify the decision in terms of intent.
3. Compare human, agent, and algorithmic verification instruments on cost,
   repeatability, and coverage, and name one way each can produce an invalid result.
4. Write a planning prompt whose first step requires the agent to enumerate gaps and
   inconsistencies in the specifications before proposing a plan.

## Before class

Assigned before the module's first meeting (see `../reading-list.md`):

- [required] `../demos/lecture-01-note-specs-demo/starter/note-set-conops.md` and
  `starter/note-format-spec.md` (five minutes; the tour in class is then a reminder,
  not a first reading)
- [recommended] RFC 2119, key words for requirement levels

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–4 | Framing (demo Segment 0) | `ls` the repo: two specifications, a `CLAUDE.md`, no notes. The one-way description of spec-driven development and why it has single-pass development's weakness. State the five claims; promise one piece of evidence for each. Hook: "at least one thing in these drafts is wrong; we will not find it by staring at them." |
| 4–12 | Four terms (replaces Segment 1's tour) | With `note-format-spec.md` on screen: specification, realization, conformance, verification, defined as in the notes and instantiated on R1–R6. Diagram 1. Note the RFC 2119 keywords, the numbered rules, and `Version: 0.1 (draft)`. Show `CLAUDE.md` rules 2 and 4 and say when each will matter. One S, many R, in one sentence. |
| 12–24 | Planning: the specs push back (demo Segment 2) | Plan mode; the gap-finding prompt; the agent's numbered issue list; resolve with the three scripted decisions; amendments as a numbered list; approve; `git diff HEAD~1 -- note-format-spec.md`; `git log --oneline`. Say: information flowed from planning into S before any artifact existed. |
| 24–30 | Change S or change R (demo Segment 3, compressed) | Diagram 2. A failed check is a fact about the pair; S itself can be wrong (a missing rule, conflicting rules). Two ways to look for defects in S: examples that exercise every rule; analysis for incompleteness and inconsistency. Segment 2 was the S-side move: scope, R3, R7, 0.1 → 1.0.0, changelog with rationale. Who decided: a person, on record; a coordinating agent may share this later. Then `cat note-set-operations.md` after the scaffold: three specifications now govern the repository, each abstracting something different. |
| 30–36 | Operations (demo Segment 4) | Add blank note; add note with content (paste `sample-inputs/no-silver-bullet-content.md`); if ahead, add then remove "Design by Contract". `ls notes/`, `git log --oneline`. R6 held through every operation: conformance as an invariant, not a milestone. |
| 36–46 | The verification gate (demo Segment 5) | Paste the nonconformant Royce note; "check and report before fixing"; four findings citing R2, R3, R4, R5; repair; re-check passes. The R-side move. The R3 finding exists only because of Segment 2. The passing re-check is the completion condition. |
| 46–56 | Instruments and trust (Segment 6 from captures) | The three-instrument table; Diagram 3; captures of `check_notes.py --all`, the sabotage run (exit 1), the restore (exit 0). Mechanical rules vs judgment clauses. Then the six ways a result can be invalid; the checker is a realization too. |
| 56–62 | Specification 2.0.0 and the migration (Segment 7 from captures) | R8 and the amended R6; the migration commit; the agent-written summaries; the mechanical-vs-judgment table now splits R8. The false pass a 1.0.0 checker would have given. |
| 62–68 | Five claims, five pieces of evidence | The table; Diagram 4; the Royce closing point (the demo's first note argues against single-pass development). |
| 68–72 | Prompt template, Exercise 1, Project 0 | The six moves; what belongs in `CLAUDE.md`; Exercise 1 in three sentences; the Project 0 mapping (PKB specification, checklist, validator). |

Blocks sum to 72 minutes; 3 minutes slack.

## Demos

### Demo 1 — The note-set demo, interleaved

- **Artifacts:** `../demos/lecture-01-note-specs-demo/demo-script.md` (the
  segment-by-segment script with expected outcomes and recoveries); `starter/`,
  `sample-inputs/`, and `completed/check_notes.py` as described there.
- **Setup (before class):** the script's "Before class" checklist in full: a fresh
  demo repo from `starter/` with an initial commit; `python3` confirmed; the
  reference checker copied outside the repo; the sample inputs open in a plain-text
  editor; Claude Code started in the repo; one rehearsal with screenshots at every
  `[fallback capture]` marker. Segments 6 and 7 are shown from those captures in
  this lecture, so their rehearsal captures are required, not optional.
- **Script:** Segment 0 in the 0–4 block; Segment 1's tour folded into the 4–12
  block; Segment 2 in 12–24; Segment 3 compressed to a `cat` of the operations
  document in 24–30; Segment 4 in 30–36; Segment 5 in 36–46; Segments 6 and 7 from
  captures in 46–62; Segment 8's table in 62–68.
- **Expected outcome:** the class sees S change with R still (Segment 2), R change
  with S still (Segment 5), and three instruments report the same rule IDs on the
  same note.
- **Fallback:** the rehearsal captures, segment by segment, and the demo script's
  "If it goes differently" note for each segment.

## Discussion prompts

1. The agent found the three seeded gaps and possibly more. For one of the extra
   ones, was it a defect in S or a preference of the agent? How would you tell?
2. The R3 repair changed the heading because the amended rule says the field is
   authoritative. Who benefited from that sentence being in the specification rather
   than decided case by case?
3. `check_notes.py` returned exit 0 after the restore. List everything that exit code
   does and does not tell you.

## Assigned after class

- Readings (for L02): [required] Royce (1970); [recommended] Meyer (1992); see
  `../reading-list.md`.
- Exercise: `../exercises/exercise-01-conformance-three-ways.md`, due before
  Lecture 03.

## Instructor notes

- **Cut if running long:** first the add/remove pair in the 30–36 block (say why O3
  needs its precondition and move on); then compress the 56–62 block to one capture
  (the migration diff) and one sentence on the false pass.
- **Risks:** plan-mode UI differs across Claude Code versions; the script's recovery
  is to run the same prompt in normal mode with "do not create or modify files
  until I approve a plan." The agent may miss a seeded gap; the script has one nudge
  per gap. Segment 5 depends on pasting from a plain-text editor; a Markdown-aware
  editor can silently repair the seeded violations. Time: the 12–24 block runs over
  if the issue list is long; defer extras to the operations document's "Deferred
  questions" section rather than resolving each one.
- **Variants:** with a strong room, pause after the gap-finding prompt is typed and
  have students write their own gap list for two minutes before the agent's appears;
  compare. With laptops, students can run Segment 5 on a note of their own in
  parallel.
