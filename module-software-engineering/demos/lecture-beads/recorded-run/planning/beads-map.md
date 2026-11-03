# Original task ID → Beads ID map (two-player milestone)

Beads is authoritative for live status; this file records the translation only.

| Original task | Beads ID | Issue |
|---------------|----------|-------|
| (milestone) | ttt-cik | Epic: two-player five-in-a-row (T018–T024) |
| T018, T021 | ttt-cik.1 | Board rendering and message text |
| T019, T022 | ttt-cik.2 | Move and menu parsing plus menu-caller refactor (one bead; II(c) parser commit, then separate II(b) refactor commit) |
| T020, T023 | ttt-cik.3 | Two-player game loop with tests |
| T024 | ttt-cik.4 | Verify two-player milestone conformance |

## Blocking dependencies (`bd dep add`)
- ttt-cik.3 is blocked by ttt-cik.1 and ttt-cik.2.
- ttt-cik.4 is blocked by ttt-cik.3.
- ttt-cik.1 and ttt-cik.2 have no blockers and are independent of each other.

Epic membership (parent-child) groups the work; only the dependencies above express order.
