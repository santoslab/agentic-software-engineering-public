# Lecture 13 — The Port: Spec as a Cross-Language Contract

> **Unit:** weeks-04-07 · **Week 7, meeting 1 of 2** · 75 minutes
>
> **Thesis:** If your spec is real, the engine can be rebuilt in a language you
> don't know and proven equivalent mechanically — and every place the port stalls
> is a spec bug, not a code bug.

## Learning objectives

After this lecture, students can:

1. Set up differential testing: one fixture file, two implementations, loaders on
   both sides, equivalence as a mechanical claim.
2. Use a strict compiler (`tsc --noEmit`) as a new *kind* of gate and say what it
   catches that tests don't.
3. Work productively agent-assisted in an unfamiliar language while writing an
   honest could-not-verify section.
4. Convert a port ambiguity into a committed spec clarification.

## Before class

- [required] TypeScript docs: "TypeScript for JavaScript Programmers" (10 min).
- [required] `student-materials/fixtures/README.md` — the scenario format.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–10 | Cold open: the Java port, revisited | L04's punchline becomes today's assignment. The 9x9 ConOps produced a Java implementation with its own build system and a 100% branch-coverage gate — *the document crossed the language boundary; no prompt could have.* Your SPEC.md now takes the same trip to TypeScript. If it can't make the trip, that's the finding. |
| 10–24 | What porting interrogates | Every implicit Python-ism must become an explicit decision. Worked example, live on the two snippets: `_is_valid_coord` — Python needs `isinstance(int) and not isinstance(bool)` (because `True` *is* an int in Python); TypeScript needs `Number.isInteger` (because there's no int type at all). Neither mechanism is in the spec — and that's correct: the spec says *"row and column are integers 1..N; anything else is rejected"* and each language enforces it its own way. The spec states the contract; the mechanism is the implementation's business. Where students find themselves porting *mechanisms*, the spec has failed to state the contract. |
| 24–36 | Differential testing | The fixture file: named scenarios, move lists, expected outcomes — one JSON file, checked into *both* worlds, loaders on each side (parametrized pytest on one, the TS runner on the other). Why this beats translating the test suite: the fixtures are a *third artifact* both implementations answer to — disagreement between implementations becomes a red test, not an argument. This is the same three-way structure as spec/code/tests, at the cross-language level. |
| 36–50 | Demo 1 — one fixture file, two greens, one ambiguity | Live: run the shared scenarios under pytest (green), then under the TS runner (green). Then the staged find: a scenario exposes a behavior the spec never pinned (what `check_winner` returns when called twice after a win — or whichever ambiguity the instructor staged). Stop. Fix SPEC.md, its own commit. Continue. The port workflow in miniature: **stall → spec fix → proceed**, never stall → guess → diverge. |
| 50–62 | Working where you can't verify by reading | The unfamiliar-tech workflow: the agent as tutor (ask for the diff *explained*, not just produced); the compiler as your first reviewer — `tsc --noEmit` strict catches whole bug classes (null paths, wrong shapes) before any test runs, which is why it's a *gate*, not a convenience. Then the honesty requirement, anchored in the pass-5 quote from L06 — *"I can only provide counsel on what I already know"* — your STAGE-D-REPORT's could-not-verify section names what you accepted on the strength of gates alone. That's not a confession; it's engineering: knowing which claims rest on which evidence. |
| 62–75 | Stage D walkthrough + Q&A | Scaffold tour: `package.json` scripts (`test`, `typecheck`), strict `tsconfig`; scope discipline (engine + AI + tests, nothing else); the SPEC-is-source rule (resist pasting Python in — the spec and fixtures are the inputs); expected spec finds logged in BACKLOG.md. Pacing: this is a half-week stage — Thursday launches Stage E. |

## Demos

### Demo 1 — One fixture file, two greens, one ambiguity

- **Artifacts:** instructor's Stage D repo: Python side with fixture loader; TS
  side from the scaffold, complete; `fixtures/scenarios.json`; one scenario
  designed to expose the staged spec ambiguity.
- **Setup (before class):** both suites green in rehearsal; `npm install` done
  (never live); the ambiguous scenario prepared but not yet in the fixture file —
  it gets added on stage.
- **Script:** (1) `pytest` on the fixture loader — green, N scenarios; (2)
  `npm test` — green, same N; hold the beat: *same file*; (3) add the prepared
  edge scenario; (4) one side disagrees with the other, or the expected value is
  unwritable — either way the spec is silent; (5) open SPEC.md, write the clause,
  commit it alone; (6) set the fixture expectation, both sides green again.
- **Expected outcome:** equivalence experienced as a mechanical, file-backed
  claim; the stall → spec fix → proceed loop performed once in full.
- **Fallback:** recorded run; the fixture file + both green outputs work as
  slides, and the ambiguity beat survives as a two-slide diff story.

## Discussion prompts

1. The fixtures pass in both implementations. State precisely what has and has
   *not* been proven. (Equivalence on the covered scenarios — nothing about
   rendering, I/O flow, or performance; fixtures are the engine's contract only.)
2. `tsc` strict vs the pytest suite: name a bug each catches that the other
   structurally cannot.
3. Your could-not-verify list has an entry. What would it take to *move* it off
   the list — and is it worth it at this scale?

## Assigned after class

- Readings (for L14):
  - [required] MCP docs: core concepts (host/client/server, tools) + the FastMCP
    quickstart.
  - [required] `student-materials/mcp-example/README.md`.
- Project: **Stage D** launched today; due mid-week so Stage E gets its half.

## Instructor notes

- **Cut if running long:** the 10–24 block can drop to the single
  `_is_valid_coord` example (it carries the whole argument); the workflow block
  (50–62) must keep the could-not-verify framing — it's graded in Stage D.
- **Risks:** never run `npm install` live. The staged ambiguity must be genuinely
  underdetermined by the spec students have seen, or the beat feels rigged —
  `check_winner` twice-after-win works because the starter's spec-from-code
  session (L07) usually leaves it open. TS-experienced students may finish Stage D
  fast: point them at the stretch (property-based fixture generation) rather than
  letting them expand scope.
- **Variants:** if a student volunteers their Stage A spec, run the 36–50 demo's
  ambiguity hunt against *their* SPEC.md live (with consent) — finding the gap in
  a real student artifact lands harder than the staged one.
