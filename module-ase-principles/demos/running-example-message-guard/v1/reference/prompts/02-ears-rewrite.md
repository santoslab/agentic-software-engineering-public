# Retained prompt: the EARS rewrite of the requirements (task 5)

Typed to the agent after `/elicit` had revised the concept of operations and
written the glossary, and before the audit. Kept as reference (rule WF-2's
record discipline applied to prompts): it is what the agent was told, not a
specification.

> Read `specs/glossary.md`, `specs/conops.md`, and `specs/requirements.md`.
> Rewrite the four requirements REQ-0 to REQ-3 in EARS form. Keep every
> identifier, every `Method:` value, and every `Derived from:` reference as
> they are; the Terms section has moved to the glossary, so REQ-0's
> derivation becomes `Glossary: message, security level, payload`. Add a
> `Pattern:` field to each header naming the EARS pattern you used
> (ubiquitous, event-driven, state-driven, unwanted-behavior,
> optional-feature, or complex). The subject of every sentence is "the
> filter" or "the guard", the verb is "shall", and every domain term is one
> the glossary defines, used in its defined sense. Do not change what any
> requirement requires: REQ-1 to REQ-3 must still assign each security level
> the same outcome as before. Show me the four rewritten clauses and stop;
> do not edit any other file.

What the agent returned became the draft of `specs/requirements.md` that
the audits of task 6 examined, after the gaps of the A1 plan's section 6
were seeded into it (`reference/drafts/requirements.md`).
