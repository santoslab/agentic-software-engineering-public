# Lecture 01 — Intent, Specifications, Realizations, and the Judgments That Connect Them

> Agentic software engineering principles module, meeting 1. Companion reading
> for the lecture; self-contained. The example is version A0 of the message
> guard, in `../demos/running-example-message-guard/v0/`; file paths below are
> relative to that directory unless they say otherwise. Vocabulary follows the
> course glossary, `../../glossary.md`. Launches **Exercise 1**.

## The example: a message guard

An organization keeps a protected enclave. The systems inside it produce
messages of differing sensitivity, and some of those messages need to reach a
less trusted network outside. The *message guard* sits on the boundary and
decides, one message at a time, whether a message may leave. A message has two
parts: a security level, which is one of Public, Restricted, or Critical, and a
payload, which in this version is a single integer. In version A0 the guard has
one stage, called `filter`: a Critical message is dropped, and any other
message passes unchanged.

The example was chosen for three reasons. It is small: the file that does the
work is ten lines, and every artifact in the version can be read in
half an hour. Its shape is realistic: there is a boundary, a stakeholder who is
responsible for what crosses it, and a wrong outcome (a Critical message
leaving) that matters. And it grows: later versions add a second stage that
changes payloads, a record of what was stopped, a change of policy, sessions
with an ordering protocol, and a standard message format, and each of those
additions needs a kind of specification that this version does not. (The guard
is the Python counterpart of a guard built in the HAMR toolchain for seL4;
students who go on to that material will meet the same requirements again in
a different notation.)

The version is a directory, `v0/`, and its contents fall into categories that
this lecture will use throughout:

| Category | Files | Role |
|---|---|---|
| Intent | none | lives with the stakeholders; consulted through a person |
| Specifications | `specs/conops.md`, `specs/requirements.md` | what the system must do, as identified clauses |
| Realization | `guard/` (the code), `tests/` (the test suite) | what was built, and the executable claims about it |
| Development rules | `process/rules.md` | how each judgment is established and when it must hold |
| Reports | `reports/ledger.md`, `reports/dev-log.md`, `reports/walkthrough.md`, `reports/conformance.md` | the state of the development, readable without reading the code |
| Technology | `pyproject.toml`, `uv.lock` | Python 3.12 or later; `pytest`, `pytest-cov`, `ruff`; managed by `uv` |
| Support | `tools/gate.sh`, `tools/walk.py` | the gate command; a helper for walking through a scenario |

This lecture defines the entities in the first three rows and the five
judgments that relate them, points at the file in A0 that holds each, and
breaks two of the judgments to show which part of the repository notices.

## The question the code cannot answer

Here is the whole of `guard/filter.py`:

```python
"""The filter stage: pass or drop a message by its security level (REQ-1 to REQ-3)."""

from guard.message import Message, SecurityLevel


def filter_message(message: Message) -> Message | None:
    """Return the message unchanged if it may leave the enclave, or None if it is dropped."""
    if message.level is SecurityLevel.CRITICAL:
        return None  # REQ-1
    return message  # REQ-2, REQ-3
```

Is this code right? The question has no answer from the code alone, because
the code does not say three things. It does not say what was asked for: which
levels were meant to be stopped. It does not say what was promised: a statement
of the guard's behavior that someone responsible agreed to. And it does not
say whether the promise has been checked, by what, and when. The code would
look exactly like this if the security officer had wanted Restricted messages
stopped as well, and it would be wrong.

This has always been true of code. It matters more when an agent writes the
code, for a practical reason: an agent produces code quickly and in volume,
and the person directing the work does not read all of it. For a system of
any size they cannot. What that person reads instead is the specification,
the evidence that the code conforms to it, and the record of whether that
evidence is current. When those three things exist and can be trusted, a
person can direct the work, review it, and take responsibility for a system
whose code they have not read line by line. When they do not exist, the
person is relying on the agent's own description of what it did, and an
agent's description of its work is not evidence about the work. This lecture
is about the three things: the artifacts that hold them and the judgments
that say whether they hold.

## Three entities and five judgments

Diagram 1 in the slides shows the arrangement. There are three entities.
*Intent* is what the stakeholders want; it has no file. The *specifications*
are the documents in `specs/`. The *realization* is the code in `guard/` and
the tests in `tests/`. Between and on these entities sit five judgments, each
a claim about the current artifacts whose truth is tracked from commit to
commit:

| Judgment | The question it answers | Established in A0 by | Evidence in A0 |
|---|---|---|---|
| **SQ**, specification quality | Are the specifications well-formed, unambiguous, consistent with themselves and with each other, and complete for their level? | a person reading the two specifications together (rule SQ-1) | the SQ row of `reports/ledger.md` |
| **RQ**, realization quality | Does the code lint, and does the test suite collect and follow the test discipline? | `ruff`; `pytest --collect-only` (RQ-1) | exit codes, recorded in `reports/dev-log.md` |
| **CONF**, conformance | Does the realization satisfy every clause of every specification? | the test suite, two coverage measures, and the walkthroughs (CONF-1, CONF-2) | `reports/conformance.md`; the coverage table; `reports/walkthrough.md` |
| **VAL**, validated | Do the specifications describe what the stakeholders intend? | a stakeholder of each user category signing the concept of operations (VAL-1) | the sign-off in `reports/walkthrough.md` |
| **TR**, traceable | Does every clause carry an identifier, and does every link between artifacts resolve? | the markers and the "derived from" fields, read by a program and a person (TR-1) | the "Unknown identifiers" section of `reports/conformance.md` |

Four terms describe the bookkeeping. An **artifact** is anything under
version control that a judgment is about: a specification, the code, a rule
file, a report. The **development state** is the artifacts at a commit
together with the ledger. A **development-state judgment** is one of the five
claims above. The **ledger**, `reports/ledger.md`, is the table that states,
at a named commit, which judgments hold, on what evidence, and which have gone
stale.

Why five judgments rather than one judgment of "the system is good"? Because
they fail independently, and knowing which one failed tells you what to do.
The specifications can be sound and the code wrong (CONF fails, SQ holds).
The code can conform exactly to a specification that nobody wanted (CONF
holds, VAL fails). Every claim can be true and yet impossible to connect to
its evidence because an identifier was mistyped (TR fails). A single verdict
would hide the difference; five rows show it.

One remark for students who like formal models: the three entities, the four
judgments other than TR, and the rule that a change to an artifact invalidates
the judgments that depend on it are also the content of a small formal model
of development, written in Lean, that the course draws on. Nothing in this
lecture depends on it.

## Intent

Intent is what the stakeholders have in mind for the system. It lives in their
minds and is never fully written down, for the ordinary reason that a person
cannot enumerate everything they want from a system of any size, and would not
recognize some of what they want until they saw a system that lacked it. The
only way to consult intent is to ask a person: "is this what you want?", or
"does this behavior match what you expected?".

A0 therefore has no file called intent. What it has is the nearest written
thing, the **purpose statement** that opens `specs/conops.md`:

> An organization keeps a protected enclave whose systems produce messages of
> differing sensitivity, and it needs some of those messages to reach a less
> trusted network outside the enclave. The message guard sits on that boundary
> and decides, one message at a time, whether a message may leave. Nothing
> leaves the enclave except through the guard.

The purpose statement is an engineering artifact: a short text that the
stakeholders revised until they agreed with it, and that is audited like the
rest of the document. It is not a transcript of what anyone said. The
distinction matters because the two are treated differently: the purpose
statement is a clause that other clauses derive from and that can be checked
for consistency; a transcript is reference material that informs the writing
but is not itself checked.

The practical consequence for agentic development is that an agent has no
access to intent except through a person. An agent can read every file in the
repository and still not know that the security officer meant something
other than what the specification says. That is why one of the five
judgments, validation, is reserved to a person, and why the course keeps
intent out of the diagram's set of artifacts rather than pretending a file
could stand in for it.

How the purpose statement and the stories were obtained from the stakeholders
is the subject of the next lecture, which introduces elicitation on version
A1. In A0 they are given as already agreed.

## Specification

A **specification** is a document that states, at a higher level than the
artifact it governs, what the system must do. It fixes some properties and
deliberately omits others; the omissions leave the realization free where the
stakeholders do not care. Its clauses carry identifiers so that reports can
cite them.

A0 has two specifications. `specs/conops.md`, the **concept of operations**,
has five sections: the purpose statement; the scope and system boundary, with
a list of terms; the user categories; the user stories; and a pointer to the
sign-off. `specs/requirements.md` has four requirements. Together they are a
*family*: two documents of different kinds that govern one system and must
agree with each other.

The unit of a specification is the **clause**. Here is one from each file, as
it appears:

> **US-1** · Method: walkthrough (human) · User category: message sender
>
> As a message sender, when I send a Public message, I expect it to arrive
> outside the enclave unchanged.
>
> Example: the guard is given a message with level Public and payload 42; it
> outputs a message with level Public and payload 42.

> **REQ-1** · Method: test · Derived from: US-3
>
> The filter drops every message whose security level is Critical: for such a
> message it produces no output.

Every clause carries an **identifier** and a **verification method**, and
every requirement carries the clause it **derives from**. Each of the three
has a job.

The identifier is what a report cites. A person, an agent, and a program can
each check REQ-1 and say so, and because they all name the same clause their
reports can be compared. Without identifiers a finding is "the thing about
Critical messages", which two readers may locate differently and a program
cannot locate at all.

The method says how the clause is verified and therefore who can verify it.
In A0 two methods are in use. A clause marked *test* is decided by a program:
a test in the suite cites it and either passes or fails. A clause marked
*walkthrough* is decided by a person, who exercises the system along the
scenario and judges what they observe. The course calls a clause
**mechanical** when a program can decide it and a **judgment clause** when it
needs a reader; in A0 the four requirements are mechanical and the three
stories are judgment clauses. The method is recorded on the clause, rather
than in the verifier's head, because the choice has consequences that others
need to see. A mechanical clause can be checked at every commit by a program
that nobody has to remember to run. A judgment clause costs a person's
attention every time it is checked. When an agent is writing the code and the
tests, one wants as many clauses as possible to be mechanical, and the method
field is where that pressure is recorded and where a clause that cannot be
made mechanical is marked as such rather than silently left unchecked. Later
versions add two more methods, *analysis* for properties a program decides by
examining the artifact rather than running it, and *review* for properties a
reader decides from the text.

The "derived from" field links a requirement to the story or term it refines.
It is what makes the two documents a family rather than two files that happen
to be in the same directory: every requirement can be followed back to
something a stakeholder said they wanted, and every story can be followed
forward to the requirements that make it precise.

Notice also what the specifications leave open. They say nothing about how a
message reaches the guard, how its level was assigned, or what happens to a
dropped message. Those are outside the system boundary stated in section 2 of
the concept of operations. The realization is free there, and a later version
that adds a record of dropped messages will have to add clauses, not reinterpret
these.

## Specification quality

A specification can be wrong in ways that have nothing to do with the code.
Two of its clauses can contradict each other, so that no realization could
satisfy both. A clause can admit two readings, so that two verifiers would
reach different verdicts on the same code. A clause can be missing, so that a
whole behavior is unconstrained. Checking code against a specification with
one of these defects gives a confident answer to the wrong question. The
situation is worse with an agent than with a human developer, because an agent
realizes what the text says, at speed, and will produce a passing test suite
for either reading of an ambiguous clause.

The course names five properties of a good specification. Each is stated
here with the place in A0 where it can be checked.

- **Well-formed.** Every clause has an identifier and a method, in a form a
  program can read. In A0 the form is the header line `**REQ-1** · Method:
  test`, and the program that writes the conformance report reads exactly that
  line to learn which clauses exist.
- **Unambiguous.** Each clause has one reading, so that a verifier reaches a
  yes-or-no verdict. REQ-1 says what "drops" means in the same sentence: "it
  produces no output". Consider REQ-2 in class: it says a Restricted message
  passes "unchanged", and the test decides that with `filter_message(message)
  == message`, equality of level and payload. Is that the only reading? A
  reader who thinks of identity rather than equality, or of a message with
  more fields than two, has a different one. A0's answer is that the term
  *pass* in the concept of operations defines "unchanged" and that the message
  has exactly two fields; whether that is enough is the kind of question the
  next lecture's audit is built to ask.
- **Internally consistent.** No two clauses contradict. REQ-1 to REQ-3 assign
  each of the three levels one outcome and do not overlap. A requirement that
  "every message is passed" would contradict REQ-1, and no realization could
  satisfy the document.
- **Externally consistent.** The documents of the family agree. Every
  requirement derives from a story or from the terms; the words Public,
  Restricted, Critical, pass, and drop are used in the same sense in both
  files; nothing in the requirements promises a behavior that a story
  contradicts.
- **Complete for its level.** Completeness is relative to the abstraction the
  specification has chosen. The concept of operations says nothing about
  transport, and that is not incompleteness; the boundary excludes it. But
  there are three levels and three requirements that say what happens to each,
  and if there were a fourth level with no requirement, the document would be
  incomplete at its own level.

In A0 the SQ judgment is established in the simplest way: rule SQ-1 requires
the properties, and a person read the seven clauses together and recorded the
reading in the ledger. The ledger row says who read them and which clauses,
which is the pattern every row follows. The next lecture replaces the reading
with an audit: a procedure, run by a person and then by an agent, over a
specification that has gaps placed in it on purpose, and it introduces the
form in which gaps are reported and ruled on. That is the deep treatment of
specification quality; this lecture establishes only what the judgment asks.

A sixth property, traceability, is sometimes listed with these five. The
course tracks it as its own judgment, TR, because a program can check it
directly, and it is treated below.

## Realization

A **realization** is an artifact built to satisfy a specification. When the
artifact is code the usual word is implementation; the general term is used
because a test suite, a document, or a configuration can each be built to
satisfy a specification, and because a realization need not be the only one.
A different program in a different language that drops Critical messages and
passes the rest would be another realization of the same two specifications.

A0's realization is `guard/` and `tests/`. The code is two modules.
`guard/message.py` defines the security level as an enumeration with exactly
three members and the message as a frozen dataclass, and it rejects a message
whose level is not a `SecurityLevel` or whose payload is not an integer;
that is REQ-0 made concrete. `guard/filter.py` is the function shown at the
start of the lecture.

The test suite is a realization too, of a particular kind: an **executable
specification**, in which each test is a claim about one clause and cites
it. Here is `tests/test_filter.py`:

```python
import pytest

from guard import Message, SecurityLevel, filter_message


@pytest.mark.req("REQ-1")
@pytest.mark.parametrize("payload", [0, 100, -5])
def test_critical_is_dropped(payload):
    assert filter_message(Message(SecurityLevel.CRITICAL, payload)) is None


@pytest.mark.req("REQ-2")
def test_restricted_passes_unchanged():
    message = Message(SecurityLevel.RESTRICTED, 7)
    assert filter_message(message) == message


@pytest.mark.req("REQ-3")
def test_public_passes_unchanged():
    message = Message(SecurityLevel.PUBLIC, 42)
    assert filter_message(message) == message
```

The marker `@pytest.mark.req("REQ-1")` is the citation. It serves three
readers. A program can compute, from the markers, which clauses have tests
and which do not. A person who sees this test fail knows which clause is in
question without reading the test body. And an agent that writes a test must
say which clause the test is evidence for, which rules out the common failure
of a test that exercises the code without claiming anything about it. A test
that cites no clause is, under A0's rules, not allowed in the suite.

**Realization quality** is the judgment that the realization is in a state
where it can be checked at all. In A0 it has two parts, both decided by
programs: `ruff check` finds a class of mistakes (unused names, undefined
names, syntax that will not run) more cheaply than any test would, and
`pytest --collect-only` confirms that every test file imports and every
marker is declared. Rule RQ-1 names both commands. The suite is also held to a
test discipline, stated in the course's development rules: a test must be
able to fail, must assert no more loosely than the clause it cites, and must
set up its inputs by construction rather than by reaching into the code's
internals. Those three are reviewed rather than computed in A0.

Realization quality is kept separate from conformance for a reason that
becomes visible on the ledger. A suite that does not collect produces no
conformance evidence at all; a module with an undefined name may pass every
test that does not reach the name. Checking the realization's own soundness
first means that a conformance result, when it comes, is a result about code
that is at least runnable and a suite that at least ran.

## Conformance and verification

**Conformance** is the relationship between a specification S and a
realization R that holds when R satisfies every property S states. It is a
yes-or-no question about the pair, and properties S does not state are not
part of it. **Verification** is the activity of trying to confirm that the
relationship holds. The word *trying* is deliberate. A verification produces
a result, and the result is evidence with a scope: which verifier produced
it, against which version of the specification, over which clauses. Within
that scope it can be trusted; outside it, it says nothing; and, as a later
lecture will take up, even within it the verifier can be wrong.

In A0, conformance is not one thing but four, and the reason is the central
technical point of this lecture. A passing test suite, on its own,
establishes only that the suite's own claims hold. When an agent has written
both the code and the tests, a green suite can mislead in three ways. The
suite may contain no test for some clause, in which case the clause is
unverified and the green run says nothing about it. The tests may exercise
only part of the code, in which case the untested part may do anything. And
the clauses that no test can decide, the stories, may simply have been
skipped. The CONF judgment is therefore the conjunction of four conditions,
each with its own evidence:

1. **Every test passes.** The run itself.
2. **Requirements coverage.** Every clause whose method is *test* is cited by
   at least one passing test. The program that writes `reports/conformance.md`
   reads the clause identifiers from the specifications, collects the markers
   from the suite, and produces one row per clause:

   | Clause | Specification | Method | Tests citing it | Status |
   |---|---|---|---|---|
   | US-1 | `conops.md` | walkthrough | — | walkthrough: see `reports/walkthrough.md` |
   | US-2 | `conops.md` | walkthrough | — | walkthrough: see `reports/walkthrough.md` |
   | US-3 | `conops.md` | walkthrough | — | walkthrough: see `reports/walkthrough.md` |
   | REQ-0 | `requirements.md` | test | five tests in `test_message.py` | pass |
   | REQ-1 | `requirements.md` | test | `test_filter.py::test_critical_is_dropped[0]`, `[100]`, `[-5]` | pass |
   | REQ-2 | `requirements.md` | test | `test_filter.py::test_restricted_passes_unchanged` | pass |
   | REQ-3 | `requirements.md` | test | `test_filter.py::test_public_passes_unchanged` | pass |

   A clause with no citing test would show **no evidence**, and the run would
   fail. This is a coverage measure over the specification, in the same way
   that the next condition is a coverage measure over the code.
3. **Structural coverage.** The suite exercises every branch of `guard/`.
   `pytest-cov` measures it and fails the run below 100 percent:

   ```
   Name                Stmts   Miss Branch BrPart  Cover
   ---------------------------------------------------------------
   guard/__init__.py       3      0      0      0   100%
   guard/filter.py         5      0      2      0   100%
   guard/message.py       13      0      4      0   100%
   ---------------------------------------------------------------
   TOTAL                  21      0      6      0   100%
   ```

   Branch coverage is not a strong property. It says every branch was taken
   by some test, not that the test checked anything useful on that path. But
   a branch that no test took is a place where the code can do anything
   without the suite noticing, and the measure finds those places cheaply.
4. **Every judgment clause has been walked.** The three stories cannot be
   decided by a test in this version. Each was exercised by a person, in the
   role the story names, and the record is a table in `reports/walkthrough.md`:

   | Clause | Role | Command | Observed | Finding |
   |---|---|---|---|---|
   | US-1 | message sender | `tools/walk.py Public 42` | `pass: Public 42` | as the story expects |
   | US-2 | message sender | `tools/walk.py Restricted 7` | `pass: Restricted 7` | as the story expects |
   | US-3 | security officer | `tools/walk.py Critical 100`, then `Critical 0` | `drop`, both times | as the story expects |

The first three conditions are decided by one command, `tools/gate.sh`,
which runs `ruff` and then `pytest`. Its output at v0 ends:

```
conformance: every test clause has passing evidence; report in reports/conformance.md
...
Required test coverage of 100% reached. Total coverage: 100.00%
============================== 10 passed in 0.03s ==============================
```

Rules CONF-1 and CONF-2 state the four conditions; the CONF row of the ledger
cites all four pieces of evidence.

Asking who decided each condition introduces a distinction the course will
use repeatedly. The first three were decided by programs: `pytest`, the
report-writing plugin, `pytest-cov`. The fourth was decided by a person. The
course names three kinds of **verifier**. A *human verifier* reads the
specification and the realization and works through the clauses; it can
decide any clause, including a judgment clause, and it is slow and only as
reliable as its attention. An *agent verifier* is asked to check and report;
it can also decide judgment clauses, costs tokens, and may give different
results on two runs. An *algorithmic verifier* is a program; it is
deterministic, immediate, and free to run, decides only mechanical clauses,
and because it returns an exit code it can stand in front of a commit. A0
uses the first and the third. The second enters in A1, when an agent is asked
to audit the specification, and the question of how a check moves from a
person to an agent to a program is a thread through the whole module.

Finally, what a green CONF does not establish. It does not establish that
the clauses are the right clauses; that is validation. And it does not
establish that the verifiers are correct: a test can assert the wrong thing,
a plugin can misread a marker, a coverage tool can be misconfigured. The
ledger records which verifier produced each piece of evidence partly so that,
when a verifier is later found to be wrong, the claims it made can be found.
That is as far as this lecture takes the point.

## Validation

**Validation** is the question whether the specifications describe what the
stakeholders intend. It differs from verification in what it compares.
Verification compares two artifacts, a specification and a realization, both
of which are in the repository. Validation compares an artifact with what is
in a person's mind, which is not. So validation can only be decided by a
person, and the decision is recorded as a **sign-off**. A0's is in
`reports/walkthrough.md`:

> "The concept of operations, version A0, describes the guard I intend: a
> Critical message never leaves, and anything else leaves as it arrived."
>
> Security officer: role played by the instructor, 2026-10-20, on
> `specs/conops.md` version A0. Message sender: role played by the instructor,
> 2026-10-20, on `specs/conops.md` version A0.

The sign-off names who signed, in which role, when, and which version of
which document. Rule VAL-1 requires one from each user category.

The walkthrough table shown above does double duty, and the two duties should
be kept apart in thought even though one activity serves both. When the
security officer walks US-3 and sees `drop`, two questions are answered at
once: does the system behave as the story says (a conformance question about
a judgment clause), and is the story what the officer wants (a validation
question). A different officer, walking the same story and seeing the same
output, might answer the first question yes and the second no, and that is
exactly the case the next paragraph constructs.

Suppose the security officer had meant that Restricted messages must be
stopped as well, and that the person who wrote the concept of operations had
not understood this. Look at the repository. The two specifications are
consistent with each other: US-2 says a Restricted message arrives unchanged
and REQ-2 agrees. Every requirement has a passing test. Branch coverage is
complete. Every identifier resolves. Four of the five ledger rows are
established on sound evidence, and the fifth will be too if the officer signs
without reading. Nothing in the repository can detect that the system is
wrong, because every artifact in the repository was derived from the same
misunderstanding. The only thing that catches it is the officer walking US-2,
seeing `pass: Restricted 7`, and saying that this is not what they want, or
reading the concept of operations and declining to sign. This is why
validation is a separate judgment with a separate row, and why the row's
evidence is a person's recorded decision rather than a tool's output.

The point has particular force with agents. An agent given a specification
will realize that specification, and a well-run process will produce a green
ledger for it. If the specification describes the wrong system, the agent
has built the wrong system correctly, and the process has certified that.
The sign-off is the one place where the process asks a person whether the
system being certified is the one they wanted.

One more consequence, which later versions develop: the VAL row can go stale
when no file has changed. If the officer changes their mind, the
specification no longer describes what they intend, and the process learns of
it only when they say so. Version A3 records such a declaration as a change
request and shows the row turning stale while every other row stays green.

## Traceability

**Traceability** is the set of links between identified items in different
artifacts, and the TR judgment is that every link resolves. In A0 the links
run in a chain: a story in the concept of operations, to the requirements that
derive from it, to the tests that cite them by marker, to the rows of the
conformance report, to the CONF row of the ledger that cites the report. Rule
TR-1 requires that every marker name a clause the specifications define and
that every "derived from" name a clause that exists. The first part is
decided by the report-writing program, which lists any marker it cannot
resolve under "Unknown identifiers" and fails the run; `pytest` itself is
configured with `--strict-markers`, so a marker that was never declared is
rejected before any test runs. The second part is read by a person as part of
SQ-1.

Traceability is given its own row for two reasons. It can be decided by a
program, so it is cheap to keep established. And the other four rows depend on
it clause by clause: a conformance report is only readable if its identifiers
resolve, and an audit finding is only actionable if it names a clause. In
agentic development the identifiers are the vocabulary shared by the person,
the agent, and the programs. When all three say REQ-1 they mean the same
sentence, and a report from any of them can be checked against a report from
any other.

## The ledger

`reports/ledger.md` is the table of the five judgments at a named commit.
The CONF row at v0, condensed:

| Judgment | Status | Evidence | Provenance | Goes stale when |
|---|---|---|---|---|
| CONF | established | tests: 10 passed; requirements coverage 4 of 4 test clauses; branch coverage 100 percent of `guard/`; US-1 to US-3 walked | analysis: pytest 9.1.1 with pytest-cov 7.1.0 and the plugin in `tests/conftest.py`, specifications and realization at v0, clauses REQ-0 to REQ-3; walkthrough (human): the instructor as sender and as security officer, 2026-10-20, clauses US-1 to US-3 | a specification or the code changes |

A row has four parts, and each is there for a reason.

The **status** is established or stale. A judgment is *established* when its
evidence has been produced and recorded. It goes *stale* when an artifact it
depends on changes, and stays stale until it is re-established. The last
column says, for each row, what change would do that; a specification change
makes four rows stale, a code change three, and a stakeholder's declared
change of mind one.

The **evidence** is what was produced: a report, a run, a record. It is named
precisely enough to be found.

The **provenance** says who or what produced the evidence, against which
versions of which artifacts, over which clauses. These are the three scope
lines of a verification result from earlier in the lecture, moved onto the
row. They are there because a row is a claim made by a verifier, not a fact
about the system, and a claim can be wrong. If the plugin that writes the
conformance report is later found to misread a marker, the rows whose
provenance names the plugin are the rows to distrust. And the provenance is
what distinguishes evidence from a description of evidence: "pytest 9.1.1
exited 0 at v0" is a claim that can be rerun; "all tests pass" in an agent's
completion message is not. A0's rule RPT-1 requires the provenance on every
row for this reason.

A ledger with all five rows established is what the course means by a green
development state. It is not a proof. It is five claims, each with named
evidence and a named scope, which is what a person who has not read the code
can examine and, if they choose, rerun.

## The gate

Rule WF-1 says that before work is committed, the command `tools/gate.sh`
must exit 0. The command runs `ruff`, then `pytest` with the coverage
requirement and the report-writing plugin, so it decides RQ and the three
mechanical conditions of CONF in one step. A **gate** is a condition placed in
front of a step so that the step cannot complete unless the condition holds.
This one is an *algorithmic* gate: a program decides, and the decision is an
exit code. The course also names *approval* gates, where the condition is a
recorded human decision; A0's sign-off is a human decision but does not stand
in front of a commit, and the first approval gate in that position arrives
with the build plan in version A2.

The reason to have a gate at all, rather than a rule that says to run the
checks, is that an agent commits often and a rule that depends on someone
remembering is a rule that will be skipped. A gate makes the checks a
property of every commit, which is to say an invariant: at every commit in
the history, the gate passed.

## Breaking it: conformance

Each judgment in A0 has a sabotage that turns exactly its row red and shows
which verifier notices. Two are run in this lecture; the README lists three
more for the lecture on testing.

The first is a wrong realization. In `guard/filter.py`, change
`SecurityLevel.CRITICAL` to `SecurityLevel.RESTRICTED`, so that Critical
messages pass and Restricted ones are dropped. Run the gate:

```
conformance: REQ-1: FAIL
conformance: REQ-2: FAIL
conformance: FAIL, see reports/conformance.md
...
4 failed, 6 passed in 0.05s
```

Four tests fail: the three parametrized cases for REQ-1 and the one for REQ-2.
The conformance report shows those two clauses as **FAIL** and the other two
as pass. Branch coverage is still 100 percent, which is worth pointing out:
coverage is a property of which code ran, not of whether it was right. The
verifier that caught the change is the test suite, and the row that turned
red is CONF; SQ, VAL, and TR are untouched, because no specification changed
and every link still resolves. Restore the file and the gate is green again.

A failed conformance check reports a fact about the pair: the specification
and the realization do not agree. It does not say which side is wrong. Here
the specification is right and the code was changed, so the code moves back.
In other cases the realization is what the stakeholders want and the
specification stated it badly, and the specification is amended. Deciding
which side moves is an engineering decision made by a person and recorded; in
A0 the record is the entry in `reports/dev-log.md`, and the fuller machinery
of amendments and change requests arrives in version A3.

The second sabotage, validation, was described above and has no command to
run, which is its point.

## The development rules

Everything above is governed by `process/rules.md`, which holds eight rules:
one for each of the five judgments, with CONF having two, plus one for the
workflow (the gate) and one for reports (the dev log and the ledger). Each is
filed under the judgment it maintains and has the same fields. Here is CONF-1:

| Field | |
|---|---|
| Style | obligation |
| Maintains | CONF |
| When | at every commit; applies to every clause whose method is *test* |
| Statement | Every clause with method *test* MUST be cited, by marker, by at least one test; every citing test MUST pass; and the suite MUST reach 100 percent branch coverage of `guard/`. |
| Decided by | analysis: `uv run pytest`. The plugin in `tests/conftest.py` fails the run on a clause with no evidence or with a failing citation; `pytest-cov` fails it below 100 percent. |
| Evidence | `reports/conformance.md`; the coverage table in the run output, recorded in the dev log |
| On failure | a test is added or fixed, or the code is fixed; a clause is never weakened to make the run pass |
| Example | REQ-1 is cited by `test_filter.py::test_critical_is_dropped` |

Two of the fields deserve attention now. *Decided by* names the verifier, so
that a rule is something that can actually be checked rather than a statement
of good intentions; a rule with no decider cannot be followed by a program and
is easy for a person to believe they are following. *On failure* says what
happens, so that a red result has a next step. The rules in A0 come in two
styles: an **obligation**, "every X must have property P", and a **gate**,
"when step S would complete, condition C must hold". Later versions add
further styles as the process grows.

The rules are a file in the repository, rather than a convention, because the
agent reads the file. An agent started in this directory is told, through
the project's instructions, to read `process/rules.md`, and from that point
the person and the agent are following the same written process. When the
agent adds a test it cites a clause because CONF-1 says so; when it finishes
a task it records the gate result because RPT-1 says so. A process that lives
in a person's habits cannot be followed by an agent, and a process that lives
in the agent's prompt cannot be audited by a person; a process that is a file
can be both followed and audited.

The remaining report, `reports/dev-log.md`, is the append-only record of what
each task did: the files it touched, the judgments it affected, and the gate
result. A0's has three entries, for writing the specifications, realizing them
with tests, and walking the stories and writing the ledger. It is the record a
person reads to learn what happened, as the ledger is the record they read to
learn where things stand.

One observation about where effort goes. In A0 the code is under thirty lines.
The specifications, rules, and reports are more than three hundred. That ratio is not
a property of this small example; it reflects a shift in what a person does
when an agent writes the code. The person's effort goes into saying what is
wanted, deciding how it will be checked, and reading the evidence, because
those are the parts an agent cannot do alone and the parts that make the
agent's output something a person can stand behind.

In class, the lecture may close with one demonstration: an agent started in
the A0 directory is asked what the system does and how it is known that the
code does it. The useful thing to watch is where the agent looks. An answer
drawn from `specs/`, `reports/conformance.md`, and `reports/ledger.md` is an
answer a person could check; an answer drawn from reading `guard/filter.py`
is the agent's opinion of the code.

## What is not here yet

Version A1 keeps the same system and improves the specifications. It shows
how the purpose statement and the stories are obtained from stakeholders
(elicitation), adds a glossary of the domain's terms as a specification of
its own, rewrites the requirements in a structured natural-language form,
derives fixtures from the stories so that a story can be checked by a test as
well as by a walkthrough, and replaces the reading of the specifications with
an audit that finds gaps placed in the specification on purpose, first by a
person, then by an agent, then as a packaged skill. The next two lectures
cover that material.

Version A2 adds the second stage, `sanitize`, and with it the first
specifications of structure: an architecture with two stages in a fixed
order, a definition of the message's format, and contracts between the stages.
The work is large enough to need a plan with tasks and waves, and the ledger
is generated by a tool rather than written by hand. Later versions add a
change of policy, sessions with an ordering protocol, and a standard message
format, each bringing the kind of specification it needs.

## Exercise 1

Take a copy of A0 and add a requirement: a message whose payload is negative
is dropped, whatever its level. Before writing any code, read the new
requirement together with REQ-0 to REQ-3 and decide whether the five
specification-quality properties still hold; at least one does not, and the
resolution is an amendment to existing clauses, not just an addition. Record
which ledger rows the amendment makes stale and why. Then carry the
requirement through: the clause with its identifier, method, and derivation; a
test that cites it; the gate; the ledger; and a dev-log entry. If a story is
affected, say what the sign-off would have to say now.

Deliverable: the diff of the specifications and the realization, the ledger
after the change, and half a page on which rows went stale, which verifier
re-established each, and which could not be re-established without a person.

## Questions to think about

1. REQ-2 says a Restricted message passes "unchanged", and the test decides it
   by equality. Write down a reading of "unchanged" under which the test is
   too weak, and say which artifact you would change to rule the reading out.
2. Write a change to `guard/filter.py` under which every test passes and every
   requirement has evidence, yet the gate is red. Say what the change does to
   a message that no test sends, and what that tells you about which of the
   four conformance conditions found it.
3. For each of the five rows at v0, say whether the evidence was produced by a
   program or a person. For each row a person produced, say what would have
   to be written down before a program could produce it instead, and whether
   anything is lost if it is.

## Before next meeting

- Run A0 yourself: `uv sync`, then `tools/gate.sh`, then the two sabotages
  from the README, restoring the file after the first. Read `reports/ledger.md`
  and check one row's evidence against the file it names.
- Read the glossary entries for the terms introduced here: intent, purpose
  statement, specification, realization, conformance, verification,
  validation, development-state judgment, ledger, establish and stale,
  provenance, traceability, gate, mechanical clause and judgment clause,
  verification method, verifier, executable specification, requirements
  coverage and structural coverage.
- Read `specs/conops.md` once more and ask how its author could have found
  out what the security officer wanted. The next lecture is about that.
