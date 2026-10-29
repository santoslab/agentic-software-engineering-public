# Recorded Beads lecture run

This folder contains one consolidated, sanitized transcript, exact prompt copies, nine restorable work states, the run-session recovery helper, and selected verification evidence.

- [Consolidated transcript](transcript.md) — nine successful calls across six sessions, with visible tool activity and results.
- [Restore instructions](RESTORE.md) — extract any checkpoint without changing the original source records.
- [Prompts](prompts/) — one file per call; calls 07 and 08 use the same source prompt.
- [Checkpoint archives](states/) — 01–09, with `work/.git`, `work/.beads`, source, and the archive-root `run-session.py` retained.
- [Planning records](planning/) — execution plan, task map, and the recorded reviews.
- [Initialized project policy](policy/) — the actual `CLAUDE.md` and `AGENTS.md` snapshot.
- [Verification evidence](verification/) — milestone review and independent test results.
- [Source provenance](source.json) — public repository and input commit.
- [Redaction manifest](redaction-manifest.json) — source/output SHA256 hashes and changes.

The source's preceding authentication-rejected attempt and private diagnostic files are not included. The original research records remain in their authoring repository. Per-call JSONL, per-call transcript Markdown, stderr captures, and full CLI metadata are intentionally not part of this publication bundle. Hidden reasoning content was removed; tool, hook, failure, recovery, and visible assistant evidence remains.

The checkpoint archives are sanitized derivatives. Their tar ownership headers are normalized, while the Git object graphs, commit IDs, project source, and Beads state remain intact. See the manifest for counts and hashes.
