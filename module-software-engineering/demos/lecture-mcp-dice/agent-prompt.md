# Prompt for developing an adapter with an agent

Implement a small local stdio MCP adapter using the official Python SDK
`mcp==2.3.0`, `from mcp.server import MCPServer`. Keep the ordinary functions
independent of the transport. Expose roll(count=1, sides=6) and flip_coins(count=1).
Dice count is an integer 1–20; sides is one of 4/6/8/10/12/20. Coin count is an
integer 1–100. Reject bools and string/float coercions in the final adapter.
Return ordered dice plus total/sides, or an H/T string plus head/tail counts.
Publish accurate descriptions and input/output schemas. Make domain failures
explicit tool errors; distinguish them from malformed JSON-RPC requests.

Pin dependencies and provide fresh-checkout commands. Keep stdout exclusively
for protocol messages. Test controlled randomness, sums, counts, boundaries,
invalid values, discovery, result shapes, and a real stdio subprocess. Capture
actual messages using the pinned client's supported discovery behavior; do not
copy an assumed initialization sequence. Supply exact host rehearsal prompts;
if no authenticated host is available, state that limit and never invent a
transcript. Report commands, versions, results, and remaining checks. Do not add
a database, a generic adapter framework, credentials, or global host configuration.
