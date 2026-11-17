# Diagram sources

Mermaid `.mmd` files in this folder are the editable source of truth for slide
diagrams. `slides/build.sh` renders each one to an `.svg` that the decks embed.
The `.svg` files are tracked, so the decks and the repository view render without
a build; re-run `build.sh` after editing a source and commit the `.svg` with it.
The slide `.pdf` and `.html` outputs are the gitignored build artifacts.

Copy the `%%{init: ...}%%` block from
`../../../weeks-01-03/slides/diagrams/agent-loop.mmd` so new diagrams use the shared
palette (`#beaefc` fill, `#310066` text, borders, and lines).

`music-graph.svg` is also shipped as a tracked copy at
`../../../neo4j/02-neo4j-music-mcp/assets/music-graph.svg`, so the homework's
Cypher primer renders without this folder. `build.sh` does not refresh that copy:
when `music-graph.mmd` changes, re-render and copy the `.svg` there by hand.
