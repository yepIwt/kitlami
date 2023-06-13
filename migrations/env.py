# noqa: E401
from alembic import context
from sqlalchemy import create_engine

from kitlami.app.auth.models import User  # noqa: F401
from kitlami.config import settings
from kitlami.db import Base

config = context.config


def run_migrations_online() -> None:
    engine = create_engine(settings.ALEMBIC_DATABASE_URL)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
