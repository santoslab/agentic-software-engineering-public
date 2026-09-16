# Exercise 1 — Conformance Three Ways

> **Assigned:** Lecture 01 · **Due:** before Lecture 03 · **Effort:** 2–3 hours
>
> **Requires:** Claude Code; Python 3.11 or newer; git. Uses the note-set demo in
> `../demos/lecture-01-note-specs-demo/`.
>
> **Status:** draft; instructor review required before assigning.

## Goal

Run the same conformance check with three instruments (yourself, an agent, and a
program) on a note you wrote, and account for where they agree, where they differ,
and how each could have been wrong. This is Lecture 01's verification section
applied to your own artifact. It is deliberately small: Project 0 is starting at
the same time and is the larger application of the same ideas.

## Setup

1. Copy the demo's `starter/` directory somewhere outside the course repository and
   make it a git repository with one initial commit (the demo script's "Before
   class" checklist, step 1).
2. Do **not** read `sample-inputs/royce-note-filled-nonconformant.md` until step 5
   of the task. The exercise depends on your own note, not the demo's.
3. Read the demo script's final section, "Recreating this demo yourself."

## Task

1. **Plan.** Run the demo's Segment 2 in your own Claude Code session: the
   gap-finding prompt in plan mode, your own resolutions, the amendments, the
   commit. Save the agent's numbered issue list. Then read the demo script's
   "Folder layout" section and compare your list with the three seeded gaps. Note
   which seeded gaps your run found, which it missed, and what else it found.
2. **Scaffold and populate.** Run Segments 3 and 4 far enough to have `notes/`,
   `index.md`, `note-set-operations.md`, and at least one note.
3. **Write a note carelessly.** In a plain-text editor, write a note of your own on
   any software-engineering topic, 20–40 lines, without consulting the format
   specification. Save it into `notes/` and add an index entry by hand. Commit it
   with the message `careless note (before)`.
4. **Check it three ways.**
   - *Person:* read `note-format-spec.md` at its current version and list every
     violation you can find in your note, citing rule IDs.
   - *Agent:* ask the agent to check the note for conformance and report before
     fixing anything (Segment 5's prompt). Save the report.
   - *Program:* either have the agent write `check_notes.py` with Segment 6's
     prompt and run it, or run the demo's reference `completed/check_notes.py`. The
     reference checker implements specification version 2.0.0; if your
     specification is at 1.0.0, it will report R8 findings that your specification
     does not contain. Keep them in your table and explain them in step 5.
5. **Compare.** Build a table with one row per finding and one column per
   instrument (found / not found / not applicable). Explain at least one row where
   the instruments disagree or where one instrument could not decide the clause.
   Now read the demo's `sample-inputs/royce-note-filled-nonconformant.md` and the
   four-violation table in the script's Segment 5; note any violation type it
   seeded that your note did not contain.
6. **Decide and reflect.** For one finding, state whether the specification or the
   note should change, and why. For each of the three instruments, name one
   concrete way its result on your note could have been invalid (Lecture 01 lists
   six failure modes; pick the ones that apply).
7. **Repair.** Have the agent repair the note; confirm the re-check passes; commit
   as `careless note (after)`.

## Deliverable

A folder (zip or repo link) containing:

- your repository's final `note-format-spec.md` and `note-set-operations.md`
- the careless note before and after repair (two files, or the two commits)
- `findings.md` — the agent's issue list from step 1 with your comparison to the
  seeded gaps, and the findings-by-instrument table from step 5 with its
  explanation
- `reflection.md` — half a page: the S-or-R decision from step 6 with its reason,
  and one failure mode per instrument

## Completion checklist (all required for satisfactory)

- [ ] Issue list from your own planning run, compared with the three seeded gaps
- [ ] A note you wrote yourself, checked by all three instruments, with rule IDs
      cited in each report
- [ ] Findings table with at least one explained disagreement or coverage gap
- [ ] One S-or-R decision with a stated reason
- [ ] One concrete failure mode named for each instrument
- [ ] Before and after versions of the note, with the passing re-check shown

## Relation to Project 0

Your PKB specification will need the same three instruments. The Open Knowledge
Format keeps conformance light on purpose; the decision of how much to tighten
your PKB's rules, and which of those rules a script can decide, is the decision
this exercise practices on a handful of rules. The Project 0 stretch-goal validator
is `check_notes.py` at PKB scale.
