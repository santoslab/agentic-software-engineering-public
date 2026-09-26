# Kinds of Specification — A Catalog for the Course

> A standing reference for the whole course. It is cited by the
> software-engineering module (Lectures 01 to 06), by the Project 0 brief, and
> by the Project 1 brief. It is an informal summary: every audit rule and
> verification rule it names is defined in the module's process documents
> (`module-software-engineering/demos/lecture-03-game-demo/reference/process/`,
> the same set the Project 1 starter ships), and those documents are normative
> where this catalog is not.

## Purpose

A system is not governed by one specification. It is governed by a *family of
specifications* of several kinds. Each kind fixes something the others leave
open, each is audited by checks of its own, and each is verified against its
realization by its own means. Lecture 03 shows eight kinds at once, on a game;
Lecture 04 adds the test suite and the fixtures; Lecture 06 adds the tool
contract. This catalog lists every kind the course uses, so that you can name
the kinds your own system needs, say what each one is for, and know how it will
be audited and verified before you write it.

Choosing the kinds is itself a decision. In practice it is the developer's or
the organization's — many companies fix a standard collection of specification
kinds, with a format for each, that every project must produce. Where nobody
has chosen, whoever writes the first document decides by default, and with an
agent that is the agent. The module's demo and the Project 1 brief pre-pick the
kinds to keep the work simple and deterministic; this catalog is the menu they
were picked from.

**Important**: the kinds in this catalog are general. The game in Lecture 03
has *rules of play*; a bank has *transaction rules*; a thermostat has *control
rules*. All three are the same kind — behavioral requirements — with a
different name in each domain. When you read a lecture's table of kinds, ask
which names are the domain's and which are the catalog's.

## How to read this catalog

1. The **summary table** gives every kind in one page: what it is for, how it
   is audited, how it is used in verification, whether it survives a port to
   another programming language, and where the course shows it.
2. The **entries**, grouped from intent to environment, give each kind in a
   fixed form (the template is under the table).
3. **Notes on naming** say which items in the lectures are kinds, which are
   *sections of* a kind, and which are *subjects* that span several kinds.
4. **Mapping to the S/R essay** relates the catalog to the essay
   `software-engineering/specification-implementation.md`, which introduced
   the specification/realization idea with seven classical examples.

Entries are cited by name — "the catalog's *fixtures* entry" — never by number.
The numbers in the summary table give reading order only; nothing in the course
cites them.

## Relation to Lecture 01

Lecture 01 defined four terms. A **specification** (S) states, at a higher level
than the artifact it governs, what the developer intends; it fixes some
properties and deliberately omits others. A **realization** (R) is an artifact
built to satisfy S. **Conformance** holds when R satisfies every property S
states. **Verification** is the activity of trying to confirm conformance, by a
human, an agent, or an algorithmic **verifier**.

Every entry in this catalog is a kind of S. Each entry's *Used in verification*
facet names the R, the kinds of verifier that check it, and what a pass
establishes and does not establish — which is the conformance question and how
far a verification result can be trusted. Two artifacts appear in two roles,
and it helps to see this once: the **test suite** is a realization of the
verification obligations *and* the algorithmic verifier of the code; the
**fixture file** is a specification of behavior *and* a stored artifact with a
format of its own.

Lecture 01 also gave five quality properties of a specification — unambiguous,
internally consistent, externally consistent, complete for its level,
traceable — and the module's process documents state them as the generic audit
rules AUD-1 to AUD-5, with AUD-6 and AUD-7 governing how an audit is run. Those
apply to every kind. The per-kind rules (AUD-8 to AUD-14 for seven kinds of the
technical specification, AUDCON-1 to AUDCON-8 for the concept of operations)
add checks that only that kind needs. So the *Audited by* facet of every entry
reads "AUD-1 to AUD-7, and …".

**Important**: this catalog defines no rules. Where an entry and a process
document seem to disagree, the process document is right and the catalog is
corrected.

Terminology used throughout: a specification is *audited* (AUD, AUDCON); a
realization is *verified* (VER); a *verifier* is human, agent, or algorithmic;
"the specifications" or "the technical specifications" means the document
`SPECS.md` of the game examples, whose sections are one kind each; and we say
*family of specifications* for the set that governs one system.

## Summary table

Codes in the last column: L01–L06 the module's lectures; P0 Project 0; P1 the
Project 1 brief; PU the project unit (Stages B to E); E the essay only.

| # | Kind (module instance) | Purpose | Audited by | Verified by | Survives a port? | Shown in |
|---|---|---|---|---|---|---|
| 1 | Concept of operations | what the system is for; what a user observes | AUD-1–7; AUDCON-1–8 | a person, scenario by scenario — validation | yes | L02, L03, L05, P0, P1 |
| 2 | Behavioral requirements (rules of play) | states, transitions, terminal conditions, precedence, initial state | AUD-1–7; AUD-8 | unit tests; fixtures | yes | L03, L04, L05, P1, PU |
| 3 | Display format | exactly what is rendered | AUD-1–7; AUD-9 | golden-string tests | yes | L03, L05, P1 |
| 4 | Input grammar | every accepted and rejected form; the effect of a rejection | AUD-1–7; AUD-10 | rejection tests | yes | L03, L05, P1 |
| 5 | Interaction flow | menus, loops, exits, the state after each | AUD-1–7; AUD-11 | scripted-input tests | mostly | L03, L05, P1 |
| 6 | Data format (note format; fixture shape) | the exact form of a stored or exchanged artifact | AUD-1–7 | a verifier program; a parser or schema validator | yes | L01, L02, P0, P1, PU |
| 7 | Interface contract (operations document) | per operation: parameters, precondition, postcondition, behavior outside it | AUD-1–7; AUD-12 | unit tests; a type checker where used | re-expressed | L02, L03, L05, P1, PU |
| 8 | Tool contract | an interface contract read by a machine | AUD-1–7; AUD-12 applied | schema validation; a call transcript, read | yes | L06, PU |
| 9 | Example session | one whole transcript | AUD-1–7; AUD-13 | an end-to-end scripted run | yes | L03, L05, P1 |
| 10 | Verification obligations | what the tests must claim, traced to clauses | AUD-1–7; AUD-14 | the suite read against them (VER-8) | yes | L03, L04, L05, P1 |
| 11 | Test suite | the obligations as executable claims | VER-6; read against the obligations | it is the verifier; a broken realization must fail it | no — re-expressed | L04, P1, PU |
| 12 | Fixtures | scenarios with outcomes every implementation must reproduce | VER-7 | the loader, on every implementation | yes | L04, L05, P1, PU |
| 13 | Architecture (module split) | parts, boundaries, allowed dependencies | AUD-1–7 | reading; a dependency check where one is written | mostly | L03, P1, E |
| 14 | Technology and platform | named languages, versions, libraries, tools | AUD-1–7 | dependency and build files; provenance by judgment | no | P1, PU, E |
| 15 | Development process | steps, gates, hand-offs, reporting forms | its own mechanism (DEV-3, RPT-3); AUD-1–7 | the repository's history; the gate (VER-4); hooks | yes | L01–L06, PU |

### The entry template

Every entry below has the same eight facets:

- **Fixes / leaves open** — what this kind decides and what it deliberately
  does not: its purpose as an abstraction.
- **Typical forms** — how the kind is usually written.
- **Place in the specification family** — what it is derived from and what it must agree
  with (our audit rule AUD-3, external consistency, checks the agreement).
- **Audited by** — the generic rules, and the kind's own rule where the course
  has one.
- **Used in verification** — which verifier checks the realization, whether the
  clauses are mechanical or judgment (our verification rule VER-2 makes that
  classification), and what a pass establishes and does not establish.
- **Examples** — instances in the course, then one from outside it.
- **Survives a port?** — whether the document is unchanged when the realization
  moves to another programming language.
- **In the course** — where it appears, and whether it is *demonstrated*,
  *named only*, or *not demonstrated*.

## A. Purpose

### Concept of operations

**Fixes / leaves open.** What the system is for, who uses it, which operations
they perform, what they can observe, and the scenarios of use. It leaves open
everything a user cannot observe: how the system is built, how state is
stored, what a function returns. It is the one specification that answers a
*validation* question — is this the system that was wanted? — rather than a
verification question.

**Typical forms.** Prose in a skeleton. The course uses a light skeleton for
the note set (purpose, the system, roles, operations, conformance, change
management) and the full nine-section skeleton for the games (scope; current
situation; justification for and nature of the changes; the concept for the
proposed system with its objectives, policies, modes, user classes, and
environment; scenarios; summary of impacts; analysis; future capabilities;
glossary). Operations are written with a precondition and a postcondition
stated from the user's side; scenarios are written in the user's words.

**Place in the specification family.** The governing document. Every other kind is derived
from it or must agree with it; the technical specifications never contradict
it (our development rule DEV-5). A fact stated here and stated differently in
the rules of play is an AUD-3 finding.

**Audited by.** AUD-1 to AUD-7, and the concept-of-operations rules AUDCON-1
to AUDCON-8: implementation-independent, observable policies, operations and
scenarios that cover every mode and policy, defined terms, third-person voice
and self-containment, versioned, the skeleton's optional sections present only
when there is a baseline, and each fact in the section whose purpose it serves.

**Used in verification.** Verifier: a person, by reading the scenarios and
playing or walking through each one; an agent can do the walkthrough and
report. Clauses: judgment. A pass establishes that the realized system is the
one the document describes; it does not establish that any clause of the
technical specifications holds — that is the other kinds' job.

**Examples.** Course: `module-software-engineering/demos/lecture-01-note-specs-demo/starter-l02/note-set-conops.md`
(the light skeleton);
`module-software-engineering/demos/lecture-03-game-demo/reference/CONOPS.md`
(the full skeleton); the Reversi sketch students receive,
`module-software-engineering/student-materials/reversi-starter/CONOPS-sketch.md`;
the concept of operations you write for your knowledge base in Project 0.
General: the concept of operations for a hospital's bed-management system —
who books a bed, what the ward clerk sees, what happens when no bed is free —
written so that a nurse can read it and say whether it is the system they
need.

**Survives a port?** Yes, unchanged: it names no language or implementation.

**In the course.** Lecture 02 ("The concept of operations: a specification of
purpose"); Lecture 03 ("A concept of operations for a program"); Lecture 05
("Learning Reversi from its concept of operations sketch"); demonstrated.

## B. Behavior

### Behavioral requirements (in the module: rules of play)

**Fixes / leaves open.** The states the system can be in, the transitions
between them, the terminal conditions and the precedence among them when one
event could satisfy two, what happens on an accepted and on a rejected
operation, and the initial state. It leaves open how any of it is implemented.
In classical software engineering "the requirements" is one document that
bundles several catalog kinds; the course separates them, so that what a user
observes lives in the concept of operations and what a verifier decides lives
here.

**Typical forms.** Numbered clauses with RFC 2119 keywords, one identifier per
clause, so that tests, fixtures, and amendments can cite them.

**Place in the specification family.** Derived from the concept of operations' policies;
must agree with it, with the example session, and with the verification
obligations. The chain in Lecture 03 — the concept of operations says "five or
more", the rule says overlines count, the obligations require an overline
case, a test cites the rule, a fixture is named for it — is one intent stated
five times.

**Audited by.** AUD-1 to AUD-7, and AUD-8: our audit rule AUD-8 requires that
the rules state every terminal condition and the precedence between them when
one move could satisfy two, what happens to the turn on an accepted and on a
rejected move, and the initial state.

**Used in verification.** Verifier: algorithmic — unit tests on the engine and
the fixture loader. Clauses: mechanical. A pass establishes that the engine
does what the tests and fixtures claim about the rules; it does not establish
that every clause is claimed by some test (that is clause coverage, VER-8).

**Examples.** Course: `SPECS.md` §3 and §4 of the game
(`module-software-engineering/demos/lecture-03-game-demo/reference/SPECS.md`:
the board and its coordinates, the winning line, the tie, their precedence);
the brief's "Rules of play" decisions for Reversi (`project-1-reversi-brief.md`
§4); the six-item "port contract" for the cost hook in
`weeks-04-07/student-materials/hooks/README.md`, which states what any port of
the hook must do. General: an elevator controller's requirements — which floor
requests are served in which order, what happens when a door is obstructed —
as numbered clauses.

**Survives a port?** Yes, unchanged.

**In the course.** Lecture 03 ("Round 2: deriving specifications from the
concept of operations"); Lecture 04 (the tests that cite §4.1); Lecture 05
("What Reversi demands that tic-tac-toe did not"); the project unit's Stage D,
where the same rules govern two implementations; demonstrated.

## C. Surfaces and formats

### Display format

**Fixes / leaves open.** Exactly what is rendered — every glyph, every fixed
measurement, byte for byte — for the initial state, a mid-play state, and a
terminal state. It leaves open nothing about the rendered text; that is what
"byte-exact" means. It leaves open how the rendering is computed.

**Typical forms.** An exact example plus the measurements a reader cannot
count reliably from the example (leading spaces, rule lengths), and a
statement of how lines are joined.

**Place in the specification family.** Derived from the concept of operations (what a player
sees) and must agree with the example session character for character.

**Audited by.** AUD-1 to AUD-7, and AUD-9: our audit rule AUD-9 requires that
a display format be byte-exact, with examples for at least the initial, a
mid-play, and a terminal state, and state every glyph and every fixed
measurement; "looks like the example" is an AUD-1 finding.

**Used in verification.** Verifier: algorithmic — golden-string tests that
compare the rendered string with the specification's example. Clauses:
mechanical. A pass establishes that the code renders what the test's constant
says; it does not establish that the constant matches the specification —
Lecture 04's third sabotage step, where both were wrong in the same way and the
gate stayed green.

**Examples.** Course: `SPECS.md` §7.2 of the game (four leading spaces on the
header, nineteen dashes in each border, `.` for an empty cell); the Reversi
display decisions the brief leaves to you — glyphs, labels, whether hints are
shown. General: the fixed-width layout of a printed bank statement, specified
column by column so that two printing systems produce identical pages.

**Survives a port?** Yes, unchanged.

**In the course.** Lecture 03 (the display ruling in round 2); Lecture 05;
the brief §4 "Display"; demonstrated.

### Input grammar

**Fixes / leaves open.** Every accepted form of an input and every rejected
form, how whitespace, case, and length are treated, and the effect of each
rejection on the turn and on the state. It leaves open the wording of the error
message unless the concept of operations fixes it.

**Typical forms.** A grammar — a pattern such as `[1-9][1-9]` — with an
enumerated list of rejected forms and the effect of each.

**Place in the specification family.** Derived from the concept of operations (how a player
enters a move); must agree with the interaction flow (what happens after a
rejection) and the example session.

**Audited by.** AUD-1 to AUD-7, and AUD-10: our audit rule AUD-10 requires
that the grammar enumerate every accepted and every rejected form, with the
effect of each rejection on the turn and on the state, and say how whitespace,
case, and length are treated.

**Used in verification.** Verifier: algorithmic — parametrized rejection tests,
one function with the specification's list of rejected forms as its inputs.
Clauses: mechanical. A pass establishes that each listed form is rejected as
specified; it does not establish that the list is complete — a form the
grammar never mentions is an AUD-4 finding, not a test failure.

**Examples.** Course: `SPECS.md` §6.2 of the game (exactly two characters,
each `1` to `9`, `0` rejected, whitespace stripped) and the test
`test_prompt_human_rejects_invalid_forms` in
`module-software-engineering/demos/lecture-03-game-demo/reference/tests/test_main.py`;
the Reversi notation `d3` and its edge cases (`D3`, `d9`, `i3`). General: the
accepted forms of a date field on a web form, with what each rejected form
produces.

**Survives a port?** Yes, unchanged.

**In the course.** Lecture 03 (the grammar ruling in round 2); Lecture 04 (the
parametrized test); Lecture 05; demonstrated.

### Interaction flow

**Fixes / leaves open.** Every menu with every option, every loop and every
exit from it, and the state the program is in after each. It leaves open how
the flow is coded.

**Typical forms.** Numbered steps per mode, or a state machine. The state
machine is the classical form (the essay's fourth example); the module writes
numbered steps because the flows are small.

**Place in the specification family.** Derived from the concept of operations' modes and
scenarios; must agree with the input grammar and the example session.

**Audited by.** AUD-1 to AUD-7, and AUD-11: our audit rule AUD-11 requires
every menu with every option, every exit from every loop, and the state after
each; no option may lead to an unstated state.

**Used in verification.** Verifier: algorithmic — scripted-input tests that
feed a sequence of inputs and check the sequence of screens and the final
state. Clauses: mechanical. A pass establishes that the scripted paths behave
as specified; it does not establish anything about paths no script takes,
which is why branch coverage (VER-5) and the per-menu obligations (§9) exist.

**Examples.** Course: `SPECS.md` §5.3 of the game (the main menu, the per-game
loop, the post-game menu, side alternation); the Reversi pass handling and
post-game options in the brief §4. General: a web shop's checkout — cart,
address, payment, confirmation — with every "back" and every failure exit
named.

**Survives a port?** Mostly: the menus and loops survive; the way input and
output are performed is re-expressed.

**In the course.** Lecture 03 (the flow in round 2); Lecture 05; the brief §4
"Interaction flow"; demonstrated.

### Data format

**Fixes / leaves open.** The exact form of a stored or exchanged artifact — a
file, a record, a message — down to what a parser can check: required fields,
their types and forms, structural rules. It leaves open the content and, unless
it says otherwise, anything a parser cannot check.

**Typical forms.** Numbered rules with an exact example (Lecture 01's format
specification), a schema (JSON Schema, an interface definition language), or a
loader contract that says how a file is read and what each field means.

**Place in the specification family.** Often the first specification a system has. For the
note set it is the governing document beside the concept of operations; for a
program it may govern a configuration file, a persisted state, or — as the
fixture file's shape — an executable specification's own container. It must
agree with any concept of operations that names the artifact.

**Audited by.** AUD-1 to AUD-7; the course has no per-kind rule for it. The
audit in Lecture 01 is the model: is each rule unambiguous enough for a program
to decide (AUD-1), do the rules agree with one another (AUD-2), are the
scoping questions answered (AUD-4) — is `index.md` a note? — and does every
rule have an identifier (AUD-5).

**Used in verification.** Verifier: algorithmic where the rules are
mechanical — a verifier program such as `check_notes.py`, a parser, or a schema
validator; human or agent for judgment clauses such as R8's "accurately
summarizes". A pass establishes that the artifact has the specified form; it
does not establish anything about the meaning of its content.

**Examples.** Course: `note-format-spec.md` R1 to R8
(`module-software-engineering/demos/lecture-01-note-specs-demo/completed/note-format-spec.md`)
and its verifier `check_notes.py`; the fixture file's shape — the loader
contract in
`module-software-engineering/demos/lecture-03-game-demo/reference/fixtures/README.md`
and the Reversi shape in `project-1-reversi-brief.md` §3.1; the entry format of
your Project 0 knowledge base (`module-software-engineering/project-0-pkb-brief.md`, §3 and §4);
the persisted game state of the project unit's Stage B
(`weeks-04-07/project-1-brief.md`). General: a JSON Schema for an application's
configuration file, against which every configuration is validated at start-up.

**Survives a port?** Yes, unchanged; a port writes a new parser for the same
format.

**In the course.** Lecture 01 (the whole lecture); Lecture 02 (the format
specification at 2.0.0); Project 0; the brief §3.1; Stage B; demonstrated.

## D. Interfaces

### Interface contract (in Lecture 02: the operations document)

**Fixes / leaves open.** For each public operation: its parameters and their
ranges, its precondition, its postcondition — what it returns and what state it
changes — and its behavior when called outside its precondition, including
after the system has reached a terminal state. It leaves open the algorithm.

**Typical forms.** Signatures with preconditions and postconditions (Meyer's
design by contract); for an agent's operations, the input, precondition,
steps, and postcondition of Lecture 02's operations document.

**Place in the specification family.** Derived from the concept of operations' operations;
must agree with the behavioral requirements (a move's postcondition is the
rules applied once) and with the verification obligations. The operations
document of the note set is the note set's instance, with one caveat: its
*Steps* field is a procedure, which a contract leaves open; the notes on naming
below say more.

**Audited by.** AUD-1 to AUD-7, and AUD-12: our audit rule AUD-12 requires,
for every public operation, its parameters and their ranges, its precondition,
its postcondition, and its behavior when called outside its precondition —
including after the game is over. Lecture 03's ruling that a move after the
game is over is rejected came from this rule.

**Used in verification.** Verifier: algorithmic — unit tests, and a type
checker where the language has one (the signature part of the contract is what
a compiler checks, the essay's second example). Clauses: mechanical. A pass
establishes that each operation behaves as the tests claim on the inputs they
use; it does not establish behavior on inputs no test uses.

**Examples.** Course: `SPECS.md` §5.1 of the game (`make_move(row, col) ->
bool`, when it returns `False`, that it changes nothing then); the note set's
`note-set-operations.md`
(`module-software-engineering/demos/lecture-01-note-specs-demo/completed/note-set-operations.md`);
the Reversi contract the brief asks for, in which a move's postcondition names
the discs that flip. General: a Java interface whose documentation states, for
each method, what must hold before the call and what holds after.

**Survives a port?** Re-expressed per language: the signatures change; the
preconditions and postconditions keep their meaning.

**In the course.** Lecture 02 ("Deriving lower-level specifications from the
concept of operations"); Lecture 03; Lecture 05; the project unit's Stage D;
demonstrated.

### Tool contract

**Fixes / leaves open.** An interface contract whose reader is a machine that
cannot read the source: the parameter schema, the description a model chooses
by, the return shape field by field, and errors as data the model can relay.
It leaves open the implementation behind the tool.

**Typical forms.** A function signature whose type hints become the schema and
whose docstring is the contract (FastMCP); an OpenAPI description; a
function-calling schema.

**Place in the specification family.** In the module it is derived from the interface
contract (DEV-5) and obliged to say more, because its consumer cannot look
inside: what an unknown identifier returns, that an illegal call returns a
structured error and never raises. Whether it is better seen as derived from
the interface contract or as a peer of it is Lecture 06's discussion question,
and this catalog does not settle it.

**Audited by.** AUD-1 to AUD-7, and AUD-12 applied to a tool: behavior outside
the precondition is the check that matters most, because the model will make
the call the contract did not anticipate.

**Used in verification.** Verifier: algorithmic for the schema (validation of
every call and return); human or agent for the behavior, by reading a call
transcript against a scenario of the concept of operations. Clauses: mixed. A
pass establishes that calls and returns have the specified shape and that the
transcript shows the scenario; it does not establish that a differently
worded description would lead the model to the same calls — Lecture 06's
sabotage step shows a misleading docstring changing the agent's play.

**Examples.** Course: the `make_move` docstring of the tic-tac-toe server in
Lecture 06; the dice server in
`weeks-04-07/student-materials/mcp-example/dice_server.py`; the Reversi server
of the project unit's Stage E. General: the OpenAPI description of a payment
endpoint, which a client generator and a human reader both consume.

**Survives a port?** Yes, at the protocol level: the schema and description are
independent of the server's language.

**In the course.** Lecture 06 ("The tool contract as a kind of
specification"); the project unit's Stage E; demonstrated in Lecture 06.

## E. Evidence and executable specifications

### Example session

**Fixes / leaves open.** One whole transcript — menu, moves, screens, the end —
as a specification by example. It fixes exactly one path and leaves every other
path to the other kinds.

**Typical forms.** A verbatim transcript in a code block.

**Place in the specification family.** Derived from the display format, the input grammar,
and the interaction flow; must agree with all three character for character. A
discrepancy is a finding against whichever of them is wrong, and a person
decides which (our development rule DEV-4).

**Audited by.** AUD-1 to AUD-7, and AUD-13: our audit rule AUD-13 requires
the session to be consistent, character for character, with the display
format, the input grammar, and the interaction flow.

**Used in verification.** Verifier: algorithmic — an end-to-end scripted run
that feeds the session's inputs and compares the output. Clauses: mechanical. A
pass establishes that one path is right end to end; it does not establish any
other path.

**Examples.** Course: `SPECS.md` §8 of the game; the one-game session with a
pass that the Reversi brief asks for. General: a recorded request-and-response
exchange kept as a contract test between two services.

**Survives a port?** Yes, unchanged.

**In the course.** Lecture 03 (round 2); Lecture 05; the brief §2;
demonstrated.

### Verification obligations

**Fixes / leaves open.** What the tests must claim about *this* system,
category by category — every direction of win, at least one overline, every
rejected input form, every menu branch — each obligation traced to the clauses
it verifies and every clause traced to at least one obligation. It leaves open
how the tests are written; and it does not contain the *policy* — the coverage
target, the single permitted pragma, the citation discipline — which lives in
the process documents (VER-4 to VER-8) and is the same for every project.

**Typical forms.** A list of categories under the technical specifications'
last section (`SPECS.md` §9 in the module), each naming the clauses it covers.

**Place in the specification family.** Derived from every other section of the technical
specifications; must map both ways to their clauses. It is the specification
that the test suite realizes.

**Audited by.** AUD-1 to AUD-7, and AUD-14: our audit rule AUD-14 requires
that the obligations map every clause to at least one obligation and every
obligation to the clauses it verifies, so that clause coverage can be reported
independently of code coverage.

**Used in verification.** Verifier: partly algorithmic — the suite's presence
per category — and otherwise human or agent, reading the suite against the
obligations to see that each is actually claimed by a test (VER-8; the
completion note of RPT-5 reports it). Clauses: mixed. A pass establishes that
every obligation has a test claiming it; it does not establish that the tests'
expectations are right.

**Examples.** Course: `SPECS.md` §9.5 of the game; the brief's Phase 1,
step 2, which asks you to write the same section for Reversi. General: a
requirements-to-test traceability matrix, as certification standards for
avionics software require.

**Survives a port?** Yes: the obligations are about the system, not the
language.

**In the course.** Lecture 03 (the ruling that "picks at random" becomes an
obligation about the result being among the available moves); Lecture 04
(clause coverage); Lecture 05; demonstrated.

### Test suite

**Fixes / leaves open.** The obligations, realized as executable claims: each
test cites the clause it verifies and asserts tighter than the clause, never
looser. As a specification it fixes what a conformant realization must do on
the inputs the tests use; it leaves open everything on other inputs.

**Typical forms.** Unit tests, golden-string tests, scripted-input tests, and
a fixture loader, one file per source module, each test with a docstring that
names its clause.

**Place in the specification family.** A realization of the verification obligations and, at
the same time, the algorithmic verifier of the code. It must agree with the
technical specifications clause by clause, and a test whose expectation
disagrees with a clause is a nonconformant realization of that clause.

**Audited by.** VER-6, the test discipline: our verification rule VER-6
requires that every test cite its clause, assert tighter never looser, use
direct assignment for setup only, and be able to fail; and the suite is read
against the obligations (AUD-14, VER-8). AUD-1 to AUD-7 apply to the suite as
a document — in particular AUD-5, traceability.

**Used in verification.** The suite *is* the algorithmic verifier: run under
the gate (VER-4), it decides the mechanical clauses. Its own verification is
different in kind: a realization that has been deliberately broken must fail
it — Lecture 04's sabotage steps — and a person or an agent reads its
expectations against the specification. A green gate establishes that the
code does what the tests claim and that every branch was reached; it does not
establish that the tests claim what the specification says, nor that every
clause is claimed (VER-8).

**Examples.** Course: the reference suite under
`module-software-engineering/demos/lecture-03-game-demo/reference/tests/` —
`test_check_winner_overline_counts` cites §4.1, the parametrized rejection
test cites §6.2. General: a library's unit-test suite that its maintainers run
before every release and that a contributor reads to learn what the library
promises.

**Survives a port?** No: the tests are re-expressed in the new language's test
framework. The obligations they realize survive.

**In the course.** Lecture 04 ("Tests as executable specifications"); the
brief's Phase 1, step 4; the project unit's Stage D; demonstrated.

### Fixtures

**Fixes / leaves open.** A set of scenarios with expected outcomes —
moves in, winner out; setup and attempt in, no change out — that any
implementation of the behavioral requirements and the interface contract, in
any language, must reproduce. It fixes those scenarios exactly and leaves open
everything the scenarios do not cover; it must say what it does not cover.

**Typical forms.** A data file (JSON in the course) whose shape is itself a
data format, plus a README that states the rules the fixtures assume, the
loader contract, and the known blind spots. A loader — two parametrized tests
in the course — turns each scenario into a test.

**Place in the specification family.** Derived from the behavioral requirements and the
interface contract; the file's shape is a data format; the loader is part of
the test suite. When two realizations of one specification both pass the same
fixtures, the plain one becomes the specification for the clever one — the
oracle idea of Lecture 04.

**Audited by.** VER-7: our verification rule VER-7 requires that a fixture
file state the rules it assumes and its known blind spots, and that it never be
edited to make a test pass — an expectation that looks wrong is a finding about
the pair (fixture, specification), reported as a gap and ruled on. AUD-1 to
AUD-7 apply to its README.

**Used in verification.** Verifier: algorithmic — the loader, run against every
implementation. Clauses: mechanical. A pass establishes that the implementation
reproduces the covered scenarios; it does not establish anything about the
blind spots the file names, which is why naming them is part of the file's
contract with its users.

**Examples.** Course: `fixtures/scenarios.json` and its README in
`module-software-engineering/demos/lecture-03-game-demo/reference/fixtures/`
(`x-wins-row-overline` is §4.1 as eleven moves; no tie scenario, on purpose);
the shared fixtures of the project unit,
`weeks-04-07/student-materials/fixtures/scenarios.json`; the Reversi shape in
`project-1-reversi-brief.md` §3.1, with the pass and early-end scenarios its
   §3.3 requires.
General: the published test vectors for a cryptographic hash function, which
every implementation in every language must reproduce.

**Survives a port?** Yes, unchanged: that is what it is for.

**In the course.** Lecture 04 ("Fixtures: executable specifications that
outlive the code"); Lecture 05; the brief's Phase 1, step 5; the project unit's Stage D;
demonstrated.

## F. Structure, platform, and process

### Architecture (in the module: the module split)

**Fixes / leaves open.** The parts of the system, their boundaries, and what
each may depend on — an engine with no input or output, a computer opponent as
a set of strategies, an entry point that owns every prompt. It leaves open the
algorithms inside each part and, unless it says otherwise, the names of files.

**Typical forms.** A file structure with one line per part; a sentence of
responsibility per part; in larger systems, component or container diagrams
(the essay's third example, UML).

**Place in the specification family.** Derived from the technical specifications' interface
contract and from the plan (DEV-9); must agree with both. The essay explains
why this kind drifts from its realization more than any other, and why
traceability (AUD-5) is the practical defense.

**Audited by.** AUD-1 to AUD-7; the course has no per-kind rule. The useful
checks are AUD-4 (does every part named in the concept of operations have a
home?) and AUD-5 (can each part be traced to the clauses it realizes?).

**Used in verification.** Verifier: human or agent, reading the code's
structure against the stated parts; algorithmic where a dependency rule is
written as a check ("the engine imports nothing that performs input or
output"). Clauses: judgment, unless a check is written. A pass establishes
that the parts and boundaries exist as stated; it does not establish that the
boundaries are the right ones.

**Examples.** Course: `SPECS.md` §2 (the file structure) and §5.1 ("pure
logic; no I/O") of the game; the approved plan's module list; the brief's Phase 1,
step 3, "module split per your spec". General: the rule in a layered application
that the domain layer imports nothing from the web layer, drawn as a diagram
and enforced by an import check.

**Survives a port?** Mostly: the parts and boundaries survive; file names and
packaging change.

**In the course.** Lecture 03 (the three-module result of the plan); the brief;
the essay; named only — the module states the split but does not audit or
verify it as a kind.

### Technology and platform

**Fixes / leaves open.** The named languages, versions, libraries, tools, and
hosts a realization must use. Unlike every other kind, it "flows up" from the
bottom: it does not describe the system, it limits the space of realizations.
It leaves open everything about behavior.

**Typical forms.** A "Requires" line; a dependency file (`requirements-dev.txt`,
`package.json`); a compiler configuration; a "Technology Stack" section of a
project's orientation file.

**Place in the specification family.** Constrains every realization; must agree with the
process documents (the gate command names the tools).

**Audited by.** AUD-1 to AUD-7; the course has no per-kind rule. AUD-1 is the
one that bites: "Python" is ambiguous, "Python 3.11 or newer" is not.

**Used in verification.** Verifier: algorithmic for what build and dependency
files can check (the interpreter version, the installed packages, a strict
compiler configuration); human for provenance — where a library came from and
whether it can be trusted, which the essay calls the trust gap of this kind.
Clauses: mixed. A pass establishes that the named technologies are the ones in
use; it does not establish that they are correct or safe.

**Examples.** Course: the brief's *Requires* line (Claude Code, Python 3.11 or
newer, git, `pytest` with `pytest-cov`); `SPECS.md` §1 of the game, "written in
Python"; the reference's `requirements-dev.txt`; the project unit's Stage D
scaffold with `strict` set in its `tsconfig.json` and `tsc --noEmit` as a
gate; the pinned `mcp[cli]` of Lecture 06. General: a software bill of
materials listing every third-party component in a product, with versions and
sources.

**Survives a port?** No: it is what a port changes.

**In the course.** The brief; Stage D; the essay; not demonstrated as a kind —
the course states its technologies but never audits or verifies the statement.

### Development process

**Fixes / leaves open.** How work proceeds with respect to the specifications:
the steps, their order, the gates a step must pass, the hand-offs between
steps, the forms in which findings and results are reported, and who may
change what. It leaves open every individual action within a step — which is
why an agent can follow it without being told every move.

**Typical forms.** The module's `process/` documents — development rules
(DEV), audit rules (AUD, AUDCON), verification rules (VER), reporting forms
(RPT), and a README that states the invariant they maintain — loaded by a
short `CLAUDE.md`. An approved plan under `plans/` is a process specification
for one build (DEV-9). In larger settings: a pull-request policy, a pipeline
definition, a certification standard's process objectives.

**Place in the specification family.** Governs the work on every other kind; its realization
is the repository's history — the commits, changelog entries, reports, and
completion notes. Lecture 02 says it in one sentence: auditing the process
means reading the log.

**Audited by.** Its own mechanism — a process document changes only by an
amendment proposal (RPT-3) with approval, a version bump, and a changelog entry
(DEV-3), as Lecture 04 shows when VER-5 to VER-8 are added — and AUD-1 to AUD-7
as for any specification. Rule identifiers are never renumbered.

**Used in verification.** Verifier: human or agent, reading the history against
the rules (did every operation end with the gate and a named commit? did the
amendment precede the code?); algorithmic where a step is a gate — the test
gate (VER-4) at every commit, and the hooks of the project unit that run a
check on an event. Clauses: mixed. A pass establishes that the recorded history
followed the process; it does not establish anything the history does not
record, which is why the process requires so much to be written down.

**Examples.** Course: `module-software-engineering/demos/lecture-03-game-demo/reference/process/`
and its `README.md` invariant; the loader `CLAUDE.md` beside it; the same set
in `module-software-engineering/student-materials/reversi-starter/`; the hooks
of `weeks-04-07/lecture-notes/lecture-12-hooks-and-memory.md`. General: a
team's rule that no change merges without a review and a green pipeline,
written down and enforced by the repository host.

**Survives a port?** Yes: the process is the same in every language; only the
gate command changes.

**In the course.** Every lecture of the module (Lecture 01 ships three
documents, Lecture 02 six, Lecture 04 amends them); the project unit's
cross-stage process requirements; demonstrated.

## Notes on naming

The lectures, the technical specifications, and the Project 1 brief use a few
names that are not kinds. Here is how each relates to the catalog.

- **Board and coordinates** (`SPECS.md` §3; the first item of Lecture 03's
  derivation prompt) is a *section* of the behavioral requirements: the
  surface, its coordinate system, and the initial state, which our audit rule
  AUD-8 names. Its storage clause (§3.2, the 2D list) belongs to the interface
  contract, because it is something the tests may rely on for setup.
- **Initial state** (Lecture 05's comparison table) is one clause of the
  behavioral requirements, listed on its own there only because it is a
  completeness trap in Reversi.
- **Computer opponent** (the brief's §4; Lecture 05's table) is a *subject*,
  not a kind: an actor in the concept of operations (§4.4), a section of the
  interface contract (`SPECS.md` §5.2), and a verification obligation (§9.5:
  the result is always among the available moves).
- **Testing contract**, an early planning name, is two things: the
  verification obligations (`SPECS.md` §9, what the tests must claim about this
  system) and the policy (VER-4 to VER-8, the same for every project), which is
  part of the development process.
- **Test suite** and **fixtures** are two kinds, not one: different rules
  (VER-6, VER-7), different consumers (a test runner; every implementation),
  and different answers to the port question.
- **The VER-2 table** groups clauses by verifier technique, not by kind: one of
  its rows covers the board, the rules, and the win and tie together, and
  another covers the input grammar and the interaction flow together. One VER-2
  row may therefore cover several catalog kinds.
- **The operations document** of Lecture 02 is the note set's interface
  contract, with a *Steps* field a contract does not have. The steps are an
  ordered procedure the agent follows; the precondition and postcondition are
  the contract. Lecture 02 keeps them in one document because the operations
  are few.
- **A realization used as a specification** — the plain 81-cell scan as the
  oracle for a faster engine (Lecture 04), the cost hook's original script as
  the specification of its port (the project unit) — is a *role* an artifact
  can play, not a kind; the fixtures entry says how the role works.
- **Not kinds:** the sketch (a draft of the concept of operations),
  `BACKLOG.md` (deferred questions, DEV-6), the glossary (a section of the
  concept of operations, AUDCON-4), and a plan (a process specification for one
  build, DEV-9).

## Mapping to the S/R essay

The essay `software-engineering/specification-implementation.md` introduced
specifications and realizations with seven classical examples and four
questions to ask of each. The catalog's entries relate to them as follows.

| Essay example | Catalog entries | In the course |
|---|---|---|
| Requirements and an executable system | concept of operations (the user-observable part); behavioral requirements | demonstrated, Lectures 02 to 05 |
| Interface declaration and the source of a class | interface contract (its signature part, checked by a type checker); tool contract (its schema part) | demonstrated: the VER-2 row "a type checker where used"; the Stage D `tsc --noEmit` gate |
| Documented architecture (UML) and the developed system | architecture | named only: `SPECS.md` §2 and §5, the plan; no diagrams |
| State machine diagrams and generated code | interaction flow (the form); behavioral requirements (the transitions) | the form is demonstrated as numbered steps; generation is not demonstrated |
| Technology specifications and the implemented system | technology and platform | implicit only: the brief's Requires line, dependency files |
| Development process specifications and artifact evolution | development process | demonstrated throughout the module |
| Test vectors, test suites as specifications (TODO in the essay) | verification obligations; test suite; fixtures | demonstrated, Lecture 04; this catalog stands in for the essay's missing section |

The essay's four questions are the catalog's facets:

| Essay question | Entry facet |
|---|---|
| how is the specification more abstract than the realization | Fixes / leaves open |
| what is the nature of the properties captured | Typical forms (and Fixes / leaves open) |
| what does it mean for the specification to be well-formed, and how could we check that | Audited by |
| how do we assess conformance, and what are the gaps in our confidence | Used in verification — "a pass establishes …; it does not establish …" |

Two of the essay's later ideas have names in this catalog. "Many
specifications, one realization" is the family of specifications, and the
essay's remark that the set must be consistent is our audit rule AUD-3 applied
across it. "Stacked specifications" — a higher-level specification realized by
lower-level ones — is the chain concept of operations → technical
specifications → plan, governed by DEV-5 (derived documents follow governing
ones) and AUD-5 (traceability). The essay is left as it is.
