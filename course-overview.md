# Course Overview

## Course Purpose and Overview

This course introduces students to agentic software engineering: building software and systems with AI agents through disciplined, repeatable, and scalable practices rather than "vibe coding."

The course begins by teaching students to implement a simple coding agent. LLM-based agents are themselves a computing platform: they operate through a set of primitives that includes calling an LLM with context, invoking tools, and receiving instructions from a human developer. Each step incurs costs and may introduce errors or security risks. To use agents effectively, students need to understand their anatomy, develop a mental model of their execution, estimate costs, and identify potential sources of failure and security vulnerabilities. This understanding also enables students to customize and extend agents for greater effectiveness and efficiency in a particular development context. The course also examines how agents interact with conventional development tools, such as testing frameworks and source code repositories, and how agentic development changes established practices or calls for new tools.

After learning how coding agents work and how to use them effectively in simple cases, students turn to an engineering-oriented methodology for working with agents. Earlier software engineering courses may have introduced processes, phases, and artifacts such as concepts of operations, requirements, plans, designs, implementation, verification, and validation. These practices can seem burdensome or irrelevant, especially on small projects completed individually or in small teams. In agentic development, however, they become increasingly important. Agents require clear guidance, and their work must be organized into consistent, reviewable artifacts that support evaluation and reliable handoffs among humans and agents. This course therefore reviews key software engineering processes and artifacts, and shows how they apply to agentic software engineering.  Most importantly, the course explores how conventional methodology needs to be rethought and modified to support agent-centric softare engineering.

With this foundation in place, students undertake increasingly substantial development tasks. They learn to combine development processes, engineering artifacts, and agent capabilities into repeatable, effective workflows that replace improvisation with deliberate engineering practice. A central learning outcome is the ability to design agentic development workflows: decomposing a large project into steps or waves (process decomposition), dividing an architecture into manageable units (structural decomposition), producing reviewable outcomes, and organizing handoffs between phases, agents, and humans.

After establishing these engineering principles, students apply them to a larger project. They also learn to organize and direct agents during long-running tasks (agent loops) and to coordinate teams of agents.

For hands-on work, the course uses Claude Code as its primary platform. The principles and practices taught are intended to transfer to other coding agents, such as Codex.

## Course Outline

### Part 1 (Weeks 1-3) - Foundations - Learning the Architecture of An Agent

Lecture Coverage 
  - How LLMs and agents work 
  - Walking through the architecture of a simple coding agent
  - Basic interactions with a frontier agent (Claude Code) 

Exercises and Projects
  - Reviewing the transcript of a coding agent applied to system development
  - Programming your own simple coding agent using an LLM API
  - Using a coding agent to understand and document an existing development project
  - Using a coding agent to set up a markdown-based personal knowlege base (PKB).
    You'll use this PKB through the semester to collect summaries of new articles, YouTube videos, and blog posts as well as your own on agentic software engineering. 


### Part 2 (Weeks 4-7) - Basic Agentic Software Engineering Principles 

Lecture Coverage
  - Core concepts of traditional software engineering, and re-orienting those for agentic software development
  - Core agent harness competencies for agentic development, illustrated with Claude Code (agent memory, skills, hooks, model-context protocol (MCP), efficient representation of context, tradeoffs between models, basic security configurations)
  - Specification-centric development with agents
  - Patterns and Recipes for agentic software engineering
  - Application of agentic software engineering to a non-trivial but small-scale application

Exercises and Projects
  - Exercises: Demonstrating basic software engineering concepts with small examples (specification vs implementation, verification, validation, plan mode, traceability, assurance artifacts)  
  - Exercises: Small exercises covering key harness concepts (skills, hooks, MCP, security configurations)
  - Reviewing and assessing previous project-sized agent development logs, hits and misses
  - Individual project: building a simple on-line game in several different ways using agentic software engineering principles

### Part 3 (Weeks 8-15) - Advanced Agentic Software Engineering Techniques and Larger-Scale Development

Lecture Coverage
  - Designing and managing engineering artifacts for large-scale scale systems
  - Work decomposition and planning for large-scale systems, task design, task gating
  - Sub-agents and Parallel Work
  - Agent roles, agent independence, agents as reviewers/critiques
  - Long-running, autonomous development
  - Project presentations and reflections on the course

Exercises and Projects
  - Exercises: patterns for sub-agents
  - Exercises: work decomposition and task gating
  - Team project: building a large scale knowledge base project using Neo4J
 

## Student Learning Outcomes

- Understand the behavior of Large Language Models (LLMs)
- Understand the architecture of coding agents, how coding agents are built from LLMs, be able to build your own simple coding agent
- Understand the role of an agent harness vs the role of a LLM in agentic software engineering tooling
- Understand technical software engineering concepts including Specification, Realization, Verification, Validation, Requirements, Concept of Operations, Development Process, Planning, Assurance
- Understand how conventional concepts of software engineering map to agentic-based development
- Master repeatable methodologies for building, documenting, and assuring software systems via agentic development
- Understand and predict costs and trade-offs when applying differ agent models
- Understand how to work in teams using agentic development




