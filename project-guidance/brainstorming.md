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
  types of users, an a few user stories -- or something even simpler
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

These are now turning into engineering documentst that you will track
in your git repository.


## Brownfield Projects 

In this situation, you are starting from an existing code base to
which you want to add some functionality, do a reimplementation, etc.
It is likely that this project has not been developed in a rigorous
way with agents.

Your first steps are to form some general understand of the codebase, including
   - technologies used 
   - the architecture of the codebase
     - what are the primary chunks of functionality, primary
       libraries, used
     - what are the interfaces between the chunks
     - what are the data representations used
   - how do your run the system
     - as you run the system, what are some examples inputs to provide 

Ask the agent to produce the above information for you, plus any other
information useful for supporting agentic development of the system.

Your next job is to ask the agent to turn the results of the dialog
about into your initial agentic engineering documents.  Ask the agent
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







