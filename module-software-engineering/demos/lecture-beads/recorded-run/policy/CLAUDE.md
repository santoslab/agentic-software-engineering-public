# Beads lecture: tic-tac-toe working copy

This is an independent copy of the public course game's foundational checkpoint.
Read `.specify/memory/constitution.md` and `specs/001-five-in-a-row/` before work.

## Agreed scope and policy

- Implement only the two-player milestone, original tasks T018–T024. The 9×9
  game needs five or more in a row. Computer play and the later US3 menus
  remain outside this milestone. Preserve the existing start-menu and EOF tests.
- The Spec Kit artifacts define intended behavior. Keep `tasks.md` unchanged
  as the original planning input; Beads is authoritative for live status,
  dependencies, evidence summaries, discoveries, and handoffs in this copy.
- Follow Yegge's workflow: revise the execution plan outside Beads, translate
  the plan into detailed epics/issues, then iteratively review and refine
  those records before implementation. Keep all original task IDs and links.
- The coding agent performs the planning review, issue creation/refinement,
  implementation, verification, and tracker updates. Work on one issue at a time.
- Write tests before implementation and record the intended initial failure.
  A genuine disagreement after implementation must be reported for a developer
  ruling; do not silently change the governing artifacts or weaken tests.
- The developer authorizes implementing the specified T018–T024 behavior and
  the required T022 menu refactor. Use II(c) for the new specified realization;
  make the menu-caller refactor a separate II(b) commit stating that no
  specified behavior changed, with the full suite verified first.
- Do not accept `4;7` or move engine range checks into the parser. New behavior
  proposals can be recorded as future work, never silently implemented here.
- Record actual commands, outcomes, remaining criteria, next action, and
  commit/diff references in Beads. In-progress work must remain in progress.
- Local Git commits in this disposable working copy are authorized. Never
  push, publish, contact other people, read sibling transcript directories,
  launch subagents, or access files outside this project for the task.
- Use `bd prime` for Beads workflow guidance. Its generic ending/push guidance
  does not authorize remote operations: this disposable repository has no remote.
- Automatic Claude memory is disabled for the recovery demonstration. Save
  durable work context in the project and Beads; do not use conversation logs.


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:1105d646 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/core-concepts/sync-concepts.md for details and anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files, validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close beads, run quality gates, commit, and push as part of session close. A current "do not commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->
