from datetime import date, datetime, timezone

from app.core.datetime_format import localize_datetime
from app.data.world_cup_2026 import WC2026_GROUP_MATCHES, WC2026_TEAMS
from app.services.seed import normalize_kickoff_utc


def test_all_teams_have_unique_codes_and_valid_groups():
    codes = [team["code"] for team in WC2026_TEAMS]
    assert len(codes) == len(set(codes))
    assert len(WC2026_TEAMS) == 48
    for team in WC2026_TEAMS:
        assert team["group_name"] in "ABCDEFGHIJKL"


def test_group_stage_has_72_matches():
    assert len(WC2026_GROUP_MATCHES) == 72
    groups = {match["group_name"] for match in WC2026_GROUP_MATCHES}
    assert groups == set("ABCDEFGHIJKL")
    for match in WC2026_GROUP_MATCHES:
        assert match["home_code"] != match["away_code"]


def test_opening_match_stored_in_utc_and_displays_mexico_city_local():
    opening = WC2026_GROUP_MATCHES[0]
    utc = normalize_kickoff_utc(opening["kickoff_utc"])
    assert utc == datetime(2026, 6, 11, 19, 0, tzinfo=timezone.utc)

    local = localize_datetime(utc, "America/Mexico_City")
    assert local.date() == date(2026, 6, 11)
    assert local.hour == 13
    assert local.minute == 0


def test_dallas_match_stored_in_utc_and_displays_central_local():
    ned_jpn = next(m for m in WC2026_GROUP_MATCHES if m["home_code"] == "NED" and m["away_code"] == "JPN")
    utc = normalize_kickoff_utc(ned_jpn["kickoff_utc"])
    assert utc == datetime(2026, 6, 14, 20, 0, tzinfo=timezone.utc)

    local = localize_datetime(utc, "America/Chicago")
    assert local.date() == date(2026, 6, 14)
    assert local.hour == 15
    assert local.minute == 0
