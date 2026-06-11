from app.redis_client import get_redis

BLACKLIST_PREFIX = "jwt:blacklist:"


def blacklist_token(jti: str, ttl_seconds: int) -> None:
    if ttl_seconds > 0:
        get_redis().setex(f"{BLACKLIST_PREFIX}{jti}", ttl_seconds, "1")


def is_token_blacklisted(jti: str) -> bool:
    return bool(get_redis().exists(f"{BLACKLIST_PREFIX}{jti}"))
