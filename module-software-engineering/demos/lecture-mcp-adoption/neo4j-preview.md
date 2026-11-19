# Current music database preview

Use the fictional-music-v1 homework fixture. Prepare its separate instance and
APOC configuration before class using [SETUP.md](../../../neo4j/02-neo4j-music-mcp/SETUP.md).
Show the graph, inspect schema, and run one bounded artist/distinct-playlist query.
Do not install a database during the adoption or dice lecture.

Actual LLM-free results are in the
[instructor capture](../lecture-mcp-neo4j/instructor-key/live.json); the
[answer key](../lecture-mcp-neo4j/instructor-key/README.md) explains interpretation.
The capture includes official provider discovery, schema, both query calls,
and direct reference results checked against a CSV oracle. It does not include
model-selected calls or a final model answer. Use it as a labeled fallback.

Current tested tools are `get-schema` and `read-cypher`, with the launcher
filtering provider exposure and enabling read-only mode. Database requirements
include matching APOC meta procedures and their execution configuration.

The older Neo4j course material and August airport transcript remain historical
authoring sources; they are not this fixture's dataset, installation recipe, or
newly run model evidence. The adoption lecture owns the main preview. The dice
lecture uses only a brief recap to connect consumer evidence to provider tests.
