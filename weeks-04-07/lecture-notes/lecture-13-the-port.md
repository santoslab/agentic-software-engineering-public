# Lecture 13 — The Port: Spec as a Cross-Language Contract

> Week 7, meeting 1 of 2. Companion reading for the lecture; self-contained.
> Launches **Stage D** — the TypeScript port. Half a week; Stage E launches
> Thursday.

## The document that crossed

Lecture 04 ended on a punchline you are about to live. The 9x9 game's ConOps —
written during a Python project — was handed to a fresh session with a new
target: Java. Out came a Maven project with JUnit tests and a 100% branch
coverage gate enforced by the build, implementing the same game. The Python
prompts could not have made that trip; they are soaked in Python. The document
crossed because it never mentioned a language.

*Specs are portable; prompts are not.* This week the claim gets tested against
**your** SPEC.md: the engine and AI, rebuilt in TypeScript, in a language most
of you have never written, proven equivalent to your Python not by argument but
by a fixture file that both implementations must satisfy. If your spec cannot
survive the trip, that is not failure — that is the *finding*, and fixing the
spec is most of the deliverable.

## What porting interrogates

A port is an interrogation of your spec: every implicit Python-ism must become
an explicit decision. Here is the exchange we will dwell on, because it is the
purest case in the codebase. Python's coordinate guard:

```python
def _is_valid_coord(value):
    return isinstance(value, int) and not isinstance(value, bool) \
        and 1 <= value <= BOARD_SIZE
```

Why the boolean clause? Because in Python, `True` *is* an integer — `True == 1`,
and `board[True - 1]` cheerfully indexes row zero. The guard exists to slam a
door Python leaves open.

Now the TypeScript side. There is no `isinstance`, there is no int type at all —
only `number`. The equivalent guard:

```typescript
function isValidCoord(value: number): boolean {
    return Number.isInteger(value) && value >= 1 && value <= BOARD_SIZE;
}
```

A boolean cannot even *arrive* here — `tsc` rejects the call at compile time.
But a float can, which Python's `isinstance(int)` made impossible — hence
`Number.isInteger`, guarding a door *TypeScript* leaves open that Python
doesn't.

Same contract, different doors, different locks. And here is the lesson for
your spec: it must say

> Row and column are integers from 1 to N; any other value is rejected.

and it must **not** say "the implementation checks isinstance." The spec states
the contract; the mechanism is each language's own business. When you catch
yourself porting a *mechanism* — translating `isinstance` literally instead of
asking what door it locks — that is the signal that your spec failed to state a
contract, and the fix belongs in SPEC.md, not in cleverer translation.

## Differential testing: equivalence as a file

"The TypeScript version behaves the same" is not a claim you can eyeball. Stage
D makes it mechanical with the oldest trick in the verification book:
**differential testing** — two implementations, one set of inputs, outputs must
agree.

The shared fixtures (`student-materials/fixtures/scenarios.json`) are named
game scenarios: a move list and the expected outcome, plus rejection cases
(setup, an illegal attempt, the expectation that it is refused and costs
nothing). One excerpt to show the shape:

```json
{
  "name": "x-wins-row-overline",
  "moves": [[1,1],[3,1],[1,2],[3,2],[1,3],[3,3],[1,4],[3,4],[1,6],[3,6],[1,5]],
  "expected_winner": "X"
}
```

(Read it: moves alternate X, O, X, O...; X builds 1,1 to 1,6 with a gap at 1,5
filled last — six in a row, which must win because six contains five. Every
fixture is also a tiny spec quiz.)

You write a loader on each side — a parametrized pytest test, and its
equivalent under the TS runner — so that **the same file, unmodified, runs
against both implementations.** The fixture file becomes a third artifact both
implementations answer to. When they disagree, nobody argues about whose
translation is right; a test is red, and the spec (or a port) is wrong. It is
the spec/code/tests triangle from Stage A, raised one level: contract, two
implementations, shared evidence.

Be precise about what green proves, because Stage D's report asks you to be:
the fixtures cover the *engine contract on the covered scenarios* — win
geometry, turn alternation, rejection behavior. They prove nothing about
rendering, I/O, or performance. Scoping the claim is part of the discipline.

## The compiler joins the gate table

Your gates so far run code to check code. Stage D adds a different species:
`tsc --noEmit` — the TypeScript compiler in strict mode, checking without
building. It is a gate that proves things *about all paths at once*: no null
slips through unhandled, no function is called with a shape it didn't declare,
no case of a union goes unconsidered. Your tests sample the behavior space;
the type checker quantifies over it. Neither subsumes the other — `tsc` will
never notice that your win-check scans the wrong diagonal, and no finite test
suite proves what `strictNullChecks` proves about `winner: Player | null`.

The practical effect you will feel within the hour: strict `tsc` changes what
the agent gets away with. A whole class of plausible-but-wrong generated code
— the class that *runs* until the one input arrives — dies at compile time,
with an error message the agent can read and fix in the same breath. This is
"give Claude the tools to check itself" (the cheat sheet's third principle)
implemented by a compiler, and it is why the scaffold ships with strict mode
on and why turning it down is the one scaffold change the brief prohibits.

## Working where you cannot verify by reading

Most of you cannot yet review TypeScript the way you review Python. The course
put you here on purpose, and the fifth-pass retrospective says why it matters:
*"I can only provide counsel on what I already know."* The agent does not
relieve you of expertise; it spends yours. This stage is training for spending
it well where it runs thin:

- **The agent as tutor, not just producer.** Ask for the diff *explained* —
  "what would a Python programmer misread here?" is the highest-yield prompt
  of the week. You are buying understanding with tokens; it is cheap this
  week and expensive to lack in week 14.
- **Lean on the mechanical evidence.** You cannot fully read the code, but you
  can fully read the gates: fixtures green on both sides, `tsc` clean, the
  engine untouched. Knowing *which claims rest on which evidence* is the
  skill; pass 5 called it out as exactly what got hard when the operator left
  familiar ground.
- **Report honestly.** `STAGE-D-REPORT.md` requires a *what I could not verify
  by reading* section. Naming the limits of your review is not a confession —
  it is the engineering. (And "nothing" is not credible from a first-week
  TypeScript reviewer; the grader has read the fifth-pass critique too.)

One workflow rule ties the week together: **when the port stalls on an
ambiguity, the spec is the bug.** The session asks "what should `check_winner`
return when called again after a win?" and your SPEC.md is silent — stop. Do
not let the port guess; a guess here is Attempt 1's drift bug with a language
boundary in the middle. Fix SPEC.md in its own commit, log the find in
BACKLOG.md, then continue. Each such commit is Stage D succeeding, not
stumbling: the port is the best spec review your document will ever get.

## Stage D, concretely

From the brief: engine + AI + tests only, from the scaffold (`npm test`,
`npm run typecheck`; strict tsconfig — leave it); SPEC.md and fixtures are the
inputs, not `game.py` (resist pasting it — the spec is what is being tested);
all shared scenarios green on both sides, same file; at least one committed
spec clarification (or a report section defending its absence); the honest
report. Pacing: this is a *half-week* stage — the engine is 80 lines of logic;
the learning is the loop, not the volume. Thursday: your program grows a tool
interface.

## Questions to think about

1. The fixtures pass on both sides. A classmate says "so the port is correct."
   Correct the claim to exactly what has been shown — then name the cheapest
   *additional* fixture that would most expand it. (What is your current file's
   biggest blind spot: rejection-after-rejection? tie? first-move-wins-races?)
2. `Number.isInteger` vs `isinstance(value, int) and not isinstance(value,
   bool)`: write the one SPEC sentence that makes both of these *correct
   implementations of the same clause*. Now write the bad spec sentence that
   would have forced a literal translation.
3. Your could-not-verify list has entries. For each: what would move it off
   the list — a test, a reading session, a reviewer — and is that worth doing
   at this scale? (Sometimes the honest answer is no. Say so like an engineer:
   state the risk you are accepting.)
