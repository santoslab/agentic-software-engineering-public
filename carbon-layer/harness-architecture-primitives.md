---
type: Topic
title: Harness Architecture Primitives
description: The named building blocks of an agent harness — instructions through verification/observability and harness evolution — as decomposed primitive-by-primitive by the Harness Engineering Masterclass.
status: draft
topics:
  - harness-engineering
generated:
  by: claude-code/claude-fable-5
  at: 2026-08-15
sources:
  - id: hem
    resource: https://www.youtube.com/watch?v=mQfTdNVCOB0
    author: The Carbon Layer
    last_modified: 2026-05-16
---

# Harness Architecture Primitives

**Harness architecture primitives** are the named building blocks that make up an agent harness
— the system around the model that turns a capable LLM into a dependable agent (see
[Harness Engineering](harness-engineering.md)). The decomposition here follows the
[Harness Engineering Masterclass](harness-engineering-masterclass.md), which first separates
three things people conflate — the **model** (a reasoning engine), the **runtime** (the agentic
loop: reason, act, observe, repeat), and the **harness** (the system around that runtime) — and
then walks the harness itself primitive by primitive, each layer's limitation motivating the
next.[^hem] The speaker's own caveat applies: "these are not all well defined, these are not
something that everyone has agreed upon"
([0:00](https://youtu.be/mQfTdNVCOB0?t=0) ·
[transcript §t-0000](../library/harness-engineering-masterclass-transcript.md#t-0000)) — this
is one practitioner's taxonomy, adopted here as a working vocabulary.[^hem]

Each primitive below links to the moment it is introduced in the talk (the `youtu.be/…?t=` link,
the citation of record) and to the matching region of the transcript capture (offline, annotatable
reading — spec §3.1).

## Scope

**In scope:**

- The individual building blocks of an agent harness — their responsibilities, their limits, and
  how each layer's shortfall motivates the next.
- Future per-primitive concepts (e.g. *Context Management*, *Durable State*, *Sub-Agents*,
  *Verification & Observability*) — when a primitive is split out into its own concept (§5.4), it
  is classified here.
- Alternative or competing decompositions of harness architecture, recorded against this one.

**Out of scope:**

- The discipline as a whole — its thesis, case studies, and whole-harness designs →
  [Harness Engineering](harness-engineering.md) (the parent Topic).
- Concrete harness products and implementations → Tool concepts (e.g.
  [Pi (Coding Agent)](pi-coding-agent.md)).

## The eleven primitives

In the talk's order, with its rationale — each limitation is what calls the next primitive into
existence:[^hem]

1. **Instructions** — who the agent is, what work it does, its tone, constraints, and coding
   rules: `AGENTS.md`, `CLAUDE.md`, system prompts, repository/cursor rules. They move repeated
   guidance into the environment — but they are *passive*: they can say "follow the project
   conventions" yet cannot discover them.
   ([3:45](https://youtu.be/mQfTdNVCOB0?t=225) ·
   [transcript §t-0345](../library/harness-engineering-masterclass-transcript.md#t-0345))
2. **Context delivery** — gives the model the material it needs: `@`-file references, the failing
   test, the stack trace. The limit: dumping everything in is not context engineering — the
   context window is finite, attention is not free, and "wrong context sometimes ends up being
   way much more worse than missing context."
   ([6:15](https://youtu.be/mQfTdNVCOB0?t=375) ·
   [transcript §t-0615](../library/harness-engineering-masterclass-transcript.md#t-0615))
3. **Context management** — decides *what enters the model now*: RAG and re-ranking,
   summarization, compaction, prompt caches, session summaries. The job under all the names:
   protect the model's attention.
   ([8:14](https://youtu.be/mQfTdNVCOB0?t=494) ·
   [transcript §t-0814](../library/harness-engineering-masterclass-transcript.md#t-0814))
4. **Tool interfaces** — structured action instead of talk: a name/description/schema contract
   the model can invoke (function calling, MCP, bash/grep). The model no longer just describes
   work; it requests actions.
   ([10:46](https://youtu.be/mQfTdNVCOB0?t=646) ·
   [transcript §t-1046](../library/harness-engineering-masterclass-transcript.md#t-1046))
5. **Execution environments** — where a tool call becomes *bounded reality*: sandboxes,
   containers, worktrees, browser profiles; filesystem scope, network, credentials, approvals.
   The layer "where trust gets practical" — instead of telling the model not to touch secrets,
   the harness makes secrets unreachable.
   ([12:20](https://youtu.be/mQfTdNVCOB0?t=739) ·
   [transcript §t-1219](../library/harness-engineering-masterclass-transcript.md#t-1219))
6. **Durable state** — "the workbench that survives the current turn": plan files, checkpoints,
   task state, session summaries, logs, diffs, memory stores. Progress becomes inspectable
   outside the model's attention — but state preserves work, it does not coordinate it.
   ([14:16](https://youtu.be/mQfTdNVCOB0?t=856) ·
   [transcript §t-1416](../library/harness-engineering-masterclass-transcript.md#t-1416))
7. **Orchestration** — the harness deciding *how work moves*: lifecycle hooks, retries, approval
   gates, human handoff, step ordering, model routing (Claude Code hooks are the given example).
   This is where agent work looks "less like chat and more like a runtime."
   ([16:19](https://youtu.be/mQfTdNVCOB0?t=979) ·
   [transcript §t-1619](../library/harness-engineering-masterclass-transcript.md#t-1619))
8. **Sub-agents** — work split into bounded loops, each "a model with a narrower job, narrower
   context, and often narrower tools," with a manager integrating the results (agents-as-tools
   and handoff patterns). The cost is the *delegation problem*: without shared procedure,
   parallel workers return inconsistent interpretations.
   ([18:13](https://youtu.be/mQfTdNVCOB0?t=1093) ·
   [transcript §t-1813](../library/harness-engineering-masterclass-transcript.md#t-1813))
9. **Skill layer** — reusable procedures loaded on demand: skills, slash commands, playbooks,
   runbooks. Moves repeated expertise "from *remember to do that thing* … into a named capability
   that the harness can invoke." A procedure is necessary — but it is not evidence.
   ([20:20](https://youtu.be/mQfTdNVCOB0?t=1220) ·
   [transcript §t-2020](../library/harness-engineering-masterclass-transcript.md#t-2020))
10. **Verification & observability** — the trust pair, presented as one primitive with two
    facets. *Verification* "asks for receipts" — tests, builds, type checks, lint, screenshots,
    evals — because "looks good to me is not a verification strategy"
    ([22:20](https://youtu.be/mQfTdNVCOB0?t=1340) ·
    [transcript §t-2220](../library/harness-engineering-masterclass-transcript.md#t-2220)).
    *Observability* is the run's recorder — traces, tool-call timelines, logs, cost, prompt
    versions, approval events — turning "the agent messed up" into a debuggable system: "you
    cannot improve what you cannot inspect"
    ([23:59](https://youtu.be/mQfTdNVCOB0?t=1439) ·
    [transcript §t-2359-observability](../library/harness-engineering-masterclass-transcript.md#t-2359-observability)).
11. **Harness evolution** — failures become infrastructure: a repeated context miss becomes a
    retrieval rule, a bad tool result a stricter schema, a dangerous command a permission gate, a
    missed edge case a test, a recurring correction a memory, a repeated workflow a skill. "The
    agent version of the post-mortem loop" — without it every session relearns the same lesson;
    with it the harness compounds.
    ([25:14](https://youtu.be/mQfTdNVCOB0?t=1514) ·
    [transcript §t-2514](../library/harness-engineering-masterclass-transcript.md#t-2514))

## Using the decomposition

The talk's closing diagnostic is the practical payoff: when an agent fails, do not only ask *was
the model good enough* — ask **which harness layer ran out of road**. Was the instruction
missing? The context wrong? The memory stale? The tool schema vague? The command run in the wrong
environment? Did the workflow need durable state, orchestration, delegation, a skill, a
verification step — or a trace that would have let you look inside?
([26:48](https://youtu.be/mQfTdNVCOB0?t=1608) ·
[transcript §t-2514](../library/harness-engineering-masterclass-transcript.md#t-2514))[^hem]

## Related

- **Topic (parent):** [Harness Engineering](harness-engineering.md) — the discipline these
  primitives decompose.
- **Primary source:** [Harness Engineering Masterclass](harness-engineering-masterclass.md) — the
  talk this taxonomy is taken from; its transcript capture is the deep-link target throughout.
- **See also:** [Harness Design for Long-Running Application Development](harness-design-for-long-running-application-development.md)
  — a whole-harness case study readable through this decomposition (context management, durable
  state, orchestration, verification).

<a id="members"></a><!-- #derived members -->
## Members

_Derived from `topics` frontmatter across the bundle. Do not hand-edit; regenerate via `reindex` (§7)._

**Subtopics:**

- [Skills](skills.md) — Reusable, named procedures an agent can invoke — skills, slash commands, playbooks, runbooks — packaging repeated expertise into the harness's skill layer.

**Concepts:**

- ["Architectural Convergence in Three LLM Agent Harnesses" (Dai)](architectural-convergence-in-three-llm-agent-harnesses-dai.md) — _Reference._ A source-level, multi-case study of three LLM coding-agent harnesses (LangChain's deepagents, Earendil's pi, DeepSeek's dsh) built from opposing philosophies that nonetheless converge on five architectural elements — with external, tamper-evident verifiability the one axis where none of them converge.
<!-- #endderived members -->

[^hem]: "Harness Engineering Masterclass: Technical Deep Dive on how to build Agentic Systems,"
    The Carbon Layer, YouTube — see `sources: hem`. All primitive names, characterizations, and
    quotes are from the talk's spoken words; each item's inline `youtu.be/…?t=` link locates the
    claim in the video (citation of record) and the paired `transcript §…` link opens the same
    passage in the §3.1 capture
    `library/harness-engineering-masterclass-transcript.md`.
