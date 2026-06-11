from sqlalchemy import select

from app.config import get_settings
from app.core.roles import UserRole
from app.data.world_cup_2026 import WC2026_GROUP_MATCH_COUNT, WC2026_TEAM_COUNT
from app.models.match import Match
from app.models.user import User
from app.services.seed import run_seed, seed_summary


def test_seed_creates_admin_matches_and_demo_user(db_session):
    settings = get_settings()
    first = run_seed(db_session, settings)
    second = run_seed(db_session, settings)
    counts = seed_summary(db_session)

    assert first.teams_created == WC2026_TEAM_COUNT
    assert first.matches_created == WC2026_GROUP_MATCH_COUNT
    assert first.admin_created is True
    assert first.demo_user_created is True

    assert second.teams_created == 0
    assert second.matches_created == 0
    assert second.admin_created is False
    assert second.demo_user_created is False

    assert counts["teams"] == WC2026_TEAM_COUNT
    assert counts["matches"] == WC2026_GROUP_MATCH_COUNT
    assert counts["users"] == 2
    assert counts["admins"] == 1

    admin = db_session.scalar(select(User).where(User.username == settings.seed_admin_username))
    demo = db_session.scalar(select(User).where(User.username == settings.seed_user_username))
    assert admin is not None
    assert admin.role == UserRole.ADMIN
    assert demo is not None
    assert demo.role == UserRole.USER

    matches = db_session.scalars(select(Match).order_by(Match.kickoff_time)).all()
    assert len(matches) == WC2026_GROUP_MATCH_COUNT


def test_seeded_demo_user_can_log_in_via_api(client, db_session):
    settings = get_settings()
    run_seed(db_session, settings)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": settings.seed_user_username,
            "password": settings.seed_user_password,
        },
    )
    assert response.status_code == 200
    assert response.json()["user"]["username"] == settings.seed_user_username


def test_seeded_matches_are_queryable_via_api(client, db_session):
    settings = get_settings()
    run_seed(db_session, settings)

    login = client.post(
        "/api/v1/auth/login",
        json={
            "username": settings.seed_user_username,
            "password": settings.seed_user_password,
        },
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/matches",
        params={"date": "2026-06-11"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["date"] == "2026-06-11"
    opening = payload["matches"][0]
    assert opening["home_team"]["code"] == "MEX"
    assert opening["away_team"]["code"] == "RSA"
    assert opening["group_name"] == "A"
    assert opening["kickoff_display"]
    assert opening["home_team"]["logo_url"]
