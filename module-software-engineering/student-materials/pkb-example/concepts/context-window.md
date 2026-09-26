---
type: Concept
title: Context windows
description: The finite token budget that is the only state a language model has during a call, and the cost consequences of replaying it.
generated:
  by: claude-code/claude-fable-5-1
  at: 2026-09-25
sources:
  - id: ece
    resource: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    author: Anthropic
    last_modified: 2025-09-29
status: draft
---

# Context windows

The model is stateless between calls: everything it knows about a session is
in the tokens sent with the current call, and the window that holds them is
finite. Input tokens are billed on every call, so a conversation replayed on
every iteration of the [agent loop](/concepts/agent-loop.md) has a cost that
grows with its length. Prompt caching makes replay affordable — a cache read
costs a fraction of fresh input — which is why the cost data of long sessions
shows cache-read tokens far exceeding input tokens.

## Consequences for how work is organized

Durable knowledge does not belong in the conversation. It belongs in artifacts
that are re-injected cheaply and survive a cleared context: a repository's
`CLAUDE.md`, the governing documents it names, and a knowledge base such as
this one. Anthropic's guidance is to treat the context as a budget and to
choose, for each call, the smallest set of high-signal tokens that lets the
model act — instructions, tool definitions, retrieved documents, and a compacted
history.[^ece] The [reference note](/references/effective-context-engineering.md)
summarizes that guidance.

[^ece]: Anthropic, *Effective context engineering for AI agents*, 2025 — see `sources: ece`.
