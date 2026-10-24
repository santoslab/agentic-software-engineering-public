# Glossary: Message Guard (version A1)

Version A1. The domain terms of the message guard, each defined once. Every
specification of this system uses these terms in the sense given here and
defines none of them itself (Gloss-SQ-1). Entries are alphabetical; a term in
**bold** inside a definition is itself an entry. The terms come from the
Terms section of the A0 concept of operations and from elicitation
(`reference/elicitation.md`, cited as E-n).

- **drop**: the **guard** outputs nothing for a **message**. Nothing else
  happens in this version: no record is kept, and the **message sender** is
  not told (E-2, E-3).
- **enclave**: the protected network whose systems produce messages; the
  **guard** sits on its boundary.
- **filter**: the **stage** of the **guard** that passes or drops a
  **message** by its **security level**. In this version the guard is the
  filter alone.
- **guard** (message guard): the library that takes one **message** and
  returns either that message or nothing; the system these specifications
  describe.
- **message**: the unit of data that crosses the boundary: a **security
  level** and a **payload**. A message does not change after it is created.
- **message sender**: a user category: a person or system inside the
  **enclave** that produces messages.
- **output**: what the **guard** returns for one **message**: the message,
  or nothing.
- **pass**: the **guard** outputs the **message** **unchanged**.
- **payload**: the content of a **message**; in this version a single
  integer, which the **guard** does not inspect. The specification does not
  constrain how a programming language represents integers (not elicited:
  see "Not asked" in `reference/elicitation.md`).
- **security level**: the marking that says how sensitive a **message** is;
  exactly one of Public, Restricted, or Critical, in increasing sensitivity.
  It is assigned before the message reaches the **guard** (assumption A-1).
- **security officer**: a user category: the person responsible for what
  leaves the **enclave**, and the owner of the policy that a Critical
  message never leaves.
- **stage**: one step of the **guard**'s processing; in this version there is
  one, the **filter**.
- **unchanged**: of an **output** message, having the same **security
  level** and the same **payload** as the input message.
