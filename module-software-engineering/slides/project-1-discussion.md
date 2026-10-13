---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
  }
  section.lead {
    background: #310066;
    color: #ffffff;
  }
  section.lead h1, section.lead h2 {
    color: #ffffff;
  }
  section.standout {
    background: #beaefc;
    color: #310066;
    text-align: center;
    font-size: 36px;
  }
  h1, h2 {
    color: #310066;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

## Project 1 discussion (1/2)

<style scoped>
section { font-size: 20px; }
li { margin: 0.15em 0; }
</style>

- **Accepting Claude's recommendation is still your ruling** — 4 of 5 SPECS example sessions never show a player who cannot move, though the brief requires one. Each was Claude's recommendation, accepted. One rested on a false premise, Claude's "isn't reproducible in a short game": eight moves reach one.
- **An ambiguous rule** — the starter's test gate is meant for code, but it "MUST pass … before any commit", and it fails while no code exists. Five students gave five answers: amend the rule, rule an exception, wave each commit through, leave it open, or let Claude decide it "does not apply". Which is a legitimate process change?
- **Where does the test plan go when every commit must pass the gate?** Most students folded it into the build plan to keep each build commit green. One kept it separate and committed the engine with the gate failing, by ruling. Plan-before-build and green-before-every-commit pull against each other. In practice, the default branch stays green and work in progress goes on a branch, which the brief's steps don't allow for.
- **A person playing finds what tests can't** — one student had ruled in the ConOps that entering `h` lists the allowed moves, but their playthrough found that the move prompt never mentioned it. A spec amendment fixed that before any code changed. No coverage figure could have shown it. Only one submission records a person playing each mode.
- **"An engine is not the oracle for its own fixtures" (the brief)** — every expectation in all five fixture files was correct. They were checked through the game under test, Claude's scratch models, or a separate reference; no submission records a person checking them by hand against the spec. When Claude writes both the engine and the checker, how independent is the check? A person working from the spec is.

---

## Project 1 discussion (2/2)

<style scoped>
section { font-size: 19px; }
li { margin: 0.15em 0; }
</style>

- **Who did what, in a report drafted with Claude** — two reports made first-person claims for checks the transcripts show Claude running. Another left out Claude's independent check. A report says who ran each check.
- **Coverage is not conformance, seen in your own sessions** — deleting the only test of one obligation left 100% branch coverage. A computer opponent that chose randomly only when it had exactly four legal moves, as at the opening, and otherwise always took the first legal move, still passed the whole suite. With the up-right diagonal deleted from the engine's flip rule, the fixture tests still passed: no fixture move flipped discs along that diagonal.
- **Pushback that kept Claude in check** — one student asked "Did I ask you to implement any parts in any of my prompts?" and got Claude to admit it had built all four modules unasked; the rewritten history records why. Another rejected Claude's edit twice because it duplicated text instead of replacing it. A third overruled Claude's recommended example sessions, neither of which showed a pass: "§8 must contain at least one pass (the brief requires it)" — the only example session that meets the brief.
- **Approving a ruling is not approving the text** — a ruling decides what should change; the amendment is the exact wording that goes into the document, and it needs its own approval. One student answered "go with recommended", and Claude edited the documents directly, though it had offered to show the new wording first.
- **The fixture file is a contract between implementations** — the brief sets its format and names the colors black and white "so the file stays independent of your code". Three of five changed the format without arguing all of it in the README: starting from a board laid out directly instead of a new game, and marking a pass some other way than the word "pass".
