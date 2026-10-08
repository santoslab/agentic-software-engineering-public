# Data Model: Five-in-a-Row Tic-Tac-Toe

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Date**: 2026-10-08

Entities from the spec's *Key Entities*, refined with the fields and rules the design
needs. The column **Owner** says which module defines the entity (see
[research.md R3](research.md#r3-separating-engine-opponent-and-cli-so-each-can-evolve-independently)).
Engine entities are immutable values (R4).

## Engine entities

### Mark — owner: engine

| Field | Values | Rule |
|-------|--------|------|
| value | `X`, `O` | `X` moves first in every game (FR-002). |

Operation: `other()` — the opposite mark.

### Square — owner: engine

| Field | Type | Rule |
|-------|------|------|
| row | integer | 1–9; 1 is the top row (FR-004). |
| col | integer | 1–9; 1 is the leftmost column (FR-004). |

Two squares are equal when row and col are equal. A `Square` with a value outside 1–9 can
be *described* (so the CLI can report "out of range"), but the engine rejects it in
`play` (FR-005).

### Board — owner: engine

| Field | Type | Rule |
|-------|------|------|
| cells | 9×9 grid of `Mark` or empty | All empty at the start of every game (FR-001). |

Operations: `at(square) -> Mark | None`; `empty_squares() -> tuple[Square, ...]` in
row-major order; `is_full()`.
Invariant: a square, once holding a mark, never changes within a game.

### Line — owner: engine (internal)

A run of consecutive squares in one of four directions: row (0, +1), column (+1, 0),
diagonal (+1, +1), anti-diagonal (+1, −1). Used only inside win detection (R5); not part
of the public API.

### Result — owner: engine

| Value | Meaning |
|-------|---------|
| `IN_PROGRESS` | Moves may still be played. |
| `X_WON` / `O_WON` | That mark made five or more in a line (FR-008). |
| `DRAW` | The last empty square was filled without a win (FR-010). |

### GameState — owner: engine

| Field | Type | Rule |
|-------|------|------|
| board | `Board` | |
| turn | `Mark` | Whose move it is. Starts `X`; alternates after each accepted move (FR-003). |
| result | `Result` | Derived from the last move; `IN_PROGRESS` at the start. |
| last_move | `Square` or none | The square most recently played; none at the start. |

**Validation of `play(square)`** — rejected, with the state unchanged (FR-005), when:

| Reason | Condition |
|--------|-----------|
| `GAME_OVER` | `result` is not `IN_PROGRESS`. |
| `OUT_OF_RANGE` | row or col outside 1–9. |
| `OCCUPIED` | the square already holds a mark. |

**State transitions**:

```text
          play(sq) accepted, no win, board not full
        ┌───────────────────────────────┐
        ▼                               │
  ┌─────────────┐  play wins   ┌──────────────┐
  │ IN_PROGRESS │─────────────▶│ X_WON / O_WON│   (terminal)
  └─────────────┘              └──────────────┘
        │ play fills last square, no win
        ▼
  ┌─────────────┐
  │    DRAW     │   (terminal)
  └─────────────┘
```

A win is checked before fullness, so a win on the last square is a win, not a draw
(spec Edge Cases). A terminal state accepts no further moves.

## Opponent entities

### Opponent — owner: opponent

A strategy that, given a `GameState` that is `IN_PROGRESS`, returns an empty `Square`.
It holds no reference to the CLI and never changes the state it is given. The only
strategy in this feature is `RandomOpponent` (FR-012): uniform choice among
`empty_squares()`, using an injectable random generator (R6).

## CLI entities

These live only in the CLI and are not visible to the engine or opponent.

### Mode

`VS_COMPUTER` or `TWO_PLAYER` (FR-011).

### Session

The CLI's memory across games between visits to the start menu.

| Field | Type | Rule |
|-------|------|------|
| mode | `Mode` | Set when the player picks from the start menu. |
| human_mark | `Mark` | `VS_COMPUTER` only. `X` when the mode is chosen from the start menu; flipped on each "play again" (FR-013). |

**Transitions**:

```text
           ┌──────────── quit ─────────────▶ (program ends)
           │
  ┌────────────┐ pick mode  ┌─────────┐ game ends ┌────────────┐
  │ START_MENU │───────────▶│ PLAYING │──────────▶│ GAME_OVER  │
  └────────────┘            └─────────┘           └────────────┘
     ▲      ▲                  │   ▲                 │      │
     │      └── leave (m) ─────┘   └── play again ───┘      │
     │                              (VS_COMPUTER: flip      │
     │                               human_mark)            │
     └─────────────────── back to start menu ───────────────┘
                           (human_mark reset to X on next pick)
```

Leaving with `m` shows no result and offers no "play again" (FR-018; spec Assumptions).
End of input or interrupt in any state ends the program (FR-020).
