from fastapi import Request

from app.config import Settings, get_settings
from app.core.i18n import get_locale_from_request, get_translator


def get_app_settings() -> Settings:
    return get_settings()


def get_request_locale(request: Request) -> str:
    return get_locale_from_request(request)


def get_request_translator(request: Request):
    locale = get_locale_from_request(request)
    return get_translator(locale)
