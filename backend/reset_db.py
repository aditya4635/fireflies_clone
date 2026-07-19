import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.database import Base
import app.models

engine = create_async_engine('sqlite+aiosqlite:///./meetings.db')

async def reset():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(reset())
