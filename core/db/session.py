from contextvars import ContextVar, Token
from typing import Any, Union

from sqlalchemy import DateTime, Column, func, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session, async_sessionmaker,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.expression import Update, Delete, Insert
from core.config import SETTINGS


session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


class CreateEngines:
    def __init__(self, reader=False) -> None:
        self.reader = reader

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        engines = {create_async_engine(SETTINGS.DB_URL, pool_recycle=SETTINGS.DB_POOL_RECYCLE), }
        return engines


engines = CreateEngines(reader=False)()

engines = {
    "writer": create_async_engine(SETTINGS.DB_URL,
                                  pool_recycle=SETTINGS.DB_POOL_RECYCLE,
                                  connect_args={'server_settings': {'jit': 'off'}}),
    "reader": create_async_engine(SETTINGS.DB_URL,
                                  pool_recycle=SETTINGS.DB_POOL_RECYCLE,
                                  connect_args={'server_settings': {'jit': 'off'}}),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine
        else:
            return engines["reader"].sync_engine


class SingleRoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        return engines["writer"].sync_engine


async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=SingleRoutingSession,
    autoflush=False,
    expire_on_commit=False,
)

session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)


class SyncSessionContext:
    _engine = None
    _session_factory = None

    def init_sync_db(self):
        if not SyncSessionContext._engine:
            SyncSessionContext._engine = create_engine(SETTINGS.DB_URL)
        if not SyncSessionContext._session_factory:
            SyncSessionContext._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
                bind=SyncSessionContext._engine,
            )

    def __init__(self):
        self.init_sync_db()

    def __enter__(self):
        self.session = SyncSessionContext._session_factory()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()


class DateTimeBase:
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())


Base = declarative_base()
