# Audit 01: the specifications, by a person (version A1)

| Field | |
|---|---|
| Audit | 01 |
| Date | reserved for the live session of the third lecture |
| Auditor | a person: the instructor, or the room, reading once without the checklist, in five minutes |
| Audited | the working tree before commit a1-specs: `reference/drafts/conops.md`, `glossary.md`, `requirements.md` overlaid onto `specs/` |
| Checks applied | none by name: a one-pass reading against the five quality properties of Lecture 01 |
| Read first | the three files, once |

**Status of this file.** The human audit is performed live; this file is
the rehearsal prediction from the A1 plan, kept so that the live result can
be compared with it, and it is **not evidence for SQ**. The assurance report
at a1-specs cites audits 02 and 03 and the rulings for the SQ clauses, not this file. When the
live audit has been run, its gap list replaces the table below and the
status line is removed.

## Expected pattern (from the A1 plan, section 6)

A reader working once through the three files tends to find the gaps that
sit inside one sentence and to miss the ones that sit between two documents.
The key uses the plan's numbering G1 to G7; audits 02 and 03 number their
own findings and map them to this key in their rulings column.

| Key | Location | Seeded text | A one-pass reader typically | Why |
|---|---|---|---|---|
| G1 | US-3 | "every sensitive message stopped" | finds | an undefined word in a story the reader is reading closely |
| G2 | REQ-1 against scope and D-1 | "and shall record the drop" | misses | contradiction with another document; needs the scope section and the deferred wants held in mind while reading REQ-1 (threat T1, capacity) |
| G3 | REQ-2 | "Restricted messages are allowed through." | finds | the only requirement that does not look like the others |
| G4 | US-2 example | "(Restricted, 7); it outputs (Public, 7)" | may miss | an example is read as illustration, not checked by execution |
| G5 | REQ-5 | "The guard shall receive every message that leaves the enclave." | misses | reads as reasonable; recognizing it as an assumption needs the scope section's list of what is outside the boundary |
| G6 | REQ-4 | header without `Method`; "no output when it receives no message" | finds the missing field; may accept the content | the missing field is visible; the content's problem (not an input of a one-message function; implied by REQ-1 to REQ-3) needs the boundary |
| G7 | Purpose | "a Python function" | finds | Lecture 01 made implementation-independence of the purpose statement explicit |

Expected count for a five-minute human read: four or five of seven; the
misses are the between-document gaps, which is the lecture's point about a
reader's capacity and the reason the agent's audit comes next.

Searched: within each document ✔ · between documents (partly) · by execution
(not usually, in five minutes).

**Rulings:** none; this file records no findings of its own.
