> Design response (2026-10-18): see `running-example-design.md` for the endorsed example, the five development-state judgments, four candidate progressions, the canonical list of specification forms, and the proposed glossary changes.

## Prompt

I want to develop a running example to present the basic concepts for
agentic software engineering.  One important goal is get students to
understand agent-based coding as an "engineering discipline", i.e.,
repeatable processes, leading to measurable quality, the ability to
discover and assess problems with both systems and the processes by
which they are developed and make improvements in both.   We want the
students to distinguish "agentic software engineering" from "vibe
coding".   With "agentic software engineering", we want to develop a
system development approach in which humans (and external auditors)
can maintain their understand of the system (they don't need to
understand every line of code, but they should understand all
specifications, the means by which code is demonstrated to conform with
a specification, and the current status of such conformance). 

The example should illustrate basic
concepts of
  - human intent, specification, realizations.  In particular, we want
    successive versions of the example to illustrate different forms
    of specifications (e.g., those presented in `specification-implemention.md` and perhaps more).  For each style of specification, we want to illustrate a
    corresponding realization along with mechanisms for evaluating if the 
    realization conforms to the specification (this is an example of a
    development state judgement discussed below). 
  - planning and work decomposition into discrete tasks, logical waves
    (groups) of tasks that produce development phases with outcomes
    that developers can easily digest and review before proceeding to next
    steps.  We want to illustrate notions of gating for important
    tasks or ending states of waves
  - development process rules (governance).  We want to illustrate
    basic development process (governance) rules.  These rules should
    illustrate how rules can be step of to achieve the following..
      - organized commits of the results of development tasks
      - organized evolution of specifications and realizations so that
      relationships (judgements) on specifications, realizations, and
      relationships between specifications and realizations are
      maintained as invariants (perhaps not at each commit, but at the
      end of waves and at other crucial task completions)
  - reporting aiming to support human understanding of the development
    state.  This may include task lists (both completed and pending)
    as well as assurance "ledgers" that indicate at each commit 
    the current truth of declared development state judgements 

## Development State Judgements

Judgements on the development state are crucial elements of the
running example.  Initially (within the first several versions of the
running example the following notions development state judgements
must be present):
  - specification quality rules - there should distinction
    recognizable artifacts or rules/material within markdown files
    that describes various quality rules on specifications.  That
    include
      - unambiguous
      - consistent
      - any notion of syntactic correctness or syntactic
        well-formedness, e.g., for structure natural language
        requirements or syntactic correctness for formal
        specifications
    The tic-tac-toe example 
    `module-software-engineering/demos/lecture-03-game-demo/starter/process/spec-audit.md` 
    contains some examples.
    Note that specification quality rules make speak to single
    specifications or that may speak to relationships between
    specifications (e.g., requirements are consistent with user
    stories).
    An important specification is the glossary of terms (a simple
    example of a "domain model") which aims to establish a common
    vocabulary across the development artifacts
  - realization/implementation quality rules
      - code compiles, 
      - passes linters or other static analysis tools
      - passes tests
      - has appropriate architecture and abstraction
  - realization conforms to specification(s) (verification) and mechanisms for
    demonstrating that specifications conform to realizations
      - example: an code is demonstrated to conform to a specification
        via testing 
  - specifications conform to human intent (validation)
  - traceability - the notion of traceability is an overarching
    concept that must be emphasize throughout all artifacts.  That
    means that the artifacts themselves need to be designed to have
    appropriate identifiers or markers that enable one point in an
    artifact (e.g., a test case in a test suite) to be traceable to a
    requirement.
    
## Development Process Rules

We want the development process to be organized in such a way to
support human understanding.  In the process, specifications serve as
abstractions or summaries of the realization (and perhaps other
lower-level specifications that help humans understand the system).

The development process should main different artifacts that support
audits by humans other other agents including..
  - development logs that indicate what was accomplished in particular
    ways or commits
  - an assurance "ledger" that indicates the current state of
    development state judgements at a particular commit.

## Things to Watch Out For

I tried introducing some of these concepts systematically in the game
(tic-tac-toe) example and associated lecture and in the PKB project.
But things were not introduced in a systematic way.  Moreover, **too
much was introduced at once**.  For example, in the starter files for
the game-demo, I gave the students example development rules and
specification audits, etc.   But this was too much for them to consume
in one go (I estimate they would need 60-70% of the material).
Moreover, the content wasn't organized as well as it could be.  I
would like the the development rules to clearly be organized in
different categories, or notions of specification quality to be
clearly recognizable using that term, for the notions of what it means
for a realization to conform to a specification be clearly
recognizable.

## Different Forms of Specification

As the example unfolds, I want it to gradually introduce different
forms of specification (for example, see
`specification-implementation.md`).  We may expect 2-3 lectures where
the running example grows by adding features that lead to new
specification forms being illustrate.

For example, 
- an initial example might illustrate a simple conops (system scope,
  user categories, and user stories for each user category) and system
  requirements
- a subsequent lecture might introduce data specifications and notions
  of architecture specifications in contraints
- a subsequent lecture might introduce notions of state machines and
  message sequence charts etc.    

To support the above, I want to work with you to develop a canonical
list of specifications forms that we aim to cover in the course.   For
specification form, students should understand (a) in what types of
situations is the particular specification appropriate, (b) what are
the mechanisms by which one demonstrates that a realization (e.g.,
code or lower-level specifications) satisfies the given specification,
and (c) what are the expected notions of alignment or consistency
between that specification and other forms of specifications.

## Alignment with Other Artifacts

In addition to other material in this repository, I am trying to align
with abstract models of a development process being developed for
other purposes.  For example, in
`/Users/hatcliff/Dev/Lean/AgenticDev`.  You should not regard
`AgenticDev` as the ultimate "truth".  WHy not? It's current notions
are very abstract and many things that I have mentioned above are not
present in that model.  In addition, I may want to evolve that model
to make it align with the running example that we work on?

In this repo, the most important things to try to align on are the 
glossary `glossary.md` and the drafty concepts in
`specification-implementation.md`

## Desired Outcomes

- Student should understand all concepts in the glossary, they should
  be able to see examples of these concepts in the course material

- Students should understand the key elements of a generic spec-driven
  development process for agentic software engineering.  They should
  see these concepts illustrated in course materials, and they should
  be able to apply them to their own systems.  

- Students should be able to scale up the concepts here to bigger
  systems.


## Criteria for example

- The example should start off with programming languages and dev
  tooling that they are familiar with and are easy to install (e.g.,
  basic Python with accompanying tools like pytest and some simple
  Python linters)


## Possible ideas for an example

I will give a suggestion below, but we are not tied to my suggestion.
If you think it is not appropriate, or there is a better example let
me know.

My suggestion: - a simple library that support "message filtering and
"transformations".  Why do I propose this?
  - the data formats for messages can start with something extremely
    simple (but can later scale up and included different types of
    data formats that have standardized specifications, code
    generators (e.g., for parsing, serializing), and well-formedness
    checkers).
  - the notions of functions involved (check if a message has this
    feature, do not forward a message that has a certain feature, 
    transform a message to replace the contents of a particular field
    with a new value) are all very localized.  The functions can be
    flexibly arranged into different architectures (strict pipeline, 
    "parallel" processing of independent filtering, transforming, with
     merges, etc. )

Some inspiration might come frome
`/Users/hatcliff/Dev/git-repos/hamr-agent-context-git/examples/HAMR-SysMLv2-Rust-seL4-P-EDP-SNG-Example'
The idea is that the two different components in that example (Gate,
Filter) could be represented by two python functions.  The message
data structure in that example could also be represented in a very
simple way in Python.  Composition of components like these could be
presented by a top-level python file that successively calls, e.g.,
the filter, then the gate.

The first iteration of the sample could have
 - Simple ConOps that identifies scope of system (a message processor
   or simple "firewall"), user stories describe example imput messages
   and expect outputs
 - Simple requirements would indicate drop/pass conditions  
 - Simple architecture contraints indicate that steps in processing a
   message are to be organized in discrete stages (like gate, filer,
   and then composed)  (or this could be done in a subsequent step)
 - Simple data spec (informal / adhoc - not using a standard message
   format library)
 - Specification quality 
      - no inconsistent rules
      - alignment between ConOps user stories and requirements
 - Realization quality 
      - passes python linter
      - passes tests
 - Conformance
      - test suite demonstrating implementation behavior conforms to
        requirements and ConOps user stories

When in doubt, *simplify* - we want the concepts to be easily fit in
lectures.  The students will be work on exercises and homeworks that
apply the concepts to different examples.

Subsequent steps that expand the example
  - Using skills to organize the different audit concepts
    (specification quality, realization quality, conformance)
  - Developing specific reports and other features to understand
    status of development and status of assurance.
  - Things to illustrate designing of specific development process or
    governance rules that recognize the notions of human audits as
    gates, satisfication of development artifact judgements as gates  
  - Illustrating each style of specification and
    specification/realization conformance checking (following our list
    of canonical specifications).
       - For example, 
            - a state machine might be used to check for some notion
              of ordering on messages received (i.e., some basic
              protocol) 
              (e.g., first we receive a message of this type, then we
              must receive a message of this type)
            - introduction standard message type with an IDL like
              specification and associated code generation
              
                


   