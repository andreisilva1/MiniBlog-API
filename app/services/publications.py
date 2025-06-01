from datetime import datetime, timedelta
from fastapi import HTTPException, status
import humanize
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.publication import (
    CreatePublication,
    DateSearch,
    ReadPublication,
    UpdatePublication,
)
from app.database.models import (
    DislikedPublicationAndUsers,
    LikedPublicationAndUsers,
    Publication,
    Tags,
    User,
)


class PublicationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int):
        publication = await self.session.get(Publication, id)
        return publication

    async def add(
        self, create_publication: CreatePublication, current_user: User
    ) -> Publication:
        publication = Publication(
            **create_publication.model_dump(),
            creator_id=current_user.id,
            published_at=datetime.now(),
            creator=current_user,
        )
        self.session.add(publication)
        await self.session.commit()
        await self.session.refresh(publication)
        return publication

    async def get_my_publications(self, current_user: User):
        query = await self.session.execute(
            select(Publication).where(Publication.creator_id == current_user.id)
        )
        publications = query.scalars().all()
        return publications

    async def get_latest_publications(self):
        latest_publications = await self.session.execute(
            select(Publication).order_by(desc(Publication.published_at)).limit(1)
        )
        return latest_publications.scalars().all()

    async def update(
        self, id: int, current_user: User, publication_update: UpdatePublication
    ):
        publication = await self.get(id)

        if not publication:
            publication_id_not_found()

        if current_user.id != publication.creator_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions.",
            )

        publication_update = {**publication_update.model_dump()}
        for key, value in publication_update.items():
            setattr(publication, key, value)

        publication.last_update_at = datetime.now()
        print(publication)
        self.session.add(publication)
        await self.session.commit()
        await self.session.refresh(publication)
        return await self.get(publication.id)

    async def delete(self, id: int, current_user: User):
        publication = await self.get(id)
        if not publication or not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A error occurred. Verify if you are authenticated and provided a valid publication id.",
            )
        if publication.creator_id == current_user.id:
            await self.session.delete(await self.get(publication.id))
            await self.session.commit()
            return {
                "detail": f"The publication with the id #{publication.id} has been deleted."
            }

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot delete a post that hasn't been created by you.",
        )

    async def get_by_id(self, id: int):
        publication = await self.session.get(Publication, id)
        if not publication:
            publication_id_not_found()
        creator = await self.session.get(entity=User, ident=publication.creator_id)
        return ReadPublication(
            **publication.model_dump(
                exclude=["published_at", "creator", "last_update_at"]
            ),
            creator_name=creator.nickname,
            published_at=humanize.naturaltime(
                datetime.now() - publication.published_at
            ),
            last_update_at=humanize.naturaltime(publication.last_update_at),
        )

    async def get_by_tag(self, tag: Tags):
        query = await self.session.execute(
            select(Publication).where(Publication.tag == tag)
        )
        publications = query.scalars().all()
        if not publications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No publication with that tag has been posted yet. Maybe you can be the first? :)",
            )
        return publications

    async def get_by_days(self, days: int, date_of_post: DateSearch):
        if date_of_post not in DateSearch:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A error occurred. Try again with one of the pre-determined options.",
            )
        if date_of_post == DateSearch.last:
            query = await self.session.execute(
                select(Publication).where(
                    Publication.published_at >= datetime.now() - timedelta(days=days)
                )
            )

        elif date_of_post == DateSearch.up:
            query = await self.session.execute(
                select(Publication).where(
                    Publication.published_at <= datetime.now() - timedelta(days=days)
                )
            )

        publications = query.scalars().all()
        if not publications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No publication found during that period of time.",
            )
        return publications

    async def like(self, post_id: int, current_user: User) -> ReadPublication:
        publication = await self.get(post_id)
        if not publication:
            publication_id_not_found()

        disliked_posts = await self.get_disliked_publications(current_user)
        verification_disliked = 1
        if disliked_posts and publication in disliked_posts:
            verification_disliked = await self.dislike(
                post_id, current_user
            )  # will remove the dislike (existent link between the post and the user)

        existent_link = await self.session.execute(
            select(LikedPublicationAndUsers).where(
                LikedPublicationAndUsers.publication_id == publication.id,
                LikedPublicationAndUsers.user_id == current_user.id,
            )
        )
        existent_link = existent_link.scalar_one_or_none()
        if existent_link:
            await self.session.delete(existent_link)
            publication.likes -= 1
            await self.session.commit()
            publication_converted = await convert_publication_to_readable_publication(
            publication, self.session
        )
            return {
                "message": "You remove your like from this post.",
                "publication": publication_converted,
            }

        new_link = LikedPublicationAndUsers(
            publication_id=publication.id, user_id=current_user.id
        )
        self.session.add(new_link)
        publication.likes += 1
        await self.session.commit()
        await self.session.refresh(new_link)
        await self.session.refresh(publication)
        publication_converted = await convert_publication_to_readable_publication(
            publication, self.session
        )

        if verification_disliked != 1:
            return {
                "message": "Your dislike changed to a like! :)",
                "publication": publication_converted,
            }
        return {"message": "You liked this post!", "publication": publication_converted}

    async def get_liked_publications(self, current_user: User):
        liked_posts = await self.session.execute(
            select(LikedPublicationAndUsers).where(
                LikedPublicationAndUsers.user_id == current_user.id
            )
        )
        if not liked_posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You don't liked any publications yet.",
            )
        liked_posts = liked_posts.scalars().all()
        result = []
        for post in liked_posts:
            result.append(await self.session.get(Publication, post.publication_id))
        return result

    async def dislike(self, post_id: int, current_user: User) -> ReadPublication:
        publication = await self.get(post_id)
        if not publication:
            publication_id_not_found()
        liked_posts = await self.get_liked_publications(current_user)
        verification_liked = 1

        if liked_posts and publication in liked_posts:
            verification_liked = await self.like(
                post_id, current_user
            )  # will remove the like (existent link between the post and the user)

        existent_link = await self.session.execute(
            select(DislikedPublicationAndUsers).where(
                DislikedPublicationAndUsers.publication_id == publication.id,
                DislikedPublicationAndUsers.user_id == current_user.id,
            )
        )
        existent_link = existent_link.scalar_one_or_none()
        if existent_link:
            await self.session.delete(existent_link)
            publication.dislikes -= 1
            await self.session.commit()
            publication_converted = await convert_publication_to_readable_publication(publication, self.session)

            return {
                "message": "You remove your dislike from this post.",
                "publication": publication_converted,
            }

        new_link = DislikedPublicationAndUsers(
            publication_id=publication.id, user_id=current_user.id
        )
        self.session.add(new_link)
        publication.dislikes += 1
        await self.session.commit()
        await self.session.refresh(new_link)
        publication_converted = await convert_publication_to_readable_publication(
            publication, self.session
        )

        if verification_liked != 1:
            return {
                "message": "Your like changed to a dislike! :(",
                "publication": publication_converted,
            }
        return {
            "message": "You disliked this post!",
            "publication": publication_converted,
        }

    async def get_disliked_publications(self, current_user: User):
        disliked_posts = await self.session.execute(
            select(DislikedPublicationAndUsers).where(
                DislikedPublicationAndUsers.user_id == current_user.id
            )
        )
        if not disliked_posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You don't disliked any publications yet.",
            )
        disliked_posts = disliked_posts.scalars().all()
        result = []
        for post in disliked_posts:
            result.append(await self.session.get(Publication, post.publication_id))
        return result


def publication_id_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No publication with that id has been found.",
    )


async def convert_publication_to_readable_publication(
    publication: Publication, session: AsyncSession
) -> ReadPublication:
    creator = await session.get(entity=User, ident=publication.creator_id)
    publication = ReadPublication(
        **publication.model_dump(exclude=["published_at", "creator", "last_update_at"]),
        creator_name=creator.nickname,
        published_at=humanize.naturaltime(datetime.now() - publication.published_at),
        last_update_at=humanize.naturaltime(publication.last_update_at),
    )

    return publication
