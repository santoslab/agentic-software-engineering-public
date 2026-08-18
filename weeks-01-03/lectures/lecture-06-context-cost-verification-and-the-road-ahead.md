# Lecture 06 — Context, Cost, Verification, and the Road Ahead

> **Unit:** weeks-01-03 · **Week 3, meeting 2 of 2** · 75 minutes
>
> **Thesis:** You now know how agents work; the rest of the semester is about making
> their output trustworthy at increasing scale — and five principles are the rubric.

## Learning objectives

After this lecture, students can:

1. Predict what a given API turn costs and why (input/output/cache-write/cache-read),
   grounded in the toy-agent loop.
2. Choose between `/compact`, `/clear`, and a fresh session, and justify the choice.
3. Place conversation, CLAUDE.md, and their PKB in a memory taxonomy
   (ephemeral ↔ durable, per-repo ↔ cross-project).
4. Argue from evidence (NautilusTRX pass 4 vs pass 5) why autonomy without checkpoints
   fails, and name the checkpoints that fix it.
5. State the five agentic principles and map each to something they did in weeks 1–3.

## Before class

- [required] Anthropic engineering, *Effective context engineering for AI agents*
- [required] [*Agentic Development Principles* handout](../student-repo/handouts/handout-agentic-principles.md)
- [required] [NautilusTRX pass-retrospectives handout](../student-repo/handouts/handout-nautilustrx-retrospectives.md)

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–15 | Context economics, grounded | Open with a quiz the toy agent makes answerable: "turn 30 of a session — what gets sent?" (everything, again). Token pricing; prompt caching: cache-write vs cache-read, why caching makes replay affordable. Then real data: `session-costs.csv` on screen — columns InputTokens / OutputTokens / CacheWriteTokens / CacheReadTokens / EstCostUSD; first row shows CacheRead ≈ 3.7M vs Input ≈ 19K. Ask: "why is the cache-read number 190× the input number?" — they can now answer. |
| 15–30 | Context management in practice | `/compact` (summarize, lossy) vs `/clear` (reset) vs fresh session (reset + re-gather); context rot and poisoning — old wrong statements keep getting replayed; when re-contextualizing from durable artifacts beats compacting a long sick session. Per-directory CLAUDE.md as scoped injection. The L04 trajectory restated: move context out of the conversation into artifacts. |
| 30–45 | Verification & trust | The cautionary tale, from the retrospectives handout: **pass 4** — autonomous epic-driven run, single Opus session, $25–50, skipped verification, "well below par" — vs **pass 5** — checkpointed waves, Red→Green→Coverage→Self-review→Checkoff→Commit, best end product (8/10). The lesson is not "autonomy bad" — it's *autonomy without embedded checkpoints outruns trust*. Demonstrate a mechanical coverage gate with the bundled starter's pytest coverage report. |
| 45–58 | The five agentic principles | Walk the handout: Spec-Driven Development; The Cycle of Development; Project Context Management (CLAUDE.md); Requirement Elicitation; Verification. For each: where weeks 1–3 already practiced it (Ex. 1 saw its absence; L04/Project 0 practiced elicitation and specs; Ex. 2 practiced context management; Ex. 4 built the thing being verified). **These five are the semester's grading lens for Projects 1–3.** |
| 58–65 | Memory taxonomy | Conversation = ephemeral, expensive, replayed. CLAUDE.md = durable, per-repo, injected. **Your PKB = durable, cross-project, yours** — the externalized memory that survives every `/clear` and every project; OKF's `log.md` is its history, `index.md` its compaction. Same engineering problem at three scales. |
| 65–72 | The road ahead | Use the self-contained process excerpt in the companion notes: Brief → Gather → Develop → Verify → Report, mechanical gates, "the todo list is the enforcement mechanism" — *this is week-11 you.* Explain which advanced tools unlock when (hooks/subagents ~W9, MCP ~W12). |
| 72–75 | Close | Ex. 4 checkpoint Q&A; Project 0 kickoff due now-ish; Project 1 brief drops next meeting. |

## Demos

### Demo 1 — Live context/cost inspection

- **Artifacts:** a deliberately long-running Claude Code session (prepared before
  class — e.g., the L03 demo session continued).
- **Script:** `/context` — read the composition; `/cost` — read the spend; `/compact` —
  show what survives; discuss what was lost.
- **Fallback:** screenshots from the prepared session.

### Demo 2 — session-costs.csv in a spreadsheet

- **Artifacts:** the five-column cost row reproduced in the companion notes and the
  bundled retrospective's $25–50 pass-four account.
- **Setup:** put the reproduced row on a slide with the four token columns and
  EstCostUSD visible.
- **Script:** quiz first (predict the ratio), reveal second; ask what makes a
  never-cleared session expensive.
- **Fallback:** static; no failure mode.

### Demo 3 — Coverage report as a gate

- **Artifacts:** the [bundled tic-tac-toe starter](../student-repo/tictactoe-starter/).
- **Setup (instructor prep, day before):** install its development requirements and
  run `pytest --cov=game --cov-branch --cov-report=html`; confirm the report opens.
- **Script:** open the report; distinguish statement and branch coverage; show how
  the same command can become a non-negotiable project gate.
- **Fallback:** screenshots of the report.

## Discussion prompts

1. Pass 4 was cheap per feature and disappointing overall — where exactly did trust
   break? Which single checkpoint would have caught it earliest?
2. Which of the five principles would you drop for a 50-line script? For a 50-KLOC app?
   (There is no right answer — the point is that discipline scales with stakes.)
3. Your PKB and CLAUDE.md are both "memory" — when would you write a fact into one vs
   the other?

## Assigned after class

- Readings: none new — finish Ex. 4 and the Project 0 kickoff.
- Next meeting: **Project 1 brief** (week 4; tic-tac-toe-scale build applying all five
  principles).

## Instructor notes

- **Cut if running long:** the memory taxonomy (58–65) folds into two sentences inside
  the road-ahead block; never cut pass-4-vs-pass-5 — it is the emotional core of the
  unit.
- **Risks:** rehearse the coverage command in a clean virtual environment; the quiz
  format in the opening block only works if Ex. 4 is substantially done —
  if the room hasn't built the loop yet, switch the quiz to a walkthrough.
- **Variants:** if student session-cost data exists (volunteers sharing `/cost`
  output from Ex. 2), use it alongside the NautilusTRX CSV — local data always beats
  imported data.
