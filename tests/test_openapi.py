def test_web_routes_are_excluded_from_openapi_schema(client):
    schema = client.get("/api/v1/openapi.json").json()
    paths = schema["paths"]

    assert "/login" not in paths
    assert "/matches" not in paths or "/api/v1/matches" in paths
    assert "/api/v1/matches" in paths
    assert "/api/v1/auth/login" in paths
