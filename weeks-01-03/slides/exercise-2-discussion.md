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

## Exercise 2 discussion

<style scoped>
section { font-size: 18px; }
li { margin: 0.12em 0; }
</style>

- **Two failure modes, from one investigator, on the agent's claims** — missing evidence: claimed the search box was empty at load, never opened `index.html`; unchecked extrapolation: right that CI can't see a database bug, wrong about the fix that would surface it — different checks catch each, "did it read the file" vs. "does the last sentence carry the same citation standard"
- **A traced simulation is weaker evidence than a runnable test, no matter who traces it** — Claude pattern-matched an "off-by-one" from a quick read; a follow-up prompt forced an explicit trace of concrete state — the claim came back wrong. But a trace of three cases only proves the invariant for those three — an executable check (feed the code synthetic data, run it, assert on the output) proves it for as many cases as you generate, and can be re-run by someone else. Two students settled a separate bug this same way — running the suspect condition in Node across several inputs — same lesson, better executed. The same pattern-over-derivation failure showed up in `/init`'s own summary elsewhere in the batch: it described a conditional's apparent purpose, not what it actually computes — a narrow prompt to re-derive just those lines caught what the full-repo pass missed
- **A before/after comparison, not a controlled one — and that's the point** — same question asked vague vs. detailed, `/context` checkpointed around each instead of once at the end; two variables moved at once (phrasing *and* warm vs. cold session), and the write-up says so directly — naming your own confound beats missing it or overclaiming past it. The fix: run the detailed prompt in its own fresh session too, so phrasing is the only thing left to vary
- **The same bug, found twice, by different routes** — one by direct reading, one by a blind background agent in a fresh session — independent convergence is real evidence a defect exists, not a coincidence
- **Different prompts — or the same prompt twice — can surface different things** — most students independently found the same tautology bug in `neo4jApi.js`'s connection logic (a De Morgan's slip that makes a version-gating condition always true); one student's documented prompts never targeted that file specifically, and missed it. Without the raw session log there's no way to know whether that's a prompting difference or just which way a broad exploration happened to go — worth putting to the class directly rather than assuming