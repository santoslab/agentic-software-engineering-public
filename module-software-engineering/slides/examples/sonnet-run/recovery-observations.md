# Observed recovery, including a missed instruction

The interrupted and recovery calls have different session IDs. The recovery
call did not use --resume/--continue and received only its saved generic prompt,
project guidance, Beads, and the working files. Automatic memory was disabled.

The raw recovery transcript shows these actions before the first test edit
(JSONL event positions below are zero-based, counting every event):

- Event 4: list in-progress/open beads, Git status, and recent commits.
- Event 9: show the actual active parsing bead and inspect the partial commit.
- Event 11: read parse.py, test_parse.py, app.py, and the relevant CLI contract.
- Event 39: append the missing menu-parser tests.

The first implementation action therefore targets the work recorded as remaining.
However, the requested explicit recovered-understanding/next-action report
**was not given before editing**. The only earlier assistant text was a general
statement that it would recover context. Do not present this run as satisfying
that reporting criterion. The tool sequence and later outcome are separate evidence.

A BSD sed invocation failed while adding the import. The agent noticed it,
corrected the import, and recorded the intended ImportError before implementing
parse_menu. Both the failed edit attempt and corrected red test run remain in
the original transcript.

The agent then completed menu parsing and made a separate II(b) caller-refactor
commit. Its recorded full run is 72 passed; no other implementation issue was
started. The generated test report does not resolve the existing D2 question
about plus signs/non-ASCII move digits, and the agent still reports that limitation.
