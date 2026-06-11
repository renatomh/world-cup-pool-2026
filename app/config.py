from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "World Cup Pool 2026"
    app_env: str = "development"
    secret_key: str = "change-me"
    debug: bool = False

    host: str = "0.0.0.0"
    port: int = 8000

    database_url: str = "postgresql://pool:pool@localhost:5432/world_cup_pool"
    redis_url: str = "redis://localhost:6379/0"

    default_locale: str = "en"
    supported_locales: str = "en,pt_BR"
    default_timezone: str = "UTC"

    bet_lock_minutes_before_kickoff: int = 15

    session_cookie_secure: bool = False
    session_cookie_httponly: bool = True

    @property
    def locale_list(self) -> list[str]:
        return [locale.strip() for locale in self.supported_locales.split(",") if locale.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
