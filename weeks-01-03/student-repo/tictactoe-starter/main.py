import sys

from game import Game
from computer_ai import ComputerAI


def _read_menu_choice(num_options):
    while True:
        choice = input("> ").strip()
        if choice.isdigit():
            value = int(choice)
            if 1 <= value <= num_options:
                return value
        print(f"Invalid input. Please enter a digit 1-{num_options}.")


def _prompt_human(game):
    while True:
        print(f"\nYour turn ({game.current_player}). Enter a row (1-9):")
        choice = input("> ").strip()
        if not choice.isdigit():
            print("Invalid input. Please enter a digit 1-9.")
            continue
        row = int(choice)
        if row < 1 or row > 9:
            print("Invalid input. Please enter a digit 1-9.")
            continue
        if not game.row_has_space(row):
            print(f"Row {row} is already full. Try another row.")
            continue
        break

    print()
    print(game.render(selected_row=row))

    while True:
        print(f"\nRow {row} chosen. Enter a column (1-9):")
        choice = input("> ").strip()
        if not choice.isdigit():
            print("Invalid input. Please enter a digit 1-9.")
            continue
        col = int(choice)
        if col < 1 or col > 9:
            print("Invalid input. Please enter a digit 1-9.")
            continue
        if game.board[row - 1][col - 1] is not None:
            print(f"Cell ({row}, {col}) is already occupied. Try another column.")
            continue
        return (row, col)


def _computer_turn(game):
    row, col = ComputerAI.random_move(game)
    print(f"\nComputer ({game.current_player}) plays row {row}, column {col}.")
    return (row, col)


def _announce_result(game):
    if game.winner == 'tie':
        print("It's a tie!")
    else:
        print(f"{game.winner} wins!")


def main_menu():
    print()
    print("==== TIC-TAC-TOE ====")
    print("1) 1 Player (vs. Computer)")
    print("2) 2 Players")
    print("3) Quit")
    return _read_menu_choice(3)


def one_player_mode():
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
    while not game.is_over():
        print()
        print(game.render())
        move = on_turn(game)
        game.make_move(*move)
        game.check_winner()


def post_game_menu(game):
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
    while True:
        choice = main_menu()
        if choice == 1:
            one_player_mode()
        elif choice == 2:
            two_player_mode()
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
