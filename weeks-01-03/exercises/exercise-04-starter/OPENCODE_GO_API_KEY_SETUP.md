# Using an OpenCode Go API Key with the Toy Agent

This guide explains two safe, low-friction ways to make an OpenCode Go API key
available to `toy_agent.py` (this same approach can be adapted to other projects that want to use 
OpenCode models via endpoints):

There are two options.

1. **User-level configuration:** configure the key once and use it from projects
   in any repository.
2. **Project-level configuration:** keep the key in an ignored `.env` file in
   one project.

In both cases, the program receives the key through the
`OPENCODE_API_KEY` environment variable. The key is never written in Python
source code and must never be committed to Git.

> Each person should use their own OpenCode account, Go subscription, and API
> key. Do not share an instructor's key with a class, and do not share keys 
> with each other. Anyone who accidentally
> exposes a key should revoke it and create a new one immediately.

## 1. Prepare the toy agent

These instructions explain how to set up a Python program to access OpenCode models
via endpoints (via an OpenCode Go subscription).

OpenCode Go uses a different endpoint from the keyless Zen service. It also uses
model IDs without the `-free` suffix. The current endpoints and model IDs are
listed in the [OpenCode Go documentation](https://opencode.ai/docs/go/).

Install the packages in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
pip install requests python-dotenv
```

Add `python-dotenv` to `required-packages.txt` if the project records its
dependencies there.

Use the following configuration near the top of `toy_agent.py`. It supports
both options in this guide and retains the keyless free service as a fallback:

```python
import os
import time
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load a project-level .env file if one exists. By default, load_dotenv does not
# replace a value already supplied by the user's environment.
load_dotenv(Path(__file__).with_name(".env"))

API_KEY = os.getenv("OPENCODE_API_KEY")

if API_KEY:
    # OpenCode Go subscription
    MODEL = "mimo-v2.5"
    ZEN_CHAT_URL = "https://opencode.ai/zen/go/v1/chat/completions"
else:
    # Keyless free fallback
    MODEL = "mimo-v2.5-free"
    ZEN_CHAT_URL = "https://opencode.ai/zen/v1/chat/completions"

# OpenCode requires clients to identify themselves with a real User-Agent
# and to send a stable per-conversation session id (used for routing and
# prompt caching) -- see https://opencode.ai/docs/go .  Requests without
# the session id are rejected with a 400 error on both endpoints.
HEADERS = {"Content-Type": "application/json",
           "User-Agent": "toy-agent/1.0",
           "x-opencode-session": str(uuid.uuid4())}
if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"
```

Note the two extra headers. As of September 2026, both the keyed Go endpoint and
the keyless free endpoint reject requests that do not carry an
`x-opencode-session` header, with `400 Bad Request` (`MissingSessionID`). The
value should be a session identifier that stays the same for all requests in one
conversation — generating one `uuid.uuid4()` when the program starts is exactly
that. OpenCode also asks that clients identify themselves with a descriptive
`User-Agent` (such as `toy-agent/1.0`) rather than the default HTTP-library name.

For a raw HTTP request such as this one, the Go model is named `mimo-v2.5`.
Do not put the OpenCode client prefix `opencode-go/` in the JSON request's
`model` field.

## Option 1: Store the key at the user level

This is the recommended option for someone who uses the subscription from
several repositories. The environment variable becomes available to programs
started from that user's terminal, while repositories contain no secret files.

### macOS or Linux

Keep the key in a separate configuration file so that it is not embedded in a
shell configuration file that might be tracked in a dotfiles repository.

Create and protect a configuration directory:

```bash
mkdir -p ~/.config/opencode-go
chmod 700 ~/.config/opencode-go
nano ~/.config/opencode-go/env
```

Put the following line in the file, replacing the example value with the real
key:

```bash
export OPENCODE_API_KEY='your-real-key-here'
```

Save the file, then restrict its permissions:

```bash
chmod 600 ~/.config/opencode-go/env
```

For zsh, add this non-secret line to `~/.zshrc`:

```bash
[[ -r "$HOME/.config/opencode-go/env" ]] && source "$HOME/.config/opencode-go/env"
```

For bash, add the same line to `~/.bashrc` instead. Open a new terminal, or
reload the appropriate configuration:

```bash
source ~/.zshrc    # zsh
# source ~/.bashrc # bash
```

Verify that the variable exists without displaying the key:

```bash
python -c 'import os; print("configured" if os.getenv("OPENCODE_API_KEY") else "missing")'
```

### Windows

Use a Windows user environment variable:

1. Open the Start menu and search for **Edit environment variables for your
   account**.
2. Under **User variables**, select **New**.
3. Set the variable name to `OPENCODE_API_KEY`.
4. Paste the API key as the variable value.
5. Close and reopen PowerShell, Command Prompt, the IDE, or any other program
   that needs the new variable.

Verify it from PowerShell without displaying the key:

```powershell
if ($env:OPENCODE_API_KEY) { "configured" } else { "missing" }
```

### User-level considerations

- The setting works across repositories and programming languages.
- Programs launched before the variable was configured must be restarted.
- Programs started from the terminal inherit the key, so run only trusted code
  in that environment.
- The key remains plaintext in the user's account. On macOS and Linux, the
  permissions above restrict the file to that user.
- Do not commit the user configuration directory to a dotfiles repository.

## Option 2: Store the key at the project level

This option is convenient for students who want the key available only to this
exercise, or who prefer not to configure their shell or operating system.

Add these patterns to the repository's `.gitignore` and commit the
`.gitignore` change:

```gitignore
.venv/
.env
.env.*
!.env.example
```

Create and commit an `.env.example` template containing no secret:

```dotenv
# Leave this empty to use the keyless free model.
# Copy this file to .env and add your own OpenCode API key there.
OPENCODE_API_KEY=
```

Each user then creates a local `.env` file.

macOS or Linux:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add the user's real key:

```dotenv
OPENCODE_API_KEY=your-real-key-here
```

Confirm that Git ignores the file before running or committing anything:

```bash
git check-ignore .env
git status --short
```

`git check-ignore .env` should print `.env`, while `git status --short` should
not list it.

### Project-level considerations

- Setup is self-contained and does not modify the user's shell configuration.
- A separate `.env` file is needed in every repository that uses the key.
- The committed `.env.example` documents the required variable but contains no
  secret.
- `.env` is plaintext. Git ignoring it prevents accidental normal commits, but
  users must still avoid copying, displaying, or sharing it.

## Which option should I choose?

| Situation | Recommended option |
|---|---|
| The key will be used in several repositories | User-level environment variable |
| The key is only for this exercise | Project-level `.env` |
| A student wants the fewest system changes | Project-level `.env` |
| A developer wants one-time setup across languages and tools | User-level environment variable |

If both are configured, the user-level environment variable wins because
`load_dotenv` does not override an existing environment variable by default.

## OpenCode's own credential storage

The OpenCode application stores credentials entered through `/connect` or
`opencode auth login` in its user-level `~/.local/share/opencode/auth.json`
file. That makes the key available to OpenCode itself across repositories.

The toy agent should not read that file directly: it is owned by OpenCode, may
contain credentials for other providers, and its structure is not part of this
exercise. Continue to give custom programs access through
`OPENCODE_API_KEY`. See the
[OpenCode authentication documentation](https://opencode.ai/docs/cli/#auth)
for details.

## If a key is accidentally committed

1. Revoke the exposed key in the OpenCode console immediately.
2. Create a replacement key.
3. Remove the secret from the project and make sure `.env` is ignored.
4. Replace the key in the user-level configuration or local `.env` file.

Deleting the key in a later Git commit is not sufficient because the original
value remains in Git history.
