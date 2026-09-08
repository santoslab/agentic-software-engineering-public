---
reference: harness-engineering-masterclass
source_url: https://www.youtube.com/watch?v=mQfTdNVCOB0
captured: 2026-08-15
---

# Harness Engineering Masterclass: Technical Deep Dive on how to build Agentic Systems

*The Carbon Layer · uploaded 2026-05-16 · 28:06 · manual captions (en-IN) · https://www.youtube.com/watch?v=mQfTdNVCOB0*

<a id="t-0000"></a><!-- #region t-0000 -->
## [0:00] Introduction to harness engineering and its significance.

**[0:00]** Hello everyone. Today we'll be trying to demystify what harness engineering is all about. In particular, I'm talking about the AI agent harness engineering, Um, and so I'll try to walk through all the different uh components and primitives as I'm calling it. Now, these are not all well defined, these are not something that everyone has agreed upon. This is just my way of trying to explain what goes in when you use systems like Codex and Claude code, and it's not just the model. . So harness engineering, yeah, maybe that's a good way to start, is the system around the model, the model matters. Like of course it does, which is why we have the whole model wars that we see with all the benchmarks and stuff that goes around. But once you start building the real agent workflows, the model is only one part of this

**[0:45]** entire machine. So the harness gets to decide what the model sees, what it can act on, via tools, of course, um, what it remembers.
<!-- #endregion t-0000 -->

<a id="t-0101"></a><!-- #region t-0101 -->
## [1:01] Explanation of the model's role and the concept of hallucinations.

**[1:01]** what works get delegated, how and what it verifies, and and overall like how it recovers from a failure. So this is the deep dive in that topic to reveal uh how the magic as we see uh Claude Code and Codex do and expose the machinery that is uh making that happen, the Center of all of this is the model, ? and with model, what happens is um you give it a prompt, and model gives you a text, and it gives you a text back, and that in itself is already useful. Early on, when the whole Chat GPT era was just starting on, um, that's all most of the people did. they would kind of craft these nice prompts. And out comes an uh some text, and that text can be used to help you explain a concept, it can help draft a plan, It can even write an email, If you provided uh a good prompt.

**[2:01]** and so that is all it was. It's just basically a model, and you interacted with the model directly via some API. But this has a boundary, and that boundary is obvious, The model. only sees what is inside of that prompt. and all the uh data that it's trained on. that is what will help it to kind of give you that output or the text, So if your current project or repository or the ticket or incident or workflow is not part of that input, the model will start guessing. And that's what we call hallucination. So the first question is not actually that is the model smart, I think the first question is what are we giving it?
<!-- #endregion t-0101 -->

<a id="t-0239"></a><!-- #region t-0239 -->
## [2:39] Definition of an AI agent and the agentic loop.

**[2:39]** To work with in the first place, What is in the prompt is what the question would become, So if this is the model, what does an agent mean? So again, the word agent gets thrown around quite a lot. Um, OpenAI's uh agent SDK defines it as like an LLM or a model that is configured with some instructions and it's provided some tools and it's put into this uh environment that it can uh act on. Um that's what is the definition of like an agent, and codex and Claude code show the product version of that agent, Um but that loop where it follows Reason, act, observe, and repeat that loop is what we call as the agentic loop, But before we jump in and start talking about the primitives, I think we should clarify three things as to not confuse them, Model, that is a reasoning engine.

**[3:30]** Second is this runtime that we just talked about. That is the loop where the model will observe, decide, call and act on And then third, which is what our deep dive is going to be, the harness itself, That is the system around this runtime.
<!-- #endregion t-0239 -->

<a id="t-0345"></a><!-- #region t-0345 -->
## [3:45] Discussion on the importance of instructions as a primitive.

**[3:45]** And we'll talk about some of those one by one. When an agent fails, we usually blame the model, We'll say, like, oh, the model might not be that great. Um, and sometimes that is true. Like there is clearly difference between model capabilities and smartness, but often is the it's the layer, one of these components or the layer around it. it just didn't support the model, And and That's basically what I want to talk about in the rest of the video. So having said that, let's talk about the first primitive itself, And that is instruction, what does this mean, So you tell the model who it is, you tell it the kind of work that it is doing, you tell it the tone, you tell it the constraints, you tell it the coding styles. you give it some your rules of how to review the code and things that you it should not do

**[4:27]** that becomes the instruction that you're giving to the model and so that's why we should treat that as a primitive this is where AGENTS . md is one form of instruction CLAUDE.md if you're using CLAUDE that fit into this primitive again in the same family you can think of system prompt custom instructions, repository rules that some uh of these agent and agent harnesses support, um, cursor call it cursor rules, So those are all in some form or the other this primitive, this instruction. They are powerful because they move the repeated guidance that you otherwise would have given to the model into the environment itself, So you As a user, don't have to repeat those things over and over again. You don't even have to copy paste that instructions all the time. there is some orchestration, this primitive instruction that uh the harness will take care

**[5:17]** of. And so that's why they say, like, hey, AGENTS.md will automatically be provided um to the model. So Uh instruction are the first harness layer, ? Because they shape the behavior of anything that happens with the model. But there is a limit to what instructions can on its own do, Um, so instructions are uh passive, They can say follow the project convention, but they cannot discover those conventions unless those files are available, for example, they can say be careful with like say the the migrations, um, but they cannot inspect the actual migration um itself, Um, and because the agent can't see it. Instructions help the model to behave better, but they do not give it the entire world.

**[6:10]** You cannot give everything, Um so keeping that in mind, let's see what then the next
<!-- #endregion t-0345 -->

<a id="t-0615"></a><!-- #region t-0615 -->
## [6:15] Context delivery and its impact on model performance.

**[6:15]** primitive would be . And that next one is the context delivery, This context delivery mechanism of the harness gives the model the material that it needs, So you would have used the @ rate symbol to refer to a file Um all of those are in some way or the other this primitive, which is context delivery. This is where you immediately see the difference between like a bare bone model and an agent working inside this harness that has context delivery. so because now you you uh can give it a relevant file, You can give it the failing test, you can give the stack trace, and and now you have a very different animal, And so if earlier you used to ask a model to fix a bug with no files, it would give you a generic fix. But now if you give that source file, you're gonna get a very different answer. But here

**[7:02]** We will now start seeing the limitation of this layer as well. So this alone is also not enough, And so let's see why. so you have instructions and you have a context delivery where you can make it refer to files and logs and docs, ? But dumping that in uh is not on on its own context engineering, you might have a chat that is way too long, sometimes your production incident has logs that are like Too long So if you pour all of that into the model, you are not gonna get some really smart thing. You'll actually see the AI slop as we are all know. because model has a finite context window, So if you start putting everything, it it cannot hold that. into its context window, So even inside that window that that model has the attention is not free. So wrong context sometimes ends up being way much more worse than missing context because

**[7:48]** it gives the model a plausible distraction. So the problem now changes. Like we no longer can ask, can we provide context? I think we start asking who decides what context matters now, and that's an interesting question. Harness is is meant to kind of uh help with that aspect of it.
<!-- #endregion t-0615 -->

<a id="t-0814"></a><!-- #region t-0814 -->
## [8:14] Context management and its role in maintaining focus.

**[8:14]** So yes, we as humans of course play a part in it, but at the same time, there is a lot that harness can do on our behalf, And that brings us to the third primitive, and that is the context management, This is where the management of that context enters, the harness, as you would have seen, does a lot of the stuff to manage that context as to what is the context that the model should be provided. This means that you might have heard of RAG or retrieval augmented generation. It might help in that aspect. uh It might re-rank that thing and figure out which parts of this retrieved chunks to include. It might summarize at a regular interval. When it sees that it's reaching the context limit, it might trigger compaction. You might have heard that word as well. Putting all of these in in order or in in in a way that it assembles this entire context.

**[9:07]** The job basically ends up deciding what enters the model at that particular instance, And that's something small until you try to run a real task, So if a repository is too large and a chat transcript gets too long, if all of that gets dumped into the model, you have not made the agent smarter. You have made the prompt noisier, So popular names for this show up as context compressors, prompt caches, retrieval rankings, session summaries, compaction. The name change, but the job is still how do we protect the model's attention? How do we get the model to focus on the context for it to do the task that we want it to do? the point is simple that harness is uh managing the attention for the model by context management. but The context management makes the agent smarter inside the conversation.

**[10:01]** it can keep the important parts and summarize the stale parts and retrieve the files at the time, avoid spending half the window on on on noisy context, But the agent is still mostly a talker, It can tell what it would do, it can identify the file, It can propose a command to run. It can say the next step is for us to run a failing test. Great. But at some point, that alone is not enough, If the work requires action, the model needs a way to ask the outside world to do something. Someone has to then do that act part that the model has decided or identified at that stage.
<!-- #endregion t-0814 -->

<a id="t-1046"></a><!-- #region t-1046 -->
## [10:46] Tool interfaces and their importance in enabling model actions.

**[10:46]** And that brings us to the next primitive, which is tool interface. Tools give the model a way to act, It's no longer just uh the agent talking. this is like structured action that it will take. A tool would have a name, tool would have a description, It would have schema, um, it may have an output schema as well. And the model decides that I should call this tool with these arguments, That is the model side of the contract, Um, and if you have seen the rise of MCP, it's it's it's this layer, MCP is useful here because it serves as a way to abstract away how these tools are made available to the model. It's the model context protocol. so if anyone any service provider is authoring such mcp mcp servers uh it'll expose their tools to the model for it to then act not just talk so if you have used openai function

**[11:39]** calling uh or anthropic tool use um MCP tools, bash or grep or find you are using this primitive, Now the model is no longer just describing the work. uh it can request actions as well but again this also has uh limitations Um say the model correctly decides I should run the test command. Great. Where? On my laptop, in a container, in a cloud sandbox, with network access, with secrets, with write access to the whole repo. And what about the output? So tools can fail, tools can return messy text. Web pages can contain prompt injection, ? API can return partial data.
<!-- #endregion t-1046 -->

<a id="t-1219"></a><!-- #region t-1219 -->
## [12:19] Execution environments and their role in operational control.

**[12:20]** The model may choose the tool and valid arguments, but the harness still has to answer the operational question, which is where does this run? Under what boundaries, and how much do we trust what comes back? That is the execution environment. And that is our next primitive, so the execution environment is where the tool calls become bounded reality. It's the file system scope, network call. Credentials, sandboxing, containers, browser sessions, cloud workplaces, all of those is what we are putting in this primitive, This is where words that you might have heard of sandbox container, dev container, work tree, browser profile. there are companies that are formed in for this layer as well. Uh Daytona uh is one that comes to E2B is another one that comes to mind. I know Docker now has sandbox, a dev sandbox.

**[13:11]** So this is a primitive that we should be thinking of as well. And it is harness that is providing configuring and collaborating with the tool call and putting it in, and that is what is making it possible basically, this is why running each task in an isolated sandbox matters. It's not just a deployment detail, it is a harness primitive at this stage. And the model can ask to run a command, the harness decides where that command runs, What it can see, what it can change, and what it needs in terms of say human approval. So this layer is also where trust gets practical, we are We are not just telling the model like please do not touch secrets, But instead, at this layer, we can make it such that it does not get secrets, So then environment gives the agent a place to work, but one clean sandbox is not enough

**[13:53]** for long work, real task sometimes pause, they resume, they fork, They fail sometimes. and they need a plan, they need a log, they need to record what was tried, they need uh continuity uh so that the next step is where it starts rather than redoing from scratch,
<!-- #endregion t-1219 -->

<a id="t-1416"></a><!-- #region t-1416 -->
## [14:16] Durable state and its significance in preserving work.

**[14:16]** if the only place where all of this was stored is inside the model context, yeah, if it crashes or if something happens, we lose it, The system needs something much more durable than yeah I think I remember that one. So that brings us to the next primitive that um you would think of when you're creating a custom harness. And that is durable state. So durable state is the workbench that survives the current turn, Plan files, checkpoints, task state, where it is in the task, the the session summaries, Uh logs of what it has done, diff, memory stores, all of these. Right. Context management decides what gets brought into the model now, but the durable state preserves the facts, the artifacts, the progress outside the prompt so that they can survive the current run.

**[15:07]** For coding agents, durable state might be a branch with changes, a test log, a plan document, Or a summary of what failed. For research agents, it might be a source map. Or extracted quotes, a confidence table, The important part is not the storage format. The important part is that the progress becomes inspectable outside the model's current attention, And that is important. Durable state will preserve work, but it does not coordinate the work, A plan file can say what should happen. It does not decide what to retry or when to retry. A lock can be can be recording that a command failed, but it does not decide whether to ask for approval or not. Similarly, a memory can preserve a lesson, but it does not schedule the next run, So once the workflow has lifecycle, state alone clearly is not enough, You need something that

**[16:00]** says start here. Pause there, resume after this, run this check uh after this action, ask the human before the risky step, That part is a whole new primitive, Um and in the agent harness, that primitive will show up as the orchestration, So I have kind of uh zoomed out a little bit here,
<!-- #endregion t-1416 -->

<a id="t-1619"></a><!-- #region t-1619 -->
## [16:19] Orchestration and its role in managing workflows.

**[16:19]** So we now have all the previous ones showing up. Instructions is there, context delivery is there, context management is there, durable state is there, execution environment, model of course is there. And now we have another primitive which is orchestration. Orchestration is the harness deciding how work moves, Life cycle hooks, Heartbeats, as we have seen from OpenClaw and all, retries, approval gates, human handoff, Wrapping the tools, ordering some steps, the task list, routing the model, There is a lot that goes on into this one, So before a tool called do this and after failure, do that, all of that comes becomes part of this particular primitive. Claude code hooks are a great example of this, Agent frameworks expose lifecycle events because real system needs places to intercept the behavior

**[17:08]** The model is not doing all of that by willpower, the harness is carrying the workflow, And it's this particular primitive that is doing the busy work. Um This layer is where the agent work starts to look less like chat and more like a runtime. but as you have seen the pattern. Orchestration helps one agent do more, but one agent still has one attention stream, sometimes you need branches. you might want mid-work someone to go and research something, you know, or go and look inside that Git repository, or draft something on these uh on a separate thing, review the diagrams, uh, verify the browser rendered correctly, If one agent does all of these serially, the process has two issues. One, it becomes very slow because it happens in serial.

**[18:00]** And the second is the context, the thing that we talked about gets crowded, So when work branches, the harness needs to do that branching as well, And that brings us to the next primitive in the harness. and that one is
<!-- #endregion t-1619 -->

<a id="t-1813"></a><!-- #region t-1813 -->
## [18:13] Sub-agents and their function in dividing tasks.

**[18:13]** sub agents. Okay. So not all harness or not all providers uh that are putting out harness even open source one keep this I think if I'm not wrong Pi is a classic example of this where they don't have a built-in sub agent if you want you can add it in Pi but yeah they do serve a purpose Sub-agents let the harness split work into bounded loops. Now, instead of just one of all of those things that we had, no, it's multiple of those. One agent explores the code base, one reviews the diff, one verifies sources, one drafts a plan, you get the point, ? Um, and the main one that fires off all of these things keeps the responsibility for uh integrating all of the output, Um and I think OpenAI's agent SDK has two useful patterns here. One is agents as tools, So we talked about tools already. What if you treat agent as a tool as well?

**[19:07]** And that basically where you end up with the sub agent Where a manager keeps control and calls the specialists and then hands off Where the active conversation moves to a specialist. but that's a primitive the primitive is the capability to fire off and branch off with clean context with with the existing context of the main agent. Um so sub agent is not just more model, it is a model with a narrower job, narrower context, and often narrower tools, Um that's why the term specialists, Um that is why sub agents help Uh as well because they reduce the surface area each worker has to reason about, Remember that whole context and the attention. Well, that's what the harness is doing via this. Yeah, the harness is helping say that don't worry about all of these things, you just worry about these tools, you just worry about this aspect of the work that you need to do,

**[19:59]** and off you go. And then once it comes back, it integrates all of that stuff, Um But delegation creates a new problem, ? If every subagent invents its own process, you get parallel inconsistency. So this is the delegation problem. It feels faster until everyone comes back with a different interpretation of the job that were given to them, So agents
<!-- #endregion t-1813 -->

<a id="t-2020"></a><!-- #region t-2020 -->
## [20:20] Skill layers and their importance in providing reusable procedures.

**[20:20]** Need procedures, They need reusable know-how that can be loaded at the time. And a way that the um a primitive for that helps with this particular aspect is the skill layer, It's the skills and procedures basically. So if these sub-agents are gonna be fired uh to do a very narrow task, wouldn't it be awesome if we can provide uh an exact checklist that it can follow or a procedure that it can follow in a reusable pattern so that every time you want a a narrow sub agent to do that you would just hand off that agent give it a skill off you go so skills are reusable procedures for the recurring work um how to review a PR or a pull request how do you prep for for an for an episode how do you Use a certain Git repository, How do you do browser checks and tests and so on and so forth?

**[21:14]** I think at this stage everyone is very familiar with what skills do, what kind of skills are available. But you will see this as skills, the slash commands, the playbooks and run books and recipes and workflows, but they are all part of this particular primitive, A good skill will encode a workflow, When to use it, what inputs it should should be given, what steps it would follow, in what order, if need be, which tools to prefer, So they make the harness. Less dependent on every agent rediscovering the same process from scratch, They move. repeated expertise from remember to do that thing as instruction into a named capability that the harness can invoke and that's that's important that's why this was a pivotal moment when skill became a thing and of course it became part of our Linux foundation now

**[21:59]** skills make work repeatable but they do not prove the work succeeded A skill can say run the test, but it the pass, It can say check the browser, was the screenshot clean, So the procedure is necessary, but it is not evidence, And so
<!-- #endregion t-2020 -->

<a id="t-2220"></a><!-- #region t-2220 -->
## [22:20] Verification and observability as key components for reliability.

**[22:20]** that primitive is verification and observability. Verification asks for receipts, tests, uh builds, type check, lint, browser screenshot, visual inspection, some sort of evals basically, The the agent would say, I am done, and the harness can then ask, Well, show me. So this is one of the biggest mindset shifts in harness engineering, You do not trust the final sentence because it sounds confident. You ask what external checks can back it up, For coding work, it's easy. Like you want a test to run and and and pass, Um for a presentation, it might be a browser screenshot. With no overlap in text or or so, For research, it might be primary sources and claim table. I remember my first interaction with agent within a harness, of course. Um, when I asked it to do some coding task, it automatically said, like, okay, now let me

**[23:07]** run the test. And I'm like, wow, that is great. I didn't have to say it. And this was even before a skill thing, ? Um, but that's because the harness was written in a in a way that it uh prompted the model to then look for verification as an extra step. and for a very long time that was a differentiating factor, And a lot of people attributed that to the model smartness. And again, that was a component of that. But harness played a big role in that as well. If the harness requires verification, it will guide the model to do so. So in the end, of course, it's a model doing it, but harness played a part in giving it the attention at the time for it to be doing the verification. Right. So looks good to me is is not a verification strategy.

**[23:59]** it basically needs to have some checks and balances, and then harness can play a part in that aspect as well.

<a id="t-2359-observability"></a><!-- #region t-2359-observability -->
Now, verification tells you whether something passed, it does not tell you. why it failed, So a test fails, but was it the context that was wrong? Or did the tool return bad output? Did the agent edit the wrong file? Did a sub agent miss a constraint? Without a run record, debugging becomes hard, And that does not scale, So you need to know what the model saw, what tool it called, what argument it used, what came back and what changed. And that is the observability part, So observability is the recorder for the agent run, Traces, tool call timelines, logs, cost, latency, prompt versions, tool versions, approval events, The full chain of user intent to the final output,

**[24:51]** Um, Bug is often not in the final message, it is in one of these in between steps. It is the three tool calls earlier when the agent searched for the wrong symbol, Or trusted the wrong page or skipped the failing test, Um, and so this observability turns the agent messed up into a debug debuggable system, ? and this matters because you cannot improve what you cannot inspect, and so
<!-- #endregion t-2359-observability -->
<!-- #endregion t-2220 -->

<a id="t-2514"></a><!-- #region t-2514 -->
## [25:14] Evolution of harness engineering and its impact on AI systems.

**[25:14]** Then comes the evolution of the harness itself, This is where failures become infrastructure. A repeated context miss might be pointing at something that you need to add, a retrieval rule, ? A bad tool result becomes a stricter schema. A dangerous command that you saw in your observability becomes a permission gate that you would add after you saw that. A missed edge case that you see from your observability. Becomes a test, a recurring correction that the model has to do might become a memory, And a repeated workflow becomes a skill. What Hermes agent does. This is the agent version of the post mortem loop. Do not just explain the incident, change the system so the class of the failure, same class of failure has a harder time coming back. The point is not to produce a perfect run once.

**[26:07]** point is to make the next run start from a better place. And without this layer, every agent session becomes the same lesson delivered with a new wrapper, if you will, But with it, the harness will compound. So this is when the harness engineering becomes more than agent babysitting, if you will, So If you put all of these together, , all of these components that we have talked about, and then you would go back at the time when the articles were discussing and creating architecture of how Claude code is working, you would then realize that this looks very much like that diagram, This at some level is how Claude Code works, and this at some level is how Codex works, and this at some level is how Gemini CLI works, And it is useful now because it should now uh not look like a random complex thing that

**[26:48]** you see in here. Each primitive that is listed here has a purpose, it has a meaning, it was put there um for a reason. That is the payoff that I wanted you to have, Here's a practical test that I would leave everyone with, When an agent fails, do not only ask, was the model good enough, Ask which harness layer ran out of the road, Was the instruction missing? Was the context wrong? Did the memory go stale? Was it tool schema that was vague? Did the command run in the wrong environment, Did the workflow need state that to be durable, Did it need orchestration? Should it have been delegated? Uh was there no skill? Was there no verification? or did we not have a trace that allowed us to To all that allows us to look inside.

**[27:40]** And did we learn nothing from the last failure? That is the shift. Harness engineering is how we move from clever agents to dependable systems, The model is still important, but reliability gets built in the system around the model. Hope this was helpful. Thank you.
<!-- #endregion t-2514 -->
