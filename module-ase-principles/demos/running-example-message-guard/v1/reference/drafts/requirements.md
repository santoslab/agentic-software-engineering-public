# Requirements: Message Guard (version A1)

Version A1. Each requirement carries an identifier, a verification method,
the EARS pattern it uses (rule SQ-3), and the story or glossary terms it
derives from (rule TR-1). Every requirement in this version is a mechanical
clause with method *test*: a test in `tests/` cites it by marker, and the
generated report `reports/conformance.md` shows which tests cite which
clause. Domain terms are those of `glossary.md` (rule SQ-4). Stakeholder
sign-off is recorded separately in `reports/validation.md`.

**REQ-0** · Method: test · Pattern: ubiquitous · Derived from: Glossary: message, security level, payload

The guard shall take as its input a message consisting of a security level,
which is exactly one of Public, Restricted, or Critical, and an integer
payload. The guard shall not change a message after it is created.

**REQ-1** · Method: test · Pattern: event-driven · Derived from: US-3

When the filter is given a message whose security level is Critical, the
filter shall drop the message and shall record the drop.

**REQ-2** · Method: test · Pattern: event-driven · Derived from: US-2

Restricted messages are allowed through.

**REQ-3** · Method: test · Pattern: event-driven · Derived from: US-1

When the filter is given a message whose security level is Public, the
filter shall pass the message unchanged.

**REQ-4** · Derived from: US-3

The filter shall produce no output when it receives no message.

**REQ-5** · Method: test · Pattern: ubiquitous · Derived from: ConOps §2.1

The guard shall receive every message that leaves the enclave.
