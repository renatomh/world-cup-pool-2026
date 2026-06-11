from datetime import date, datetime, timezone

from app.config import get_settings
from app.services.matches import (
    adjacent_dates,
    get_match_day,
    get_matches_for_date,
    list_match_dates,
    resolve_match_date,
)
from app.services.seed import run_seed


def test_list_match_dates_groups_by_user_timezone(db_session):
    settings = get_settings()
    run_seed(db_session, settings)

    dates_utc = list_match_dates(db_session, "UTC")
    dates_ny = list_match_dates(db_session, "America/New_York")

    assert len(dates_utc) > 0
    assert dates_utc[0] == date(2026, 6, 11)
    assert dates_ny[0] == date(2026, 6, 11)


def test_get_matches_for_date_returns_only_that_day(db_session):
    settings = get_settings()
    run_seed(db_session, settings)

    opening_day = date(2026, 6, 11)
    matches = get_matches_for_date(db_session, opening_day, "America/Mexico_City")

    assert len(matches) == 2
    assert matches[0].home_team.code == "MEX"
    assert matches[0].away_team.code == "RSA"
    assert matches[1].home_team.code == "KOR"


def test_adjacent_dates_for_tournament_navigation():
    dates = [date(2026, 6, 11), date(2026, 6, 12), date(2026, 6, 13)]
    assert adjacent_dates(dates, date(2026, 6, 11)) == (None, date(2026, 6, 12))
    assert adjacent_dates(dates, date(2026, 6, 12)) == (date(2026, 6, 11), date(2026, 6, 13))
    assert adjacent_dates(dates, date(2026, 6, 13)) == (date(2026, 6, 12), None)


def test_resolve_match_date_clamps_out_of_range_requests():
    dates = [date(2026, 6, 11), date(2026, 6, 12)]
    assert resolve_match_date(dates, date(2026, 6, 5), "UTC") == date(2026, 6, 11)
    assert resolve_match_date(dates, date(2026, 6, 30), "UTC") == date(2026, 6, 12)


def test_get_match_day_returns_navigation_and_matches(db_session):
    settings = get_settings()
    run_seed(db_session, settings)
    frozen_now = datetime(2026, 6, 10, 12, 0, tzinfo=timezone.utc)

    selected, prev_date, next_date, matches = get_match_day(
        db_session,
        timezone_name="America/Mexico_City",
        requested_date=None,
        now=frozen_now,
    )

    assert selected == date(2026, 6, 11)
    assert prev_date is None
    assert next_date is not None
    assert len(matches) == 2
