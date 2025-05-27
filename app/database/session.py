from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from .config import DatabaseSettings as settings
print(settings().db_url)
engine = create_async_engine(settings().db_url, echo=True)

async def create_db_tables():
    async with engine.begin() as connection:
        from .models import User, Post
        print("Criando tabelas no banco...")
        await connection.run_sync(SQLModel.metadata.create_all)
        print("Tabelas criadas.")


async_session = sessionmaker(bind=engine,
                                class_=AsyncSession,
                                expire_on_commit=False)      
async def get_session():
    async with async_session() as session:
        yield session