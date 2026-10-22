# Audit 02: the specifications, by an agent with an ad-hoc prompt (version A1)

| Field | |
|---|---|
| Audit | 02 |
| Date | 2026-10-22 |
| Auditor | an agent (Claude, a fresh session), given the prompt of `reference/prompts/03-audit-adhoc.md`; no skill, no checklist |
| Audited | the working tree before commit a1-specs (`reference/drafts/` overlaid onto `specs/`) |
| Checks applied | the agent named its own: well-formed headers; EARS shape; glossary discipline; internal and cross-document consistency; completeness for the scope; story-to-requirement coverage; execution of every example; resolution of every cited file, rule, and entry. It reported no per-check pass or fail; it reported findings only. |
| Read first | the three files named in the prompt; it also read `reference/elicitation.md` and `process/rules.md` and listed `reports/`, which the prompt did not ask for |

The agent's report is reproduced in the gap table below, condensed to the
form of rule RPT-2 and with its own numbering (1 to 20) kept; the full text
is in the dev-log entry's session record. Severities are the agent's. The
*Key* column maps a finding to the A1 plan's seeded gaps (G1 to G7) or marks
it as not seeded. Rulings follow the A1 plan's section 6 where a gap was
seeded and the build's judgment otherwise, on the instructor's behalf.

## Gaps

| Gap | Location | Check | Quoted | Proposed resolution | Key | Ruling | Amendment |
|---|---|---|---|---|---|---|---|
| 1 (Major) | ConOps preamble, §6; requirements preamble | cross-document: a cited file does not exist | "recorded separately in `reports/validation.md`" | cite `reports/walkthrough.md` (the file that exists), or create the file and amend VAL-1 | not seeded: an inconsistency of this working tree | **accepted** for this commit: the validation record and rule VAL-2 arrive with the validation task of this version; until then the documents cite the file and the rule that exist | preamble and §6 cite `reports/walkthrough.md`; `requirements.md` preamble likewise |
| 2 (Moderate) | ConOps §4 intro | a cited rule does not exist | "(rules VAL-2 and VAL-1)" | cite CONF-2 and VAL-1, or add VAL-2 first | not seeded, as above | **accepted**: cite VAL-1 only in this commit; VAL-2 is added with the validation record | §4 intro |
| 3 (Major) | US-2 example | by execution: the example contradicts the story and the glossary | "(Restricted, 7); it outputs (Public, 7)" | "(Restricted, 7); it outputs (Restricted, 7)" | **G4** | **accepted** | US-2 example |
| 4 (Major) | US-3 | glossary discipline; the story is not in the stakeholder's words; contradicts US-2 under the glossary's ordering | "every sensitive message stopped" | "every message whose security level is Critical dropped at the guard" | **G1** | **accepted** | US-3 |
| 5 (Moderate) | A-3 | an assumption that is a property of the guard, not of the deployment | "keeps nothing between messages" | move to §2 as a boundary statement | not seeded; a genuine finding | **accepted**: A-3 removed; §2 says each call is independent and the guard keeps no state between messages; the elicitation record's note on A-3 amended | §2; `reference/elicitation.md` |
| 6 (Moderate) | D-3 | contradicts the permanent Critical rule of §1 and E-1 | "A change to which security levels are stopped" | restrict to Restricted and Public | not seeded; a genuine finding | **accepted** | D-3 |
| 7 (Minor) | story headers | `Method` and `Validated by` carry the same value | "Method: walkthrough (human) ... Validated by: walkthrough (human)" | drop the field or say what distinguishes them | not seeded | **rejected**: the two fields answer different questions (how the story's behavior is verified; how its rightness is decided), and the next commit changes the first to *test* while the second stays. The §4 intro already says so | none |
| 8 (Moderate) | §2 | completeness: an input that is not a message is unspecified | "Input: one message." | say in §2 that such an input is outside the boundary | not seeded | **accepted** (one sentence) | §2 |
| 9 (Minor) | purpose | implementation-dependence; "function" against "library" | "a Python function" | use the glossary wording, drop "Python" | **G7** | **accepted** | §1 |
| 10 (Minor) | §2 output line; glossary *guard*, *output* | "the same message" may mean the identical object | "Output: the same message, or nothing." | phrase as "a message unchanged" | not seeded; **the over-report**: value equality is what *unchanged* defines, and object identity is an implementation choice the specification leaves open (Lecture 01, question 1) | **rejected** with that reason | none |
| 11 (Minor) | several | synonyms for glossary terms: stopped, marking, content, allowed to leave | "stopped", "marking", "content" | use the glossary term in clauses; add synonyms to entries | not seeded | **ruled**: "stopped" replaced by "dropped" in clauses and *drop* gains "(a stakeholder may say *stopped*)"; "content" replaced by "payload" in §3; "marking" is the glossary's own word inside the *security level* entry and stays; "allowed to leave" and "arrive unchanged" are the sender's words in a story, whose header says how it is verified | US-3, D-3, §3, glossary *drop* |
| 12 (Minor; Moderate for "record" and "nothing") | several | terms used and not defined | "record", "nothing", "boundary", "transport", "policy" | add entries | not seeded | **ruled**: "record" leaves the requirements with gap 16 and stays plain English in D-1; *output* gains "nothing means no message; how a realization represents it is left open"; the rest are ordinary words, not domain terms | glossary *output* |
| 13 (Minor) | §5 | a "scenario" artifact this version does not have yet | "No requirement, story, or scenario of this version" | drop "scenario" | not seeded: an inconsistency of this working tree | **accepted** for this commit; the word returns with the scenario file | §5 |
| 14 (Minor) | glossary | the bold convention not followed in three definitions | "whose systems produce messages" | bold them | not seeded | **accepted** | glossary *enclave*, *message sender*, *unchanged* |
| 15 (Moderate) | REQ-0 | two "shall" sentences; restates the glossary; the guard as subject of a message property | "The guard shall take as its input ... The guard shall not change a message" | one clause that cites the glossary; a separate identifier for immutability | not seeded | **ruled otherwise**: one sentence, the guard as subject, the form restated because a requirement is read alone and `test_message.py` checks exactly these properties; no new identifier | REQ-0 |
| 16 (Major) | REQ-1 | contradicts §2, §5 (D-1), the glossary, US-3's examples, and E-2 | "and shall record the drop" | delete the clause | **G2** | **accepted** | REQ-1 |
| 17 (Major) | REQ-2 | not in EARS form; no "unchanged" | "Restricted messages are allowed through." | "When the filter is given a message whose security level is Restricted, the filter shall pass the message unchanged." | **G3** | **accepted** | REQ-2 |
| 18 (Major) | REQ-4 | malformed header; derivation from a story about something else; a trigger outside the input domain | "**REQ-4** · Derived from: US-3" / "when it receives no message" | delete | **G6** (both findings) | **accepted**; noted for the HAMR mapping | REQ-4 deleted |
| 19 (Major) | REQ-5 | assumption A-2 promoted to a tested requirement; derivation is a section, not a story | "The guard shall receive every message that leaves the enclave." | delete; A-2 stays an assumption | **G5** | **accepted** | REQ-5 deleted |
| 20 (Minor) | REQ-1, REQ-3, REQ-4 | trigger verb and subject vary | "is given" / "receives" | one trigger verb; a stated subject convention | not seeded | **accepted**: "is given" throughout; the preamble states the convention | requirements preamble |

Searched (the agent's words): within each document ✔ · between documents ✔
· by execution ✔ (it executed every example against the clauses and listed
the results).

## What this audit shows, beside its findings

- It found all seven seeded gaps (G1 to G7: items 4, 16, 17, 3, 19, 18, 9).
- It reported one non-gap, item 10, the object-identity reading of "the
  same message": the over-report the plan expected, in the scope section
  rather than on REQ-2.
- It found three real inconsistencies the plan did not seed (items 1, 2,
  13), all forward references to artifacts of later commits, and two
  improvements (items 5, 6) that the rulings accepted. An agent audit at
  rung 2 can be better than its prompt.
- It did not find two things the skill's checklist did (audit 03): the
  three story headers carry a judgment method and no `Reason`, and US-2's
  `Source` names an entry answered by the other user category.
- It read two files the prompt did not name, and it invented its own
  severity scale and check list, so a second run would report differently;
  that is what the skill of audit 03 fixes.
