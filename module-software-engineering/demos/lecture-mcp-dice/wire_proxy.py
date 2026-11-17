"""Teaching-only stdio tee. Logs dice JSON-RPC to a chosen file, never stdout."""
import json
import subprocess
import sys
import threading

path, *command = sys.argv[1:]
child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
lock = threading.Lock()
with open(path, "w") as log:
    def record(direction, line):
        with lock:
            log.write(json.dumps({"direction": direction, "message": json.loads(line)}) + "\n")
            log.flush()

    def forward():
        for line in sys.stdin.buffer:
            record("client -> server", line)
            child.stdin.write(line)
            child.stdin.flush()
        child.stdin.close()

    threading.Thread(target=forward, daemon=True).start()
    for line in child.stdout:
        record("server -> client", line)
        sys.stdout.buffer.write(line)
        sys.stdout.buffer.flush()
child.wait(timeout=5)
sys.exit(child.returncode)
