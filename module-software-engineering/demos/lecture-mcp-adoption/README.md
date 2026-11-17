# Adopt a documentation MCP server

The lecture uses Microsoft Learn's public documentation endpoint. No Microsoft
account or PowerShell installation is needed for its search/fetch tools. A model
host account is still needed to have Claude select tools and explain results.

In this directory, prepare the independent client:

```sh
uv sync --locked
uv run --frozen python check_remote.py
```

Expect discovery of documentation tools and successful search/fetch calls.
The script writes [evidence/remote.json](evidence/remote.json): actual definitions,
arguments, negotiated version, response hashes/lengths, and a short excerpt.
It does not bundle full third-party articles or claim a model conversation ran.
Read the returned source article yourself when checking the answer.

The instructor's 2026-11-17 Claude Code session is recorded in the
[Claude-generated transcript](claude-session/mcp-microsoft-learn-transcript.md)
and [companion walkthrough](claude-session/mcp-microsoft-learn-tutorial.md).
They document a live instructor run, while the transcript itself was reconstructed
by Claude from its context at the instructor's request. The walkthrough mixes
model-visible material with illustrative protocol/API envelopes; it is not a raw
host or network trace. The companion walkthrough now labels those distinctions and links the worked
examples in the notes and slides. The transcript is preserved unchanged.

Follow [DEMO.md](DEMO.md) for the project-scoped configuration walkthrough,
exact prompts, failure exercise, and authenticated-host rehearsal. Use
[EVIDENCE.md](EVIDENCE.md) to record a student attempt. The file
`.mcp.json.example` is a copyable example, not an active server registration.
No configuration is installed globally or in this repository.

The provider is remote and cannot be version-pinned by this package. Record
the date and observed schema whenever rehearsing. The client is official
`mcp==2.3.0`, with `uv.lock`; its actual negotiation can differ from the local
dice server's trace. A successful network call does not verify host tool selection.
