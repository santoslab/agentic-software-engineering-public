# Weeks 4-7 — Project 1: The Growing Tic-Tac-Toe

**Unit thesis:** a program that grows stage by stage, where every classical SE
artifact the growth demands — spec, backlog, migration, gate checklist, port
contract, tool contract — is built *as an agent-facing artifact*. Students stop
hearing that specs matter and start living inside a repo where the spec is the only
thing holding five stages together. Solo work; 6-8 hrs/week; everything due at the
start of week 8.

Each lecture pairs one classical practice with one Claude Code capability, and the
project stage that practices both lands the same week. The course's own experiments
(the 9x9 attempts, NautilusTRX passes, lost-communities pass-1) are the case-study
corpus throughout — students build parallel work, not copies.

## The arc

| Lecture | Title | Core question | Stage served | Launches |
|---------|-------|---------------|--------------|----------|
| [07](lectures/lecture-07-project-1-kickoff-own-the-spec.md) | Project 1 Kickoff — Own the Spec | What does a spec *do* for an agent? | A | **P1 Stage A** |
| [08](lectures/lecture-08-the-growing-program.md) | The Growing Program | How does change stay governed as the program grows? | A→B | — |
| [09](lectures/lecture-09-persistence.md) | Persistence | What makes a migration a *spec* and not a script? | B | **Stage B** |
| [10](lectures/lecture-10-skills.md) | Skills: Packaging Reusable Expertise | When is a prompt worth turning into an asset? | B | Stage B skill |
| [11](lectures/lecture-11-the-web-layer.md) | The Web Layer | Which testing types become which mechanical gates? | C | **Stage C**; **PKB cp 1** |
| [12](lectures/lecture-12-hooks-and-memory.md) | Hooks and Memory | What should the environment do without being asked? | C | Stage C hook |
| [13](lectures/lecture-13-the-port.md) | The Port | Can your spec survive a language it's never met? | D | **Stage D** |
| [14](lectures/lecture-14-mcp.md) | MCP: Giving the Agent New Tools | What makes a good tool contract? | E | **Stage E** |

Project 1 is **due at the start of week 8**; Lecture 15 (weeks-08-11 unit) runs the
retrospective.

## Project 1

- [`project-1-brief.md`](project-1-brief.md) — the five stages A-E with per-stage
  required-elements checklists, cross-stage process rules, and grading.
- `student-materials/` — artifacts shipped with the brief, staged per stage:
  differential-testing fixtures (Stage D), the TypeScript scaffold (D), the original
  PowerShell cost hook to port (C), and a neutral-domain FastMCP example (E). Its
  README states what is exported to students and when.

## Files in this unit

- `lectures/lecture-07…14-*.md` — outline-level lecture plans for the instructor
  (timings, demo setup/fallbacks, cut-if-long notes; format per
  `../templates/lecture-outline-template.md`)
- `lecture-notes/lecture-07…14-*.md` — full prose lecture notes, student-facing and
  self-contained; distribute per lecture (pandoc-convertible to PDF)
- `slides/lecture-07…14-*.md` — Marp slide decks (`slides/build.sh` renders PDF +
  presentable HTML; diagrams as Mermaid sources in `slides/diagrams/`)
- `project-1-brief.md`, `student-materials/` — see above

## Standing references (live outside this unit)

- `../prompt-cheat-sheet.md`, `../technical-concepts.md` — the standing handouts
- `../weeks-01-03/student-repo/tictactoe-starter/` — the starter students receive
