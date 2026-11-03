# Contract: Engine public API

**Module**: `five_in_a_row.engine` | **Depends on**: nothing (standard library only)

The engine owns the rules: board, turns, legal moves, win and draw. It does no I/O and
knows nothing about who is playing. Everything listed here is importable from
`five_in_a_row.engine`; anything else in the package is private and may change without
notice. Entity details: [data-model.md](../data-model.md#engine-entities).

## Constants

| Name | Value | Meaning |
|------|-------|---------|
| `SIZE` | `9` | Rows and columns on the board (FR-001). |
| `WIN_LENGTH` | `5` | Marks in a line needed to win; a longer line also wins (FR-008). |

## Types

```python
class Mark(Enum):
    X = "X"
    O = "O"
    def other(self) -> "Mark": ...

@dataclass(frozen=True, slots=True)
class Square:
    row: int    # 1..SIZE expected; other values are rejected by GameState.play
    col: int

class Result(Enum):
    IN_PROGRESS, X_WON, O_WON, DRAW

class Board:                      # immutable
    def at(self, square: Square) -> Mark | None: ...      # raises ValueError if off-board
    def empty_squares(self) -> tuple[Square, ...]: ...    # row-major order
    def is_full(self) -> bool: ...

class IllegalMoveReason(Enum):
    GAME_OVER, OUT_OF_RANGE, OCCUPIED

class IllegalMove(Exception):
    reason: IllegalMoveReason
    square: Square

class GameState:                  # immutable
    board: Board
    turn: Mark
    result: Result
    last_move: Square | None
    @classmethod
    def new(cls) -> "GameState": ...
    def play(self, square: Square) -> "GameState": ...
    @property
    def winner(self) -> Mark | None: ...   # X for X_WON, O for O_WON, else None
```

## Behavior

### `GameState.new()`

Returns a state with an empty board, `turn == Mark.X`, `result == IN_PROGRESS`,
`last_move is None` (FR-001, FR-002).

### `GameState.play(square)`

**Pre**: none (all checking is done here).

**On rejection** raises `IllegalMove` with the first matching reason, in this order, and
leaves `self` unchanged (it is immutable) — FR-005:

1. `GAME_OVER` — `self.result != IN_PROGRESS`.
2. `OUT_OF_RANGE` — `square.row` or `square.col` not in `1..SIZE`.
3. `OCCUPIED` — `self.board.at(square) is not None`.

**On acceptance** returns a new state `s` where:

- `s.board` equals `self.board` with `self.turn` placed at `square`; every other square
  is unchanged.
- `s.last_move == square`.
- `s.result` is
  - `X_WON`/`O_WON` (for `self.turn`) if `square` now lies on a line of `WIN_LENGTH` or
    more consecutive `self.turn` marks in any of the four directions (FR-008);
  - otherwise `DRAW` if `s.board.is_full()` (FR-010);
  - otherwise `IN_PROGRESS`.
- `s.turn == self.turn.other()` (FR-003). (After a terminal result, `turn` is not
  meaningful; callers use `result`.)

## Evidence expected (tests in `tests/engine/`)

| Contract clause | Spec IDs |
|-----------------|----------|
| `new()` fields | FR-001, FR-002 |
| alternation | FR-003, US1-2 |
| each rejection reason; state unchanged | FR-005, SC-006 |
| win in each of the four directions | FR-008, US1-3, US1-4, US1-5 |
| six-in-a-row by filling a gap | FR-008, US1-6 |
| two lines completed at once → one win | Edge Cases |
| win on the last square is a win | FR-010, Edge Cases |
| draw on full board without a win | FR-010, US1-7 |
| `play` after a terminal result → `GAME_OVER` | FR-009 |
| no false wins: four in a line, five broken by a gap or by the other mark | SC-003 |
