# Prompt template: planning and realizing a system from specifications

Use this when you have one or more specifications and want an agent to plan and
build a realization of them. The template's distinguishing step is the third:
before any plan, the specifications are audited, and the agent stops for your
rulings. Everything after that step is cheaper for its having run.

The template accompanies Lecture 02 of the software-engineering module. Most of
its demands are also rules in the `process/` documents that the course's
starters ship; where a move has a rule, the rule is named, and the prompt can
cite it instead of repeating it.

## The template

Replace each `<slot>`. Send the moves as one prompt or as successive prompts;
in either case, do not let the agent proceed past a "wait" until you have
answered.

> **1. Read.** Read `<specification file 1>`, `<specification file 2>`, … and
> the process documents in full.
>
> **2. State the target.** I want to realize these specifications by creating
> `<artifacts>` and documenting `<operations>`, each with a precondition and a
> postcondition, in `<derived document>`.
>
> **3. Audit before planning.** Run the audit in `process/spec-audit.md` on
> each specification — and `process/conops-audit.md` on the concept of
> operations — including the walkthrough of `<an operation>` step by step.
> Report one gap list per RPT-1: numbered, placed, quoted, categorized, each
> with a recommended resolution, and stating which of the three places (AUD-6)
> you searched. Then stop and wait for my rulings.
>
> *(Rule on each item. For any you cannot decide now: "defer it; record it in
> `BACKLOG.md`.")*
>
> **4. Amend with approval.** Propose the amendments per RPT-3 — old text, new
> text, rationale citing the finding, version bump, changelog entry — and wait
> for my approval before editing any document.
>
> **5. Plan.** Propose the plan for `<artifacts>`, citing for each step the
> clauses it realizes, and wait for my approval.
>
> **6. Realize with a verification gate.** Proceed. After each step, verify the
> affected artifacts against the specification, report per RPT-2 — which
> verifier, which version, which clauses — and end each operation per DEV-7.
> Do not repair anything until I rule (RPT-4).

## Filled example: the note-set demo, part 2

The Lecture 02 demo's second segment, sent in plan mode, covers moves 1 and 3:

> Read `note-set-conops.md`, `note-format-spec.md`, and the process documents.
> Run the audits in `process/conops-audit.md` and `process/spec-audit.md` on the
> concept of operations. Check it against the format specification (AUD-3) and
> walk through each of O1, O2, and O3 (AUD-4). Report one gap list per RPT-1 and
> wait for my rulings.

After the rulings, move 4:

> Propose the amendments to `note-set-conops.md` per RPT-3 and wait for my
> approval.

Moves 2, 5, and 6 are the derivation prompt in the demo's third segment: state
the target (`note-set-operations.md`, four operations with contracts), audit the
new document against the governing ones, commit. In Lecture 01 the same moves
were made on the format specification alone; the audit found three defects
before any note existed.

## What to look for in the gap list

The agent's list is only as good as the places it searched. AUD-6 names three;
check that all three appear:

- **Within one document.** Two clauses that constrain the same thing without
  stating their relationship (a required `title` field and a required H1). A
  term used without a definition. A scope sentence the document's own rules
  contradict (every markdown file must have front-matter; the index has none).
- **Between documents.** A requirement in one document that another document's
  artifact cannot satisfy. Two names for one thing. A precondition in one
  document that no operation in another can establish.
- **Between a document and executing it.** A step the agent cannot carry out
  without inventing a convention (a title supplied, no filename rule). A
  postcondition that no step produces. A judgment clause ("preserving the
  user's meaning") with no stated verifier.

If a place is missing from the list, ask for it by name.

## Where each move lives

Some demands apply to every operation and are rules in `process/`, loaded every
session or invoked by name. The prompt need not repeat them; it can cite them.

| Move | Rule |
|---|---|
| Read the specifications and process documents first | DEV-1 |
| Audit before planning; stop for rulings | AUD-1 to AUD-7; AUDCON for a ConOps; DEV-8 from Lecture 03 |
| Amend only with approval; version and changelog | DEV-3; RPT-3 |
| In a verification failure, a person decides whether the specification or the realization changes; the decision is recorded | DEV-4; RPT-4 |
| A derived document never contradicts a governing one | DEV-5 |
| Defer rather than guess | DEV-6; `BACKLOG.md` |
| Verify after every change; report with scope; end with a named commit | VER-3, VER-4; RPT-2, RPT-5; DEV-7 |
