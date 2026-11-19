# MCP: from an ordinary function to an agent tool — instructor outline

75 minutes; prepared walkthrough for graduate students who have completed the
basic agent loop, toy-agent exercise, and the preceding MCP adoption and Neo4j
lectures. No database is required. Working
lecture title, no lecture number assigned. Sources and migration decisions are
in [source map](../demos/lecture-mcp-dice/planning/source-map.md); current evidence is in
[verification](../demos/lecture-mcp-dice/reports/verification.md).

## Student-testable objectives

Students can trace a dice request through model API and MCP links; map the four
toy-agent integration artifacts to an MCP host; assign provider/SDK/host duties;
distinguish function validation, SDK validation, tool errors, and protocol errors;
and justify CLI or MCP for a given task. Ask for observable evidence, not a
recitation of protocol vocabulary.

## Prepare before class

- Follow [DEMO.md](../demos/lecture-mcp-dice/DEMO.md), sync the locked environment, run tests,
  inspect the captured B/D/E JSON and wire logs, and render the deck.
- Rehearse Claude Code in a scratch directory with the session config; host
  authentication was unavailable during authoring. Capture both tools before
  claiming the model integration has passed. Keep a terminal on the saved
  protocol result as the opening fallback.
- Open `dice.py`, `dice_server.py`, tests, and protocol evidence side by side.
  Have the component and sequence SVGs ready. Do not type the whole example live.
- Do not install or show a database in this lecture. If the recap at 58–61
  needs a concrete consumer-side example, point back to the Neo4j lecture's
  slides or its captures (`../demos/lecture-mcp-neo4j/reports/`), not a live
  instance.

## Timing and actions

| Minutes | Slides | Instructor actions and evidence | Check / fallback / cut |
|---|---|---|---|
| 0–5 | 1–2 | Finished host prompt: roll 3d6 once, show each die and total, compare with 12. Expand real call and result. | Ask which part executed code. If host fails, show captured `[2,4,5]`, total 11; compute below 12 and label it LLM-free. |
| 5–10 | 3–5 | Run Stage A CLI; show JSON. Map `TOOLS_SCHEMA`, `TOOLS_DICTIONARY`, dispatch, appended tool result from toy-agent Steps 5–6. | Ask what MCP standardizes when CLI already works. Keep limits/errors recognized from the exercise. Cut extended CLI debate. |
| 10–20 | 6–8 | Trace component diagram and sequence. Separate model API and local stdio. Allocate duties to host, SDK, provider; orient resources/prompts. | Ask who executes and who grants permission. Local server does not imply offline model. Cut remote-transport detail. |
| 20–45 | 9–13 | A function → B import/constructor/decorator → C real discovery → D strict bounds/output/errors → E coins. Run protocol demo, inspect wire IDs and fields. | Show B count=0 vs D count=0 and sides=7. Confirm no initialize on captured modern path. Use saved files if process fails. Cut optional extension first. |
| 45–58 | 14–15 | Run tests; inspect controlled outcomes, schema assertions, real subprocess, malformed call. State host grounding check separately. | Ask which test detects wrong launch environment; ask why Error text can still succeed. If tests fail in class show verification and diagnose after class. |
| 58–61 | 16 | Brief recap of the adoption and Neo4j lectures from the consumer's side (the discovered contract, the argument, the rows, the replay, the dialog); connect that evidence to provider responsibilities. | Refer back to the two lectures' slides; no capture needed. Cut this recap if behind. |
| 61–68 | 17–18 | Pitfalls and costs: stdout, paths, coercion, descriptions, context, turns, server execution. | Ask whether every tool definition always loads; discuss host-dependent deferral. No invented prices/tokens. |
| 68–72 | 19–20 | CLI/MCP decision and two recipes. Show development prompt's contract and evidence requirements. | Exit prompt: choose an interface for one existing command and justify. Skip optional extension if behind. |
| 72–75 | 21 | Questions and slack. | Revisit any misunderstood boundary. |

## Relation to the adoption and Neo4j lectures

Configuration, discovery as a consumer, and the provider survey were introduced
in the adoption lecture; the Neo4j lecture added a local stdio server, a tool
whose argument is a program, and writes behind the permission dialog, all seen
from the consumer's side. Keep slides 3–5 a five-minute retrieval exercise.
Use the recovered time for the implementation and testing walkthrough. The
[expanded student tutorial](../lecture-notes/lecture-mcp-dice.md) provides complete
examples and explanations beyond what fits on slides.

## Walkthrough details

Use [the exact runnable script](../demos/lecture-mcp-dice/DEMO.md) rather than reconstructing
commands. In B the ordinary function still enforces limits; its wrapper formats
successful text or catches a ValueError into ordinary Error text. D advertises
count bounds through Field, enforces strict integers, returns Pydantic results,
and maps invalid sides to ToolError. The sides whitelist intentionally remains
in code plus description; integer schema alone does not express it. E adds one
decorator, and discovery returns both names. This is a complete small tool, not
a framework design session.

On the wire, match request/response IDs. SDK 2.3.0 auto mode discovers revision
2026-07-28 through `server/discover`; don't teach an old handshake as if it was
captured. Legacy peers can still take a compatibility path. The model arrows
in the sequence diagram explain the host loop; only its client/server arrows
are represented by the protocol capture.

Have students point out `description`, `inputSchema`, `outputSchema`, `content`,
`structuredContent`, and `isError`. A model-friendly description is part of the
interface alongside the schemas and result contract. Tests establish bounds and
internal consistency, not fairness or guaranteed model behavior.

## Discussion and checks for understanding

- “If we already have a JSON CLI, what work would an MCP adapter save across
  hosts, and what lifecycle cost would it add?” Look for discovery and routing.
- “Does the model send MCP directly?” Look for host conversion at both boundaries.
- “What validates count=0? What validates sides=7?” Look for SDK vs function.
- “Could a server be healthy while the answer is wrong?” Look for tool selection,
  arithmetic/grounding, and host policy checks.
- “Would local stdio remove model charges?” Look for separate execution/turn/context costs.

Optional two-minute extension: use the bounded target-check contract in DEMO.md.
Request a controlled valid example and invalid arguments; do not turn it into a
large assignment. A misleading-description experiment is optional and requires
an observed outcome, never a promised model failure. It is not part of the main
sequence.

## After rehearsal / eventual publication

Complete the authenticated host evidence and inspect Inspector's web UI on a
supported Node version. Review pacing with this deck's 21 slides. Choose a course
unit and lecture number later. Curate prose/media under CC BY 4.0 and code/config
under MIT when transferred; this task does not publish or edit the public repo.
