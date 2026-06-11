from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.datetime_format import format_date
from app.database import get_db
from app.dependencies import get_app_settings, get_request_translator
from app.services.matches import get_match_day
from app.templates import templates
from app.web.common import page_context, require_login

router = APIRouter(tags=["web-matches"])


def _match_day_context(
    request: Request,
    db: Session,
    match_date: date | None,
) -> dict:
    user = request.state.user
    selected, prev_date, next_date, matches = get_match_day(
        db,
        timezone_name=user.timezone,
        requested_date=match_date,
    )
    return {
        "selected_date": selected,
        "selected_date_display": format_date(selected, locale=user.locale),
        "prev_date": prev_date,
        "next_date": next_date,
        "matches": matches,
    }


@router.get("/matches", response_class=HTMLResponse)
def matches_page(
    request: Request,
    match_date: date | None = Query(None, alias="date"),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_app_settings),
    _: object = Depends(get_request_translator),
):
    redirect = require_login(request)
    if redirect is not None:
        return redirect

    return templates.TemplateResponse(
        request,
        "matches.html",
        {
            **page_context(settings),
            **_match_day_context(request, db, match_date),
        },
    )


@router.get("/matches/day", response_class=HTMLResponse)
def matches_day_partial(
    request: Request,
    match_date: date | None = Query(None, alias="date"),
    db: Session = Depends(get_db),
    _: object = Depends(get_request_translator),
):
    redirect = require_login(request)
    if redirect is not None:
        return redirect

    return templates.TemplateResponse(
        request,
        "partials/match_day.html",
        _match_day_context(request, db, match_date),
    )
