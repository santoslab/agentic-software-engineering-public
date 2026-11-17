---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 24px;
  }
  h1, h2 {
    color: #310066;
  }
  li { margin: 0.2em 0; }
---

## Beads exercise discussion (1/3): what worked, in all five submissions

<style scoped>
section { font-size: 22px; }
</style>

- **The work graphs separated independent work from integration.** The rendering and parsing work did not block each other, so either could start first; the game loop, which needs both, waited on both.
- **Session 1 stopped where told.** The board was drawn and tested, the partial work committed, and the bead left `in_progress` with a handoff: commands and results, what remains, files and commits, the next step.
- **Every fresh session found the unfinished bead without being given its ID**, from Beads, Git and the files alone.
  - Every recovery report marked which results it had checked itself and which it had only read in the bead, such as session 1's test counts: "I did not run pytest, so the 4-passed and 48-passed counts are recorded evidence only, not re-verified."
- **Closing stayed within scope.**
  - Tests came before the code they cover, with the failures recorded.
  - Only the rendering bead was closed; no submission claimed the game or the milestone complete.
  - No submission added the leave-game hint (the `m` command), which the rendering task defers to a later story; those that raised the conflict before coding recorded the ruling in a bead.

---

## Beads exercise discussion (2/3): a review that shows two records cannot vouch for all of them

<style scoped>
section { font-size: 23px; }
</style>

- **In four of five submissions, the turn that reviewed the newly created records displayed only one or two of them**, some cut short (`bd show … | head -30`); the rest appeared as titles in a list.
  - Two of those turns then vouched for all of them, for example: "Every record has original task references, governing paths, acceptance criteria and evidence needs."
- **The same gap reappeared in recovery.** One session 2 recovery report said "I found no open developer-decision request", while another bead's acceptance criteria held "OPEN FOR THE DEVELOPER: …". That bead was never displayed.
- **Why it matters:** Beads holds the plan in many small records. A summary of the graph is only as good as the records actually read; a list of titles shows that a record exists, not what it says.
- For discussion: how could a review be set up so it is clear that every record was read?

---

## Beads exercise discussion (3/3): holes in the evidence setup

<style scoped>
section { font-size: 22px; }
</style>

- **The read-only check covered only what Git tracks.** The `git status` and `git diff` captures taken before and after the recovery turn cannot see Beads writes or files Git ignores.
  - In one submission, the recovery prompt allowed running the test suite. The test run rewrote the ignored `reports/conformance.md`; the Git captures matched, and the recovery report opened "I changed no files and no Beads data".
- **The conformance report shows where things stand, not what a piece of work changed.** Closing records credited the passing rows they listed to the new message-helper tests. In two submissions, six of nine and seven of ten of those rows were already passing from the starter's engine tests; only three were new: the board drawing (FR-006), the prompt naming the mark (FR-007), and the unreadable-entry message (EDGE-unreadable-input).
- **A tag is a claim, so it should be checked.** The conformance report counts a test toward a requirement whenever it carries the tag, whatever the test asserts. In four submissions, the test for the "not understood" message checks the line's shape, not its meaning; unrelated text such as `Hello.` would pass.
- For discussion: how would you close these holes?
