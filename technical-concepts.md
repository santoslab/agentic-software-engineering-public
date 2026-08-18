# Technical Concepts

This is a list of technical concepts used in Claude Code, as well as 
references to educational material for each concept.

> **Where each concept is taught:** see the [course overview](./course-overview.md) for the course
> schedule and [weeks-01-03/](./weeks-01-03/) for the foundations unit. Roughly: the
> Basic Concepts below are covered in Lectures 03–06 (weeks 2–3); of the Tools,
> skills get a first taste in week 2 (grill-me) with depth around week 5, hooks and
> subagents arrive with Project 2 (~week 9), and MCP servers with Project 3 (~week 12).

### Basic Concepts
1. **Prompting and Permissions**
    - Claude Code has the ability to modify contents of files and run bash commands, but we need to give it permission to do so. 
    - [Udemy Section 6: Basic Usage and IDE Integration](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529153#overview)
    - [Claude Code Docs: Available Modes](https://code.claude.com/docs/en/permission-modes#available-modes)
    - [Claude API Docs: Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
    - [Prompting Cheat Sheet](./prompt-cheat-sheet.md)

2. **Links and Commands**
    - Since Claude Code runs in a workspace, you can reference files using the `@` symbol. This will force Claude to read it before answering. You can also call commands or other tools using the `/` symbol.
    - Use to enrich your prompt, but avoid overusing them to flood the context window with copies of the same file or unnecessary files.
    - _Agentic-Engineering-with-Claude:_ Chapter 3, Controlling Claude with Slash Commands

3. **Context**
    - To work effectively with Claude Code, you need to manage the Context that Claude is given. Better context management will not only provide better results, but also reduce the cost.
    - [Claude Code Docs: Explore the Context Window](https://code.claude.com/docs/en/context-window)
    - [Udemy Section 22: Prompt & Context Engineering Recommendations](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54578723#overview)
    - _Agentic-Engineering-with-Claude:_ Chapter 1


4. User maintained Memory (*Claude.md*) 
    - One way of providing specific workspace context is Claude.md files. One will be generated when first running `/init`, but more can be placed in sub-directories for specific information. 
    - [Udemy Section 23: Initializing Claude Projects](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529223#overview)
    - [Udemy Section 24: Creating Great CLAUDE.MD Files](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529225#overview)
    - [Udemy Section 25: CLAUDE.md vs "Auto Memory"](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/55027397#overview)
    - [Claude Code Docs: Write an effective CLAUDE.md](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md)
    - _Agentic-Engineering-with-Claude:_ Chapter 3, Understanding Memory in Claude Code
    - _Agentic-Engineering-with-Claude:_ Chapter 5, Adding repository context with CLAUDE.md

5. **Plan Mode**
    - To help Claude with larger tasks, enable Plan mode to have Claude propose a plan to execute. Once approved, it will use it to help stay guided on current task and its requirements.
    - [Udemy Section 26: Leveraging Plan Mode](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529229#overview)
    - [Claude Code Docs: Analyze before you edit with plan mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode)
    - _Agentic-Engineering-with-Claude:_ Chapter 6, Claude Code planning mode

6. [_Claude Code Docs: Best Practices_](https://code.claude.com/docs/en/best-practices)


### Tools

In your claude project you have a `.claude` folder where, among other things, your custom tools and permissions for Claude to use are stored. Here are the different tools and their use cases.

`.claude-template` holds some template examples for what some fo these tools would look like in your `.claude` folder. 

- **Sandbox**
    - To reduce the risk of Claude causing damage to your system or other files, you can set up a sandbox for Claude to work in. There are different
    types of sandboxes with different levels of complexity and protection.
    - [Udemy Section 15: Using Claude Code's Native Sandboxing](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529195#overview)
    - [Claude Code Docs: Choose a sandbox environment](https://code.claude.com/docs/en/sandbox-environments#choose-a-sandbox-environment)
    - [Claude Code Docs: Bash sandbox](https://code.claude.com/docs/en/sandboxing)

- **Hooks**
    - Hooks provide an opportunity to run a command after a specific event (ex. After a user prompt, after Claude Output, After a specific tool use, etc)
    - [Udemy Sections 40: Understanding & Using Hooks](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529329#overview)
    - [Claude Code Docs: Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
    - _Agentic-Engineering-with-Claude:_ Chapter 3, Using hooks in Claude Code


- **Subagents**
    - Sometimes it is best for complex tasks to be broken down into well defined Subagents. They can run in parallel and have separate context windows. Primarily spawned by the main agent.
    - [Udemy Section 29: Understanding Subagents](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529253#overview)
    - [Udemy Section 30: Creating & Using a Custom Subagent](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529257#overview)
    - [Udemy Section 31: Encouraging Subagent Use](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529263#overview)
    - [Claude Code Docs: Create Custom Subagents](https://code.claude.com/docs/en/sub-agents#create-custom-subagents)
    - _Agentic-Engineering-with-Claude:_ Chapter 7

- **Skills**
    - Skills are a way to provide specific and focused context to help with a common task. 
    - [Udemy Section 32: Introducing Agent Skills](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529271#overview)
    - [Udemy Section 33: Adding Custom Skills](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529267#overview)
    - [Udemy Section 34: Using Agent Skills as Commands](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529265#overview)
    - [Claude Code Docs: Extend Claude with Skills](https://code.claude.com/docs/en/skills)
    - _Agentic-Engineering-with-Claude:_ Chapter 3, Custom slash commands in Claude Code (powered by Skills)
    - _Agentic-Engineering-with-Claude:_ Chapter 9

- **MCP Servers**
    - To provide Claude additional external tools and resources, MCP for Model Context Protocol servers can be installed and used.
    - [Udemy Section 28: Using MCP Servers & More on Permissions](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529251#overview)
    - [Claude Code Docs: MCP Quickstart](https://code.claude.com/docs/en/mcp-quickstart)
    - _Agentic-Engineering-with-Claude:_ Chapter 4

- **Plugins**
    - Plugins allow you to interface with other programs (ex. Slack, email, etc.) Use the plugin marketplace to manage your installed plugins.
    - [Udemy Section 41: Installing and using Plugins](https://www.udemy.com/course/claude-code-the-practical-guide/learn/lecture/54529337#overview)
    - [Claude Code Docs: Discover and Install Prebuilt Plugins](https://code.claude.com/docs/en/discover-plugins)
