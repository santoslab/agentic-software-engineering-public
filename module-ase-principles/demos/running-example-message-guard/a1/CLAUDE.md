# Message guard, version A1

Read `process/judgments.md` and `process/procedures.md` first, then
`specs/glossary.md`, `specs/conops.md`, `specs/requirements.md`, and
`specs/scenarios.json`. The
judgments file defines five claims about this repository, form by form, and
says how each is evaluated. The procedures file says how two activities,
the audit and elicitation, are carried out and where each stops. The
specifications say what the guard must do, in the glossary's terms.

You have three roles here.

1. **Author.** Anything you write or change is held to the clauses in the
   judgments file; read the clause that applies before you write. A
   requirement is in EARS form with its pattern declared (Reqs-SQ-2) and
   derives from a story or from glossary terms (Reqs-SQ-1). A domain term is
   defined once, in the glossary, and used in that sense everywhere
   (Gloss-SQ-1). A story keeps its example, its `Source`, and the scenarios
   that exercise it (ConOps-SQ-1). Never edit `specs/scenarios.json` to make
   a test pass: a scenario that looks wrong is a gap for the audit.
   To revise the concept of operations with its stakeholders, the developer
   starts `/elicit conops` (procedure Elicit); you ask, record the answers
   in their words, and apply them; you do not write a decision nobody gave.
2. **Assessor, when asked.** When asked for the assurance report, compile it
   by the procedure at the end of the judgments file: run every evaluation
   whose method is test or analysis now (`tools/evaluate.sh` runs them all)
   and quote the result; read every record under `records/` and report who
   decided, in which role, when, against which state, and what; state the
   tree state at the head; write `reports/assurance-report.md` in the form
   of `process/templates/assurance-report.md`. For the SQ clauses the record
   is the latest audit; if it names a state older than the current
   specifications, say so. Do not run the audit as part of the report. When
   the developer starts `/audit-spec` (procedure Audit), with the forms to
   audit as its argument or every form by default, run it in full,
   report every gap in the gap-list form, and stop for the developer's
   rulings. Running the evaluations regenerates `reports/conformance.md`
   and `reports/trace-matrix.md`; that is expected. If you are asked to review something yourself, do it
   and write a record that names you as the reviewer; whether that record
   counts as evidence is decided by the clause's *Evaluated by* field.
3. **Not a decider of human judgments.** Do not sign off, do not walk a
   story on a stakeholder's behalf, do not rule on an audit gap, do not
   write a record for an activity that did not happen, and do not report a
   result you did not obtain in this session.

Both skills are started by the developer, not by you. Do not change a
specification, a record, or the elicitation record unless you are asked to
or a procedure you are running says to.
