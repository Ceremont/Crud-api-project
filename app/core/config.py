import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    database_url: str
    allowed_origins: list[str]


def _parse_allowed_origins(value: str) -> list[str]:
    return [origin.strip() for origin in value.split(",") if origin.strip()]


def get_config() -> Config:
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres",
    )
    allowed_origins = _parse_allowed_origins(
        os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    )

    return Config(
        database_url=database_url,
        allowed_origins=allowed_origins,
    )
