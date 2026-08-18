# Lecture 04 — Prompting + Spec-Driven Development

> **Unit:** weeks-01-03 · **Week 2, meeting 2 of 2** · 75 minutes
>
> **Thesis:** The two 9×9 attempts in the course repo are the same task with different
> discipline — requirements and specs, not prompt cleverness, separate the outcomes.

## Learning objectives

After this lecture, students can:

1. Apply the five cheat-sheet principles to rewrite a weak development prompt.
2. Run a requirement-elicitation session (the grill-me pattern) before building.
3. Distinguish a ConOps (operational, user-perspective) from a SPECS document
   (behavioral contract), and say what each is *for*.
4. Explain why a good spec is language-portable and a good prompt is not.
5. Explain why development prompts *shrink* as project artifacts mature.

## Before class

- [required] [`prompt-cheat-sheet.md`](../../prompt-cheat-sheet.md)
- [required] Anthropic, *Claude Code Best Practices*
- [recommended] Claude Code docs: permission modes, memory, plan mode
- Ex. 1 due today — the transcript vocabulary it built is assumed from here on.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–10 | Cold open: a tale of two attempts | Both 9by9 runs branch from the same 3×3 game. Attempt1, Session 12: all requirements delivered in **one prose paragraph** ("scale to 9×9… two step process where a player first picks a column then a row…") — docs revised in passing, then code. Note the drift: that prompt says column-then-row; the shipped SPECS says row-then-column. Attempt2, Session 14: starts over, declares the existing SPECS "sub-par," and runs `/grill-me` to rewrite it **before any code** — "so we don't have to change it in the future." Session 16 goes further: an implementation-independent ConOps, also by elicitation. Hold the payoff (9by9_Java) for minute 45. |
| 10–30 | The five principles | Walk the handout (`prompt-cheat-sheet.md`), each principle with its base-vs-better pair and a 60-second live rewrite on 3by3: specific instructions; spec-driven development; give Claude the tools to check itself; promote positive behaviors (don't just restrict); point to existing patterns. Thread back: L03's vague-prompt failure was principle 1 violated. |
| 30–45 | Requirement elicitation | The grill-me skill is 13 lines — "a methodology in a paragraph": make the agent interview *you* until the decision tree is resolved. Read an excerpt from Attempt2 Session 16 (the ConOps interview). The principle: **the agent can only be as right as your requirements**; elicitation converts unknown-unknowns into decisions before they become rework. |
| 45–58 | ConOps vs SPECS — and the punchline | Use the implementation-independent ConOps summary and shipped-spec excerpt in [Handout B](../student-repo/handouts/handout-B-9by9-excerpts.md), then explain the documented Java-port outcome: same ConOps, new language, Maven + JaCoCo, 100% branch coverage. **Specs are portable; prompts are not.** The ConOps outlived the codebase. |
| 58–68 | Prompt evolution at scale | Use the prompt excerpts in the [NautilusTRX retrospectives](../student-repo/handouts/handout-nautilustrx-retrospectives.md): first-pass development prompts carried review and process instructions inline; later prompts named only the wave and elicitation step. The prompt *shrank* as ConOps, CLAUDE.md, and development plans grew — context moved from the prompt into durable artifacts. |
| 68–75 | Project 0 kickoff | Everything today applies to a non-code artifact you'll keep all semester: your personal knowledge base. Tour the OKF spec in 3 minutes (frontmatter with `type`; reserved `index.md`/`log.md`; bundle-relative links; permissive conformance; Obsidian-viewable). Kickoff = grill-me your own KB design → 1-page spec → Claude scaffolds it. Spec-driven development where the "code" is markdown. |

## Demos

### Demo 1 — Side-by-side transcript excerpts

- **Artifacts:** [Handout B](../student-repo/handouts/handout-B-9by9-excerpts.md):
  Attempt 1 Session 12, Attempt 2 Sessions 14 and 16, and the shipped-spec excerpt.
- **Setup:** pre-extract the excerpts (2–3 exchanges each) onto slides — do not scroll
  a 150 KB file live.
- **Script:** read Attempt1's Session 12 opening prompt aloud, then show the
  row/column-order drift against the shipped-spec excerpt ("who caught this, and
  when?"); contrast with Session 14's opening ("sub-par SPECS… grill-me… so we don't
  have to change it in the future") and Session 16's interview rhythm.
- **Expected outcome:** discipline differences are visible in the *transcript shape*,
  before any code is compared.
- **Fallback:** static slides (this demo is slides-first by design).

### Demo 2 — CONOPS/SPECS/Java walkthrough

- **Artifacts:** Handout B's implementation-independent ConOps summary and
  shipped-spec excerpt, plus the portability explanation in the companion notes.
- **Setup:** highlight that the ConOps summary names no implementation language.
- **Script:** (1) ConOps — "could a non-programmer confirm this describes the game
  they want?"; (2) spec — find one testable behavioral clause; (3) explain the
  documented Java reuse; (4) contrast a portable requirement with a language-specific
  coverage gate.
- **Expected outcome:** the artifact hierarchy (ConOps → spec → code+tests) and its
  portability click.
- **Fallback:** static; no live agent needed.

### Demo 3 — OKF in three minutes

- **Artifacts:** the OKF SPEC.md (GitHub, have it cached/offline too); the worked
  example bundle `../student-repo/pkb-example/`.
- **Script:** frontmatter of one concept note (`type` required, rest recommended);
  `index.md` as progressive disclosure; a bundle-relative link; "broken links are
  allowed — they mark knowledge not yet written."
- **Expected outcome:** OKF understood as *just markdown with light rules* — no
  toolchain fear.
- **Fallback:** the local `pkb-example/` copy covers a GitHub outage.

## Discussion prompts

1. The ConOps never mentions Python — what exactly does that buy you? (It bought the
   Java port.)
2. When is grill-me a waste of time? (Small, reversible, well-understood tasks —
   discipline scales with stakes.)
3. Why did the NautilusTRX development prompt get *shorter* pass over pass?

## Assigned after class

- Readings (for L05):
  - [required] Anthropic API docs: Messages API + Tool use (this time in depth — Ex. 4
    is built on these).
  - [required] Thorsten Ball, *How to Build an Agent* (ampcode.com, Apr 2025) — a
    ~300-line agent in Go; students build the Python equivalent.
  - [recommended] re-read *Building Effective Agents*, the "agents" section.
  - [recommended] Anthropic, *Writing effective tools for agents — with agents*
    (engineering blog).
- Project: **Project 0 — PKB kickoff**
  (`../exercises/project-0-pkb-kickoff.md`), kickoff due end of week 3.
- Reminder: Ex. 2 due before Lecture 05.

## Instructor notes

- **Cut if running long:** Demo 2 can drop the SPECS.md tab (ConOps → Java is the
  irreducible pair); prompt-evolution (58–68) compresses to the two quoted prompts on
  one slide.
- **Risks:** use Handout B's B1, B2a, and B2b headings as stable anchors (the transcripts
  share Sessions 1–13 as carried-forward history — don't present them as independent
  runs of that early work). Don't overstate Attempt1 as a failure — it *worked*, and
  its prompt even asked for docs first; the difference is elicitation depth and the
  spec's authority, and the do-over itself is the evidence of what that cost.
- **Variants:** if Ex. 1 critiques were strong, open by quoting two anonymized student
  observations instead of the instructor's framing.
