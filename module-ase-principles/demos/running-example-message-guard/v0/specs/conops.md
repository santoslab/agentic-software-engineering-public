# Concept of Operations: Message Guard (version A0)

Version A0. The three user stories carry identifiers and verification
methods. The purpose, scope, terms, and user-category descriptions provide
context for interpreting them and are reviewed with them. The requirements
derived from the stories and terms are in `requirements.md`. Stakeholder
sign-off is recorded separately in `reports/walkthrough.md`.

## 1. Purpose

An organization keeps a protected enclave whose systems produce messages of
differing sensitivity, and it needs some of those messages to reach a less
trusted network outside the enclave. The message guard sits on that boundary
and decides, one message at a time, whether a message may leave. Deployment
assumption: messages leaving the enclave are routed through the guard;
preventing bypass is outside this library's scope.

In this version the decision rests on one thing, the security level marked on
the message: a message marked Critical never leaves, and every other message
leaves exactly as it arrived. Later versions will sanitize what leaves, record
what was stopped, and let the security officer change the policy. This version
establishes the guard itself, and the way its behavior is specified and shown
to hold.

## 2. Scope and system boundary

The guard is a library: a function that takes one message and returns either
that message or nothing. Inside the boundary is the decision to pass or drop a
message. Outside it are the transport that carries messages to and from the
guard, the authentication of senders, the assignment of security levels, any
record of what was dropped, and any change to a message's payload.

Input: one message. Output: the same message, or nothing.

### Terms

- **message**: the unit of data that crosses the boundary: a security level and
  a payload.
- **security level**: the marking that says how sensitive a message is; exactly
  one of Public, Restricted, or Critical, in increasing sensitivity.
- **payload**: the content of a message; in this version a single integer,
  which the guard does not inspect.
- **pass**: the guard outputs the message, unchanged.
- **drop**: the guard outputs nothing for the message.
- **filter**: the stage of the guard that passes or drops a message by its
  security level. In this version the guard is the filter alone.

## 3. User categories

- **Message sender**: a person or system inside the enclave that produces
  messages and expects the ones that may leave to arrive unchanged. Observes
  which messages arrive outside, and their content.
- **Security officer**: the person responsible for what leaves the enclave.
  Owns the policy that a Critical message never leaves; reads this document and
  the requirements and confirms that they describe the guard that is wanted.
  Observes the specifications, and in later versions the record of what was
  stopped.

## 4. User stories

Each story is verified by a walkthrough: a person, in the role the story names,
gives the guard the story's example message and judges what they observe. The
record is `reports/walkthrough.md`.

**US-1** · Method: walkthrough (human) · User category: message sender

As a message sender, when I send a Public message, I expect it to arrive
outside the enclave unchanged.

Example: the guard is given a message with level Public and payload 42; it
outputs a message with level Public and payload 42.

**US-2** · Method: walkthrough (human) · User category: message sender

As a message sender, when I send a Restricted message, I expect it to arrive
unchanged, because in this version a Restricted message is allowed to leave.

Example: the guard is given (Restricted, 7); it outputs (Restricted, 7).

**US-3** · Method: walkthrough (human) · User category: security officer

As the security officer, I need every Critical message stopped at the guard,
whatever its payload, so that nothing marked Critical can leave the enclave.

Example: the guard is given (Critical, 100); it outputs nothing. The guard is
given (Critical, 0); it outputs nothing.

## 5. Sign-off

Validation of this document, by a stakeholder of each user category naming
this version, is recorded in `reports/walkthrough.md` under "Sign-off".
