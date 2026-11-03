#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ -e work ]; then
  echo "work already exists; use a fresh extracted bundle" >&2
  exit 1
fi
cp -R starter work
cd work
git init -b 001-five-in-a-row
git var GIT_AUTHOR_IDENT >/dev/null
git config commit.gpgsign false
git config core.hooksPath .git/hooks
npm ci
export PATH="$PWD/node_modules/.bin:$PATH"
uv sync --frozen
uv run pytest
git add .
git commit -m "Import foundational checkpoint for the Beads rendering exercise"
bd init --prefix ttt --non-interactive
printf '\nStarter ready in %s\n' "$PWD"
