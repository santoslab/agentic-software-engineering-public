# Music homework evidence template

Copy this file to `evidence.md` in your submission folder and replace each
item with what you observed. Paste exact texts (Cypher, dialog wording,
`check` output) and small result tables. Never include a password, and never
write down a call that did not happen.

## Setup (Tasks 1 to 3; the checkpoint)

- Date; Neo4j version and edition (instance card); APOC version (Plugins
  tab); Claude Code version (`claude --version`); `uv --version`:
- The two APOC checks in Query: procedure names listed; the result of
  `apoc.meta.schema()` on the empty database:
- `database.py check` output (fixture, database, nine counts):
- `/mcp`: server status, tool count, the two model-visible tool names, the
  parameters of `read-cypher`:
- The permission mode line under the input box:
- Your `.mcp.json` as submitted (password referenced, never written) and
  anything you changed from the example:
- Anything that failed on the way, with the exact text and what fixed it:

## Question A (Task 4)

- Schema prompt; number of calls; the model's table and whether it matches
  the primer's diagram:
- Proposal prompt; the proposed Cypher verbatim; did anything execute before
  you asked?
- Your review: labels and directions, `Playlist` not `Album`, distinct count
  versus path count, both sort keys, `LIMIT`, no write clause; what you
  changed or rejected:
- Run prompt; the `query` argument of the `read-cypher` call; the returned
  rows; the model's answer:
- Query replay: Database selector on `music`; the rows; field-by-field
  comparison with the agent's rows and, if they differ, with
  `queries/question-a.cypher`; what the replay does and does not prove:
- Any mistake and its correction, preserved:

## The write cycle (Task 5)

- The one field changed in `.mcp.json`; the `/mcp` tool count afterwards; the
  third tool's name:
- Your playlist name and track ids; the prompt:
- The proposed Cypher verbatim and your review (`MERGE` on `id`, `MATCH` for
  existing nodes, a position on each `HAS_TRACK`, nothing beyond P09):
- The permission dialog: its heading, the tool title, the options, the one
  you chose:
- Read-back in Query: the rows (owner, playlist, position, track, title):
- `database.py check` after the write: the mismatch, and which counts moved
  by how much:
- The revert prompt; the Cypher; the dialog; `check` after the revert:
- `NEO4J_MCP_READ_ONLY` set back to `"true"`:
- Any dialog for a shell command, and what you answered:

## Reflection (Task 6)

One paragraph: what Claude proposed that you changed or rejected; what you
could only know by looking outside the conversation, and at which step it
became visible.

## Optional extensions

Question B, the ambiguity question, or a diagnosis, if you did them.

## If live access failed

Say so here. Include the setup evidence you have, the exact error texts, and
the layer you believe failed. Label any analysis of instructor-supplied
recordings as such; it is not a live connection.
