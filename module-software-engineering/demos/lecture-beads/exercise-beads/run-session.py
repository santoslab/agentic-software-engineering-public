#!/usr/bin/env python3
"""Record one Claude CLI invocation, including its prompt and tool transcript."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import uuid


def fenced(value, language="text"):
    text = value if isinstance(value, str) else json.dumps(value, indent=2)
    fence = "`" * max(3, 1 + max((len(m) for m in re.findall(r"`+", text)), default=0))
    return f"{fence}{language}\n{text}\n{fence}\n"


def markdown(prompt, events):
    parts = ["# Claude CLI transcript\n", "## Prompt\n", fenced(prompt)]
    for event in events:
        kind = event.get("type", "unknown")
        if kind in ("assistant", "user"):
            message = event.get("message", {})
            content = message.get("content", [])
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            for block in content:
                block_kind = block.get("type")
                if block_kind == "text":
                    parts += [f"## {kind.title()}\n", block.get("text", "") + "\n"]
                elif block_kind == "tool_use":
                    parts += [f"## Tool call: {block.get('name')} ({block.get('id')})\n",
                              fenced(block.get("input", {}), "json")]
                elif block_kind == "tool_result":
                    parts += [f"## Tool result: {block.get('tool_use_id')}\n", fenced(block, "json")]
                else:
                    parts += [f"## {kind.title()}: {block_kind}\n", fenced(block, "json")]
        else:
            parts += [f"## {kind.title()}: {event.get('subtype', '')}\n", fenced(event, "json")]
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--prompt", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Output prefix outside the project")
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--resume", help="Continue an existing session; omit to start a fresh session")
    parser.add_argument("--budget-usd", default="8")
    args = parser.parse_args()
    project = args.project.resolve()
    prefix = args.output.resolve()
    if prefix.is_relative_to(project):
        parser.error("Keep transcripts outside the agent's project directory")
    prefix.parent.mkdir(parents=True, exist_ok=True)
    prompt = args.prompt.read_text()
    session_id = args.resume or str(uuid.uuid4())
    claude = shutil.which("claude") or str(Path.home() / ".local/bin/claude")
    command = [claude, "-p", "--model", args.model, "--verbose",
               "--output-format", "stream-json", "--include-hook-events",
               "--permission-mode", "dontAsk", "--permission-prompts", "none",
               "--tools", "Read,Write,Edit,Glob,Grep,Bash",
               "--allowedTools", "Read,Write,Edit,Glob,Grep,Bash",
               "--setting-sources", "project", "--settings", '{"autoMemoryEnabled":false}',
               "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
               "--disable-slash-commands", "--max-budget-usd", args.budget_usd,
               "--resume" if args.resume else "--session-id", session_id]
    env = os.environ.copy()
    env["PATH"] = str(project / "node_modules/.bin") + os.pathsep + env.get("PATH", "")
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    metadata = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(project), "prompt_file": str(args.prompt.resolve()),
        "session_id": session_id, "resumed": bool(args.resume), "command": command,
        "cli_version": subprocess.check_output([claude, "--version"], text=True).strip(),
        "auto_memory_enabled": False, "prior_transcript_supplied": bool(args.resume),
    }
    Path(str(prefix) + ".prompt.txt").open("x").write(prompt)
    metadata_path = Path(str(prefix) + ".metadata.json")
    with metadata_path.open("x") as file:
        file.write(json.dumps(metadata, indent=2) + "\n")
    print(f"Starting {prefix.name}: session {session_id}", flush=True)
    with Path(str(prefix) + ".jsonl").open("x") as output, Path(str(prefix) + ".stderr.log").open("x") as error:
        completed = subprocess.run(command, cwd=project, env=env, input=prompt,
                                   text=True, stdout=output, stderr=error)
    events = [json.loads(line) for line in Path(str(prefix) + ".jsonl").read_text().splitlines() if line.strip()]
    metadata.update(finished_utc=datetime.now(timezone.utc).isoformat(), exit_code=completed.returncode)
    results = [event for event in events if event.get("type") == "result"]
    metadata["results"] = results
    metadata["observed_models"] = sorted({event["model"] for event in events if event.get("model")} |
                                         {event["message"]["model"] for event in events
                                          if isinstance(event.get("message"), dict) and event["message"].get("model")})
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
    Path(str(prefix) + ".md").write_text(markdown(prompt, events))
    print(json.dumps({"exit_code": completed.returncode, "session_id": session_id,
                      "models": metadata["observed_models"], "events": len(events),
                      "result": results[-1] if results else None}, indent=2), flush=True)
    return completed.returncode or int(not results or results[-1].get("is_error", False))


if __name__ == "__main__":
    raise SystemExit(main())
