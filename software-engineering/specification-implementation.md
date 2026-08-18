# Specifications and Realizations 


## Definitions of Specification and Realization

Many of the agentic software engineering principles that we introduce are related to the concepts of *specification S* and a *realization R of S* (instead of using the term "term" realization, we can often say "implementation" without going wrong).  

- A specification S documents the abstract properties of some item that you are using (or *aiming* to build or use) in your engineering activity. 

- A realization R of S is an engineered item that satisfies the properties given in S.

These definitions are fairly abstract.  Examples of the specification/realization concept will help understand it better.  When we look at each of these examples, we want to consider the following questions:
- how is the specification more abstract (contains fewer details) than the realization? what information is present in the specification verus what is (purposefully) omitted?
- what is the nature of the properties captured in the specification?
- what does it mean for the specification to be well-formed (internally consistent) and how could we check that?
- what are ways that we assess if the realization R conforms to (satisfies) the properties of S?  What are the possible gaps in our confidence about R actually conforming to S?

## Examples of Specifications and Realizations

**Example: Requirements (specification) and an executable system (realization)**  This is the most well-known example of concept in software engineering.  Requirements capture abstract properties of system (e.g. it's desired functional behavior) and when we execute the system we observe the functionality documented in the requirements (we hope!)
- the specification is more abstract because it only indicates the desired behavior (i.e., if the system is given input value *a*, it outputs value *b*).  It does not indicate what algorithm is used to obtain *how* *b* from *a*, it does not indicate what programming language is used to implement the algorithm, etc.
- many of the properties in a typical requirements document are *functional*, describing the desired relationships between the systems inputs and outputs, or how the state of the system changes upon certain events. 
- the most common way to assess the conformance of system to the requirements is via testing (i.e., we experiment with the system).  In a single test, we supply a chosen input, execute the system on the input, and check if the output matches the desired functionality indicated in the requirements.  In general, the more experiments we perform the more confidence we have in the conformance.  However, because it is generally infeasible to test the system against all possible inputs, we cannot be completely confident that we have compliance.  We can increase or confidence if we somehow reason that test suite is "good" in that it "sufficiently" addresses all the functional relationships described in the requirements.

**Example: Interface declaration (specification) and source code for a class or object (realization)**  This is another example familiar to almost every experienced programmer.   Often a programming language allows one to define a set of method signatures (method names with their parameter and output types).  Examples include a Java or C# interface, a Scala trait, etc.  Then class source code provides the implementation of the interface.  
- the specification is more abstract because it only captures the desired set of methods and the input/output data types for each method.  It does not capture how the method is coded, how long the method takes to execute, etc. 
- the properties of the specific are a mix of structure constraints and type constraints (and the type constraints can then be viewed as constraints on data values).  Structurally, we require that the class provides at least the methods listed.  Moreover, the types declared for each method in the class must align with the types declared in the interface (sometimes, they the types don't have to exactly match if the language used has notions of subtyping).  
- Class to interface matching is performed algorithmicly in the language's compiler.  In contrast to the requirements/implementation above, we rely completely on a tool (the compiler) to judge the conformance (we don't have to argue ourselves whether we have done enough).  There is a remaining issue: are the appropriate sections of the compiler implementation (e.g., the type checker) correct? In general, we choose to trust the compiler (what are the justifications for this?)

**Example: Documented software architecture (e.g., in UML) (specification) and developed system (realization).**
Software/system modeling languages (sometimes called "architecture description languages") allow engineers to sketch the structure of a system.  The languages can address both software and hardware, but in this discussion we will use software-related examples.  Moreover, we focus on the structural aspects (e.g., class diagrams, package diagrams, subsystem interfaces, etc.) of these modeling languages rather than behavioral aspects (e.g., state charts, message sequence charts) -- we will address some of these next.  The idea that the specification is abstract in this case is reflected in the terms that we have used (e.g., "modeling", "sketching").  In general, languages like UML and SysML are often used first to brainstorm about the possible structure of the software.  They may be then "firmed up" and handed off to developers as guidelines for coding the system.
- the specifications (e.g., the software models) are more abstract because they do not indicate the algorithms to be used, or even the programming language.  In contrast to functional requirements, they do not even capture relationships between system and component inputs and outputs.  Rather, they aim to support "design" -- how the system is structually decomposed into parts and how those parts come together to make the system.
- the properties of specification are already mentioned above: the specification indicates part boundaries, features of a part available at a part boundary (e.g., the operations that can be called on a system, the messages sent by a component), relationships between parts (e.g., a set of classes held in a package (containment hierarchy), binding of one part's provided interface (service) to another client part's interface that uses the service).
- Unfortunately, in many situations today, the relationship between architecture designs and actual implementations is a murky one.  In fact, many companies still rely on informal (non-machine parseable) architecture diagrams drawn in Visio or PowerPoint.  In such cases, the specifications themselve cannot even by checked for internal consistency (e.g., are a fixed set of icons and diagram elements used where each has an intutive interpretation, are the diagram elements put together correctly).  When modeling languages are used, developers often work by hand to code the system so that it aligns with the diagrams.  Thus, the initial realization of the system may conform to the diagrams, but often they tend to drift apart over time (e.g., developers get lazy and don't continuous check that their implementations match the specifications, or the specifications get updated and it's "too hard" to refactor the system to exactly match the specification).  In these situations, the "best practice" is to maintain supplementary "traceability" documentation that describes how each feature in the diagram relates to a particular software feature.  One often wants these traceability relationships to be bi-directional, i.e., looking first at the software, we want to know if a particular feature is related to something in the architecture specification (note that not all software features have a corresponding analogue in the architecture diagram (e.g., a local variable, or while loop are concepts not captured in the architecture speciation).   Typically, the manual audits (human reviews are necessary to check the conformance.  In this case, establishing the conformance is a mix of the engineering producing correct and complete traceability documentation and the auditor confirming the correctness and completeness.   Overall, this type of conformance harder to have confidence is because it is based on informal traceability documentation and manual (rather than algorithmic) confirmation of the documentation.   Such cases, our confidence in the conformance relies strongly on the experience and competence of the auditor.  

**Example: State machine diagrams (specification) and auto-generated code that implements the state machine (realization)**  The behavior of certain classes of system elements can sometimes be specified in a high-level behavioral diagram like a state machine.  
- The state machine diagram is an abstraction because it doesn't indicate what programming language will be used to implement the state machine, how the possible states, start state, end state, and current state of the machine is represented, how implementation carries a transition between states.  
- In contrast to the structure specifications above, state machines indicate the important states of a system or a component, what states may follow (or precede) other states (e.g., they capture constraints on the evolution of the component or system execution), and the conditions under which one state may transition to another state.
- State machines are useful as specifications because they have mathematical definitions (formalizations) that provide a semantics (in this case, a notion of execution) that is completely independent of realizations in program code.  This has several implications.  First, the semantics 
of a state machine is so precise that the realization (e.g., in the form of source code) can be completely and deterministically derived from the specification by a tool (e.g., a code generator tool that parses a state machine diagrams and generates C code).  In this case, the conformance question can be re-oriented from "does the code match the specification" to "is the code generator correct".  When we establish the correctness of the code generator, we establish once that for any well-formed state machine specification, the generated realization is conformant.  This is an extremely powerful concept because we have turned the need for a potentially unbounded number of checks (checking conformance every time we have a different state machine) to a single check (the code generator for the state machine is correct).  It's typically much harder to establish with complete confidence that a "realization generator" is correct than to perform a conformance check, but if it can be done, it has significant payoffs.

We used the example of a state-machine specification to present the notion of code generation (or more generally, realization generation) from a specification but this concept is also applicable for a variety of other types of artifacts.  Common examples include *interface specification languages* (IDLs) or more general component interface specifications found in "frameworks".  An IDL compiler not only translates high-level data types and method signatures to a particular programming language implementation, it also be generate marshalling and unmarshalling algorithms that translate data types of wire-formats.

**Example: Technology specifications and implemented system (realization)**  In modern computer system development, we never develop a system completely from scratch.  At the very least, we choose 
existing programming languages that have accompanying editors and compilers.  And (hopefully), 
we have engineering rationale for the particular programming that we choose (e.g. does it
support rapid prototyping, or is it a memory safe language, or does it have a rich library 
that supports the domain we are working in).  It's also common that there is some framework 
or libraries that we believe we can make use of to avoid having to implement some functionality ourselves.  Or, we may be developing in a context in which we are required to interface with some existing systems, or run a particular platform, operating system, or processor.  These types of requirements can also be viewed as specifications.  In conventional development, we often refer to these as "platform requirements".  In contrast to specifications like system requirements or architecture specifications that "flow down" from the "top" (i.e., the more abstract concepts of the system), these types of specifications "flow up" from the "bottom". Or at least they serve as constraints that limit the possible range of realizations (i.e., they limit the "solution space").
- It's harder to see these specifications as abstractions, but we can still think of them that way because they are often presented to the implementation activity via enumerations of named programming languages (and versions), named libraries (and versions), named processors, named OSes, etc.  In this we rely on the fact that the names and versions alone are sufficient to retrieve the implementations (e.g., to retrieve library packages from a distribution repository).  Or that the name things have accompanying specifications (e.g., a programming language specification, a processor specification) that provide information sufficient to constrain the development process.
- This type of specification is relevant in agentic software engineering because we very often tell the agents not only the system behavior that we want to achieve but also the technologies that we want to make use of.  For example, it is quite common to have a section of a CLAUDE.md file (or other high-level project documents) called "Technology Stack" that indicates the specific technologies to be used.  Alternatively, if the technologies are not dictated to use, an important part of human-agentic planning is identify possible technologies, understand their trade-offs, and make some decision about the specific technologies to use.
- Establishing the conformance relationship can be murky.  A common manifestation of the conformance relationship would be found in build system artifacts that indicate the specific external packages that are pulled in to our code.  More broadly, compliance regimes are increasingly requiring a software "bill of materials" that explicitly enumerates all the software beyond our control that we incorporated into this system.   While the build system elements provide some mechanized way of establishing conformance, one potential trust gap is the trustworthiness (correctness, absense of security vulnerabilities) in the libraries themselves.  Thus to fully establish correctness/security of the system, we depend on the trustworthiness of the libraries and the provenance (did we obtain the libraries from a trusted source or did we download it from some sketchy distribution site).

**Example: Development process specifications and evolution of development artifacts**  Often times in development of large-scale systems, we are concerned about the steps by which the system is developed.
In this context, development process refers to documented steps, arranged according to some ordering constraints, that include "gates" that indicate when a step is completed satisfactorily, and that also indicates "hand-offs" between steps (i.e., what artifacts are required for the step to begin, what artifacts are produced to hand-off to subsequent steps).  The "gates" may be simple things like 
source code compiles and builds, or stronger constraints like "all tests pass".  Our development instructions may dictate when/what we commit to a source code repository, how regression tests are run, etc.  All of these examples include source code and gates that can enforced automatically for the most part (e.g., "run all tests and check that they are no failing tests" is a gate that can be performed automatically). More challenging are situations where non-mechanical audits are required, e.g., human reviews of requirements, human reviews of pull-requests, etc..  The goals of having a well-defined process (or a "recipe" for building systems) include being able to develop software at consistent level of quality, being able to coordinate development across a larger number of people, being able to control how the system artifacts evolve, being able to assess that each recognized step of development produces artifacts that are "in a good state", being able to more easily isolate changes and problems that led to the system artifacts being in a bad state (e.g., what commit introduced a bug), being able to roll-back a bad state to a previous good state.  Unfortunately, following a rigorous development process often doesn't seem necessary in small, one-person projects, and the ideas of understanding good processes, designing processes, tracking that developers follow a process are not sufficiently addressed in our small classroom-sized projects.  However, they are absolutely essential in development of large systems and for development that involves many different developers.  In small settings, we often were able to get by without worrying about all the heavy-weight "process stuff", because we intuitively understand whether the system was in a good state, or all of the developers on the team could have a reasonable intuition based on informal discussions.  However, with the advent of agentic development, agents don't talk over lunch or coffee about the current state of the system.  They work only from artifacts that they see (and their own training).  Moreover, concepts like agent swarms (thousands of agents working together) are demonstrating promise, but they only work when they follow specific rules for handing off to each other.
- Thus, process specifications that were once commonly viewed as boring or unnecessary are becoming central in agent-based developed.  The current emphasis on "graph engineering" with agents is really just a buzz word for precisely specifying development steps, agent capabilities for steps, and hand-offs between steps, i.e., "orchestrating" agents.  These specifications are abstractions in the sense that they don't dictate every model call or tool call that they agent makes (in the same what they did not dictate every line of code or every test that a human developer writes).  They instead indicate ordering constraints between coarse-grained activities, they indicate constraints (invariants) that must be achieved on the development artifacts as state evolves (e.g., tests always pass for each pull request).  In fact, the same types of notations that were often used to state constraints on the evolution of system state (such as state machines or petri nets) are now being used to state constaints on the evolution of system development artifacts.  Instead of constraining the system, they are being used to constrain the building of the system.
- Ensuring conformance for this type of specification/realization is also a challenge.  In constrast to some of the other notions of conformance, this notion is not a strictly post-facto (after the fact) check.  That is, we don't want to wait until the system is delivered to check if the process was followed (although we would like to be able to audit the development history to determine if the process was followed).  We need to be able to ensure compliance with the development process at each step.  Exiting a step while by-passing a gate might lead to the artifacts being in a bad state which would cause subsequent agent steps to fail.  Failing to specify how artifacts get merged when multiple agents are working, causes thrashing and prevents some automation.  We don't have the technology now for formally verifying that agents followed a specified process, so the best thing that we can do is rely on "testing" of the workflow framework by having agents build example system, and having some way to dynamic monitor if steps are followed.

**Example: Test vectors, test suites as specifications** (TODO)


## Different Arrangements of Specifications and Realizations

### One Specification, Many Realizations

For a single specification S, there may be multiple realizations R1, R2, .., of S.  In fact, since S is by definition abstract wrt its possible realizations (i.e., it omits details not found in the realizations), then for all but the most trivial domains, we necessarily have multiple realizations of S.

We have already identified some examples above.
- System implementations R1 and R2 may use different programming languages, different algorithms, or different coding idioms to satisfy the same system requirements S.  
- Data representations R1 in programming language P1, R2 in P2, and R3 in P3 may all satisfy the same IDL data specification.

What examples can you think of?

### Many Specifications, One Realization

In practice, we don't have a single specification for a system -- we have a *set* of specifications, e.g., a system requirements document, an architectural specification, and platform requirements.  Each specification provides a different "view" of the system (for a related concept, see Philippe Kruchten’s [4+1 Views](https://arxiv.org/pdf/2006.04975) or the IEEE standards on software views) and addresses different concerns.  However, we need the set of specifications for a system to be *consistent*.  For example, if the requirements state how a building's environmental controls settings (e.g., air-conditioning) are derived from the current temperature each of its rooms, we expect the system architecture to include features such as the temperature sensors that provide the temperature values and on/off or fan speed interfaces for the environment controls.  This is another notion of *traceability* -- in this case traceability between companion specifications instead of traceability between implementation features and specification features as we discussed with architecture features.

### Stacked Specifications

In addition to companion specifications, we can also have "stacked" or "hierarchical" specifications.  A common situation is when a higher level specification is decomposed into lower-level more precise specifications.  For example, system requirements specifying how the system behaves "end to end" may be decomposed into software requirements and hardware requirements.  Software requirements at the top-level of a software system may be decomposed into requirements on individual subsystems, packages, etc.  The DO-178C certification standard for civilian avionics software has a notion of high-level requirements (HLRs) and low-level requirements (LLRs), where LLRs roughly correspond to requirements on classes and methods.

In such cases, we may say that a high-level specification HS is realized by a collection of low-level specifications LS1, LS2, ..., LSn where the low-level specifications are consistent with the decomposition present in an architecture specification.  Note that low-level specifications aren't "implementations" in the conventional sense even though they reflect some thing about how HS will be achieved.  That's one reason why we chose to use the term *realization* of HS -- to include situations where the things conforming to HS aren't executable implementations.   

When we have specification hierarchies, it's more common to use the term "specification refinement" to describe the conformance relationship.  For example, we might say that LS1, LS2, ..., LSn together with architecture specification *refine* HS.  In general, defining exactly what we mean by *refinement* in this case and *checking* the conformance relation (i.e., checking that the lower-level specs are indeed a refinement according to the definition) is a tricky business.  Because such requirements almost always written in natural language and because the architecture description almost never completely captures how subsystems behave as they are communicating with each other, etc., it's practically impossible to achieve would we would really want as a refinement, i.e., a guarantee that if a system satisfies LS1+LS2+..+LSn+architecture then it will satisfy HS.   Instead, we fall back on some notions that based on traceability and manual inspection.  For example, we might require that..
 - every HLR in HS is implemented by one or more components C1,..,Cm in the architecture and there are identifiable LLRs in C1, .., Cm that in their aggregate achieve HLR.  In traceability documentation, we would say that HLR is "allocated" to C1, .., Cm (i.e., those components are responsible for achieving) the HLR, and we would have forward and reverse traceability links between the HLR and implementing LLRs.
 - every LLR and architectural feature is traceable in some way to a high-level requirement.  This obligation, often phrased as "no gold plating" ensures that we haven't added additional features or constraints to the system that aren't strictly necessary to the the HLRs.
 On top of this, we have manual (human) audits that confirm the correctness of this traceability information. 

The traceability approach described above is in essence what is required in DO-178C.  We typical development of non-critical applications in the past we almost certainly viewed this type of documentation and reviewing activity as overkill.  However, with agentic development, it is a best practice to ask agents to produce, maintain, and even help audit such information.  This is because the human development burdern shifts from producing the realization towards assessing that the code the agents produced conforms to the specification.  For example, whereas in the past we as humans had more intuition about our implementations because we built them, that intuition no longer exists when agents to the coding.  Often you will want to ask the agents
- what is the evidence that you addressed every concept in the specification?
- what is the evidence that you didn't add anything extra or surprising in the implementation that I did not ask for?

Then, as a developer you can inspect this evidence or ask an independent review agent to review the evidence.

## Engineering Approaches and Activities that Leverage Specifications

It is often useful to think of specifications as "blueprints" for a system.  Just like architectural blueprints, specifications are engineering artifacts that must satisfy basic well-formedness properties.  Blueprints are abstractions -- they indicate key properties of interest to builders, but they don't describe everything about the building.  Blueprints also provide [different views](https://www.masterplanservices.com/post/5-basic-architectural-views-explained) of a building: floor plans, elevations, etc. and their are consistency rules and notions of traceability between the views.  Just like software specifications, blueprints provide guidance to different categories of builders (electricians, plumbers, physical construction).  Blueprints also serve as analyzeable abstractions that are assessed by third parties (e.g., government inspectors) to determine if the building meets various building codes, to estimate costs, etc.

Below we list key engineering functions of specifications and explain how these have traditionally been used in human-centric development.  We discuss why they might have slightly different emphases in agentic-centric engineering.

- *Specifications serve as directives to builders* -- in this use, specifications are developed early in the develop process to summarize at a high-level *what* should be built and/or what *properties* the constructed system should possess.  They are key products of planning, and they can be analyzed before coding begins.  Traditionally, in human-centric development, this has saved costs and time by allowing potential problems to be discovered before code.  In agentic-centric development, the same "assess and rework before coding" reduces wasteful token spend.  In some special circumstances, code can be deterministically generate from specifications.  In such cases, agents might be asked to follow that process via precise translation rules.  Better yet, agents are asked to build a tool that implements the translation to avoid any agent non-determinism and to eliminate token spend for these particular code generation steps.
- *Specifications as constraints or guardrails* -- in this use, a system might already be partially or completely developed, but a refactoring or optimization needs to be carried out.  In this case, humans or agents have the freedom to adjust the realization for better performance or to reduce technical debt, but they need to make sure the new version of the system still complies with the original specifications. 
This relates to the concept where we may have multiple realizations of a specification as follows:  both the original system and updated system are realizations that conform to the same specification.
In this use, the specification acts as *invariants* that must be maintained as the state of the development artifacts evolve.  Process specifications complement this view by constraining the actions, sequencing, and division of labor that human/agents carry out to achieve the evolution.
- *Specifications can help in engineering better interfaces and seams* - Often times we define *interfaces* at some boundaries in the code where we want to hide the details of a service being provided to clients (TODO: give examples).  With such interfaces in different realizations of the interface/service specification may be implemented by different organizations using different technologies.  Or within a single organization, because the client software is not tangled with the implementation of the service, we have more freedom to evolve the service implementation without needing to update the client code.  The most rigorous interace specifications capture not only method signature and data format, but also use the notion of *software contracts* or *behavioral interface specification languages* to capture behavioral constraints such as pre- and post-conditions on provided services.   Interface specifications are useful to agents because they can be told to develop a client of an interface without needing to spend tokens reading the code that implements the service (this is always the case if the behavior of the methods on the interface aren't clearly specified).  Often times agents will tend to build a complete chunk of software providing a desired end-to-end capability.  You may need to tell the agent where to design in an interface layer.  A related notion is the idea of a software *seam* -- Michael Feathers defined this concept in his book "[Working Effectively with Legacy Code](https://learning.oreilly.com/library/view/working-effectively-with/0131177052/)".  The analogy is a seam in clothing: it's a place where two parts are stitched together. The piece on each side only touches the other right at the seam.  In working with legacy software, if you identify the seam you have identified the place where you can potentially have a well-defined interface.  Having agents discover or design seams and interfaces allows supports testing by provide points at which full implementations can be swapped out with mock implementations to support testing.  To say this more strongly, designing or discovering seams enables code to be carved up in manageable chunks that can be more easily tested because you can swap real parts for fake ones.  With human development, there is often reluctance to do such refactorings because they are effort intensive.  With agents, one may be more willing to spend tokens to substantially improve code organization and testability.

- *Specifications aid in understanding* 

- *Specifications as abstractions that enable cheaper analyzes* 

- *Specifications service as directives to testing and verification*







Specification quality properties (internal "goodness" of the specification)
  - consistency
  - completeness


Conformity assessment ("goodness" of the relationship between the realization and the specification)
  - typical methods
     - documentation and artifacts
     - audits (could be tool supported)
     - decision procedures (tools)
     - experiments (specific cases, relying on generalization, induction)


Multiplicities - more than one realization meets a specification, can have many specifications associated with one realization


Verification



Control over the decomposition of work, granularity of work and over the flows (and dependences of artifacts) and handoffs


Intent (as a intangible specification)


 Validation 





Assurance 
 - explain and convince through arguments and evidence that specs meet their quality properties








Certain libraries packages used, interfaces adhered to, provenance, bill of materials 

Definitions 

artifact







Conformance 

Traceability

Assurance

Idea of conformance checker vs a translation tool that ensures conformance for all specifications.


Activities
 - done by a human
 - done by an model (at least in part)
 - done by an tool (a executable program external to the model)


Mechanical conformance checker, a correct generated tool that always produces compliant implementations.

