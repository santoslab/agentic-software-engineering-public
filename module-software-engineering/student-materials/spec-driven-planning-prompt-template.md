# Prompt template: planning and realizing a system from draft specifications

Use this when you have one or more draft specifications and want an agent to plan
and build a realization of them. The template's distinguishing step is the third
one: before any plan, the agent must enumerate the places where the specifications
are ambiguous, incomplete, or inconsistent, and stop for your decisions. Everything
downstream is cheaper when that step runs first.

The template accompanies Lecture 01 of the software-engineering module and is
generalized from the note-set demo's planning prompt, which is reproduced below as
the filled example.

## The template

Replace each `<slot>`. Send the moves as one prompt or as successive prompts; in
either case, do not let the agent proceed past a "wait" until you have answered.

> **1. Read.** Read `<specification file 1>`, `<specification file 2>`, ... in full.
>
> **2. State the target.** I want to realize these specifications by creating
> `<artifacts: directories, files, scaffolding>` and documenting `<operations>`,
> each with preconditions and postconditions, in `<operations file>`.
>
> **3. Find gaps before planning.** Before proposing a plan, list every place where
> the specifications are ambiguous, incomplete, or inconsistent, and anything that
> would force you to guess during implementation. Look within each document, between
> documents, and between a document and what executing it would require: walk
> through `<an operation>` step by step and say what you would have to invent.
> Number the issues and ask me to resolve them before you plan.
>
> *(Resolve the issues. For any you cannot decide now, say: "defer it; record it
> under a Deferred questions heading in `<operations file>`.")*
>
> **4. Amend with approval.** Propose the exact amendments to `<specification files>`
> as a numbered list, including a version bump and a changelog entry for each
> changed document, and wait for my approval before editing any of them.
>
> **5. Plan.** Propose the plan for `<artifacts>` and wait for my approval.
>
> **6. Realize with a verification gate.** Proceed. After each step, check the
> affected artifacts against `<specification file>` and report every finding,
> citing the rule identifier and quoting the rule text, before declaring the step
> complete. Do not repair anything until I say so.

## Filled example: the note-set demo

The demo's Segment 2 prompt, sent in plan mode, covers moves 1 through 3:

> Read note-set-conops.md and note-format-spec.md carefully. I want to set up this
> note set so it fully realizes the ConOps: create the notes directory and the
> index, and document each agent operation — add blank note, add note with initial
> content, remove note, check conformance — with preconditions and postconditions
> in a new file note-set-operations.md. Before proposing a plan, list every place
> where the two specifications are ambiguous, incomplete, or inconsistent with each
> other — anything that would force you to guess during implementation. Number the
> issues and ask me to resolve them before you plan.

After the issues are resolved, move 4:

> Good. Before any scaffolding: propose the exact amendments to
> note-format-spec.md and note-set-conops.md as a numbered list, and wait for my
> approval before editing either file.

Moves 5 and 6 are the scaffold prompt in the demo script's Segment 3. In the demo
the gap list contained at least three defects in the drafts: whether `index.md` is
a note, whether a note's H1 must equal its `title` field, and what filename a title
produces. Each became a specification amendment before any note existed.

## What to look for in the gap list

The agent's list is only as good as the categories it searched. Check that it
covered:

- **Within one document.** Two rules that constrain the same thing without stating
  their relationship (a required `title` field and a required H1, with no rule that
  they agree). A term used without a definition. A rule whose scope is unstated.
- **Between documents.** A requirement in one document that another document's
  artifact cannot satisfy (a format rule that applies to "every Markdown file" and
  an index file with no front-matter). Two names for one thing. A precondition in
  one document that no operation in another can establish.
- **Between a document and executing it.** A step the agent cannot carry out
  without inventing a convention (a title supplied, no filename rule). A
  postcondition that no step produces. A judgment clause ("preserving the user's
  meaning") with no stated arbiter.

If a category is missing from the list, ask for it by name.

## Standing rules that belong in `CLAUDE.md`

Some demands apply to every operation and should not be repeated in prompts. The
demo's `CLAUDE.md` states them once. Generalized:

1. Read `<specification files>` in full before performing any operation.
2. Never modify a specification without explicit approval. Propose changes as a
   numbered list of amendments and wait.
3. After any operation that creates, changes, or removes an artifact, check the
   affected artifacts for conformance and report the result, citing rule
   identifiers, before declaring the operation complete.
4. When a check finds violations, report them and wait for approval before
   repairing.
5. When reporting a violation, quote the violated rule's text alongside the finding.
6. Once an operations document exists, perform operations exactly as documented
   there; if the documentation is wrong or incomplete, propose an update rather
   than improvising.
7. End every completed operation with a commit whose message names the operation.

Rules 2 and 4 keep the decision about which side of a mismatch to change with you.
Rule 1 keeps the check driven by the current document rather than by the agent's
recollection of it.
