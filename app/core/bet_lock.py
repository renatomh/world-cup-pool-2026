from datetime import datetime, timedelta, timezone


def bet_lock_time(kickoff: datetime, lock_minutes: int) -> datetime:
    """Return the UTC instant when bets close for a match."""
    if kickoff.tzinfo is None:
        kickoff = kickoff.replace(tzinfo=timezone.utc)
    else:
        kickoff = kickoff.astimezone(timezone.utc)
    return kickoff - timedelta(minutes=lock_minutes)


def is_bet_locked(kickoff: datetime, now: datetime, lock_minutes: int) -> bool:
    """True when the current time is at or past the bet lock window."""
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    else:
        now = now.astimezone(timezone.utc)
    return now >= bet_lock_time(kickoff, lock_minutes)
