### Specification and Realization

Development MUST recognize the distinction between specifications and
realizations (implementations).  Specifications express developer
intent and indicate constraints on development.  The development 
process should emphasis providing evidence that realizations conform
to the specifications, e.g., via testing or manual reviews.

### Specification before realization

A realization changes for one of three reasons, and the history MUST show which.

(a) **Repair.** The realization did not conform and is changed so that it does.

(b) **Conformance-preserving change.** The realization conformed before and
conforms after; what changed lies in what the specification deliberately leaves
open — the algorithm, its efficiency, the structure or naming of the code. No
specification change is needed. The change MUST be verified, and its
commit message MUST state that no specified behavior changed.

(c) **Change of specified behavior.**  A specification has been
updated, and the realization would no longer conform to
the current specification unless changes are made to the realization.

### In a verification failure, a person decides whether the specification or realization gets changed

When a specification and a realization disagree, the finding is a fact about the
pair; which side changes is the developer's decision. The decision and its reason
MUST be recorded — in the changelog when the specification moves, in the commit
message when the realization moves.

### Derived documents follow governing ones

A document derived from a governing specification MUST NOT contradict it. When
it is wrong or incomplete, the agent proposes a correction to it rather than
improvising; when it and the governing document disagree, the governing document
wins and the derived document is corrected. 

### Reports

Development should produce reports that
  - help explain specifications with examples
  - help the developer easily ascertain the current state of the
    desired conformance relationship between realizations and
    specifications
    
    