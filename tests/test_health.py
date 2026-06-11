def test_api_health_returns_ok(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "app_name" in payload
    assert "environment" in payload


def test_swagger_docs_available(client):
    response = client.get("/api/v1/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()


def test_redoc_available(client):
    response = client.get("/api/v1/redoc")
    assert response.status_code == 200
    assert "redoc" in response.text.lower()
