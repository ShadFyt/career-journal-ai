"""Global test fixtures for all domains."""

import pytest_asyncio

from database.session import SessionDep
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest_asyncio.fixture(name="engine")
async def engine_fixture():
    """Create a new database engine for testing."""
    engine = AsyncEngine(create_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    ))
    return engine


@pytest_asyncio.fixture(name="db_session")
async def db_session_fixture(engine) -> SessionDep:
    """Create a new database session for testing."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)