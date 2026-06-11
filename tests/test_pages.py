def test_landing_page_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "World Cup Pool 2026" in response.text or "Bolão Copa do Mundo 2026" in response.text
    assert "Join the pool" in response.text or "Entrar no bolão" in response.text


def test_home_redirects_when_unauthenticated(client):
    response = client.get("/home", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_home_renders_when_authenticated(client, registered_user):
    response = client.get("/home")
    assert response.status_code == 200
    assert registered_user["display_name"] in response.text


def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert 'name="username"' in response.text
    assert 'name="password"' in response.text


def test_signup_page_renders(client):
    response = client.get("/signup")
    assert response.status_code == 200
    assert 'name="display_name"' in response.text
    assert 'name="password_confirm"' in response.text


def test_signup_rejects_mismatched_passwords(client):
    response = client.post(
        "/signup",
        data={
            "display_name": "Test User",
            "username": "testuser",
            "password": "password123",
            "password_confirm": "different",
        },
    )
    assert response.status_code == 200
    assert "do not match" in response.text or "não coincidem" in response.text


def test_web_signup_logs_in_and_redirects_home(client):
    response = client.post(
        "/signup",
        data={
            "display_name": "Web Player",
            "username": "webplayer",
            "password": "password123",
            "password_confirm": "password123",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/home"

    home_response = client.get("/home")
    assert home_response.status_code == 200
    assert "Web Player" in home_response.text


def test_web_logout_redirects_to_landing(client, registered_user):
    response = client.post("/logout", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/"

    home_response = client.get("/home", follow_redirects=False)
    assert home_response.status_code == 303
    assert home_response.headers["location"] == "/login"
