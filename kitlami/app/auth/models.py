import uuid
from enum import StrEnum
from typing import Self

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TEXT, VARCHAR

from kitlami.db.connection import db_session
from kitlami.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    class UserRole(StrEnum):
        USER = "user"

    first_name = sa.Column("first_name", VARCHAR(50), nullable=True)
    last_name = sa.Column("last_name", VARCHAR(50), nullable=True)
    email = sa.Column("email", VARCHAR(254), nullable=False)
    picture_url = sa.Column("picture_url", TEXT, nullable=True)
    hashed_password = sa.Column("hashed_password", TEXT, nullable=True)

    @classmethod
    async def create(cls, email: str, hashed_password: str):
        query = (
            sa.insert(User)
            .values(
                email=email,
                hashed_password=hashed_password,
            )
            .returning(User.id)
        )
        result = await db_session.get().execute(query)
        return result.scalars().first()

    @classmethod
    async def update(
        cls,
        user_id: uuid.UUID,
        first_name: str = None,
        last_name: str = None,
        picture_url: str = None,
    ):
        query = (
            sa.update(cls)
            .where(cls.id == user_id)
            .values(
                first_name=first_name,
                last_name=last_name,
                picture_url=picture_url,
            )
        )
        await db_session.get().execute(query)

    @classmethod
    async def get_by_email(
        cls, email: str
    ) -> Self | None:  # TODO: Write function get for BaseModel with 404 error
        query = sa.select(User).where(User.email == email)
        result = (await db_session.get().execute(query)).scalars().first()
        return result

    @classmethod
    async def get_by_id(cls, id):
        query = sa.select(User).where(User.id == id)
        result = (await db_session.get().execute(query)).scalars().first()
        return result
