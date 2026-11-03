# Contract: Computer opponent

**Module**: `five_in_a_row.opponent` | **Depends on**: `five_in_a_row.engine` public API only

The opponent decides where the computer moves. It does not place the mark, print
anything, or keep game state; the CLI asks it for a square and plays that square through
the engine. Replacing the strategy (ConOps §4, "a smarter computer opponent") means adding
a class that satisfies `Opponent` — nothing in the engine or CLI changes.

## Interface

```python
class Opponent(Protocol):
    def choose_move(self, state: GameState) -> Square: ...

class RandomOpponent:
    def __init__(self, rng: random.Random | None = None) -> None: ...
    def choose_move(self, state: GameState) -> Square: ...
```

## `Opponent.choose_move(state)` — applies to every strategy

**Pre**: `state.result == Result.IN_PROGRESS` (so at least one square is empty).

**Post**:

- returns a `Square` with `state.board.at(square) is None` — so `state.play(square)` is
  always accepted (FR-012, SC-004);
- does not depend on, or change, anything outside `state` and the opponent's own fields;
- needs no player input (FR-012).

Calling it with a terminal state raises `ValueError`.

The opponent is told nothing about which mark it holds: it is always `state.turn`.

## `RandomOpponent`

- Chooses uniformly at random among `state.board.empty_squares()` — every empty square is
  equally likely (FR-012) — via `rng.choice`.
- `rng` defaults to a new, unseeded `random.Random()`. Tests pass a seeded instance so
  runs are repeatable (research.md R6).

## Evidence expected (tests in `tests/opponent/`)

| Contract clause | Spec IDs |
|-----------------|----------|
| 1,000 moves across random positions are all onto empty squares | FR-012, SC-004, US2-3 |
| same 10-empty-square position, 1,000 trials, each square chosen ≥ 1 time | FR-012, SC-004, US2-3 |
| terminal state → `ValueError` | (contract only) |
| does not mutate `state` (compare before/after) | (contract only) |
