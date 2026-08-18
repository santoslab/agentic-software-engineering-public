---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
  }
  section.lead {
    background: #310066;
    color: #ffffff;
  }
  section.lead h1, section.lead h2 {
    color: #ffffff;
  }
  section.standout {
    background: #beaefc;
    color: #310066;
    text-align: center;
    font-size: 36px;
  }
  h1, h2 {
    color: #310066;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->

# The Port: Spec as a Cross-Language Contract

**Agentic Software Engineering — Lecture 13**
Week 7 · Meeting 1 of 2 · launches **Stage D** (half-week)

---

## The one idea

If your spec is real, the engine can be rebuilt in a language you don't know and **proven equivalent mechanically.**

Where the port stalls, you found a **spec bug**, not a code bug.

---

## The document that crossed

The 9x9 ConOps — written during a *Python* project — was handed to a fresh session targeting **Java**. Out came Maven, JUnit, a 100% branch gate, the same game.

The Python prompts could not have made that trip. They are soaked in Python.

**Specs are portable; prompts are not.**

This week the claim is tested against *your* SPEC.md.

<!-- 0-10 min. -->

---

## Same contract, different doors

```python
def _is_valid_coord(value):                      # Python
    return isinstance(value, int) and not isinstance(value, bool) \
        and 1 <= value <= BOARD_SIZE
```

Why the bool clause? In Python, `True == 1` — `board[True - 1]` indexes row zero.

```typescript
function isValidCoord(value: number): boolean {  // TypeScript
    return Number.isInteger(value) && value >= 1 && value <= BOARD_SIZE;
}
```

A boolean can't even *arrive* (tsc rejects the call). But a **float** can — a door Python's `isinstance(int)` had locked.

---

<!-- _class: standout -->

## The spec states the **contract**.
## The mechanism is each language's business.

*"Row and column are integers 1 to N; anything else is rejected."*

Porting a mechanism instead of a contract = the spec failed to state one. **Fix SPEC.md.**

<!-- 10-24 min. This is the lecture's center of gravity. -->

---

## Differential testing: equivalence as a file

`fixtures/scenarios.json` — named scenarios, move lists, expected outcomes:

```json
{ "name": "x-wins-row-overline",
  "moves": [[1,1],[3,1],[1,2],[3,2],[1,3],[3,3],[1,4],
            [3,4],[1,6],[3,6],[1,5]],
  "expected_winner": "X" }
```

(Read it: X builds 1,1-1,6 with the gap filled last. Six contains five. Every fixture is a tiny spec quiz.)

One file → a loader on each side → **the same file, unmodified, green in both worlds.**

Disagreement becomes a red test, not an argument.

<!-- 24-36 min. Green proves: engine contract, covered scenarios. NOT rendering, I/O, performance. Scope the claim. -->

---

<!-- _class: standout -->

## Demo: two greens, one ambiguity

pytest green → vitest green → *same file* →
a new scenario the spec can't answer → **stop → fix SPEC.md → continue**

<!-- 36-50 min. stall → spec fix → proceed. Never stall → guess → diverge. -->

---

## The compiler joins the gate table

`tsc --noEmit`, strict — a gate that proves things **about all paths at once**:

- Your tests *sample* the behavior space
- The type checker *quantifies* over it (`winner: Player | null` — every unhandled null dies at compile time)

Neither subsumes the other: `tsc` will never notice a wrong diagonal; no finite suite proves what `strictNullChecks` proves.

**Felt effect:** the plausible-but-wrong code class — the kind that runs until the one input arrives — dies before running. *Give Claude the tools to check itself*, implemented by a compiler.

<!-- 50-62 min intro. Strict mode stays on — the one prohibited scaffold change. -->

---

## Working where you can't verify by reading

> *"I can only provide counsel on what I already know."* — pass 5

- **Agent as tutor**: "what would a Python programmer misread here?" — the highest-yield prompt of the week
- **Lean on mechanical evidence**: you can't fully read the code; you *can* fully read the gates
- **Report honestly**: `STAGE-D-REPORT.md` requires *what I could not verify by reading* — naming limits is the engineering, not a confession

("Nothing" is not credible from a first-week TypeScript reviewer.)

---

## Stage D checklist (from the brief)

- [ ] Engine + AI + tests only, from the scaffold; strict stays on
- [ ] `npm test` green **and** `npm run typecheck` clean
- [ ] Shared scenarios green on **both** sides — same file, unmodified
- [ ] Inputs are SPEC.md + fixtures — **not `game.py`**
- [ ] At least one committed spec clarification (or defend its absence)
- [ ] The honest report

Half-week stage: the engine is ~80 lines of logic. **The learning is the loop, not the volume.**

---

## Questions to think about

1. "Fixtures pass, so the port is correct" — repair that claim to exactly what was shown, then name the cheapest fixture that most expands it.
2. Write the one SPEC sentence that makes `Number.isInteger` and the `isinstance` pair both *correct implementations* — then the bad sentence that forces literal translation.
3. For each could-not-verify entry: what would move it off the list, and is it worth it *at this scale*? (Sometimes no — say so like an engineer.)

---

## Before Thursday

- [required] MCP docs: core concepts + FastMCP quickstart
- [required] `student-materials/mcp-example/README.md`

**Thursday: your program becomes something an agent can act *with*.**
