# Stage D Scaffold — TypeScript Engine Port

Copy this folder into your project repo as `ts/` (so the fixtures at
`fixtures/scenarios.json` are reachable at `../fixtures/scenarios.json`), then:

```sh
cd ts
npm install          # once; needs Node LTS (one download from nodejs.org)
npm test             # vitest
npm run typecheck    # tsc --noEmit, strict
```

Suggested layout (create as you go):

```
ts/
  src/game.ts          # the engine
  src/computerAi.ts    # the AI
  tests/fixtures.test.ts   # the shared-scenario loader (Lecture 13)
  tests/...                # any additional unit tests
```

## Rules of the scaffold

- **Strict mode stays on.** `strict` and `noUncheckedIndexedAccess` in
  `tsconfig.json` are part of the gate, not a suggestion — turning them down is
  the one scaffold change the brief prohibits. `noUncheckedIndexedAccess` will
  force you to handle `board[r][c]` being possibly undefined; that is the
  compiler asking a question your spec should answer (what *are* the legal
  indices?).
- **Both scripts are gates:** `npm test` green and `npm run typecheck` clean at
  stage end.
- `resolveJsonModule` is on, so the fixture file can be imported directly if you
  prefer that to `fs` — either is fine; the loader contract in
  `fixtures/README.md` is what matters.

## Inputs

Your **SPEC.md** and the **shared fixtures** — not `game.py`. Where the spec
turns out to be silent, the workflow is: stop, fix SPEC.md in its own commit,
log the find in BACKLOG.md, continue (Lecture 13).
