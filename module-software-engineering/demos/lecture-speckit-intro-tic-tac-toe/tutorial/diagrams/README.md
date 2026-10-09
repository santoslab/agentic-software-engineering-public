# Tutorial diagram sources

The Mermaid `.mmd` files here are the editable sources of the diagrams in
`../speckit-walkthrough.md`; the `.svg` files are the rendered output and are tracked
so the tutorial renders on GitHub without a build. After editing a source, re-render it
and commit the `.svg` with it:

```sh
npx -y @mermaid-js/mermaid-cli -i NAME.mmd -o NAME.svg
```

Each file starts with the `%%{init: ...}%%` block copied from
`../../../../../weeks-01-03/slides/diagrams/agent-loop.mmd`, which sets the course palette
(`#beaefc` fill, `#310066` text, borders and lines).
