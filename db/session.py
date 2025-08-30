from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import scoped_session, sessionmaker

from api.core.settings import Settings
from db.utils.url import PsqlUrl, postgres_url

settings = Settings()


class EngineCreator:
    as_sync = None
    as_async = None

    def __init__(self, uri: PsqlUrl):
        self.sync_ = create_engine(
            uri.sync_uri, pool_pre_ping=True, echo=False
        )
        self.async_ = create_async_engine(
            uri.async_uri, pool_pre_ping=True, echo=False
        )


class SessionCreator:
    sync_ = None
    async_ = None

    def __init__(self, engine: EngineCreator):
        self.sync_ = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine.sync_)
        )
        self.async_ = async_scoped_session(
            async_sessionmaker(
                bind=engine.async_, autoflush=False, class_=AsyncSession
            ),
            scopefunc=current_task,
        )


# Create Sync and Async Engines
engine = EngineCreator(postgres_url)

# Create Session
Session: SessionCreator = SessionCreator(engine)


def get_session() -> Session:
    """Return DB session and close after using"""
    return Session
