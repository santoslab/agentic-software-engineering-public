import os
import time
from pathlib import Path
import requests

## ----- Configure Models ---------

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

HEADERS = {"Content-Type": "application/json"}
if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"


## --------- System Prompt ----------

SYSTEM = "You are a helpful assistant."

## ------ model call -------

def call_zen(messages: list) -> dict:
    resp = requests.post(
        ZEN_CHAT_URL,
        headers=HEADERS,
        json={"model": MODEL, "messages": messages},
        timeout=60,
    )
    resp.raise_for_status()

    payload = resp.json()
    if not payload.get("choices"):
        raise RuntimeError(f"Zen returned no choices: {payload}")
    return payload["choices"][0]["message"]

#------- Harness Opening Message -----------

def print_intro():
    print("Welcome to a toy chat bot!")
    print("You will be prompted for input via the :")
    print("\nThe current model is " + MODEL)
    print("\n Type 'EXIT' to exit the program\n\n")


#------ Harness entry point -------

if __name__ == "__main__":
     # Include the system prompt as the first item in the messages list data structure
    messages = [{"role": "system", "content": SYSTEM}]
    print_intro()

    user = input(": ")
    # REPL
    while user != "EXIT":
        messages.append({"role": "user", "content": user})

        # model interaction
        message = call_zen(messages)
        messages.append(message)
        if message.get("content"):
            print(message["content"])

        # new user input 
        time.sleep(1.0)
        user = input("\n: ")
