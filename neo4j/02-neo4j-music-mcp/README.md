# Using MCP to explore and verify a music database

Connect Claude Code to a prepared Neo4j music database, ask precise questions,
and verify the answers. You will use an existing MCP server. You do not need
to implement one, design a database, or learn a recommendation algorithm.
The supplied data is entirely fictional and describes this fixture only.

Allow about 2–3 hours after host access is working. Submit the setup checkpoint
within two days of release and the complete work within one week, unless the
instructor supplies different dates. If setup takes more than 45 minutes, send
the instructor your sanitized diagnostic record rather than repeatedly changing
unrelated settings. Installation time estimates need classroom piloting.

Start with [SETUP.md](SETUP.md), then the [graph and Cypher primer](PRIMER.md).
The [fixture manifest](fixture/manifest.json) identifies `fictional-music-v1`.
It contains 36 tracks, 8 artists, 6 albums, 8 playlists, and 4 users. No inference
about real listeners, commercial popularity, or the Spotify catalogue is valid.
[Provenance and duplicate policy](fixture/PROVENANCE.md) explain the construction.

## Tasks

1. **Setup checkpoint.** Create a disposable instance, load the fixture, run the
   readiness check, configure the `music` server in your homework repository,
   and inspect `/mcp`. Record the database, provider, and host versions; fixture
   identity; readiness counts; discovered tools; and sanitized configuration.
2. **Explain the schema.** Ask the agent to inspect the actual schema. Save the
   schema-tool evidence and draw the path from a Playlist to an Artist. Explain
   the intermediate Track, relationship directions, and why IDs matter.
3. **Answer questions A and B below.** Ask for a proposed bounded read query
   first. Review its meaning, then ask the agent to execute it using `music`.
   Preserve actual arguments, Cypher, returned rows, and the final answer.
4. **Independently verify.** Run at least one supplied reference query in Neo4j's
   Query tool, outside the model conversation. Compare IDs, counts, ordering,
   and meaning with the agent-assisted result. Explain the query; a screenshot
   of matching prose alone is insufficient.
5. **Clarify ambiguity.** Give two possible meanings of “Which artist is most
   popular?” Choose one supported by this fixture and restate it precisely.
   Explain what data the other interpretation would need. You may reuse A.
6. **Diagnose and reflect.** Explain one encountered failure or the provided
   failure case below. Identify the failing layer and next check. Briefly state
   what the agent helped with and what still required your judgment.

**Question A.** Which five artists appear in the greatest number of distinct
playlists in this fixture? Credit every artist on a collaboration. Count a
playlist at most once per artist. Return artist ID, name, and playlist count;
order by count descending, then artist ID ascending for ties.

**Question B.** For playlist **P01**, which other playlists share at least one
distinct track? Exclude P01. Return the top five playlist IDs, names, and
shared-track counts; order by shared-track count descending, then playlist ID
ascending for ties. “Shared” means the same track ID, not a similar title or
an artist in common.

Use two prompts so you can examine the query before requesting execution:

> Use the music MCP server to inspect the schema. Propose a bounded read-only
> Cypher query for [paste the full question]. Explain how it avoids duplicate
> counting. Show the query before executing it.

After reading it:

> Run the reviewed query using the music MCP tool. Show the returned rows and
> answer using those rows. State that the result describes fictional-music-v1.

A prompt is not an execution boundary enforced by the database. Watch what the
host actually does. If it executes early, record that fact rather than rewriting
the history. Preserve a mistaken first query and its correction; first-attempt
perfection is not the assessment target.

## Reference execution

Open Query for the disposable instance and paste one of the complete queries in
[question-a.cypher](queries/question-a.cypher) or
[question-b.cypher](queries/question-b.cypher). Run it directly and save the result.
These are intentionally supplied so this task tests explanation and verification,
not whether you can hide an answer from an agent. Do not claim that replaying a
query is independent evidence about every aspect of data loading; the instructor
also checks the fixture with a separate CSV-based implementation.

Provided diagnosis case, observed during preparation: the database accepted
direct read queries, but the MCP provider rejected connection because APOC's
meta procedures were missing. Which layer was healthy? Which additional
requirement failed? Why would changing the question prompt not repair it?

## Submission

Use this structure, adjusting filenames only if the instructor requests it:

```text
music-mcp-homework/
  README.md
  .mcp.json
  queries/question-a.cypher
  queries/question-b.cypher
  evidence/connection.md
  evidence/schema.md
  evidence/question-a.md
  evidence/question-b.md
  evidence/verification.md
  reflection.md
```

Copy [EVIDENCE.md](EVIDENCE.md) as a template. Include reproducible queries and
small result tables; sanitized tool exports or screenshots plus readable text
are acceptable. Exclude passwords, account identifiers, local environment files,
and unrelated conversation history. Record agent assistance and explain the
queries in your own words. Exact model wording and a prescribed call count are
not requirements.

| Criterion | Points |
|---|---:|
| Reproducible setup and configuration | 15 |
| Schema understanding | 10 |
| Correct query semantics, distinct counts, exclusions, ties, bounds | 25 |
| Actual tool/results and grounded answer evidence | 20 |
| Direct reference execution and explained comparison | 20 |
| Ambiguity, diagnosis, and reflection | 10 |
| Total | 100 |

If provider/network/host access prevents completion, submit the diagnostic record
at the checkpoint. The instructor can supply recorded schema/results for a
labeled evidence-analysis path and arrange a later live setup check. Recorded
analysis is not a successful live connection; do not claim it is. The instructor
will specify any accommodation deadline. You need not intentionally break a
working setup or grant the agent write access.

Instructional prose follows [CC BY 4.0](LICENSE-CC-BY-4.0); code, configuration, and the
fictional fixture follow [MIT](LICENSE-MIT), as [fixture/PROVENANCE.md](fixture/PROVENANCE.md)
states. `export_students.py` copies this student package alone into an empty directory.
