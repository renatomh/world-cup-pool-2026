from fastapi import Request
from fastapi.responses import RedirectResponse

from app.config import Settings
from app.core.roles import UserRole


def page_context(settings: Settings) -> dict:
    return {
        "app_name": settings.app_name,
        "locales": settings.locale_list,
    }


def require_login(request: Request) -> RedirectResponse | None:
    if request.state.user is None:
        return RedirectResponse(url="/login", status_code=303)
    return None


def require_admin(request: Request) -> RedirectResponse | None:
    redirect = require_login(request)
    if redirect is not None:
        return redirect
    if request.state.user.role != UserRole.ADMIN:
        return RedirectResponse(url="/home", status_code=303)
    return None
