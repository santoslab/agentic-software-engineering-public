import pytest

import main
from game import Game


# ---------- Helpers ----------

def scripted_input(monkeypatch, inputs):
    """Patch builtins.input to feed values from `inputs` in order."""
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda *a, **kw: next(it))


def scripted_ai(monkeypatch, moves):
    """Patch ComputerAI.random_move to return (row, col) values from `moves`."""
    it = iter(moves)
    monkeypatch.setattr(
        "computer_ai.ComputerAI.random_move",
        staticmethod(lambda game: next(it)),
    )


# A canonical 9-move 2-player input chain that lands X a horizontal 5-win on row 1:
# X plays (1,1)..(1,5); O plays (9,1)..(9,4).
X_WIN_2P_INPUTS = ["11", "91", "12", "92", "13", "93", "14", "94", "15"]


# ---------- _read_menu_choice (SPECS §6.3) ----------

def test_read_menu_choice_accepts_valid(monkeypatch):
    """SPECS §6.3: valid single-digit menu choice is returned."""
    scripted_input(monkeypatch, ["2"])
    assert main._read_menu_choice(3) == 2


def test_read_menu_choice_reprompts_on_non_digit(monkeypatch, capsys):
    """SPECS §6.3: non-digit input is rejected and re-prompted."""
    scripted_input(monkeypatch, ["abc", "2"])
    assert main._read_menu_choice(3) == 2
    assert "Invalid input" in capsys.readouterr().out


def test_read_menu_choice_reprompts_on_out_of_range(monkeypatch, capsys):
    """SPECS §6.3: in-range digit constraint — '0' and '4' (when num_options=3) are rejected."""
    scripted_input(monkeypatch, ["0", "4", "3"])
    assert main._read_menu_choice(3) == 3
    assert capsys.readouterr().out.count("Invalid input") == 2


# ---------- _prompt_human (SPECS §6.2) ----------

def test_prompt_human_accepts_valid_move(monkeypatch):
    """SPECS §6.2: a 2-char digit input pointing at an empty cell returns (row, col)."""
    g = Game()
    scripted_input(monkeypatch, ["35"])
    assert main._prompt_human(g) == (3, 5)


@pytest.mark.parametrize("bad_input", [
    "",       # empty (length 0)
    "5",      # length 1
    "555",    # length 3
    "05",     # contains '0' in first position
    "50",     # contains '0' in second position
    "a5",     # non-digit first
    "5a",     # non-digit second
    "  ",     # all whitespace stripped to empty
])
def test_prompt_human_rejects_invalid_forms(monkeypatch, capsys, bad_input):
    """SPECS §6.2: every invalid move form is rejected and re-prompted."""
    g = Game()
    scripted_input(monkeypatch, [bad_input, "35"])
    assert main._prompt_human(g) == (3, 5)
    out = capsys.readouterr().out
    assert "Invalid input" in out


def test_prompt_human_rejects_occupied_cell(monkeypatch, capsys):
    """SPECS §6.2: pointing at an occupied cell is rejected with a distinct message."""
    g = Game()
    g.make_move(5, 5)  # (5, 5) is now occupied.
    scripted_input(monkeypatch, ["55", "11"])
    assert main._prompt_human(g) == (1, 1)
    assert "already occupied" in capsys.readouterr().out


# ---------- _computer_turn (SPECS §5.3) ----------

def test_computer_turn_returns_move_and_announces(monkeypatch, capsys):
    """SPECS §5.3: _computer_turn returns the AI's move and prints an announcement."""
    g = Game()
    g.make_move(5, 5)  # X plays; computer is O.
    scripted_ai(monkeypatch, [(1, 1)])
    move = main._computer_turn(g)
    assert move == (1, 1)
    assert "Computer (O) plays 11." in capsys.readouterr().out


# ---------- _announce_result (SPECS §5.3 post-game menu) ----------

def test_announce_result_x_wins(capsys):
    """SPECS §5.3: announce 'X wins!' when winner is X."""
    g = Game()
    g.winner = 'X'
    main._announce_result(g)
    assert "X wins!" in capsys.readouterr().out


def test_announce_result_o_wins(capsys):
    """SPECS §5.3: announce 'O wins!' when winner is O."""
    g = Game()
    g.winner = 'O'
    main._announce_result(g)
    assert "O wins!" in capsys.readouterr().out


def test_announce_result_tie(capsys):
    """SPECS §5.3: announce 'It's a tie!' on a tie."""
    g = Game()
    g.winner = 'tie'
    main._announce_result(g)
    assert "It's a tie!" in capsys.readouterr().out


# ---------- main_menu (SPECS §5.3) ----------

def test_main_menu_displays_and_returns_choice(monkeypatch, capsys):
    """SPECS §5.3: main_menu prints the menu and returns the selected option."""
    scripted_input(monkeypatch, ["2"])
    assert main.main_menu() == 2
    assert "TIC-TAC-TOE" in capsys.readouterr().out


# ---------- play_game (SPECS §5.3 per-game loop) ----------

def test_play_game_runs_to_x_win():
    """SPECS §5.3: per-game loop terminates when the game is over."""
    g = Game()
    moves = iter([(1, 1), (9, 1), (1, 2), (9, 2),
                  (1, 3), (9, 3), (1, 4), (9, 4), (1, 5)])
    main.play_game(g, lambda _g: next(moves))
    assert g.winner == 'X'
    assert g.is_over() is True


def test_play_game_renders_board_each_turn(capsys):
    """SPECS §5.3 step 1: the board is rendered before each turn.

    A 9-move game produces 9 renders. Each render contains 2 border lines, so
    we expect 18 occurrences of the border in the captured output.
    """
    g = Game()
    moves = iter([(1, 1), (9, 1), (1, 2), (9, 2),
                  (1, 3), (9, 3), (1, 4), (9, 4), (1, 5)])
    main.play_game(g, lambda _g: next(moves))
    border = "+-------------------+"
    assert capsys.readouterr().out.count(border) == 18


# ---------- post_game_menu (SPECS §5.3) ----------

@pytest.mark.parametrize("choice_input,expected", [("1", 1), ("2", 2), ("3", 3)])
def test_post_game_menu_returns_choice(monkeypatch, choice_input, expected):
    """SPECS §5.3: post_game_menu returns the user's selection."""
    g = Game()
    g.winner = 'X'
    scripted_input(monkeypatch, [choice_input])
    assert main.post_game_menu(g) == expected


def test_post_game_menu_announces_tie(monkeypatch, capsys):
    """SPECS §5.3: post_game_menu announces a tie."""
    g = Game()
    g.winner = 'tie'
    scripted_input(monkeypatch, ["3"])
    main.post_game_menu(g)
    assert "It's a tie!" in capsys.readouterr().out


# ---------- one_player_mode (SPECS §5.3) ----------

def test_one_player_mode_alternates_human_symbol_both_ways(monkeypatch, capsys):
    """SPECS §5.3: in 1-player mode, human's symbol alternates after each Play Again.

    Three games verify both ternary branches:
      Game 1 (human=X): human wins row 1.
      Play Again -> human flips X->O. Game 2 (human=O, computer=X): computer wins row 1.
      Play Again -> human flips O->X. Game 3 (human=X again): human wins row 1.
      Main Menu -> exits one_player_mode.
    """
    scripted_ai(monkeypatch, [
        # Game 1: computer (O) plays harmless cells in row 9.
        (9, 1), (9, 2), (9, 3), (9, 4),
        # Game 2: computer (X) wins row 1 — moves first.
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
        # Game 3: computer (O) again plays row 9.
        (9, 1), (9, 2), (9, 3), (9, 4),
    ])
    scripted_input(monkeypatch, [
        # Game 1 human (X) wins row 1.
        "11", "12", "13", "14", "15",
        # Post-game: Play Again.
        "1",
        # Game 2 human (O) plays harmless cells in row 5 (only 4 turns needed
        # because computer wins on its 5th move).
        "51", "52", "53", "54",
        # Post-game: Play Again.
        "1",
        # Game 3 human (X) wins row 1 again.
        "11", "12", "13", "14", "15",
        # Post-game: Main Menu.
        "2",
    ])

    main.one_player_mode()

    out = capsys.readouterr().out
    # Game 1 and 3: human is X. Game 2: computer is X.
    assert out.count("X wins!") == 3
    # Game 2 explicitly proves the flip: human plays as O and computer as X.
    assert "Your turn (O)" in out
    assert "Computer (X) plays" in out


def test_one_player_mode_quit_exits_program(monkeypatch):
    """SPECS §5.3: choosing Quit from the 1-player post-game raises SystemExit."""
    scripted_ai(monkeypatch, [(9, 1), (9, 2), (9, 3), (9, 4)])
    scripted_input(monkeypatch, [
        "11", "12", "13", "14", "15",   # Game: human wins row 1.
        "3",                              # Post-game: Quit.
    ])
    with pytest.raises(SystemExit):
        main.one_player_mode()


# ---------- two_player_mode (SPECS §5.3) ----------

def test_two_player_mode_play_again_then_main_menu(monkeypatch, capsys):
    """SPECS §5.3: 2-player mode supports Play Again followed by Main Menu."""
    scripted_input(monkeypatch, X_WIN_2P_INPUTS + ["1"] + X_WIN_2P_INPUTS + ["2"])
    main.two_player_mode()
    assert capsys.readouterr().out.count("X wins!") == 2


def test_two_player_mode_main_menu_returns(monkeypatch):
    """SPECS §5.3: choosing Main Menu after a 2-player game returns cleanly."""
    scripted_input(monkeypatch, X_WIN_2P_INPUTS + ["2"])
    main.two_player_mode()


def test_two_player_mode_quit_exits(monkeypatch):
    """SPECS §5.3: choosing Quit from the 2-player post-game raises SystemExit."""
    scripted_input(monkeypatch, X_WIN_2P_INPUTS + ["3"])
    with pytest.raises(SystemExit):
        main.two_player_mode()


# ---------- main (SPECS §5.3 top-level entry) ----------

def test_main_quit_from_top_menu(monkeypatch):
    """SPECS §5.3: Quit from the top menu raises SystemExit."""
    scripted_input(monkeypatch, ["3"])
    with pytest.raises(SystemExit):
        main.main()


def test_main_routes_to_one_player_mode(monkeypatch):
    """SPECS §5.3: top menu '1' enters 1-player mode; Main Menu returns to top; Quit exits."""
    scripted_ai(monkeypatch, [(9, 1), (9, 2), (9, 3), (9, 4)])
    scripted_input(monkeypatch, [
        "1",                                  # Top menu -> 1-player.
        "11", "12", "13", "14", "15",         # Human wins row 1.
        "2",                                  # Post-game -> Main Menu.
        "3",                                  # Top menu -> Quit.
    ])
    with pytest.raises(SystemExit):
        main.main()


def test_main_routes_to_two_player_mode(monkeypatch):
    """SPECS §5.3: top menu '2' enters 2-player mode; Main Menu returns to top; Quit exits."""
    scripted_input(monkeypatch, [
        "2",                                  # Top menu -> 2-player.
        *X_WIN_2P_INPUTS,                     # 2-player game; X wins.
        "2",                                  # Post-game -> Main Menu.
        "3",                                  # Top menu -> Quit.
    ])
    with pytest.raises(SystemExit):
        main.main()


def test_one_player_human_resets_to_x_after_main_menu(monkeypatch, capsys):
    """SPECS §5.3 Post-Game Menu: Main Menu resets 1-player human-symbol alternation.

    Re-entering 1-player mode after a Main Menu return must start with the human
    as X again, not as O (which would happen if alternation persisted).
    """
    scripted_ai(monkeypatch, [
        # Session 1: computer is O, plays row 9.
        (9, 1), (9, 2), (9, 3), (9, 4),
        # Session 2: if reset works, computer is O again (not X).
        (9, 1), (9, 2), (9, 3), (9, 4),
    ])
    scripted_input(monkeypatch, [
        "1",                                  # Top -> 1-player.
        "11", "12", "13", "14", "15",         # Session 1: human (X) wins row 1.
        "2",                                  # Post-game -> Main Menu (resets alternation).
        "1",                                  # Top -> 1-player again.
        "11", "12", "13", "14", "15",         # Session 2: human must still be X.
        "2",                                  # Post-game -> Main Menu.
        "3",                                  # Top -> Quit.
    ])
    with pytest.raises(SystemExit):
        main.main()

    out = capsys.readouterr().out
    assert out.count("X wins!") == 2
    assert "Computer (X) plays" not in out
