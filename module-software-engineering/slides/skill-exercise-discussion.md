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

## Skill exercise discussion (1/4): each skill re-run 4 times, 3 tic-tac-toe, 1 [Lecture 01 note set](https://github.com/santoslab/agentic-software-engineering-public/tree/main/module-software-engineering/demos/lecture-01-note-specs-demo/completed) *(without `note-set-operations.md`)*

<style scoped>
section { font-size: 21px; }
h2 em { font-size: 0.65em; font-style: normal; }
li { margin: 0.15em 0; }
</style>

- **A cited source may not say what the model claims; the model can read more or less into it** — a report lists as "settled" what the repository already answers, and the developer is not asked to rule on those.
  - In three of five skills, a run listed as settled something no document states, for example "There is no mid-game quit" and "the no-commit rule — settled by RPT-5 and DEV-7."
  - In two of them, run 2 treated quitting mid-game as settled, citing CONOPS sections that are silent on it and a process example that defers it; runs 1 and 3 of the same two skills asked about it instead.
  - In two runs, Sonnet 5.5 listed the skill's own "do not commit" instruction among the settled rules, although the repository requires a commit after each operation.
  - Two skills tell the model never to list as settled anything no document states; their runs followed that.
  - With one run per version, you would have seen only one of the two answers on quitting mid-game.
- **The model followed a simple instruction every time** — every skill tells the model to stop after each step and wait for the developer to rule on its questions.
  - In all 20 re-runs, including the note set, Sonnet 5.5 stopped with a list of questions and wrote no file.
  - For contrast, one student asked "Write SPECS.md from CONOPS.md" without the skill: the model wrote the whole `SPECS.md` first, deciding every open question itself, and asked for rulings only afterwards.
  - A judgment instruction, such as never listing as settled what no document states, was followed less reliably.

---

## Skill exercise discussion (2/4)

<style scoped>
section { font-size: 23px; }
li { margin: 0.2em 0; }
</style>

- **Each skill, as the exercise asked, targets `SPECS.md` with tic-tac-toe's sections; the note set's `CLAUDE.md` calls for a different document, an operations specification. Sonnet 5.5 noticed, then mostly followed the skill.**
  - In three skills, the run pointed out the conflict (for example, that the note set has none of the tic-tac-toe kinds) and still recommended `SPECS.md` or the tic-tac-toe sections; a fourth asked which target to use and left it open.
  - On renaming those sections to fit the note set, one run wrote: "This breaks the instruction."
  - The fifth skill's run followed the note set's own list of documents instead.
  - In reflections, all five students had predicted that their skill's game-specific parts would not carry over to a project that is not a game.
  - What should a skill state itself, and what should it read from the repository?

---

## Skill exercise discussion (3/4)

<style scoped>
section { font-size: 22px; }
li { margin: 0.2em 0; }
</style>

- **A gap no document addresses: how to test a random opponent** — the CONOPS says the computer picks a legal move uniformly at random, and nothing in `process/` says how a test can check that.
  - All 15 tic-tac-toe runs asked about it; one put it as "Uniformity cannot be decided by one expected value."
  - Why it matters: if the specification never says how randomness is tested, tests can check only that each move is legal, and an opponent that does not choose at random passes.
    - In Project 1, an opponent that chose randomly only when it had exactly four legal moves, and otherwise always took the first legal move, still passed a whole test suite.
- **Every question costs the developer a ruling** — a list of questions helps only if most are worth answering.
  - On the note set, the lists ran from 15 to 40 questions, and two fifths to two thirds of them were low-stakes, trivial, already answered by the repository, or about the skill itself.
  - On tic-tac-toe, the lists were about as long (roughly 14 to 30 questions per run).
  - For discussion: a developer must rule on every question. How long can the list get before rulings turn into rubber stamps, and should a skill ask fewer questions even if it misses some?

---

## Skill exercise discussion (4/4): what each line of your note checked

<style scoped>
section { font-size: 19px; }
table { font-size: 17px; }
th, td { padding: 4px 10px; }
</style>

| | Item | What was checked |
|---|---|---|
| **Evaluation** | Key committed before the runs | In your git history, the commit adding `key.md` comes before the first run transcripts |
| | Runs per version | At least three scored runs for each version of the skill |
| | Behavior and precision checked | Each run's record says whether it stopped, wrote or invented a rule, and how many questions were worth asking, not only which key gaps it found |
| | Negative trigger tests | Prompts that should not start the skill did not; for "Write SPECS.md from CONOPS.md", what happened without the skill |
| | Misses reported | The evaluation names the gaps a run missed or only half asked |
| | Reason to stop | The evaluation says why you stopped changing the skill |
| **Design** | Description says when and when not | The front-matter description names when to use the skill and when not to |
| | User-invoked only | `disable-model-invocation: true`, so only `/specs-from-conops` starts it |
| | Phases end in stops | Each phase ends by waiting for the developer's rulings before anything is written |
| | Output grouped by kind | The report groups questions by kind of specification (AUD-8 to AUD-14) |
| | A bundled file the body sends the model to | `SKILL.md` points the model to a supporting file it must read |
| | Lines carrying an answer | No line in the skill states a tic-tac-toe answer instead of asking the question |
