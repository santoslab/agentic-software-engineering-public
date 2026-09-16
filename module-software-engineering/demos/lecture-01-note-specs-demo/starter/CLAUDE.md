# Note set — working rules for the agent

An agent-maintained set of markdown study notes. Governing documents:
`note-set-conops.md` (what the system is for) and `note-format-spec.md`
(what a conformant note is).

## Working rules

1. Read `note-set-conops.md` and `note-format-spec.md` in full before
   performing any note operation.
2. Never modify `note-set-conops.md` or `note-format-spec.md` without
   explicit user approval. Propose spec changes as a numbered list of
   amendments and wait.
3. After any operation that creates, changes, or removes a note, check the
   affected notes for conformance and report the result — citing rule IDs —
   before declaring the operation complete.
4. When a conformance check finds violations, report them first and wait for
   the user's go-ahead before repairing anything.
5. When reporting a violation, quote the violated rule's text from
   `note-format-spec.md` alongside the finding.
6. Keep `index.md` consistent with the contents of `notes/` at all times
   (rule R6). Never edit `index.md` except as part of an operation.
7. Once `note-set-operations.md` exists, perform operations exactly as
   documented there; if its documentation is wrong or incomplete, propose an
   update rather than improvising.
8. End every completed operation with a git commit whose message names the
   operation (for example, `add-blank-note: The Mythical Man-Month`).
