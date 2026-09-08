# Chapter 7 — Skills: reusable procedures the model loads on demand

By the end of chapter 6 the agent manages a finite window, but it still starts every session without repository-specific procedures. This stage adds skills: reusable procedures stored as files, advertised to the model through short descriptions, and loaded in full only when the model requests one. The walkthrough calls this "operational memory via progressive disclosure." In concrete terms, *operational memory* is a persisted procedure, while *progressive disclosure* means that only its summary is always present in context and its full text is loaded on demand.

## The primitive

A skill is a directory containing a `SKILL.md` file: YAML frontmatter with a `name` and a `description`, followed by a body of instructions — the agentskills.io layout. The module docstring in [harness/skills.py](../stages/ch-07-skills/harness/skills.py) draws the boundary against the previous primitives precisely: "Skills are not tools — a tool is a capability ('run pytest'), a skill is a procedure ('how we cut a release')." A tool extends what the agent *can do*; a skill records *how we do things here* — the release checklist, the sign-off convention, the migration recipe.

Call it memory because it behaves like memory. The conversation history (chapter 2) is episodic — it remembers this session and dies with it. `AGENTS.md` (chapter 3) is standing policy, injected whole every turn. Skills are procedural knowledge that outlives any session: they live in the repo, they're versioned in git, and anyone who clones the project gets the same operational memory. The model's weights never change; the harness turns the filesystem into a memory the model can consult.

Progressive disclosure is the delivery discipline that makes this memory affordable inside the finite window chapter 6 just taught us to respect. The window holds a *menu*, not every recipe: each skill costs one line of system prompt (name + description + file path), and the full body costs nothing until the model reads it — with the `read_file` tool it has had since chapter 5. It is the complementary move to compaction: chapter 6 shrinks what is already in the window; chapter 7 keeps things out of the window until they're needed.

This has to live in the harness. The harness owns prompt assembly, so it is the only place the menu can be built; it owns the filesystem convention, so it decides what counts as a skill and where skills live. What is genuinely new here is how little machinery the primitive needs: no new tool, no change to the drive loop's control flow — just a file layout, a loader, and one more part in the instruction layer. The model supplies the judgment (does this skill apply?) and the existing capability (read the file); the harness supplies discovery and advertisement.

## From the video

The segment opens at [16:58](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1018s) by naming the loose end chapter 6 left: managing the window keeps the agent sharp, but "it still rederives the same procedures every time" — it has no memory of how things are done in this repository. Skills give it "an operational memory," and the author compresses the tool/skill distinction into one line at [17:15](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1035s): "a tool is a verb, a skill is a procedure."

The mechanism is named at [17:29](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1049s): "So here's the trick: progressive disclosure. We advertise only the one-line description in the prompt." The full body stays on disk until the model decides it is relevant, and then it reads it with the read-file tool it already has. After this change three things load automatically at the start of every turn: the built-in system prompt, the `AGENTS.md` from chapter 3, and now the skills — "not the entire skill, only the description and the name."

The demo at [18:27](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1107s) is built to be its own proof. The author asks the agent to use the sign-off skill; the agent reads `SKILL.md` and ends its reply with a codeword that appears nowhere else — not in the system prompt, not in `AGENTS.md`, not in the transcript so far. "That is the proof that it loaded the body itself, not from anything we had pre-injected." The segment closes at [19:26](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1166s) by pointing at the next gap: the agent can now follow procedures, "but what about running code that we don't fully trust on our own machine?" — that is chapter 8's problem.

## The code

### Integration with the instruction layer

Start where the loop changes, because it changes in exactly one place. In
[harness/agent.py](../stages/ch-07-skills/harness/agent.py) the constructor grows a
`skills: list[Skill] | None = None` parameter. The constructor stores `skills or []`, so either
`None` or an empty list produces a new empty list; a non-empty caller list is retained rather than
copied. `_system_text` — the instruction layer from chapter 3 — joins a third part:

```python
    def _system_text(self) -> str:
        """Instruction layer = system prompt + project AGENTS.md + skills menu."""
        parts = [
            p
            for p in (
                self.system,
                load_agents_md(self.agents_dir),
                skills_prompt(self.skills),
            )
            if p
        ]
        return "\n\n".join(parts)
```

Everything else in the loop — the managed window, `@path` injection, tools behind the approval
gate, and repeated `chat` calls through the `model/` seam — is untouched. The REPL's `main()` wires
the convention in with `skills=load_skills("skills")`, so any `skills/<name>/SKILL.md` under the
working directory is discovered at startup. Passing skills without also advertising a usable
`read_file` tool produces a menu the model cannot follow; the constructor does not enforce that
cross-interface dependency.

### Skill metadata and loader interfaces

The new module, [harness/skills.py](../stages/ch-07-skills/harness/skills.py), is 66 lines and has three moving parts. A `Skill` is a dataclass of `name`, `description`, and `path`. The loader scans one directory level for the agentskills.io layout:

| Interface | Inputs | Return value | Failure behavior |
|---|---|---|---|
| `Skill(name, description, path)` | Two strings and a `Path`. | Mutable metadata object; it does not load the body. | Dataclasses do not validate field types at runtime. |
| `_parse_frontmatter(text)` | Complete file text. | Top-level string key/value dictionary from the leading fenced block. | Missing opening fence returns `{}`; missing closing fence parses through EOF; malformed lines are ignored. |
| `load_skills(directory)` | String or `Path` root. | Sorted list of one `Skill` per immediate `*/SKILL.md`. | Missing/non-directory root returns `[]`; a discovered unreadable or undecodable file raises. |
| `skills_prompt(skills)` | Skill list. | Menu string, or `""` for no skills. | Does not read or validate body paths. |

```python
def load_skills(directory: str | Path) -> list[Skill]:
    """Load skills from ``<directory>/<name>/SKILL.md`` (agentskills.io layout)."""
    root = Path(directory)
    if not root.is_dir():
        return []
    skills = []
    for skill_md in sorted(root.glob("*/SKILL.md")):
        meta = _parse_frontmatter(skill_md.read_text())
        skills.append(
            Skill(
                name=meta.get("name", skill_md.parent.name),
                description=meta.get("description", ""),
                path=skill_md,
            )
        )
    return skills
```

`root.glob("*/SKILL.md")` means exactly one directory level below `root`; a file placed directly at
`skills/SKILL.md` or two levels down is not discovered. `sorted(...)` makes menu order stable by
path rather than depending on filesystem iteration order.

`_parse_frontmatter` is a deliberately tiny hand-rolled parser: `splitlines()` separates the text;
the first stripped line must equal `---`; the loop stops at the next fence; `partition(":")` splits
only at the first colon and returns the left side, separator, and remainder. It reads top-level
`key: value` pairs and skips indented lines, so a nested metadata map does not become a false
top-level field. This is not general YAML: quotes remain part of values, comments are not removed,
and lists, folded blocks, duplicate-key rules, and type conversion are unsupported. A file with
missing or unrecognized metadata falls back to the directory name and an empty description, but
filesystem read errors still propagate.

### Menu rendering and progressive disclosure

`skills_prompt` renders the menu, and its wording carries the whole protocol — it tells the model which tool closes the loop and hands it the exact path to read:

```python
def skills_prompt(skills: list[Skill]) -> str:
    if not skills:
        return ""
    lines = [
        "You have skills available. When one applies, use the read_file tool to "
        "read its file, then follow it exactly:"
    ]
    lines += [f"- {s.name}: {s.description} (file: {s.path})" for s in skills]
    return "\n".join(lines)
```

The stage ships one skill, [skills/sign-off/SKILL.md](../stages/ch-07-skills/skills/sign-off/SKILL.md), engineered as an experiment rather than a real procedure:

```markdown
---
name: sign-off
description: Sign off a reply for the secret project. Use when the user asks to "sign off", to use the sign-off skill, or to end a message for the secret project.
---

# Sign-off procedure

When the user asks you to sign off (or to use the sign-off skill):

1. Answer their request normally.
2. On the final line, append the project codeword exactly: **Haila!**

The codeword lives only in this file — never guess it. If you have not read this
skill, you do not know it.
```

Note the two roles the file's two halves play. The description is the *routing signal* — it enumerates the phrasings that should trigger the skill, because that one line is all the model sees when deciding. The body is the *payload* — and it contains a fact (`Haila!`) that exists nowhere else, which is what makes the acceptance check falsifiable.

At runtime a full round trip looks like this: the user says "use the sign-off skill"; the system message already contains the menu line `- sign-off: … (file: skills/sign-off/SKILL.md)`; the model emits a `read_file` tool call with that path; the harness runs it (reads aren't in the `approval_required` set, so no gate fires), clamps the result with chapter 6's door control, and appends it as a tool message; on the next model call the body is in context and the reply ends with the codeword.

The `Skill.path` field is therefore **deferred state**: loading metadata records where the body can
be found but does not read or inject that body. The later `read_file` call crosses the deferral
boundary. A deleted or moved file remains advertised until restart and then fails through the tool
result channel when selected.

### Offline tests and live acceptance evidence

The offline gate, [tests/episodes/test_ch07.py](../stages/ch-07-skills/tests/episodes/test_ch07.py), proves the harness half deterministically. One test checks loading and — crucially — non-disclosure:

```python
def test_load_and_prompt(tmp_path):
    _write_skill(tmp_path, "foo", "does foo")
    skills = load_skills(tmp_path)
    assert skills[0].name == "foo"
    assert "does foo" in skills[0].description
    prompt = skills_prompt(skills)
    assert "read_file" in prompt and "foo" in prompt
    # the body is NOT advertised — only the description
    assert "body here" not in prompt
```

The second test patches `chat` with a fake and asserts the outgoing system message contains both the base prompt and the skill name — advertisement verified without a model. What no offline test can prove is that a real model *routes* correctly, so the acceptance check in [tasks/checks.py](../stages/ch-07-skills/tasks/checks.py) drives a live model:

```python
    a = agent.Agent(
        system="Follow available skills when they apply.",
        tools=default_tools(),
        skills=load_skills("skills"),
    )
    reply = a.send("Use the sign-off skill. Say goodbye to the team.")
    read_used = any(m.get("role") == "tool" for m in a.messages)
    print("read a skill file:", read_used, "| reply:", repr(reply))
    return "haila" in reply.lower() and read_used
```

`uv run verify` checks parsing, advertisement, and non-disclosure offline. `uv run accept ch-07` evaluates the remaining model-dependent behavior: the live model must use a tool and produce the codeword contained only in the skill file.

The offline non-disclosure assertion is particularly important: merely producing `Haila!` in a
mocked response would say nothing about progressive disclosure. Instead, the test inspects the
system prompt and proves the body text is absent. The live check then joins two observations—the
codeword in the reply and a tool message in history. It does not assert that the tool was
specifically `read_file`, but the planted codeword makes another tool an implausible source.

### Skill-loading execution trace

For a `skills/sign-off/SKILL.md` file and a request to use the sign-off procedure:

1. `load_skills("skills")` reads the file's metadata at agent construction and creates a `Skill`
   whose name and description are available separately from its full body.
2. `_system_text()` adds the short skills menu to the system message. The procedure body is not
   included, which preserves context space when the skill is irrelevant.
3. The model sees the menu and requests the ordinary `read_file` tool for the advertised path.
4. The harness executes the tool and appends its result. Only now does the full procedure enter
   conversation history.
5. The next model call can follow the loaded procedure and produce the final response.

The model's choice in step 3 is probabilistic, so parsing and non-disclosure are checked offline
while correct selection is evaluated with a live-model acceptance check.

## Design decisions & gotchas

**The description is the router.** The model decides whether to load a skill from one line of text, so descriptions should be written like the sign-off skill's: say what the skill does *and* enumerate the trigger phrasings. A vague description is a skill that never fires; an over-broad one is a skill that fires constantly and wastes a tool step.

**The menu can't be compacted away; the body can.** `_system_text` is recomputed on every model call and prepended in `_payload` — the menu never enters `self.messages`, so chapter 6's compaction can never summarize it out. A loaded body, by contrast, is an ordinary tool message: door control clamps it on entry, and compaction may eventually fold it into a summary. That is fine, and it is the point — disk is the source of truth and the window is just a cache; the model can always re-read the file.

**Discovery is startup-only; bodies are live.** `main()` calls `load_skills("skills")` once, so a skill directory added mid-session isn't advertised until restart. But because the model reads bodies from disk on demand, editing a skill's *body* mid-session takes effect on the very next load. Also note both `load_skills("skills")` and the advertised paths are relative to the process working directory — run the REPL from the repo root or the menu comes up empty.

**Skills are trusted input.** The menu says "follow it exactly," which makes a skill body exactly as privileged as `AGENTS.md`: instructions the harness vouches for. For your own repo that is the feature. For a repo you just cloned, `SKILL.md` files are an injection channel — the harness has no notion of untrusted skills. Relatedly, `read_file` is still unscoped (the docstring in [harness/tools.py](../stages/ch-07-skills/harness/tools.py) flags it): the model can read any path on disk, and the menu happily hands it paths to ask for. Confining execution and file access behind a boundary is deliberately deferred to chapter 8.

**The acceptance proof is a conjunction.** `read_used` only checks that *some* tool message exists — a calculator call would satisfy it. The codeword assertion is the real evidence, and the two together are strong: the model cannot produce "Haila!" without the read, and the read is visible in the history.

**Kept deliberately small.** No YAML library, no multi-line frontmatter values, no bundled scripts or resources inside skill directories, and no way for the agent to write its own skills — memory here is read-only and human-authored. Writable, durable state arrives in chapter 9. One historical footnote for readers browsing `upstream/carbon`: the ch-07 commit *message* mentions a codeword ZEBRA-42, but the file at the tag ships `Haila!` — trust the file, and remember the package is still named gemma at this tag.

## Study pointers

Read the stage in this order:

1. [harness/skills.py](../stages/ch-07-skills/harness/skills.py) — the whole primitive: `Skill`, `_parse_frontmatter`, `load_skills`, `skills_prompt`.
2. [skills/sign-off/SKILL.md](../stages/ch-07-skills/skills/sign-off/SKILL.md) — a skill written as a falsifiable experiment.
3. [harness/agent.py](../stages/ch-07-skills/harness/agent.py) — the one-line-of-behavior change in `_system_text`, plus the wiring in `main()`.
4. [tests/episodes/test_ch07.py](../stages/ch-07-skills/tests/episodes/test_ch07.py) — advertisement and non-disclosure, proven offline.
5. [tasks/checks.py](../stages/ch-07-skills/tasks/checks.py) — `_accept_ch07`, the live proof.

Things to try (the demo and acceptance run require LM Studio serving a local model, configured via `.env`): run `uv run demo ch-07` and watch the codeword appear; then add your own skill — a new directory under `skills/` with a `SKILL.md` — restart, and ask for it using one of your description's trigger phrasings *without* naming the skill, to see routing work from the description alone. As a control, ask a fresh session for the project codeword without mentioning sign-off and see whether it reads the file or admits it doesn't know.

Previous: [ch-06 — context management](ch-06-context-management.md), which made the window finite and managed — the constraint that makes progressive disclosure necessary. Next: [ch-08 — execution environment](ch-08-execution-environment.md), which puts running code (and file access) behind a boundary. Chapter 9's durable state is the other half of memory: skills are the read-only, human-authored half; ch-09 makes the agent's own session survivable.
