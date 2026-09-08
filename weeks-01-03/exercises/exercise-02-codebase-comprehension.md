# Exercise 2 — Codebase Comprehension with Claude Code

> **Assigned:** Lecture 03 · **Due:** before Lecture 05 · **Effort:** 2–3 hours
>
> **Requires:** Claude Code installed and authenticated (Claude Pro).

## Goal

Your first real Claude Code sessions — on a codebase you've never seen, in
*comprehension* mode. You will use the agent to build an accurate mental model of an
unfamiliar project, improve its machine-generated documentation with human intent, and
— critically — **catch the agent being wrong at least once**. You don't modify the
code in this exercise; the first agentic build is Project 1.

## Target codebase

**Repo:** <https://github.com/neo4j-examples/movies-javascript-bolt> at commit
`ad0172cef320`

A small browser application — jQuery front end, webpack build — that talks to a Neo4j
graph database through the official JavaScript driver: search movies by title, open a
movie to see its cast, vote for a movie, and render a force-directed graph of the
movie/actor network. Roughly 360 lines of source across five files.

It is deliberately small. Nothing here is hard because there is a lot of it; what is
unfamiliar is the *paradigm* — a graph database, Cypher queries embedded in
JavaScript, driver session semantics, and a build step that injects configuration you
will not find by reading the application code alone.

Clone it read-only and pin the commit so everyone explores identical code:

```
git clone https://github.com/neo4j-examples/movies-javascript-bolt
cd movies-javascript-bolt
git checkout ad0172cef320
```

**Running it.** `npm ci && npm start`, then open <http://localhost:8080>. You do not
need to install Neo4j: the build supplies default connection settings pointing at a
public demo instance. Where those defaults live, and what happens when you override
them, is one of the things you are here to figure out.

**On tests.** Answer the question set honestly about what this repository does and
does not verify. If you conclude something is missing, prove it — and then find out
whether the project verifies it somewhere else. `.github/` is part of the codebase.

**Keep the agent out of `package-lock.json`.** It is 8,000 lines — on the order of
90,000 tokens, most of a context window — and it tells you nothing that
`package.json` does not say in twenty-five. If the agent reaches for it, stop it.
Noticing that this is a decision *you* have to make is part of the exercise.

**Ground rules.** Work from the repository and the agent first — that is where the
value is. Cite anything you use from outside the repo in `architecture.md`, like any
other source.

The agent will read the repo's own documentation and tell you what it found. Good:
documentation states intentions, code states behaviour, and the gap between them is
what `gotcha.md` is for.

Show your route, not just your conclusions — the prompt you asked, what the agent
claimed, the file and line you checked it against. The trail is worth more than the
answer.

## Task

1. **Explore.** Start a Claude Code session in the repo. Use exploration prompts,
   @-mentions, and (if useful) plan mode's read-only analysis to answer the instructor
   question set below. Watch `/context` as you go — notice what exploring costs.
2. **Generate, then improve.** Run `/init`. Read the generated CLAUDE.md critically,
   then produce an improved version: correct what's wrong, cut what's noise, and add
   at least three things `/init` could not have known from the code alone (intent,
   conventions, gotchas you established by asking).
3. **Question set.** Answer in your own words (the agent may help you find evidence,
   but every claim must cite a file path you actually opened):
   - What does this system do, in one paragraph for a new teammate?
   - Trace the main data flow: from entry point to the core computation/state change
     to output/persistence.
   - Where are the tests, what do they actually cover, and what's conspicuously
     untested?
   - Find one design decision you'd question, and steelman why the authors did it.
4. **Catch it being wrong.** Document at least one instance where Claude's claim about
   the codebase was inaccurate, incomplete, or confidently overstated — and how you
   caught it (reading the source, running the code, running tests). If everything it
   said checked out, document the claim you *verified hardest* and how.

## Deliverable

A folder (zip or repo link) containing:

- `CLAUDE.md` — your improved version (mark your three-plus additions with `<!-- added -->`)
- `architecture.md` — 1–2 pages answering the question set, with file-path citations
- `gotcha.md` — the caught-being-wrong writeup (claim, evidence, how you checked)
- `reflection.md` — half a page: which exploration prompts earned their keep, which
  wasted context, and what you'd ask first next time

## Completion checklist (all required for satisfactory)

- [ ] Improved CLAUDE.md with ≥3 marked additions the generator couldn't know
- [ ] Question set answered with file-path citations throughout
- [ ] One verified inaccuracy (or hardest-verified claim) documented with evidence
- [ ] Reflection names specific prompts, not generalities
- [ ] No code modifications (comprehension only)

## Troubleshooting

- **Permission prompts on every file read:** normal on first contact — consider
  accepting reads for the session; keep write/execute prompts on.
- **Session feels sluggish or answers degrade:** check `/context`; a fresh session plus
  your improved CLAUDE.md re-gathers cheaper than compacting a bloated one (this is
  Lecture 06's topic — you're living it early).
- **Claude asserts something about the code you can't find:** that may be your
  `gotcha.md` — make it show you the file and line.
