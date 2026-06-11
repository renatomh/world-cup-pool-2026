from datetime import datetime, timezone

from app.core.datetime_format import format_datetime, format_datetime_for_user, localize_datetime


UTC_KICKOFF = datetime(2026, 6, 11, 20, 0, tzinfo=timezone.utc)


def test_localize_datetime_converts_utc_to_user_timezone():
    localized = localize_datetime(UTC_KICKOFF, "America/Sao_Paulo")
    assert localized.hour == 17
    assert localized.minute == 0


def test_format_datetime_english_12_hour_clock():
    formatted = format_datetime(UTC_KICKOFF, timezone_name="America/New_York", locale="en")
    assert formatted == "Jun 11, 2026, 4:00 PM"


def test_format_datetime_portuguese_brazil():
    formatted = format_datetime(UTC_KICKOFF, timezone_name="America/Sao_Paulo", locale="pt_BR")
    assert formatted == "11 de jun. de 2026, 17:00"


def test_format_datetime_for_user_matches_api_helper():
    formatted = format_datetime_for_user(
        UTC_KICKOFF,
        timezone_name="America/Chicago",
        locale="en",
    )
    assert formatted == "Jun 11, 2026, 3:00 PM"


def test_format_datetime_handles_naive_datetime_as_utc():
    naive = datetime(2026, 6, 11, 20, 0)
    formatted = format_datetime(naive, timezone_name="UTC", locale="en")
    assert formatted == "Jun 11, 2026, 8:00 PM"


def test_format_datetime_unknown_timezone_falls_back_to_utc():
    formatted = format_datetime(UTC_KICKOFF, timezone_name="Not/A_Real_Zone", locale="en")
    assert formatted == "Jun 11, 2026, 8:00 PM"
