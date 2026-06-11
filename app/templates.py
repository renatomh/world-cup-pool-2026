from pathlib import Path

from fastapi.templating import Jinja2Templates

from app.core.i18n import get_translator

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def _(message: str, locale: str = "en") -> str:
    return get_translator(locale)(message)


templates.env.globals["_"] = _
