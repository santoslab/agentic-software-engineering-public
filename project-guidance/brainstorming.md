# Brainstorming and Informal Planning

Consider that there are two types of project starting points for
almost everyone in the class:
- "greenfield" projects - you are starting from scratch, and you just
  have an "idea"
- "brownfield" projects - you are starting from some existing code
  base

In both cases, you can use agents to help you come up with possible
directions and form some understanding for your project.

## Greenfield Projects

We assume that you have some general idea for a system including:
 - what functions it will provide
 - what type(s) of interface(s) will be presented to users.

To get the agent going on a project, you typically need 
- something approaching the type of content that is found in an
  informal ConOps sketch (i.e., just a sketch of the system purpose,
  types of users, and a few user stories -- or something even simpler
  like "I want users to be able to (..do this..) and (..do that..))", 
- something that indicates to the agent the basic technologies that
  you want to use for the development
- a git repository prepared (or you ask the agent to set up one).

First, write a paragraph about what your system should do and include
the types of users or other systems it should interact with.

Then, you probably have questions about:
 - what technologies are best suited for your needs
   - programming language(s) 
   - data representations 
   - data storage
   - UI technologies, graphics libraries
   - communication, network interfaces
 - how do you want the agent to install the required development technologies

### Example Interaction

```bash
I have an idea for a project and I would like to brainstorm with you to identify the technology stack for it.
```

[The agent will most likely ask you to describe your project at this
point, and then lead you through some discussions about the possible technologies.]

When you are interacting with the agents and are focusing on a
particular technology, ask it to give you the pros and cons of each
choice.  From this information, make a decision and let it know which
direction you want to go.  If you can't decide, ask the agent to make
a recommendation.

### Turning your brainstorming chat into some initial engineering documents 

Once you feel like you have dialogued enough with the agent, use the
ConOps elicitation skill in feeding the reference information that you
have developed so far as the seed.  Or, ask the agent to
draft a simple ConOps for you (give it an example of the outlines we
have used in the class) and ask it to give you in a separate file, a
description of the technology stack based on what you have concluded
in your interactions.

These are now turning into engineering documents that you will track
in your git repository.


## Brownfield Projects 

In this situation, you are starting from an existing code base to
which you want to add some functionality, do a reimplementation, etc.
It is likely that this project has not been developed in a rigorous
way with agents.

Your first steps are to form some general understanding of the codebase, including
   - technologies used 
   - the architecture of the codebase
     - what are the primary chunks of functionality, primary
       libraries, used
     - what are the interfaces between the chunks
     - what are the data representations used
   - how do you run the system
     - as you run the system, what are some example inputs to provide 

Ask the agent to produce the above information for you, plus any other
information useful for supporting agentic development of the system.

Your next job is to ask the agent to turn the results of the dialog
above into your initial agentic engineering documents.  Ask the agent
to develop 
  - an initial ConOps for the system (following the outline used in
    class -- give it an outline or it will try to put too much info in
    the document) to explain the system "to the rest of your team"
  - a summary of the technology stack that will be read by other
    agents moving forward 
  - a description of the data formats used
  - a description of the architecture including boundaries of primary
    components and interfaces between these.

## Next Steps

The next steps are to firm up your ConOps document (see the next
note).

## Resources - Example Prompts

Here are some example prompts that you might consider.

The prompts are grouped by the step of this note they belong to.
Replace the bracketed parts with your own project's details. Several
of the brownfield prompts are taken, lightly edited, from the
brownfield example conversation in
[brainstorming-examples/](brainstorming-examples/brownfield-hamr-sysml-viz-conversation.md),
where you can see how the agent responded to them.

### Greenfield: the brain dump

Open with the big picture explaining the purpose of the system, 
what already exists (if anything), your constraints, and
what you want back as the result of the planning discussion. 

```
I want to brainstorm with you about a project that I want to build.
Here is the big picture: [purpose; who uses it; the two or three
things they must be able to do; any existing code or data; what I
already know; my constraints, for example: must use Neo4j, solo
developer, seven weeks]. Do not propose a design yet. List what you
need to know from me before you can recommend a technology stack,
ranked by how much the answer would change your recommendation, then
ask one at a time with a recommended answer for each.
```

Alternatively, stop after "Do not propose a design yet."  and then
explicit ask for guidance on the technology stack, as illustrated below.

### Greenfield: choosing the technology stack

```
Here are some software layers that I expect to be in the project, 
[indicate what you are imaging that you will need: language, data model and storage, UI, communication
between parts]  For each layer  give two or three candidates with pros and cons for 
[the project time line and your human resources -- 
 e.g., solo developer with seven weeks], then one recommendation and why.
Treat every constraint I gave as fixed.  Also, indicate if there are additional
technology elements that you think I will need to have in the system, and provide 
an assessment (pros/cons/recommentations) for those.
```

Archive (at least until you are sure of all of the choices) the
different options that you have in your reference material (remember:
reference material is background info -- not part of your engineering specifications).

```
Write reference/decisions.md: one entry per technology choice from
this conversation with the options considered, pros and cons, the
decision, and the reason. Mark anything undecided as open, with your
recommendation.
```

### Greenfield: scoping the first version

Brainstorm about the scope of some very simple initial version of the system.
```
Propose the smallest version of this system that demonstrates the idea
end to end by [deadline for initial demo, e.g., - November 16]. 
List what it includes and what it excludes.
The exclusions will become the deferred wants section of the ConOps.
```

Or ask the agent to help you identify a single module or subset of the
system that can be developed and tested as a standalone entity.

[Claude: suggest something here.]


### Greenfield: setting up the environment

```
Set up the development environment for the stack and initial version of the 
system that we chose: install
the toolchain, pin versions, and produce a buildable skeleton of the system 
with key files, etc. that are sufficient for testing if the tools are installed 
correctly.  Record the exact install, build, run, and test commands in README.md.
Stop and show me when the skeleton runs.
```

### Greenfield: the first engineering documents

Produce a basic draft ConOps (we will refine it in the next phase of development).
```
Draft specs/conops.md using exactly these six sections: purpose; scope
and boundary, with assumptions; user categories; user stories, each
with one concrete example;. Use only what we
have discussed. Put every feature we mentioned but did not choose for
the first version under `reference/deferred-features`. 
Mark anything you had to guess with TODO so I can run elicitation on it. Say nothing about
implementation or technology.
```

Now set up an initial technology stack specification.
```
Write specs/technology.md for other agents: each language, framework,
library, and tool with a pinned version, why it was chosen, its
license, and how it is installed. End with a one-line Requires
statement that another developer could check.
```

### Brownfield: understanding the codebase

```
Read this repository and write docs/orientation.md: technologies and
versions in use, the main components and what each does, the
interfaces between them, the data representations, external
dependencies, and how to build, run, and test. Every claim must cite
the file it comes from. List what you could not determine.
```

```
Build the system as it is and run its tests. Report the exact
commands, what passed, what failed, and anything you had to install.
Change no code. Then tag the commit as baseline.
```

```
Give me three example inputs that exercise different parts of the
system, run each, and show me the output. Record them in
docs/running.md so I can repeat them.
```

```
Describe each data format used as data flows through the system. Take
one tiny example and show its representation at every stage. For each
transition, explain why the representation changes to suit its new
purpose.
```

```
List the larger cohesive chunks of code that implement functionality
this project will not use. For each: the files, the size, what depends
on it, the risk of removing it, and a recommendation. Remove nothing.
```

### Brownfield: the first engineering documents

There are several possible ways to get the initial set of engineering
documents going.  The easiest may be to ask the agent to produce engineering 
documents for the current baseline. Then you would develop a plan 
for evolving things from that baseline, with specific feature requests.

```
Draft specs/conops.md for the system as it exists today, using exactly
these sections: purpose; scope and boundary, with assumptions;
user categories; user stories, each with one concrete example.
Write it to explain the system to a teammate
who has never seen it: users and what they observe only, nothing about
implementation.
```

```
From docs/orientation.md, write two documents for other agents:
specs/technology.md (each language, framework, library, and tool with
its version, license, and how it is installed) and
docs/architecture.md (the primary components, the boundary of each,
and the interfaces between them, each citing the files that realize
it).
```


### Both: stress-testing the plan and keeping the record

```
Grill me on the plan in reference/decisions.md: interview me about
every decision it depends on, one at a time, with your recommended
answer for each, until we reach a shared understanding.
```

```
Write your open questions into docs/open-questions.md, one per
heading, with your recommended answer under each. I will answer them
in a commit; then proceed with the next round based on my answers.
```

```
Create a markdown transcript of this conversation, my messages and
your replies verbatim, with links to every file you produced, and save
it under reference/ so the rest of my team can read how we got here.
```
