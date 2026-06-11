from app.config import get_settings
from app.data.world_cup_2026 import WC2026_GROUP_MATCH_COUNT
from app.services.seed import run_seed


def _login(client, db_session):
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
    return response.json()["access_token"], settings


def test_list_matches_returns_date_paginated_payload(client, db_session):
    token, _ = _login(client, db_session)

    response = client.get(
        "/api/v1/matches",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert "date" in payload
    assert "prev_date" in payload
    assert "next_date" in payload
    assert "matches" in payload
    assert isinstance(payload["matches"], list)
    assert len(payload["matches"]) >= 1


def test_list_matches_filters_by_date(client, db_session):
    token, _ = _login(client, db_session)

    response = client.get(
        "/api/v1/matches",
        params={"date": "2026-06-11"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["date"] == "2026-06-11"
    assert payload["matches"]
    match = payload["matches"][0]
    assert match["home_team"]["code"] == "MEX"
    assert match["away_team"]["code"] == "RSA"
    assert match["home_team"]["logo_url"].endswith("/mx.png")
    assert match["away_team"]["logo_url"].endswith("/za.png")


def test_list_matches_all_days_sum_to_group_stage_count(client, db_session):
    token, _ = _login(client, db_session)
    headers = {"Authorization": f"Bearer {token}"}

    first = client.get("/api/v1/matches", headers=headers).json()
    total = len(first["matches"])
    next_date = first["next_date"]
    seen_dates = {first["date"]}

    while next_date:
        page = client.get("/api/v1/matches", params={"date": next_date}, headers=headers).json()
        assert page["date"] not in seen_dates
        seen_dates.add(page["date"])
        total += len(page["matches"])
        next_date = page["next_date"]

    assert total == WC2026_GROUP_MATCH_COUNT
