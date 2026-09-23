# Lecture 04 — Verifying a Game: Tests as Executable Specification

> **Unit:** module-software-engineering · **Module week 2, meeting 2 of 2** · 75 minutes
>
> **Thesis:** A test suite is a specification a program can check; coverage
> tells you which code the suite's claims reach, not whether the claims are
> right — and the process makes both facts visible.

## Learning objectives

After this lecture, students can:

1. Write a test that cites the clause it verifies, and explain why it may assert
   tighter than the clause but never looser (VER-6).
2. Read a branch-coverage report and distinguish branch coverage — a property of
   (tests, code) — from clause coverage — a property of (tests, specification)
   (VER-8).
3. Given a green gate, list what it does and does not establish, citing VER-2
   and the scope lines of RPT-2.
4. Explain why a fixture file is an executable specification and why it is never
   edited to make a test pass (VER-7).
5. Classify a change to a realization as a repair, a conformance-preserving
   change, or a change of specified behavior (DEV-2), and say what the history
   must show for each.

## Before class

Assigned at Lecture 03:

- [required] `process/verification.md` at its L04 level (VER-5 through VER-8):
  `../demos/lecture-03-game-demo/reference/process/verification.md`.
- [required] The fixtures README: `../demos/lecture-03-game-demo/reference/fixtures/README.md`.
- [recommended] coverage.py on branch coverage.
- Exercise 2 is due before this meeting.

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–6 | Where we are; extending the process documents | The specification family; `t3` exists. The three kinds of verifier on code: a human reads code against the spec; an agent reviews; the algorithmic verifier is tests + coverage + static types. Today `process/verification.md` goes from 1.2 to 1.3 — VER-5 through VER-8 arrive by an RPT-3 amendment, approved, committed (Demo 1). A process document changes the way a specification does. |
| 6–20 | Tests as executable specifications | VER-6 line by line: every test cites its clause (AUD-5 applied to tests); tighter never looser — the specification is the floor; direct assignment for *setup* only, the public operation for *behavior*; a test that cannot fail is not a test (the 3×3 suite's seeded-RNG story). Parametrize: one clause, many realizations. SPECS §9 is *obligations* (AUD-14): clause → obligation → test, readable off the suite. Show three tests from the reference with their citations. |
| 20–38 | Demo 2 — the gate, then sabotage (`t4`) | Run the VER-4 command; read term-missing; branch versus line on one `if`; the single pragma (VER-5). Delete the test that claims §4.1's overline clause → the gate is still green (VER-8). Flip one entry of the direction table → the diagonal tests fail; the gate returns the work (RPT-4); restore. Third step: a test whose expected string is wrong passes wrong code — who verifies the verifier (VER-1). |
| 38–50 | Why coverage is not conformance | The VER-2 table by kind. RPT-2's scope lines applied to a test run: which suite (commit), which SPECS version, which clauses claimed. RPT-5 reports clause coverage separately from the gate. L01's six invalidity modes, for code: stale version; wrong expectation; memory; clauses no test claims; attention; a defective S. DEV-2's three kinds, on what the class just saw: the direction flip repaired (a); a refactor that would keep every test green (b); the after-game-over rejection, which needed an amendment first (c). |
| 50–62 | Demo 3 — executable specifications that outlive the code (`t5`) | `fixtures/scenarios.json`: the shape; a ten-line loader; run it. The deliberate tie gap — "a fixture set's blind spots are part of its contract" (VER-7). The same file will run against an engine in another language: the port, previewed. The oracle idea: the obvious implementation is the specification for the clever one. The Java port as evidence — ConOps → Java, JaCoCo at 100%. |
| 62–72 | Close | Reversi: the specification-family table, unfilled, and one line on what each kind will demand (the pass; the opening; flips as a postcondition; hints as a display decision). L05 is the walkthrough; L06 is MCP. |

Blocks sum to 72 minutes; 3 minutes slack.

## Demos

### Demo 1 — The process amendment

- **Artifacts:** `t3` with the L03 `process/`; the L04 set in
  `../demos/lecture-03-game-demo/reference/` (`CLAUDE.md`, `process/README.md`,
  `process/reporting.md`, `process/verification.md`); the pre-written RPT-3
  proposal in `../demos/lecture-03-game-demo/demo-script-lecture-04.md`.
- **Setup (before class):** the proposal in a text file; the diff rehearsed.
- **Script:** show the proposal (thirty seconds); approve; apply; `git diff` the
  changelog; commit `process: verification 1.2 -> 1.3 (VER-5..8)`.
- **Expected outcome:** students see DEV-3 applied to a process document — the
  rules that govern the rules change by the same mechanism.
- **Fallback:** show the diff from the rehearsal repository.

### Demo 2 — The gate, then sabotage

- **Artifacts:** `t4` (tests citing §; the gate green); the names of the overline
  test and the direction table noted from rehearsal; the wrong-expected-string
  test on a scratch branch.
- **Setup (before class):** a venv with `pytest-cov` installed and the gate
  verified green on the presentation machine *that day*; `PYTHONDONTWRITEBYTECODE=1`
  and no `__pycache__` (the flip keeps the file size; a stale cache hides it);
  the three sabotage edits scripted (`git checkout --` restores each).
- **Script:** (1) gate, read the report; (2) delete the overline test, gate:
  100%; (3) restore; flip the up-right scan (`c + i` → `c - i`), gate: two
  failures — the up-right test and the tie test — exit 1; the RPT-2 report;
  the ruling; (4) restore; check out the scratch branch: a wrong expectation,
  gate green; (5) restore. Each step ends with a sentence that states what the
  gate did and did not establish. The script's table has the verified results.
- **Expected outcome:** three green-or-red results whose meaning differs, and the
  vocabulary (VER-2, VER-8, RPT-2 scope) to say how.
- **Fallback:** captures of each step; the point is visible on stills.

### Demo 3 — Fixtures

- **Artifacts:** `t5` (`fixtures/scenarios.json`, `fixtures/README.md`, and
  `tests/test_fixtures.py`, as in `../demos/lecture-03-game-demo/reference/`).
- **Script:** open the file; run the loader tests; point at the README's
  known-blind-spots section; one sentence on the port.
- **Fallback:** recorded; the run is seconds.

## Discussion prompts

1. After the overline test is deleted the gate is green. What, exactly, is still
   verified about §4.1 — and what is not?
2. The fixtures have no tie scenario, on purpose. Is that a defect in the
   specification, in the realization, or in the verifier? What does VER-7 say a
   fixture file owes you instead?
3. Classify under DEV-2: replacing the 81-cell scan with a check around the last
   move; fixing tie-versus-win precedence; adding the after-game-over rejection.
   Which needs an amendment first, and what does each commit message have to say?

## Assigned after class

- Readings (for L05): [required] the Project 1 brief
  (`../project-1-reversi-brief.md`) in full; [required] the Reversi
  `CONOPS-sketch.md` (`../student-materials/reversi-starter/`; five minutes —
  read it as a player, not an implementer). Do not read the rules of Reversi
  elsewhere; L05 learns them from the sketch.
- Exercise: Ex. 3 (optional) continues.

## Instructor notes

- **Cut if running long:** Demo 3 compresses to the loader run and one sentence
  on the port; the "coverage is not conformance" block compresses to the VER-2
  table and the RPT-2 scope lines. Never cut Demo 2; the lecture's claim depends
  on it.
- **Risks:** `pytest-cov` missing on the presentation machine (the pipx `pytest`
  used in planning lacks it); the reference's 100% claim was confirmed in a
  venv on 2026-09-22 (99 tests, 155 statements, 62 branches) and must be
  confirmed again on the presentation machine. A stale bytecode cache can hide
  the direction flip (same file size). The overline test's name differs from
  rehearsal if `t4` is regenerated. Students take "100%" as "done": the
  sentence after each step corrects this.
- **Variants:** before deleting, have students predict which single test could
  be deleted with coverage unchanged, and why.
