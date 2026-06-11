from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

MONTHS_EN = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

MONTHS_PT_BR = [
    "jan.",
    "fev.",
    "mar.",
    "abr.",
    "mai.",
    "jun.",
    "jul.",
    "ago.",
    "set.",
    "out.",
    "nov.",
    "dez.",
]


def _resolve_timezone(timezone_name: str):
    if timezone_name in {"UTC", "Etc/UTC", "GMT"}:
        return timezone.utc
    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        return timezone.utc


def localize_datetime(dt: datetime, timezone_name: str) -> datetime:
    """Convert a UTC-aware datetime to the given IANA timezone."""
    if dt.tzinfo is None:
        utc_dt = dt.replace(tzinfo=timezone.utc)
    else:
        utc_dt = dt.astimezone(timezone.utc)

    target_tz = _resolve_timezone(timezone_name)
    if target_tz is timezone.utc:
        return utc_dt
    return utc_dt.astimezone(target_tz)


def format_datetime(
    dt: datetime | None,
    *,
    timezone_name: str = "UTC",
    locale: str = "en",
) -> str:
    """Format a UTC datetime for display in the user's timezone and locale."""
    if dt is None:
        return ""

    localized = localize_datetime(dt, timezone_name)
    day = localized.day
    month = localized.month
    year = localized.year
    hour = localized.hour
    minute = localized.minute

    if locale == "pt_BR":
        month_label = MONTHS_PT_BR[month - 1]
        return f"{day} de {month_label} de {year}, {hour:02d}:{minute:02d}"

    month_label = MONTHS_EN[month - 1]
    period = "AM" if hour < 12 else "PM"
    hour_12 = hour % 12 or 12
    return f"{month_label} {day}, {year}, {hour_12}:{minute:02d} {period}"


def format_datetime_for_user(dt: datetime | None, *, timezone_name: str, locale: str) -> str:
    """API helper: format a datetime using a user's timezone and locale preferences."""
    return format_datetime(dt, timezone_name=timezone_name, locale=locale)


def match_local_date(kickoff_utc: datetime, timezone_name: str) -> date:
    """Calendar date of a UTC kickoff in the user's timezone."""
    return localize_datetime(kickoff_utc, timezone_name).date()


def format_date(match_date: date, *, locale: str = "en") -> str:
    """Format a calendar date for display."""
    if locale == "pt_BR":
        return f"{match_date.day} de {MONTHS_PT_BR[match_date.month - 1]} de {match_date.year}"
    return f"{MONTHS_EN[match_date.month - 1]} {match_date.day}, {match_date.year}"


def utc_window_for_local_date(match_date: date, timezone_name: str) -> tuple[datetime, datetime]:
    """Return UTC [start, end) bounds for a calendar day in the given timezone."""
    target_tz = _resolve_timezone(timezone_name)
    start_local = datetime.combine(match_date, time.min, tzinfo=target_tz)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)
