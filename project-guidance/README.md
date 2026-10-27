# Project Guidance

Notes for the class project: what is expected and when, how to get a
project started with an agent before applying the spec-driven method
of the course, and transcripts of real brainstorming conversations to
learn from.

Read the first two in order.

| File | What it is |
|---|---|
| [`general-guidance-timeline.md`](general-guidance-timeline.md) | The purpose and expected content of the project, the four deliverables (proposal, initial presentation, completed repository, final presentation), and the 2026 timeline. The proposal is due October 28. |
| [`brainstorming.md`](brainstorming.md) | How to use an agent to get from an idea (greenfield) or an existing codebase (brownfield) to a first set of engineering documents: a ConOps, a description of the technology stack, and for brownfield projects descriptions of the data formats and the architecture. Ends with a catalog of example prompts, grouped by step. |

## Brainstorming examples

[`brainstorming-examples/`](brainstorming-examples/) holds transcripts
of real conversations with agents. The two project transcripts were
produced with Grok Bot assistants driving Cursor cloud agents; the
pattern of each prompt transfers directly to Claude Code.

| File | What it is |
|---|---|
| [`brownfield-hamr-sysml-viz-conversation.md`](brainstorming-examples/brownfield-hamr-sysml-viz-conversation.md) | A six-day conversation (October 21 to 26, 2026) that built a graphical visualizer for HAMR SysMLv2 instance models, starting from an existing prototype visualizer. Five pull requests, each one round of the conversation. The index "Interesting Prompts to Discuss" at the top links to five anchored points used in class: the request for an initial architecture and testing plan, the request for expanded documentation, the request to find dead code, the agent's assessment of unused code, and the request for a plan for the next phase. |
| [`greenfield-hamr-sysml-microkit-conversation.md`](brainstorming-examples/greenfield-hamr-sysml-microkit-conversation.md) | A two-day conversation (October 25 to 26, 2026) that started from an empty repository: Phase 1 of a SysMLv2 library for seL4 Microkit system description concepts. Shows one written brief turned into a delivered pull request. |
| [`investigating-a-technical-topic-with-grok.md`](brainstorming-examples/investigating-a-technical-topic-with-grok.md) | A chat assistant's answer to a technology question, GraphQL versus SPARQL: a comparison table, advantages and disadvantages of each, and when to use which or both. An example of the "pros and cons of each choice" step in `brainstorming.md`. |
