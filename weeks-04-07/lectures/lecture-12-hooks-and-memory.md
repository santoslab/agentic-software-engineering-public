# Lecture 12 — Hooks and Memory: Automating the Environment

> **Unit:** weeks-04-07 · **Week 6, meeting 2 of 2** · 75 minutes
>
> **Thesis:** What must happen every time cannot depend on remembering — hooks make
> process automatic at lifecycle events, and the memory hierarchy decides where each
> fact lives so every session starts already knowing it.

## Learning objectives

After this lecture, students can:

1. Name the main hook lifecycle events and write a hook that honors the iron rule:
   a logging hook never blocks the session.
2. Read a hook's stdin contract (JSON in, exit code out) and register a hook in
   `.claude/settings.json`.
3. State the full CLAUDE.md hierarchy — user, project, per-directory — plus
   auto-memory, and place a given fact in the right layer.
4. Use permission deny-lists to isolate context, and explain a real case where
   isolation was the difference between an experiment and contamination.

## Before class

- [required] Claude Code docs: Hooks; Memory.
- [recommended] `student-materials/hooks/log-cost-on-end.ps1`, read as a spec.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–10 | Cold open: gates that depend on remembering | The pass-4 verdict from L06, one more time: *"I should have interrupted the model as soon as it skipped a verification step I intended."* Steps that depend on someone remembering to care get skipped — at production prices. A hook is remembering, automated: code that runs at a lifecycle event whether or not anyone is thinking about it. |
| 10–26 | Hook anatomy | The event list (SessionStart, SessionEnd, PreCompact, PreToolUse/PostToolUse — when each fires and what each is *for*); the contract: JSON on stdin (session id, transcript path, reason, cwd), exit code out. Then the iron rule, read from the .ps1 itself: the entire body is one try/catch and the last line is `exit 0` — **a logging hook must never block session exit.** A hook that can fail loudly at the wrong moment is worse than no hook. |
| 26–38 | Worked example: the cost hook as a program | Walk `log-cost-on-end.ps1` block by block: the pricing table (rates per million, editable in one place); collecting main + subagent transcripts; the JSONL walk; **dedupe by message id** (the subtle bug it prevents: the same message counted from two transcript files); per-model accumulation with a priced fallback for unknown models; the CSV append. This is Thursday-you's spec: Stage C asks for a behavior-preserving Python port — same columns, same never-block guarantee, cross-platform. |
| 38–48 | Demo 1 — the hook fires | Live: end a session in the instructor's Stage C repo; open `session-costs.csv`; the new row is there, nobody did anything. Then the registration that made it happen (`.claude/settings.json`, the SessionEnd entry) and one cross-platform gotcha preview: the command line that invokes Python differs by OS — the port's README must say so. |
| 48–62 | The memory hierarchy, completed | L06 gave three kinds of memory (conversation / CLAUDE.md / PKB). Today the middle layer unfolds: **user** CLAUDE.md (`~/.claude/` — your preferences, every project) → **project** (the laws: coverage gate, layering) → **per-directory** (`web/CLAUDE.md`: this layer's rules and commands — loaded when working there). Plus **auto-memory**: Claude Code curating its own notes across sessions — the agent's counterpart to your PKB, and a thing to *review*, not blindly trust. Worked example: place four facts — "I prefer uv over pip" (user), "engine at 100% branch" (project), "templates never contain game logic" (web/), "migration 7 was a two-day fight, here's why" (PKB — it's *your* lesson, portable to every future project). |
| 62–70 | Isolation by deny-list | Use a self-contained `settings.json` example that denies Read/Edit/Write for sibling attempts and course solution paths. Explain why: one stray read of an earlier implementation contaminates a rebuild-from-scratch experiment. Permissions as *context* engineering, not just safety. |
| 70–75 | Stage C hook assignment + Q&A | The port checklist: same CSV columns, never-block, works on three OSes, registered, five real rows committed. The .ps1 is the spec — where it's ambiguous, that's a spec-reading exercise too. |

## Demos

### Demo 1 — The hook fires

- **Artifacts:** instructor Stage C repo with the (reference) Python hook
  registered; `Documentation/session-costs.csv` with prior rows.
- **Setup (before class):** verify the hook fired in rehearsal *today* (pricing
  table current); keep the CSV small enough to show whole.
- **Script:** (1) trivial session ("read GATES.md, summarize") and exit; (2) open
  the CSV — new row, with cache-read dwarfing input (L06's economics, now
  self-collected); (3) show the settings.json registration; (4) delete the row,
  break the transcript path in a copy, run again — session exits cleanly anyway:
  the never-block rule, demonstrated, not asserted.
- **Expected outcome:** hooks feel like plumbing, not magic; the never-block rule
  has been *seen*.
- **Fallback:** recorded run; the settings.json and CSV read fine as slides.

## Discussion prompts

1. Sort into hook / skill / CLAUDE.md: "run gates before every commit" — and
   defend your answer. (Trick: it's a hook *if* you can make it mechanical
   (PreToolUse on git commit), a checklist line otherwise; L20 revisits this
   exact question at team scale.)
2. What belongs in auto-memory vs your PKB? Where do the two disagree, and who
   wins?
3. The fifth-pass deny-list is 60 lines for one experiment. What's the smallest
   deny-list your Project 1 repo actually needs?

## Assigned after class

- Readings (for L13):
  - [required] TypeScript docs: "TypeScript for JavaScript Programmers" (10
    minutes; do not study — the point of Stage D is learning *in* the work).
  - [required] `student-materials/fixtures/README.md` — the scenario format.
- Project: the Stage C hook is now a required element; Stage C due end of week.

## Instructor notes

- **Cut if running long:** the deny-list block (62–70) compresses to two slides
  (the file + the moral); auto-memory can shrink to its one worked-example line —
  but do not cut the hierarchy block, L20 and P2's ops-lead role build on it.
- **Risks:** the live hook demo depends on the reference port actually working —
  test it the morning of, on the presentation machine's OS. Don't let the .ps1
  walkthrough become a PowerShell tutorial; it's being read as a *spec* (what,
  not how). Students may ask why the hook recomputes cost instead of reading it —
  the answer is in the .ps1's header comment (the SessionEnd payload carries no
  cost), which is itself a lesson in reading before assuming.
- **Variants:** if PKB checkpoint 1 surfaced strong memory-placement examples,
  swap one into the 48–62 worked example.
