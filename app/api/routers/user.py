from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.models import User
from app.database.session import get_session
from app.api.schemas.user import CreateUser
from ...services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_user(nickname: str, session: Annotated[UserService, Depends(get_session)]) -> User:
    user = await session.get(nickname)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found with the nickname provided.")
    return user

@router.post("/")
async def create_user(user: CreateUser, session: Annotated[AsyncSession, Depends(get_session)]) -> User:
    user = await UserService(session).add(user)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The nickname given has already in use.")