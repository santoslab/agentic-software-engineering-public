"""The session loop: start menu, games, end of input (contracts/cli.md)."""

from typing import TextIO

from five_in_a_row.engine import GameState, IllegalMove, Result

from .parse import parse_move
from .render import move_prompt, rejection, render_board, result_line, unreadable

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
        if not self._in.isatty():
            # Piped or scripted input is not echoed by a terminal; echo it so the
            # transcript reads as it would on screen.
            self._out.write(line if line.endswith("\n") else line + "\n")
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
            if entry == "2":
                self.two_player_game()
                continue
            if entry == "1":
                raise NotImplementedError("playing the computer arrives with User Story 2")
            self.say(f"'{entry}' is not a choice.")


    def two_player_game(self) -> None:
        state = GameState.new()
        self.show_board(state)
        while state.result is Result.IN_PROGRESS:
            state = self.human_move(state)
        self.say(result_line(state))
        # Interim (tasks.md T023): back to the start menu until US3 adds the game-over menu.

    def show_board(self, state: GameState) -> None:
        self.say()
        self.say(render_board(state.board))
        self.say()

    def human_move(self, state: GameState) -> GameState:
        """Ask until an accepted move; return the new state, board redrawn (C-6 to C-8)."""
        while True:
            entry = self.ask(move_prompt(state.turn))
            square = parse_move(entry)
            if square is None:
                self.say(unreadable(entry.strip()))
                continue
            try:
                new_state = state.play(square)
            except IllegalMove as err:
                self.say(rejection(err.reason, err.square))
                continue
            self.show_board(new_state)
            return new_state


def run(stdin: TextIO, stdout: TextIO, opponent_factory=None) -> int:
    """Run one session on the given streams; return the exit status (contracts/cli.md §1)."""
    return _App(stdin, stdout, opponent_factory).run()
