import asyncio
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.models import Book, Author, BookCreate, AuthorCreate, New_Response, Base

DATABASE_URL = 'postgresql+asyncpg://postgres:gimeori@localhost:5432/book'
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
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# async def f_builder(session):
#     async with session.begin():
#         new_author = Author(name="Ivanov")
#         session.add(new_author)
#         await session.commit()
#
# async def execute_f_builder():
#     async with async_session() as session:
#         await f_builder(session)
