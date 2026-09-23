# Instructor key — decisions the Reversi sketch leaves open, with the standard rulings

Not student-facing. The brief's §4 (`../../project-1-reversi-brief.md`) is the
student-facing version of this list; the sketch is
`../../student-materials/reversi-starter/CONOPS-sketch.md`;
`demo-script-lecture-05.md` uses rows 1, 2, 5, 6, and 7 live. Use this when
grading Part 1: every row must be *stated* somewhere in the student's
`CONOPS.md` or `SPECS.md`; a standard rule left implicit is a completeness
failure. Rows marked *student's choice* accept any recorded ruling. The *Found
by* column names the rule (AUD, AUDCON) that surfaces the gap; a Part 1 gap list
that cites those rules is doing the audit the process requires (DEV-8).

## Seeded in the sketch

| # | Gap | Where in the sketch | Standard ruling | Found by |
|---|---|---|---|---|
| 1 | End of game is stated as "board is full" — **in tension with** the pass rule (with forced passes the board may never fill) | §4.2 last bullet vs third bullet; §5.1 | The game ends when neither player has a legal move; a full board is one case of that | AUD-2 |
| 2 | The opening position | §1.2 "a few discs already in the middle" | d4 and e5 light, d5 and e4 dark | AUD-4; AUD-8 |
| 3 | Who moves first | silent | Dark | AUD-4; AUD-8 |
| 4 | Equal counts | §4.2 "whoever has more wins" | A tie | AUD-4; AUD-8 |
| 5 | Consequences of a pass: whose turn, announced, forced or chosen, two in a row | §4.2 "forfeit your turn"; §5.1 "the computer goes again" | Forced, never chosen; announced; the opponent moves; two consecutive passes end the game | AUD-4; AUDCON-3 |
| 6 | Must *all* flanked runs flip, in all eight directions | §4.2 "everything trapped flips" (one line implied) | Yes — every direction, every run | AUD-1 |
| 7 | Legal-move hints | §4.2 flagged as undecided | *Student's choice*; must say when shown and how rendered | AUD-4 (flagged) |
| 8 | Score during play | §4.1 "keep score" vs §5.1 counts only at the end | *Student's choice* | AUD-2 |
| 9 | Colors → glyphs in a terminal | §1.2 black/white; §4.5 terminal | *Student's choice* (`X`/`O`, `B`/`W`, `●`/`○`); named `dark`/`light` in fixtures | AUD-4 |
| 10 | Notation edge cases: case, whitespace, out of range (`d9`, `i3`), length | §1.2 "like d3" | *Student's choice*, stated as a grammar | AUD-1; AUD-10 |
| 11 | An entry that is not a square; a square that flips nothing; an occupied square | §5.1 shows one case | Brief error, re-prompt; the turn does not pass; the board is unchanged | AUDCON-2; AUD-4 |
| 12 | Solo: which color the human has; rematch alternation; reset at the menu | silent | *Student's choice*; the demo's ruling (human alternates sides on rematch; reset at menu) is a fine default | AUD-4; AUDCON-3 |
| 13 | Two-player rematch | silent | No alternation; the program cannot tell two people apart | AUD-4 |
| 14 | Post-game options | §4.3 "play again or start menu"; §5.1 "play again" | *Student's choice*; must be consistent across sections | AUD-2 |
| 15 | Taking a move back | §7 "no taking a move back" — a policy stated only under Limitations | Not supported; stated in §4.2 | AUDCON-8 |
| 16 | Persistence, sessions, network | silent | One sitting; nothing saved; one keyboard | AUD-4 |
| 17 | Scenario coverage | §5.1 only | Add two-player, a pass, an early end, a rejected entry | AUDCON-3 |
| 18 | Glossary; register | §9 TBD; first person | Define disc, flip, flank, pass, legal move, dark/light; third person | AUDCON-7; AUDCON-4; AUDCON-5 |

## Surfacing when SPECS.md is derived

| # | Gap | Kind | Ruling | Found by |
|---|---|---|---|---|
| 19 | Byte-exact board with labels a–h and 1–8; the hint glyph if any | display | *Student's choice*, byte-exact with two examples | AUD-9 |
| 20 | How the engine names a square: `"d3"` vs `(row, col)`; where the notation→index translation lives | interface | *Student's choice*; translation inside the engine (the demo's coordinate lesson) | AUD-12 |
| 21 | What a move operation returns and changes; the flipped set as postcondition | interface | Returns success plus the flipped squares, or equivalent | AUD-12 |
| 22 | Legality query; "no legal move" exposure; game-over and count exposure | interface | `legal_moves(color)`, `must_pass(color)` or equivalent; `is_over()`; `score()` | AUD-12 |
| 23 | A move after the game is over | interface | Rejected, no state change | AUD-12 |
| 24 | Disc-count invariant (dark + light + empty = 64; discs = 4 + accepted moves) | rules / testing | State it; test it | AUD-8; AUD-14 |
| 25 | "Random among legal moves" — testability | testing | Result ∈ `legal_moves(color)` on non-trivial boards; no seeding | AUD-14 |
| 26 | Module split; verification obligations | structure / testing | The demo's split; `SPECS.md` §9 lists obligations traced to clauses (AUD-14); the policy is VER-4 through VER-8 and is not the student's to weaken | DEV-9; VER-5, VER-6 |

## Nudges, if a gap is missed during the L05 walkthrough

- 1: "Both players are stuck with twelve empty squares left. What does the program do?"
- 2: "Draw the board before the first move. Which squares hold which color?"
- 5: "You have no move. What is the very next thing that happens — and the thing after that?"
- 6: "A square would trap discs both across and diagonally. What flips?"
