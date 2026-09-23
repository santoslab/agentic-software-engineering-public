# Game demo, part 1 (Lecture 03) — from a sketch to a family of specifications

Part 1 of a demonstration that runs across Lectures 03 and 04. The repository
starts with a sketch of a concept of operations for a game and nothing else but
the process documents. The class watches the sketch audited and rewritten as a
concept of operations, a behavioral contract of several kinds derived from it,
and the game built from the contract. Tests, the coverage gate, and fixtures are
part 2.

**A caution that governs the whole script.** Do not depend on the agent making
one specific move. The *Expected* notes describe the usual shape; every segment
has an *If it goes differently* note; rehearse at least once and capture
screenshots at every `[fallback capture]` marker. Rehearsal also produces the
tags: the rewritten concept of operations (`t1`), the contract (`t2`), and the
implementation (`t3`) each take the agent more than two minutes, so in class
they are shown from the tag, and the live time goes to the gap lists and the
rulings.

## What the starter contains, and what is seeded in it

`starter/` (tag `t0`) has `CONOPS-sketch.md`, the loader `CLAUDE.md`, `process/`
(the L03 set: AUD with its per-kind appendix, AUDCON with the skeleton rules,
DEV-1 through DEV-10, VER-1 through VER-4, RPT-1 through RPT-5, and the
invariant), and `BACKLOG.md`.

The sketch is written in the first person, as a client's general idea. It keeps
sections 2 and 3 of the full skeleton short (ordinary 3×3 tic-tac-toe is the
baseline) and skips section 6. It leaves the following open. Do not reveal
them before Segment 2. The *Found by* column names the rule that surfaces each.

### Round 1 — the sketch to a concept of operations

| # | Gap | Where in the sketch | Scripted ruling | Found by |
|---|---|---|---|---|
| 1 | Does more than five in a row win? | §4.2 "five in a row" | five **or more** wins | AUD-1 |
| 2 | A win on the last empty square — win or draw? | §4.2 is silent | a win takes precedence | AUD-4 |
| 3 | Solo play: which side is the human, and does it change on a rematch? | §4.2 flagged as undecided | X moves first; the human is X in game 1; sides alternate on rematch | AUD-4; AUDCON-3 |
| 4 | Does the alternation survive a return to the menu? | silent | no — the menu resets it | AUD-4 |
| 5 | Two-player rematch: who starts? | silent | X, always; the program cannot tell two people apart | AUD-4 |
| 6 | An entry that is not a square | silent | a brief error, ask again; the turn does not pass | AUDCON-2; AUD-4 |
| 7 | Post-game options — **an internal inconsistency** | §4.3 "play again or start menu"; §5.1 "play again or quit" | three options: play again, main menu, quit | AUD-2 |
| 8 | The form of a move entry | §1.2 "its row and column" | a two-digit entry, row then column, no separator | AUD-1 |
| 9 | Scenario coverage | only §5.1, which assumes a win | add two-player, tie, invalid-entry scenarios | AUDCON-3 |
| 10 | Is a draw realistic; is it final? | §5.1 aside | a tie is a full board with no line; final; rare | AUD-4 |
| 11 | Persistence — a fact in the wrong section | §7 "nothing is saved" | stated in §4.5: one sitting, nothing saved, one keyboard | AUDCON-8 |
| 12 | Quitting mid-game | silent | **defer** to `BACKLOG.md` | AUD-4 → DEV-6 |
| 13 | Glossary | §9 "TBD" | define the terms | AUDCON-7; AUDCON-4 |
| 14 | Voice | first person | third person, implementation-free | AUDCON-5 |

Rule on six or seven live (1, 2, 3, 7, 8, 11, and the deferral of 12); mark the
rest *ruled* in one sentence each or *deferred*.

### Round 2 — the concept of operations to the contract

| # | Gap | Kind | Scripted ruling | Found by |
|---|---|---|---|---|
| 15 | What the board looks like | display | byte-exact; labels always; `.` for empty; 4 leading spaces on the header; 19 dashes | AUD-4; AUD-9 |
| 16 | Entry grammar: `0`, whitespace, length | input grammar | strip; exactly two characters; digits `1`–`9`; `0` rejected | AUD-10 |
| 17 | A move after the game is over | interface contract | rejected with no state change — **the reference specification is silent here; say so** | AUD-12 |
| 18 | "Picks randomly" — how is that verified? | obligations | the result is in the available moves, on a partly filled board; no seeding | AUD-14 |
| 19 | The engine's public interface | interface contract | `(row, col)` in 1–9; `make_move → bool`; row-major `available_moves` | AUD-12 |
| 20 | The coverage policy | not a contract decision | already in `process/verification.md` (VER-4); §9 lists what the tests must claim | — |
| 21 | Menus and the per-game loop, exactly | interaction flow | numbered steps; the board rendered every turn | AUD-11 |
| 22 | An example session | example | one full transcript | AUD-13 |

Rule on 15, 16, 17, and 18 live; 20 is the one to say aloud — it is not a
decision the contract makes.

## Before class — setup checklist

1. Create the demo repository from `starter/` and tag it:

   ```sh
   rm -rf ~/game-demo
   cp -R <path-to-this-demo>/starter ~/game-demo
   cd ~/game-demo && git init && git add -A
   git commit -m "demo start: conops sketch and process" && git tag t0-conops-sketch
   ```

2. Rehearse the whole of part 1 once, and tag the states: `t1-conops` after
   Segment 2, `t2-spec-family` after Segment 3, `t3-engine` after Segment 4.
   Keep this rehearsal repository; in class, a fresh copy of `starter/` is used
   for the live segments, and the rehearsal repository is what you switch to
   when a segment would exceed two minutes.
3. A venv with `pytest` and `pytest-cov` installed, and `python main.py`
   confirmed to run at `t3`.
4. Claude Code started in the live repository with the always-on process files
   loaded; two terminals, large font; the prompts in a text file; captures at
   every `[fallback capture]` marker.

## Segment 1 — Tour (about 6 minutes)

**Do (shell):** `ls`; `cat CONOPS-sketch.md`; `cat CLAUDE.md`; `ls process/`.

**Say:** a sketch, not a draft: first person, sections 2 and 3 kept short
because there is a baseline (ordinary tic-tac-toe), section 6 skipped, two
sections marked TBD. The loader names the concept of operations as the first
governing document — "until it exists, the sketch stands in" — and a contract
that does not exist yet. The process documents are the ones from Lecture 02
with three additions, which the tour names but does not read: audit before
planning (DEV-8), plan before build (DEV-9), and the audit's checks by kind of
specification (AUD-8 to AUD-14).

`[fallback capture]` — the sketch and `ls process/`.

## Segment 2 — The sketch to a concept of operations (about 16 minutes)

**Do:** plan mode. Type the prompt, then pause; the room writes its own gap
list for two minutes.

> Read `CONOPS-sketch.md` and the process documents. I want a `CONOPS.md` 1.0
> that realizes this sketch as a full-skeleton concept of operations. Before
> proposing anything, run the audits in `process/conops-audit.md` and
> `process/spec-audit.md` on the sketch (DEV-8) and report the gap list per
> RPT-1 — numbered, each with your recommended resolution. Then stop and wait
> for my rulings.

**Expected:** an RPT-1 list containing most of round 1, usually more.

`[fallback capture]` — the list.

**Do:** rule per the round-1 table; defer 12 to `BACKLOG.md` on purpose, and say
why (DEV-6). Then:

> Propose the amendments per RPT-3 and wait for my approval.

Approve. Then:

> Write `CONOPS.md` 1.0, run the audits on it again, report per RPT-1, and
> commit as `conops: 0.1 sketch -> 1.0`.

If the rewrite runs past two minutes, switch to the rehearsal repository at
`t1-conops`.

**Do (shell):** `git diff --stat`; `head -40 CONOPS.md`; `cat BACKLOG.md`.

**Say:** the content survived the rewrite; the voice did not. Two findings were
not gaps but faults — the post-game inconsistency (AUD-2) and the misfiled
fact (AUDCON-8) — and the audit found both by reading, before anything realized
the document.

**If it goes differently:** nudges — 1: "Walk through a move that makes six in
a row." 2: "The 81st square completes five in a row. Win or draw?" 7: "Read
§4.3 and §5.1 side by side." 11: "Where does the sketch say nothing is saved? Is
that the right section?"

## Segment 3 — The concept of operations to the contract (about 16 minutes)

**Do:** plan mode, in the live repository at `t1` (or the rehearsal
repository). Prompt:

> Read `CONOPS.md` and the process documents. Derive `SPECS.md` 1.0.0 from it:
> one section per kind — board and coordinates; rules of play; display format,
> byte-exact; input grammar; interaction flow; interface contract with
> preconditions and postconditions; an example session; verification
> obligations. Before writing, run the audit (DEV-8) and list every decision
> the concept of operations leaves open, grouped by the kind of specification
> that must settle it, per RPT-1 with a recommendation each. Wait for my
> rulings.

**Expected:** a list grouped by the kinds the prompt names, containing round 2.

`[fallback capture]` — the grouped list.

**Say:** the agent did not choose the kinds. The loader names the eight
sections of `SPECS.md`, the prompt repeats them, and AUD-8 to AUD-14 check one
kind each, so a missing kind would be a finding. In general, choosing the kinds
of specification is the developer's decision — or the organization's: a
company often has a fixed collection, with a format for each. Without that
guidance, someone has to decide the kinds and their formats, and by default
that someone is the agent. We pre-pick them here, and the Reversi brief
pre-picks the same eight, to keep the demo simple and more deterministic.

**Do:** rule on 15–18. Say aloud, for 20, that the coverage policy is not a
decision the contract makes: it is in `process/verification.md` already, and
§9 will list what the tests must *claim*. Approve amendments if any concern
the concept of operations (none are expected). Then:

> Write `SPECS.md` 1.0.0 and commit as `specs: 1.0.0`.

Switch to `t2-spec-family` rather than wait.

**Do (shell):** `grep '^## ' SPECS.md`; `sed -n '/^## 4/,/^## 5/p' SPECS.md`.

**Say:** eight sections, eight kinds. Point at §4.1 and read "five or more":
the concept of operations said it, the rule pins it, and §9 will require a test
for it — one intent, three statements, one identifier chain. Point at §9 and
say why it is obligations, not policy. And say that finding 17 went beyond
the reference implementation the course keeps: its specification was silent on
a move after the game is over, so the contract written today is stricter than
the code that will be built — which Lecture 04 will catch.

**If it goes differently:** if the list is not grouped, ask: "Group these by
the kind of specification that must settle each." If it is long, rule on the
four and defer the rest.

## Segment 4 — The implementation, from the tag (about 8 minutes)

DEV-8 is satisfied, so DEV-9 applies. Show the prompt, not the run:

> Read `SPECS.md` and the process documents. Propose a plan for the engine
> module, the computer opponent, and the command-line interface, citing for
> each step the clauses it realizes, and wait for my approval.

**Do:** switch to `t3-engine`. `cat plans/*.md | head -60`; `ls`;
`python main.py` for one move each way; `git log --oneline`.

**Say:** the plan cites §3, §4, and §5.1 step by step, so the history reads
specification → plan → realization. `CLAUDE.md` is two rules; the laws are in
`process/`. Nothing has been verified yet except by running it once — that is
Lecture 04.

## End of part 1

The repository holds `CONOPS.md` 1.0, `SPECS.md` 1.0.0, an approved plan, and
the three modules. Part 2 starts from `t3-engine`.

## Recreating this part yourself (students)

Copy `starter/` outside the course repository, follow step 1 of the checklist,
and run Segment 2 with your own session. Compare your gap list with the round-1
table — you will find some of it, miss some, and find things it does not list.
Exercise 3 (optional) asks for Segment 3 as well: from your own `t1`, derive the
contract and submit the grouped gap list with your rulings.
