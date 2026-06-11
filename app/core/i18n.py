from collections.abc import Callable

from fastapi import Request

from app.config import get_settings

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "World Cup Pool 2026": "World Cup Pool 2026",
        "Welcome to the betting pool for the 2026 FIFA World Cup.": (
            "Welcome to the betting pool for the 2026 FIFA World Cup."
        ),
        "Matches": "Matches",
        "Leaderboard": "Leaderboard",
        "Save Bet": "Save Bet",
        "API": "API",
        "Health": "Health",
    },
    "pt_BR": {
        "World Cup Pool 2026": "Bolão Copa do Mundo 2026",
        "Welcome to the betting pool for the 2026 FIFA World Cup.": (
            "Bem-vindo ao bolão da Copa do Mundo FIFA 2026."
        ),
        "Matches": "Jogos",
        "Leaderboard": "Classificação",
        "Save Bet": "Salvar Palpite",
        "API": "API",
        "Health": "Status",
    },
}


def get_locale_from_request(request: Request) -> str:
    settings = get_settings()
    query_locale = request.query_params.get("lang")
    if query_locale and query_locale in settings.locale_list:
        return query_locale

    accept_language = request.headers.get("accept-language", "")
    for part in accept_language.split(","):
        candidate = part.split(";")[0].strip()
        if candidate in settings.locale_list:
            return candidate
        if candidate.startswith("pt") and "pt_BR" in settings.locale_list:
            return "pt_BR"

    return settings.default_locale


def get_translator(locale: str) -> Callable[[str], str]:
    catalog = TRANSLATIONS.get(locale, TRANSLATIONS["en"])

    def translate(message: str) -> str:
        return catalog.get(message, message)

    return translate
