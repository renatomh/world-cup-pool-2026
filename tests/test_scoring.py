from app.core.scoring import CORRECT_RESULT_POINTS, EXACT_SCORE_POINTS, calculate_bet_points


def test_exact_score_awards_max_points():
    assert calculate_bet_points(2, 1, 2, 1) == EXACT_SCORE_POINTS


def test_correct_result_only_awards_one_point():
    assert calculate_bet_points(2, 0, 3, 1) == CORRECT_RESULT_POINTS


def test_wrong_prediction_awards_zero_points():
    assert calculate_bet_points(1, 0, 0, 1) == 0


def test_draw_prediction_on_actual_draw():
    assert calculate_bet_points(0, 0, 1, 1) == CORRECT_RESULT_POINTS
