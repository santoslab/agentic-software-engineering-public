# Shared Differential-Test Fixtures

`scenarios.json` is the third artifact both of your engine implementations answer
to (Lecture 13). Copy it into your project repo at `fixtures/scenarios.json` and
write a loader on each side. **The file is never modified to make a test pass** —
if an expectation looks wrong, that is a spec conversation, not an edit.

Baseline rules pinned by these fixtures: 9x9 board, win length 5, X moves first,
players alternate on every *accepted* move. If your Stage A extension made the
geometry configurable, run the fixtures against the 9x9/5 configuration.

## Loader contract

**Games** (`games` array): starting from a fresh game, play `moves` in order via
your move function. Every listed move must be **accepted**. After each move, run
winner detection; no scenario produces a winner before its final move. After the
final move, the winner must equal `expected_winner` (`"X"`, `"O"`, or `null` for
no winner yet).

**Rejections** (`rejections` array): starting from a fresh game, play
`setup_moves` (all accepted), then submit `attempt`. The attempt must be
**rejected**, and after the rejection: the board is unchanged and it is still the
same player's turn.

## Sketch of the Python side

```python
import json, pytest
from game import Game

SCENARIOS = json.load(open("fixtures/scenarios.json"))

@pytest.mark.parametrize("s", SCENARIOS["games"], ids=lambda s: s["name"])
def test_game_scenario(s):
    g = Game()
    for row, col in s["moves"]:
        assert g.make_move(row, col), f"move ({row},{col}) was rejected"
        winner = g.check_winner()
    assert winner == s["expected_winner"]
```

(The intermediate no-winner assertion and the rejections loader are yours to
write — and the TypeScript side must make the same claims under `vitest`.)

## Known gap — on purpose

There is no **tie** scenario: filling all 81 cells with no five-in-a-row is
genuinely hard to construct by hand, which is itself worth noticing. Options if
you want the coverage: generate one programmatically and *verify it against your
spec* before trusting it, or — if your Stage A extension made geometry
configurable — a 3x3 tie is nine moves. Either way, document what you did (or
didn't) in your Stage D report. A fixture set's blind spots are part of its
contract.
