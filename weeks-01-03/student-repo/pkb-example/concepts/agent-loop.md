---
type: Concept
title: The agent loop
description: The while-loop-with-tools that turns a stateless token predictor into a system that acts.
tags:
  - agents
  - architecture
timestamp: 2026-07-14T00:00:00Z
---

# The agent loop

An agent is a language model called in a loop by a harness. Each iteration: send the
system prompt, the conversation so far, and the tool definitions; if the model responds
with a tool call, the *harness* executes it and appends the result to the conversation;
repeat until the model stops asking for tools.

Two consequences worth remembering:

- The model never executes anything. Every safety property (permissions, sandboxing,
  allowlists) lives in the harness.
- The conversation is re-sent on every iteration, so long sessions grow quadratically
  in transmitted tokens — see [context windows](/concepts/context-window.md).

# Examples

Claude Code is this loop plus engineering: permission UI, context compaction, CLAUDE.md
injection, plan mode.

# Citations

- Anthropic, *Building Effective Agents* (2024)
- Thorsten Ball, *How to Build an Agent* (2025)
