from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.publication import CreatePublication, UpdatePublication
from app.database.models import Publication, User


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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No post found with the id provided.",
            )

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
