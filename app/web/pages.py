from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.config import Settings
from app.dependencies import get_app_settings, get_request_translator
from app.templates import templates

router = APIRouter(tags=["web"])


def _page_context(settings: Settings) -> dict:
    return {
        "app_name": settings.app_name,
        "locales": settings.locale_list,
    }


@router.get("/", response_class=HTMLResponse)
def landing(
    request: Request,
    settings: Settings = Depends(get_app_settings),
    _: object = Depends(get_request_translator),
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "landing.html",
        _page_context(settings),
    )


@router.get("/home", response_model=None)
def home(
    request: Request,
    settings: Settings = Depends(get_app_settings),
    _: object = Depends(get_request_translator),
):
    if request.state.user is None:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(
        request,
        "home.html",
        _page_context(settings),
    )
