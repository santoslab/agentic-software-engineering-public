---
type: Reference
title: Effective context engineering for AI agents (Anthropic, 2025)
description: Anthropic's engineering post on choosing what goes into an agent's context — system prompt, tools, examples, retrieved documents, history — and why the context is a budget.
resource: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
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

# Effective context engineering for AI agents (Anthropic, 2025)

## Summary

The post argues that as models improve, the limiting factor in an agent's
performance shifts from the wording of a prompt to the composition of everything
the model is sent: the system prompt, tool definitions, examples, retrieved
documents, and the history of the run. It names this composition context
engineering and treats the context window as a finite budget with diminishing
returns, because attention over a long context degrades and every token
competes with every other.[^ece]

Its practical guidance: keep system prompts at the altitude of principles rather
than brittle rules; define few tools, each with an unambiguous purpose; prefer a
small set of representative examples to an exhaustive list; retrieve documents
when they are needed rather than preloading them; and, for long-running tasks,
use compaction, structured note-taking outside the context, and sub-agents with
their own contexts. The last three are the mechanisms this course's harness
lectures, and the PKB itself, rely on.[^ece]

## Why it is in this knowledge base

It is the source most of the course's claims about
[context windows](/concepts/context-window.md) rest on, and its note-taking
recommendation is one justification for keeping a knowledge base the agent can
read.

[^ece]: Anthropic, *Effective context engineering for AI agents*, 2025 — see `sources: ece`.
