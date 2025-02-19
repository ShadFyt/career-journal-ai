from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = AsyncEngine(create_engine(sqlite_url, echo=True, future=True))


async def create_db_and_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
