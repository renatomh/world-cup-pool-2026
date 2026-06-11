def test_signup_returns_token_pair_and_user(client):
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "alice",
            "password": "password123",
            "display_name": "Alice",
        },
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
    assert payload["refresh_token"]
    assert payload["user"]["username"] == "alice"
    assert "wc_pool_access_token" in response.cookies
    assert "wc_pool_refresh_token" in response.cookies


def test_signup_rejects_duplicate_username(client, registered_user):
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": registered_user["username"],
            "password": "password123",
            "display_name": "Another Player",
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "username_taken"


def test_login_returns_token_pair(client, registered_user):
    client.cookies.clear()
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": registered_user["username"],
            "password": "password123",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["access_token"]
    assert payload["refresh_token"]
    assert payload["user"]["username"] == registered_user["username"]


def test_login_rejects_invalid_credentials(client, registered_user):
    client.cookies.clear()
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": registered_user["username"],
            "password": "wrong-password",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "invalid_credentials"


def test_me_requires_authentication(client):
    client.cookies.clear()
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user_with_cookie(client, registered_user):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["username"] == registered_user["username"]


def test_me_accepts_bearer_token(client, auth_tokens):
    token = auth_tokens["access_token"]
    client.cookies.clear()
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == auth_tokens["user"]["username"]


def test_refresh_issues_new_token_pair(client, auth_tokens):
    old_refresh = auth_tokens["refresh_token"]
    client.cookies.clear()

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["access_token"]
    assert payload["refresh_token"]
    assert payload["refresh_token"] != old_refresh

    client.cookies.clear()
    stale = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh},
    )
    assert stale.status_code == 401


def test_refresh_with_rotated_token_works(client, auth_tokens):
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": auth_tokens["refresh_token"]},
    )
    new_refresh = refresh_response.json()["refresh_token"]
    client.cookies.clear()

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": new_refresh},
    )
    assert response.status_code == 200


def test_logout_blacklists_tokens(client, auth_tokens):
    access_token = auth_tokens["access_token"]
    refresh_token = auth_tokens["refresh_token"]
    client.cookies.clear()

    response = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh_token},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_response.status_code == 401

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_response.status_code == 401


def test_logout_clears_cookies(client, registered_user):
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 204

    me_response = client.get("/api/v1/auth/me")
    assert me_response.status_code == 401
