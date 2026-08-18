# Lecture 01 — Course Intro + How LLMs Actually Work

> **Unit:** weeks-01-03 · **Week 1, meeting 1 of 2** · 75 minutes
>
> **Thesis:** An LLM is a stateless next-token predictor; every agentic behavior you
> will see this semester is engineered on top of that one primitive.

## Learning objectives

After this lecture, students can:

1. Explain tokenization and next-token prediction, and why code tokenizes differently
   than prose.
2. Distinguish pretraining, instruction tuning, and RLHF at a conceptual level (what
   each stage buys, no math).
3. Define "context window" and explain why the prompt is the *entire* program state of
   a stateless model.
4. State three engineering consequences of the above: hallucination, nondeterminism,
   and the verification burden.

## Before class

None (first meeting). Publish the reading list and Claude Pro purchase instructions
before the semester starts so week-2 logistics don't slip.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–10 | Course intro | What agentic SWE is and is not (not "prompt tips" — an engineering discipline). Semester arc: introduce the three named case studies — Tic-Tac-Toe, NautilusTRX, and lost-communities — and point to the bundled excerpts used in this public edition. Logistics: 2×75, no exams, 3 exercises + Project 0 (tease only) + three projects; Claude Pro needed by week 2. |
| 10–15 | Hook demo | 3-minute clip: Claude Code adding a feature to the 3×3 tic-tac-toe end-to-end. Frame: "by week 12 you do this on a full-stack web app — with discipline. First: what is actually happening here?" |
| 15–30 | Tokens & prediction | Live tokenizer playground: same sentence, then Python code (indentation, identifiers split oddly). Autoregressive generation: one token at a time, each conditioned on everything so far. Sampling and temperature: why the same prompt yields different code. |
| 30–45 | Transformers at 10,000 ft | Embeddings (tokens → vectors); attention as soft key-value lookup — ONE diagram, no equations; stacked layers + scale = the whole trick. Anchor: Vaswani et al. 2017 as the historical origin. Explicitly defer depth to the self-study videos (Karpathy, 3Blue1Brown) — say out loud that mixed ML backgrounds are expected and the gap-filler track exists for exactly this. |
| 45–55 | Training vs inference | Pretraining objective (predict the internet) → SFT (follow instructions) → RLHF (prefer helpful outputs): why base models complete text but assistants answer questions. Knowledge cutoff. Hallucination as a *consequence of the objective* — the model is rewarded for plausible, not true. |
| 55–65 | Context windows & statelessness | Window sizes and per-token pricing (one slide of current numbers, dated). The model has **no memory**: every API call replays the whole conversation. "Where does a 2-hour session's memory live?" — set up as the cliffhanger for L02. |
| 65–72 | Consequences for engineers | LLM = pure function `tokens → next-token distribution`. Therefore: (a) context is everything → L03/L06; (b) instructions are everything → L04; (c) output is plausible-by-construction, so **you must verify** → L06 and the whole semester. |
| 72–75 | Wrap | Assign readings (below); tease Ex. 1: "next lecture you'll see the loop; then you'll read a real 7-session transcript and grade the human." |

## Demos

### Demo 1 — Tokenizer playground

- **Artifacts:** a browser tokenizer (e.g., platform tokenizer demo page); prepared
  snippets: an English sentence, a Python function from
  [the bundled starter's `game.py`](../student-repo/tictactoe-starter/game.py).
- **Setup:** verify the playground URL works on the podium machine; keep snippets in a
  text file.
- **Script:** (1) tokenize prose — point at subword splits; (2) tokenize the Python
  function — point at whitespace/identifier fragmentation; (3) ask: "which costs more
  tokens per line of meaning?"
- **Expected outcome:** students see tokens are not words and code is token-expensive.
- **Fallback:** static screenshots of both tokenizations.

[Tokenizer to use for demo](https://huggingface.co/spaces/Xenova/the-tokenizer-playground)

### Demo 2 — Hook clip: Claude Code on 3×3

- **Artifacts:** [the bundled tic-tac-toe starter](../student-repo/tictactoe-starter/)
  (any small feature; e.g., improve the board rendering).
- **Setup:** pre-record the 3-minute clip; do NOT do this live in lecture 1 (permission
  prompts and setup friction eat time before students have any model to hang them on).
- **Script:** play clip at 1.5×; narrate: prompt → plan → edits → tests run.
- **Expected outcome:** curiosity, not comprehension — comprehension is L02–L05's job.
- **Fallback:** none needed (it's a recording).

## Discussion prompts

1. If the model is stateless, where does a 2-hour coding session's "memory" live?
2. Which of your existing Copilot/ChatGPT habits does next-token prediction explain?
3. Why might a model confidently invent an API that doesn't exist?

## Assigned after class

- Readings (for L02):
  - [required] Karpathy, *Intro to Large Language Models* (YouTube, ~1 h) — the
    designated gap-filler; tell students with ML background they may skim.
  - [recommended] 3Blue1Brown, *But what is a GPT?* and *Attention in Transformers*
    (YouTube) — for the visually inclined.
  - [gap-filler] Karpathy, *Deep Dive into LLMs like ChatGPT*; Vaswani et al.,
    *Attention Is All You Need* (skim §1–2); Ouyang et al. 2022 (InstructGPT) for RLHF.
- Exercise: none yet (Ex. 1 launches at L02).
- Logistics: reminder — Claude Pro subscription active before week 2.

## Instructor notes

- **Cut if running long:** compress "Training vs inference" (45–55) to five minutes —
  the SFT/RLHF distinction can live in the readings; do not cut statelessness (55–65),
  it is the spine of the unit.
- **Risks:** mixed ML backgrounds — name the gap-filler track explicitly so the
  ML-literate don't check out and the rest don't panic. Keep transformers to ONE
  diagram; every equation added here is a minute stolen from statelessness.
- **Variants:** if the room has laptops, students can tokenize their own snippets during
  Demo 1 (adds ~5 min; take it from the 30–45 block).
