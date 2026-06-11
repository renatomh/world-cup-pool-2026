from datetime import datetime, timedelta, timezone

from app.core.bet_lock import bet_lock_time, is_bet_locked


KICKOFF = datetime(2026, 6, 15, 20, 0, tzinfo=timezone.utc)
LOCK_MINUTES = 15


def test_bet_lock_time_is_before_kickoff():
    lock_at = bet_lock_time(KICKOFF, LOCK_MINUTES)
    assert lock_at == KICKOFF - timedelta(minutes=LOCK_MINUTES)


def test_bet_not_locked_before_window():
    now = KICKOFF - timedelta(minutes=LOCK_MINUTES + 1)
    assert is_bet_locked(KICKOFF, now, LOCK_MINUTES) is False


def test_bet_locked_at_lock_window():
    now = KICKOFF - timedelta(minutes=LOCK_MINUTES)
    assert is_bet_locked(KICKOFF, now, LOCK_MINUTES) is True


def test_bet_locked_after_kickoff():
    now = KICKOFF + timedelta(minutes=5)
    assert is_bet_locked(KICKOFF, now, LOCK_MINUTES) is True
