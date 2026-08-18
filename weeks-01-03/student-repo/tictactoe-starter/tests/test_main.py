import pytest

import main
from game import Game


def scripted_input(monkeypatch, inputs):
    """Patch builtins.input to feed values from `inputs` in order."""
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda *a, **kw: next(it))


def scripted_ai(monkeypatch, moves):
    """Patch ComputerAI.random_move to return values from `moves` in order."""
    it = iter(moves)
    monkeypatch.setattr(
        "computer_ai.ComputerAI.random_move",
        staticmethod(lambda game: next(it)),
    )


# ---------- _read_menu_choice ----------

def test_read_menu_choice_accepts_valid(monkeypatch):
    scripted_input(monkeypatch, ["2"])
    assert main._read_menu_choice(3) == 2


def test_read_menu_choice_reprompts_on_invalid(monkeypatch, capsys):
    scripted_input(monkeypatch, ["", "abc", "0", "4", "3"])
    assert main._read_menu_choice(3) == 3
    out = capsys.readouterr().out
    assert out.count("Invalid input") == 4


# ---------- _prompt_human ----------

def test_prompt_human_happy_path(monkeypatch, capsys):
    g = Game()
    scripted_input(monkeypatch, ["5", "5"])
    assert main._prompt_human(g) == (5, 5)
    out = capsys.readouterr().out
    # Caret render appears between row and column input.
    assert "> 5|" in out
    # Both prompts were shown.
    assert "Enter a row" in out
    assert "Enter a column" in out


def test_prompt_human_rejects_non_digit_row_then_accepts(monkeypatch, capsys):
    g = Game()
    scripted_input(monkeypatch, ["abc", "5", "5"])
    assert main._prompt_human(g) == (5, 5)
    assert "Invalid input" in capsys.readouterr().out


def test_prompt_human_rejects_out_of_range_row_then_accepts(monkeypatch, capsys):
    g = Game()
    scripted_input(monkeypatch, ["0", "10", "5", "5"])
    assert main._prompt_human(g) == (5, 5)
    out = capsys.readouterr().out
    assert out.count("Invalid input") == 2


def test_prompt_human_rejects_full_row_then_accepts(monkeypatch, capsys):
    g = Game()
    for c in range(9):
        g.board[4][c] = 'X'  # row 5 is full
    scripted_input(monkeypatch, ["5", "6", "1"])
    assert main._prompt_human(g) == (6, 1)
    out = capsys.readouterr().out
    assert "Row 5 is already full" in out


def test_prompt_human_rejects_non_digit_column_then_accepts(monkeypatch, capsys):
    g = Game()
    scripted_input(monkeypatch, ["5", "abc", "5"])
    assert main._prompt_human(g) == (5, 5)
    out = capsys.readouterr().out
    assert "Invalid input" in out
    # Row prompt only shown once — row choice sticks.
    assert out.count("Enter a row") == 1


def test_prompt_human_rejects_out_of_range_column_then_accepts(monkeypatch, capsys):
    g = Game()
    scripted_input(monkeypatch, ["5", "0", "10", "5"])
    assert main._prompt_human(g) == (5, 5)
    out = capsys.readouterr().out
    assert out.count("Invalid input") == 2


def test_prompt_human_rejects_occupied_cell_column_then_accepts(monkeypatch, capsys):
    g = Game()
    g.make_move(5, 5)  # X at (5, 5)
    scripted_input(monkeypatch, ["5", "5", "6"])
    assert main._prompt_human(g) == (5, 6)
    out = capsys.readouterr().out
    assert "already occupied" in out
    assert "Cell (5, 5)" in out
    # Row prompt only shown once.
    assert out.count("Enter a row") == 1


# ---------- _computer_turn ----------

def test_computer_turn_returns_move_and_announces(monkeypatch, capsys):
    g = Game()
    scripted_ai(monkeypatch, [(3, 7)])
    move = main._computer_turn(g)
    assert move == (3, 7)
    out = capsys.readouterr().out
    assert "Computer (X) plays row 3, column 7." in out


def test_computer_turn_announces_o_when_computer_is_o(monkeypatch, capsys):
    g = Game()
    g.make_move(1, 1)  # now current_player is 'O'
    scripted_ai(monkeypatch, [(3, 7)])
    main._computer_turn(g)
    assert "Computer (O) plays row 3, column 7." in capsys.readouterr().out


# ---------- play_game ----------

def test_play_game_x_wins_via_5_in_a_row():
    g = Game()
    # X plays row 5 cols 1-5; O plays row 9 cols 1-4 in between.
    moves = iter([
        (5, 1), (9, 1), (5, 2), (9, 2), (5, 3), (9, 3), (5, 4), (9, 4), (5, 5),
    ])

    def on_turn(_g):
        return next(moves)

    main.play_game(g, on_turn)
    assert g.winner == 'X'
    assert g.is_over() is True


def test_play_game_renders_board_each_turn(capsys):
    g = Game()
    moves = iter([
        (5, 1), (9, 1), (5, 2), (9, 2), (5, 3), (9, 3), (5, 4), (9, 4), (5, 5),
    ])

    def on_turn(_g):
        return next(moves)

    main.play_game(g, on_turn)
    out = capsys.readouterr().out
    # play_game renders before each of 9 turns.
    assert out.count("     1 2 3 4 5 6 7 8 9") == 9


def test_play_game_handles_tie():
    g = Game()
    # Pre-populate the tie pattern; clear (3, 3) so X (default player) restores it.
    # (3, 3) internal -> (2, 2): (2 + 4) % 5 = 1 -> 'X' in the pattern.
    for r in range(9):
        for c in range(9):
            g.board[r][c] = 'O' if (r + 2 * c) % 5 == 0 else 'X'
    g.board[2][2] = None
    moves = iter([(3, 3)])

    def on_turn(_g):
        return next(moves)

    main.play_game(g, on_turn)
    assert g.winner == 'tie'


# ---------- post_game_menu ----------

@pytest.mark.parametrize("choice_input,expected", [("1", 1), ("2", 2), ("3", 3)])
def test_post_game_menu_returns_choice(monkeypatch, choice_input, expected):
    g = Game()
    g.winner = 'X'
    scripted_input(monkeypatch, [choice_input])
    assert main.post_game_menu(g) == expected


def test_post_game_menu_announces_x_winner(monkeypatch, capsys):
    g = Game()
    g.winner = 'X'
    scripted_input(monkeypatch, ["3"])
    main.post_game_menu(g)
    assert "X wins!" in capsys.readouterr().out


def test_post_game_menu_announces_o_winner(monkeypatch, capsys):
    g = Game()
    g.winner = 'O'
    scripted_input(monkeypatch, ["3"])
    main.post_game_menu(g)
    assert "O wins!" in capsys.readouterr().out


def test_post_game_menu_announces_tie(monkeypatch, capsys):
    g = Game()
    g.winner = 'tie'
    scripted_input(monkeypatch, ["3"])
    main.post_game_menu(g)
    assert "It's a tie!" in capsys.readouterr().out


# ---------- main_menu ----------

def test_main_menu_returns_choice(monkeypatch, capsys):
    scripted_input(monkeypatch, ["2"])
    assert main.main_menu() == 2
    assert "TIC-TAC-TOE" in capsys.readouterr().out


# ---------- one_player_mode ----------

def _human_x_wins_row_1_inputs():
    """Human (X) plays (1,1), (1,2), (1,3), (1,4), (1,5) — wins row 1."""
    return ["1", "1", "1", "2", "1", "3", "1", "4", "1", "5"]


def _computer_o_harmless_in_row_9():
    """Computer (O) plays in row 9 cols 1..4 — does not block the human's row 1 win."""
    return [(9, 1), (9, 2), (9, 3), (9, 4)]


def test_one_player_mode_alternates_human_symbol(monkeypatch, capsys):
    """Game 1: human=X wins row 1. Play Again -> Game 2: computer=X wins row 2."""
    scripted_ai(monkeypatch, [
        # Game 1: computer is O, plays harmless cells.
        (9, 1), (9, 2), (9, 3), (9, 4),
        # Game 2: computer is X, plays row 2 cols 1-5 and wins.
        (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
    ])
    scripted_input(monkeypatch, [
        # Game 1 human (X) plays row 1 cols 1-5.
        *_human_x_wins_row_1_inputs(),
        # Post-game: Play Again.
        "1",
        # Game 2 human (O) plays harmless cells in row 9 (4 moves).
        "9", "1", "9", "2", "9", "3", "9", "4",
        # Post-game: Main Menu.
        "2",
    ])
    main.one_player_mode()
    out = capsys.readouterr().out
    # Game 1: human-X wins; Game 2: computer-X wins.
    assert out.count("X wins!") == 2
    # In Game 2 the human plays as O and the computer plays as X.
    assert "Your turn (O)" in out
    assert "Computer (X) plays" in out


def test_one_player_mode_main_menu_returns(monkeypatch, capsys):
    """Choosing Main Menu from the post-game returns from one_player_mode normally."""
    scripted_ai(monkeypatch, _computer_o_harmless_in_row_9())
    scripted_input(monkeypatch, [*_human_x_wins_row_1_inputs(), "2"])
    main.one_player_mode()  # must return cleanly


def test_one_player_mode_quit_exits_program(monkeypatch):
    """Choosing Quit from the post-game raises SystemExit."""
    scripted_ai(monkeypatch, _computer_o_harmless_in_row_9())
    scripted_input(monkeypatch, [*_human_x_wins_row_1_inputs(), "3"])
    with pytest.raises(SystemExit):
        main.one_player_mode()


# ---------- two_player_mode ----------

def _two_player_x_wins_row_1_inputs():
    """X plays row 1 cols 1-5; O plays row 9 cols 1-4."""
    return [
        "1", "1",  # X (1,1)
        "9", "1",  # O (9,1)
        "1", "2",  # X (1,2)
        "9", "2",  # O (9,2)
        "1", "3",  # X (1,3)
        "9", "3",  # O (9,3)
        "1", "4",  # X (1,4)
        "9", "4",  # O (9,4)
        "1", "5",  # X (1,5) -> wins
    ]


def test_two_player_mode_one_game_then_main_menu(monkeypatch, capsys):
    scripted_input(monkeypatch, [*_two_player_x_wins_row_1_inputs(), "2"])
    main.two_player_mode()
    out = capsys.readouterr().out
    assert "X wins!" in out


def test_two_player_mode_play_again_then_main_menu(monkeypatch, capsys):
    scripted_input(monkeypatch, [
        *_two_player_x_wins_row_1_inputs(),
        "1",  # Play Again
        *_two_player_x_wins_row_1_inputs(),
        "2",  # Main Menu
    ])
    main.two_player_mode()
    assert capsys.readouterr().out.count("X wins!") == 2


def test_two_player_mode_quit_exits(monkeypatch):
    scripted_input(monkeypatch, [*_two_player_x_wins_row_1_inputs(), "3"])
    with pytest.raises(SystemExit):
        main.two_player_mode()


# ---------- main entry point ----------

def test_main_quit_from_top_menu(monkeypatch):
    scripted_input(monkeypatch, ["3"])
    with pytest.raises(SystemExit):
        main.main()


def test_main_routes_to_one_player_mode(monkeypatch):
    scripted_ai(monkeypatch, _computer_o_harmless_in_row_9())
    scripted_input(monkeypatch, [
        "1",                              # top -> 1-player
        *_human_x_wins_row_1_inputs(),    # human X wins
        "2",                              # post-game -> Main Menu
        "3",                              # top -> Quit
    ])
    with pytest.raises(SystemExit):
        main.main()


def test_main_routes_to_two_player_mode(monkeypatch):
    scripted_input(monkeypatch, [
        "2",                                   # top -> 2-player
        *_two_player_x_wins_row_1_inputs(),    # X wins row 1
        "2",                                   # post-game -> Main Menu
        "3",                                   # top -> Quit
    ])
    with pytest.raises(SystemExit):
        main.main()


def test_one_player_human_resets_to_x_after_main_menu(monkeypatch, capsys):
    """SPECS §4.3: choosing Main Menu resets 1-player human-symbol alternation."""
    scripted_ai(monkeypatch, [
        # Session 1: computer is O.
        *_computer_o_harmless_in_row_9(),
        # Session 2: alternation reset -> computer is O again.
        *_computer_o_harmless_in_row_9(),
    ])
    scripted_input(monkeypatch, [
        "1",                              # top -> 1-player
        *_human_x_wins_row_1_inputs(),    # session 1: human X wins
        "2",                              # Main Menu (resets alternation)
        "1",                              # top -> 1-player again
        *_human_x_wins_row_1_inputs(),    # session 2: human X again
        "2",                              # Main Menu
        "3",                              # Quit
    ])
    with pytest.raises(SystemExit):
        main.main()

    out = capsys.readouterr().out
    assert out.count("X wins!") == 2
    assert "Computer (X) plays" not in out
    # "Your turn (X)" appears once per human move; 5 per session, 10 total.
    assert out.count("Your turn (X)") == 10
