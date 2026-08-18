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

# Course Introduction + How LLMs Actually Work

**Agentic Software Engineering — Lecture 1**
Week 1 · Meeting 1 of 2

---

## The one idea

An LLM is a **stateless next-token predictor**.

Every agentic behavior you'll see this semester — planning, editing files, running tests, "remembering" your project — is engineered **on top of that one primitive**.

<!-- 0–10 min block: course intro. This slide frames the whole unit; return to it at the end. -->

---

<!-- _class: lead -->

# What this course is

---

## Engineering with agents — not prompting tricks

- You will build real software with an AI agent doing most of the typing
- Your job: **requirements, specifications, context, verification**
- Every claim comes with receipts: real transcripts, cost logs, and retrospectives from this course's own experiments

---

## The semester at a glance

| Weeks | Unit | Scale |
|-------|------|-------|
| 1–3 | Foundations *(you are here)* | exercises + a toy agent |
| 4–6 | Project 1 | small game (~500 LOC) |
| 7–10 | Project 2 | desktop + web finance tracker |
| 11–14 | Project 3 | full-stack web application |
| 15 | Retrospectives & presentations | — |

Running underneath: **Project 0** — a personal knowledge base you design in week 2 and grow all semester.

---

## Logistics

- 2 × 75 minutes per week — **no exams**
- Weeks 1–3: four completion-based exercises
- Projects carry the grade
- **Claude Pro subscription needed by week 2**
- All handouts distributed as PDFs; starter repo link on the course page

---

<!-- _class: standout -->

## Demo: three minutes of week 12

Claude Code adds a feature to a small game —
prompt, plan, edits, tests.

<!-- 10–15 min. Play the pre-recorded clip at 1.5x. Frame: "hold your reaction — the next three weeks explain every second of this." -->

---

<!-- _class: lead -->

# Tokens and prediction

---

## Tokens are not words

Text is split by a fixed **tokenizer** into subword units:

- common words ≈ one token
- rare words shatter into pieces
- code fragments in surprising places — indentation, identifiers

**Consequence:** code is *token-expensive* relative to its information content. (That becomes money in Lecture 6.)

<!-- 15–30 min block. Live tokenizer demo goes here. -->

---

<!-- _class: standout -->

## Demo: the tokenizer playground

One English sentence. Then one Python function from a real game.

*Which costs more tokens per line of meaning?*

---

## Generation is autoregressive

```
predict one token  →  append it  →  predict again  →  …
```

- No plan exists anywhere — only *"given everything so far, what comes next?"*
- Repeated thousands of times per response
- Coherence is a **learned property**, not a mechanism

---

## Sampling and temperature

- The model outputs a **distribution**; the system samples from it
- Temperature ≈ 0 → nearly deterministic
- Higher temperature → lower-probability tokens admitted

**Consequence:** the same prompt can produce a different function body tomorrow. *"It worked when I ran it" is not reproducibility.*

---

<!-- _class: lead -->

# Transformers at 10,000 feet

---

## The machine, in four sentences

1. Each token becomes a high-dimensional vector (**embedding**)
2. **Attention**: every position looks at every other — a soft, learned key-value lookup
3. Dozens of stacked layers refine every token in the light of all the others
4. **Scale** turned a 2017 translation paper into everything we use today

*Vaswani et al., "Attention Is All You Need" (2017)*

---

## Filling in the depth — on your own

That was deliberately all we will say in class.

- **Required:** Karpathy, *Intro to Large Language Models* (1 hr)
- **Recommended:** 3Blue1Brown, transformer + attention chapters
- **Gap-fillers:** Karpathy *Deep Dive*; the 2017 paper; InstructGPT

Mixed ML backgrounds are expected. The gap-filler track exists for exactly this — use it this week.

---

<!-- _class: lead -->

# From predicting the internet to following instructions

---

## Three training stages

1. **Pretraining** — predict the next token over an enormous corpus
   → a formidable text-completer
2. **Instruction tuning (SFT)** — curated instruction/response pairs
   → completes an instruction *with an answer*
3. **Preference training (RLHF)** — optimize toward human-preferred outputs
   → assistant behavior

<!-- 45–55 min block. If running long, compress this to the slide and move on — never cut the statelessness block that follows. -->

---

## Two engineering facts fall out

**Knowledge cutoff.**
The model has never seen your codebase, this week's library release, or anything behind your VPN. Whatever it needs, *you* must bring into the conversation.

**Hallucination is a consequence of the objective.**
Every stage rewards *plausible* text. Where plausible and true diverge, the model confidently produces the plausible thing — an API that *should* exist.

---

<!-- _class: lead -->

# Context windows and statelessness

---

## The model has no memory

**None.**

Every API call is a pure function: tokens in → distribution out.

A two-hour "conversation" = the entire history **replayed into the model on every single call**. The model isn't remembering. It is *re-reading*.

---

## The context window

- The maximum tokens a single call can carry
- Hundreds of thousands of tokens on current models — sounds infinite, isn't
- Everything competes for it: conversation, files, tool output, instructions
- Providers bill **per token, per call** — replay has a price
  *(Lecture 6: real cost data from this course's experiments)*

---

<!-- _class: standout -->

## So where does a session's memory live?

In a list of messages, maintained by ordinary software **outside the model**.

That software is called a **harness** — and it is Lecture 2.

---

## Preview: the harness, whole

![w:1050 center](diagrams/agent-loop.svg)

The "memory" is the messages list. The loop is the harness. In week 3, you build this.

<!-- 60 seconds max — this is Lecture 2's whole content in one picture; just point and move on. Diagram source: diagrams/agent-loop.mmd (Mermaid), pre-rendered to SVG by build.sh. -->

---

<!-- _class: lead -->

# Consequences

---

## Memorize this line

> An LLM is a **pure function** from a token sequence to a next-token distribution.

---

## Three consequences structure the course

1. **Context is everything.**
   The prompt is the entire program state. → Lectures 3 & 6
2. **Instructions are everything else.**
   Vague in, plausible-but-wrong out. → Lecture 4
3. **You must verify.**
   Plausible code compiles, reads well, and is wrong in ways only tests catch. → Lecture 6, and the whole semester

---

## Questions to think about

1. If the model is stateless, where does a 2-hour session's "memory" live — and who is responsible for its accuracy?
2. Which of your Copilot/ChatGPT habits does next-token prediction explain?
3. Why might a model confidently invent an API that doesn't exist?

---

## Before next lecture

- **Required:** Karpathy, *Intro to Large Language Models*
- **Recommended:** 3Blue1Brown transformer series
- **Gap-fillers:** *Deep Dive into LLMs*; Vaswani et al. §1–2; InstructGPT
- **Logistics:** Claude Pro active before week 2

*Next: an agent is an LLM in a while-loop with tools.*
