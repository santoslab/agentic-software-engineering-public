# Concept of Operations: Message Guard (version A1)

Version A1. Revised from A0 through elicitation with the stakeholders (procedure
Elicit); the record is `reference/elicitation.md`, reference material that
this document cites by entry identifier (E-n). The three user stories carry
identifiers and verification methods; their examples are the scenarios of
`scenarios.json`, which any realization of the guard must reproduce. The
purpose, scope, assumptions,
user-category descriptions, and deferred wants provide context for
interpreting them and are reviewed with them (ConOps-SQ-1). Domain terms are
defined once, in `glossary.md`, and used here in that sense (Gloss-SQ-1). The
requirements derived from the stories and the terms are in
`requirements.md`. Stakeholder sign-off is recorded separately in
`records/validation.md`.

## 1. Purpose

An organization keeps a protected enclave whose systems produce messages of
differing sensitivity, and it needs some of those messages to reach a less
trusted network outside the enclave. The message guard sits on that boundary
and decides, one message at a time, whether a message may leave.

In this version the decision rests on one thing, the security level marked
on the message: a message marked Critical never leaves, and every other
message leaves exactly as it arrived. The guard does not inspect the payload
(E-1). This version establishes the guard itself, and the way its behavior
is specified and shown to hold; what later versions may add is recorded in
section 5 as deferred wants, not promised here.

Agreed by the security officer and a message sender on 2026-10-22; their
words are in `reference/elicitation.md` (E-1, E-3).

## 2. Scope and system boundary

The guard is a library: a function that takes one message and returns either
that message or nothing. Inside the boundary is the decision to pass or drop
a message by its security level. Outside the boundary are the transport that
carries messages to and from the guard, the authentication of senders, the
assignment of security levels, any record of what was dropped, and any change
to a message's payload. Each call is independent: the guard keeps no state
between messages. An input that is not a message as the glossary defines it
is outside the boundary: REQ-0 requires that the guard not accept it, and how
a realization signals that it did not is not specified in this version.

Input: one message. Output: the same message, or nothing.

### 2.1 Assumptions

Each assumption is an obligation of the organization that deploys the guard,
not a requirement on this library. Establishing that an assumption holds
needs evidence about the deployment, not tests of the guard.

- **A-1** A message's security level is assigned before the message reaches
  the guard, and the guard trusts the marking (E-5).
- **A-2** Every message that leaves the enclave is routed through the guard;
  the guard cannot prevent a bypass. (The deployment assumption of A0, now
  labeled.)

## 3. User categories

- **Message sender**: a person or system inside the enclave that produces
  messages and expects the ones that may leave to arrive unchanged. Observes
  which messages arrive outside, and their payloads; observes nothing when a
  message is dropped (E-3).
- **Security officer**: the person responsible for what leaves the enclave.
  Owns the policy that a Critical message never leaves; reads this document
  and the requirements and confirms that they describe the guard that is
  wanted. Observes the specifications; in this version has no record of what
  was dropped (E-2; deferred want D-1).

The developer who builds the guard is not a user category (E-4); the
developer's roles are in `CLAUDE.md`, and the judgments the developer's work is held to are in `process/judgments.md`.

## 4. User stories

Each story is in the words of a stakeholder of the category it names; its
`Source` is the elicitation entry. The story's behavior is verified by test:
the scenarios its header names are run by `tests/test_scenarios.py`, each
citing the story (Scen-CONF-1). Whether the story describes what the
stakeholder wants is a separate question, validated by a walkthrough with a
stakeholder of that category and the sign-off (ConOps-VAL-1).

**US-1** · Method: test · Scenarios: SC-1, SC-2 · User category: message sender · Validated by: walkthrough (human) · Source: E-3

As a message sender, when I send a Public message, I expect it to arrive
outside the enclave unchanged, whatever its payload.

Example: the guard is given a message with level Public and payload 42; it
outputs a message with level Public and payload 42. Given (Public, -3), it
outputs (Public, -3).

**US-2** · Method: test · Scenarios: SC-3, SC-4 · User category: message sender · Validated by: walkthrough (human) · Source: E-3

As a message sender, when I send a Restricted message, I expect it to arrive
unchanged, because in this version a Restricted message is allowed to leave
and its payload is neither inspected nor altered (E-1).

Example: the guard is given (Restricted, 7); it outputs (Restricted, 7).
Given (Restricted, 150), it outputs (Restricted, 150).

**US-3** · Method: test · Scenarios: SC-5, SC-6 · User category: security officer · Validated by: walkthrough (human) · Source: E-1

As the security officer, I need every message whose security level is
Critical dropped at the guard, whatever its payload, so that nothing marked
Critical can leave the enclave.

Example: the guard is given (Critical, 100); it outputs nothing. The guard is
given (Critical, 0); it outputs nothing.

## 5. Deferred wants

Heard during elicitation and recorded here so that they are neither
forgotten nor promised. No requirement, story, or scenario of this version
derives from any of them.

- **D-1** A record of every dropped message, observable by the security
  officer (E-2).
- **D-2** Changing the payload of a Restricted message before it leaves, for
  instance cutting a large payload down (E-1).
- **D-3** A change to whether Restricted or Public messages are dropped;
  that a Critical message is dropped does not change (E-1).

## 6. Sign-off

Validation of this document, by a stakeholder of each user category naming
this version, is recorded in `records/validation.md` under "Sign-off".
