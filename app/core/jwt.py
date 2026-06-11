from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt
from fastapi import Request, Response

from app.config import Settings
from app.core.token_blacklist import blacklist_token, is_token_blacklisted

TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"


def _create_token(user_id: UUID, settings: Settings, token_type: str, expire_seconds: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "jti": str(uuid4()),
        "type": token_type,
        "iat": now,
        "exp": now + timedelta(seconds=expire_seconds),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: UUID, settings: Settings) -> str:
    return _create_token(user_id, settings, TOKEN_TYPE_ACCESS, settings.jwt_access_token_expire_seconds)


def create_refresh_token(user_id: UUID, settings: Settings) -> str:
    return _create_token(user_id, settings, TOKEN_TYPE_REFRESH, settings.jwt_refresh_token_expire_seconds)


def _decode_token_payload(token: str, settings: Settings) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        return None


def _token_ttl_seconds(payload: dict) -> int:
    exp = payload.get("exp")
    if exp is None:
        return 0
    return max(0, int(exp - datetime.now(timezone.utc).timestamp()))


def revoke_token(token: str | None, settings: Settings) -> None:
    if not token:
        return
    payload = _decode_token_payload(token, settings)
    if payload is None:
        return
    jti = payload.get("jti")
    if jti:
        blacklist_token(jti, _token_ttl_seconds(payload))


def _validate_token_payload(payload: dict, expected_type: str) -> dict | None:
    if payload.get("type") != expected_type:
        return None
    jti = payload.get("jti")
    if jti and is_token_blacklisted(jti):
        return None
    return payload


def decode_access_token(token: str, settings: Settings) -> UUID | None:
    payload = _decode_token_payload(token, settings)
    if payload is None:
        return None
    payload = _validate_token_payload(payload, TOKEN_TYPE_ACCESS)
    if payload is None:
        return None
    return UUID(payload["sub"])


def decode_refresh_token(token: str, settings: Settings) -> UUID | None:
    payload = _decode_token_payload(token, settings)
    if payload is None:
        return None
    payload = _validate_token_payload(payload, TOKEN_TYPE_REFRESH)
    if payload is None:
        return None
    return UUID(payload["sub"])


def get_access_token_from_request(request: Request, settings: Settings) -> str | None:
    authorization = request.headers.get("Authorization")
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    return request.cookies.get(settings.jwt_cookie_name)


def get_refresh_token_from_request(
    request: Request,
    settings: Settings,
    body_token: str | None = None,
) -> str | None:
    if body_token:
        return body_token
    return request.cookies.get(settings.jwt_refresh_cookie_name)


def attach_access_token_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        key=settings.jwt_cookie_name,
        value=token,
        max_age=settings.jwt_access_token_expire_seconds,
        httponly=settings.jwt_cookie_httponly,
        secure=settings.jwt_cookie_secure,
        samesite="lax",
    )


def attach_refresh_token_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        key=settings.jwt_refresh_cookie_name,
        value=token,
        max_age=settings.jwt_refresh_token_expire_seconds,
        httponly=settings.jwt_cookie_httponly,
        secure=settings.jwt_cookie_secure,
        samesite="lax",
    )


def attach_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
    settings: Settings,
) -> None:
    attach_access_token_cookie(response, access_token, settings)
    attach_refresh_token_cookie(response, refresh_token, settings)


def clear_access_token_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        key=settings.jwt_cookie_name,
        httponly=settings.jwt_cookie_httponly,
        secure=settings.jwt_cookie_secure,
        samesite="lax",
    )


def clear_refresh_token_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        key=settings.jwt_refresh_cookie_name,
        httponly=settings.jwt_cookie_httponly,
        secure=settings.jwt_cookie_secure,
        samesite="lax",
    )


def clear_auth_cookies(response: Response, settings: Settings) -> None:
    clear_access_token_cookie(response, settings)
    clear_refresh_token_cookie(response, settings)
