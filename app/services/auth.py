from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.jwt import create_access_token, create_refresh_token
from app.core.roles import UserRole
from app.core.security import hash_password, verify_password
from app.models.user import User


class AuthError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def register_user(
    db: Session,
    *,
    username: str,
    password: str,
    display_name: str,
    locale: str,
    timezone: str,
) -> User:
    user = User(
        username=username.strip().lower(),
        password_hash=hash_password(password),
        display_name=display_name.strip(),
        role=UserRole.USER,
        locale=locale,
        timezone=timezone,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise AuthError("username_taken") from exc
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.scalar(select(User).where(User.username == username.strip().lower()))
    if user is None or not verify_password(password, user.password_hash):
        raise AuthError("invalid_credentials")
    if not user.is_active:
        raise AuthError("inactive_user")
    return user


def issue_token_pair(user: User, settings: Settings) -> tuple[str, str]:
    access_token = create_access_token(user.id, settings)
    refresh_token = create_refresh_token(user.id, settings)
    return access_token, refresh_token


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.get(User, user_id)
