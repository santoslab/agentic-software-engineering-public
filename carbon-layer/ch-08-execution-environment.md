# Chapter 8 — Execution environment: the harness runs code behind a boundary

Since ch-05 the agent has been able to request shell commands: the harness routes each command through `Sandbox`, and the model receives text containing output and an exit code. In chapter 5 the local backend still ran on the host as the current user with the inherited environment. This chapter applies security policy at that centralized execution point: a more restrictive Docker configuration, a scrubbed local fallback, a workspace-confined `read_file`, and a helper that runs candidate Python in a scrubbed process. It also changes compaction to use provider-reported token usage instead of a character-count estimate.

## The primitive

The execution environment is the place where model-originated code actually runs, and the harness owns it completely. The model never executes anything; it emits text that *asks* for execution. The harness decides where that code runs, as which user, with which environment variables, with what filesystem view, and with how much network. That decision cannot live in the model, because a prompt can express policy but cannot enforce it — a model that has been told "never read secrets" is one adversarial instruction, one bad completion, or one confused turn away from trying anyway. Enforcement has to sit below the model's outputs, in code the model cannot talk its way around.

The posture this chapter installs is *start closed*: default-deny, then grant back deliberately. No network. A scoped, throwaway working directory. An environment with no inherited credentials — the sandbox hands untrusted code a minimal `PATH` and nothing else, so there is no secret to leak. When the agent genuinely needs a capability, you add it back explicitly and size the isolation to the blast radius: an OS sandbox, a container, a user-space kernel, a micro-VM. This build stops at the container rung, and says so.

Two ideas meet here. Chapter 5 centralized code execution in `Sandbox.run()`; chapter 8 applies containment policy at that call boundary. The approval gate and sandbox address different risks. The gate asks a human whether the requested action should run. The sandbox limits what an approved command can access if its behavior is broader than the human expected. Neither control makes the other unnecessary.

## From the video

The video opens by naming the debt: the agent runs code and follows procedures now, but all of that code has been running on our own machine, and the model will happily ask to run anything. The one-line rule the whole chapter hangs on comes at [19:45](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1185s): "The prompt is intent, not containment." So the boundary has to live in the harness, and the move is start closed — network none, filesystem scoped, credentials absent — then climb the isolation ladder only as needed, "chosen by the blast radius": an OS sandbox, then containers, maybe a user-space kernel, a micro-VM. The bash tool now runs inside the sandbox; that is the change this chapter makes.

Then every seam that untrusted code touches gets hardened. `read_file`, which could previously reach `/etc/passwd`, is confined to the workspace. The verifier, which would have run candidate code with our full environment, gets scrubbed. The rule underneath it all, at [20:29](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1229s): "don't tell the model not to touch secrets, just don't give it secrets."

Walking the code, the author notes the small change in the agent first — compaction now triggers on the model's reported token count, not the estimate — and flags that a verification helper file shows up here but "it's only exercised by the sandbox for now. The loop doesn't call it until the later chapter." The main event is at [21:16](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1276s): `sandbox.py` now runs Docker with no network, a non-root user, capabilities dropped, a read-only filesystem, and hard caps on memory and processes, falling back to a scrubbed local run when Docker is absent.

The live demo at [21:44](https://www.youtube.com/watch?v=oUBgqzcV1qw&t=1304s) shows both halves: a shell command is approved and runs inside the box with working directory `/work`, then a request to read `/etc/passwd` through the read tool fails — path outside the workspace. "So the boundary lives in the harness, not the prompt." The closing beat sets up ch-09: code runs safely now, but it all still lives inside one process — kill the agent and the whole conversation is gone.

## The code

### The hardened `Sandbox` interface

Start at [harness/sandbox.py](../stages/ch-08-execution-environment/harness/sandbox.py), where most of
the diff lands. The public signatures remain unchanged from ch-07, which is important: callers get
a stronger boundary without changing how they construct or invoke it.

| Interface | Inputs/defaults | Return or state | Failure behavior |
|---|---|---|---|
| `Sandbox(image="busybox", timeout=15.0, prefer_docker=True)` | Docker image, execution timeout, and whether to probe Docker. | Stores configuration; `_docker` remains unknown until first run. | Construction does no I/O. |
| `run(command, workdir=None)` | Shell command and optional persistent directory. | `SandboxResult` with separate stdout/stderr, integer exit, and selected backend. | Docker probe failures select local; command start and timeout errors propagate. |
| `bash_tool(sandbox, workdir=None)` | Configured sandbox and directory. | Tool result combines streams behind `[exit N via backend]`. | ToolRegistry later converts raised errors to `error:` text. |

`Sandbox.run` probes for a Docker daemon and dispatches to `_run_docker` or `_run_local`; both
backends are hardened, but they do not become equivalent. The Docker invocation grows six flags:

```python
        work = ["-v", f"{workdir}:/work"] if workdir else ["--tmpfs", "/work:rw,size=16m"]
        argv = [
            "docker", "run", "--rm",
            "--network", "none",
            "--user", "65534:65534",
            "--cap-drop", "ALL",
            "--memory", "256m",
            "--pids-limit", "128",
            "--read-only",
            *work,
            "-w", "/work",
            self.image,
            "sh", "-c", command,
        ]  # fmt: skip
```

Read the flags as the start-closed checklist. `--network none`: exfiltration and call-home are off by default. `--user 65534:65534`: the command runs as `nobody`, not root. `--cap-drop ALL`: no Linux capabilities. `--memory 256m` and `--pids-limit 128`: a fork bomb or allocation loop hits a hard cap instead of the host. `--read-only`: the container's root filesystem is immutable; the only writable path is `/work`, which is a 16 MB throwaway tmpfs unless the caller bind-mounts a persistent workspace (the workspace seam from ch-05, preserved — a bash command can still see the file a write tool just created).

### The scrubbed local subprocess

The local fallback gets the subset of that posture a plain subprocess can offer — a scrubbed
environment and a timeout:

```python
    def _run_local(self, command: str, workdir: str | None) -> SandboxResult:
        # Fallback: scrubbed env + timeout. Uses the persistent workspace if given,
        # else a fresh throwaway dir. (network is NOT isolated here — that needs Docker.)
        cwd = workdir or tempfile.mkdtemp(prefix="sandbox-")
        env = dict(_SCRUBBED_ENV, HOME=cwd, TMPDIR=cwd)
        proc = subprocess.run(
            ["bash", "-c", command],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
```

`_SCRUBBED_ENV` establishes the non-inheriting environment with two entries:
`{"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LC_ALL": "C"}`. `dict(_SCRUBBED_ENV, HOME=cwd,
TMPDIR=cwd)` constructs a new dictionary rather than modifying the module constant. Nothing is
inherited from the parent process, so a parent `AWS_SECRET_ACCESS_KEY` does not exist in the child
environment. `HOME` and `TMPDIR` are pointed into the sandbox directory so well-behaved tools that
write to either stay inside it.

`subprocess.run()` waits synchronously. `timeout` raises `TimeoutExpired`; it does not turn a timeout
into a `SandboxResult`. `capture_output=True` creates pipes for both streams, and `text=True` decodes
them. A nonzero command exit is normal data in `proc.returncode`, not an exception. This difference
is why a failed test command can be recorded and shown to the model, while a hung command follows
the registry's exception-to-error-string path.

### Workspace-confined reads

The second hardened seam is in
[harness/tools.py](../stages/ch-08-execution-environment/harness/tools.py). `read_file` was
explicitly unscoped through ch-07 — the module docstring flagged confinement as “the
execution-environment concern of ch-08.” This stage adds that read-side boundary:

```python
def read_file(path: str) -> str:
    """Return a file's contents — confined to the workspace (ch-08 hardening).

    The model-invoked tool must not wander the host filesystem (no /etc/passwd).
    Paths are resolved and must live under the current working directory.
    """
    root = Path.cwd().resolve()
    p = Path(path).resolve()
    if p != root and root not in p.parents:
        return f"error: path outside workspace: {path}"
    return p.read_text() if p.is_file() else f"error: no such file: {path}"
```

`Path.resolve()` does the real work: it canonicalizes `..` segments and symlinks before the
containment check, so `workspace/../../etc/passwd` and a symlink pointing outside both resolve to
their true targets and fail the `root not in p.parents` test. This is the same pattern
`Workspace._safe` has used for the write and edit tools since ch-05 — ch-08 closes the read-side
hole to match. Missing files return an error string. Permission, decoding, or race failures after
`is_file()` can still raise and are normalized only when the function is invoked through the tool
registry.

### Deferred Python verification helpers

New in this stage is
[harness/verification.py](../stages/ch-08-execution-environment/harness/verification.py), a small
module the loop does not call yet.

| Interface | Inputs/defaults | Return | Failure behavior |
|---|---|---|---|
| `extract_code(text)` | Model output string. | First fenced block's body, stripped; otherwise stripped input. | Accepts an unlabelled or lowercase `python` fence only; never executes. |
| `run_python(code, check, timeout=10.0)` | Candidate source, appended check source, seconds. | `VerificationResult(passed, output)` from a fresh child; its temporary directory remains on disk. | Timeout becomes a failed result; file/process-start failures propagate. |

`extract_code` uses a regular expression with `re.DOTALL`, which lets `.` match newlines inside a
code fence. `(.*?)` is a non-greedy capture, so it stops at the first closing fence. The helper does
not parse Markdown generally and does not select among multiple blocks.

`run_python` writes candidate code plus an assertion into a temp directory and runs it in a fresh
process:

```python
    script = f"{code}\n\n{check}\nprint('VERIFICATION_OK')\n"
    workdir = Path(tempfile.mkdtemp(prefix="verify-"))
    candidate = workdir / "candidate.py"
    candidate.write_text(script)
    scrubbed_env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "HOME": str(workdir), "LC_ALL": "C"}
```

`sys.executable` selects the same Python interpreter that is running the harness. The candidate and
check share one file and namespace, then the sentinel prints only if execution reaches the last
line. `passed` requires both child exit 0 and the sentinel in stdout. At this tag the sentinel is
fixed text and therefore forgeable by candidate code; the appendix follows the later hardening to a
per-run nonce. Because the function uses `tempfile.mkdtemp()` without a cleanup call or context
manager, each invocation also leaves its `verify-*` directory and candidate script behind.

Same posture, different seam: model-written code is exactly as untrusted as a model-written shell
command, so it gets the same scrubbed environment and scoped workdir. The docstring is explicit
that this lands now because it is an execution-environment concern; turning it into a self-checking
feedback loop — run, feed failures back, correct — is the ch-12 primitive.

### Reported usage in the agent loop

The loop change is in [harness/agent.py](../stages/ch-08-execution-environment/harness/agent.py). Every response now feeds a running usage counter, and `_maybe_compact` prefers it over the estimate:

```python
            self._last_tokens = int(resp.usage.get("total_tokens", 0)) or self._last_tokens
```

```python
    def _maybe_compact(self) -> None:
        # ch-08: prefer the model's reported usage; fall back to an estimate on turn one.
        self.just_compacted = False
        window = self._last_tokens or estimate_tokens(self.messages)
        if window > self.context_limit:
            self.messages = compact(self.messages, model=self.model)
            self._last_tokens = 0  # recomputed from the next response
            self.just_compacted = True
```

Since ch-06 the window budget was a characters-divided-by-four guess. The response interface has
carried a `usage` dictionary all along; now the harness reads `total_tokens`. This is only more
accurate when the provider supplies a meaningful value. Missing or zero usage preserves the
previous nonzero count, and the very first call still uses the estimate. A `None` usage object or a
non-numeric token value raises during `.get(...)` or `int(...)` and aborts the turn at this tag; the
first post-ch-14 hardening commit normalizes those live-boundary cases.

### Offline boundary tests and live acceptance

The tests in [tests/episodes/test_ch08.py](../stages/ch-08-execution-environment/tests/episodes/test_ch08.py) check the boundary deterministically, forcing `Sandbox(prefer_docker=False)` so they do not require a Docker daemon. One containment test places a secret in the parent process and checks that the child cannot read it:

```python
def test_environment_is_scrubbed():
    os.environ["SANDBOX_SECRET"] = "POULTRY-FARM"
    try:
        r = Sandbox(prefer_docker=False).run("printenv SANDBOX_SECRET || echo CLEAN")
    finally:
        del os.environ["SANDBOX_SECRET"]
    assert "POULTRY-FARM" not in r.stdout
    assert "CLEAN" in r.stdout
```

Further tests block `/etc/passwd` while allowing `pyproject.toml`, prove the verifier does not inherit a planted `LEAKY_SECRET`, and drive compaction purely from a faked `usage` field while the character estimate stays tiny. The hardening also forced a rewrite of [tests/conftest.py](../stages/ch-08-execution-environment/tests/conftest.py): the old fixture isolated every test by `chdir`-ing into a temp directory, but `read_file` is now scoped to the current working directory, so the ch-08 tests *need* to run from the repo root. The new fixture is surgical — it monkeypatches `load_agents_md` to ignore only the ambient default directory, and leaves the real cwd alone.

Both gates are registered in
[tasks/checks.py](../stages/ch-08-execution-environment/tasks/checks.py). `uv run verify` runs the
offline suite. It forces the local backend, so it proves environment scrubbing, directory choice,
read confinement, verifier containment, and usage-triggered compaction without claiming Docker's
kernel boundary was exercised. `uv run accept ch-08` additionally checks the configured live model
path: the model requests `echo hello-from-sandbox`; a planted `SANDBOX_SECRET` is absent from the
command environment; `read_file("/etc/passwd")` returns a workspace error while `README.md` remains
readable; the verifier cannot see a planted host variable; and a real response leaves
`_last_tokens > 0`. Docker flags are established by source inspection here; their effective host
security also depends on the installed Docker runtime.

### Sandboxed-command execution trace

For an approved `bash` request while Docker is available:

1. The tool loop passes the model-supplied command to `Sandbox.run()` only after the approval
   callback returns true.
2. `Sandbox.run()` selects the Docker backend and constructs `docker run` arguments with no
   network, a non-root user, resource limits, a controlled working directory, and a restricted
   environment.
3. The container executes the command and returns captured output plus an exit status to the
   Python process.
4. `bash_tool` converts that result into a string beginning with the backend and exit status.
5. The agent appends the string as a tool message; the next model call sees the result but receives
   no direct handle to the container or host process.

When Docker is unavailable, the local backend cannot provide the same isolation. It reduces
exposure by using a scrubbed environment and controlled directory, a difference the chapter must
state rather than treating both backends as equivalent sandboxes.

## Design decisions & gotchas

**The sandbox is the backstop, not the only defense.** The module docstring says exactly that. The approval gate still fronts every `bash`, `write_file`, and `edit_file` call in the REPL; the sandbox is what limits the damage when an approved command misbehaves. Layers, not a single wall.

**Be honest about the local fallback.** The repo is, in its own comments: "network is NOT isolated here — that needs Docker." A scrubbed environment keeps credentials out of `env`, and a fresh temp cwd keeps commands out of your repo, but the fallback is still a plain subprocess running as your user: it can open sockets, and nothing stops the *code it runs* from reading host paths directly — `cat /etc/passwd` inside local-backend bash succeeds even though the `read_file` tool refuses. Only the Docker backend delivers the filesystem and network boundary. Check the `backend=` field in `SandboxResult` if you care which one you got.

**This is teaching-grade even with Docker.** Containers share the host kernel; the isolation ladder the video names — user-space kernels (gVisor-style), micro-VMs — exists precisely because container escape via kernel bugs is a real class of attack. The chapter demonstrates the posture and the container rung; it does not claim the top of the ladder. Relatedly, the timeout wraps the `docker run` client process, and a bind-mounted `workdir` is deliberately writable — mount a real project directory only if you mean the blast radius to include it.

**`read_file`'s workspace is the process cwd.** The confinement root is `Path.cwd()`, not a configured workspace object. Launch the agent from your home directory and its "workspace" is your home directory. This is simple for a REPL started from a project root, but a production harness should store and enforce an explicit root, as `Workspace` already does for writes.

**Two shells, two dialects.** The Docker backend runs `sh -c` in busybox; the local backend runs `bash -c`. A bashism can pass locally and fail in the container.

**The `or`-fallback cuts both ways.** `int(resp.usage.get("total_tokens", 0)) or self._last_tokens` keeps the last known count when a provider omits usage — but that also means a stale number can linger. The reset to `0` after compaction matters: without it, the pre-compaction count would keep tripping the threshold every turn until a fresh response arrived.

**Deliberately deferred.** `verification.py` ships dark — wired into the loop at ch-12 (`ch-12-verification.md`). Everything still lives in one process; durability is ch-09.

## Study pointers

Read the stage in this order:

1. [harness/sandbox.py](../stages/ch-08-execution-environment/harness/sandbox.py) — the boundary itself: Docker flags, the scrubbed fallback, `bash_tool`.
2. [harness/tools.py](../stages/ch-08-execution-environment/harness/tools.py) — the `read_file` confinement; compare with `_safe` in [harness/workspace.py](../stages/ch-08-execution-environment/harness/workspace.py).
3. [harness/verification.py](../stages/ch-08-execution-environment/harness/verification.py) — the same posture applied to model-written Python.
4. [harness/agent.py](../stages/ch-08-execution-environment/harness/agent.py) — `_run`'s usage capture and `_maybe_compact`.
5. [tests/episodes/test_ch08.py](../stages/ch-08-execution-environment/tests/episodes/test_ch08.py) and [tests/conftest.py](../stages/ch-08-execution-environment/tests/conftest.py) — one test per boundary, plus the isolation rework the cwd-scoping forced.
6. The ch-08 block of [tasks/checks.py](../stages/ch-08-execution-environment/tasks/checks.py) — what "accept" proves live.

Things to try: the pytest suite and the sandbox itself are offline, so from the stage directory run `python -c "from harness.sandbox import Sandbox; print(Sandbox().run('env; pwd').stdout)"` with Docker up, then again with `prefer_docker=False`, and compare what the two backends expose. Ask `read_file` for `/etc/passwd` and watch it refuse. The demo and acceptance runs (`uv run demo ch-08`, `uv run accept ch-08`) need a real model — LM Studio serving a local model, per `.env.example`.

Previous: [ch-07 — skills](ch-07-skills.md). Next: [ch-09 — durable state](ch-09-durable-state.md). Chapter 12 uses this execution boundary while verifying generated code, and chapter 11's subagents increase the number of independently generated actions the harness may need to contain.
