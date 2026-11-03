# Conformance Report: 001-five-in-a-row

**Generated**: 2026-10-26 18:54 | **Spec**: `specs/001-five-in-a-row/spec.md` | **Tests tagged**: 78

**Summary**: no evidence: 19, pass: 35

Status: **pass** — every tagged test passed; **FAIL** — a tagged test failed; **manual** — checked by hand (see quickstart.md); **partial** — some tagged tests skipped or not run; **no evidence** — no test is tagged with this ID.

## Functional Requirements

| ID | Tests | Status |
|----|-------|--------|
| FR-001 | `engine/test_board.py::test_new_board_has_81_empty_squares_in_row_major_order`<br>`engine/test_state.py::test_new_game` | pass |
| FR-002 | `cli/test_two_player.py::test_x_wins_a_full_game`<br>`cli/test_two_player.py::test_game_starts_with_an_empty_board_and_x_to_move`<br>`engine/test_board.py::test_mark_other_swaps_x_and_o`<br>`engine/test_state.py::test_new_game` | pass |
| FR-003 | `cli/test_two_player.py::test_x_wins_a_full_game`<br>`cli/test_two_player.py::test_game_starts_with_an_empty_board_and_x_to_move`<br>`engine/test_state.py::test_accepted_move_places_mark_and_passes_turn`<br>`engine/test_state.py::test_play_does_not_change_the_old_state` | pass |
| FR-004 | `cli/test_parse.py::test_two_integers_separated_by_spaces_or_a_comma_are_a_square[4 7]`<br>`cli/test_parse.py::test_two_integers_separated_by_spaces_or_a_comma_are_a_square[4,7]`<br>`cli/test_parse.py::test_two_integers_separated_by_spaces_or_a_comma_are_a_square[ 4 , 7 ]`<br>`cli/test_parse.py::test_two_integers_separated_by_spaces_or_a_comma_are_a_square[4   7]`<br>`cli/test_parse.py::test_out_of_range_integers_are_readable_and_left_for_the_engine[0 3-square0]`<br>`cli/test_parse.py::test_out_of_range_integers_are_readable_and_left_for_the_engine[10 3-square1]`<br>`cli/test_parse.py::test_out_of_range_integers_are_readable_and_left_for_the_engine[-1 3-square2]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[abc]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[5]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[1 2 3]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[   ]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[4;7]`<br>`cli/test_render.py::test_board_has_numbered_columns_numbered_rows_and_every_mark`<br>`engine/test_board.py::test_squares_are_equal_by_row_and_column`<br>`engine/test_board.py::test_at_off_board_square_raises[square0]`<br>`engine/test_board.py::test_at_off_board_square_raises[square1]`<br>`engine/test_board.py::test_at_off_board_square_raises[square2]`<br>`engine/test_board.py::test_at_off_board_square_raises[square3]` | pass |
| FR-005 | `cli/test_two_player.py::test_occupied_square_is_rejected_and_the_same_mark_asked_again`<br>`cli/test_two_player.py::test_out_of_range_square_is_rejected_and_the_same_mark_asked_again`<br>`cli/test_two_player.py::test_unreadable_input_is_rejected_and_the_same_mark_asked_again`<br>`engine/test_state.py::test_out_of_range_is_rejected[square0]`<br>`engine/test_state.py::test_out_of_range_is_rejected[square1]`<br>`engine/test_state.py::test_out_of_range_is_rejected[square2]`<br>`engine/test_state.py::test_out_of_range_is_rejected[square3]`<br>`engine/test_state.py::test_occupied_is_rejected`<br>`engine/test_state.py::test_game_over_is_rejected_before_other_reasons`<br>`engine/test_state.py::test_out_of_range_is_reported_before_occupied` | pass |
| FR-006 | `cli/test_render.py::test_board_has_numbered_columns_numbered_rows_and_every_mark`<br>`cli/test_two_player.py::test_x_wins_a_full_game`<br>`cli/test_two_player.py::test_game_starts_with_an_empty_board_and_x_to_move`<br>`cli/test_two_player.py::test_a_move_appears_on_the_board_and_o_is_asked_next` | pass |
| FR-007 | `cli/test_two_player.py::test_x_wins_a_full_game`<br>`cli/test_two_player.py::test_game_starts_with_an_empty_board_and_x_to_move` | pass |
| FR-008 | `engine/test_state.py::test_row_win`<br>`engine/test_state.py::test_column_win`<br>`engine/test_state.py::test_diagonal_win`<br>`engine/test_state.py::test_anti_diagonal_win`<br>`engine/test_state.py::test_o_wins_too`<br>`engine/test_state.py::test_six_in_a_row_by_filling_a_gap_wins`<br>`engine/test_state.py::test_two_lines_at_once_is_one_win` | pass |
| FR-009 | `cli/test_two_player.py::test_x_wins_a_full_game`<br>`cli/test_two_player.py::test_game_starts_with_an_empty_board_and_x_to_move`<br>`cli/test_two_player.py::test_o_wins_a_full_game`<br>`engine/test_state.py::test_game_over_is_rejected_before_other_reasons`<br>`engine/test_state.py::test_row_win`<br>`engine/test_state.py::test_column_win`<br>`engine/test_state.py::test_diagonal_win`<br>`engine/test_state.py::test_anti_diagonal_win` | pass |
| FR-010 | `cli/test_two_player.py::test_a_full_board_without_a_line_is_a_draw`<br>`engine/test_state.py::test_win_on_the_last_square_is_a_win`<br>`engine/test_state.py::test_full_board_without_a_win_is_a_draw` | pass |
| FR-011 | `cli/test_two_player.py::test_x_wins_a_full_game`<br>`cli/test_two_player.py::test_game_starts_with_an_empty_board_and_x_to_move`<br>`cli/test_two_player.py::test_the_opponent_factory_is_not_called_in_two_player_games` | pass |
| FR-012 | — | **no evidence** |
| FR-013 | — | **no evidence** |
| FR-014 | `cli/test_parse.py::test_a_menu_entry_is_its_number_with_surrounding_spaces_ignored[1-1]`<br>`cli/test_parse.py::test_a_menu_entry_is_its_number_with_surrounding_spaces_ignored[3-3]`<br>`cli/test_parse.py::test_a_menu_entry_is_its_number_with_surrounding_spaces_ignored[ 2 -2]`<br>`cli/test_parse.py::test_a_menu_entry_is_its_number_with_surrounding_spaces_ignored[\t3  -3]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[0]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[4]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[x]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[   ]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[1 2]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[01]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[+1]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[-1]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[1_0]`<br>`cli/test_parse.py::test_the_number_of_choices_sets_the_upper_bound`<br>`cli/test_start_menu.py::test_start_menu_offers_exactly_three_numbered_choices` | pass |
| FR-015 | — | **no evidence** |
| FR-016 | `cli/test_start_menu.py::test_quit_ends_the_program`<br>`cli/test_start_menu.py::test_quit_accepts_surrounding_spaces` | pass |
| FR-017 | `cli/test_parse.py::test_a_menu_entry_is_its_number_with_surrounding_spaces_ignored[1-1]`<br>`cli/test_parse.py::test_a_menu_entry_is_its_number_with_surrounding_spaces_ignored[3-3]`<br>`cli/test_parse.py::test_a_menu_entry_is_its_number_with_surrounding_spaces_ignored[ 2 -2]`<br>`cli/test_parse.py::test_a_menu_entry_is_its_number_with_surrounding_spaces_ignored[\t3  -3]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[0]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[4]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[x]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[   ]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[1 2]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[01]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[+1]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[-1]`<br>`cli/test_parse.py::test_anything_outside_the_choices_is_not_a_choice[1_0]`<br>`cli/test_parse.py::test_the_number_of_choices_sets_the_upper_bound`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[7]`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[x]`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[]`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[1 2]` | pass |
| FR-018 | — | **no evidence** |
| FR-019 | — | **no evidence** |
| FR-020 | `cli/test_end_of_input.py::test_end_of_input_at_the_start_menu[empty]`<br>`cli/test_end_of_input.py::test_end_of_input_at_the_start_menu[after-invalid-choice]`<br>`cli/test_end_of_input.py::test_interrupt_at_the_start_menu`<br>`cli/test_two_player.py::test_end_of_input_mid_game_prints_goodbye_and_returns_zero` | pass |

## Success Criteria

| ID | Tests | Status |
|----|-------|--------|
| SC-001 | — | **no evidence** |
| SC-002 | — | **no evidence** |
| SC-003 | `cli/test_two_player.py::test_o_wins_a_full_game`<br>`cli/test_two_player.py::test_a_full_board_without_a_line_is_a_draw`<br>`engine/test_state.py::test_full_board_without_a_win_is_a_draw`<br>`engine/test_state.py::test_four_in_a_line_is_not_a_win`<br>`engine/test_state.py::test_five_broken_by_a_gap_is_not_a_win`<br>`engine/test_state.py::test_five_broken_by_the_other_mark_is_not_a_win` | pass |
| SC-004 | — | **no evidence** |
| SC-005 | — | **no evidence** |
| SC-006 | `cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[7]`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[x]`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[]`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[1 2]`<br>`cli/test_two_player.py::test_occupied_square_is_rejected_and_the_same_mark_asked_again`<br>`cli/test_two_player.py::test_out_of_range_square_is_rejected_and_the_same_mark_asked_again`<br>`cli/test_two_player.py::test_unreadable_input_is_rejected_and_the_same_mark_asked_again`<br>`engine/test_state.py::test_out_of_range_is_rejected[square0]`<br>`engine/test_state.py::test_out_of_range_is_rejected[square1]`<br>`engine/test_state.py::test_out_of_range_is_rejected[square2]`<br>`engine/test_state.py::test_out_of_range_is_rejected[square3]`<br>`engine/test_state.py::test_occupied_is_rejected` | pass |

## Acceptance Scenarios

| ID | Tests | Status |
|----|-------|--------|
| US1-1 | `cli/test_two_player.py::test_x_wins_a_full_game`<br>`cli/test_two_player.py::test_game_starts_with_an_empty_board_and_x_to_move` | pass |
| US1-2 | `cli/test_two_player.py::test_x_wins_a_full_game`<br>`cli/test_two_player.py::test_game_starts_with_an_empty_board_and_x_to_move`<br>`cli/test_two_player.py::test_a_move_appears_on_the_board_and_o_is_asked_next`<br>`engine/test_state.py::test_accepted_move_places_mark_and_passes_turn` | pass |
| US1-3 | `cli/test_two_player.py::test_x_wins_a_full_game`<br>`cli/test_two_player.py::test_game_starts_with_an_empty_board_and_x_to_move`<br>`engine/test_state.py::test_row_win` | pass |
| US1-4 | `engine/test_state.py::test_diagonal_win` | pass |
| US1-5 | `engine/test_state.py::test_anti_diagonal_win` | pass |
| US1-6 | `engine/test_state.py::test_six_in_a_row_by_filling_a_gap_wins` | pass |
| US1-7 | `cli/test_two_player.py::test_a_full_board_without_a_line_is_a_draw`<br>`engine/test_state.py::test_full_board_without_a_win_is_a_draw` | pass |
| US2-1 | — | **no evidence** |
| US2-2 | — | **no evidence** |
| US2-3 | — | **no evidence** |
| US2-4 | — | **no evidence** |
| US2-5 | — | **no evidence** |
| US2-6 | — | **no evidence** |
| US2-7 | — | **no evidence** |
| US3-1 | `cli/test_start_menu.py::test_start_menu_offers_exactly_three_numbered_choices` | pass |
| US3-2 | — | **no evidence** |
| US3-3 | — | **no evidence** |
| US3-4 | `cli/test_start_menu.py::test_quit_ends_the_program` | pass |
| US3-5 | — | **no evidence** |
| US3-6 | `cli/test_end_of_input.py::test_end_of_input_at_the_start_menu[empty]`<br>`cli/test_end_of_input.py::test_end_of_input_at_the_start_menu[after-invalid-choice]`<br>`cli/test_end_of_input.py::test_interrupt_at_the_start_menu`<br>`cli/test_two_player.py::test_end_of_input_mid_game_prints_goodbye_and_returns_zero` | pass |

## Edge Cases

| ID | Tests | Status |
|----|-------|--------|
| EDGE-occupied-square | `cli/test_two_player.py::test_occupied_square_is_rejected_and_the_same_mark_asked_again`<br>`engine/test_state.py::test_occupied_is_rejected` | pass |
| EDGE-out-of-range-square | `cli/test_parse.py::test_out_of_range_integers_are_readable_and_left_for_the_engine[0 3-square0]`<br>`cli/test_parse.py::test_out_of_range_integers_are_readable_and_left_for_the_engine[10 3-square1]`<br>`cli/test_parse.py::test_out_of_range_integers_are_readable_and_left_for_the_engine[-1 3-square2]`<br>`cli/test_two_player.py::test_out_of_range_square_is_rejected_and_the_same_mark_asked_again`<br>`engine/test_state.py::test_out_of_range_is_rejected[square0]`<br>`engine/test_state.py::test_out_of_range_is_rejected[square1]`<br>`engine/test_state.py::test_out_of_range_is_rejected[square2]`<br>`engine/test_state.py::test_out_of_range_is_rejected[square3]` | pass |
| EDGE-unreadable-input | `cli/test_parse.py::test_anything_else_is_unreadable[abc]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[5]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[1 2 3]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[   ]`<br>`cli/test_parse.py::test_anything_else_is_unreadable[4;7]`<br>`cli/test_two_player.py::test_unreadable_input_is_rejected_and_the_same_mark_asked_again` | pass |
| EDGE-invalid-menu-choice | `cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[7]`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[x]`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[]`<br>`cli/test_start_menu.py::test_invalid_choice_is_rejected_and_the_menu_shown_again[1 2]` | pass |
| EDGE-more-than-five-in-a-row | `engine/test_state.py::test_six_in_a_row_by_filling_a_gap_wins` | pass |
| EDGE-win-on-the-last-square | `engine/test_state.py::test_win_on_the_last_square_is_a_win` | pass |
| EDGE-two-lines-at-once | `engine/test_state.py::test_two_lines_at_once_is_one_win` | pass |
| EDGE-end-of-input-or-interrupt | `cli/test_end_of_input.py::test_end_of_input_at_the_start_menu[empty]`<br>`cli/test_end_of_input.py::test_end_of_input_at_the_start_menu[after-invalid-choice]`<br>`cli/test_end_of_input.py::test_interrupt_at_the_start_menu`<br>`cli/test_two_player.py::test_end_of_input_mid_game_prints_goodbye_and_returns_zero` | pass |

## Unknown IDs

None.
