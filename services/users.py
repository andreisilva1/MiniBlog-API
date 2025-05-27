from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.models import Users
from app.schemas.users import CreateUser, ReadUser

class UserServices:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get(self, nickname: str) -> ReadUser:
        return await self.session.execute(select(Users).
                                          where(Users.username == nickname))
    
    async def add(self, user: CreateUser):
        if self.get(user.nickname):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="The given nickname is already in use.")
        new_user = Users(**user.model_dump(), created_at=datetime.now())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return await self.session.get(new_user)
    
    async def update(self, id: UUID, user_update: dict):
        user = self.get(Users, id)
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
        return await self.session.delete(await self.get(Users, id))