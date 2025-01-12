import asyncio
from contextvars import ContextVar, Token
from uuid import uuid4
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from wastory.database.settings import DB_SETTINGS


class DatabaseManager:
    def __init__(self):
        # TODO pool 이 뭘까요?
        # pool_recycle 은 뭐고 왜 28000으로 설정해두었을까요?
        self.engine = create_async_engine(
            DB_SETTINGS.url,
            poolclass=AsyncAdaptedQueuePool,
            pool_recycle=28000,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )


session_context_var: ContextVar[tuple[str | None, str | None]] = ContextVar(
    "session_context", default=(None, None)
)


def reset_session(token: Token) -> None:
    """세션 컨텍스트 초기화"""
    session_context_var.reset(token)


def start_default_session() -> Token:
    """DefaultSessionMiddleware 에서 단 한 번만 사용"""
    return session_context_var.set((uuid4().hex, None))


def start_new_session_if_not_exists() -> Token | None:
    """
    트랜잭션 시작 시 새로운 세션 컨텍스트 생성
    중첩된 트랜잭션에서는 최상위 트랜잭션에서만 새로운 세션을 생성
    """
    _, session_task = session_context_var.get()
    current_task_name = asyncio.current_task().get_name()  # type: ignore
    # 현재 태스크에서 이미 세션을 생성된 적 있는 경우 무시
    if session_task != current_task_name:
        return session_context_var.set((uuid4().hex, current_task_name))


def get_session_id() -> str | None:
    return session_context_var.get()[0]


SESSION = async_scoped_session(
    session_factory=DatabaseManager().session_factory, scopefunc=get_session_id
)