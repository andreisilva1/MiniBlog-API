from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from .config import DatabaseSettings as settings

engine = create_async_engine(url=settings().db_url)

async def create_db_tables():
    with engine.begin() as connection:
        from .models import Users, Post # noqa
        await connection.run_sync(SQLModel.metadata.create_all)
        
async def get_session():
    async_session = sessionmaker(bind=engine,
                                 class_=AsyncSession,
                                 expire_on_commit=False)
    async with async_session() as session:
        yield session