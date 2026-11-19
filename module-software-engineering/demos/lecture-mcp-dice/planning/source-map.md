# Sources for the dice based MCP lecture

> Authoring record, migrated from the planning repository on 2026-11-17 with links repointed to
> this repository. The closing section records the migration itself.

Authoring references inspected on 2026-11-15. The sibling public checkout was at
commit `e49631a`; it also contained unrelated working-tree changes. This record
identifies sources, not a claim that their demos have been rehearsed.

## Existing teaching materials

| Source | Intended use |
|---|---|
| [Original dice implementation](../../../../weeks-04-07/student-materials/mcp-example/dice_server.py) and [README](../../../../weeks-04-07/student-materials/mcp-example/README.md) | Baseline for `demos/dice/`; preserve its small scope |
| [Lecture 14 outline](../../../../weeks-04-07/lectures/lecture-14-mcp.md) | Architecture, demonstration flow, and discussion prompts |
| [Lecture 14 student notes](../../../../weeks-04-07/lecture-notes/lecture-14-mcp.md) | Source prose to adapt after the outline is settled |
| [Lecture 14 slide source](../../../../weeks-04-07/slides/lecture-14-mcp.md) | Initial slide structure; remove Stage E and calendar references |
| [MCP diagram source](../../../../weeks-04-07/slides/diagrams/mcp-loop.mmd) and [SVG](../../../../weeks-04-07/slides/diagrams/mcp-loop.svg) | Starting diagram for tracing the dice call |
| [Public MCP instructor draft](../../../lectures-instructor-notes/lecture-07-mcp-the-tool-contract-as-a-specification.md) | Tool contracts and evidence; substitute dice for its proposed game server |
| [Public lecture template](../../../../templates/lecture-outline-template.md) | Objectives, timing, demo fallback, and instructor notes |
| [Public repository conventions](../../../../CLAUDE.md) | Three lecture artifacts, slide styling/builds, and licensing boundary |

The public repository also has the original dice example and Lecture 14 under
`weeks-04-07/`. Consult those copies again when curating the final transfer.
The separate public MCP draft's filename says Lecture 07 while its title still
says Lecture 06; do not inherit either number without checking course placement.

## Adaptation decisions

- Use dice throughout the first lecture, without a prerequisite game database.
- Keep `flip_coins` as the second existing tool for discovery and tool selection;
  avoid adding game state merely to make the example larger.
- Treat descriptions as one part of the tool interface, alongside schemas and
  results. Replace the earlier absolute claim that the docstring is the entire
  interface.
- Treat misleading-description behavior as an experiment whose outcome is
  observed, rather than promising that the model will make a specific mistake.
- Distinguish a local server transport from the location of model inference;
  a local stdio server does not make the whole agent application offline.
- Distinguish the example's plain-text `Error:` results from protocol-level error
  signaling, and distinguish integer typing from enforcing numeric ranges.

## Technical references for drafting and rehearsal

The user has selected official SDK v2 `MCPServer`; see the
[implementation handoff](HANDOFF-SOL.md) for the migration and approved scope.

- [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture):
  host/client/server responsibilities and the separation of MCP from model use.
- [Official Python SDK](https://github.com/modelcontextprotocol/python-sdk):
  migrate the inherited FastMCP example to MCPServer and pin a tested v2 release.
- [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp):
  verify the local-server registration, scope, and discovery instructions.

The preparation pass consulted these landing pages. Runtime compatibility and
the teaching machine's setup remain rehearsal work.

## Implementation record (2026-11-15)

The handoff is implemented in this workspace with official `mcp==2.3.0` and
`uv.lock`. See [verification](../reports/verification.md) for exact executions.
The earlier preparation-status prose above describes the initial state; it is
superseded by the report and current README. No public transfer was performed.

- Toy-agent bridge was checked against Steps 5–6 of the frozen
  [exercise 04](../../../../weeks-01-03/exercises/exercise-04-toy-agent.md),
  with execution limits recognized from Step 7.
- Purple Marp styling follows the public course slide decks. Timings, prose,
  example structure, and speaker notes are newly reconciled to the handoff.
- Runtime discovery uses `server/discover` with revision 2026-07-28, not the
  inherited initialization sequence. Model arrows are explanatory, not captured.
- [SDK tagged source](https://github.com/modelcontextprotocol/python-sdk/tree/v2.3.0),
  [migration guide](https://py.sdk.modelcontextprotocol.io/migration/), and
  [v2 changes](https://py.sdk.modelcontextprotocol.io/whats-new/) were checked
  alongside installed APIs and actual wire captures.
- [Inspector documentation](https://modelcontextprotocol.io/docs/tools/inspector)
  and [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp) supply
  current setup/deferral guidance. Inspector 2.15.0's package engine declaration
  is stricter than the documentation's general Node minimum.
- [Neo4j official source](https://github.com/neo4j/mcp) and
  [installation guide](https://neo4j.com/docs/mcp/current/installation/) were
  checked for the preview. Historical local sources are recorded in
  the adoption demo's preview note (retired 2026-11-19, when the Neo4j lecture took over the music material; see `../../lecture-mcp-neo4j/DEMO.md`); no old installation pin is reused.

Preserve the prose/media CC BY 4.0 and code/config MIT boundary when curating
into the public repository. The public migration map remains in README.md.

## Adoption lecture and homework implementation on 2026-11-16

The [approved plan](../../lecture-mcp-adoption/planning/adoption-lecture-and-music-homework-plan.md) is
implemented as the coordinated [adoption tutorial](../../../lecture-notes/lecture-mcp-adoption.md),
[music homework](../../../../neo4j/02-neo4j-music-mcp/README.md), and expanded dice tutorial.
See [current verification](../../lecture-mcp-adoption/reports/adoption-and-music-verification.md) for executions.

The local Neo4j music guide/loader were read as historical preparation. Their
medium-data import, older Labs server packages, node-key/type constraints and
similarity stage are not student prerequisites in the new package. The small
local CSVs have 40 playlists but only one or two represented tracks each and
little overlap. The new original fictional dataset uses the plan's alternative
to avoid unestablished redistribution terms and create precise counting cases.
Its generator, provenance and manifest are distributed together. It does not
reuse music records or apply the airline dataset's licensing notice.

Primary current references checked during implementation:

- [Microsoft Learn overview](https://learn.microsoft.com/en-us/training/support/mcp)
  and [developer reference](https://learn.microsoft.com/en-us/training/support/mcp-developer-reference):
  public endpoint and discoverable documentation tools. Actual capture negotiated
  2025-06-18 with the pinned SDK client.
- [Get-ChildItem reference](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.5):
  the search/fetch demonstration's source. Captures retain response hashes/lengths
  and a short excerpt, not a bundled copy of the full article.
- [Official Neo4j provider source](https://github.com/neo4j/mcp):
  package 2.1.1's installed CLI and real schema/read calls were verified.
- [APOC installation](https://neo4j.com/docs/apoc/current/installation/) and
  [procedure security](https://neo4j.com/docs/apoc/current/security-guidelines/):
  tested 5.26.0 plugin and meta procedure execution configuration. Missing/sandboxed
  APOC failures were actually observed and corrected in the disposable instance.
- [Claude Code MCP](https://code.claude.com/docs/en/mcp): project scope and
  environment expansion. Host authentication was unavailable, so exact manual
  rehearsal is supplied separately from the completed independent protocol checks.

The migration table remains in README. No original Neo4j exercises, frozen
snapshot files, public content or unrelated working-tree changes were modified.


## Instructor documentation session integration on 2026-11-17

The [instructor transcript](../../lecture-mcp-adoption/claude-session/mcp-microsoft-learn-transcript.md)
is preserved byte-for-byte after moving under adoption. The
[companion walkthrough](../../lecture-mcp-adoption/claude-session/mcp-microsoft-learn-tutorial.md)
was edited to separate model-visible records, independent SDK observations and
illustrative protocol/API envelopes. The adoption notes, slides, instructor/demo
guidance and diagrams now use ToolSearch loading, paired search/fetch requests,
and the follow-up claim review as worked examples. Reconstructed host internals,
negotiated versions, execution timing and token/cost figures are not promoted
into measurements of the instructor session. The independent capture retains
its own date/version identity.

## Public migration (2026-11-17)

Migrated into the public repository from planning commit `244f0c9` (`mcp-lecture/`,
clean working tree). Lecture artifacts went to
`module-software-engineering/{lectures-instructor-notes,lecture-notes,slides}/lecture-mcp-*.md`,
unnumbered like the Beads lecture; the demos to `module-software-engineering/demos/lecture-mcp-adoption/`
and `lecture-mcp-dice/`; the homework to `neo4j/02-neo4j-music-mcp/`; the instructor key to
`demos/lecture-mcp-adoption/neo4j-music-instructor-key/`; `demos/neo4j-preview.md` to the adoption
demo folder. The planning records and verification reports moved into each demo folder's
`planning/` and `reports/`. Diagrams `components` and `host-call` were renamed `mcp-components`
and `mcp-host-call`; `music-graph.svg` is tracked both in `slides/diagrams/` and as the homework's
`assets/` copy. The package `README.md` (absorbed into the module README), the pinned
`slides/build.sh` (Mermaid CLI 12.2.0, Marp CLI 4.5.1), `check-layout.cjs`, virtual environments,
caches, and rendered previews were not migrated. Links in migrated files were repointed; prose
in dated records that says "planning repository" was left as written.
