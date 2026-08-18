---
type: Concept
title: Context windows
description: The finite token budget that is the only state an LLM has, and the economics that follow.
tags:
  - context
  - cost
timestamp: 2026-07-14T00:00:00Z
---

# Context windows

The model is stateless: everything it "knows" about your session is in the tokens sent
with the current call. The window is finite, and input tokens are billed per call —
so a conversation replayed on every iteration of the [agent loop](/concepts/agent-loop.md)
has real economics. Prompt caching makes replay affordable (cache reads are much
cheaper than fresh input), which is why long-session cost data shows cache-read tokens
dwarfing input tokens.

Durable knowledge doesn't belong in the conversation. It belongs in artifacts that get
re-injected cheaply: CLAUDE.md for a repo, or a knowledge base like this one for
yourself.

# Citations

- Anthropic, *Effective context engineering for AI agents* (2025)
