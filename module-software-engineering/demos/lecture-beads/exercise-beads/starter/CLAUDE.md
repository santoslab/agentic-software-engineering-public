# Beads exercise: tic-tac-toe rendering

This is an independent copy of the public course game's unfinished checkpoint.
Read `.specify/memory/constitution.md` and `specs/001-five-in-a-row/` before work.
The game uses a 9×9 board and five or more in a row to win.

## Agreed scope and policy

- Planning may describe the original two-player milestone. Required coding in
  this exercise is limited to board rendering, the move prompt, rejection
  messages, and two-player win/draw messages (original tasks T018/T021).
  Parsing, the menu-caller refactor, the game loop, computer play, and later
  menus remain planned work. Preserve existing engine, menu, EOF, and
  architecture tests.
- The Spec Kit artifacts govern intended behavior. Keep tasks.md and governing
  artifacts unchanged. Beads holds live status, dependencies, evidence,
  discoveries, and handoffs. Preserve original task references in work records.
- Revise an execution plan outside Beads; create detailed issues with design
  references, criteria, and dependencies; then review/refine actual records
  before implementing. Work on one issue at a time without subagents.
- Keep board drawing and the message helpers in one bounded rendering issue.
  Implement only the phase requested in the current prompt. If asked to stop,
  preserve unfinished criteria and leave the issue in_progress.
- Tests come before the code they cover; record the intended initial failure.
  Focused unit tests of the prompt and rejection/result helpers are explicitly
  authorized and required for the existing specified behavior. Use valid
  existing requirement IDs. Avoid assertions about illustrative spacing or
  unspecified details. Record the chosen helper names for future callers.
- Follow the interim rendering task: the later leave-game command and its
  prompt hint remain deferred. Do not implement them or claim their evidence.
  Import engine types only through its public API; rendering helpers return
  strings without terminal I/O.
- Record commands/results, completed and remaining criteria, next action,
  and file/commit references in the bead. Before closing, append a completion
  summary and close with an evidence-based reason. Do not claim the whole
  milestone complete after finishing rendering.
- Report a genuine specification/realization disagreement for a developer
  decision before affected implementation. Record the decision and evidence;
  do not silently change intent or weaken tests. Proposed future work must
  be labeled as a proposal.
- Local Git commits in this disposable project are authorized. Follow the
  constitution and original task notes for change-type records. Do not push,
  publish, contact other people, or access sibling handouts, prompts,
  transcripts, or checkpoints for the task. The repository has no remote.
- Read bd prime for workflow guidance; its generic remote/push guidance does
  not authorize remote operations. The supplied recorder disables automatic
  memory. Recover from project instructions, Beads, Git, and working files;
  do not use previous conversation logs as recovery input.
