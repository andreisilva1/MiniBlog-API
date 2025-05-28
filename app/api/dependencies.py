from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database.session import get_session
from app.services.user import UserService


SessionDep = Annotated[AsyncSession, Depends(get_session)]

def create_user_service(session: SessionDep):
    return UserService(session)

UserServiceDep = Annotated[UserService, Depends(create_user_service)]