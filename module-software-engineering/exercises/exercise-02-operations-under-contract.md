# Exercise 2 — Operations Under Contract

> **Assigned:** Lecture 02 · **Due:** before Lecture 04 · **Effort:** 2–3 hours
>
> **Requires:** Claude Code; Python 3.11 or newer; git. Uses part 2 of the
> note-set demo in `../demos/lecture-01-note-specs-demo/`.
>
> **Status:** draft; instructor review required before assigning.

## Goal

Perform operations on a note set under the process documents introduced in
Lecture 02, see conformance maintained as an invariant, break it by hand and
watch the gate catch it, and account for which rule governed each step. This is
Lecture 02 applied to notes of your own. It is deliberately small; Project 0 is
the larger application.

## Setup

1. Either copy the demo's `starter-l02/` directory somewhere outside the course
   repository and make it a git repository with one initial commit
   (`demo-script-lecture-02.md`, checklist step 1), or continue your Exercise 1
   repository: copy in the files `starter-l02/` adds — `note-set-conops.md`,
   `CLAUDE.md`, `process/`, `BACKLOG.md` — and commit them as
   `part 2 start: conops 0.1 and process`.
2. Confirm that `python3 check_notes.py --all` exits 0 before you begin.
3. Read the script's final section, "Recreating this part yourself."

## Task

1. **Audit the concept of operations.** Run the demo's Segment 2 prompt in plan
   mode. Save the agent's RPT-1 gap list. Rule on every item — an amendment, or
   *no change* with a reason, or *deferred*. Approve the amendments (RPT-3) and
   commit as `conops: 0.1 -> 1.0`. Then read the script's table of five findings
   and compare: which your run found, which it missed, what else it found.
2. **Derive the operations document.** Run the Segment 3 prompt: the four
   operations with input, precondition, steps, and postcondition; the
   conventions; an audit of the new document against both governing documents
   (AUD-3). Commit.
3. **Perform three operations on notes of your own.** Not the demo's sample
   inputs. O2 with a paragraph or two you wrote about any software-engineering
   topic; O1 with a title of your choosing; O3 on the note O1 created. Each
   operation ends as DEV-7 requires: the gate passes, the agent gives a
   completion note (RPT-5), the commit names the operation. Save the three
   completion notes.
4. **Break the invariant by hand, then repair.** From the shell, not through the
   agent, rename one file in `notes/` to a name that is not the slug of its
   title, and commit as `careless rename (before)`. Run
   `python3 check_notes.py --all` and record what it reports (expect R6 and R7).
   Ask the agent to check the set and report per RPT-2 without changing
   anything. Rule — the specification is right; the file is wrong — and ask for
   the repair, the re-check, and a commit as `careless rename (after)`. Say which
   of the three kinds of change in DEV-2 the repair is, and what had to precede
   it.
5. **Defer one question.** While doing step 3, find something the operations
   document does not settle — what O2 does if the pasted text already has
   front-matter; what R7 produces from a title with no letters or digits; what
   O1 should do if the title is only whitespace. Write it to `BACKLOG.md` as
   DEV-6 requires, with the options if you see them. Do not decide it.
6. **Reflect.** Half a page: for each commit in your history, the DEV rule or
   rules it obeyed; one thing the gate could not tell you and which judgment
   clause that was; one finding the concept-of-operations audit made that an
   audit of the format specification alone could not have made.

**Optional stretch.** A requirement change of your own — for example, an
optional `source` field in the front-matter (a minor change to R2) — carried
through as an amendment (RPT-3), with the verifier, the VER-2 table, and the
existing notes updated in one commit, and every note re-checked against the new
version (VER-3).

## Deliverable

A folder (zip or repository link) containing:

- your repository, with `note-set-conops.md` at 1.0, `note-set-operations.md`,
  `notes/`, `index.md`, `BACKLOG.md`, and the full history
- `findings.md` — the RPT-1 list from step 1 with your rulings and the
  comparison with the script's five findings; the RPT-2 report from step 4
- `operations-log.md` — the three completion notes from step 3
- `reflection.md` — the half page from step 6

## Completion checklist (all required for satisfactory)

- [ ] The concept of operations audited, every finding ruled, amended to 1.0
      with a changelog entry
- [ ] The operations document derived and audited against both governing
      documents
- [ ] Three operations on your own notes, each with a named commit and a
      completion note
- [ ] The hand-made break caught by the gate, reported per RPT-2, ruled, and
      repaired, with the DEV-2 classification stated
- [ ] At least one entry in `BACKLOG.md`, written instead of decided
- [ ] A reflection that maps every commit to the rule it obeyed

## Relation to Project 0

Your PKB will have an operations document derived from its concept of
operations and its format specification, and every operation you perform on it
ends the way step 3 ends. The stretch is what a requirement change looks like at
your PKB's scale.
