---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
    padding: 42px 46px;
  }
  section > *:first-child {
    margin-top: 0;
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

# Other LLMs and Harnesses

**Agentic Software Engineering — Lecture 4**
Week 2 · Meeting 2 of 2


---

## Lecture 3 recap

<style scoped>
section { font-size: 18px; }
li { margin: 0.12em 0; }
</style>

- **`/init`, and a hidden lever** — Opus found `CLAUDE_CODE_DISABLE_CLAUDE_MDS` reading the compiled binary directly, undocumented; its effect was never tested — the name implies it kills all CLAUDE.md discovery, but that was reason enough to avoid it, not confirm it
- **CLAUDE.md: derivable vs. non-derivable** — code-derivable facts vs. intent, rationale, and gotchas only a human can supply; rule of thumb: agents stumbled on the same thing multiple times? Put it in CLAUDE.md — too aggressive for one-offs, and for a *cluster* of correlated instructions (a recurring task, not a universal fact), a Skill fits better — only its one-line description is paid on every turn; the full instructions load on demand
- **Claude-specific conventions — a portability question** — global/project/folder CLAUDE.md, MEMORY.md, and similar constructs don't carry over to other harnesses — sets up today's theme
- **`/permissions`** — manages the allow/ask/deny rule set directly; the two-second habit before any live keypress feeds into it too: what does this touch, and is it reversible? `(a) always allow` is how an over-permissive setup accumulates into that rule set one keystroke at a time
- **Test coverage: 100% ≠ absence of issues** — coverage measures what code executed, not whether it does the right thing; necessary? assumed so, for good reasons — at least a high degree of coverage — but not sufficient
- **Plan mode: catch it in prose, not the diff** — the plan surfaces the agent's understanding before any file changes; a natural checkpoint to inject constraints while they're cheap; approval turns it into the working contract for execution — "cheap words before expensive edits, both cheaper than rework." *Note: also allows mixed LLM/harness usage* — plan with one model/harness, execute with another, since the plan itself is just portable text


---

## Exercise 1 discussion

<style scoped>
section { font-size: 20px; }
li { margin: 0.15em 0; }
</style>

- **Placement determines whether a reversal costs rework** — grilling *after* a plan exists invalidates work already built (a UI preview, a helper name); grilling *before* anything is committed costs nothing when the same decision reverses
- **Silent resolution vs. noticed ambiguity** — the agent quietly picked "starting player never alternates," never flagged it as a choice; surfaced two sessions later, by accident, while writing unrelated tests; "ask if unsure" doesn't fix silence — the fix is forced disclosure
- **A "definition of done" that outlives its own gaps** — 74 tests declared done survives a real bug fix *and* an unrelated tutorial before the human asks for 100% branch coverage; was the ask underspecified, or did the standard just mature?
- **Picking the best example of "vague prompt → costly follow-up work"** — 4 of 5 students picked the coverage case above (turns out: pure addition, no rework); 1 picked the silent starting-player case above (turns out: the real rework)
- **One prompt, two clauses — not a disagreement** — *"...works correctly. Provide several suggestions... and your recommendation"* — asking for options was good steering; "works correctly" set no bar; both readings are right, about different halves of the same sentence


---

## Tic-tac-toe starter experiment with different LLMs/harnesses

The task every run was given:

```
fix the AI it plays bad
```

Same six words. Same repo, same commit. Different harness, different model.

**What would count as success?**


---

## Measured results — 17 artifacts, one prompt

<style scoped>
section { font-size: 21px; }
table { font-size: 14px; }
th, td { padding: 1px 6px; }
</style>

**vs random** — 10 games vs a random-move baseline. **head-to-head** — 10 games against each of the other 16, so 160 per artifact; points: win = 1, draw = ½.

| model / artifact | harness | vs random | head-to-head |
|---|---|---|---|
| fable-max | Claude Code | 10/0/0 | **75.3%** |
| opus-max | Claude Code | 10/0/0 | 74.1% |
| sol-max | Codex | 10/0/0 | 69.7% |
| terra-max | Codex | 10/0/0 | 67.2% |
| modelA | OpenCode | 10/0/0 | 64.7% |
| haiku-max | Claude Code | 10/0/0 | 63.8% |
| grok | Grok | 10/0/0 | 62.2% |
| modelD | OpenCode | 10/0/0 | 61.6% |
| sonnet | Claude Code | 10/0/0 | 58.4% |
| luna-max | Codex | 10/0/0 | 57.5% |
| sonnet-max | Claude Code | 10/0/0 | 55.9% |
| modelF | OpenCode | 10/0/0 | 54.4% |
| modelB | OpenCode | 10/0/0 | 40.9% |
| modelC | OpenCode + local-server | 10/0/0 | 18.8% |
| modelG | OpenCode | **7/0/3** | 13.4% |
| modelH | OpenCode | 10/0/0 | 9.7% |
| starter (random) | — | *— it **is** the baseline* | 2.5% |

## **16 of 17 sweep the random baseline. The same field spreads 75% to 2%.**


---

## Every pairing, 17 artifacts

<style scoped>
table { font-size: 11px; }
th, td { padding: 1px 2px; }
td:first-child, th:first-child { text-align: left; white-space: nowrap; }
</style>

Stage 1 — 10 games per pairing. **Columns are the same 17 in the same order.** Cells are win/draw/loss from the row's point of view.

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1 fable-max** | · | 2/7/1 | 5/4/1 | 1/8/1 | 3/7/0 | 5/3/2 | 4/5/1 | 4/6/0 | 5/4/1 | 6/2/2 | 3/7/0 | 3/7/0 | 10/0/0 | 10/0/0 | 9/1/0 | 10/0/0 | 10/0/0 |
| **2 opus-max** | 1/7/2 | · | 2/5/3 | 2/7/1 | 2/8/0 | 5/2/3 | 2/8/0 | 2/8/0 | 6/4/0 | 5/3/2 | 6/4/0 | 6/3/1 | 10/0/0 | 10/0/0 | 10/0/0 | 10/0/0 | 10/0/0 |
| **3 sol-max** | 1/4/5 | 3/5/2 | · | 5/4/1 | 4/4/2 | 3/4/3 | 6/2/2 | 6/1/3 | 4/2/4 | 5/3/2 | 6/2/2 | 3/2/5 | 9/0/1 | 10/0/0 | 10/0/0 | 10/0/0 | 10/0/0 |
| **4 terra-max** | 1/8/1 | 1/7/2 | 1/4/5 | · | 1/7/2 | 4/2/4 | 3/6/1 | 3/5/2 | 4/5/1 | 5/3/2 | 3/7/0 | 5/5/0 | 7/1/2 | 10/0/0 | 9/1/0 | 10/0/0 | 10/0/0 |
| **5 modelA** | 0/7/3 | 0/8/2 | 2/4/4 | 2/7/1 | · | 1/8/1 | 1/8/1 | 1/9/0 | 2/7/1 | 3/6/1 | 2/8/0 | 4/6/0 | 7/1/2 | 10/0/0 | 8/2/0 | 10/0/0 | 10/0/0 |
| **6 haiku-max** | 2/3/5 | 3/2/5 | 3/4/3 | 4/2/4 | 1/8/1 | · | 2/7/1 | 3/5/2 | 5/4/1 | 2/4/4 | 1/8/1 | 4/5/1 | 6/2/2 | 10/0/0 | 9/0/1 | 10/0/0 | 10/0/0 |
| **7 grok** | 1/5/4 | 0/8/2 | 2/2/6 | 1/6/3 | 1/8/1 | 1/7/2 | · | 2/7/1 | 3/6/1 | 5/1/4 | 1/8/1 | 1/8/1 | 8/1/1 | 10/0/0 | 10/0/0 | 10/0/0 | 10/0/0 |
| **8 modelD** | 0/6/4 | 0/8/2 | 3/1/6 | 2/5/3 | 0/9/1 | 2/5/3 | 1/7/2 | · | 2/6/2 | 3/4/3 | 2/7/1 | 4/6/0 | 9/0/1 | 9/1/0 | 9/0/1 | 10/0/0 | 10/0/0 |
| **9 sonnet** | 1/4/5 | 0/4/6 | 4/2/4 | 1/5/4 | 1/7/2 | 1/4/5 | 1/6/3 | 2/6/2 | · | 3/5/2 | 0/10/0 | 4/6/0 | 7/0/3 | 9/1/0 | 9/1/0 | 10/0/0 | 10/0/0 |
| **10 luna-max** | 2/2/6 | 2/3/5 | 2/3/5 | 2/3/5 | 1/6/3 | 4/4/2 | 4/1/5 | 3/4/3 | 2/5/3 | · | 3/5/2 | 3/5/2 | 4/1/5 | 8/2/0 | 10/0/0 | 10/0/0 | 10/0/0 |
| **11 sonnet-max** | 0/7/3 | 0/4/6 | 2/2/6 | 0/7/3 | 0/8/2 | 1/8/1 | 1/8/1 | 1/7/2 | 0/10/0 | 2/5/3 | · | 1/9/0 | 5/1/4 | 9/1/0 | 8/2/0 | 10/0/0 | 10/0/0 |
| **12 modelF** | 0/7/3 | 1/3/6 | 5/2/3 | 0/5/5 | 0/6/4 | 1/5/4 | 1/8/1 | 0/6/4 | 0/6/4 | 2/5/3 | 0/9/1 | · | 8/0/2 | 8/2/0 | 8/2/0 | 10/0/0 | 10/0/0 |
| **13 modelB** | 0/0/10 | 0/0/10 | 1/0/9 | 2/1/7 | 2/1/7 | 2/2/6 | 1/1/8 | 1/0/9 | 3/0/7 | 5/1/4 | 4/1/5 | 2/0/8 | · | 10/0/0 | 9/0/1 | 10/0/0 | 10/0/0 |
| **14 modelC** | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/1/9 | 0/1/9 | 0/2/8 | 0/1/9 | 0/2/8 | 0/0/10 | · | 6/1/3 | 10/0/0 | 10/0/0 |
| **15 modelG** | 0/1/9 | 0/0/10 | 0/0/10 | 0/1/9 | 0/2/8 | 1/0/9 | 0/0/10 | 1/0/9 | 0/1/9 | 0/0/10 | 0/2/8 | 0/2/8 | 1/0/9 | 3/1/6 | · | 4/1/5 | 6/0/4 |
| **16 modelH** | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 5/1/4 | · | 10/0/0 |
| **17 starter** | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 0/0/10 | 4/0/6 | 0/0/10 | · |


---

## The top eight, resolved

<style scoped>
section { font-size: 22px; }
table { font-size: 16px; }
th, td { padding: 2px 5px; }
</style>

Stage 2 — **40 games per pairing**, 4x Stage 1's precision. Win/draw/loss from the row.

| | fable-max | sol-max | opus-max | terra-max | modelA | grok | haiku-max | modelD |
|---|---|---|---|---|---|---|---|---|
| **fable-max** | · | 21/13/6 | 12/27/1 | 10/27/3 | 13/26/1 | 19/15/6 | 18/17/5 | 19/20/1 |
| **sol-max** | 6/13/21 | · | 9/20/11 | 19/15/6 | 13/24/3 | 19/12/9 | 19/11/10 | 22/8/10 |
| **opus-max** | 1/27/12 | 11/20/9 | · | 8/27/5 | 7/31/2 | 12/25/3 | 16/19/5 | 12/24/4 |
| **terra-max** | 3/27/10 | 6/15/19 | 5/27/8 | · | 3/32/5 | 8/26/6 | 12/17/11 | 9/26/5 |
| **modelA** | 1/26/13 | 3/24/13 | 2/31/7 | 5/32/3 | · | 2/34/4 | 5/31/4 | 5/31/4 |
| **grok** | 6/15/19 | 9/12/19 | 3/25/12 | 6/26/8 | 4/34/2 | · | 11/21/8 | 12/20/8 |
| **haiku-max** | 5/17/18 | 10/11/19 | 5/19/16 | 11/17/12 | 4/31/5 | 8/21/11 | · | 13/15/12 |
| **modelD** | 1/20/19 | 10/8/22 | 4/24/12 | 5/26/9 | 4/31/5 | 8/20/12 | 12/15/13 | · |

**fable-max won both stages.** Beat opus 12/27/1, sol 21/13/6.


---

## Who ever beat the champion

<style scoped>
section { font-size: 22px; }
table { font-size: 12px; }
th, td { padding: 1px 5px; }
</style>

| opponent | stage 1 (10) | stage 2 (40) | W | **D** | **L** |
|---|---|---|---|---|---|
| grok | 4/5/1 | 19/15/6 | 23 | **20** | **7** |
| haiku-max | 5/3/2 | 18/17/5 | 23 | **20** | **7** |
| sol-max | 5/4/1 | 21/13/6 | 26 | **17** | **7** |
| terra-max | 1/8/1 | 10/27/3 | 11 | **35** | **4** |
| opus-max | 2/7/1 | 12/27/1 | 14 | **34** | **2** |
| luna-max | 6/2/2 | — | 6 | **2** | **2** |
| modelA | 3/7/0 | 13/26/1 | 16 | **33** | **1** |
| modelD | 4/6/0 | 19/20/1 | 23 | **26** | **1** |
| sonnet | 5/4/1 | — | 5 | **4** | **1** |
| modelF | 3/7/0 | — | 3 | **7** | **0** |
| sonnet-max | 3/7/0 | — | 3 | **7** | **0** |
| modelG | 9/1/0 | — | 9 | **1** | **0** |
| modelC | 10/0/0 | — | 10 | **0** | **0** |
| modelB | 10/0/0 | — | 10 | **0** | **0** |
| modelH | 10/0/0 | — | 10 | **0** | **0** |
| starter | 10/0/0 | — | 10 | **0** | **0** |
| **TOTAL (440 games)** | | | **202** | **206** | **32** |

**fable won by rarely losing, not by often winning:** of its 440 games it lost only **32** — but drew **206**, nearly half. **12 of its 16 opponents drew with it; the 4 that never did are the 4 it beat outright.** 9 never beat it once.


---

## Do not take the ranking seriously

<style scoped>
section { font-size: 18px; }
li { margin: 0.02em 0; }
p { margin: 0.35em 0; }
h2 { margin: 0.3em 0; }
</style>

**One vague prompt, one shot, one task, one domain.** It cannot see:

- **Human interaction** — nobody iterated or pushed back. That is most of real use.
- **Hallucination rate** — unmeasured, *including for the agent that built this.*
- **Long-context degradation** — every run was short.
- **How the model behaves** — we scored the artifact, not the conduct. **modelD went hunting for other processes' Python and text files, was refused, then tried four escalating installs and ran `csrutil status` — asking macOS whether System Integrity Protection was what blocked it — before finding a route around.** **Every run was inside a kernel sandbox — that, not the permission prompt, is what actually held.** haiku declared done while its own check hung; sol left 15 MB of pytest deps in `/tmp`, terra deleted its own.
- **And conduct is a property of the version, not the family.** **modelE**, released hours later and given the identical prompt, never probed another workspace and never tripped a prompt — but still reached for `pip --break-system-packages`, which only the sandbox stopped. Better behaved, not well behaved.
- **n = 1, on a very small codebase.** Two runs of *one* model landed **25 points apart**, a bigger gap than any adjacent tier here.

**And they nearly all did well** — from `fix the AI it plays bad` and nothing else:

- **16 of 17** beat random **10/0/0**; **15 of 17** ship a green suite.
- **Zero fouls** — not one illegal move or crash in either stage.
- **14 of 17** ran tests with no test runner installed; four wrote their own.

## **The only undeniable aspect is cost.**


---

## What each artifact cost to produce

<style scoped>
section { font-size: 18px; }
table { font-size: 12px; }
th, td { padding: 0 4px; }
p { margin: 0.35em 0; }
h2 { margin: 0.3em 0; }
</style>

*Active API time — **not** wall clock.*

| run | harness | cost | active | in (fresh/cached) | out | placing |
|---|---|---|---|---|---|---|
| fable-max | Claude Code | $5.05 | 12m 31s | 24.7K / 4.36M | 195K | **75.3%** |
| opus-max | Claude Code | $2.36 | 6m 58s | 0.1K / 4.10M | 90.7K | 74.1% |
| grok | Grok | $2.13 | 11m 07s | 173K / 1.38M | 36.7K | 62.2% |
| sol-max | Codex | $1.15* | 11m 45s | 82.6K / 0.96M | 21.7K | 69.7% |
| terra-max | Codex | $0.96* | 13m 42s | 104K / 1.40M | 38.9K | 67.2% |
| sonnet-max | Claude Code | $0.71 | 4m 45s | 0.1K / 2.61M | 59.5K | 55.9% |
| haiku-max | Claude Code | $0.13 | 1m 08s | 0.3K / 1.43M | 15.3K | 63.8% |
| luna-max | Codex | $0.07* | 8m 14s | 101K / 1.01M | 24.9K | 57.5% |
| modelA | OpenCode | *$0.010* | 2m 25s | 60.2K / 0.20M | 5.1K | 64.7% |
| modelD | OpenCode | *$0.007* | 4m 12s | 46.8K / 0.58M | 6.7K | 61.6% |
| modelE | OpenCode | **N/A** | 0m 51s | 27.8K / 0.30M | 3.5K | 62.8%† |
| modelF | OpenCode | **N/A** | 5m 48s | 79.5K / 0.39M | 8.3K | 54.4% |
| modelB | OpenCode | **N/A** | 4m 26s | 80.9K / 0.31M | 2.9K | 40.9% |
| modelG | OpenCode | **N/A** | 106m 22s | 904K / 0.96M | 10.9K | 13.4% |
| modelH | OpenCode | **N/A** | 110m 11s | 396K / 0 | 6.2K | 9.7% |

*(…)* = what the free run **would** have cost at its own paid tier. So fable is **~485x modelA's price** (for 1.16x its score). modelF, modelB, modelE and modelG and modelH are free-only — no paid SKU exists to price them against. \* derived — **Codex is the only harness with no cost field at all.** Claude Code and Grok record USD directly; OpenCode has a per-message `cost` field (0 in every run here — all free or local). † modelE arrived after the round robin; its placing is over modelD's exact 16 opponents, so the two rows compare directly.

## **$5.05 bought 75.3%. One cent would have bought 64.7%.**

---

## The harnesses, side by side

| | source | weights | runs |
|---|---|---|---|
| Claude Code | closed | closed | cloud |
| Codex | **open** | closed | cloud |
| Grok | closed | closed | cloud |
| OpenCode | **open** | **any** | cloud **or local** |

**The local run — `modelC` in the tables** — served a ~2-bit modelC with **local-server**, an inference server, and drove it with **OpenCode**. An inference server is not a harness: it runs no agent loop, no tools, no permissions. **Model, server and harness are three separate choices, and you can mix them.**

**Every "open" in that table describes the client only.** For the three cloud rows we have no idea what happens server-side — what the model is, how it is served, or what is logged. `modelC` is the one run where the whole stack was on the machine.


---

## What each one lets you see

| | permission events | reasoning |
|---|---|---|
| Grok | **logged** | discarded (empty) |
| OpenCode | not logged | **plain text, readable** |
| Codex | classifier decides | **encrypted** |
| Claude Code | not logged | discarded — *except fable, 6 of 20* |

**Nobody is good at both.**


---

## Open source ≠ transparent

<style scoped>
section { font-size: 23px; }
</style>

Codex is **open source**. Its reasoning is stored **on your disk, encrypted**.

The key is server-side. The client is a courier, not a decryptor — you can read every line of it and still not read the bytes it just wrote.

**Three separate things:**

| | you can… |
|---|---|
| open **source** | audit what the client does — Codex, OpenCode |
| open **weights** | run it yourself, offline — modelC |
| readable **data** | read what it stored about your work — OpenCode, Claude Code, **Grok** |

**Grok is the mirror image of Codex:** closed client, yet its whole store is plain text — cost, tokens, permission events. **Codex is open and unreadable; Grok is closed and readable.**

**What Claude Code keeps, it keeps in the clear. But it mostly does not keep reasoning at all** (0 of 15 haiku, 0 of 17 opus, 0 of 11 sonnet; 6 of 20 fable). Codex encrypts it; Grok and Claude discard it. **Either way you do not have it.**


---

## Compaction: what happens when context runs out

<style scoped>
section { font-size: 22px; }
li { margin: 0.1em 0; }
</style>

**Effectiveness — does the session still work afterwards?**

**Codex ≈ Grok  >  OpenCode  >  Claude Code**

*Personal experience, 120B tokens across all four. Codex and Grok are not separable — most hours on Codex, **no problems with either**. **OpenCode's and Claude Code's summaries have both caused issues.***

**Why — forced a compaction in each and read what it wrote:**

- **Grok** archives the dropped context to `segment_000.md` (3,131 lines) plus a grep-able `INDEX.md`, and tells the model to look things up in it — **I have seen it recall compacted detail**
- **Codex** keeps paginated windows with a **6 KB encrypted** carry-over — *we cannot see what is in it, or whether it summarises*
- **OpenCode** prints the summary — it leaves holes, but you can see exactly what it kept, displayed in the TUI
- **Claude Code** cut **115,751 → 4,266 tokens**: a summary plus a preserved tail. The other **111,485 are unrecoverable**

## **The ones that kept the detail held up. The ones that compressed it did not.**

---

## Poor man's context management on a budget

- Maintain a **`STATE.md`** in the project root across sessions (with the agent's help) — keep the information you want to survive a session
- **Keep it current**, and depend on version control for the changes (code and/or `STATE.md`)
- After a checkpoint — or **before compaction** in Claude Code — update it, then clear/compact the context
- **Works across harnesses and LLMs**
- We'll look at more sophisticated memory approaches later


---

## Axes worth thinking over

1. Who adjudicates a risky action — you, or a classifier acting for you?
2. Is your accumulated context **portable** or **captive**?
3. What does the harness let you *see* — permissions, reasoning, cost?
4. What does it do at compaction, and can you tell?
5. Does frontier capability matter for *this* task?

