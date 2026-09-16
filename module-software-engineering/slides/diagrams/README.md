# Diagram sources

Mermaid `.mmd` files in this folder are the editable source of truth for slide
diagrams. `slides/build.sh` renders each one to an `.svg` that the decks embed; the
`.svg` output is a gitignored build artifact.

Copy the `%%{init: ...}%%` block from
`../../../weeks-01-03/slides/diagrams/agent-loop.mmd` so new diagrams use the shared
palette (`#beaefc` fill, `#310066` text, borders, and lines).
