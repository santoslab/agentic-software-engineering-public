# Recorded walkthrough evidence

The JSON files are actual Beads 1.3.2 read-only query output captured from
restored session archives. Their issue states come from the recorded Sonnet
run; these are not seeded demonstration records. The
[recorded-run materials](../../../demos/lecture-beads/recorded-run/README.md)
provide the sanitized transcript, exact prompts, checkpoint hashes, and
provenance. Original raw captures remain in the authoring repository.

- after-creation: 02-after-bead-creation.tar.gz
- after-interruption: 05-after-interruption.tar.gz
- after-recovery: 06-after-recovery.tar.gz
- after-milestone: 09-after-milestone.tar.gz

Final tests/conformance are copied from the independent final verification;
recovery observations identify the missed report before editing. Diagram
labels, abbreviated tables, and console excerpts are derived presentations of these facts.


`dep-tree-after-creation.txt` is standard output from Beads 1.3.2:

```sh
bd --readonly --sandbox --no-color dep tree ttt-cik.4
```

It was replayed for the lecture against a temporary restoration of
02-after-bead-creation.tar.gz; ANSI styling was removed. This is a later
read-only query of the recorded state. The original Sonnet creation transcript
queried the epic (`bd dep tree ttt-cik`), rather than the verification child.
Slide 33 shortens titles, omits priority/status metadata, and tidies the tree's
indentation. The parent-child row denotes epic membership; blocking relations
are labeled `[blocks]`.


`prime-workflow.txt` preserves the decoded `additionalContext` from the first
SessionStart hook in [recorded call 03](../../../demos/lecture-beads/recorded-run/transcript.md#call-03). The hook
supplied actual Beads 1.3.2 `bd prime` output. The JSON envelope is omitted;
the decoded text is unchanged. Slide 15 selects excerpts in their original
order and marks omissions with `...`. The local-only/no-remote closing
checklist reflects this demo's configuration, rather than a universal Beads
policy.
