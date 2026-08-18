---
type: Practice
title: Spec-driven development
description: Writing the behavioral contract before the code, so the agent builds against a stable target.
tags:
  - specs
  - methodology
timestamp: 2026-07-14T00:00:00Z
---

# Spec-driven development

Requirements delivered as a prose paragraph drift; requirements elicited into a spec
hold. The pattern: interview until the decision tree is resolved, write the spec, then
point every implementation prompt at it. A good spec is implementation-independent —
in the course's tic-tac-toe experiments, the same Concept of Operations produced both
a Python and a Java implementation.

Depends on the [agent loop](/concepts/agent-loop.md) only in the sense that specs are
what keep a long-running loop aimed.

# Examples

The development prompt for a well-specified project can shrink to one line:
"Wave 1 is complete, now implement Wave 2."

# Citations

- Course prompt cheat sheet, principle 2
- NautilusTRX pass retrospectives
