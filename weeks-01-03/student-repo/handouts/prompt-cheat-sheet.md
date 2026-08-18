# Prompting Cheat Sheet

>Built for Claude models, but may include standard prompting engineering 
> guidelines that can be applied with other models. Many of these are 
> variations of recommendations from [Claude Best Practices](https://code.claude.com/docs/en/best-practices)

Prompting is the single best way to influence the output of an LLM. 
Here are Prompt Engineering principles to consider when constructing a 
prompt. 

## Provide Specific Instructions

Claude can't read your mind. Whenever possible, provide details relevant 
to the task to Claude. 


__Base__: `Review the code`

__Better__: `Conduct a review of the new Login Feature. Consider both 
security risks and user experience.`


__Base__: `Fix the bug with the new login UI`

__Better__: `When using the new login UI, the submit request does not seem to go through. Double
check that the submit request is being handled properly so the page reacts correctly.`

## Spec-driven Development

For large scale or complex tasks, consider using a spec to help guide
development. This could be a Concept of Operations, derived from 
assignment instructions, or manually generated to give specific form
to the piece of software you are trying to develop.

__Base__: `Add a new login page to our website`

__Better__: `Use the login section in @website-spec to implement the login page`

## Give Claude the tools to check itself (and encourage their use)

Along with developing tests with your project, allowing Claude to check its own
work will produce more reliable code. 

__Base__: `Add a new login page to our website`

__Better__: `Add a new login page to our website. Use the unit tests to check your implementation. Use the website tools at your disposal (playwright mcp) to verify the UI of the page.`


## Instead of restricting Claude, Promote positive behaviors

By encouraging desirable behavior, you may observe a more natural and coherent 
output. While there are still times to discourage behavior, encouraging other behaviors
will allow the LLM to still exercise its full ability to accomplish its task.

__Base__: `Don't use bulleted lists in the code report`

__Better__: `Strive to use complete paragraphs that flow together when writing the code report`

## Point Claude to existing patterns

Rather than describing a feature from scratch, point Claude at code that already solves 
a similar problem. This keeps new work consistent with your codebase and encourages 
reuse over reinvention.

__Base__: `Add a calendar widget to the dashboard`

__Better__: `Look at how the existing widgets on the dashboard are built (@HotDogWidget is a good example). Follow that same pattern to add a calendar widget, using only the libraries already in the project.`
