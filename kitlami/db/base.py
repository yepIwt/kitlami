import punq
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from kitlami.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
test_engine = create_async_engine(settings.TEST_DATABASE_URL, echo=True, future=True)

Base = declarative_base()

session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
test_session_maker = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


class SessionMaker:
    def __new__(cls):
        return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class TestSessionMaker:
    def __new__(cls):
        return sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


container = punq.Container()
container.register(sessionmaker, SessionMaker)
