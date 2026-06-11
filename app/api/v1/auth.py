from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.i18n import get_locale_from_request
from app.core.jwt import (
    attach_auth_cookies,
    clear_auth_cookies,
    decode_refresh_token,
    get_access_token_from_request,
    get_refresh_token_from_request,
    revoke_token,
)
from app.database import get_db
from app.dependencies import get_app_settings, get_current_user
from app.models.user import User
from app.schemas.user import AuthResponse, LoginRequest, LogoutRequest, RefreshRequest, SignupRequest, UserResponse
from app.services.auth import AuthError, authenticate_user, get_user_by_id, issue_token_pair, register_user

router = APIRouter(prefix="/auth", tags=["auth"])

AUTH_STATUS_CODES = {
    "username_taken": status.HTTP_409_CONFLICT,
    "invalid_credentials": status.HTTP_401_UNAUTHORIZED,
    "inactive_user": status.HTTP_403_FORBIDDEN,
    "invalid_refresh_token": status.HTTP_401_UNAUTHORIZED,
}


def _raise_auth_error(code: str) -> None:
    raise HTTPException(
        status_code=AUTH_STATUS_CODES.get(code, status.HTTP_400_BAD_REQUEST),
        detail={"code": code, "detail": code},
    )


def _signup_locale_timezone(
    request: Request,
    settings: Settings,
    payload: SignupRequest,
) -> tuple[str, str]:
    locale = payload.locale or get_locale_from_request(request)
    if locale not in settings.locale_list:
        locale = settings.default_locale
    timezone = payload.timezone or settings.default_timezone
    return locale, timezone


def _auth_response(user: User, settings: Settings, response: Response) -> AuthResponse:
    access_token, refresh_token = issue_token_pair(user, settings)
    attach_auth_cookies(response, access_token, refresh_token, settings)
    return AuthResponse(access_token=access_token, refresh_token=refresh_token, user=user)


def _revoke_request_tokens(request: Request, settings: Settings, refresh_token: str | None = None) -> None:
    revoke_token(get_access_token_from_request(request, settings), settings)
    revoke_token(get_refresh_token_from_request(request, settings, refresh_token), settings)


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(
    payload: SignupRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_app_settings),
) -> AuthResponse:
    locale, timezone = _signup_locale_timezone(request, settings, payload)
    try:
        user = register_user(
            db,
            username=payload.username,
            password=payload.password,
            display_name=payload.display_name,
            locale=locale,
            timezone=timezone,
        )
    except AuthError as exc:
        _raise_auth_error(exc.code)

    return _auth_response(user, settings, response)


@router.post("/login", response_model=AuthResponse)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_app_settings),
) -> AuthResponse:
    try:
        user = authenticate_user(db, payload.username, payload.password)
    except AuthError as exc:
        _raise_auth_error(exc.code)

    return _auth_response(user, settings, response)


@router.post("/refresh", response_model=AuthResponse)
def refresh_tokens(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_app_settings),
    payload: RefreshRequest | None = None,
) -> AuthResponse:
    body_token = payload.refresh_token if payload else None
    refresh_token = get_refresh_token_from_request(request, settings, body_token)
    if not refresh_token:
        _raise_auth_error("invalid_refresh_token")

    user_id = decode_refresh_token(refresh_token, settings)
    if user_id is None:
        _raise_auth_error("invalid_refresh_token")

    revoke_token(refresh_token, settings)

    user = get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        _raise_auth_error("invalid_refresh_token")

    return _auth_response(user, settings, response)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    settings: Settings = Depends(get_app_settings),
    payload: LogoutRequest | None = None,
) -> Response:
    refresh_token = payload.refresh_token if payload else None
    _revoke_request_tokens(request, settings, refresh_token)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    clear_auth_cookies(response, settings)
    return response


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
