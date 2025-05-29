from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
import humanize

from app.api.dependencies import UserDep
from app.api.schemas.publication import CreatePublication, ReadPublication
from app.database.models import User
from app.database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.publications import PublicationService


router = APIRouter(prefix="/publications", tags=["Publications"])

@router.get("/news")
async def get_first_publications():
    pass

@router.get("/me", response_model=List[ReadPublication])
async def get_current_user_publications(session: Annotated[AsyncSession, Depends(get_session)], current_user: UserDep):
    publications_by_current_user = await PublicationService(session).get_my_publications(current_user)
    if not publications_by_current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You don't have any posts yet. Why not try?")
    result = []
    for publication in publications_by_current_user:
        creator = await session.get(User, publication.creator_id)
        result.append(ReadPublication(**publication.model_dump(exclude=["datetime", "creator"]), creator_name=creator.nickname, datetime=humanize.naturaltime(datetime.now() - publication.datetime)))
    return result



@router.get("/by-categories")
async def get_publications_by_categories():
    pass

@router.post("/like-post")
async def like_publication_by_id():
    pass

@router.post("/")
async def create_publication(user: UserDep, publication: CreatePublication, session: Annotated[AsyncSession, Depends(get_session)]):
    return await PublicationService(session).add(publication, user)

@router.patch("/")
async def update_publication():
    pass

@router.delete("/")
async def delete_publication():
    pass