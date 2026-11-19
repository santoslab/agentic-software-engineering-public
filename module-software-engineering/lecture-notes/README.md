# Student lecture notes

This folder holds the full prose notes for each lecture. Each file is student-facing
and self-contained, is distributed per lecture, and converts to PDF with pandoc.

- File naming: `lecture-NN-<slug>.md`, matching the outline in
  `../lectures-instructor-notes/`.
- Header: the title line, then a one-line blockquote giving the meeting and what the
  lecture launches, as in
  `../../weeks-04-07/lecture-notes/lecture-09-persistence.md`.
- Sections follow the outline's topic blocks in order and close with
  `## Questions to think about`.

## Beads lecture

- [Beads: Managing Agent Work Across Sessions and Subsystems](lecture-beads.md)
  — accompanies the [slide deck](../slides/lecture-beads.md) and
  [recorded demonstration](../demos/lecture-beads/recorded-run/transcript.md).

## MCP lectures

- [Connecting an agent to existing MCP servers](lecture-mcp-adoption.md) —
  accompanies the [slide deck](../slides/lecture-mcp-adoption.md) and the
  [adoption demo](../demos/lecture-mcp-adoption/README.md); launches the
  [music homework](../../neo4j/02-neo4j-music-mcp/README.md).
- [Connecting an agent to a database through a local MCP server: Neo4j](lecture-mcp-neo4j.md) —
  accompanies the [slide deck](../slides/lecture-mcp-neo4j.md) and the
  [Neo4j demo](../demos/lecture-mcp-neo4j/README.md); explains what changes
  when the server is a local child process in front of a database you own,
  follows one read and one write end to end, and launches the
  [music homework](../../neo4j/02-neo4j-music-mcp/README.md). Draft pending
  instructor rehearsal.
- [MCP: from an ordinary function to an agent tool](lecture-mcp-dice.md) —
  accompanies the [slide deck](../slides/lecture-mcp-dice.md) and the
  [dice example](../demos/lecture-mcp-dice/README.md).
