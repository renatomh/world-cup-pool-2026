from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.config import Settings
from app.dependencies import get_app_settings, get_request_translator
from app.templates import templates
from app.web.common import page_context, require_login

router = APIRouter(tags=["web-profile"])


@router.get("/profile", response_class=HTMLResponse)
def profile_page(
    request: Request,
    settings: Settings = Depends(get_app_settings),
    _: object = Depends(get_request_translator),
):
    redirect = require_login(request)
    if redirect is not None:
        return redirect

    return templates.TemplateResponse(
        request,
        "profile.html",
        page_context(settings),
    )
