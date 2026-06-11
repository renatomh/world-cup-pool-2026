def test_api_health_returns_ok(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "app_name" in payload
    assert "environment" in payload


def test_home_page_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "World Cup Pool 2026" in response.text or "Bolão Copa do Mundo 2026" in response.text
