from typing import Annotated
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.core.security import oauth2_scheme
from app.database.models import User
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.blocks import BlockService
from app.services.publications import PublicationService
from app.services.user import UserService
from app.utils import decode_access_token


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def create_user_service(session: SessionDep):
    return UserService(session)


def create_block_service(session: SessionDep):
    return BlockService(session)


def create_publication_service(session: SessionDep):
    return PublicationService(session)


async def return_the_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    data = decode_access_token(token)
    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
        )
    return data


async def get_current_user(
    data: Annotated[dict, Depends(return_the_access_token)], session: SessionDep
):
    return await session.get(User, UUID(data["user"]["id"]))


PublicationServiceDep = Annotated[
    PublicationService, Depends(create_publication_service)
]
UserServiceDep = Annotated[UserService, Depends(create_user_service)]
UserDep = Annotated[User, Depends(get_current_user)]
BlockServiceDep = Annotated[BlockService, Depends(create_block_service)]
