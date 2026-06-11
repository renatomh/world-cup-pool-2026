from pathlib import Path

from fastapi.templating import Jinja2Templates
from jinja2 import pass_context

from app.core.datetime_format import format_date as format_date_value
from app.core.datetime_format import format_datetime as format_datetime_value
from app.core.i18n import get_translator
from app.core.team_logos import team_logo_url

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def _(message: str, locale: str = "en") -> str:
    return get_translator(locale)(message)


@pass_context
def format_datetime_filter(
    context: dict,
    dt,
    timezone_name: str | None = None,
    locale: str | None = None,
) -> str:
    request = context.get("request")
    if timezone_name is None and request is not None:
        user = getattr(request.state, "user", None)
        if user is not None:
            timezone_name = user.timezone
    if locale is None and request is not None:
        locale = getattr(request.state, "locale", None)
    return format_datetime_value(
        dt,
        timezone_name=timezone_name or "UTC",
        locale=locale or "en",
    )


@pass_context
def format_date_filter(context: dict, match_date, locale: str | None = None) -> str:
    request = context.get("request")
    if locale is None and request is not None:
        locale = getattr(request.state, "locale", None)
    return format_date_value(match_date, locale=locale or "en")


templates.env.globals["_"] = _
templates.env.filters["format_datetime"] = format_datetime_filter
templates.env.filters["format_date"] = format_date_filter
templates.env.filters["team_logo_url"] = team_logo_url
