# Restore a recorded state

Each archive contains a `work/` project snapshot with its Git history and Beads store. Choose a state from the [checkpoint list](transcript.md#checkpoint-states), then extract it into a new directory:

```sh
mkdir -p /tmp/beads-checkpoint
tar -xzf states/09-after-milestone.tar.gz -C /tmp/beads-checkpoint
cd /tmp/beads-checkpoint/work
npm ci
export PATH="$PWD/node_modules/.bin:$PATH"
uv sync --frozen
git log --oneline -5
bd --readonly --sandbox info
bd --readonly --sandbox list --all
uv run pytest
```

Replace `09-after-milestone.tar.gz` with another archive name to inspect an earlier state. The archive includes the working source, `.git`, `.beads`, and `run-session.py` at its root; the outer bundle supplies the exact prompts. No transcript, stderr capture, authentication diagnostic, or full CLI metadata is duplicated inside the checkpoints. The failed authentication attempt is documented in `transcript.md` but its checkpoint is withheld.
`bd` is the version locked by `package-lock.json`; no globally installed copy is required. The `run-session.py` helper is at the extracted archive root.

These steps extract a sanitized derivative. They do not overwrite the historical source archives.
