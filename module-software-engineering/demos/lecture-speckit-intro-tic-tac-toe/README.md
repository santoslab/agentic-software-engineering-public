# Five-in-a-Row Tic-Tac-Toe

Tic-tac-toe on a 9×9 board where five or more marks in a line — across, down, or
diagonal — wins. Play in a terminal against a computer that picks random squares, or with
a friend at the same keyboard. Type a square as row then column, e.g. `4 7`; type `m` to
leave a game.

## Run the game

```sh
uv run five-in-a-row          # or: uv run python -m five_in_a_row
```

Requires Python 3.12 or later and [`uv`](https://docs.astral.sh/uv/). Without `uv`, see
the fallback in [quickstart.md](specs/001-five-in-a-row/quickstart.md#prerequisites).

## Run the tests

```sh
uv run pytest
```

Each test is tagged with the specification IDs it is evidence for. Every run writes
`reports/conformance.md` (not committed), listing each requirement, acceptance scenario,
success criterion and edge case in the spec with its tests and status.

## Documents

- [Specification](specs/001-five-in-a-row/spec.md) — what the game must do
- [Implementation plan](specs/001-five-in-a-row/plan.md) — engine, opponent and CLI
  modules and how they depend on each other
- [Quickstart](specs/001-five-in-a-row/quickstart.md) — how to validate the game
- [Constitution](.specify/memory/constitution.md) — development rules for this project
