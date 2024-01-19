from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

DATABASE_URL = 'postgresql+asyncpg://postgres:033150RRSQL@localhost:5432/movie'
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_async_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

