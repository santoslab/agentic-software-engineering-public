# `/elicit`: the elicitation skill

## Goal

Obtain, from the stakeholders of a concept of operations, the answers that
the document does not yet settle, in at most five questions, and record their
words so that every sentence of the document can be followed back to who said
it. It packages procedure `Elicit` of `process/procedures.md`, which from
version 1.1 takes the form to elicit as its argument. It is a procedure skill,
not a verifier: it produces a
specification and reference material, and the verifier that reads its
product is `/audit-spec`.

## Requirements

1. Reads the document named by its form argument (`conops` by default),
   the glossary and the elicitation record if they exist, and
   `process/procedures.md`; asks nothing the repository already answers.
2. Scans the document against the form's fixed taxonomy (`forms/conops.md`:
   eight concept-of-operations categories) and rates each Clear, Partial, or
   Missing; a form with no taxonomy stops the skill.
3. Builds a queue of at most five questions ranked by impact times
   uncertainty; each answerable with a letter or at most five words;
   implementation, technology, and task order excluded.
4. Asks one question at a time, addressed to a named user category, in the
   fixed format (`question-format.md`): a full interrogative, one "why it
   matters" sentence, the recommended option first with its reason, an
   options table, the reply line.
5. After each accepted answer, immediately appends an entry to
   `reference/elicitation.md` with the answer verbatim and who gave it
   (`record-template.md`), and applies the answer to the part of the
   document it affects, replacing contradicted text.
6. Never touches the requirements, the scenarios, the tests, or the code.
7. Ends with a completion report: questions asked, sections touched, a
   coverage summary, and the next steps (`/audit-spec`, then the validation
   walkthrough and sign-off).
8. Only the developer can start it (`disable-model-invocation: true`); the
   same switch for Codex is in `agents/openai.yaml`.

## The prompt

The skill was written by the build agent from the A1 plan's section 8a,
which specified requirements 1 to 8 and the adaptation from Spec Kit's
`speckit-clarify` skill (the model for the whole procedure). What the plan
told the agent, condensed to its operative sentences:

> Base the skill on `speckit-clarify`'s steps 3 to 7: a taxonomy scan rated
> Clear, Partial, or Missing; a queue of at most five questions by impact
> times uncertainty; one full-interrogative question at a time, with a "why
> it matters" sentence, the recommended option first, and an options table;
> after each accepted answer, record it and apply it to the section it
> affects, replacing contradicted text; validate after each write; finish
> with a completion report. Change three things: the taxonomy is shaped by
> the parts of a concept of operations (purpose, scope and boundary,
> assumptions, user categories, stories, terms, wants and non-goals,
> validation), each question is addressed to a named user category, and the
> record goes to `reference/elicitation.md` with the stakeholders' verbatim
> words, not into the specification. Leave out clarify's extension hooks and
> its checklist re-validation; `/audit-spec` is the next step instead. Write
> it in the house style of the course's `conops-from-sketch` skill: a short
> body with reasons, bundled detail, a narrow description, and the stops
> named.

## Review points

Before trusting a run: the questions name a user category, not "the user";
every question is an interrogative, not a topic label; the recommended option
comes first and has a reason; nothing in the queue is answered by a file in
the repository; the record entry quotes the answer rather than paraphrasing
it; the document changed only where the consequences line says; the
requirements, scenarios, tests, and code are untouched; the completion
report's coverage table accounts for every taxonomy category.

## Deliberate-failure checks

A procedure skill has no exit code, so its check is an evaluation in the
manner of the course's skills lecture: run it several times on the same
document and compare the queues. The check is that the queue stays on the
high-impact areas and that no run takes a decision nobody gave.

**Evaluation on the A0 concept of operations, 2026-10-22, three runs**
(fresh agents, read-only, asked to print the whole queue instead of asking
one question at a time; the runs could not reach step 5, so "a decision taken
without asking" was checked on the queues and the exclusion lists only).

| | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Questions queued | 5 | 5 | 5 |
| Coverage ratings | Assumptions, User categories, Wants: Partial; the other five Clear | the same | the same, and Terms: Partial ("enclave", "policy" undefined; "arrive" against "pass") |
| Addressee named on every question | yes | yes | yes |
| Recommended option first, with a reason | yes | yes | yes |
| Trust in the marking as an assumption (A-1) | asked (Q2) | asked (Q2) | asked (Q1) |
| What a sender observes on a drop (E-3) | asked (Q3) | asked (Q5) | asked (Q3) |
| The later-version promises as deferred wants (D-1 to D-3) | asked (Q5, "any other wants") | asked (Q4, "which are yours") | asked (Q4) |
| Who is, and is not, a user (E-4) | asked (Q1, the outside receiver) | asked (Q3, receiver or installer) | asked (Q2, the receiver; Q5, who marks) |
| Fifth question, which varied | the transport's obligation for "arrives unchanged" | whether "Critical never leaves" is permanent or a changeable policy | who assigns the marking, the sender or a separate step |
| The payload's domain (CF-13) | excluded: REQ-0 says integer; the rest is implementation | excluded, same reason | excluded, same reason |
| Candidates excluded, with reasons | 14 | 12 | 18 |
| A decision written without asking | none seen | none seen | none seen |
| Format deviations | a one-line rank note before each question, not in the format | none | none |

What the evaluation shows. The four high-impact areas (the marking
assumption, the drop, the wants, the user categories) are asked in every run;
the fifth slot varies, which is the ranking heuristic doing its job on
near-ties. No run asks a terms question even when it rates Terms as Partial:
all three treat a missing definition as the writer's job rather than a
stakeholder's, which is defensible for "enclave" and would be wrong for an
adjective such as "large" that only a stakeholder can quantify. Every run
excludes the payload-domain question as answered by REQ-0, so the
language-level question of CF-13 stays open and is recorded as such in the
glossary rather than decided by a stakeholder who could not answer it. The
live session (`reference/elicitation.md`) used run 2's queue.

A proposed change for version 1.1, not applied: add to the Terms row of the
taxonomy that an unquantified adjective in a story is the stakeholder's to
quantify, so that a run on a document containing one queues the question.

## Adapting it to your project

Project-specific: the default path of the concept of operations; the names
of the user categories (the skill reads them from the document); the rule
procedure it cites (Elicit). Carries over as an idea: the cap, the ranking,
the one-at-a-time protocol with a recommended default, the verbatim record
under identifiers that the specification cites, and the rule that facts are
looked up and decisions are asked. For a document that is not a concept of
operations (a requirements document, a data format), add a taxonomy under
`forms/` and name the form in the skill's table; the body does not change.
Version 1.1 (2026-10-24) made that arrangement: `taxonomy.md` became
`forms/conops.md` and the form became the first argument. The taxonomy's
content did not change, so the evaluation above stands for it; a changed
taxonomy would be re-evaluated the same way.

## Making it shared infrastructure

The skill folder is self-contained and harness-portable (`SKILL.md` for
Claude Code; `agents/openai.yaml` for Codex). An organization that keeps its
concept-of-operations skeleton fixed can ship this skill with the skeleton as
one package: the taxonomy is the skeleton's section list stated as questions.
Version the skill (the record's header names the version that asked), keep
the evaluation runs beside it, and rerun them when the taxonomy or the format
changes; a change that drops a high-impact area from the queue is a
regression every project using the skill would inherit.
