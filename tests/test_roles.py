import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app.core.roles import UserRole
from app.core.security import hash_password
from app.dependencies import get_current_admin
from app.models.user import User


def _request_with_user(user: User | None) -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [],
    }
    request = Request(scope)
    request.state.user = user
    return request


def test_signup_assigns_user_role(client):
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "roleuser",
            "password": "password123",
            "display_name": "Role User",
        },
    )
    assert response.status_code == 201
    assert response.json()["user"]["role"] == UserRole.USER


def test_get_current_admin_allows_admin():
    admin = User(
        username="admin",
        password_hash=hash_password("password123"),
        display_name="Admin",
        role=UserRole.ADMIN,
    )
    user = get_current_admin(_request_with_user(admin))
    assert user.role == UserRole.ADMIN


def test_get_current_admin_rejects_regular_user():
    regular = User(
        username="player",
        password_hash=hash_password("password123"),
        display_name="Player",
        role=UserRole.USER,
    )
    with pytest.raises(HTTPException) as exc_info:
        get_current_admin(_request_with_user(regular))
    assert exc_info.value.status_code == 403
