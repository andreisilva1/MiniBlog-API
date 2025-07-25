from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
import humanize

from app.api.dependencies import PublicationServiceDep, SessionDep, UserDep
from app.api.schemas.publication import (
    BasePublication,
    CreatePublication,
    DateSearch,
    ReadPublication,
    UpdatePublication,
)
from app.database.models import Publication, Tags, User
from app.database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.publications import PublicationService


router = APIRouter(prefix="/publications", tags=["Publications"])


@router.get("/latest", response_model=List[ReadPublication])
async def get_latest_publications(service: PublicationServiceDep, session: SessionDep):
    result = await service.get_latest_publications()
    return await convert_publication_to_readable_publication(result, session)


@router.get("/me", response_model=List[ReadPublication])
async def get_current_user_publications(
    service: PublicationServiceDep, current_user: UserDep, session: SessionDep
):
    publications_by_current_user = await service.get_my_publications(current_user)
    if not publications_by_current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have any posts yet. Why not try?",
        )
    return await convert_publication_to_readable_publication(
        publications_by_current_user, session
    )


@router.get("/id", response_model=ReadPublication)
async def get_publications_by_id(
    id: int, service: PublicationServiceDep, session: SessionDep
):
    return await service.get_by_id(id)


@router.get("/tag")
async def get_publications_by_tag(
    tag: Tags, service: PublicationServiceDep, session: SessionDep
):
    return await convert_publication_to_readable_publication(
        await service.get_by_tag(tag), session
    )


@router.get("/days")
async def get_publications_by_days_of_posted(
    service: PublicationServiceDep,
    days: int,
    session: SessionDep,
    date_of_post: DateSearch = Query(
        ...,
        description='Use "last" to post in the last x days and "up" to posts up to x days ago',
    ),
):
    publications_by_date = await service.get_by_days(days, date_of_post)
    return await convert_publication_to_readable_publication(
        publications_by_date, session
    )


@router.get("/like-post")
async def like_publication_by_id(
    id: int, service: PublicationServiceDep, current_user: UserDep
):
    return await service.like(id, current_user)


@router.get("/liked-posts")
async def get_liked_posts(
    current_user: UserDep, service: PublicationServiceDep, session: SessionDep
):
    liked_posts = await service.get_liked_publications(current_user)
    return await convert_publication_to_readable_publication(liked_posts, session)


@router.get("/dislike-post")
async def dislike_publication_by_id(
    id: int, current_user: UserDep, service: PublicationServiceDep
):
    return await service.dislike(id, current_user)


@router.get("/disliked-posts")
async def get_disliked_posts(service: PublicationServiceDep, current_user: UserDep, session: SessionDep):
    disliked_posts = service.get_disliked_posts(current_user)
    return await convert_publication_to_readable_publication(disliked_posts, session)



@router.post("/")
async def create_publication(
    user: UserDep,
    publication: BasePublication,
    session: Annotated[AsyncSession, Depends(get_session)],
    tag: Tags,
):
    publication = CreatePublication(**publication.model_dump(), tag=tag)
    return await PublicationService(session).add(publication, user)


@router.patch("/")
async def update_publication(
    current_user: UserDep,
    id: int,
    update_publication: UpdatePublication,
    service: PublicationServiceDep,
    session: SessionDep,
):
    publication = await service.update(id, current_user, update_publication)
    creator = await session.get(entity=User, ident=publication.creator_id)
    return ReadPublication(
        **publication.model_dump(exclude=["published_at", "creator", "last_update_at"]),
        creator_name=creator.nickname,
        published_at=humanize.naturaltime(datetime.now() - publication.published_at),
        last_update_at=humanize.naturaltime(publication.last_update_at)
    )


@router.delete("/")
async def delete_publication(
    id: int, current_user: UserDep, service: PublicationServiceDep
):
    return await service.delete(id, current_user)


async def convert_publication_to_readable_publication(
    publications: List[Publication], session: SessionDep
) -> List[ReadPublication]:
    result = []
    for publication in publications:
        creator = await session.get(entity=User, ident=publication.creator_id)
        result.append(
            ReadPublication(
                **publication.model_dump(
                    exclude=["published_at", "creator", "last_update_at"]
                ),
                creator_name=creator.nickname,
                published_at=humanize.naturaltime(
                    datetime.now() - publication.published_at
                ),
                last_update_at=humanize.naturaltime(publication.last_update_at)
            )
        )

    return result
