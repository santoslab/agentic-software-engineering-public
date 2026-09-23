# Exercise 1 — Conformance Three Ways

> **Assigned:** Lecture 01 · **Due:** before Lecture 03 · **Effort:** 2–3 hours
>
> **Requires:** Claude Code; Python 3.11 or newer; git. Uses part 1 of the
> note-set demo in `../demos/lecture-01-note-specs-demo/`.
>
> **Status:** draft; instructor review required before assigning.

## Goal

Run the same conformance check with the three kinds of verifier — yourself, an
agent, and a program — on a note you wrote, and account for where they agree,
where they differ, and how each could have been wrong. This is Lecture 01's
verification section applied to your own artifact. It is deliberately small:
Project 0 is starting at the same time and is the larger application of the
same ideas.

## Setup

1. Copy the demo's `starter/` directory somewhere outside the course repository
   and make it a git repository with one initial commit (the checklist in
   `demo-script-lecture-01.md`, step 1).
2. Do **not** read `sample-inputs/royce-note-filled-nonconformant.md` until
   step 5 of the task. The exercise depends on your own note, not the demo's.
3. Read the demo script's final section, "Recreating this part yourself."

## Task

1. **Audit.** Run the demo's Segment 2 in your own Claude Code session: the
   audit prompt in plan mode, your own rulings, the amendments, the commit. Save
   the agent's RPT-1 gap list. Then read the script's section "What the starter
   contains, and what is seeded in it" and compare your list with the three
   seeded findings: which your run found, which it missed, what else it found.
2. **Write a note carelessly.** In a plain-text editor, write a note of your own
   on any software-engineering topic, 20–40 lines, without consulting the
   specification. Save it into `notes/` under a filename of your choosing and
   add an index entry by hand. Commit it as `careless note (before)`.
3. **Check it three ways.**
   - *Human verifier:* read `note-format-spec.md` at its current version and
     list every violation you can find in your note, citing rule identifiers.
   - *Agent verifier:* ask the agent to check the note and report per RPT-2
     before changing anything (Segment 3's prompt). Save the report.
   - *Algorithmic verifier:* either have the agent write `check_notes.py` with
     Segment 4's prompt and run it, or run the demo's
     `starter-l02/check_notes.py`, which implements specification 1.0.0. If your
     rulings in step 1 differed from the demo's (a different filename rule, for
     instance), the reference verifier will report against a specification that
     is not yours; keep those lines in your table and explain them in step 5.
4. **Report with scope.** For each of the three results, write the three RPT-2
   scope lines: which verifier (and version), which specification version,
   which clauses were checked and which were not.
5. **Compare.** Build a table with one row per finding and one column per
   verifier (found / not found / not decided). Explain at least one row where
   the verifiers disagree or where one could not decide the clause. Now read
   `sample-inputs/royce-note-filled-nonconformant.md` and the four-violation
   table in the script's Segment 3; note any violation it seeded that your note
   did not contain.
6. **Decide and reflect.** For one finding, state whether the specification or
   the note should change, and why. For each kind of verifier, name one concrete
   way its result on your note could have been invalid (Lecture 01 lists six
   ways; pick the ones that apply).
7. **Repair.** Rule; have the agent repair the note; confirm the re-check
   passes; commit as `careless note (after)`.

## Deliverable

A folder (zip or repository link) containing:

- your repository's final `note-format-spec.md`
- the careless note before and after repair (two files, or the two commits)
- `findings.md` — the agent's RPT-1 list from step 1 with your comparison to
  the seeded findings; the three RPT-2 scope statements from step 4; the
  findings-by-verifier table from step 5 with its explanation
- `reflection.md` — half a page: the S-or-R decision from step 6 with its
  reason, and one failure mode per kind of verifier

## Completion checklist (all required for satisfactory)

- [ ] Gap list from your own audit, compared with the three seeded findings
- [ ] A note you wrote yourself, checked by all three kinds of verifier, with
      rule identifiers cited in each report
- [ ] RPT-2 scope lines for each of the three results
- [ ] Findings table with at least one explained disagreement or undecided clause
- [ ] One S-or-R decision with a stated reason
- [ ] One concrete failure mode named for each kind of verifier
- [ ] Before and after versions of the note, with the passing re-check shown

## Relation to Project 0

Your PKB specification will need the same three kinds of verifier. The Open
Knowledge Format keeps conformance light on purpose; the decision of how much to
tighten your PKB's rules, and which of those rules a program can decide, is the
decision this exercise practices on a handful of rules. The Project 0
stretch-goal validator is `check_notes.py` at PKB scale.
