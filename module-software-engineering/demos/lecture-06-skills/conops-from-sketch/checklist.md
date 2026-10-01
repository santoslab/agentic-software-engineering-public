# Fallback audit checklist

Use only when the repository has no audit of its own. Cite these as C-1…C-12.

- **C-1 Unambiguous.** Two careful readers cannot disagree whether a behavior
  satisfies a clause. Any clause constraining form has an exact example.
- **C-2 Internally consistent.** Clauses touching the same property agree and
  state their relationship.
- **C-3 Externally consistent.** Terms and facts match the project's other
  documents.
- **C-4 Complete for its level.** Every operation can be walked through step by
  step without inventing a convention.
- **C-5 Implementation-independent.** Nothing only a builder would encounter.
- **C-6 Observable.** Each policy names a moment a user would see it kept or
  broken.
- **C-7 Coverage.** Each operation has input, precondition, postcondition; each
  mode, policy, and user class appears in a scenario.
- **C-8 Terms.** Repeated terms are defined and used with one meaning.
- **C-9 Voice.** Third person, present tense, self-contained.
- **C-10 Versioned.** Version, status, changelog with rationale.
- **C-11 Skeleton.** Full skeleton (1 Scope; 2 Current Situation; 3 Justification
  and Nature of Changes; 4 Concept — objectives, policies, modes, user classes,
  environment; 5 Scenarios; 6 Impacts; 7 Analysis; 8 Future; 9 Glossary); 2, 3, 6
  only when a baseline exists; no TBD in kept sections.
- **C-12 Facts in their section.** Policies in §4.2, environment in §4.5 — not
  only in Limitations or Future.

Search three places: within the document, between documents, and a
walkthrough of executing each operation. Report as a numbered gap list and stop
for rulings.
