# Transcript: Claude Code using the Microsoft Learn MCP server

| Item | Value |
|---|---|
| Session date | 2026-11-17 |
| Host / client | Claude Code CLI, run in a terminal |
| Model | Claude Fable 5.1 (`claude-fable-5-1`), reached by the host through the Anthropic Messages API |
| MCP server | connection name `microsoft-learn`, endpoint `https://learn.microsoft.com/api/mcp`, transport `http` (Streamable HTTP) |
| Working directory | a fresh scratch git repository whose only file was `.mcp.json` |
| Prompts | the three prompts from `demos/adoption/DEMO.md`, typed in order |

This file is the model's own record of the session, written from its context window at the
instructor's request in the fourth turn. It is **live-use evidence** of what the model was shown and
what it produced. The model never sees the JSON-RPC traffic between the host and the server; that
layer is reconstructed in the companion tutorial, `mcp-microsoft-learn-tutorial.md`.

## How to read this transcript

| Marker | Meaning |
|---|---|
| `USER →` | Text typed by the instructor. Reproduced verbatim. |
| `MODEL →` | Text the model wrote for the instructor to read. Final answers are reproduced verbatim. |
| `MODEL ⇒ tool call` | A `tool_use` block the model emitted. The JSON shows the tool name and the arguments object exactly as the model produced them. |
| `HOST ⇒ model` | Material the host placed into the model's context: system-prompt text, tool schemas, tool results. |
| `[abridged: …]` | Content removed from this file, with a note saying what was removed. Nothing else has been edited. |

Tool results that themselves contain Markdown code fences are wrapped in four-backtick fences so
the inner fences survive.

---

## 0. Session start: what the host placed in front of the model

Before the first prompt arrived, the host had already loaded `.mcp.json`, connected to the server,
run the MCP `initialize` handshake, and listed the server's tools. Two traces of that work were
visible to the model.

### 0.1 Server instructions, injected into the system prompt

An MCP server may return an `instructions` string in its `initialize` response. The host placed that
string in the model's system prompt under a heading it generates for every connected server:

```
# MCP Server Instructions

The following MCP servers have provided instructions for how to use their tools and resources:

## microsoft-learn
# Microsoft Learn MCP Server

This server gives structured access to official Microsoft and Azure documentation via three tools:

## Tools

### microsoft_docs_search
Search official documentation and return up to 10 concise, high-quality content chunks (max 500 tokens each), including title, URL, and excerpt.

- Use first to get a quick, reliable overview
- Ideal for grounding answers in Microsoft knowledge

### microsoft_code_sample_search
Search for code snippets and examples in official Microsoft Learn documentation and return up to 20 relevant, high-quality code samples.

- Use when you need to provide sample Microsoft/Azure related code in your answers.
- Ideal for generating code snippets or practical implementation examples.
- Optional parameter `language` can filter results.

### microsoft_docs_fetch
Fetch and convert full Microsoft documentation pages to markdown.

- Use after search when you need full content from a specific URL
- Required for detailed tutorials, troubleshooting, prerequisites, code samples, or when search results are incomplete or outdated

## Workflow

1. Use `microsoft_docs_search` to find relevant documents.
2. If you need code examples or practical snippets, use `microsoft_code_sample_search`.
3. If deeper or complete information is needed, use `microsoft_docs_fetch`.

**Search gives breadth. Code Sample Search gives practical examples. Fetch gives depth.**

All content comes from Microsoft Learn or official sources, returned in clean markdown format.
```

### 0.2 Tool names, registered as deferred tools

The host told the model that these tools existed but did not include their schemas:

```
The following deferred tools are now available via ToolSearch. Their schemas are NOT loaded —
calling them directly will fail with InputValidationError. Use ToolSearch with query
"select:<name>[,<name>...]" to load tool schemas before calling them:
...
mcp__microsoft-learn__microsoft_code_sample_search
mcp__microsoft-learn__microsoft_docs_fetch
mcp__microsoft-learn__microsoft_docs_search
```

Naming pattern: `mcp__` + connection name from `.mcp.json` + `__` + tool name from the server's
`tools/list` response. Other MCP servers connected to this host (for example
`mcp__claude_ai_Claude_Docs__*`) used the same pattern and were not used in this session.

---

## 1. Turn 1: find the Depth documentation

`USER →`

> Use the Microsoft Learn MCP tools to find the official documentation for PowerShell Get-ChildItem. Explain how to limit recursive directory listing depth. Cite the relevant page. Do not execute shell commands.

`MODEL →`

> I'll load the Microsoft Learn MCP tools, search for the Get-ChildItem reference page, and pull the section on limiting recursion depth.

### 1.1 The model loads the two tool schemas (host-internal, not MCP)

`MODEL ⇒ tool call`

```json
{
  "name": "ToolSearch",
  "input": {
    "query": "select:mcp__microsoft-learn__microsoft_docs_search,mcp__microsoft-learn__microsoft_docs_fetch"
  }
}
```

`HOST ⇒ model` (verbatim; each definition arrived as one line of JSON, pretty-printed here)

```
<functions>
<function>
```
```json
{
  "description": "Search official Microsoft/Azure documentation to find the most relevant and trustworthy content for a user's query. This tool returns up to 10 high-quality content chunks (each max 500 tokens), extracted from Microsoft Learn and other official sources. Each result includes the article title, URL, and a self-contained content excerpt optimized for fast retrieval and reasoning. Always use this tool to quickly ground your answers in accurate, first-party Microsoft/Azure knowledge.\n\n## Follow-up Pattern\nTo ensure completeness, use microsoft_docs_fetch when high-value pages are identified by search. The fetch tool complements search by providing the full detail. This is a required step for comprehensive results.",
  "name": "mcp__microsoft-learn__microsoft_docs_search",
  "parameters": {
    "properties": {
      "query": {
        "default": null,
        "description": "a query or topic about Microsoft/Azure products, services, platforms, developer tools, frameworks, or APIs",
        "type": "string"
      }
    },
    "type": "object"
  }
}
```
```
</function>
<function>
```
```json
{
  "description": "Fetch and convert a Microsoft Learn documentation webpage to markdown format. This tool retrieves the latest complete content of Microsoft documentation webpages including Azure, .NET, Microsoft 365, and other Microsoft technologies.\n\n## When to Use This Tool\n- When search results provide incomplete information or truncated content\n- When you need complete step-by-step procedures or tutorials\n- When you need troubleshooting sections, prerequisites, or detailed explanations\n- When search results reference a specific page that seems highly relevant\n- For comprehensive guides that require full context\n\n## Usage Pattern\nUse this tool AFTER microsoft_docs_search when you identify specific high-value pages that need complete content. The search tool gives you an overview; this tool gives you the complete picture.\n\n## URL Requirements\n- The URL must be a valid HTML documentation webpage from the microsoft.com domain\n- Binary files (PDF, DOCX, images, etc.) are not supported\n\n## Output Format\nmarkdown with headings, code blocks, tables, and links preserved.",
  "name": "mcp__microsoft-learn__microsoft_docs_fetch",
  "parameters": {
    "properties": {
      "url": {
        "description": "URL of the Microsoft documentation page to read",
        "type": "string"
      }
    },
    "required": ["url"],
    "type": "object"
  }
}
```
```
</function>
</functions>
```

Compare these with the server's own `tools/list` output in `demos/adoption/evidence/remote.json`.
The host renamed each tool with the `mcp__microsoft-learn__` prefix, renamed `inputSchema` to
`parameters`, passed `description` through unchanged, and dropped `title`, `outputSchema`, and
`annotations` from what the model sees.

`USER →`

> Tool loaded.

(A short user-role message acknowledging the schema load. It is not part of the MCP exchange.)

### 1.2 The model calls search and fetch in one response

`MODEL ⇒ tool call` (two `tool_use` blocks in the same response, so the host could run them concurrently)

```json
[
  {
    "name": "mcp__microsoft-learn__microsoft_docs_search",
    "input": {
      "query": "PowerShell Get-ChildItem -Depth parameter limit recursion"
    }
  },
  {
    "name": "mcp__microsoft-learn__microsoft_docs_fetch",
    "input": {
      "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem"
    }
  }
]
```

### 1.3 The host returns both results

`HOST ⇒ model` (outer wrapper exactly as presented; payloads abridged)

````
<result>
<name>mcp__microsoft-learn__microsoft_docs_search</name>
<output>{"results":[{"title":"Get-ChildItem-Description","content":"# Get-ChildItem\r\n\r\n- Module:\r\n    - [Microsoft.PowerShell.Management Module](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/?view=powershell-7.6)\r\n\r\nGets the items and child items in one or more specified locations.\r\n\r\n## Description\r\n\r\n ... [abridged] ... ","contentUrl":"https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6"}, ... ]}</output>
</result>
<result>
<name>mcp__microsoft-learn__microsoft_docs_fetch</name>
<output># Get-ChildItem

- Module:
    - [Microsoft.PowerShell.Management Module](./?view=powershell-7.6)

Gets the items and child items in one or more specified locations.
 ... [abridged] ...
</output>
</result>
````

**Search payload**, pretty-printed. The `output` was a single JSON object serialized as text. Ten
chunks came back. Every chunk pointed at the same page. Two chunks are shown; `\r\n` sequences are
preserved as they arrived.

```jsonc
{
  "results": [
    {
      "title": "Get-ChildItem-Description",
      "content": "# Get-ChildItem\r\n\r\n- Module:\r\n    - [Microsoft.PowerShell.Management Module](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/?view=powershell-7.6)\r\n\r\nGets the items and child items in one or more specified locations.\r\n\r\n## Description\r\n\r\nThe `Get-ChildItem` cmdlet gets the items in one or more specified locations. If the item is a container, it gets the items inside the container, known as child items. You can use the **Recurse** parameter to get items in all child containers and use the **Depth** parameter to limit the number of levels to recurse.\r\n\r\n ... [abridged: second Description paragraph] ... \r\n\r\n## Parameters\r\n\r\n### -Depth\r\n\r\n#### Parameter properties\r\n\r\n|  |  |\r\n| --- | --- |\r\n| Type: | [UInt32](https://learn.microsoft.com/en-us/dotnet/api/system.uint32) |\r\n| Default value: | None |\r\n| Supports wildcards: | False |\r\n| DontShow: | False |\r\n\r\n ... [abridged: Parameter sets table, Notes section] ...",
      "contentUrl": "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6"
    },
    {
      "title": "Get-ChildItem-Description",
      "content": " ... [abridged: page header and Description] ... ## Examples\r\n\r\n### Example 8: Get items using the Depth parameter\r\n\r\nThis example displays the items in a directory and its subdirectories. The **Depth** parameter determines the number of subdirectory levels to include in the recursion. Empty directories are excluded from the output.\r\n\r\n```powershell\r\nGet-ChildItem -Path C:\\Parent -Depth 2\r\n```\r\n\r\n ... [abridged: Output block] ... \r\n\r\nThe `Get-ChildItem` cmdlet uses the **Path** parameter to specify `C:\\Parent`. The **Depth** parameter specifies two levels of recursion. `Get-ChildItem` displays the contents of the directory specified by the **Path** parameter and the two levels of subdirectories.\r\n\r\n ... [abridged: Notes section] ...",
      "contentUrl": "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6"
    }
    // [abridged: 8 more chunks. Titles alternate between "Get-ChildItem-Description" and
    //  "Get-ChildItem-Syntax". Each chunk repeats the page header, the Description, and the Notes
    //  section around one Parameter or Example section (-Include, -Exclude, -Path, -Eku, Example 9,
    //  Example 13, the Items syntax block, the LiteralItems syntax block). All share the contentUrl above.]
  ]
}
```

**Fetch payload.** The `output` was the whole reference page converted to Markdown. The course's
LLM-free client measured an equivalent fetch of this page at about 42,000 characters
(`demos/adoption/evidence/remote.json`). The sections the model relied on are kept verbatim.

````markdown
# Get-ChildItem

- Module:
    - [Microsoft.PowerShell.Management Module](./?view=powershell-7.6)

Gets the items and child items in one or more specified locations.

## Syntax

### Items (Default)

```Syntax
Get-ChildItem
    [[-Path] <string[]>]
    [[-Filter] <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Recurse]
    [-Depth <uint>]
    [-Force]
    [-Name]
    [<CommonParameters>]
```

[abridged: LiteralItems syntax block]

## Description

The `Get-ChildItem` cmdlet gets the items in one or more specified locations. If the item is a container, it gets the items inside the container, known as child items. You can use the **Recurse** parameter to get items in all child containers and use the **Depth** parameter to limit the number of levels to recurse.

[abridged: second Description paragraph; Examples 1 through 7]

### Example 8: Get items using the Depth parameter

This example displays the items in a directory and its subdirectories. The **Depth** parameter determines the number of subdirectory levels to include in the recursion. Empty directories are excluded from the output.

```powershell
Get-ChildItem -Path C:\Parent -Depth 2
```

```Output
    Directory: C:\Parent

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/14/2019     10:24                SubDir_Level1
-a----        2/13/2019     08:55             26 file.txt

    Directory: C:\Parent\SubDir_Level1

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/14/2019     10:24                SubDir_Level2
-a----        2/13/2019     08:55             26 file.txt

    Directory: C:\Parent\SubDir_Level1\SubDir_Level2

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/14/2019     10:22                SubDir_Level3
-a----        2/13/2019     08:55             26 file.txt
```

The `Get-ChildItem` cmdlet uses the **Path** parameter to specify `C:\Parent`. The **Depth** parameter specifies two levels of recursion. `Get-ChildItem` displays the contents of the directory specified by the **Path** parameter and the two levels of subdirectories.

[abridged: Examples 9 through 13; Parameters -Attributes and -CodeSigningCert]

### -Depth

This parameter was added in PowerShell 5.0 and enables you to control the depth of recursion. By default, `Get-ChildItem` displays the contents of the parent directory. The **Depth** parameter determines the number of subdirectory levels that are included in the recursion and displays the contents.

For example, `-Depth 2` includes the **Path** parameter's directory, first level of subdirectories, and second level of subdirectories. By default directory names and filenames are included in the output.

Note

On a Windows computer from PowerShell or **cmd.exe**, you can display a graphical view of a directory structure with the **tree.com** command.

#### Parameter properties

| Type: | [UInt32](/en-us/dotnet/api/system.uint32) |
| --- | --- |
| Default value: | None |
| Supports wildcards: | False |
| DontShow: | False |

[abridged: Parameter sets table; remaining parameters -Directory through -System, including
-FollowSymlink ("introduced in PowerShell 6.0", FileSystem provider only); CommonParameters;
Inputs; Outputs]

## Notes

PowerShell includes the following aliases for `Get-ChildItem`:

- All platforms:
    - `dir`, `gci`
- Windows:
    - `ls`

**Recursion behavior with the `-Path` parameter:**

When you use `Get-ChildItem -Recurse` with the **Path** parameter, the cmdlet searches for the last path component whether or not it's a wildcard pattern or a literal name.

[abridged: four bullets on Path and Name behavior]

You should avoid using the **Path** parameter with the **Recurse** parameter. For best results:

- Use **LiteralPath** to specify the target directory to avoid triggering a recursive search for the last path component.
- Use **Filter** or **Include** parameters to specify wildcard or literal patterns that should be searched for in every level of the target directory's hierarchy.

[abridged: Related Links]
````

### 1.4 The model's answer

`MODEL →` (verbatim)

---

The official page confirms everything needed, so no further lookups are required.

**Use the `-Depth` parameter.** It limits how many subdirectory levels Get-ChildItem descends into, and it implies recursion on its own, so you do not need to add `-Recurse` alongside it.

How it works, per the official reference:

- **Counting starts at the target directory.** The documentation says `-Depth 2` returns the directory given in Path, its first level of subdirectories, and its second level of subdirectories. Nothing deeper is listed.
- **Added in PowerShell 5.0.** On older versions the parameter does not exist and you would have to filter paths manually.
- **Type is an unsigned integer.** Negative values are rejected. A value of zero lists only the immediate contents of the target directory.
- **Empty directories are omitted** from the output in the depth-limited listing, as noted under Example 8.

The documented example:

```powershell
Get-ChildItem -Path C:\Parent -Depth 2
```

This prints the contents of C:\Parent, then C:\Parent\SubDir_Level1, then C:\Parent\SubDir_Level1\SubDir_Level2, and stops there. SubDir_Level3 appears as an entry inside Level2 but its contents are never enumerated.

Two related points from the same page worth knowing:

- **Prefer LiteralPath over Path when recursing.** The Notes section warns that combining Path with Recurse can trigger a recursive search for the last path component rather than a plain enumeration. Using LiteralPath for the directory and Filter or Include for the pattern avoids that surprise, and the same advice applies when Depth drives the recursion.
- **Symbolic links are not followed by default.** Add `-FollowSymlink` if you want link targets traversed. It is FileSystem-provider only and was introduced in PowerShell 6.0.

**Source:** Get-ChildItem reference, Microsoft.PowerShell.Management module, Microsoft Learn (PowerShell 7.6 view). Relevant sections are the Description paragraph, Example 8 ("Get items using the Depth parameter"), the `-Depth` parameter entry, and the Notes section on recursion behavior.
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6

---

---

## 2. Turn 2: fetch the article and check the Depth section

`USER →`

> Use the Microsoft Learn fetch tool to open the relevant article and check the Depth parameter section against your explanation.

`MODEL →`

> I'll re-fetch the Get-ChildItem article and compare the Depth section word for word against what I wrote.

### 2.1 One fetch call

`MODEL ⇒ tool call`

```json
{
  "name": "mcp__microsoft-learn__microsoft_docs_fetch",
  "input": {
    "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6"
  }
}
```

No schema load was needed this time. The two schemas loaded in Turn 1 stayed in the model's context.

### 2.2 The host returns the page

`HOST ⇒ model`

The same page as in Turn 1, byte for byte identical in every section the model compared. The
`-Depth` section is reproduced in 1.3 above and is not repeated here.

### 2.3 The model's answer

`MODEL →` (verbatim)

---

The Depth section matches my explanation on every documented point. Three of my statements went beyond what that section actually says, and I should flag them.

**What the Depth parameter section states, and how my explanation held up:**

- **Added in PowerShell 5.0.** Confirmed verbatim.
- **Counting includes the starting directory.** The section says `-Depth 2` includes the Path directory, the first level of subdirectories, and the second level. My description matched this exactly.
- **Type is UInt32, default value None, no wildcards.** Confirmed in the parameter properties table.
- **Directory names and filenames are both included by default.** Confirmed. I did not state this explicitly before, so it is a small omission.
- **Note about tree.com.** The section adds that on Windows you can get a graphical directory view with the tree.com command. I left this out.

**Claims I made that the Depth section does not state:**

- **Depth implies recursion without -Recurse.** The parameter text never says this. It is supported only by Example 8, where `Get-ChildItem -Path C:\Parent -Depth 2` recurses with no Recurse switch in the command. So the claim is grounded in the page, but in the example rather than the parameter definition.
- **Negative values are rejected.** This follows from the UInt32 type but is not written anywhere on the page. It is an inference.
- **Depth 0 lists only the immediate contents.** The page does not document this value at all. I extrapolated it from the counting rule. Treat it as plausible but unverified against official text.
- **LiteralPath advice applies to Depth.** The Notes section frames that guidance around Recurse specifically. Extending it to Depth was my reasoning, not the documentation's wording.

**Items confirmed elsewhere on the page:** empty directories excluded from output is stated in Example 8, and FollowSymlink details match the FollowSymlink parameter section.

**Source checked:** Get-ChildItem reference, Microsoft.PowerShell.Management module, PowerShell 7.6 view.
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6

---

---

## 3. Turn 3: find how to include hidden items

`USER →`

> Use Microsoft Learn MCP documentation tools to find how Get-ChildItem can include hidden items. Cite the relevant documentation. Do not execute commands.

`MODEL →`

> I'll search Microsoft Learn for the hidden-item behavior and also pull the FileSystem provider article, since the Hidden and Attributes parameters are provider-specific.

### 3.1 Search and fetch in one response

`MODEL ⇒ tool call` (two `tool_use` blocks in the same response)

```json
[
  {
    "name": "mcp__microsoft-learn__microsoft_docs_search",
    "input": {
      "query": "Get-ChildItem show hidden files -Force -Hidden -Attributes"
    }
  },
  {
    "name": "mcp__microsoft-learn__microsoft_docs_fetch",
    "input": {
      "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6"
    }
  }
]
```

### 3.2 The host returns both results

`HOST ⇒ model`

**Search payload.** Ten chunks again, this time from five different pages. Listed by position, with
the one excerpt the model quoted:

| # | title | contentUrl |
|---|---|---|
| 1 | Working with files, folders and registry keys | https://learn.microsoft.com/powershell/scripting/samples/working-with-files-folders-and-registry-keys?view=powershell-7.6 |
| 2 | Working with files and folders | https://learn.microsoft.com/powershell/scripting/samples/working-with-files-and-folders?view=powershell-7.6 |
| 3 | about_FileSystem_Provider | https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6#dynamic-parameters |
| 4 | about_FileSystem_Provider | same page, `#dynamic-parameters` anchor |
| 5 | Get-ChildItem-Description | https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6 (Example 3 chunk) |
| 6 | Get-ChildItem-Description | same page (Example 1 chunk) |
| 7 | about_FileSystem_Provider | same page, `#getting-files-and-folders-with-specified-attributes` anchor |
| 8 | Working with files, folders and registry keys | same page, `#enumerating-files,-folders,-and-registry-keys` anchor |
| 9 | GetChildItem.Hidden Property-Definition | https://learn.microsoft.com/dotnet/api/microsoft.powershell.management.activities.getchilditem.hidden?view=powershellsdk-1.1.0 |
| 10 | Get-ChildItem-Description | get-childitem page (-Attributes chunk) |

Chunk 1, the part the model quoted:

```jsonc
{
  "title": "Working with files, folders and registry keys",
  "content": " ... [abridged] ... ### Forcibly listing hidden items\nItems that are hidden in File Explorer or `cmd.exe` aren't displayed in the output of a `Get-ChildItem` command. To display hidden items, use the **Force** parameter of `Get-ChildItem`. For example:\n```powershell\nGet-ChildItem -Path C:\\Windows -Force\n```",
  "contentUrl": "https://learn.microsoft.com/powershell/scripting/samples/working-with-files-folders-and-registry-keys?view=powershell-7.6"
}
```

**Fetch payload.** The full `about_FileSystem_Provider` article as Markdown. The two sections the
model used are kept verbatim.

````markdown
# about_FileSystem_Provider

[abridged: Provider name, Drives, Capabilities, Short description, Detailed description, Types
exposed, Navigating, Getting files and directories, Copying, Moving, Managing file content,
Managing security descriptors, Creating, Renaming, Deleting, Invoking]

## Getting files and folders with specified attributes

[abridged: Get System files]

### Get Hidden files

This command gets all files, including hidden files, in the current directory.

It uses the **Attributes** parameter with two values, `!Directory+Hidden`, which gets hidden files, and `!Directory`, which gets all other files.

```powershell
Get-ChildItem -Attributes !Directory,!Directory+Hidden
```

`dir -Att !d,!d+h` is the equivalent of this command.

[abridged: Get Compressed and Encrypted files]

## Dynamic parameters

Dynamic parameters are cmdlet parameters that are added by a PowerShell provider and are available only when the cmdlet is being used in the provider-enabled drive.

[abridged: Encoding, Delimiter, Wait]

### Attributes <FlagsExpression>

Gets files and folders with the specified attributes. This parameter supports all attributes and lets you specify complex combinations of attributes.

The **Attributes** parameter was introduced in Windows PowerShell 3.0.

[abridged: list of fourteen attribute names]

Use the following operators to combine attributes.

- `!` - NOT
- `+` - AND
- `,` - OR

No spaces are permitted between an operator and its attribute. However, spaces are permitted before commas.

[abridged: Directory, File]

### Hidden <SwitchParameter>

Gets only hidden files and directories (folders). By default, `Get-ChildItem` gets only non-hidden items.

The **Hidden** parameter was introduced in Windows PowerShell 3.0.

To get only hidden items, use the **Hidden** parameter, its `h` or `ah` aliases, or the **Hidden** value of the **Attributes** parameter. To exclude hidden items, omit the **Hidden** parameter or use the **Attributes** parameter.

#### Cmdlets supported

- `Get-ChildItem`

[abridged: ReadOnly, System, NewerThan, OlderThan, Stream, Raw, ItemType; Using the pipeline;
Getting help]
````

The model also drew on the Get-ChildItem reference page already in its context from Turns 1 and 2.
The `-Force` entry there reads: "Allows the cmdlet to get items that otherwise can't be accessed by
the user, such as hidden or system files. The **Force** parameter doesn't override security
restrictions. Implementation varies by provider." The `-Hidden` entry reads: "To get only hidden
items, use the **Hidden** parameter or the **Attributes** parameter with the **Hidden** property. By
default, `Get-ChildItem` doesn't display hidden items. Use the **Force** parameter to get hidden
items." Aliases listed: `ah`, `h`.

### 3.3 The model's answer

`MODEL →` (verbatim)

---

No further lookups are needed. The reference page, the FileSystem provider article, and a Microsoft sample article together cover all three documented approaches.

**Use `-Force` to see hidden items alongside everything else.** This is the plain answer for "show me the full listing." The Get-ChildItem reference describes Force as allowing the cmdlet to get items that otherwise cannot be accessed by the user, such as hidden or system files, and notes it does not override security restrictions. Example 3 on the same page shows it in action:

```powershell
Get-ChildItem -Path .\*.txt -Recurse -Force
```

The example output includes a file whose Mode column shows the `h` flag, which the page identifies as the hidden attribute.

The sample article "Working with files, folders and registry keys" states the default behavior directly: items hidden in File Explorer or cmd.exe are not displayed by Get-ChildItem, and you add Force to display them.

**Two other documented options behave differently from Force:**

- **`-Hidden` returns only hidden items, not hidden plus normal.** The reference page says to use Hidden to get only hidden items and reiterates that Force is the way to get hidden items added to a normal listing. Aliases are `h` and `ah`. The FileSystem provider article adds that it was introduced in Windows PowerShell 3.0.
- **`-Attributes` lets you build a custom filter that includes Hidden.** The provider article gives this example for all files including hidden ones, where `,` means OR, `+` means AND, and `!` means NOT:

```powershell
Get-ChildItem -Attributes !Directory,!Directory+Hidden
```

The article notes the abbreviated form `dir -Att !d,!d+h` is equivalent. No spaces are allowed between an operator and its attribute.

**Provider scope matters.** Hidden and Attributes are dynamic parameters that the FileSystem provider adds, so they only exist when you are working against a file system drive. Force is a core parameter available across providers, though the reference page says its implementation varies by provider.

**Sources:**

- Get-ChildItem reference, Microsoft.PowerShell.Management module, PowerShell 7.6 view. See Example 3, the `-Force` parameter entry, the `-Hidden` parameter entry, and the `-Attributes` parameter entry.
  https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6
- about_FileSystem_Provider, PowerShell 7.6 view. See "Get Hidden files" under "Getting files and folders with specified attributes," and the Hidden and Attributes entries under "Dynamic parameters."
  https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6
- Working with files, folders and registry keys, PowerShell 7.6 view. See "Forcibly listing hidden items."
  https://learn.microsoft.com/powershell/scripting/samples/working-with-files-folders-and-registry-keys?view=powershell-7.6

---

---

## 4. Turn 4: produce this transcript and the tutorial

`USER →` asked for this transcript and a companion tutorial, placed in
`demos/claude-session/`, aligned with the "Follow the task" message sequence chart in
`slides/lecture-mcp-adoption.md`.

No MCP calls were made in this turn. The model used the host's local file tools to read the slide
source, the chart's Mermaid source (`slides/diagrams/adoption-call.mmd`), the LLM-free discovery
capture (`demos/adoption/evidence/remote.json`), the demo notes, and the scratch repository's
`.mcp.json`, then wrote the two files.

---

## 5. Summary of every MCP tool call in the session

| Turn | Tool (server name) | Arguments | Result shape | Approx. size |
|---|---|---|---|---|
| 1 | `microsoft_docs_search` | `{"query": "PowerShell Get-ChildItem -Depth parameter limit recursion"}` | JSON object, `results[10]` of `{title, content, contentUrl}` | tens of KB |
| 1 | `microsoft_docs_fetch` | `{"url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem"}` | Markdown text of the page | ~42 KB |
| 2 | `microsoft_docs_fetch` | `{"url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6"}` | Markdown text of the page | ~42 KB |
| 3 | `microsoft_docs_search` | `{"query": "Get-ChildItem show hidden files -Force -Hidden -Attributes"}` | JSON object, `results[10]` from five pages | tens of KB |
| 3 | `microsoft_docs_fetch` | `{"url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6"}` | Markdown text of the page | tens of KB |

Sizes are approximate. The ~42 KB figure is the LLM-free client's measurement of an equivalent fetch
recorded in `demos/adoption/evidence/remote.json`; the model cannot measure its own inputs exactly.
`microsoft_code_sample_search` was discovered but never called.
