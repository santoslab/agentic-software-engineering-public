import os
import time

import requests

MODEL = "mimo-v2.5-free"
ZEN_CHAT_URL = "https://opencode.ai/zen/v1/chat/completions"

HEADERS = {"Content-Type": "application/json"}
if os.environ.get("OPENCODE_API_KEY"):
    HEADERS["Authorization"] = f"Bearer {os.environ['OPENCODE_API_KEY']}"

SYSTEM = "You are a helpful assistant."


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


def print_intro():
    print("Welcome to a toy chat bot!")
    print("You will be prompted for input via the :")
    print("\nThe current model is " + MODEL)
    print("\n Type 'EXIT' to exit the program\n\n")


if __name__ == "__main__":
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
