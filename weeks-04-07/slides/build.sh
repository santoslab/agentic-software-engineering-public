#!/bin/sh
# Build the lecture slide decks (Marp). Needs node; PDF export needs Chrome.
# PDFs/HTML are build artifacts (gitignored) — rebuild on demand.
set -e
cd "$(dirname "$0")"

# Diagrams: Mermaid sources -> SVG (same node+Chrome stack as Marp).
# Keep diagrams as .mmd text — agent-maintainable, renders in GitHub/Obsidian;
# slides include the pre-rendered SVG.
for d in diagrams/*.mmd; do
  [ -e "$d" ] || continue
  npx -y @mermaid-js/mermaid-cli -i "$d" -o "${d%.mmd}.svg"
  echo "rendered ${d%.mmd}.svg"
done

# Decks. --allow-local-files is required for local images (diagrams/*.svg) in
# PDF export. The HTML output is standalone: present from it directly in a
# browser (press P for presenter view with the HTML-comment speaker notes).
for f in lecture-*.md; do
  [ -e "$f" ] || continue
  npx -y @marp-team/marp-cli@latest --allow-local-files "$f" -o "${f%.md}.pdf"
  npx -y @marp-team/marp-cli@latest --allow-local-files "$f" -o "${f%.md}.html"
  echo "built ${f%.md}.pdf and .html"
done
