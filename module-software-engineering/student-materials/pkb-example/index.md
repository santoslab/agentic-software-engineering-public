---
okf_version: "0.2"
---

# Example PKB — Agentic Software Engineering

A small bundle in the Open Knowledge Format, restricted to the profile that the
Project 0 brief gives in its §3 (`../../project-0-pkb-brief.md`). It shows what a
conformant bundle looks like — the frontmatter of a note, an index entry, a log
entry, a bundle-relative link, a link to a note not yet written — and nothing
about what yours should contain. Yours will be larger, organized around your own
interests, and governed by documents this example does not include: the concept
of operations, the format specification, and the operations document are
modeled by the note-set demo, not here.

## Concepts

- [The agent loop](/concepts/agent-loop.md) — The loop in which a harness calls a language model, executes the tool calls it returns, and appends the results, until the model stops calling tools.
- [Context windows](/concepts/context-window.md) — The finite token budget that is the only state a language model has during a call, and the cost consequences of replaying it.

## References

- [Effective context engineering for AI agents (Anthropic, 2025)](/references/effective-context-engineering.md) — Anthropic's engineering post on choosing what goes into an agent's context — system prompt, tools, examples, retrieved documents, history — and why the context is a budget.

## Not yet written

- [Tool schemas](/concepts/tool-schemas.md) — a link to a note that does not exist yet. OKF permits it, and Obsidian shows it as an unresolved link.
