# The replay script: `build-history.sh`

## Goal

Turn the published snapshots into a tagged git history, so that a reader can
`git log`, `git diff a1-specs..a1-scenarios`, and check out the state at
each of A1's four commits. The history is a **reconstruction**: it is
rebuilt from the patches that the actual A1 build produced, in the same
order, but the dates and the author are the replay's. The commits it makes
pass the mechanical evaluations of their version by construction, because
the patches came from commits that did.

## Requirements

1. `build-history.sh TARGET_DIR` creates `TARGET_DIR` as a git repository
   whose first commit is the complete A0 snapshot, tagged `a0`.
2. Applies, in order, the patches of `a1/reference/history/`, one commit
   each, with the commit messages of the build, and tags them `a1-specs`,
   `a1-scenarios`, `a1-trace`, `a1`.
3. Labels every commit message as a replay, and writes a note in the
   repository saying that the history is a reconstruction.
4. The replayed `a1` tree equals the `a1/` snapshot except for the `.patch`
   files of `reference/history/` (the patches are not part of the commits,
   since they describe them; the folder's README is), which the script's
   header says. The script lives beside the snapshots, in the directory that
   holds `a0/` and `a1/`, not inside `a1/`.
5. Fails loudly if a patch does not apply.

## The prompt

New in A1, written by the build agent after the four commits existed. The
prompt a developer would give:

> Export each commit after the baseline as a patch under
> `reference/history/`, and write a script that recreates the history from
> the `a0` snapshot and those patches, tagging each commit with its name.
> Say in the script and in the commit messages that this is a reconstruction.

## Review points

The patches are exported from real commits (`git format-patch`), not written
by hand; the script does not invent intermediate states; the tags are the
names the dev log uses; the difference between the replayed tree and the
snapshot is stated, not discovered.

## Deliberate-failure checks

Run it, then run `tools/evaluate.sh` at the `a1` tag in the replayed
repository: it must exit 0. Run it a second time into the same directory: it must refuse. Both
observed on 2026-10-22 and again on 2026-10-24, after the snapshots were
re-layered and the patches regenerated.

## Adapting it to your project

Not needed in a project that has a real history. It exists because the
course publishes snapshots, not repositories.

## Making it shared infrastructure

Not applicable; it is a teaching artifact.
