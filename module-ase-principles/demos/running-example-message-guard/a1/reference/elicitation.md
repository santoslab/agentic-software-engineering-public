# Elicitation Record: Message Guard (version A1)

Reference material, not a specification; the record that procedure Elicit leaves. Each entry is one
question put to a stakeholder and the answer in their words. Stories, terms,
assumptions, and deferred wants of `specs/conops.md` and `specs/glossary.md`
cite entries by identifier. No judgment of the development state is about
this file, and it is not audited.

Session 2026-10-22 · asked by: the agent running `/elicit` 1.0 on the A0
concept of operations (the queue is the one the skill produced in evaluation
run 2; all three evaluation runs are recorded on `tooling/skill-elicit.md`)
· answered by: the build agent playing both roles, giving the stakeholder
answers scripted in the A1 plan (section 5.5). As in A0's sign-off, one
person plays both roles; the instructor can re-run the session live, and a
live answer that differs from a scripted one is recorded as a new entry,
never edited into an old one.

### E-1 · to the security officer

Question: Is the rule that a message marked Critical never leaves meant to
hold permanently, in every version of the guard, or is it the current
setting of a policy that you expect to be able to change later?
Why it matters: a permanent rule keeps US-3 as it stands in every version
and narrows the later "let the security officer change the policy" to the
other two levels, while a changeable setting makes US-3 a statement about
this version only.
Options: A. permanent; what may later change is whether Restricted or Public
messages leave (recommended) · B. a current setting; a later version may let
some Critical messages leave · Short.
Answer (verbatim): "A. Critical never leaves, full stop. The marking alone
decides; we don't look inside the message in this version. If anything
changes later it's what happens to the other two levels, and I may want
large Restricted payloads cut down before they go out. That's later."
Answered by: the security officer (role played by the build agent), 2026-10-22
Consequences: purpose, second paragraph (the decision rests on the marking
alone; the payload is not inspected); US-3 reworded as "every message whose
security level is Critical ... whatever its payload"; US-2 ("neither
inspected nor altered"); deferred wants D-2 and D-3.

### E-2 · to the security officer

Question: Of the three things this document says later versions will do,
removing sensitive parts from messages before they leave, keeping a record
of what was stopped, and letting you change the policy, which are things you
actually want?
Why it matters: the "later versions will" sentence becomes a list of wants
recorded as deferred, each with its owner, so that none is built or required
before a stakeholder has asked for it, and anything you do not want is
removed from the document.
Options: A. all three are mine, deferred (recommended) · B. the record and
the policy change are mine; sanitizing is not · C. only the record · D. none;
they are the developers' plan · Short.
Answer (verbatim): "A, all three are mine. The record of what was stopped
I'd like eventually; it's not needed for this version. Don't build any of
it now."
Answered by: the security officer (role played by the build agent), 2026-10-22
Consequences: the "Later versions will ..." promise removed from the purpose;
section 5, deferred wants D-1, D-2, D-3, owned by the security officer; the
security officer's "observes" line (no record of what was stopped in this
version).

### E-3 · to the message sender

Question: When a message you send is stopped at the guard, do you want to be
told that it was stopped?
Why it matters: "yes, in this version" adds a story and changes what the
guard gives back for a stopped message, "later" is recorded as a deferred
want, and "no" is recorded so that no notification is ever required of the
guard on the sender's behalf.
Options: A. no; a stopped message simply does not arrive (recommended) · B.
not in this version, but eventually · C. yes, in this version · Short.
Answer (verbatim): "A. No. It just doesn't arrive, and I may not even know.
What I care about is that anything I send that is allowed out comes out
exactly as I sent it, whatever the number in it, Public or Restricted."
Answered by: a message sender (role played by the build agent), 2026-10-22
Consequences: the message sender's "observes" line (observes nothing when a
message is dropped); glossary entry *drop* (the sender is not told); US-1
and US-2 reworded in the sender's words, with "whatever its payload" and the
second example of each.

### E-4 · to the security officer

Question: Besides the message sender and yourself, should anyone else, for
instance the people or systems on the outside network that receive what the
guard lets through, or the person who puts the guard in the path of outgoing
messages, be written down as a user of the guard with expectations of their
own?
Why it matters: each added category needs its own story and a line saying
what it observes, and if none is added the document will say who is not a
user.
Options: A. no one else; the document says so (recommended) · B. the outside
recipient, with a story · C. the person who installs the guard, with a story
· D. both · Short.
Answer (verbatim): "A. No one else. The people outside get what the sender
sent; that's the sender's story. The developer is not a user of the guard."
Answered by: the security officer (role played by the build agent), 2026-10-22
Consequences: section 3, the sentence that the developer is not a user
category; no category added.

### E-5 · to the security officer

Question: Should the guard take the security level marked on a message as
correct, so that marking every message correctly before it reaches the guard
is the organization's responsibility rather than the guard's?
Why it matters: the answer decides whether the scope section states, as an
obligation on the deploying organization, that every message reaching the
guard is already and correctly marked, or whether the guard's boundary grows
to include some check of the marking.
Options: A. yes; the guard trusts the marking, and correct marking before
arrival is the deploying organization's obligation (recommended) · B. yes,
and anything arriving without one of the three markings is stopped · C. no;
the guard checks the marking itself · Short.
Answer (verbatim): "A. Yes. It's marked before it gets to the guard, and the
guard trusts the marking. That's on us, not on the guard."
Answered by: the security officer (role played by the build agent), 2026-10-22
Consequences: assumption A-1 in section 2.1; glossary entry *security level*
(assigned before the message reaches the guard).

## Not asked

Candidates the skill excluded, with its reason, kept because a reader of the
concept of operations may wonder why they are not here:

- Whether Restricted messages should also be stopped: answered by the
  repository (US-2 and the A0 sign-off, "anything else leaves as it
  arrived"). Only a declared change of mind reopens it.
- What the guard does with a marking outside the three, or a payload that
  is not a whole number: answered by the repository (REQ-0, which the tests
  enforce at construction). The residue, how a malformed input is signaled
  and whether a programming language's booleans count as integers, is an
  implementation matter; the glossary entry *payload* records that the
  specification leaves the language-level representation open.
- Whether "unchanged" includes the marking: answered by the examples of
  US-1 and US-2 and by REQ-2.
- Ordering, batching, and transport: answered ("one message at a time";
  transport outside the boundary) or implementation.
- Who agreed to the purpose statement and when: answered by the A0 sign-off;
  re-agreed for A1 in this session (E-1, E-3).
- Which deferred want to build first: task order, outside elicitation.

Assumption A-2 (routing through the guard) was not elicited: it is A0's
deployment assumption, now labeled. The scope section's statement that each
call is independent and the guard keeps no state between messages was not
elicited either: it describes the guard, not the deployment, which is why
audit 02 moved it out of the assumptions.
