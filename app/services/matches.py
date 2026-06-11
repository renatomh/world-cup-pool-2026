from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.datetime_format import localize_datetime, match_local_date, utc_window_for_local_date
from app.models.match import Match


def list_match_dates(db: Session, timezone_name: str) -> list[date]:
    """Distinct calendar dates with matches, ordered chronologically in the user's timezone."""
    kickoffs = db.scalars(select(Match.kickoff_time).order_by(Match.kickoff_time)).all()
    dates: list[date] = []
    seen: set[date] = set()
    for kickoff in kickoffs:
        day = match_local_date(kickoff, timezone_name)
        if day not in seen:
            seen.add(day)
            dates.append(day)
    return dates


def default_match_date(
    dates: list[date],
    timezone_name: str,
    now: datetime | None = None,
) -> date:
    """Pick the best default day: today during the tournament, else first or last day."""
    now = now or datetime.now(timezone.utc)
    today = localize_datetime(now, timezone_name).date()
    if not dates:
        return today
    if today < dates[0]:
        return dates[0]
    if today > dates[-1]:
        return dates[-1]
    for day in dates:
        if day >= today:
            return day
    return dates[-1]


def resolve_match_date(
    dates: list[date],
    requested: date | None,
    timezone_name: str,
    now: datetime | None = None,
) -> date:
    """Resolve a requested date to a valid tournament day."""
    if not dates:
        return default_match_date(dates, timezone_name, now)
    if requested is None:
        return default_match_date(dates, timezone_name, now)
    if requested in dates:
        return requested
    if requested < dates[0]:
        return dates[0]
    if requested > dates[-1]:
        return dates[-1]
    for day in dates:
        if day >= requested:
            return day
    return dates[-1]


def adjacent_dates(dates: list[date], current: date) -> tuple[date | None, date | None]:
    """Previous and next tournament dates relative to the current day."""
    if current not in dates:
        return None, None
    index = dates.index(current)
    prev_date = dates[index - 1] if index > 0 else None
    next_date = dates[index + 1] if index < len(dates) - 1 else None
    return prev_date, next_date


def get_matches_for_date(db: Session, match_date: date, timezone_name: str) -> list[Match]:
    """Matches whose kickoff falls on the given calendar day in the user's timezone."""
    utc_start, utc_end = utc_window_for_local_date(match_date, timezone_name)
    return list(
        db.scalars(
            select(Match)
            .options(joinedload(Match.home_team), joinedload(Match.away_team))
            .where(Match.kickoff_time >= utc_start, Match.kickoff_time < utc_end)
            .order_by(Match.kickoff_time)
        ).all()
    )


def get_match_day(
    db: Session,
    *,
    timezone_name: str,
    requested_date: date | None = None,
    now: datetime | None = None,
) -> tuple[date, date | None, date | None, list[Match]]:
    """Resolve date navigation and return matches for that day."""
    dates = list_match_dates(db, timezone_name)
    selected = resolve_match_date(dates, requested_date, timezone_name, now)
    prev_date, next_date = adjacent_dates(dates, selected)
    matches = get_matches_for_date(db, selected, timezone_name)
    return selected, prev_date, next_date, matches
