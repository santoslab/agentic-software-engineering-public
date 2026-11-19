# Music homework instructor key

This directory is not part of the student package. It sits beside the lecture
that launches the homework (the MCP Neo4j lecture, `lecture-mcp-neo4j`), apart
from the homework folder `neo4j/02-neo4j-music-mcp/`. Students receive the
precise question, the reference Cypher, and the open verification code; the
assignment assesses review, evidence, and verification, not answer secrecy.
The captures here are instructor fallbacks and must not be mistaken for
student transcripts.

## Fixture and expected answers

The fixture is original, fictional, deterministic, and versioned as
`fictional-music-v1`. The [CSV oracle output](expected-answers.json) was computed
without Neo4j.

Question A's rows are:

| Artist ID | Name | Distinct playlists |
|---|---|---:|
| A07 | Glass Meadow | 8 |
| A08 | Indigo Current | 8 |
| A01 | Amber Circuit | 5 |
| A02 | Blue Orchard | 5 |
| A03 | Copper Kite | 4 |

Question B's rows (an optional extension in the current handout) are:

| Playlist ID | Name | Distinct shared tracks with P01 |
|---|---|---:|
| P02 | Mix 2 | 6 |
| P03 | Evening | 6 |
| P07 | Mix 7 | 4 |
| P08 | Mix 8 | 4 |
| P04 | Evening | 2 |

A collaboration credits every artist. Repeated occurrences and repeated CSV
records do not inflate distinct-playlist or distinct-track counts. P03 and P04
have the same display name and must stay separate. P01 is excluded from B.
Tie ordering is by ID, not name or incidental database order. No answer describes
real popularity or recommendation quality.

## The write cycle

Students create playlist `P09` with a name and three to five tracks of their
own choosing, owned by `U01`, then delete it. The expected `database.py check`
mismatch is exactly: Playlist 9 (was 8), OWNS 9 (was 8), PLAYLIST_HAS_TRACK
89 + N where N is the number of tracks added; every other count unchanged.
After the revert all nine counts match. In the instructor's pilot
(2026-11-18) with four tracks: 9 / 9 / 93, then a pass.

The permission dialog students must record reads `Tool use` /
`neo4j — Write Cypher Tool: (MCP)` / the `query` / `About the neo4j — Write
Cypher Tool:` / `Do you want to proceed?` with the options `1. Yes`,
`2. Yes, and don't ask again for neo4j — Write Cypher commands in <project
path>`, `3. No`. It appears only in manual permission mode. Evidence that
shows no dialog and no `manual mode on` line means the student was in auto
mode: feed that back as a finding; it is not by itself a failing write part
if the write and the revert are otherwise verified in Query and by `check`.

## Grading and feedback

Use the handout's 15-point completion rubric: setup 5, read 4, write 4,
reflection 2.

- Setup credit needs the `check` output on database `music`, the `/mcp` tool
  list with the model-visible names, the mode line, and a `.mcp.json` whose
  password is a `${NEO4J_MCP_PASSWORD}` reference; not a copied example alone.
- Read credit needs the proposed Cypher, a review that names what was checked
  (labels and directions, the `Playlist` anchor, `count(DISTINCT p)`, both
  sort keys, `LIMIT`), the call with its rows, and a Query replay with a
  comparison, not a second screenshot.
- Write credit needs the tool count change, the proposal and review, the
  dialog wording, the read-back rows, the mismatch with the counts that moved,
  and the passing check after the revert.
- Reflection credit goes to what the student checked and where it became
  visible, not to praise of the agent.

Common mistakes: `count(*)` counts paths; anchoring on `Album` or omitting the
label counts album membership; grouping by name merges distinct playlists
(P03 and P04 are both "Evening"); `LIMIT` without `ORDER BY` does not rank;
merging the user or the tracks instead of matching them creates phantom
nodes on a typo; a `DETACH DELETE` without the id filter removes every
playlist (the check then shows Playlist 0); choosing the dialog's "don't ask
again" option, which writes a standing allow rule. Preserve and assess
corrections. Do not require a particular model sentence or exactly two tool
calls. The model's wording of its own "wait for approval" varies ("approved",
"go") and is not the control; the dialog is.

Optional extensions: for Question B see the table above; for "most popular",
accept streams, listeners, playlist appearances, or preferences if the student
distinguishes them and chooses a supported definition (the fixture has no
streams); for a diagnosis, the student should name a layer and a next check.
Actual failures with their texts are in
[failure-cases.json](../../../../neo4j/02-neo4j-music-mcp/evidence/failure-cases.json)
(2026-11-16 command-line rehearsal; 2026-11-18 Desktop pilot). Do not require
students to induce failures.

## Captures

- [`expected-answers.json`](expected-answers.json): the CSV oracle, computed
  without Neo4j.
- [`live.json`](live.json): LLM-free direct-driver results and official
  server schema/read calls checked against the oracle, captured 2026-11-16 on
  Neo4j 5.26.0 Community through the package's former launcher. The same
  capture on the Desktop edition students use (Neo4j 2026.10.0 Enterprise,
  2026-11-18) is [`../reports/live-desktop.json`](../reports/live-desktop.json);
  the full pilot record is [`../reports/desktop-pilot.md`](../reports/desktop-pilot.md).
  Regenerate `live.json` with the command below once the rewritten verifier
  has run against the piloted database.

Neither capture establishes model tool selection or answer grounding.

## Instructor reproduction and export

From `neo4j/02-neo4j-music-mcp/` with the SETUP.md variables set:

```sh
uv run --frozen python music_data.py
uv run --frozen python database.py check
uv run --frozen python verify_live.py --output ../../module-software-engineering/demos/lecture-mcp-neo4j/instructor-key/live.json
uv run --frozen pytest -q
uv run --frozen python export_students.py /tmp/music-student-bundle
```

The export includes the fixture, generator, provenance, lock, scripts,
reference queries, handout, setup file, primer, evidence template,
`.mcp.json.example`, `.claude/settings.json`, diagram, and tests. It excludes
this key, any saved live result, the local environment, account state, and
credentials. Run it against a nonexistent or empty destination, and check the
exported setup in a fresh directory before assigning it.

Use the saved captures for a labeled evidence-analysis path if a student's
live access fails, and arrange the later live check the handout describes.
Do not count saved evidence as a successful connection. The one-hour estimate
comes from the instructor's pilot (about 20 minutes of terminal work, 45 of
read rehearsal, and 30 of write rehearsal, including note taking); it has not
been piloted with students.
