# Changelog — 001-five-in-a-row specification

Records changes to `spec.md` and the reason for each, as required by the constitution
(Principle III; Records of Change).

## 2026-10-08

- Initial draft from `ASE-seed-conops.md` via `/speckit-specify`.
- Clarifications decided by the developer:
  - FR-008: five **or more** consecutive marks win (six in a row counts). Reason: the
    simplest rule and the most intuitive for new players. Added User Story 1 scenario 6.
  - FR-013: against the computer, the human is X in the first game from the start menu;
    marks swap on each "play again". Reason: fairer across a series of games. Answers the
    question left open in ConOps §2.2. Added User Story 2 scenarios 5–7 and two assumptions.
- `/speckit-clarify` session; answers decided by the developer:
  - Added FR-018: a leave-game command at every move prompt abandons the game (no result)
    and returns to the start menu. Replaces the assumption that leaving mid-game was out of
    scope. Added User Story 3 scenario 5; updated FR-005 and the unreadable-input edge case.
  - Added FR-019: after each computer move the program names the square it took, as well as
    redrawing the board. Updated User Story 2 scenario 2.
  - FR-004 now fixes the move format: row then column on one line, separated by a space or
    a comma (`4 7` or `4,7`). Removed the assumption that left the format to planning;
    updated the unreadable-input edge case.
- Added FR-020, User Story 3 scenario 6, and an edge case: if input ends or the player
  interrupts the program at any prompt, it ends promptly with a short goodbye and no error
  trace. Decided by the developer: accepted proposal P1 raised during `/speckit-plan`
  (research.md), which found the spec silent on this.
