---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
  }
  section.lead {
    background: #310066;
    color: #ffffff;
  }
  section.lead h1, section.lead h2 {
    color: #ffffff;
  }
  section.standout {
    background: #beaefc;
    color: #310066;
    text-align: center;
    font-size: 36px;
  }
  h1, h2 {
    color: #310066;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->

# Specifications, Realizations, and Conformance

**Agentic Software Engineering — Software-Engineering Module, Lecture 1**
Meeting 1 of 6 · runs the note-set demo · launches **Exercise 1**

---

## The one idea

A specification and a realization are two artifacts. **Conformance** is a relation between them; **verification** is the activity that checks it.

When the check fails, you change one side or the other, re-check, and record which side moved and why.

<!-- 0–4 min. Demo Segment 0 runs here: ls the repo (two specs, CLAUDE.md, no notes); the one-way description of spec-driven development and its weakness; promise evidence for five claims. Hook: at least one thing in these drafts is wrong. -->

---

## The example: a note set under two specifications

At t=0: a ConOps (one user, one agent, three operations), a format specification, a `CLAUDE.md` of eight working rules, and no notes.

| Rule | Requirement (v0.1, condensed) |
|---|---|
| R1 | YAML front-matter block; the opening `---` is line 1 |
| R2 | exactly two fields: `title`, `created` (ISO-8601) |
| R3 | the body begins with a level-1 heading |
| R4 | exactly one level-1 heading |
| R5 | no skipped heading levels |
| R6 | `index.md` links every note exactly once; every link resolves |

<!-- 4–12 min. This block replaces Segment 1's tour. Keep the format spec on screen while defining the terms. Note the RFC 2119 keywords, the numbered rules, and "Version: 0.1 (draft)". Show CLAUDE.md rules 2 and 4 and say when each will matter. -->

---

## Four terms

- **Specification (S)** — states, above the level of the artifact it governs, what the developer intends; fixes some properties and omits the rest
- **Realization (R)** — an artifact built to satisfy S; *implementation* when R is code; a note or a script can also be one
- **Conformance** — the relation that holds when R satisfies every property S states
- **Verification** — the activity of *trying* to confirm that R conforms to S

The participants (S, R) · the desired relation (conformance) · the act of checking it (verification)

---

## The arrangement

![w:1000 center](diagrams/spec-realization.svg)

Every file in `notes/` realizes the format specification. So will `check_notes.py`.

<!-- One S, many R: two conformant notes differ in everything S does not state. Lecture 02 takes this up. -->

---

<!-- _class: standout -->

## These drafts contain at least one defect.

Planning is where we find it.

<!-- 12–24 min. Demo Segment 2: plan mode; the gap-finding prompt; the agent's numbered issue list; resolve with the three scripted decisions; amendments as a numbered list; approve; git diff HEAD~1 -- note-format-spec.md; git log. Seeded gaps, for your eyes: A (is index.md a note? it cannot satisfy R1/R2), B (H1 vs title), D (no filename rule). -->

---

## When conformance fails: change S or change R

![w:1000 center](diagrams/conformance-repair.svg)

Segment 2 changed **S**: a scope statement (`index.md` is not a note), R3 (the H1 equals `title`; the field is authoritative), a new R7 (filename = slug of title). Version 0.1 → 1.0.0, with a changelog entry. A person decided each one.

<!-- 24–30 min. Segment 3 compressed: cat note-set-operations.md after the scaffold; three specifications now govern the repository, each abstracting something different. 30–36 min, Segment 4 live: add blank; add with content (paste no-silver-bullet-content.md); the add/remove pair only if ahead. ls notes/; git log. R6 held through every operation. -->

---

<!-- _class: standout -->

## The verification gate

A note written carelessly, in another editor, with no process watching.

<!-- 36–46 min. Demo Segment 5: paste the nonconformant Royce note over the blank one; "check it and report before fixing anything"; four findings; then "repair, re-check, finish per the working rules". -->

---

## Segment 5 changed R

| In the file | Rule | Repair |
|---|---|---|
| `created: Sept 11, 2026` | R2 | `2026-09-11` |
| H1 `The Waterfall Paper` vs `title: Royce 1970 Waterfall Paper` | R3 (as amended) | heading rewritten; the field is authoritative |
| a second H1, `# My take` | R4 | demoted to `##` |
| `##` followed directly by `####` | R5 | demoted to `###` |

The passing re-check is the completion condition. Segment 2 moved S with R still; Segment 5 moved R with S still. Both end in conformance.

---

## Three instruments for the same check

| | Person | Agent | Program (`check_notes.py`) |
|---|---|---|---|
| Cost per check | minutes | tokens | milliseconds |
| Same result on repeat | not guaranteed | not guaranteed | yes |
| Mechanical rules | yes | yes | yes |
| Judgment clauses | yes | yes | **no** |
| Usable as a gate | no | with effort | yes: exit 0 / 1 / 2 |

All three cite the same rule IDs. That is why the rules are numbered.

<!-- 46–56 min. Segment 6 from rehearsal captures: the checker's --all run; the sabotage (created: Sept 2026) and exit 1; the restore and exit 0. Then the six failure modes on the next slides. -->

---

## Instruments

![w:860 center](diagrams/verification-instruments.svg)

The operations document records which rules the script decides and which clauses remain for judgment.

---

## Six ways a verification result can be wrong

1. Checked against the wrong **version** of S (checker at 1.0.0, spec at 2.0.0: a false pass)
2. The checker is itself a **realization** of S, and can fail conformance
3. Checked from **memory** rather than from the document (working rule 1)
4. **Coverage**: a pass says nothing about clauses the instrument does not decide
5. **Attention**: the person is the instrument for everything no process checks
6. A **defective S**: before the amendments, no `index.md` could conform

A result is evidence with a scope: the instrument, the spec version, the clauses checked.

<!-- 56–62 min. Segment 7 from captures: R8 and the amended R6; version 2.0.0; the migration commit; summaries written by the agent; the ops document's table now splits R8. A 1.0.0 checker would have passed the old notes: failure mode 1. -->

---

## Five claims, and the evidence from the demo

<style scoped>table { font-size: 23px; }</style>

| Claim | Evidence |
|---|---|
| A continuously maintained document of intent | 0.1 → 1.0.0 → 2.0.0 under git, with changelogs and deferred questions |
| An abstraction of the realization | R1–R8 describe every conformant note and no particular one |
| Conformance: an invariant while both sides change | a check after every operation; S moved (Segments 2, 7); R moved (Segment 5) |
| Several specifications, mutually consistent | ConOps, format spec, operations document; the `index.md` gap was fixed in two |
| Information flows both ways | planning produced R7 and the R3 amendment; checkability tightened R2; one requirement changed four artifacts |

<!-- 62–68 min. -->

---

## Not one-way

The one-way description: intent → specification → realization, and nothing flows back. What the demo showed:

![w:900 center](diagrams/information-flow.svg)

Royce (1970), the subject of the demo's first note, made the same argument about single-pass development.

---

## A planning prompt in six moves

1. **Read** the named specification files in full
2. **State the target**: which artifacts, which operations, documented where
3. **Find gaps before planning**: number every ambiguity, omission, and inconsistency (within a document, between documents, between a document and executing it); stop and ask
4. **Amend with approval**: amendments as a numbered list; wait
5. **Plan**; wait
6. **Realize with a gate**: check affected artifacts against S and report, citing rule IDs, before declaring a step done

Full text and a filled example: `student-materials/spec-driven-planning-prompt-template.md`

<!-- 68–72 min. -->

---

## What goes in the prompt, what goes in `CLAUDE.md`

| Per task (the prompt) | Every operation (`CLAUDE.md`) |
|---|---|
| which specifications, which target | read the specifications first |
| the gap list, the amendments, the plan | never modify a specification without approval |
| what "done" means for this step | report violations before repairing; quote the rule |
| | end each operation with a named commit |

The demo's `CLAUDE.md` has eight rules and does not change during the demo. Today's specifications were human drafts; later lectures have the agent write them.

---

## Exercise 1, and Project 0

**Exercise 1** — run Segments 2–5 yourself; write one note carelessly; check it with all three instruments; report the findings by instrument, one disagreement or coverage gap, and which side should have moved. Due before Lecture 03. Deliberately small.

**Project 0** — the same structure at your scale: your PKB specification is these three documents grown up; its conformance checklist is R1–R8 grown up; the stretch-goal validator is `check_notes.py` grown up.

---

## Questions to think about

1. Name a property that specification 2.0.0 leaves unconstrained. Should it stay that way? If not, write the rule and name the instrument.
2. For the R3 finding, defend moving S instead of R. What would it cost?
3. A compiler's type checker is an algorithmic instrument. Which failure modes apply, and who verifies that verifier?

---

## Before next meeting

- Read Royce (1970) and Meyer (1992); see `reading-list.md`
- Exercise 1 is due before Lecture 03; Project 0 continues

**Next meeting:** the ConOps and the operations document as further expressions of intent; building specifications with the agent.
