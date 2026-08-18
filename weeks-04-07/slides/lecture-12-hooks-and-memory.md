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

# Hooks and Memory: Automating the Environment

**Agentic Software Engineering — Lecture 12**
Week 6 · Meeting 2 of 2 · assigns the **Stage C hook port**

---

## The one idea

What must happen **every time** cannot depend on remembering.

Gates were discipline you execute. A hook is discipline that **executes itself**.

---

## The sentence that started this course's discipline

> *"I should have interrupted the model as soon as it **skipped a verification step I intended**."* — the pass-4 retrospective

The step was intended. It was understood. It depended on someone remembering to care — and it got skipped, at production prices.

A **hook**: code that runs at a session lifecycle event. Automatically. Every time.

<!-- 0-10 min. -->

---

## Hook anatomy

| Event | Fires | Canonical use |
|---|---|---|
| `SessionStart` | New session | Prime context (surface the backlog) |
| `SessionEnd` | Session exits | Logging, transcription, **cost accounting** |
| `PreCompact` | Before compaction | Preserve what summarization loses |
| `Pre/PostToolUse` | Around tool calls | Guard or audit specific actions |

Contract: **JSON on stdin, exit code out.** A filter, in the oldest Unix sense.

---

<!-- _class: standout -->

## The iron rule

```
try {  # ... the entire program ...
} catch {  # Never block session exit on a logging failure.
}
exit 0
```

**A logging hook must never block the session.**

A cost log that misses a row: annoyance.
A cost log that can trap your session: booby trap.

---

## Reading the .ps1 as a spec — five behaviors that must survive

1. **Pricing table** — per-million rates, 4 rate types, one editable place; unknown models priced at fallback and **named** `(unknown-rate)`
2. **Transcript collection** — main + subagent transcripts
3. **The walk** — JSONL; only `message.usage` lines count; malformed lines skipped
4. **Dedupe by message id** — or sessions with subagents inflate quietly. *Test this one first*
5. **Output contract** — same CSV columns, same order (your P2 team will *merge* these files)

You are extracting a behavioral contract from a language you may not know. **Stage A's move. Tuesday's move. The move.**

<!-- 26-38 min. -->

---

<!-- _class: standout -->

## Demo: the hook fires

End a session → the CSV grows a row → nobody did anything.

Then: break it on purpose → the session **still exits cleanly**.

<!-- 38-48 min. Never-block demonstrated, not asserted. Cache-read dwarfs input: L06 economics, self-collected. -->

---

## The memory hierarchy, completed

| Layer | File | Scope |
|---|---|---|
| User | `~/.claude/CLAUDE.md` | You, every project |
| Project | `<repo>/CLAUDE.md` | The laws — every session here |
| Directory | `web/CLAUDE.md` | That layer's rules — loaded when relevant |

Same logic as prompt caching: **pay for context in proportion to how often it's needed.**

<!-- 48-62 min. -->

---

## Auto-memory vs your PKB

**Auto-memory**: Claude Code keeps its own notes across sessions.
Treat it like a junior engineer's notebook — useful, occasionally wrong, **reviewable**.

The boundary:

- Auto-memory = the agent's lessons about *this project*
- Your PKB = **your** lessons about *every project*

*"Migration 7 fought back for two days because the seeds assumed the old column"* → PKB, the moment you can phrase the general rule. No tool writes that file for you.

---

## Isolation: permissions as context engineering

A self-contained `settings.json` pattern: deny Read/Edit/Write on sibling attempts and prohibited solution paths.

Why: a rebuild-from-scratch experiment. One stray Read of pass-4 code = contamination, invisible in the output, fatal to the experiment.

Three enforcement grades:
aspiration (the brief's sentence) → discipline (you remembering) → **mechanism** (the deny-list)

**Prefer mechanism. That preference is most of this course.**

<!-- 62-70 min. Students: deny the solution paths the brief prohibits. -->

---

## The Stage C hook assignment

- `.claude/hooks/log_cost_on_end.py` — behavior-preserving per the five contract points
- Never-block; registered; **5+ real rows committed**
- Cross-platform: `pathlib`, `newline=""`, both interpreter names documented

From here to semester's end you have per-session cost data on everything you do. Lecture 22 asks you to read it like an engineer.

---

## Questions to think about

1. Hook / skill / CLAUDE.md / gate: "gates before every commit" · "transcribe at exit" · "never edit migrations" · "surface the backlog at start". One lives defensibly in two homes — which?
2. Why does the hook *recompute* cost instead of reading it? What does the .ps1's header comment teach about reading before assuming?
3. Auto-memory records "tests live in tests/unit and tests/integration." Write the PKB sentence derived from the same fact — what had to change?

---

## Before Tuesday

- [required] TypeScript docs: "TS for JavaScript Programmers" (10 min — do **not** study; the point is learning *in* the work)
- [required] `student-materials/fixtures/README.md`
- Stage C due end of week

**Tuesday: your spec meets a language it has never seen.**
