import sys

from game import Game
from computer_ai import ComputerAI


_VALID_DIGITS = "123456789"


def _read_menu_choice(num_options):
    """Prompt and re-prompt until the user enters a valid menu digit.

    Params: num_options — the largest valid choice (choices are 1..num_options).
    Returns: int in [1, num_options].
    """
    while True:
        choice = input("> ").strip()
        if choice.isdigit():
            value = int(choice)
            if 1 <= value <= num_options:
                return value
        print(f"Invalid input. Please enter a digit 1-{num_options}.")


def _prompt_human(game):
    """Prompt and re-prompt until the user enters a valid 2-digit move.

    Params: game — Game instance (used to check cell availability).
    Returns: (row, col) tuple pointing at an empty cell; both ints 1-9.
    """
    while True:
        print(f"\nYour turn ({game.current_player}). Enter a position (e.g. 35 for row 3 col 5):")
        choice = input("> ").strip()
        if len(choice) != 2 or choice[0] not in _VALID_DIGITS or choice[1] not in _VALID_DIGITS:
            print("Invalid input. Please enter two digits 1-9 (e.g. 35).")
            continue
        row, col = int(choice[0]), int(choice[1])
        if (row, col) not in game.available_moves():
            print("That cell is already occupied. Try another.")
            continue
        return row, col


def _computer_turn(game):
    """Ask the AI for a move and announce it on stdout.

    Params: game — Game instance whose current_player is the computer.
    Returns: (row, col) tuple chosen by the AI.
    """
    move = ComputerAI.random_move(game)
    print(f"\nComputer ({game.current_player}) plays {move[0]}{move[1]}.")
    return move


def _announce_result(game):
    """Print the game's outcome ('X wins!', 'O wins!', or 'It's a tie!').

    Params: game — Game instance with self.winner already set.
    """
    if game.winner == 'tie':
        print("It's a tie!")
    else:
        print(f"{game.winner} wins!")


def main_menu():
    """Display the main menu and read the user's selection.

    Returns: int 1 (1-player), 2 (2-player), or 3 (Quit).
    """
    print()
    print("==== TIC-TAC-TOE ====")
    print("1) 1 Player (vs. Computer)")
    print("2) 2 Players")
    print("3) Quit")
    return _read_menu_choice(3)


def one_player_mode():
    """Run human-vs-computer games with human-symbol alternation between rounds.

    Returns when the user selects Main Menu; calls sys.exit(0) on Quit.
    """
    human_symbol = 'X'
    while True:
        game = Game(starting_player='X')

        def on_turn(g, _human=human_symbol):
            if g.current_player == _human:
                return _prompt_human(g)
            return _computer_turn(g)

        play_game(game, on_turn)
        choice = post_game_menu(game)
        if choice == 1:
            human_symbol = 'O' if human_symbol == 'X' else 'X'
        elif choice == 2:
            return
        else:
            sys.exit(0)


def two_player_mode():
    """Run human-vs-human games. X always starts; no alternation.

    Returns when the user selects Main Menu; calls sys.exit(0) on Quit.
    """
    while True:
        game = Game(starting_player='X')
        play_game(game, _prompt_human)
        choice = post_game_menu(game)
        if choice == 1:
            continue
        elif choice == 2:
            return
        else:
            sys.exit(0)


def play_game(game, on_turn):
    """Drive the per-turn loop until the game is over.

    Params: game — Game instance; on_turn — callable taking the game and
        returning a (row, col) move for the current player.
    """
    while not game.is_over():
        print()
        print(game.render())
        row, col = on_turn(game)
        game.make_move(row, col)
        game.check_winner()


def post_game_menu(game):
    """Render the final board, announce the result, and read the next action.

    Params: game — Game instance with self.winner set.
    Returns: int 1 (Play Again), 2 (Main Menu), or 3 (Quit).
    """
    print()
    print(game.render())
    print()
    _announce_result(game)
    print()
    print("1) Play Again")
    print("2) Main Menu")
    print("3) Quit")
    return _read_menu_choice(3)


def main():
    """Top-level loop: route between modes via the main menu until Quit."""
    while True:
        choice = main_menu()
        if choice == 1:
            one_player_mode()
        elif choice == 2:
            two_player_mode()
        else:
            sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    main()
