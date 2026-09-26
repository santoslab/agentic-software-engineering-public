---
type: Concept
title: The agent loop
description: The loop in which a harness calls a language model, executes the tool calls it returns, and appends the results, until the model stops calling tools.
generated:
  by: claude-code/claude-fable-5-1
  at: 2026-09-25
sources:
  - id: bea
    resource: https://www.anthropic.com/research/building-effective-agents
    author: Anthropic
    last_modified: 2024-12-19
status: draft
---

# The agent loop

A language model predicts tokens; it does not act. An agent is the model called
in a loop by a program — the harness — that gives it tools. Each iteration sends
the conversation so far to the model. The model answers either with text, which
ends the loop, or with one or more tool calls. The harness executes each call,
appends the call and its result to the conversation, and sends the whole
conversation again. Anthropic describes an agent as a system in which the model
directs its own process and tool use, while the harness supplies the tools, the
environment, and the stopping rule.[^bea]

## What the loop implies

- Everything the model knows about the session is in the conversation it is
  sent; see [context windows](/concepts/context-window.md).
- The harness, not the model, decides which tools exist, how their results are
  formatted, and when a run stops. Changing the harness changes the agent's
  behavior without changing the model.
- Each iteration is a full model call, billed on the whole conversation. Long
  loops are expensive unless earlier turns are served from a cache.

## In this course

The foundations unit's Lecture 02 introduces the loop and Exercise 4 builds one;
Lecture 05 reads a coding agent's harness. The software-engineering module
treats the loop as given and asks which documents the harness should load so
that the model acts as specified.

[^bea]: Anthropic, *Building effective agents*, December 2024 — see `sources: bea`.
