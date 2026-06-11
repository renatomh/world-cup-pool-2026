from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.core.i18n import get_locale_from_request, get_translator
from app.core.roles import UserRole
from app.database import get_db
from app.models.user import User

__all__ = [
    "get_app_settings",
    "get_current_admin",
    "get_current_user",
    "get_current_user_optional",
    "get_db",
    "get_request_locale",
    "get_request_translator",
]


def get_app_settings() -> Settings:
    return get_settings()


def get_request_locale(request: Request) -> str:
    return get_locale_from_request(request)


def get_request_translator(request: Request):
    locale = get_locale_from_request(request)
    return get_translator(locale)


def get_current_user_optional(request: Request) -> User | None:
    return getattr(request.state, "user", None)


def get_current_user(request: Request) -> User:
    user = get_current_user_optional(request)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "not_authenticated", "detail": "not_authenticated"},
        )
    return user


def get_current_admin(request: Request) -> User:
    user = get_current_user(request)
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "forbidden", "detail": "admin_required"},
        )
    return user
