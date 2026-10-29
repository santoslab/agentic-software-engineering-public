# Task Master scalability assessment

Evaluated October 26, 2026: **task-master-ai 0.43.1**, source revision
`1c7365cab1f1d8ee5b0ecc2292a9ba9cf5efea2e`.

**Assessment:** local CLI latency stayed around 1.4 seconds through 10,000
synthetic tasks (17.58 MB). **This does not establish scalability.** The local
whole-file read/modify/rewrite design processes the backlog for individual
operations and serializes file writes. Concurrent updates to the same tag
also lost successful changes in this release. That is a reproduced defect in
the tested update path; it is distinct from the storage design's scaling limits.

## Backlog size

These are measured CLI wall-clock times on this Mac (macOS 26.6.2, ARM64,
Node 26.12.1). Each cell is the median of three fresh CLI processes with a warm
filesystem cache. Fixtures contain a sparse dependency graph, half completed
tasks, about 1.76 KB per task, and no subtasks. Writes were checked against the
saved file, and reads were checked for the expected task IDs.

| Tasks | Input JSON, MB | `show` | `next` | `set-status` |
| ---: | ---: | ---: | ---: | ---: |
| 100 | 0.18 | 1.42 s | 1.36 s | 1.40 s |
| 1,000 | 1.76 | 1.38 s | 1.38 s | 1.38 s |
| 10,000 | 17.58 | 1.39 s | 1.42 s | 1.46 s |

There was little latency growth within this range. This does not establish an
upper limit, performance on other hardware, or persistent MCP-server latency.
The implementation still reads/parses the whole file for a single-task lookup
and rewrites it for status updates. Tags are groups within the same JSON file
in this release, rather than separate storage shards.
([Storage implementation](https://github.com/eyaltoledano/claude-task-master/blob/1c7365cab1f1d8ee5b0ecc2292a9ba9cf5efea2e/packages/tm-core/src/modules/storage/adapters/file-storage/file-storage.ts),
[path resolver](https://github.com/eyaltoledano/claude-task-master/blob/1c7365cab1f1d8ee5b0ecc2292a9ba9cf5efea2e/packages/tm-core/src/modules/storage/adapters/file-storage/path-resolver.ts))

## Concurrent writers

Each process updated a different pending task to `in-progress` in the same
`master` tag. Processes were launched together using a barrier. A successful
command had exit status zero and JSON confirming its requested update.
The test then inspected the file after every process had exited.

| Backlog | Writers | Successful commands, by run | Changes retained, by run |
| ---: | ---: | --- | --- |
| 1,000 | 2 | 2 / 2 / 2 | 1 / 1 / 1 |
| 1,000 | 8 | 8 / 6 / 7 | 2 / 1 / 1 |
| 10,000 | 8 | 7 / 6 / 6 | 1 / 1 / 1 |

For example, the two-process commands were:

```sh
task-master set-status 2 in-progress --format json
task-master set-status 4 in-progress --format json
```

When launched concurrently, both reported success, but only one task retained
its new status, in all three runs. A sequential control using the same fixture
and commands retained both changes. All resulting files remained valid JSON.
Some eight-writer commands also exited unsuccessfully; those were excluded
from the success counts above.

The source explains the result: `updateTaskStatus` loads the tasks before
`saveTasks` takes its lock. The save operation re-reads the file under the lock,
but replaces the tag's whole task array with the previously prepared snapshot.
Another writer's update within that tag can therefore disappear. Atomic file
replacement protects file integrity; it does not merge those stale snapshots.
([Status update and save](https://github.com/eyaltoledano/claude-task-master/blob/1c7365cab1f1d8ee5b0ecc2292a9ba9cf5efea2e/packages/tm-core/src/modules/storage/adapters/file-storage/file-storage.ts#L451),
[locking and atomic writes](https://github.com/eyaltoledano/claude-task-master/blob/1c7365cab1f1d8ee5b0ecc2292a9ba9cf5efea2e/packages/tm-core/src/modules/storage/adapters/file-storage/file-operations.ts))

The tested `next` command also returned task 2 after it had been marked
`in-progress`. That supports resuming work; `next` itself is not an exclusive
reservation for parallel workers.
([Task selection](https://github.com/eyaltoledano/claude-task-master/blob/1c7365cab1f1d8ee5b0ecc2292a9ba9cf5efea2e/packages/tm-core/src/modules/tasks/services/task-service.ts#L320))

## Agent context and distributed work

At 10,000 tasks, `show` returned about 1.9 KB for one task. In contrast,
`list --ready --json` returned 5,000 tasks and about 8.83 MB. Backlog capacity
and agent context are separate concerns: retrieve the relevant work item and
its prerequisites rather than inserting the full backlog into a prompt.
These measurements concern CLI output, not MCP response sizes or model tokens.

Local file locks do not synchronize independent Git clones. Task Master's
documented team mode uses hosted Hamster storage and real-time synchronization.
The local-file failures above do not establish how that service behaves.
([Official solo/team comparison](https://tryhamster.com/docs/taskmaster/team/overview))

For the lecture, Task Master offers AI commands to generate tasks from
requirements and split tasks into subtasks. **There is no established evidence
for the effectiveness of these AI planning commands.** The course notes link
the examined implementation tests and timing benchmarks. With the tested local
release, serialize mutations through one writer, including when one developer
runs multiple agents. The existing SDD plan makes Beads a natural teaching
choice, but this assessment does not establish that Beads is faster or free of
concurrency defects.

## Reproduce

Run from this assessment folder. The script creates only synthetic fixtures
beside its own copy, so copy it into a disposable directory first:

```sh
TM_EVAL="$(mktemp -d)"
cp task-master-evaluate.py "$TM_EVAL/evaluate.py"
npm install --prefix "$TM_EVAL" --ignore-scripts --no-audit --no-fund --save-exact task-master-ai@0.43.1
python3 "$TM_EVAL/evaluate.py"
```

The script records individual timings, command outcomes, retained task IDs,
and the sequential control in `results.json`. Concurrent outcomes can vary
with scheduling. The measured defect should be rechecked when upgrading.

Not evaluated: AI planning quality or cost, hosted Hamster team mode, MCP
transport, network-filesystem locks, cross-machine Git merges, dense graphs,
deep subtasks, backlogs beyond 10,000 tasks, or a comparative Beads benchmark.
No provider keys or model calls were used. Task Master was installed only in
an isolated temporary directory; neither course repository gained a dependency.
