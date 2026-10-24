# Coverage taxonomy for a concept of operations (`conops`)

Rate each category Clear, Partial, or Missing. A category is Clear when a
reader who had never met the stakeholders could answer its questions from the
document alone. Partial means the document gestures at it; Missing means it
is silent. Only Partial and Missing categories produce candidate questions,
and only when a stakeholder's answer would change the document.

| Category | Clear when the document says |
|---|---|
| **Purpose** | what the system is for, in one or two paragraphs; what single decision or service it provides; who agreed to this statement and when |
| **Scope and boundary** | what comes in and what goes out; what is explicitly outside the system (transport, authentication, assignment of inputs, records kept elsewhere); what the system does not inspect or change |
| **Assumptions** | what the system assumes of its environment, each labeled as the deploying organization's obligation rather than a requirement on the system |
| **User categories** | who the users are, by role, with what each one observes of the system's behavior; who is *not* a user (for instance, the developer) |
| **Stories** | at least one story per user category, in the user's words, each with a concrete example whose expected outcome a reader could check |
| **Terms** | every domain word used in one sense and defined once; no unquantified adjective ("sensitive", "large", "promptly", "secure") standing where a definition or a number is needed |
| **Wants and non-goals** | things a stakeholder has mentioned wanting that this version does not promise, recorded as deferred, so that they do not leak into the requirements |
| **Validation** | which stakeholder can say whether this is the system they want, and on which version of the document |

Not in the taxonomy, on purpose: implementation, technology, data layout,
performance targets, and task breakdown. Those are decided later, by other
specifications, and a stakeholder is not the person to ask.
