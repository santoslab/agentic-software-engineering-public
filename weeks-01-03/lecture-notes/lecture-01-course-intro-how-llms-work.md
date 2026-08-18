# Lecture 1 Notes — Course Introduction + How LLMs Actually Work

> Agentic Software Engineering · Week 1, first meeting
>
> **The one idea:** an LLM is a stateless next-token predictor. Every agentic behavior
> you will see this semester — planning, editing files, running tests, "remembering"
> your project — is engineered on top of that single primitive. If you keep this one
> fact in view, nothing an agent does this semester will look like magic.

## 1. What this course is

This is a course about *engineering with agents*, not about prompting tricks. Over
fifteen weeks you will go from understanding what a language model actually computes to
building real software — first a small game built several different ways, then a larger project that integrates a number of different technologies — with an AI agent doing most of the
coding and you doing the things that still matter: eliciting requirements, planning development, 
writing specifications, managing what the agent knows, and verifying what it produces.

The course materials grew out of a set of real experiments: the same projects you will
build were built several times over, with different levels of discipline, and the
transcripts, specifications, cost logs, and retrospectives from those experiments are
your case studies. When we claim that a technique works, we will generally show you the
session where it worked — and often the earlier session where its absence hurt.

The shape of the semester:

- **Weeks 1–3 (now):** foundations. How LLMs work, how an agent is built out of one,
  how to drive Claude Code deliberately, and why specifications and verification
  dominate cleverness. Four small exercises, including building your own working agent
  in about 200 lines of Python.
- **Weeks 4–6:** Project 1, a complete small build (tic-tac-toe scale) done with full
  discipline.
- **Weeks 7–10:** Project 2, a medium application; new tools (hooks, subagents) arrive
  as the project demands them.
- **Weeks 11–14:** Project 3, a large full-stack application with milestone gating.
- **Week 15:** retrospectives and presentations.

Running underneath all of it is **Project 0**: a personal knowledge base on agentic
software engineering that you design in week 2, seed in week 3, and grow all semester.
More on that when we reach Lecture 4.

There are no exams. Weeks 1–3 exercises are completion-based; the projects carry the
grade. You will need a Claude Pro subscription by the start of week 2.

In class we watch a three-minute clip of Claude Code adding a feature to a small
command-line game: one English prompt, then the agent reads the code, proposes a plan,
edits three files, runs the test suite, and reports back. Hold on to whatever reaction
you have to that clip. The next three weeks explain every second of it.

## 2. Tokens and next-token prediction

A large language model does exactly one thing: given a sequence of **tokens**, it
outputs a probability distribution over what the next token might be. Everything else
is scaffolding around that operation.

Watch it happen across a few steps. Suppose the input so far is the start of a tiny
Python function (probabilities here are illustrative — real values vary by model):

**Step 1.** Input: `def add(a, b):\n    return a` — the model's top candidates for
the next token:

| candidate | probability |
|-----------|------------:|
| ` +`      | 0.91 |
| ` *`      | 0.03 |
| ` if`     | 0.02 |
| ` ,`      | 0.01 |
| …everything else | 0.03 |

**Step 2.** The system picks ` +`, appends it, and asks again. Input is now
`…return a +` — and the distribution has *sharpened*, because almost nothing but `b`
makes sense here:

| candidate | probability |
|-----------|------------:|
| ` b`      | 0.98 |
| ` 1`      | 0.01 |
| …everything else | 0.01 |

**Step 3.** Append ` b`, ask again. Now the function is complete, and the distribution
*flattens* — many continuations are plausible (end the text, a blank line, a new `def`,
a comment):

| candidate | probability |
|-----------|------------:|
| *end of turn* | 0.55 |
| `\n\n`    | 0.25 |
| `\ndef`   | 0.08 |
| ` #`      | 0.04 |
| …everything else | 0.08 |

Notice the shape of the machine: it never "writes a function." It answers *"what comes
next?"* over and over, and the distribution is sometimes nearly certain (step 2),
sometimes genuinely open (step 3). Both regimes matter for engineering: the open ones
are where identical prompts diverge (see sampling, below).

**Tokens are not words.** Text is split by a fixed tokenizer into subword units.
Common words are often one token; rare words shatter into pieces; whitespace and
punctuation have their own conventions. Try a tokenizer playground on a sentence of
prose and then on a function from a Python file and you will notice two things: code
fragments in surprising places (identifiers split mid-name, indentation consumed
token by token), and code is *token-expensive* relative to its information content.
That expense will show up as real money in Lecture 6.

Concretely, a typical tokenizer splits ordinary prose almost word-by-word:

> `The agent reads the file.` → `The` · ` agent` · ` reads` · ` the` · ` file` · `.`
> — six tokens for six words.

but shatters anything rarer:

> `tokenization` → `token` · `ization` — a rare word becomes two familiar pieces
>
> `check_winner` → `check` · `_win` · `ner` — an identifier splits mid-name, in places
> no human would choose

and code multiplies the count. Two innocent-looking lines:

```python
def check_winner(self):
    for row in self.board:
```

come out to roughly 15 tokens — the `def`, each name fragment, the punctuation, and
the *indentation itself* all spend budget. A rule of thumb you can verify in the
playground: prose runs ~¾ of a token per word; code often costs several tokens per
"word" of meaning. (Exact splits differ by tokenizer — check these in the playground
demo rather than memorizing them.)

**Generation is autoregressive.** 
An autoregressive model is a system that predicts the next item in a sequence by using 
the past items in that same sequence. The word "auto" means self, and "regressive" means 
predicting a value based on prior values. It treats prior outputs as inputs to forecast 
the next step.

Thus, to produce a response, the model predicts one token,
appends it to the sequence, and predicts again — thousands of times. There is no plan
sitting anywhere; there is only "given everything so far, what comes next," repeated.
The coherence you observe is a property the prediction learned, not a mechanism the
software provides.

**Sampling is why outputs differ.** The model outputs a *distribution*; the system
then samples from it.  The set up involves a technical concept called "temperature".
A temperature setting near zero makes the sampling nearly
greedy and outputs nearly deterministic; higher temperatures admit lower-probability
tokens. This is one reason the same prompt can produce a different function body on
Tuesday than it did on Monday — a fact your engineering process has to absorb, because
"it worked when I ran it" is not reproducibility.

Here is how the same prompt diverges. Ask twice for *"a function that reverses a
string"*, and suppose that at the naming step the distribution looks like:

| candidate | probability |
|-----------|------------:|
| `reversed_str` | 0.45 |
| `result`       | 0.30 |
| `out`          | 0.15 |
| …everything else | 0.10 |

At temperature 0 the system takes the top candidate every time — `reversed_str`,
deterministically, on Monday and on Tuesday. At a moderate temperature it *samples*:
run 1 happens to draw `reversed_str`; run 2 draws `result`. Now watch the divergence
compound — the sampled token becomes part of the input for every later step, so each
run stays consistent *with itself* while differing from the other:

```python
# Run 1                                # Run 2
def reverse(s):                        def reverse(s):
    reversed_str = ""                      result = []
    for ch in s:                           for ch in reversed(s):
        reversed_str = ch + reversed_str       result.append(ch)
    return reversed_str                    return "".join(result)
```

One early sample — a *name* — and the two runs commit to different loop shapes and
different data structures downstream. Both are correct; neither is "the" output. This
is why "regenerate" gives you a genuinely different answer, and why an agentic
workflow needs tests rather than the memory of it having worked once.

Low Temperature (Near 0)
- How it works: The model always picks the choice with the highest math score.
- Result: The output is steady, focused, and nearly the same every time you ask.
- Best use: Math, code, data extraction, or factual lookup.

High TemperatureHow it works: 
- The math scores flatten out, giving weaker or unusual word choices a higher chance of being picked.
- Result: The output is more varied, unique, and creative.
- Risk: If set too high, the model loses focus, drifts off topic, or makes things up (hallucinates) because it chases strange word combinations

In short, a temperature of near 0 yields output that is more deterministic but less creative, where as a higher temperature will result in a LLM response that is more "creative" but also more prone to hallucinations.



## 3. Transformers at 10,000 feet

You do not need the mathematics of transformers for this course, but you need the
shape of the machine, so here it is in four sentences.

Each token is mapped to a high-dimensional vector (an **embedding**). **Attention**
lets every position in the sequence look at every other position and pull in
information from the ones that matter — think of it as a soft, learned key-value
lookup rather than anything sequential. A transformer stacks dozens of such layers,
each refining the representation of every token in the light of all the others.
Scale — more layers, more data, more compute — turned this architecture from a 2017
machine-translation paper ("Attention Is All You Need," Vaswani et al.) into the
engine of everything we use in this course.

Three quick illustrations to hang those terms on:

**Embeddings: meaning as geometry.** Each token's vector is a point in a space where
*distance tracks meaning*: `file` sits near `document` and far from `banana`; `read`
and `write` sit near each other and near `file`. Directions can carry meaning too —
the classic party trick from early word-vector research is that the arithmetic
`king - man + woman` lands approximately on `queen`. The
model doesn't look words up in a dictionary; it computes with their positions.

**Attention: who should I look at?** Take the sentence
`The function returns None because it fails.` When the model processes `it`, something
must connect `it` back to `function` — that is attention. The token `it` issues a
*query* ("I'm a pronoun; who's my referent?"), every earlier token offers a *key*
("I'm a noun," "I'm a verb," …), and the strong query–key match pulls in `function`'s
*value* — its meaning flows into the representation of `it`.

**Soft, not exact.** A hash-map lookup returns exactly one value for exactly one key.
Attention scores *every* key and takes a weighted blend — for `it`, perhaps 0.7 ×
`function`, 0.2 × `None`, 0.1 × everything else (illustrative numbers again). That
softness is why the mechanism is learnable, and why it handles ambiguity gracefully:
where a human would hesitate between two referents, attention literally splits its
weight between them. The same machinery is what lets the model, while completing
`board[row - 1][` in your code, look back at the `row - 1` pattern and mirror it for
`col`.

That is deliberately all we will say. The assigned videos (Karpathy's *Intro to Large
Language Models*; 3Blue1Brown's visual transformer series) fill this in properly, and
students without an ML background should treat them as required watching this week.
Students who have taken an ML course can skim and lose nothing.

## 4. From predicting the internet to following instructions

Why does a "next-token predictor" answer questions at all? Because of three training
stages, and it pays to keep them distinct:

1. **Pretraining.** The model learns to predict the next token over an enormous corpus.
   The result (a "base model") is a formidable text-completer — but ask it a question
   and it may reply with *more questions*, because on the internet, questions are often
   followed by other questions.
2. **Instruction tuning (SFT).** The model is further trained on curated examples of
   instructions paired with good responses. Now it completes an instruction with an
   answer, because that is the pattern it was shown.

   The training data is just pairs, by the tens of thousands, along the lines of:

   > **Instruction:** Summarize the following paragraph in one sentence. *[paragraph]*
   > **Response:** *[a clean one-sentence summary]*

   > **Instruction:** Write a Python function that returns True if a number is prime.
   > **Response:** `def is_prime(n): ...` *[a correct implementation, briefly explained]*

   > **Instruction:** Explain this error message: `TypeError: 'NoneType' object is not
   > subscriptable`.
   > **Response:** *[what the error means, its usual cause, and how to find the culprit]*

   To feel what this stage changes, give the prime-number instruction to a *base*
   model: a perfectly likely continuation is *"Write a Python function that computes
   the greatest common divisor of two numbers."* — because on the internet, that
   sentence often appears in a homework problem list, followed by more problems. The
   base model completes the *document*; the instruction-tuned model has learned that
   an instruction is followed by its *answer*.

3. **Preference training (RLHF and relatives).** Human raters compare candidate
   outputs; the model is optimized toward preferred ones. This is where "helpful,
   honest, harmless" assistant behavior comes from — see the InstructGPT paper (Ouyang
   et al., 2022) in the reading list.

   Here no one writes the "right answer" at all — raters only *compare*. A training
   example looks like: prompt *"My tests are failing, what should I do?"* with two
   candidate outputs:

   > **A:** "Debug your code." *(true, useless)*
   >
   > **B:** "Start by reading the first failing assertion — what did it expect, and
   > what did it get? Then check whether the test or the code encodes the right
   > behavior…" *(concrete, actionable)*

   The rater prefers B over A, and the model is nudged so B-shaped answers become more
   probable. The same mechanism teaches judgment calls that have no verifiable answer:
   for *"Rewrite this email to my professor to sound less angry,"* raters prefer the
   candidate that is polite *while preserving the complaint* over the candidate that
   grovels — a preference you could never encode as an instruction/answer pair,
   because there is no single correct output, only better and worse ones.

Two engineering facts fall out of this pipeline:

- **Knowledge cutoff.** The model's world knowledge stops at its training date. It has
  never seen your codebase, this week's library release, or anything behind your VPN.
  Whatever it needs, *you* or the harness's tools must bring into the conversation.
  A chatbot with web search can retrieve current information even when its underlying
  model was trained months earlier; the tool result, not the model weights, supplies
  that new context.

- **Hallucination is a consequence of the objective, not a defect to be patched.** At
  every stage the model is rewarded for producing *plausible* text. Truth and
  plausibility usually coincide — that is why the model is useful — but where they
  diverge, the model confidently produces the plausible thing: an API that should
  exist, a flag that almost exists, a citation shaped exactly like a real one. This is
  the single most important fact about LLMs for a software engineer, and it is why
  verification is a pillar of this course rather than a nicety.

## 5. Context windows and statelessness

Here is the fact this whole lecture has been building toward.

**The model has no memory.** None. Every API call is a pure function: tokens in,
distribution out. When you have a two-hour "conversation" with an assistant, the
system behind it is *replaying the entire conversation* — every message, both sides —
into the model on every single call. The model isn't remembering; it is re-reading.

The **context window** is the maximum number of tokens a single call can carry —
hundreds of thousands of tokens on current frontier models, which sounds infinite and
is not. Everything competes for that budget: the conversation so far, the files the
agent has read, tool outputs, instructions. And because providers bill **per token,
per call**, replaying a long conversation has a price that grows with every turn.
(Providers mitigate this with prompt caching — Lecture 6 takes the economics
seriously, with real cost data from this course's own experiment logs.)

So where does a coding session's "memory" live? In week 1 you can already give the
real answer: *in a list of messages maintained by ordinary software outside the
model.* That ordinary software is called a **harness**, and next lecture we will build
up, on the whiteboard, the exact harness structure you will implement yourself in
week 3.

## 6. Consequences: the LLM as a pure function

Compress everything above into one line you should memorize:

> **An LLM is a pure function from a token sequence to a next-token distribution.**

Three consequences structure the rest of this course:

1. **Context is everything.** The prompt is the entire program state. What the model
   can do is bounded by what is in the window; what is *not* in the window does not
   exist. Managing that resource — what goes in, what stays out, what gets summarized
   — is a core engineering skill (Lectures 3 and 6).
2. **Instructions are everything else.** With behavior this sensitive to input, the
   difference between a vague request and a precise one is the difference between
   plausible-but-wrong and correct. Prompting, and beyond prompting *specification*,
   is Lecture 4.
3. **You must verify.** The output is plausible by construction. Plausible code
   compiles, reads well in review, and is wrong in ways that only tests, coverage,
   and skeptical reading catch. Verification is Lecture 6 and, honestly, the theme of
   the whole semester.

## Questions to think about

1. If the model is stateless, where does a two-hour coding session's "memory" live —
   and who is responsible for its accuracy?
2. Which of your existing Copilot or ChatGPT habits does next-token prediction
   explain? (Why does starting a comment produce the code you were about to write?)
3. Why might a model confidently invent an API that doesn't exist — and why is it
   *more* likely to do so for a plausible-sounding library than an implausible one?

## Before next lecture

- **Required:** Karpathy, *[1hr Talk] [Intro to Large Language Models](https://youtu.be/zjkBMFhNj_g?si=FV-E7B71kxWJnzmL)* (YouTube). This is the designated gap-filler; if you have ML background, skim at 2×.
- **Recommended for a deeper dive (optional):** 3Blue1Brown, *Transformers, the tech behind LLMs* and the attention chapter that follows it.
- **Gap-fillers (optional):** Karpathy, *Deep Dive into LLMs like ChatGPT*; Vaswani et
  al., *Attention Is All You Need* (skim §1–2); Ouyang et al. 2022 (InstructGPT).
- **Logistics:** have your Claude Pro subscription active before week 2 — Exercise 2
  depends on it.



In simplistic terms, an LLM is a function.  What are its inputs and outputs?

Parameters / weights

Training
 - Pre-training and the concept of back-propagation (adjusting weights based on training samples)
 - Instruction tuning (SFT)
 - RLHF (Reinforcement Learning with Human Feedback)

What was important about "transformer" (in the paper "Attention is all you need").  It allows training to proceed in parallel, enabling training to be run with GPUs.
