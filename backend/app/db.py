from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.models import Base


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.execute(text("SELECT pg_advisory_xact_lock(0)"))
        await conn.run_sync(Base.metadata.create_all)
