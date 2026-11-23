# Connecting an agent to a database through a local MCP server: Neo4j

75-minute instructor outline. This meeting follows the adoption lecture,
precedes the dice implementation lecture, and launches the music homework.
Students have seen `.mcp.json`, `/mcp`, `tools/list`, and the evidence
discipline of the adoption lecture; they have a Neo4j Desktop instance from
exercise 01. The [student notes](../lecture-notes/lecture-mcp-neo4j.md) are the
full tutorial, with every screenshot and quotation from the 2026-11-18 pilot;
do not compress them to match classroom time. The lecture is a demonstration
on a prepared instance with explanation between the beats; nothing is
installed in class.

## Outcomes and evidence

Students should be able to write the stdio server entry and say which process
reads each field and why the password is a reference; name the three
processes (host, server, database) and say which one proposes the Cypher,
which routes and asks permission, and which executes it; read a `tools/list`
result for this server and explain why `write-cypher` is present or absent;
review a proposed Cypher statement against the schema and the question
(anchor label, direction, distinct count, ties, bound, no write clause);
verify a result by replaying the statement in Desktop's Query tool and a write
by reading it back and running a check; name the three controls on writes and
the failure each does not prevent; and say where the record of an executed
statement lives on the database side. In class, students watch; the homework
collects the evidence.

Use [DEMO.md](../demos/lecture-mcp-neo4j/DEMO.md) for the exact prompts,
commands, and fallbacks, [the homework](../../neo4j/02-neo4j-music-mcp/README.md)
for task wording, the [setup guide](../../neo4j/neo4j-desktop-mcp-setup.md) for
the student procedure, and the [pilot report](../demos/lecture-mcp-neo4j/reports/desktop-pilot.md)
for what actually ran. Everything the slides quote was observed in that pilot;
model output is labeled as such and varies between sessions.

## Before class

- The instance is running with APOC installed, the `music` database loaded,
  and `database.py check` passing. Keep the homework package's terminal open
  with the `NEO4J_MCP_*` variables set; every Claude Code session and every
  check line in the demo starts from that terminal.
- The `uvx` cache is warm (`uvx neo4j-mcp-server@2.1.1 -v`), so the first
  session start in class is not a download.
- A fresh scratch directory per rehearsal and per class, holding `.mcp.json`
  (read-only form) and `.claude/settings.json` (the two allow rules). The
  model recalls memory files from earlier sessions in the same directory and
  reads `.mcp.json` with ordinary tools; the password must be a reference.
- Start every session with `claude --permission-mode manual` and confirm the
  mode line. The instructor's own default is auto mode, in which the write
  dialog never appears; the 2026-11-18 pilot lost that beat once this way.
- Desktop's Query tool open with the Database selector on `music`. A second
  terminal in the homework package for `query_log.py`.
- Know which beats have captures: `/mcp` drill-down (images 01–05), the read
  call (06), the two failures (07, 08), three tools (09), the write session
  (10–16), the dialogs (17–24), the deny rule (25), and the Desktop screens
  in `neo4j/resources/`. The LLM-free JSON is `reports/live-desktop.json`.
- Review the notes' Sections 6.4 and 6.7 before class: the two approvals and
  the deny-rule finding are the parts most easily misstated.

## Timed sequence

| Minutes | Slides | Actions and expected observations | Fallback or cut |
|---|---|---|---|
| 0–5 | 1–2 | Cold open in the scratch repo: the one-line prompt for the five artists. Expand the `get-schema` and `read-cypher` calls, the Cypher argument, the five rows, the answer naming the fixture. | Image 06 and the rows from `live-desktop.json`. |
| 5–15 | 3–9 | What changes architecturally. The two declarations beside each other; the three-process diagram and the responsibility table; `env` as the server's configuration and `${VAR}` as host expansion; `read-cypher`'s schema beside `microsoft_docs_fetch`, that schema filled by the opening demo's call, and the rows inside the text block; the side-by-side table. | If short, cut slide 9 to three rows; Section 1.7 of the notes has the full table. |
| 15–27 | 10–15 | Activating the server. Desktop in one slide (instance, databases, APOC once, one database per activity; procedure in the guide). The entry field by field. Start a session, `/mcp`, drill into `neo4j`, the tool list, the `read-cypher` detail. Manual mode, the mode line, the settings file. One deliberate failure: a second terminal without the variables, `/mcp`, the diagnostics text; name the layer; show where the real cause is logged. | Images 01–05, 17, 07-a/b. Keep the failure beat even if everything else is images; it is the diagnosis lesson. |
| 27–40 | 16–18 | Reading with review. Schema prompt; compare the model's table with the diagram. Propose prompt; say what the statement is meant to compute, then read it against the checklist on the slide, in particular the `Playlist` anchor and `count(DISTINCT p)`. Run prompt; expand the call; paste the statement into Query with `music` selected; same rows. Ask the class for two meanings of "most popular". | Image 06, Desktop image 09. If short, drop the replay to the notes; keep the review. |
| 40–56 | 19–24 | Writing with control. Exit, flip `NEO4J_MCP_READ_ONLY`, restart, `/mcp` shows three tools. Shared-tracks read. Write prompt with the ids spelled out; the model's precondition read; the proposed MERGE read clause by clause. "approved"; the host dialog; read it aloud; option 1. Read-back in Query. The fixture as the saved baseline; the `!` check line: mismatch 9 / 9 / 93. Revert prompt; second dialog; check passes. Three-controls diagram and the deny-rule finding. | Images 09–16 and 24, Desktop image 10. If behind, show the dialog (24), the mismatch (13), and the controls slide only. |
| 56–64 | 25–26 | Records and recovery. `query_log.py --last 10` in the second terminal: the write, the `EXPLAIN` before each read, one transaction per statement, the server's startup probes. Then the advice for a database that matters: contain, snapshot, copy, dry runs, what to do after. | Slide 25 carries the real output. Cut 26 to its four headings if behind; Section 10 of the notes has the detail. |
| 64–70 | 27–28 | The recipe as a list; the homework's six tasks, with setup done early; the OpenFlights follow-on in one sentence. | Keep the homework slide; the recipe is in the handout. |
| 70–72 | 29 | Exit question and the bridge to the dice lecture. | — |
| 72–75 | — | Slack. | — |

Blocks sum to 72 minutes with 3 minutes of slack.

## Main walkthrough

**The architectural contrast is the lecture's argument; make it in the first
fifteen minutes and return to it.** Put the adoption entry and today's entry
on one slide and let students name what is new: `command` and `args` instead
of `url`, an `env` block, a password reference. Then the three processes. The
sentence to land is that the server is not the capability: it is an adapter
holding one driver connection to a database the student owns, and the Cypher
executes in the database with the privileges of the account the server logged
in with. The responsibility table gives the answer to "who did what" at every
step and names the evidence of each; the rest of the lecture fills the
evidence column.

**The argument is a program.** The `read-cypher` schema is a required string.
Say plainly that the schema cannot tell anyone whether the string counts paths
or distinct playlists or contains a delete, and that this is why a step is
added that the adoption lecture did not need: the statement is proposed,
read by a person against the schema and the question, and only then run. The
result is rows as JSON inside the text block; the same statement can be
replayed in Query, which is the independent route the adoption lecture did not
have.

**Activation.** Keep the Desktop material to one slide and send students to
the guide; the point in class is what the host does with the entry: reads the
file, asks for approval once, expands variables, spawns `uvx`, the server
checks its requirements against the database, `tools/list`. Show the server's
log lines for that sequence. The `/mcp` drill-down mirrors the adoption
lecture's five screens; dwell on the tool annotations and the full model-visible
name. The permission-mode slide matters more than it looks: in auto mode no
dialog appears, and students whose default is auto will never see the control
the write beat depends on. Show the mode line and the allow rules, and say
why the two reads are pre-allowed (seven read dialogs before the first write
in the pilot).

**The failure beat** is a second terminal without the variables. `/mcp`
shows the diagnostics block naming the missing variable; name the layer (host
configuration, before any process starts). Then say where the server's own
words are: the per-server log, with the `Unauthorized` text from the literal
`${NEO4J_MCP_PASSWORD}`. The stopped-instance failure (`Failed to reconnect
to neo4j: 0`) is the second row; show it from the capture rather than stopping
the instance in class.

**Reading with review.** Three prompts, each with a reason: schema first
because the model has not seen the labels; propose without executing so that
the statement can be read; run and expand the call so that the argument and
the rows are visible. The review checklist is on the slide; the two checks
that catch real errors are the `Playlist` anchor (both Album and Playlist
have `HAS_TRACK`) and `count(DISTINCT p)`. The pilot's proposal differed from
the reference only in a `WITH` stage and alias case; say that different
sessions produce different statements and that the homework assesses the
review, not the match. Replay in Query with the selector on `music` and name
what the replay does and does not establish.

**Writing with control.** The one-field change and the tool count prove that
discovery follows the server's configuration. Spell the ids out in the write
prompt; a fresh session that hears "those four shared tracks" infers. Point
out the model's unrequested precondition read. Read the MERGE clause by
clause: matched user and tracks, merged playlist and relationships, a
position on each, a `RETURN`. Then the two approvals. The model's "say
approved" is a courtesy whose wording varies; the host dialog is the control,
and it appears only in a prompting mode. Read the dialog aloud, including the
second option and why it is never chosen for a write. The records show the
dialog open for two and a half minutes in the pilot. Verify three ways:
read-back in Query, the `!` check line with its exact mismatch, and (in the
records block) the query log. Revert, second dialog, check passes.

**Three controls.** Use the diagram's wording: the server flag decides whether
the tool exists, the host rules whether the model may call it, the database
account what any client may do, and only the last holds on every route. Tell
the deny-rule finding as it happened: `/mcp` still listed three tools, the
model's catalogue had two, there was no refusal message, the model blamed the
server's configuration and then proposed a direct connection, and the
instructor declined the shell dialog. State that the database-role control
was described from documentation and not exercised in the pilot.

**Records.** Run `query_log.py` live; it is the one beat that shows the
database's own account with no model in the loop. Point at the write as one
transaction, the `EXPLAIN` before each read, the `MCP4NEO4J/2.1.1` client,
and the failed `gds.version` probe. Give the prompt recipe in one sentence:
ask the model to list what it ran, then compare with the log.

**Recovery.** Two minutes, from the slide: there is no undo through the tool;
contain (one database, read-only by default, deny rule or dialog, a reader
account), snapshot the counts, take a copy before a write session (Desktop
export or `neo4j-admin database dump`, both documented and untested in the
pilot), dry-run writes (read first, id anchors, `RETURN` what changed,
`EXPLAIN`), and after a mistake: stop writing, list what ran, measure, inverse
or restore.

## Student activity and understanding checks

Students do not type in class; the homework reproduces every beat in about an
hour with the same prompts. Ask during the lecture: which process executes
the Cypher; what the model sees when it reads `.mcp.json`; why `/mcp` showed
three tools while the model had two; what would have held if the model had
taken another route to the database; which of the three records of a
statement the model cannot influence. Ask for the two readings of "most
popular" before the model picks one.

## Homework launch and instructor key

The [homework](../../neo4j/02-neo4j-music-mcp/README.md) is the lecture on the
student's own instance: instance ready, fixture loaded and checked, Claude
Code connected with the tool list recorded, Question A with the three prompts
and the Query replay, the write cycle with a playlist and tracks of their own
choosing and the dialog recorded, a reflection. Tasks 1 to 3 are to be done
in the first two days; there is no interim submission, and students who are
stuck write to the instructor. Students work in an `exercise-neo4j-mcp/`
folder of their course repository and submit that folder; the graded files
are a sanitized `.mcp.json` and the filled-in `EVIDENCE.md`; 15 points,
completion-based. Question B, the ambiguity question, and a diagnosis are
optional. The
[instructor key](../demos/lecture-mcp-neo4j/instructor-key/README.md) has the
expected rows, the expected check mismatch for N tracks, the dialog wording,
and the grading notes. Set the due date in the module README.

## Instructor notes

- **Cut if running long:** slide 26 (recovery) to its headings, then the
  Query replay in the read block. Never cut the failure beat or the dialog.
- **Risks:** starting a session in auto mode (no dialog); a stale scratch
  directory (memory recall, inferred ids); choosing the dialog's second option
  by reflex; the Database selector left on `neo4j` during the replay; a
  classroom network on a cold `uvx` cache; model variability in the proposed
  statements, which is the review lesson and not a defect.
- **Variants:** with time, the deny-rule run from the pilot can be shown live
  (`.claude/settings.json` with a `deny` entry, then the write prompt); the
  ten-node `demo` database build from the notes' Section 9 is an optional
  closing beat that the pilot did not run.
- **After class:** confirm `database.py check` passes; if a `P09` remains,
  revert it in Query. Record the session's host version and anything that
  differed from the pilot in the pilot report's open items.
