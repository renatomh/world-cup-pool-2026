"""Match bet scoring rules."""

EXACT_SCORE_POINTS = 3
CORRECT_RESULT_POINTS = 1


def match_outcome(home_score: int, away_score: int) -> str:
    if home_score > away_score:
        return "home"
    if away_score > home_score:
        return "away"
    return "draw"


def calculate_bet_points(
    predicted_home: int,
    predicted_away: int,
    actual_home: int,
    actual_away: int,
) -> int:
    if predicted_home == actual_home and predicted_away == actual_away:
        return EXACT_SCORE_POINTS

    if match_outcome(predicted_home, predicted_away) == match_outcome(actual_home, actual_away):
        return CORRECT_RESULT_POINTS

    return 0
