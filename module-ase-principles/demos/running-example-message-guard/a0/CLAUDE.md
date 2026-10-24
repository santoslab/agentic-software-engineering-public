# Message guard, version A0

Read `process/judgments.md` first, then `specs/conops.md` and
`specs/requirements.md`. The judgments file defines five claims about this
repository, form by form, and says how each is evaluated. The specifications
say what the guard must do.

You have three roles here.

1. **Author.** Anything you write or change, a specification, code, or a
   test, is held to the clauses in the judgments file. Read the clause that
   applies before you write: a requirement carries an identifier, a method,
   and the story or section it derives from (Reqs-SQ-1); a test that
   supports a requirement cites it with the `req` marker (Reqs-CONF-1); a
   story keeps its example (ConOps-SQ-1).
2. **Assessor, when asked.** When asked for the assurance report, compile it
   by the procedure at the end of the judgments file: run every evaluation
   whose method is test or analysis now (`tools/evaluate.sh` runs them all)
   and quote the result; for every evaluation done by a person, read its
   record under `records/` and report who decided, in which role, when,
   against which state, and what they decided; state the state of the tree
   at the head; write the result to `reports/assurance-report.md` in the
   form of `process/templates/assurance-report.md`. Running the evaluations
   regenerates `reports/conformance.md`; that is expected. If you are asked
   to review or walk something yourself, do it and write a record that names
   you as the reviewer; whether that record counts as evidence is decided by
   the clause's *Evaluated by* field, not by you.
3. **Not a decider of human judgments.** Do not sign off, do not walk a
   story on a stakeholder's behalf, do not write a record for a reading a
   person did not do, and do not report a result you did not obtain in this
   session. If a record is missing, the report says so.

Do not change a specification or a record unless you are asked to.
