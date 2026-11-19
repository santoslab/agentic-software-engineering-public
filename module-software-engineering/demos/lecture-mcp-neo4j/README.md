# Neo4j through a local MCP server: demo folder

Materials of the third MCP lecture, in which Claude Code is connected to a
Neo4j Desktop database through the official `neo4j-mcp-server`, started as a
child process from `.mcp.json`, and used to read and write the fictional
music fixture of the [homework](../../../neo4j/02-neo4j-music-mcp/README.md).

- [`DEMO.md`](DEMO.md): the in-class script, with exact prompts, commands,
  expected observations, and a fallback for every beat.
- [`.mcp.json.example`](.mcp.json.example) and
  [`.mcp.json.write.example`](.mcp.json.write.example): the read-only and
  write configurations the demo switches between; one field differs.
- [`PILOT.md`](PILOT.md) and [`reports/desktop-pilot.md`](reports/desktop-pilot.md):
  the instructor's pilot instructions and its record of 2026-11-18, the source
  of every quotation, screenshot, and error text in the lecture; the optional
  steps D6 (database role) and D7 (dump and restore) are still open.
- [`pilot_desktop_check.py`](pilot_desktop_check.py): LLM-free readiness
  check of a Desktop instance and of the server in both modes; run from the
  homework package so its locked environment supplies the driver and the MCP
  client. `pilot_shot.sh` files screenshots by name.
- `reports/live-desktop.json` and `reports/pilot-report.json`: the LLM-free
  captures on Neo4j 2026.10.0 Enterprise (tool lists, schema result, the two
  reference queries).
- [`instructor-key/`](instructor-key/README.md): expected answers, the
  expected check mismatch, dialog wording, grading notes. Not exported to
  students.
- [`planning/`](planning/neo4j-lecture-and-homework-plan.md): the plan, its
  decisions, and the approved outline of the lecture notes.

The lecture's three artifacts are the
[instructor outline](../../lectures-instructor-notes/lecture-mcp-neo4j.md),
the [student notes](../../lecture-notes/lecture-mcp-neo4j.md), and the
[slides](../../slides/lecture-mcp-neo4j.md). Screenshots of Claude Code are in
`../../slides/images/mcp-neo4j-*.png`; Desktop screenshots in
`../../../neo4j/resources/`. The student procedure is the
[setup guide](../../../neo4j/neo4j-desktop-mcp-setup.md).

Nothing in this folder is an active configuration. The examples are copied
into a scratch repository for each rehearsal; the password is never written
to a file.
