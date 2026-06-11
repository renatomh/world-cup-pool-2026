from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.i18n import get_locale_from_request
from app.core.jwt import (
    attach_auth_cookies,
    clear_auth_cookies,
    get_access_token_from_request,
    get_refresh_token_from_request,
    revoke_token,
)
from app.database import get_db
from app.dependencies import get_app_settings, get_request_translator
from app.services.auth import AuthError, authenticate_user, issue_token_pair, register_user
from app.templates import templates

router = APIRouter(tags=["web-auth"])

AUTH_MESSAGES = {
    "username_taken": "This username is already taken.",
    "invalid_credentials": "Invalid username or password.",
    "inactive_user": "This account is inactive.",
}


def _page_context(request: Request, settings: Settings, auth_message: str | None = None) -> dict:
    return {
        "app_name": settings.app_name,
        "locales": settings.locale_list,
        "auth_message": auth_message,
    }


def _translate_auth_error(request: Request, code: str) -> str:
    message = AUTH_MESSAGES.get(code, code)
    return request.state._(message)


def _set_auth_cookies(response: RedirectResponse, user, settings: Settings) -> None:
    access_token, refresh_token = issue_token_pair(user, settings)
    attach_auth_cookies(response, access_token, refresh_token, settings)


def _revoke_auth_tokens(request: Request, settings: Settings) -> None:
    revoke_token(get_access_token_from_request(request, settings), settings)
    revoke_token(get_refresh_token_from_request(request, settings), settings)


@router.get("/login", response_model=None)
def login_page(
    request: Request,
    settings: Settings = Depends(get_app_settings),
    _: object = Depends(get_request_translator),
):
    if request.state.user is not None:
        return RedirectResponse(url="/home", status_code=303)
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        _page_context(request, settings),
    )


@router.post("/login", response_model=None)
def login_submit(
    request: Request,
    settings: Settings = Depends(get_app_settings),
    db: Session = Depends(get_db),
    _: object = Depends(get_request_translator),
    username: str = Form(...),
    password: str = Form(...),
):
    try:
        user = authenticate_user(db, username, password)
    except AuthError as exc:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            _page_context(request, settings, _translate_auth_error(request, exc.code)),
        )

    redirect = RedirectResponse(url="/home", status_code=303)
    _set_auth_cookies(redirect, user, settings)
    return redirect


@router.get("/signup", response_model=None)
def signup_page(
    request: Request,
    settings: Settings = Depends(get_app_settings),
    _: object = Depends(get_request_translator),
):
    if request.state.user is not None:
        return RedirectResponse(url="/home", status_code=303)
    return templates.TemplateResponse(
        request,
        "auth/signup.html",
        _page_context(request, settings),
    )


@router.post("/signup", response_model=None)
def signup_submit(
    request: Request,
    settings: Settings = Depends(get_app_settings),
    db: Session = Depends(get_db),
    _: object = Depends(get_request_translator),
    display_name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
):
    if password != password_confirm:
        return templates.TemplateResponse(
            request,
            "auth/signup.html",
            _page_context(request, settings, request.state._("Passwords do not match.")),
        )

    locale = get_locale_from_request(request)
    if locale not in settings.locale_list:
        locale = settings.default_locale

    try:
        user = register_user(
            db,
            username=username,
            password=password,
            display_name=display_name,
            locale=locale,
            timezone=settings.default_timezone,
        )
    except AuthError as exc:
        return templates.TemplateResponse(
            request,
            "auth/signup.html",
            _page_context(request, settings, _translate_auth_error(request, exc.code)),
        )

    redirect = RedirectResponse(url="/home", status_code=303)
    _set_auth_cookies(redirect, user, settings)
    return redirect


@router.post("/logout")
def logout(
    request: Request,
    settings: Settings = Depends(get_app_settings),
) -> RedirectResponse:
    _revoke_auth_tokens(request, settings)
    redirect = RedirectResponse(url="/", status_code=303)
    clear_auth_cookies(redirect, settings)
    return redirect
