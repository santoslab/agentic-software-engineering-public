# Software Engineering Module Reading List

Tags: **[required]** — assigned before a lecture, assumed in class · **[recommended]**
— strengthens the lecture · **[gap-filler]** — for students who have not taken a
prior software-engineering course; skimmable by those who have.

Entries are grouped by the lecture that assumes the reading, with the lecture that
assigns it in parentheses. Each entry is one bullet: tag, author, title, venue and
year, URL, and a one-sentence note on why it is assigned or what to skim.

URLs verified 2026-09-16 unless marked ⚠ verify.

## For Lecture 01 (read before the module's first meeting)

- **[required]** The Lecture 01 handout,
  [`student-materials/handout-lecture-01-note-set-starter.md`](student-materials/handout-lecture-01-note-set-starter.md)
  (PDF alongside it): the draft specification, the loader `CLAUDE.md`, and the
  three process documents, copied from `demos/lecture-01-note-specs-demo/starter/`.
  Ten minutes. Class time is not spent reading them.
- **[recommended]** Bradner, *Key words for use in RFCs to Indicate Requirement
  Levels* (RFC 2119, 1997) — <https://www.rfc-editor.org/rfc/rfc2119>. The
  MUST/SHOULD/MAY vocabulary the specification uses.

## For Lecture 02 (assigned at L01)

- **[required]** Royce, *Managing the Development of Large Software Systems*
  (Proceedings of IEEE WESCON, 1970; reprinted in Proceedings of ICSE 9, 1987) —
  ⚠ verify: the usual PDF mirrors returned 403 or 404 on 2026-09-16; the ACM
  Digital Library entry is <https://dl.acm.org/doi/10.5555/41765.41801>. The paper
  usually cited as the origin of the waterfall model; read for its argument that
  information must flow backward between phases. It is the subject of the demo's
  first note.
- **[required]** Meyer, *Applying "Design by Contract"* (IEEE Computer, 1992) —
  <https://se.inf.ethz.ch/~meyer/publications/computer/contract.pdf>. The
  precondition and postcondition are the form Lecture 02 gives to an operation
  in the concept of operations.
- **[required]** The Lecture 02 handout,
  [`student-materials/handout-lecture-02-conops-and-operations.md`](student-materials/handout-lecture-02-conops-and-operations.md):
  the draft concept of operations and the three process documents Lecture 02
  adds. Ten minutes.

## For Project 0 (assigned at L02)

- **[required]** The Project 0 brief,
  [`project-0-pkb-brief.md`](project-0-pkb-brief.md), in full, and its §3 before
  the OKF specification.
- **[required]** Google, *Open Knowledge Format (OKF) specification*, v0.2 —
  <https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md>.
  Read after the brief's §3, which says which of its fields the course uses.
- **[recommended]** The example bundle,
  [`student-materials/pkb-example/`](student-materials/pkb-example/index.md),
  opened in Obsidian or any Markdown viewer; five minutes.

## For Lecture 03 (assigned at L02)

- **[required]** The Lecture 03 handout: the game's `CONOPS-sketch.md` and the
  process set as shipped in that demo's starter. Ten minutes.
- **[recommended]** The concept-of-operations template (the full skeleton, with
  sections 2, 3, and 6 marked as applying only when an existing system is being
  improved).
- **[recommended]** The course catalog of specification kinds,
  [`../specification-kinds.md`](../specification-kinds.md): the summary table
  and the entries for the eight kinds Lecture 03 derives; fifteen minutes.
  Return to it at Lectures 04 and 06 for the fixtures, the test suite, and the
  tool contract.

## For Lecture 04 (assigned at L03)

- **[required]** `process/verification.md` at its Lecture 04 level, VER-5
  through VER-8:
  [`demos/lecture-03-game-demo/reference/process/verification.md`](demos/lecture-03-game-demo/reference/process/verification.md).
  Four rules, two pages; the lecture applies each of them.
- **[required]** The fixtures README:
  [`demos/lecture-03-game-demo/reference/fixtures/README.md`](demos/lecture-03-game-demo/reference/fixtures/README.md).
  The loader contract and the stated blind spots; five minutes.
- **[recommended]** coverage.py, *Branch coverage measurement* —
  <https://coverage.readthedocs.io/en/latest/branch.html>. What a partial
  branch is and why an executed line can still be an uncovered branch.

## For Lecture 05 (assigned at L04)

- **[required]** The Project 1 brief,
  [`project-1-reversi-brief.md`](project-1-reversi-brief.md), in full.
- **[required]** The Reversi concept-of-operations sketch,
  [`student-materials/reversi-starter/CONOPS-sketch.md`](student-materials/reversi-starter/CONOPS-sketch.md),
  read as a player (five minutes). Do not read the rules of Reversi elsewhere;
  Lecture 05 learns them from the sketch, and the gaps in it are the point.

## For Lecture 06 (assigned at L05)

- **[required]** Model Context Protocol, *Core concepts* —
  <https://modelcontextprotocol.io/docs/concepts/tools> ⚠ verify. Tools, their
  schemas, and how a model decides to call one; the tool contract Lecture 06
  treats as a specification.
- **[required]** The MCP Python SDK's FastMCP quickstart —
  <https://github.com/modelcontextprotocol/python-sdk#quickstart> ⚠ verify. The
  ten-line server the lecture's tic-tac-toe server follows.
- **[required]** The dice-server README from the project unit,
  [`../weeks-04-07/student-materials/mcp-example/README.md`](../weeks-04-07/student-materials/mcp-example/README.md).
  How a server is registered and what the agent sees; five minutes.
- **[recommended]** The *interface contract* and *tool contract* entries of the
  course catalog, [`../specification-kinds.md`](../specification-kinds.md).
