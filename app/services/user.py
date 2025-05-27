from datetime import datetime
from uuid import UUID, uuid4
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.models import User
from app.api.schemas.user import CreateUser, ReadUser

from passlib.context import CryptContext

password_context = CryptContext(deprecated="auto", schemes="bcrypt")
class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get(self, nickname: str) -> User:
        result = await self.session.execute(select(User).
                                          where(User.nickname == nickname))
        user = result.scalar_one_or_none()
        return user
    
    
    async def add(self, user_create: CreateUser) -> User:
        if self.get(user_create.nickname):
            return None
        new_user = User(**user_create.model_dump(exclude=["password"]),
                                                 created_at=datetime.now(),
                                                 id=uuid4(),
                                                 password_hashed=password_context.hash(user_create.password))
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return await self.get(new_user.nickname)
    
    async def update(self, id: UUID, user_update: dict):
        user = self.get(User, id)
        if not user:
            raise HTTPException(status_code=status.
                    HTTP_404_NOT_FOUND("No user found with the id provided."))
            
        for key, value in user_update.items():
            setattr(user, key, value)
        self.session.add(user)
        self.session.commit()
        self.session.refresh()
        return await self.get(user.nickname)
    
    async def delete(self, id: UUID):
        return await self.session.delete(await self.get(User, id))