# Music homework instructor key

This directory is not part of the student package; it sits beside the lecture that launches the homework, apart from the homework folder under `neo4j/`. Students receive the precise questions,
reference Cypher and open verification code; the assignment assesses explanation
and evidence, not answer secrecy. The live capture and grading notes are instructor
fallbacks and must not be mistaken for student model transcripts.

## Fixture and expected answers

The fixture is original, fictional, deterministic, and versioned as
`fictional-music-v1`. The [CSV oracle output](expected-answers.json) was computed
without Neo4j. The [live capture](live.json) records real direct-driver results
and official provider schema/read calls, checked against that oracle. It is
LLM-free. It does not establish Claude Code selection or model grounding.

Question A's rows are:

| Artist ID | Name | Distinct playlists |
|---|---|---:|
| A07 | Glass Meadow | 8 |
| A08 | Indigo Current | 8 |
| A01 | Amber Circuit | 5 |
| A02 | Blue Orchard | 5 |
| A03 | Copper Kite | 4 |

Question B's rows are:

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

## Grading and feedback

Use the handout's 100-point rubric. Award configuration credit for correct project
scope, explicit versions/fixture, external credentials and readiness evidence;
not merely a copied configuration. Schema credit needs the Playlist→Track→Artist
path and relationship directions. Query credit requires the requested population,
DISTINCT target, P01 exclusion, tie ordering and LIMIT. Evidence credit requires
actual calls/results and a final answer that follows from them. Direct replay
credit requires a comparison and explanation, not just a second screenshot.

Common mistakes: count(*) counts paths; counting artists on one track selects
only a primary credit; grouping by name merges distinct playlists; forgetting
source exclusion counts P01 itself; LIMIT without ORDER BY does not rank; calling
shared artists “shared tracks” changes question B. Preserve and assess corrections.
Do not require a particular model sentence or exactly two tool calls.

For “most popular,” accept multiple interpretations such as streams, listeners,
playlist appearances, or preferences if the student distinguishes them and chooses
a supported definition. The fixture has no streams/listening history. A good
reflection identifies what the student checked rather than praising the agent.

Actual setup failure cases are in
[failure-cases.json](../../../../neo4j/02-neo4j-music-mcp/evidence/failure-cases.json).
They distinguish direct backend readiness, provider requirements, discovery,
and schema execution. Do not require students to induce failures themselves.

## Instructor reproduction and export

From `neo4j/02-neo4j-music-mcp/` after the documented environment setup:

```sh
uv run --frozen python music_data.py
uv run --frozen python database.py check
uv run --frozen python verify_live.py --output ../../module-software-engineering/demos/lecture-mcp-adoption/neo4j-music-instructor-key/live.json
uv run --frozen pytest -q
uv run --frozen python export_students.py /tmp/music-student-bundle
```

The explicit export includes the fixture/generator/provenance, lock, scripts,
reference queries, handout, primer, diagram and tests. It excludes the instructor
key, saved live result, local environment, account state, and credentials. Run
from a nonexistent or empty export destination. Check the exported setup with a
fresh environment before assigning it.

Use the saved schema/results for evidence analysis if live access fails, labeling
that path and arranging the later live checkpoint described in the handout.
Do not count saved evidence as a successful student connection. Pilot the 2–3
hour estimate and Desktop GUI instructions before setting calendar dates.
