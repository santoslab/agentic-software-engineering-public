# Lecture 03 — Specifying a Game: One System, Several Specifications

> **Unit:** module-software-engineering · **Module week 2, meeting 1 of 2** · 75 minutes
>
> **Thesis:** A system needs several specifications of different kinds; 
> starting from a ConOps, the agent helps you discover the specifications by 
> audit and interrogation.

## Learning objectives

After this lecture, students can:

1. Name the kinds of specification an interactive program needs — concept of
   operations, rules of play, display format, input grammar, interaction flow,
   interface contract, example session, verification obligations — say what
   each fixes and what it leaves open, and say which are instances of kinds in
   the course catalog of specification kinds.
2. Run the specification audits (AUD, AUDCON) on a ConOps sketch and produce an
   RPT-1 gap list with a recommended resolution for every item.
3. Rule on a gap and record the ruling as an RPT-3 amendment with a version bump
   and a changelog entry.
4. Trace one intent across the specification family by identifier — a ConOps policy, the rule
   that pins it, the obligation that verifies it.
5. State which process rule applies at each moment of the demo (DEV-8, DEV-3,
   DEV-9; RPT-1, RPT-3).

## Before class

Assigned at Lecture 02 (to be listed under L02's "Assigned after class" when L02
is written):

- [required] The L03 handout: `CONOPS-sketch.md` and the `process/` set as shipped
  in the demo starter (`../demos/lecture-03-game-demo/starter/`; ten minutes). Class time is not spent
  reading the process files; the tour names them.
- [required] Meyer (1992) on preconditions and postconditions, if not read for L02.
- [recommended] The ConOps template resource (full skeleton; sections 2, 3, and 6
  optional).
- [recommended] The course catalog of specification kinds,
  `../../specification-kinds.md`: the summary table and the entries for the
  eight kinds this lecture derives (fifteen minutes).

## Topic outline

| Time | Topic | Content |
|------|-------|---------|
| 0–6 | Frame | L02 in one slide: a ConOps is a specification of purpose; lower-level specifications are derived from it; operations have pre/postconditions; the spec is an invariant while R changes. Today R is code, S starts as a *sketch*, and the derived specifications come in several kinds. `ls` the `t0` repo: the sketch, the two-rule `CLAUDE.md`, `process/`, `BACKLOG.md` — no `CONOPS.md`, no `SPECS.md`, no code. Why a game: grid, two players, rules, a terminal condition — the shape of Project 1. |
| 6–14 | ConOps for a game | The full skeleton; sections 2, 3, 6 apply only when a baseline exists (AUDCON-7) — the sketch keeps 2 and 3 short because ordinary 3×3 is the baseline, and skips 6. Policies a player can observe (AUDCON-2); "never names a language" (AUDCON-1); the ConOps answers a validation question, every other kind answers verification questions. The game's O1 is `make_move` with its pre/postcondition; the rules of play are the invariant, as the note-format spec was. |
| 14–30 | Demo 1 — sketch → ConOps (`t0 → t1`) | Type the round-1 prompt; pause; the room writes its own gap list for two minutes. The agent's RPT-1 list appears; compare. Rule live on six or seven of the fourteen seeded gaps (overlines; win on the last square; solo side alternation; the §4.3-vs-§5.1 inconsistency; "nothing is saved" in the wrong section; the entry form); defer "quit mid-game" to `BACKLOG.md` (DEV-6) on purpose. Amendments per RPT-3, approved. The rewrite shown from the `t1` tag if it runs past two minutes. `CONOPS.md` 1.0 with a changelog; AUDCON re-run on the amended document (DEV-8, second clause). |
| 30–46 | Demo 2 — ConOps → the specification family (`t1 → t2`) | The round-2 prompt asks for the open decisions grouped by the kind of specification that must settle them; the kinds are pre-picked — the loader, the prompt, and AUD-8 to AUD-14 name them — so the list confirms the grouping rather than inventing it. Say aloud: in general, choosing the kinds of specification is the developer's or the organization's decision (many companies fix a standard collection with a format for each); without that guidance the agent would decide the kinds and formats; the demo and the Reversi brief pre-pick them to stay simple and deterministic. Rule on the four scripted round-2 gaps: the board is byte-exact with `.` (AUD-9); `0` is rejected, whitespace stripped, length exactly two (AUD-10); a move after the game is over is rejected with no state change (AUD-12) — and note the reference specification was silent here, so `t2` goes beyond it; "random" is tested as "result ∈ available moves," which ends up in the *obligations*, while the coverage policy is already in `process/verification.md`. Writing shown from `t2`. `SPECS.md` 1.0.0. |
| 46–56 | Quality checks across the family of specifications | AUD-1: "byte-exact" versus "looks like this." AUD-3: the overline chain — ConOps "five or more" → §4.1 "overlines count" → obligation "at least one overline case" → a test citing §4.1 → a fixture. AUD-4: what does `render` do on a full board? AUD-5: the § numbers the tests will cite. AUD-8 through AUD-14 as the per-kind checklist the round-2 audit used. |
| 56–64 | Planning development according to the specifications (`t3`) | DEV-8 is satisfied, so DEV-9: plan mode; the plan cites §3, §4, §5.1 step by step; approved; committed under `plans/`. Jump to the tag; the three-module split; `CLAUDE.md` is two rules — the laws live in `process/`, not in prompts. |
| 64–72 | Close | What L04 does with `t3`. Exercise 3 (optional): reproduce `t1 → t2` in your own session. At L05 you receive a Reversi sketch and make these moves yourselves. |

Blocks sum to 72 minutes; 3 minutes slack.

## Demos

### Demo 1 — Sketch → ConOps

- **Artifacts:** `../demos/lecture-03-game-demo/demo-script-lecture-03.md`
  (segments, prompts, the round-1 and round-2 tables of seeded gaps with rulings
  and nudges); `starter/` (the `t0` state); a rehearsal repository with tags
  `t0` … `t5`.
- **Setup (before class):** fresh clone of the starter with an initial commit
  tagged `t0`; the rehearsal repository with `t1` … `t5` prepared and verified;
  Claude Code open at the root; font large; prompts in a text file; rehearsal
  captures at every `[fallback capture]` marker.
- **Script:** (1) type the round-1 prompt — *"Read `CONOPS-sketch.md` and the
  process documents. I want a `CONOPS.md` 1.0 that realizes this sketch as a
  full-skeleton concept of operations. Before proposing anything, run the audits
  in `process/conops-audit.md` and `process/spec-audit.md` on the sketch (DEV-8)
  and report the gap list per RPT-1 — numbered, each with your recommended
  resolution. Then stop and wait for my rulings."*; (2) two minutes for the room's
  own list; (3) walk the agent's list against the key; rule on six or seven; defer
  one; (4) *"Propose the amendments per RPT-3 and wait for approval"*; approve;
  (5) *"Write `CONOPS.md` 1.0, re-run AUDCON on it, and commit as
  `conops: 0.1 sketch -> 1.0`"* — jump to `t1` if slow.
- **Expected outcome:** the class sees a first-person sketch become a
  third-person, implementation-free document with a changelog; every change
  traceable to a numbered gap and a ruling.
- **Fallback:** the rehearsal captures; the `t1` tag.

### Demo 2 — ConOps → the family of specifications

- **Artifacts:** `t1`; `../demos/lecture-03-game-demo/reference/SPECS.md` as the
  shape of the target (not shown to students until `t2`).
- **Script:** (1) *"Read `CONOPS.md`. Derive `SPECS.md` 1.0.0 from it: one section
  per kind — board and coordinates; rules of play; display format, byte-exact;
  input grammar; interaction flow; interface contract with pre/postconditions;
  example session; verification obligations. Before writing, run the audit
  (DEV-8) and list every decision the ConOps leaves open, grouped by the kind of
  specification that must settle it, per RPT-1 with a recommendation each; wait
  for my rulings."*; (2) the grouped list is the table; rule on the four scripted
  gaps; (3) amendments where the ConOps itself must change (none expected; if
  one appears, it goes through RPT-3 — say so); (4) jump to `t2`; scroll the
  eight sections; point at §9 and say why it is *obligations* and not policy.
- **Expected outcome:** the specification-family table filled in by elicitation, with the
  students having seen each kind arrive as a decision rather than a heading.
- **Fallback:** the `t2` tag and captures.

### Demo 3 — Implementation from the tag (recorded)

- **Artifacts:** `t2`, the approved plan under `plans/`, `t3`.
- **Script:** show the DEV-9 prompt and the plan's clause citations; jump to `t3`;
  `python main.py` for one move each way; `ls` the modules.
- **Fallback:** none needed; this segment is never live.

## Discussion prompts

1. The "how is random tested?" gap ended up in the verification obligations, not
   in the rules of play. Why is *how it is tested* not a property of the game?
2. The sketch said "five in a row"; the ConOps says "five or more." Which side
   moved, who decided, and where is the decision recorded?
3. Of the fourteen round-1 gaps, which would a player have noticed first, and
   which only an implementer? Use AUDCON-2 to sort them.

## Assigned after class

- Readings (for L04): [required] `process/verification.md` at its L04 level
  (VER-5 through VER-8) — read the rules before the lecture that teaches them;
  [required] the shared-fixtures README (`weeks-04-07/student-materials/fixtures/README.md`);
  [recommended] coverage.py on branch coverage.
- Exercise: Ex. 3 (optional) — from the `t1` tag, reproduce `t1 → t2` in your own
  session; submit the RPT-1 gap list and your rulings. Exercise 2 is due before
  Lecture 04.

## Instructor notes

- **Cut if running long:** the quality block (46–56) compresses to the overline
  chain on one slide; Demo 3 is already recorded. Never cut the round-1 rulings;
  they carry the lecture's content.
- **Risks:** the agent finds gaps the key does not list (rule or defer them; a
  live DEV-6 deferral is worth showing) or misses a seeded one (use the nudge in
  the key). The ConOps rewrite and the SPECS writing exceed two minutes — never
  wait; jump to the tag. The round-2 list is long: rule on the four scripted gaps
  and defer the rest to `BACKLOG.md`. Students conflate ConOps and SPECS all
  week; AUDCON-1's test — "would a player encounter this noun?" — is the fastest
  discriminator.
- **Variants:** strong room — students rule on two gaps instead of the
  instructor, and the class audits the ruling against AUDCON-2. Laptops — students
  run round 1 in parallel on the same sketch and compare lists at minute 30.
