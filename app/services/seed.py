from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.roles import UserRole
from app.core.security import hash_password
from app.data.world_cup_2026 import (
    WC2026_GROUP_MATCHES,
    WC2026_GROUP_MATCH_COUNT,
    WC2026_TEAM_COUNT,
    WC2026_TEAMS,
)
from app.models.match import Match
from app.models.team import Team
from app.models.user import User


@dataclass
class SeedResult:
    teams_created: int
    matches_created: int
    admin_created: bool
    demo_user_created: bool


def normalize_kickoff_utc(kickoff: datetime) -> datetime:
    """Ensure kickoff is timezone-aware UTC."""
    if kickoff.tzinfo is None:
        return kickoff.replace(tzinfo=timezone.utc)
    return kickoff.astimezone(timezone.utc)


def _get_or_create_team(db: Session, *, name: str, code: str, group_name: str | None) -> tuple[Team, bool]:
    team = db.scalar(select(Team).where(Team.code == code))
    if team is not None:
        if team.group_name != group_name:
            team.group_name = group_name
        if team.name != name:
            team.name = name
        return team, False

    team = Team(name=name, code=code, group_name=group_name)
    db.add(team)
    db.flush()
    return team, True


def _get_or_create_user(
    db: Session,
    *,
    username: str,
    password: str,
    display_name: str,
    role: str,
    locale: str,
    timezone_name: str,
) -> tuple[User, bool]:
    normalized = username.strip().lower()
    user = db.scalar(select(User).where(User.username == normalized))
    if user is not None:
        return user, False

    user = User(
        username=normalized,
        password_hash=hash_password(password),
        display_name=display_name,
        role=role,
        locale=locale,
        timezone=timezone_name,
    )
    db.add(user)
    db.flush()
    return user, True


def _upsert_match(
    db: Session,
    *,
    home_team: Team,
    away_team: Team,
    kickoff_time: datetime,
    stage: str,
    group_name: str | None,
) -> bool:
    existing = db.scalar(
        select(Match).where(
            Match.home_team_id == home_team.id,
            Match.away_team_id == away_team.id,
        )
    )
    if existing is not None:
        if existing.kickoff_time != kickoff_time:
            existing.kickoff_time = kickoff_time
        if existing.group_name != group_name:
            existing.group_name = group_name
        return False

    db.add(
        Match(
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            kickoff_time=kickoff_time,
            stage=stage,
            group_name=group_name,
        )
    )
    return True


def run_seed(db: Session, settings: Settings) -> SeedResult:
    """Insert FIFA World Cup 2026 teams, group-stage matches, and dev users."""
    teams_created = 0
    team_by_code: dict[str, Team] = {}

    for team_data in WC2026_TEAMS:
        team, created = _get_or_create_team(db, **team_data)
        team_by_code[team.code] = team
        if created:
            teams_created += 1

    matches_created = 0
    for match_data in WC2026_GROUP_MATCHES:
        home_team = team_by_code[match_data["home_code"]]
        away_team = team_by_code[match_data["away_code"]]
        kickoff_time = normalize_kickoff_utc(match_data["kickoff_utc"])
        created = _upsert_match(
            db,
            home_team=home_team,
            away_team=away_team,
            kickoff_time=kickoff_time,
            stage="group",
            group_name=match_data["group_name"],
        )
        if created:
            matches_created += 1

    _, admin_created = _get_or_create_user(
        db,
        username=settings.seed_admin_username,
        password=settings.seed_admin_password,
        display_name="Pool Admin",
        role=UserRole.ADMIN,
        locale=settings.default_locale,
        timezone_name=settings.default_timezone,
    )
    _, demo_user_created = _get_or_create_user(
        db,
        username=settings.seed_user_username,
        password=settings.seed_user_password,
        display_name="Demo Player",
        role=UserRole.USER,
        locale=settings.default_locale,
        timezone_name="America/Sao_Paulo",
    )

    db.commit()

    return SeedResult(
        teams_created=teams_created,
        matches_created=matches_created,
        admin_created=admin_created,
        demo_user_created=demo_user_created,
    )


def seed_summary(db: Session) -> dict[str, int]:
    """Return counts of core seed entities (for smoke tests)."""
    return {
        "teams": db.scalar(select(func.count()).select_from(Team)) or 0,
        "matches": db.scalar(select(func.count()).select_from(Match)) or 0,
        "users": db.scalar(select(func.count()).select_from(User)) or 0,
        "admins": db.scalar(select(func.count()).select_from(User).where(User.role == UserRole.ADMIN)) or 0,
    }


__all__ = [
    "SeedResult",
    "WC2026_GROUP_MATCH_COUNT",
    "WC2026_TEAM_COUNT",
    "normalize_kickoff_utc",
    "run_seed",
    "seed_summary",
]
