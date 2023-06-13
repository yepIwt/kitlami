from datetime import timedelta
from typing import Any, Mapping

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    APP_NAME = "kitlami-backend"
    TASKS_NAME = "kitlami-tasks"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str
    POSTGRES_TEST_DATABASE: str | None = None
    DATABASE_URL: str | None = None
    TEST_DATABASE_URL: str | None = None
    ALEMBIC_DATABASE_URL: str | None = None

    SERVER_PORT: int = 8000
    SERVER_HOST: str = "0.0.0.0"

    JWT_SECRET: str
    JWT_ALG: str

    ACCESS_TOKEN_EXP = timedelta(days=1)
    REFRESH_TOKEN_EXP = timedelta(days=30)

    class Config:
        env_file = ".env"

    @validator("DATABASE_URL", pre=True)
    def assemble_postgres_db_url(cls, v: str | None, values: Mapping[str, Any]) -> str:
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_DATABASE"]}',
            )
        )

    @validator("ALEMBIC_DATABASE_URL", pre=True)
    def assemble_alembic_database_url(cls, v: str | None, values: Mapping[str, Any]) -> str:
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_DATABASE"]}',
            )
        )

    @validator("TEST_DATABASE_URL", pre=True)
    def assemble_test_postgres_url(cls, v: str | None, values: Mapping[str, Any]) -> str:
        if not values.get("POSTGRES_TEST_DATABASE"):
            return ""
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_TEST_DATABASE"]}',
            )
        )


settings = Settings()  # type: ignore