# Music integration evidence template

Replace placeholders with your observations. Never invent calls or include passwords.

## Connection checkpoint

- Date, host/model version, OS, database version/edition, provider version:
- Fixture identity and manifest hash:
- Readiness counts and check command:
- Sanitized project configuration and discovered tool names:
- Actual status and any unresolved setup issue:

## Schema

Prompt, actual schema-tool name/arguments, relevant returned schema, diagram,
and your explanation of Playlist → Track → Artist. Explain IDs vs names.

## Question A

Exact question/prompts; proposed Cypher and review; actual tool name/arguments;
returned rows; final answer; your explanation of DISTINCT and tie ordering.
Preserve any mistake/correction.

## Question B

Same evidence, including the P01 exclusion and definition of shared track.

## Independent verification

Query run directly in Query; returned rows; field-by-field comparison with the
agent result; interpretation of agreement/disagreement; what replay cannot prove.

## Ambiguity and diagnosis

Two meanings of popularity; precise supported choice; data missing for another
choice. One observed or supplied failure, its layer, and next check.

## Reflection

Agent assistance used; what you verified yourself; remaining uncertainty.
If analyzing instructor captures because live access failed, label that path
explicitly and include the setup diagnostic for a later live check.
