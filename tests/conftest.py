import fakeredis
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.core.token_blacklist as token_blacklist_module
from app.database import get_db
from app.main import app
from app.models import Base


@pytest.fixture(autouse=True)
def test_environment(monkeypatch):
    fake_redis = fakeredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(token_blacklist_module, "get_redis", lambda: fake_redis)

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr("app.database.SessionLocal", testing_session_local)
    monkeypatch.setattr("app.main.SessionLocal", testing_session_local)

    yield

    app.dependency_overrides.clear()
    fake_redis.flushall()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_tokens(client: TestClient) -> dict:
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "poolplayer",
            "password": "password123",
            "display_name": "Pool Player",
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def registered_user(auth_tokens: dict) -> dict:
    return auth_tokens["user"]
