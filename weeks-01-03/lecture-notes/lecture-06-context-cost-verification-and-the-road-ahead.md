# Lecture 6 Notes — Context, Cost, Verification, and the Road Ahead

> Agentic Software Engineering · Week 3, second meeting
>
> **The one idea:** you now know how agents work. The rest of the semester is about
> making their output *trustworthy at increasing scale* — and five principles are the
> rubric.

## 1. Context economics, grounded in your own loop

Start with a quiz you can now answer from your Exercise 4 code: *it is turn 30 of a
session — what gets sent to the model?*

Everything. Again. The system prompt, all thirty turns, every file the agent read,
every tool result — the entire messages list, re-transmitted, re-billed. Input tokens
are cheap individually; re-sending a hundred-thousand-token history thirty times is
not. This is the economic fact your loop made visible, and providers answer it with
**prompt caching**: the unchanged prefix of a conversation can be cached, so replaying
it costs a *cache-read* rate far below the fresh-input rate (writing to the cache
costs a premium the first time; reads then recoup it many times over).

Now look at real data. The course's medium-project experiments logged every session's
token flows to CSV. Here is an actual row, from the first pass of the finance-tracker
build:

| InputTokens | OutputTokens | CacheWriteTokens | CacheReadTokens | EstCostUSD |
|------------:|-------------:|-----------------:|----------------:|-----------:|
| 19,326 | 29,903 | 607,136 | 3,676,823 | 6.48 |

Cache reads outnumber fresh input by roughly **190 to 1**. You can now explain that
ratio in one sentence: *the conversation is replayed every call, and caching is what
makes replay affordable.* Without the cache, that session's history would have been
billed at fresh-input rates on every turn — the difference between a $6 session and a
session you would remember. When we sort these CSVs by cost in class, the expensive
rows are exactly the long, never-cleared sessions you would predict.

## 2. Managing the window in practice

Knowing the economics, your three controls from Lecture 3 become an actual decision
procedure:

- **`/compact`** summarizes the conversation and continues. Lossy by design — a
  summary replaces verbatim history. Right when the session's *direction* matters but
  its details don't.
- **`/clear`** wipes the conversation. CLAUDE.md is re-injected; everything else is
  gone. Right between unrelated tasks.
- **A fresh session + good artifacts** re-gathers context from CLAUDE.md, the spec,
  and the plan. Often *cheaper and better* than compacting a long, sick session.

Run the decision on a concrete session. You are 90 minutes in: `/context` shows ~60k
tokens, of which ~40k is exploration — file reads from an approach you abandoned an
hour ago — and the last 20 minutes finally converged on the right fix, half applied.

- Mid-task, direction matters, details don't → **`/compact`**: the summary keeps
  "we're fixing the payment validator, tests 3 and 7 still red" and sheds forty
  thousand tokens of dead file reads.
- The fix just landed and your next task is unrelated → **`/clear`**: nothing from
  this session deserves to be replayed at all.
- Somewhere in that exploration the agent asserted something wrong that keeps
  resurfacing → **fresh session**: re-open from CLAUDE.md and the spec, and state the
  correct fact first. A summary of a sick session inherits the sickness.

Why "sick"? Because long contexts don't just cost — they **rot**. An early wrong
statement gets replayed every turn, competing with the correction that came later. An
abandoned approach keeps whispering from turn 12. The model attends over everything
in the window, including the parts you wish it would forget.

Here is the failure in miniature. At turn 6 the agent asserts "this project's tests
use unittest" (wrong — it's pytest). At turn 9 you correct it, and for a while all is
well. But the window has no edit history: both statements are replayed on every call,
forever. At turn 40 — the correction now thirty turns back, the agent deep in a
different subtask — it writes a `unittest.TestCase` class. Nothing malfunctioned:
attention over a long window simply stopped favoring the correction over the
original, fluent, *wrong* sentence. Wrong statements in context don't get deleted;
they get outvoted — until they aren't. When an agent seems to degrade over a long
session, the context is usually the disease, and re-contextualizing from durable
artifacts is usually the cure.

Which restates Lecture 4's trajectory as an operating rule: **move context out of the
conversation and into artifacts** — then treat the conversation as disposable.

## 3. Verification and trust: a $25–50 cautionary tale

The retrospectives you read for today contain the sharpest lesson in this unit, and
it costs real money to learn any other way. The same finance tracker was built five
times. Compare passes four and five.

**Pass 4** was the autonomy experiment: plan the project as epics in an issue
tracker, then let a single Opus session run *"and it didn't stop until it was 100%
done."* The operator had strengthened the testing requirements in advance — the agent
had the tools to check itself, and used them. The run cost **$25–50** in one session.
The retrospective's verdict: *"The overall quality of the final product was well below
par. Since I didn't verify the correct direction early on, it would require an
expensive review to find and correct the organizational and stylistic choices Claude
made."* And the operator's most useful admission: *"I should have interrupted the
model as soon as it skipped a verification step I intended."*

**Pass 5** rebuilt the same project with checkpoints welded into the process. Ten
waves; each wave ran a fixed cycle — **Red** (write the wave's tests first, from the
ConOps), **Green** (implement to passing), **coverage gate** (100% branch, enforced
by the build), **self-review** (a code-review subagent over the wave's diff), **manual
checklist** (the agent presents what it did), **checkoff** (a human approves), then
commit. It took 8–9 deliberate hours. The verdict: satisfaction 8/10, *"best end
product and best understanding of the end product so far."*

The lesson is **not** "autonomy bad." Pass 4's testing rigor *worked* — the agent
found its own bugs. What failed was direction: nobody confirmed the *shape* of the
work while the shape was still cheap to change. **Autonomy without embedded
checkpoints outruns trust.** The checkpoints that fix it are boring and mechanical —
a coverage gate that fails the build, a review subagent, a human checkoff between
waves — and mechanical is the point: gates that depend on remembering to care get
skipped, as pass 4 demonstrated at production prices.

One more instrument for the toolbox: the Java 9×9 game from Lecture 4 enforces **100%
branch coverage** via its build (JaCoCo) — the build *fails* if a branch goes
untested. That is principle 3 ("give the agent tools to check itself") hardened into
a gate no one can forget to apply. In class we open its coverage report and its
CLAUDE.md, where the gate is stated as law.

And a humbling limit worth writing down, from the pass-5 retrospective: *"I can only
provide counsel on what I already know."* The operator hit techniques (testing seams,
guard classes) they didn't fully understand, and elicitation and verification got
harder exactly there. The agent does not relieve you of expertise; it *spends* your
expertise. What you don't understand, you cannot verify — which is an argument for
your Project 0 knowledge base if there ever was one.


## 4. The five principles — your semester rubric


The one-page handout you read distills all five passes into principles, each answering
what / how / why / when. You have now *practiced* every one of them:

1. **Spec-Driven Development** — an authoritative reference document (spec or ConOps)
   written *before* the first prompt of development. You did this in miniature for
   your PKB; Attempt 2 and the Java port showed it at project scale.
2. **The Cycle of Development** — the repeated, ordered actions of each unit of work
   (tests → code → verify → checklist → approval → commit), written down and enforced.
   Pass 5's wave cycle is the reference example; pass 4 is what its absence costs.
3. **Project Context Management** — conventions and project truths live in CLAUDE.md,
   not in your prompts; amended whenever you catch yourself repeating an instruction
   or the agent repeating a mistake. You practiced this improving Exercise 2's
   generated CLAUDE.md.
4. **Requirement Elicitation** — find the gaps in your own spec by making the agent
   interview you; a few hundred tokens of questions against tens of thousands of
   tokens of rework. You ran this for your PKB kickoff.
5. **Verification** — ensure what you instructed actually happened: tests, coverage
   gates, review subagents, and your own skeptical reading. *You are responsible for
   every line you ship.* You practiced the manual half catching Claude wrong in
   Exercise 2.

From Project 1 onward, these five are the grading lens: project retrospectives will
ask you to show where each principle was applied — or to account for what happened
where it wasn't.


## 5. Three kinds of memory

Pull the unit's threads into one taxonomy. An agentic development practice maintains
memory at three scopes:

| | Lifetime | Scope | Cost profile |
|---|---|---|---|
| **Conversation** | one session | this task | replayed and re-billed every turn; rots |
| **CLAUDE.md** | the project | one repo | injected each session; cheap, durable |
| **Your PKB** | your career | every project | free to read, compounds with use |

Same engineering problem at three scales: what should be remembered, where, at what
cost. Your PKB's `log.md` is its history; its `index.md` is its compaction.

Take one hard-won fact through all three homes. During Project 2 you lose an
afternoon to a floating-point rounding bug and emerge with: *money must be `decimal`,
never `float`.*

- **In a prompt** ("remember, use decimal for amounts") it protects this session and
  evaporates with it.
- **In CLAUDE.md** — the course's finance-tracker actually carries the line "Money is
  `decimal` everywhere — never `double`/`float`" — every future session in *that
  repo* starts knowing it, for about a dozen tokens per session.
- **In your PKB**, generalized ("currency arithmetic wants exact decimal types;
  binary floats can't represent 0.10") it survives the course and applies to every
  system you ever build that touches money.

Same fact, three scopes, three costs. Choosing the right home for each fact you learn
is context engineering — the same discipline as `/compact` vs `/clear`, applied at a
longer horizon.

## 6. The road ahead

Next meeting, the Project 1 brief drops: a complete small build — tic-tac-toe scale —
done with all five principles from the first prompt. Weeks 7–10 are Project 2, at the
finance-tracker's scale, where hooks and subagents join the toolkit because that
project genuinely needs them. Weeks 11–14 are Project 3, a full-stack web application
at the scale where discipline stops being a virtue and becomes survival.

To see where this ends, we close with ninety seconds on the large project's
development plan — the real document steering the course's biggest experiment. Its
milestone cycle: **Brief → Gather → Develop → Verify → Report**, with two human
checkpoints bracketing every milestone, mechanical gates (lint, tests, smoke,
contract validation, coverage, review) that return red work to in-progress without
exceptions, and one enforcement rule that should sound familiar after today: the
agent's todo list *is* the enforcement mechanism — a skipped phase is visible as a
skipped checkbox. That is pass 4's lesson, institutionalized. In week 11, that
document is you.

## Questions to think about

1. Pass 4 was cheap per feature and disappointing overall. Where *exactly* did trust
   break — and which single checkpoint, inserted earliest, would have caught it?
2. Which of the five principles would you drop for a 50-line script? For a 50-KLOC
   application? (There is no right answer; the point is that discipline scales with
   stakes, and you should be able to argue the scaling.)
3. A hard-won fact just cost you an hour: the test suite must run with a fresh
   database per test. Prompt, CLAUDE.md, or PKB note — where does it go, and why?

## Before week 4

- Finish **Exercise 4** (due at the start of week 4) and your **Project 0 kickoff**
  (due now).
- No new reading. Rest; Project 1 starts Monday.

