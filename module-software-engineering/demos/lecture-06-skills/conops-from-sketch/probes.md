# Reading probes for a ConOps sketch

Each probe is a question to ask of the sketch. A probe that turns up something
the sketch does not settle is a gap: report it with the rule it falls under
(the repository's own rule identifiers where it has them; the parenthesis names
the kind of rule). None of these has a default answer — the point is to ask.

## Rules and boundaries

- **Counts and thresholds.** Wherever the sketch says "N of something" (N in a
  row, N attempts, N items), is it exactly N, at least N, or at most N? Walk the
  case N+1. *(ambiguous)*
- **Simultaneous conditions.** List every way an activity can end or change
  state. Can one action satisfy two of them at once (a success on the last
  available step; a limit reached at the moment of a win)? Which takes
  precedence? *(incomplete — execution walkthrough)*
- **Terminal states.** Is every end state defined exactly, and is it final?
  When the author doubts or dismisses a state ("unlikely to happen",
  "probably never happens"), report that as **its own gap** — what exactly the
  state is, whether it is final, whether it is expected to be rare — not only
  as a missing scenario. A state the sketch doubts is still a state the
  system must handle. *(incomplete)*
- **Who acts first, and on repeat — as a grid.** Where there are turns, roles,
  or sides, write a small grid before answering: one row per mode, one
  column per entry point — *first time*, *repeat right after*, *after going
  back to a menu and choosing again*. For each cell ask: who starts, who is
  who? A sketch usually answers one cell and flags another; every empty cell
  is a gap. *(incomplete)*
- **State carried across repeats.** List anything that carries from one
  round to the next (whose turn it is to start, an alternation, a score, a
  setting). For each: what resets it — repeating, returning to a menu,
  switching mode, restarting the program? *(incomplete — execution
  walkthrough)*

## Inputs

- **Form of input.** When the sketch says the user "types X" or "picks Y", what
  exactly is typed — order, separators, an example? *(ambiguous — form needs an
  exact example)*
- **Bad input.** For each input: what happens when it is malformed, out of
  range, or refers to something unavailable? Does the user lose anything
  (a turn, progress)? *(incomplete; observable)*
- **Leaving early.** Can the user stop in the middle of each activity? What
  happens to it? *(incomplete)*

## Consistency

- **Say it twice.** Find every moment or list the sketch describes in more
  than one section — especially the modes section versus the scenarios (the
  options offered when an activity ends, the menu choices, the list of
  users). Copy each section's wording next to the other's, word for word, and
  compare the *sets* of options, not the gist. Any difference — an option in
  one list and not the other — is an inconsistency, not a nuance. Scenarios
  are where this hides: they are written later and paraphrase. *(inconsistent
  within a document)*
- **Promised vs. walked through.** For every mode, user class, and policy the
  sketch names, is there a scenario that exercises it? Scenarios that only
  cover the happy path leave the alternatives (the other mode, the other
  outcome, the error) unexercised. *(scenario coverage)*
- **Facts in the wrong place.** Read the limitations, analysis, and future
  sections sentence by sentence: does any of them state something the user
  observes *now* (what is kept, what is not, where it runs)? That fact belongs
  in the policies or environment section, and is missing there. *(misfiled)*

## Words and form

- **Terms.** Which words does the sketch use repeatedly, or use two names for
  (synonyms like "user / customer", "order / request")? Is each defined? *(terms)*
- **Voice.** First person ("I", "me", "my team"), future tense, or wishes
  ("I want…") are findings; the document must be third person, present tense.
  *(voice)*
- **Implementation leaks.** Any language, library, data structure, or internal
  file named? *(implementation-independent)*
- **Placeholders and flags.** Every "TBD", "?", "not decided", "for now",
  "probably", "maybe", or skipped section is a gap — list each one, including
  the questions the author asked themselves. *(skeleton; incomplete)*
- **Skeleton fit.** Are optional sections present or absent for the right
  reason (a baseline system exists or not)? *(skeleton)*
