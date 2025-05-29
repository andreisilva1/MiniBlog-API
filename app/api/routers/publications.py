from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
import humanize

from app.api.dependencies import PublicationServiceDep, SessionDep, UserDep
from app.api.schemas.publication import CreatePublication, ReadPublication
from app.database.models import Publication, User
from app.database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.publications import PublicationService


router = APIRouter(prefix="/publications", tags=["Publications"])

@router.get("/", response_model=List[ReadPublication])
async def get_latest_publications(service: PublicationServiceDep, session: SessionDep):
    result = await service.get_latest_publications()
    return await convert_publication_to_readable_publication(result, session)


@router.get("/me", response_model=List[ReadPublication])
async def get_current_user_publications(service: PublicationServiceDep, current_user: UserDep, session: SessionDep):
    publications_by_current_user = await service.get_my_publications(current_user)
    if not publications_by_current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You don't have any posts yet. Why not try?")
    return await convert_publication_to_readable_publication(publications_by_current_user, session)


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

async def convert_publication_to_readable_publication(publications: List[Publication], session: SessionDep):
    result = []
    for publication in publications:
        creator = await session.get(entity=User, ident=publication.creator_id)
        result.append(ReadPublication(**publication.model_dump(exclude=["datetime", "creator"]), creator_name=creator.nickname, datetime=humanize.naturaltime(datetime.now() - publication.datetime)))
        
    return result