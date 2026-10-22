# Requirements: Message Guard (version A0)

Version A0. Each requirement carries an identifier, a verification method,
and the story or specification section of the concept of operations it
derives from; REQ-0 refers to the Terms section. Stakeholder sign-off is
recorded separately in `reports/walkthrough.md`. Every requirement in this
version is a mechanical clause with method
*test*: a test in `tests/` cites it by marker, and the generated report
`reports/conformance.md` shows which tests cite which clause.

**REQ-0** · Method: test · Derived from: ConOps §2 (Terms)

A message consists of a security level, which is exactly one of Public,
Restricted, or Critical, and an integer payload. A message does not change
after it is created.

**REQ-1** · Method: test · Derived from: US-3

The filter drops every message whose security level is Critical: for such a
message it produces no output.

**REQ-2** · Method: test · Derived from: US-2

The filter passes every message whose security level is Restricted, unchanged:
the output is a message with the same level and the same payload.

**REQ-3** · Method: test · Derived from: US-1

The filter passes every message whose security level is Public, unchanged.
