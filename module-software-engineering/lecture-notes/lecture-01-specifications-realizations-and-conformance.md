# Lecture 01 — Specifications, Realizations, and Conformance

> Software-engineering module, meeting 1 of 6. Companion reading for the lecture
> and the note-set demo (`../demos/lecture-01-note-specs-demo/`); self-contained.
> Launches **Exercise 1**.

## Example: A set of agent-maintained notes

This lecture uses a running example to illustrate the concepts of specification, 
realization, and conformance.  The example is a folder of notes, similar to what 
you might write as you are studying about a particular topic.  For instance, 
for each research article you read, you write a markdown file to summarize the key 
points of the article.  Some questions naturally arise:
 - how should you format your notes -- is there any "standard" to follow?
 - are there standard steps that you follow for adding / removing notes?

 To help answer these questions, will write some markdown files that are not notes themselves.
 Instead they are specifications -- (a) a format specification provide rules that the notes adhere to 
 (e.g., what markdown rules should be followed, (b) a concept of operations (ConOps) that 
 describes the purpose of the "system" (the set of notes and rules) as well as the main 
 operations that the user will apply when adding/modifying the note set.
 
This set up will enable us to explore concepts related to specifications (e.g., rules that 
our note set must adhere to), realizations (e.g., the set of notes itself), and conformance checking 
(verification) (e.g., checking that the note set and operations on the note set adhere to the rules).

This example is carefully designed to be a simplified version of the Personal Knowledge Base (PKB) 
project that is assigned after class.

The starter file for the example contains no article notes -- it only contains the specifications 
at present.  Here is an overview..

- `note-set-conops.md`, a concept of operations.  The notes are meant for a single
  user (there is no notion of sharing notes between multiple users).  
  An agent helps a human user maintain the notes in Markdown.  
  An agent performs the structural operations (add a blank note, add a
  note with initial content, remove a note); every note is expected to conform to
  the format specification at all times.
- `note-format-spec.md`, a format specification: six numbered rules that every note
  must satisfy.
- `CLAUDE.md`, eight working rules for the agent: read both specifications before
  any operation, never change a specification without approval, check conformance
  after every operation and report findings before repairing, and so on.

The format specification is the primary example for this lecture. Version 0.1
states, in condensed form:

| Rule | Requirement |
|---|---|
| R1 | A note begins with a YAML front-matter block delimited by `---` lines; the opening `---` is the first line of the file. |
| R2 | The front-matter contains exactly two fields: `title` (a non-empty string) and `created` (an ISO-8601 date, `YYYY-MM-DD`). |
| R3 | The body begins with a level-1 heading, which is the first non-blank line after the front-matter. |
| R4 | A note contains exactly one level-1 heading. |
| R5 | A heading is at most one level deeper than the nearest heading above it. |
| R6 | Every note file is linked from `index.md` exactly once, and every note link in `index.md` resolves to an existing file. |

The rules use the RFC 2119 keywords (MUST, MUST NOT, SHOULD, MAY) and are numbered
so that a conformance report, whether written by a person, an agent, or a program,
can cite them.

The example was chosen for size. Six rules fit on one screen, a conformant note is
a dozen lines, and each concept in this lecture can be pointed at in the repository
rather than described in the abstract. Project 0 (PKB) asks you to build a larger version
of the same thing; You will apply everything that you learn in this lecture to Project 0.

## Four terms

**Specification (S).** A document that states, at a higher level than the artifact
it governs, what the developer intends. It fixes some properties and deliberately
omits others. `note-format-spec.md` fixes the front-matter fields and the heading
structure of a note. It says nothing about the note's subject, length, or prose.
The omissions are deliberate: the specification constrains what matters to the
developer when implementing the "system" and leaves the rest free.

**Realization (R).** An artifact built to satisfy S. When R is code, the usual word
is *implementation*; *realization* is the general term, because a note, a script,
or another document can each be built to satisfy a specification. In the example,
every file in `notes/` is a realization of the format specification. 

**Conformance.** The relationship between S and R that holds when R satisfies every
property stated in S. It is a yes-or-no question about the pair: given this
specification and this note, does the note satisfy R1 through R6? Properties that
S does not state are not part of the question. Two notes with different content,
different lengths, and different headings below the title can both conform to S.

**Verification.** The activity of trying to confirm that R conforms to S. The word
*trying* is deliberate. A verification activity produces a result, and the result
can be wrong: the checker can have a bug, the reader can miss a line, the check can
be run against a stale copy of S. The section on verification returns to these subtleties 
-- the main point here is that we want the verification activity to be "trustworthy", and 
we need to understand when something might possibly go wrong in the verification activity 
itself.

Taken together, the four terms name the two participants (S and R), the
relationship the developer wants between them (conformance), and the act of finding
out whether the relationship holds (verification). Diagram 1 in the slides shows
the arrangement, once in the abstract and once for the demo's files.

Note that one specification can have many realizations.  For example, every conformant 
note is a distinct realization of the same S. 

## When conformance fails: change S or change R

When we first consider the idea of specifications, we are tempted to think that
the specification itself represents the "ideal truth".   The developer wrote
or guided an agent in writing the specification, so we may naively imaging the the
specification always matches what the developer intended and that the developer 
"is always right".   However, we have to accept the idea that a specification itself may
be "wrong" in some way.  For example, maybe the specification is missing a rule, 
or maybe two rules in a specification are in conflict. 

Thus, we have to understand that a conformance check that fails simplify reports a fact 
about the pair (S, R). It does not say which side is "wrong" (it could be that "R is wrong" because
it doesn't follow the rules of S, or it could be that R matches what the developer actually
wants, but the developer has incorrectly written down the rules for S). 
Re-establishing conformance means changing one of them,
and the choice is an engineering decision that should be made by a person and
recorded.

**Repairing R.** In the demo, the instructor overwrites a note with a version
written carelessly in another editor. The check finds four violations: the
`created` field reads `Sept 11, 2026` (R2); the H1 reads `The Waterfall Paper`
while the `title` field reads `Royce 1970 Waterfall Paper` (R3, as amended); a
second H1, `# My take`, appears later in the file (R4); a `####` heading follows a
`##` heading directly (R5). The specification is right and the note is wrong, so
the note is repaired: the date is rewritten, the heading is changed to match the
field, the second H1 becomes `##`, the skipped level becomes `###`. The check is
run again and passes. That passing re-check is what "the operation is complete"
means under the ConOps: the task is not "edit the file" but "make the conformance
check pass."

One detail of the R3 repair carries a decision. The heading and the field
disagreed; either could have been changed. The amended R3 states that the
front-matter `title` is authoritative and that repairs adjust the heading. That
sentence is in the specification so that neither the agent nor a script has to
choose.

**Amending S.** The other move is to change the specification. In the demo this
happens before any note exists. Asked to list every place where the two draft
specifications are ambiguous, incomplete, or inconsistent before proposing a plan,
the agent reports, among other things:

- The format spec says every Markdown file in the note set must satisfy its rules;
  the ConOps says `index.md` is a Markdown file in the repository; `index.md` has no
  front-matter and cannot satisfy R1 or R2. Neither document says whether the index
  is a note.
- R2 requires a `title` field and R3 requires an H1, but no rule says they must
  agree.
- The add-blank-note operation supplies only a title, and no rule says what
  filename the note gets. The operation cannot be executed without inventing a
  convention.

Each of these is a defect in S.  Two common ways of finding problems in specifications are
- building a collection of realistic examples that exercise every rule in the spec, 
- analyzing the specification to look for incompleteness or logical inconsistencies.

The analysis above can either be done by a human "thinking hard and systematically" or by 
an agent, or by some other tool that it suitable for finding problems with certain types of
rules.   In general, this is a *very hard problem* because, in many cases, only the developer's 
brain holds the ultimate answer to the question of "is the specification right"?
Human brains are fallible; humans get tired.  So assessing whether or not the 
specification is right is often a brainstorming activity to get a human to think of a bunch
of scenarios or possible realizations.

In any case, one of the main point that we will learn about agentic software engineering is that we want
the specs to "drive the development" and to accurately summarize the intentions of the developer.
Thus, we will put extra care into recording changes to specifications.

In our demo, the resolutions to specification problems are ultimately decided by the instructor.
But an agent helps by proposing resolutions as a numbered list
of amendments, approved, and applied.  For example, the developer
and agent in our demo will update the intended scope of a specification
(e.g., `index.md` is clarified to not be a note -- therefore note formatting rules don't apply to it;
R6 alone governs it).  R3 is extended with a clarification (the H1 equals the `title`; the field is
authoritative).  A new rule R7 is added as a way of deriving a note file name.
As we work with the agent to make these changes to the specification, we update the spec
version (it goes from 0.1 to 1.0.0).  The agent helps us maintain a changelog to record
the rationale for the changes. 

**Who decides.** In both cases a person decided which side (e.g., either S or R) moves. 
How do we record this "management principle"?  The working rules
in `CLAUDE.md` enforce the division: rule 2 says the agent never edits a
specification without approval and proposes changes as a numbered list; rule 4 says
the agent reports violations and waits before repairing. Lecture 07 of the Project 1
unit states the same principle for code: when code and spec disagree, one of them is
wrong on purpose, a human rules, and the ruling is a commit. This lecture's version
is more general in two ways: R need not be code, and the decision can go either
way.

Version numbers and changelogs are how S records its own changes. A specification
without a version cannot be cited precisely, and a conformance result that does not
say which version it was checked against cannot be interpreted later.

Diagram 2 in the slides shows the loop: verify; if conformance holds, record the
result; if not, decide which side is wrong, repair R or amend S, and verify again.

It will turn out that as our development concepts get more sophisticated, some notion 
of "coordinating agent" or "manager agent" could also decisions about what is right.
But for now, we assume that the human developer is the ultimate authority.

## Verification and its instruments

There are at least three ways to check a note against the format specification.

1. **A person reads both.** The reader opens the specification and the note and
   works through the rules. This can decide every clause, including the ones that
   require judgment. It is slow, and its reliability depends on attention: the
   careless note in the demo was written by the instructor the night before, with
   no process watching.
2. **An agent reads both.** In the demo the agent is asked to check the note and
   report before fixing anything. It reads the specification file (working rule 1
   requires this), reads the note, and reports four findings, each citing a rule ID
   and quoting the rule text. The agent can apply judgment clauses such as
   "preserving the user's meaning." Each check costs tokens, and two runs can
   differ.
3. **A program checks.** `check_notes.py`, written by the agent in the demo, takes
   note paths or `--all`, prints one line per violation citing the rule ID, and
   exits 0 for conformant, 1 for violations, 2 for usage errors. It is
   deterministic, instant, and free to run. It decides only the mechanical rules.

| | Person | Agent | Program |
|---|---|---|---|
| Cost per check | Minutes of attention | Tokens | Milliseconds |
| Same result on repeat | Not guaranteed | Not guaranteed | Yes |
| Mechanical rules (R1–R7, R8's MUST clauses) | Yes | Yes | Yes |
| Judgment clauses (R8's SHOULD; O2's "preserving meaning") | Yes | Yes | No |
| Composable into a gate (hook, CI) | No | With effort | Yes, via the exit code |

Because we have followed best practices when writing the specification and given 
each rule an ID, the different approaches above are more easily compared. 
All three approaches can cite R2, R3, R4, and R5 for the same note. 
Sometimes, not all properties can be mechnically verified.  In such cases, 
the "programmed check" might decide all that it can, and mark some potential
problems for a human or agent to decide.  For example, in our demo the operations 
document in the demo records the split explicitly: a table listing 
which rules the script decides and which clauses remain for the agent or the user.

Lecture 06 of the foundations unit showed all three instruments in use without
naming them: the coverage gate that fails the build is a program, the code-review
subagent is an agent, and the human checkoff between waves is a person.

### How verification itself can be invalid

A verification result is a claim made by a "checker" (human, agent, program), and the "checker" itself can be
wrong. Six ways this happens, each visible in the demo:

- **Wrong version of S.** In the demo's last segment the specification moves to
  2.0.0 (a required `## Summary` section, R8, and an amended R6). Had
  `check_notes.py` stayed at its 1.0.0 form, it would have reported the old notes
  as conformant. A pass against a stale specification is a false result, and
  nothing in the output says so unless the checker states which version it
  implements.
- **The checker can improperly interpret or improperly implement the conformance check.** 
 `check_notes.py` is
  built to embody R1–R8. If it mis-parses a heading inside a code block, it is a
  nonconformant realization of the specification, and its results are wrong in a
  way the results do not reveal. The question "who verifies the verifier" has to be
  answered separately: by reading the script against the rules, by testing it on
  inputs with known violations, or by comparing it with another checker. 
- **Checking from memory instead of from the document.** An agent that has seen the
  specification earlier in a session may judge from its recollection. Working rule 1
  (read the specifications before any operation) exists so that the check is driven
  by the current file.
- **Coverage.** A pass from the script says nothing about clauses the script does
  not decide. R8's SHOULD clause (the summary accurately summarizes the note) and
  O2's "preserving the user's meaning" are outside its scope. A report has to say
  which clauses were checked.
- **Attention.** The person is the checker for judgment clauses, and for
  everything else whenever no process is running. The careless note went into the
  repository because nothing checked it on the way in.
- **A defective S.** Before the amendments, the format spec required every Markdown
  file to satisfy R1 and R2, and the ConOps required an `index.md` with no
  front-matter. No `index.md` could conform. A verification result against an
  inconsistent specification cannot be valid, whichever instrument produces it.
  This is why the demo checks the specifications against each other before
  checking anything against them.

A verification result is therefore evidence with a scope, not a proof. The scope
is: which checker, which version of S, which clauses. A report that states those
three things can be trusted for what it claims and no further.

Lecture 06 also noted that you cannot verify what you do not understand. That limit
applies to the person and the agent equally, and it is a reason to prefer
instruments whose scope is stated.

## Five claims about specifications

Specification-driven development is sometimes described as a one-way process:
write the specification, hand it to an agent, receive the implementation.
This is naive and doesn't work in practice.

Here are some key points that lead us to a more nuanced understanding of the 
role of specifications.  

1. **A specification is a continuously maintained document of intent.** 
   The specification summarizes the intent of the human (and potentially agents, 
   if agent authored -- though almost always when agents author, we would like
   human review of the spec).   But our understanding of what we intend
   can change or be incorrect.  So we must plan to manage the evolution 
   of the specification.  For example, in the demo, the format
   spec moved from 0.1 to 1.0.0 during planning and to 2.0.0 when a requirement
   changed. Each version has a changelog entry, and the operations document keeps a
   "Deferred questions" section for decisions not yet made. The specification is
   under version control like any other artifact.
2. **A specification is an abstraction of the realization.** R1–R8 describe every
   conformant note without describing any particular one. The operations document
   abstracts the agent's behavior in the same way: it says what each operation
   requires and guarantees, not how the agent carries it out.  Thus, the specification
   acts as readable summary that helps us understand the system without looking at 
   all the details of a realization.
3. **Conformance is an invariant maintained while both sides change.** The ConOps
   says it directly: conformance is an invariant of the set, not a milestone. Every
   operation ends with a check. In the demo the specification moved while the notes
   held still (the amendments), and the notes moved while the specification held
   still (the repair). Both ended with conformance re-established.
4. **There will typically be several specifications, and they must be consistent with each
   other.** The repository ends with three: the ConOps (purpose and operations), the
   format spec (what a conformant note is), and the operations document (how the
   agent performs each operation). The `index.md` gap was an inconsistency between
   two of them, and it was fixed in both.
5. **Information flows in both directions.** Planning produced a new rule R7 and an update to R3.
   Writing the checker program tightened the specification's front-matter
   grammar to two scalar fields, so that a short parser could be complete. A new
   requirement changed the specification, the checker, the notes, and the index in
   one coordinated commit. None of this is a failure of the specification; it is
   how a specification is maintained.

Diagram 4 in the slides contrasts the one-way description with the flows the demo
showed.

## A prompt template for specification-driven planning

The centerpiece of the demo is a planning prompt whose first demand is not a plan.
Generalized, it has six parts. The standalone handout
(`../student-materials/spec-driven-planning-prompt-template.md`) has the full text
and a filled example.

1. **Read.** Name the specification files and require that they be read in full.
2. **State the target.** Say what realization you want: which artifacts, which
   operations documented, in which file.
3. **Find gaps in specs before planning an implementation.** 
   Ask the agents to help you find gaps in the specs.  Ask the agent to produce 
   a numbered list of every place the specifications are ambiguous, incomplete, 
   or inconsistent: within one document,
   between documents, and between a document and what executing it would require
   ("walk through the add-blank-note operation step by step; what would you have to
   invent?"). Require that the agent stop and ask you to resolve them.
4. **Amend with approval.** Require the amendments as a numbered list, and approval
   before any specification is edited.
5. **Plan.** Once you have worked with the agent to debug the specification, 
   then ask the agent to make a plan for realizing the spec(s).  Then review and approve the plan.
6. **Realize with a verification gate.** As the realization is implemented
   (or as the system is updated over time),  after each change in the system, check the
   affected artifacts against the specification (or tell the agents they must do this)
   and report the findings, citing rule IDs.  This verification of the system realization 
   update is a "gate" -- only if the verification succeeds should work be continued.

Item 3 is very important to avoid wasting time and tokens.  a few hundred
tokens of questions in exchange for defects found before any artifact exists. In
the demo it found the three seeded gaps and usually finds more.

Some of these demands belong in `CLAUDE.md` rather than in every prompt, because
they apply to every operation: read the specifications first; never modify a
specification without approval; report violations before repairing; quote the
violated rule; end each operation with a named commit. The demo's `CLAUDE.md` is
eight such rules, and it does not change during the demo.

This lecture starts from draft specifications that a person wrote. Later lectures
use the agent to produce the specifications themselves, with the same gap-finding
step applied to its own drafts.

## Exercise 1 and Project 0

Exercise 1 asks you to run the demo's planning and verification segments in your
own session, write one note carelessly, and check it with all three instruments.
The deliverable is a table of findings by instrument, one explained disagreement
or coverage gap, and a half page on which side should have moved and how each
instrument could have been wrong.

It is deliberately small. Project 0, which you are starting now, is the same
structure at larger scale: your PKB specification is these three documents grown
up, its conformance checklist is R1–R8 grown up, and the stretch-goal validator is
`check_notes.py` grown up. The Open Knowledge Format your PKB follows keeps
conformance deliberately light; deciding how much to tighten it, and which
instrument checks it, is the same decision the demo makes about R8.

## Questions to think about

1. Name one property of a note that `note-format-spec.md` 2.0.0 leaves
   unconstrained. Argue whether it should stay unconstrained, and if not, write the
   rule and say which instrument would check it.
2. For the R3 finding on the Royce note (the H1 disagrees with `title`), defend
   moving S instead of R: what would the amendment say, and what would it cost the
   rest of the system?
3. A compiler's type checker is an algorithmic verification instrument. Which of
   the six failure modes above apply to it, and what stands in for "who verifies
   the verifier" in that setting?

## Before next meeting

- Read Royce (1970), "Managing the Development of Large Software Systems," and
  Meyer (1992) on Design by Contract; see `../reading-list.md`.
- Exercise 1 is due before Lecture 03.
- Lecture 02 treats the ConOps and the operations document as two further
  expressions of intent, and begins building specifications with the agent rather
  than from a human draft.
