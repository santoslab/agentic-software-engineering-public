# Requirements: Message Guard (version A1)

Version A1. Each requirement carries an identifier, a verification method,
the EARS pattern it uses (rule SQ-3), and the story or glossary terms it
derives from (rule TR-1). Every requirement in this version is a mechanical
clause with method *test*: a test in `tests/` cites it by marker, and the
generated report `reports/conformance.md` shows which tests cite which
clause. Domain terms are those of `glossary.md` (rule SQ-4). The subject of a
clause about the input is the guard; the subject of a pass-or-drop clause is
the filter; the trigger of an event-driven clause is "When the filter is
given a message ...". Stakeholder sign-off is recorded separately in
`reports/validation.md`.

**REQ-0** · Method: test · Pattern: ubiquitous · Derived from: Glossary: message, security level, payload

The guard shall accept as its input only a message as the glossary defines
it: a security level that is exactly one of Public, Restricted, or Critical,
and an integer payload, neither of which changes after the message is
created.

**REQ-1** · Method: test · Pattern: event-driven · Derived from: US-3

When the filter is given a message whose security level is Critical, the
filter shall drop the message.

**REQ-2** · Method: test · Pattern: event-driven · Derived from: US-2

When the filter is given a message whose security level is Restricted, the
filter shall pass the message unchanged.

**REQ-3** · Method: test · Pattern: event-driven · Derived from: US-1

When the filter is given a message whose security level is Public, the
filter shall pass the message unchanged.
