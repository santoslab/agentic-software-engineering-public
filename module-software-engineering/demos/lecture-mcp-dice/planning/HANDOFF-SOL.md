# Implementation handoff for the MCP dice lecture

> Authoring record. The 2026-11-15 implementation brief for the dice lecture, preserved verbatim
> from the planning repository (`mcp-lecture/HANDOFF-SOL.md`) when the material was migrated on
> 2026-11-17. Its paths, repository rules, and instructions describe that workspace, not this one;
> the implemented example is in the parent folder, `demos/lecture-mcp-dice/`.

Prepared 2026-11-15 for continuing this work with Sol. This document preserves the
decisions made after the initial preparation files were written. It is the current
implementation brief; the existing instructor outline is an earlier draft.

## Objective and authorization

Implement a coherent first draft of a 75-minute MCP lecture and accompanying
running examples in `mcp-lecture/`. Use the official Python SDK's **MCPServer**.
Produce the runnable examples, instructor outline, student notes, slides,
diagrams, demonstration instructions, and verification evidence described below.
The user approved the revised lecture direction and explicitly selected
MCPServer over the alternatives. Continue implementation when the user sends the
handoff prompt; do not reopen that library choice or stop after another plan.

Work in:

`/Users/hatcliff/Dev/git-repos/agentic-software-engineering-planning-git`

Eventual publication target, for reading conventions and source materials only:

`/Users/hatcliff/Dev/git-repos/agentic-software-engineering-public-git`

The current task is implementation here. Moving, publishing, or merging material
into the public repository is later work.

## Repository constraints and current state

- Read root `AGENTS.md`. Everything under `course-materials/` is frozen and
  read-only. The old `se-module-public-drafts/` folder is superseded.
- Read `mcp-lecture/README.md` and `source-map.md` for layout and source links.
- Preserve unrelated work. At handoff, `SpecKit/TestProject/` and
  `SpecKit/lecture-SpecKit-overview.pptx` were untracked; root `README.md` was
  modified to link this lecture workspace; `mcp-lecture/` was untracked.
  Recheck status rather than assuming it is unchanged.
- The public sibling also has unrelated changes; do not edit it during this task.
- Existing `demos/dice/dice_server.py` still imports SDK v1's FastMCP. Only syntax
  and equivalence to the original implementation were checked. No SDK environment,
  live MCP call, host registration, or rendering has been verified here.
- Existing instructor timings and emphasis are superseded by the sequence below.
- No lecture number or final destination unit has been chosen. Use an unnumbered
  working title. Routine implementation choices do not require further approval.

## Agreed teaching direction

The audience is graduate students who have encountered the basic agent loop and
the toy-agent exercise. Use a minimal dice example throughout. There is no game
database prerequisite. Claude Code is the initial demonstration host. A second
host is optional and should not delay completion.

The user specifically wants coverage of:

1. Why MCP is useful when a harness can already invoke a CLI, with explicit ties
   to the toy-agent exercise.
2. Architecture, tool-provider responsibilities, harness responsibilities, and
   the information exchanged, illustrated with diagrams.
3. Existing integrations, including a short Neo4j preview for later coursework.
4. Library support and how to ask an agent to help implement an MCP integration.
5. An intuitive dice use case and an early demonstration of the finished behavior.
6. An incremental MVP walkthrough of the protocol elements the dice example needs.
7. Testing at the function, protocol, and agent-integration levels.
8. Practical pitfalls and model/context costs.
9. Recipes for adopting an existing server and exposing one's own tool.
10. Criteria for choosing MCP versus CLI integration.

### Approved sequence

| Minutes | Content |
|---|---|
| 0–5 | Finished dice demonstration: roll 3d6, show each die and total, compare with 12; expose the actual tool call |
| 5–15 | Motivation, CLI comparison, and toy-agent bridge |
| 15–27 | Architecture and implementer responsibilities |
| 27–45 | SDK introduction and incremental dice walkthrough |
| 45–55 | Testing at three layers |
| 55–61 | Existing integrations and brief Neo4j preview |
| 61–68 | Pitfalls and costs |
| 68–72 | Decision criteria and two practical recipes |
| 72–75 | Slack |

This is a prepared walkthrough, not 75 minutes of live implementation. Keep any
student extension activity short and optional; substantial hands-on work belongs
in a separate lab. The deliberately misleading-docstring experiment is optional,
not the central demonstration and not a guaranteed model failure.

### Toy-agent bridge

Read Steps 5–6 of
`course-materials/weeks-01-03/exercises/exercise-04-toy-agent.md` rather than relying
on the bare starter, which begins as a chatbot. Connect these concrete artifacts:

| Toy agent | MCP-enabled host |
|---|---|
| Handwritten `TOOLS_SCHEMA` | Discover server tool definitions, then adapt them to the model API |
| `TOOLS_DICTIONARY` mapping names to functions | Associate discovered tools with their server |
| Direct function dispatch | Route the request through an MCP client |
| Append a tool result to model messages | Convert the server result into the model API's tool-result representation |

Keep the underlying agent loop recognizable. Error handling and execution limits
were already present in the toy agent; MCP did not invent them.

### Architectural distinctions to preserve

- MCP provides a common integration interface; it does not make CLI execution
  obsolete or uniquely possible.
- Distinguish the model API connection from the host/client-to-server connection.
  The model selects/request tools; the host routes calls; server code executes.
- Show both a component diagram and a sequence diagram of an actual dice call.
- An adapter can expose an existing library, CLI, or service without rewriting
  the underlying tool.
- The description is part of the interface alongside schemas and results. Avoid
  the old claim that a docstring is the entire interface.
- Local stdio does not mean the whole agent system runs offline.
- Mention resources and prompts for orientation; do not invent features merely
  to demonstrate every protocol capability.
- Verify startup/discovery messages against the pinned SDK/protocol. Do not copy
  an older initialization sequence into a diagram without checking the runtime.

## Implementation choice and migration

Use **official SDK v2 MCPServer**, not standalone `fastmcp` and not an SDK v1 pin
as the final implementation. The expected starting change is:

```python
from mcp.server import MCPServer

mcp = MCPServer("dice")
```

Preserve the small decorator-based implementation. Verify the actual supported
release, imports, launch commands, dependencies, and protocol behavior. Pin a
tested version and record it; do not assume a documentation page tracking `main`
matches the installed release. Do not implement a dual-version compatibility
layer unless a concrete requirement emerges.

The earlier discussion identified a rename from bundled SDK v1 FastMCP to
MCPServer, plus broader v2 API changes. Our simple server should need little
source migration, but that has not been tested. Read current primary documentation:

- [Official SDK](https://github.com/modelcontextprotocol/python-sdk)
- [SDK migration guide](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/migration.md)
- [SDK changes](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/whats-new.md)
- [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [Inspector](https://modelcontextprotocol.io/docs/tools/inspector)
- [Claude Code integration](https://code.claude.com/docs/en/mcp)

## Running examples

Develop this progression, using small snapshots or another clearly documented
way to reproduce each stage. Choose the simplest structure; avoid a generic
framework or numerous nearly identical server copies.

| Stage | Behavior | Teaching point |
|---|---|---|
| A | Ordinary dice function, callable directly; a small CLI if useful for comparison | Underlying tool works without MCP |
| B | One `roll` tool exposed through MCPServer | Minimal adapter and decorator |
| C | Inspect actual discovery and call messages | What the SDK handles; `tools/list` and `tools/call` |
| D | Invalid-input behavior and improved result representation | Validation, structured results, errors |
| E | Add `flip_coins`; invoke both through the host | Discovery and tool selection |

Retain the original limits as a starting contract: 1–20 dice, sides in
4/6/8/10/12/20, and 1–100 coins. Changes to representation should be explicit
teaching steps with matching tests and descriptions.

Separate function checks, SDK validation, tool-execution error results, and
protocol failures. The inherited `Error:` text is an ordinary successful return
at the protocol level; do not present it as explicit MCP error signaling.

For the Neo4j preview, reuse local course material and recorded transcripts where
appropriate, clearly labeled as historical. Check the current official server
documentation before presenting installation details. A prepared schema/read-query
example is sufficient; building a graph database environment is outside this
implementation's essential scope. Do not claim historical results are newly run.

## Deliverables

1. Revised instructor outline with timings, concrete demo instructions, expected
   observations, fallbacks, and cut-if-long guidance.
2. Self-contained student notes in `lecture-notes/lecture-mcp-dice.md`.
3. Marp source in `slides/lecture-mcp-dice.md`, using the public course's visual
   style and speaker notes. Keep slide text concise; put fuller explanations in
   student notes and speaker notes.
4. Editable Mermaid diagrams plus rendered SVGs under `slides/diagrams/`.
5. Runnable incremental examples, reproducible dependency setup (prefer the
   repository's established tooling where applicable), meaningful tests, and
   commands that can be followed from a fresh checkout.
6. A demonstration script with direct calls, Inspector/protocol checks, host
   setup, exact prompts, and real captured results where execution is available.
7. A short agent-development prompt that specifies the tool contract, pinned
   library, checks, and required evidence instead of merely saying “build MCP.”
8. Updated README/source map and a verification report stating versions, commands,
   results, and any remaining rehearsal steps. The public migration map remains.

Do not add a large assignment, another backend, or an extensive framework survey.
An optional short exercise can specify a bounded dice tool that reports whether
a roll meets a target, with a contract, valid/invalid calls, and grounded answer.

## Verification and completion criteria

- Test counts, allowed outcomes, sums, coin tallies, and boundary/invalid inputs.
  Use controlled randomness where repeatability matters; do not claim a handful
  of samples proves statistical fairness.
- Exercise discovery and calls without an LLM. Include at least one real stdio
  subprocess check so in-process tests do not hide launch/transport problems.
- Check the schemas and result representations actually emitted by the chosen
  SDK, including the chosen explicit error behavior.
- If an authenticated host is available, capture real calls to both tools and
  verify the final answer against results. Prefer a scratch project/local scope
  for rehearsal; do not alter unrelated user-wide configuration.
- If host access is unavailable, complete all independent implementation and
  protocol checks, provide an exact manual rehearsal script, and state the
  missing check. Never fabricate a model transcript or claim a skipped demo ran.
- Keep stdout free of diagnostic logging in a stdio server; use stderr.
- Cost discussion distinguishes server execution, model turns, and context use.
  Avoid claiming all tool definitions always load into every prompt; verify the
  host's discovery behavior. Do not invent price or token measurements.
- Compare CLI and MCP fairly: CLI can provide structured output and bounded
  operations too. MCP can wrap a CLI.
- Render diagrams and slides; inspect for legibility/overflow and check local
  links. Generated slide PDF/HTML are preview artifacts, not public source files.
- Reconcile examples, notes, slides, and outline. Remove stale FastMCP setup and
  old Stage E/calendar assumptions from the new teaching package.
- Preserve the public repository's content/code license boundary on eventual
  transfer. Do not copy local credentials, machine-specific paths, or authoring
  references into student prerequisites.
- Do not make commits or publish unless asked. Finish with links to artifacts,
  concise verification results, and specific remaining review/rehearsal work.

## Suggested execution order

Read the brief and sources; establish and test the pinned MCPServer environment;
implement the incremental examples and tests; capture protocol evidence; draft
the three lecture artifacts together; render and review; update the status and
report. Continue through all independently executable work without pausing for
routine design choices.
