
(seeds / sketches - not necessarily archiving)
plans (project specific)
specifications (specifications for project)
development rules (process rules for the project) (app-independent)
  - quality rules for specs
  - quality rules for artifacts
  - verification rules 
  - process steps
reporting & explaining
development state (current state, wrt plan and specs pending issues) 
  - pending tasks
  - note that this where assurance case would generalize from
project (artifacts)  


How can the above be introduced incrementally
  Phase 1 
    - ConOps
    - specs 
        - behavior
        - technologies ?
    - projects     

  Phase 2
    - Development rules
       - audit rules for ConOps and specifications
       - style rules for tests
       - verification rules (testing to requirements)


Next
 - make summary diagram of concepts
 - summary of kiro artifacts and workflows
 - Process information from Grok
 - Account for the investigate or research phase

## Grok Research

What is constrained	Goals/UX → behavior → interfaces → properties → architecture → process
Authority for agents	Context (prompt/memory) → Gate (CI/tests/types) → External commit (runtime authority)
Forms to walk in lecture:

Informal & structured NL — IEEE/ISO SRS prose, Cockburn use cases, user stories + acceptance criteria, EARS (“WHEN … THE SYSTEM SHALL …”). Best for goals; weak alone as authority.
Semi-formal tables — SCR / Parnas tables, decision tables. More complete than free prose; agents can often compile toward tests/state machines.
Behavioral / model-based — UML/SysML, Harel statecharts (often Mermaid/PlantUML in design.md). Great for humans; hard gates only if generated or model-checked.
Contracts / axiomatic — Hoare triples, Meyer Design-by-Contract. Local gates at module boundaries.
Model-oriented formal — Z, VDM, B/Event-B, Alloy, TLA+/PlusCal. Strong machine checkability; costly for everyday features.
Temporal / property specs — LTL/CTL, runtime monitors. Natural gates on agent trajectories; conceptual kin to SpecHarness/AgentSpec.
Executable specs / BDD / ATDD / TDD-as-spec — Gherkin, Cucumber, Fit/FitNesse. Dual audience: readable and runnable—among the best classical authority mechanisms for agents.
Interface & schema contracts — OpenAPI, JSON Schema, GraphQL SDL, protobuf, AsyncAPI. Hard constraints for codegen; weak on goals alone.
ADLs / structural models — AADL, SysML BDD/IBD. Where code should live; needs tooling for agents.
Types & refinement types — Cheap continuous gates in edit–compile loops; not stakeholder goals.
Traceability pyramids — Vision → epics → stories → acceptance tests → contracts (mirrors Spec Kit / Kiro chains).
Agentic instruction files — AGENTS.md, CLAUDE.md, Cursor rules, SKILL.md, constitutions. Mostly context + soft process (industry practice).
External obligation authority (research) — SpecHarness, AgentSpec,
GitHarness. Specs as commit boundary, not just prompt fodder.

Narrative (lecture-ready)
Driving question. What forms of specification let a human understand what should be built and also steer and check coding agents?

Software engineering has never had a single “specification.” It has had a family of notations and artifacts whose purpose is to constrain development so that intent survives implementation. Agentic coding does not invent that family; it makes the old trade-offs newly urgent. Language models are strong at pattern completion and weak at mind-reading. Vague prompts force unstated requirements to be invented. Conversely, when a rich Markdown “spec” is loaded into the same model that later declares completion, the specification never becomes an independent authority—only more context. The lecture’s payoff is a taxonomy that separates (a) forms that communicate goals to humans and agents, (b) forms that machines can check, and (c) authority models that decide who may say “done.”

Classical backbone. Informal requirements remain foundational. IEEE 830–era SRS templates and their successors in ISO/IEC/IEEE 29148 organize stakeholder-facing prose: purpose, scope, functional and non-functional requirements. Use cases (Cockburn) and agile user stories with acceptance criteria shift discourse from system features to actor goals. These forms excel for understanding goals; they are weak as sole agent directors because ambiguity is a feature of natural language. Practice therefore introduced structure without full formality: EARS (Mavin et al.) constrains shall-statements into event/state/unwanted-behavior patterns—now reused in Amazon Kiro’s requirements artifacts. Parnas’s documentation thesis and SCR-style tabular methods treat requirements as relations over monitored and controlled variables, using tables to expose incompleteness. Decision tables play a similar role for combinatorial business rules. For agents, tables are attractive because they are both human-scannable and closer to executable decision procedures.

Behavioral modeling occupies the next band. UML/SysML and Harel’s statecharts give shared pictures of interaction, sequencing, and hierarchical modes. In agentic workflows these often reappear as Mermaid/PlantUML in a design.md: still primarily context, unless linked to code generation or model checking. Axiomatic and contractual thinking—Hoare’s triples and Meyer’s Design by Contract—relocates specification to module boundaries: preconditions, postconditions, invariants. That relocation matters for agents: a contract is a local gate the implementation must respect, readable by developers and often checkable by assertions or static analysis.

Model-oriented formal methods (Z, VDM, B/Event-B, Alloy, TLA+) push checkability further. Jackson’s Alloy emphasizes lightweight relational modeling and counterexamples; Lamport’s TLA+ emphasizes temporal properties of concurrent/distributed systems; Abrial’s B/Event-B emphasize refinement from abstract machines to implementations. Temporal logics (LTL/CTL) and runtime verification supply property specs over traces—conceptually continuous with modern agent-trajectory monitors. These forms are superb for teaching “the spec can be the truth,” and for directing agents on narrow, high-stakes fragments; they are rarely the everyday steering surface for feature work.

Executable specifications close the classical loop. Behavior-Driven
Development (North; Cucumber/Gherkin) and the Fit/FitNesse lineage
make examples both documentation and automated acceptance tests. TDD
inverts the same idea at unit scale: the failing test is a
specification fragment. Interface contracts—OpenAPI, JSON Schema,
GraphQL SDL, Protocol Buffers, AsyncAPI—specify shapes of messages and
APIs with immediate validation and codegen utility. Refinement types
enrich ordinary type systems with predicates, giving continuous
lightweight proof obligations. Architecture Description Languages
(e.g., AADL) and SysML structural diagrams constrain allocation and
interfaces at system scale. Across this classical landscape, a
recurring pattern appears: human-readable goal specs at the top;
machine-checkable gates (tests, types, schemas, model checkers)
underneath; traceability binding levels so neither humans nor tools
lose the thread.


Modern agentic SDD. Industry practice in 2025–2026 revived “spec-driven development” as a reaction to vibe coding. GitHub’s Spec Kit makes Markdown artifacts the process center: a constitution of standing principles; specify (what/why, user journeys); plan (stack and constraints); tasks (reviewable chunks); implement; converge (assess remaining work against spec/plan/tasks). Specs are framed as living and “executable” in the sense that agents derive code from them—not necessarily in the classical formal-methods sense. Amazon Kiro institutionalizes a three-file feature spec—requirements.md (often EARS + stories), design.md, tasks.md—with explicit human review gates between phases. The portable AGENTS.md convention is a README-for-agents: build/test commands, conventions, security notes—nested per package. Sibling files (CLAUDE.md, Cursor rules, Copilot instructions, SKILL.md) play the same role with tool-specific scoping. OpenSpec and related community tools emphasize change proposals as diffs against current specs (brownfield-friendly). Short courses (e.g. DeepLearning.AI / JetBrains) now teach constitutions and plan–implement–verify loops as pedagogy—SDD as named industry methodology, not yet settled peer-reviewed theory.

The authority gap. Research in 2025–2026 sharpens a distinction industry toolkits often leave implicit. SpecHarness (Li et al., arXiv:2609.29921) argues that when task instructions, guidelines, schemas, and SKILL.md files remain context for the same model that acts and self-evaluates, two gaps appear: understanding–execution (requirement understood but not satisfied) and state–authority (completion claimed without establishing required state). On SkillsBench, agents satisfied only ~80–86% of source-grounded directions extracted from visible materials, while completion-claim rates exceeded official pass rates by ~29–38 percentage points. SpecHarness’s principle: agents may propose; only admissible evidence from qualified providers may commit specification-governed state. AgentSpec (Wang, Poskitt, Sun; ICSE 2026) provides a complementary DSL—trigger, check predicates, enforce (stop, user inspection, corrective action)—for runtime mediation. GitHarness (Yang et al., arXiv:2609.36789) treats evolving requirements as first-class versioned memory paired with harness work state, so requirement shift need not force global rewrite. Together: specs as context vs specs as gates vs specs as external commit authority.

Teachable synthesis — prefer forms by what must be true for agents:

Discover goals → NL stories, use cases, EARS, Spec Kit specify / Kiro requirements (context-heavy, human-first).
Encode standing policy → constitution, AGENTS.md, ADRs (persistent context).
Shape structure & protocols → design.md diagrams, OpenAPI/AsyncAPI, Alloy/TLA+ for hard concurrency (mixed context + gates).
Make “done” checkable → Gherkin/CI, types/contracts, schema validators, property tests (gates).
Govern untrusted autonomy → runtime obligation ledgers / AgentSpec-style enforcement (external authority).
Multi-level pyramids remain the practical glue. Classical SE already knew that documentation without verification drifts; agentic SE rediscovers that prompts without authority drift faster.

Caveats. Much of “modern SDD” is vendor documentation and engineering
blogs—primary sources for practice, weaker as theory. Formal methods
citations are peer-reviewed or standard textbooks.
SpecHarness/GitHarness/AgentSpec are research proposals with stated
scopes. Label industry vs research clearly for students.




## Kiro Summary

Three primary files: 
- requirements.md (or bugfix.md) - Captures user stories, acceptance criteria, or bug analysis in structured notation
- design.md - Documents technical architecture, sequence diagrams, and implementation considerations
- tasks.md - Provides a detailed implementation plan with discrete,
trackable tasks

All specs follow a three-phase workflow that transforms your idea into executable implementation:

Requirements or Bug Analysis - Define what needs to be built or fixed
- Feature Specs: User stories and acceptance criteria in requirements.md
- Bugfix Specs: Bug analysis with current/expected/unchanged behavior in bugfix.md

Design - Create technical architecture and implementation approach in design.md
- System architecture and component design
- Sequence diagrams and data flow
- Error handling and testing strategy

Tasks - Generate discrete, executable implementation tasks in tasks.md
- Trackable tasks with clear outcomes
- Real-time status updates as you implement
- Run tasks individually or all at once

### Analyzing Requirements

Requirements are Kiro are written in the EARS structured natural
language format.

The [Kiro documentation](https://kiro.dev/docs/specs/analyze-requirements/)
states the following rules/criteria for analyzing requirements.

- Logical inconsistencies - two requirements that individually make sense but are collectively impossible
- Ambiguities - language like "large files" or "fast response times" that would produce divergent implementations
- Conflicting constraints - functional and non-functional requirements that can't all be satisfied at once
- Unstated assumptions - references to undefined concepts or behaviors
- Missing edge cases - failure modes, boundary conditions, and
concurrent access scenarios not covered by the happy path

### Testing

Kiro emphasizes [property-based
testing](https://kiro.dev/docs/specs/correctness/#workflow) 

### Steering

Kiro uses the term ["steering files"](https://kiro.dev/docs/steering/)
to refer to files that define development rules and that provide other
information about your project.

Kiro provides core project steering files to establish core project
context.  These files are always loaded into the context.

- Product Overview (product.md) - Defines your product's purpose, target users, key features, and business objectives. This helps Kiro understand the "why" behind technical decisions and suggest solutions aligned with your product goals.

Note: This seems similar to ConOps

- Technology Stack (tech.md) - Documents your chosen frameworks, libraries, development tools, and technical constraints. When Kiro suggests implementations, it will prefer your established stack over alternatives.

- Project Structure (structure.md) - Outlines file organization, naming conventions, import patterns, and architectural decisions. This helps generated code fit your existing codebase.

These foundation files are included in every interaction by default, forming the baseline of Kiro's project understanding.

Kiro identifies the following additional steering files (under the
heading of [Steering File
strategies](https://kiro.dev/docs/steering/#common-steering-file-strategies).
For each of these you can define an inclusion policy to determine when
they are loaded into the agent context.

- API Standards (api-standards.md) - Define REST conventions, error response formats, authentication flows, and versioning strategies. Include endpoint naming patterns, HTTP status code usage, and request/response examples.

- Testing Approach (testing-standards.md) - Establish unit test patterns, integration test strategies, mocking approaches, and coverage expectations. Document preferred testing libraries, assertion styles, and test file organization.

- Code Style (code-conventions.md) - Specify naming patterns, file organization, import ordering, and architectural decisions. Include examples of preferred code structures, component patterns, and anti-patterns to avoid.

- Security Guidelines (security-policies.md) - Document authentication requirements, data validation rules, input sanitization standards, and vulnerability prevention measures. Include secure coding practices specific to your application.

- Deployment Process (deployment-workflow.md) - Outline build procedures, environment configurations, deployment steps, and rollback strategies. Include CI/CD pipeline details and environment-specific requirements.


### Skills

Skills are portable instruction packages that follow the open Agent
Skills standard. They bundle instructions, scripts, and templates into
reusable packages that Kiro can activate when relevant to your task.


### Workflows

Under the hood a workflow is a graph: agent steps, sequences, loops, and parallel branches in a format both you and Kiro can read and write. You can understand most recipes through five ideas:

IDEA	MEANING

Step	One agent runs in its own session with focused context. A step cannot read another step's session; it receives earlier results only through explicit handoffs
Handoff	Captured output or a declared artifact passes evidence to a later step
Branch and join	Independent agents evaluate the same work, then a policy combines their outcomes
Loop	A group of steps repeats until evidence matches a condition or a safety cap is reached
Wait	The run watches an external system, a pull request or anything a script of yours can check, without spending model turns while nothing changes
The parent chat and each step stay connected in both directions. A step reports outward with a send_message signal that carries progress, a question, or its outcome. You can steer a running or paused step at any time; see Respond when a step needs input.

With those five ideas in hand, the figure below traces one run from
the parent chat: launch, steps in their own sessions, a review loop,
artifacts returning, and the main agent synthesizing the result. Both
channels stay open the whole time, so you can keep talking in the
parent chat and steer a selected step while it runs.


## Kiro Workflow examples

https://kiro.dev/docs/workflows/patterns/




