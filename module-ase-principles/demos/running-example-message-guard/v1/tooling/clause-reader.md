# The clause reader: `tests/conformance.py`

## Goal

Read, from the specifications themselves, every identified clause with its
fields, every scenario, every glossary term, and every elicitation entry, so
that no report in this repository depends on a hand-kept list of what the
specifications contain. Rule SQ-1 names it for the identifier and method
parts of well-formedness; the conformance plugin and the trace tool are its
two consumers.

## Requirements

1. A clause header is one line: `**ID** · Key: value · Key: value ...`. The
   identifier family (`US`, `REQ`) decides which file it belongs in and which
   keys are allowed.
2. The method is one of `test`, `analysis`, `review (human)`, `review
   (agent)`, `walkthrough (human)`, `walkthrough (agent)`.
3. A header the reader cannot accept is a **finding**, never a silent
   omission: no `Method`; an unknown method, key, or EARS pattern; a
   requirement without a `Pattern`; a judgment method without a `Reason`; a
   duplicate identifier (the first definition is kept); an identifier family
   in the wrong file; an unknown family.
4. Scenarios come from `specs/scenarios.json`: `id`, `derived_from`,
   `input`, `expected` are required; a duplicate or malformed identifier is a
   finding.
5. Glossary terms are the `- **term**:` entries of `specs/glossary.md`; a
   term defined twice is a finding.
6. Elicitation entries are the `### E-n` headings of
   `reference/elicitation.md`, read so that `Source` fields can be resolved.
7. Everything that is not a header is contextual specification text and is
   not read; the reader decides syntax only.
8. Deterministic, dependency-free (standard library), and importable by the
   plugin and the trace tool.

## The prompt

Inherited from A0, where it was adapted from the Spec Kit tic-tac-toe demo.
The provenance chain the design records: the instructor's seed development
rules supplied the reporting goals; Spec Kit planning decision R7 chose
requirement markers and a generated report; tasks T004 to T006 specified the
clause reader and the plugin; public commit `4d6a2cd` introduced them; A0's
dev-log entry 2 records adapting them. The A1 extension (fields, scenarios,
glossary, entries, findings) was written by the build agent from
requirements 1 to 8 above, which the A1 plan's section 5.6 fixed first.

Guidance for the prompt that would produce it from nothing:

> Write a module that reads the clause headers of these specification files
> (give the header format and an example), returns the clauses in document
> order with their fields, and reports as findings, rather than skipping, a
> header it cannot accept: list the finding kinds. Read the scenario file,
> the glossary, and the elicitation record the same way. No hand-kept list
> of identifiers anywhere. Show me the data model and the finding kinds
> before writing code.

## Review points

The clause list comes from the files, not from a constant; a malformed header
produces a finding and the clause is still returned where possible; the
first of two duplicates wins and the second is reported; the reader does not
resolve links (that is the trace tool's job) and does not judge meaning.

## Deliberate-failure checks

The case directories under `tests/tooling/cases/` (page
[tooling-tests.md](tooling-tests.md)): `missing-method`,
`unknown-method`, `unknown-key`, `unknown-pattern`, `missing-reason`,
`duplicate-identifier`. Run them with `uv run pytest tests/tooling`. The
A0 reader dropped a header without a `Method` silently, which is the
finding `missing-method` exists to prevent; the plan's seeded gap G6 is the
same input in the real specifications.

## Adapting it to your project

Project-specific: the header regex and the ` · ` separator; the identifier
families and the file each belongs in; the allowed keys; the scenario file's
shape; the glossary entry shape. Carries over as an idea: specifications are
the source of truth for what exists, and a reader that cannot parse a line
says so.

## Making it shared infrastructure

Package the reader with the header format it reads: the format is the
contract, and a team that fixes one header format for all its projects can
share one reader. Version them together; a reader change that starts
accepting or rejecting a header changes what every project's reports say.
