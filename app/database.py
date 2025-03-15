###################################################
#
#     Модуль FastAPI определяющий базу данных
#
###################################################

from typing import AsyncGenerator

from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from app.conf import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    REDIS_HOST,
    REDIS_PORT,
)

DATABASE_URL = "sqlite:///test.db"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# SYNC
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# ASYNC
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

celery = Celery(
    __name__,
    broker=REDIS_URL,
    backend=REDIS_URL,
    broker_connection_retry_on_startup=True
)


class Base(DeclarativeBase):
    pass


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
