import uuid
from typing import Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from kitlami.db.base import Base
from kitlami.db.connection import db_session
from kitlami.exceptions import ObjectNotFoundError


class BaseModel(Base):
    __abstract__ = True

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    async def get(self, attribute: sa.Column, value: Any):  # TODO:
        query = sa.select(self).where(attribute == value)
        try:
            result = (await db_session.get().execute(query)).scalar_one()
            return result
        except Exception as e:
            raise ObjectNotFoundError from e

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BaseDatetimeModel(BaseModel):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, onupdate=sa.func.now())
    deleted_at = sa.Column(sa.DateTime, nullable=True)
