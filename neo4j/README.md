# Neo4j exercises

Activities that use the Neo4j graph database. All run against a local Neo4j
Desktop instance that the student creates once, in exercise 01, and reuses
with one database per activity.

| Folder | Activity | Assigned |
|---|---|---|
| [`01-intro-to-neo4j-cypher/`](01-intro-to-neo4j-cypher/ReadMe.md) | Install Neo4j Desktop and follow Chapter 1 of *Neo4j: The Definitive Guide*; turn in screenshots and impressions. | Per the course schedule |
| [`02-neo4j-music-mcp/`](02-neo4j-music-mcp/README.md) | Connect Claude Code to a prepared, fictional music database through the official Neo4j MCP server: one reviewed read verified in Desktop's Query tool, one controlled write behind the permission dialog, verified and reverted, and a recipe for any database. Includes the fixture and its loader, a Cypher primer, reference queries, tests, and an evidence template. About one hour once Desktop is installed. | The [MCP Neo4j lecture](../module-software-engineering/lecture-notes/lecture-mcp-neo4j.md) in `module-software-engineering/` (draft pending the instructor's rehearsal; the adoption lecture closes with a teaser for it) |

[`neo4j-desktop-mcp-setup.md`](neo4j-desktop-mcp-setup.md) is the general
setup guide: APOC once per instance, one database per activity, the
password in the shell, the `.mcp.json` entry, `/mcp`, writes behind the
permission dialog, and diagnosis by layer. The music homework and every
later Neo4j activity link to it; `resources/` holds its screenshots.

A follow-on homework on the OpenFlights airline data, in which students design
and load a graph themselves with the same server, is planned as
`03-openflights-mcp/` under its own plan.

The music homework's instructor key is not in this folder. It lives with the
lecture that launches the homework, at
[`module-software-engineering/demos/lecture-mcp-neo4j/instructor-key/`](../module-software-engineering/demos/lecture-mcp-neo4j/instructor-key/README.md).
`export_students.py` in the homework folder copies the student package alone
into an empty directory.
