# Neo4j exercises

Two activities that use the Neo4j graph database. Both run against a local
Neo4j Desktop instance that the student creates for the activity.

| Folder | Activity | Assigned |
|---|---|---|
| [`01-intro-to-neo4j-cypher/`](01-intro-to-neo4j-cypher/ReadMe.md) | Install Neo4j Desktop and follow Chapter 1 of *Neo4j: The Definitive Guide*; turn in screenshots and impressions. | Per the course schedule |
| [`02-neo4j-music-mcp/`](02-neo4j-music-mcp/README.md) | Connect Claude Code to a prepared, fictional music database through the official Neo4j MCP server; answer two counting questions and verify them outside the model conversation. Includes setup, a Cypher primer, the fixture and its loader, reference queries, tests, and an evidence template. | The [MCP adoption lecture](../module-software-engineering/lectures-instructor-notes/lecture-mcp-adoption.md) in `module-software-engineering/` |

[`neo4j-desktop-mcp-setup.md`](neo4j-desktop-mcp-setup.md) is the general
setup guide: APOC once per instance, one database per activity, the
password in the shell, the `.mcp.json` entry, `/mcp`, writes behind the
permission dialog, and diagnosis by layer. The music homework and every
later Neo4j activity link to it; `resources/` holds its screenshots.

The music homework's instructor key is not in this folder. It lives with the
lecture that launches the homework, at
[`module-software-engineering/demos/lecture-mcp-adoption/neo4j-music-instructor-key/`](../module-software-engineering/demos/lecture-mcp-adoption/neo4j-music-instructor-key/README.md).
`export_students.py` in the homework folder copies the student package alone
into an empty directory.
