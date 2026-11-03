"""The session loop: start menu, games, end of input (contracts/cli.md)."""

from typing import TextIO

TITLE = "Five-in-a-Row — 9×9, five or more in a line wins."
START_MENU = ("Play the computer", "Play a friend", "Quit")
GOODBYE = "Goodbye."


class _EndOfInput(Exception):
    """Input ended (EOF); the session ends as for an interrupt (C-17)."""


class _App:
    def __init__(self, stdin: TextIO, stdout: TextIO, opponent_factory) -> None:
        self._in = stdin
        self._out = stdout
        self._opponent_factory = opponent_factory

    def say(self, text: str = "") -> None:
        self._out.write(text + "\n")

    def ask(self, prompt: str) -> str:
        self._out.write(prompt + " ")
        self._out.flush()
        line = self._in.readline()
        if line == "":
            raise _EndOfInput
        return line.rstrip("\n")

    def run(self) -> int:
        try:
            self.start_menu()
        except (_EndOfInput, KeyboardInterrupt):
            self.say()
            self.say(GOODBYE)
        return 0

    def start_menu(self) -> None:
        while True:
            self.say()
            self.say(TITLE)
            self.say()
            for number, label in enumerate(START_MENU, start=1):
                self.say(f"  {number}  {label}")
            self.say()
            entry = self.ask("Choose 1, 2 or 3:").strip()
            if entry == "3":
                return
            if entry in ("1", "2"):
                raise NotImplementedError("game modes arrive with User Stories 1 and 2")
            self.say(f"'{entry}' is not a choice.")


def run(stdin: TextIO, stdout: TextIO, opponent_factory=None) -> int:
    """Run one session on the given streams; return the exit status (contracts/cli.md §1)."""
    return _App(stdin, stdout, opponent_factory).run()
