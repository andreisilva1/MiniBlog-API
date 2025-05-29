from datetime import datetime
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.publication import CreatePublication
from app.database.models import Publication, User

class PublicationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add(self, create_publication: CreatePublication, current_user: User) -> Publication:
        publication = Publication(**create_publication.model_dump(), creator_id=current_user.id, datetime=datetime.now(), creator=current_user)
        self.session.add(publication)
        await self.session.commit()
        await self.session.refresh(publication)
        return publication
    
    async def get_my_publications(self, current_user: User):
        query = await self.session.execute(select(Publication).where(Publication.creator_id == current_user.id))
        publications = query.scalars().all()
        return publications
    
    async def get_latest_publications(self):
        latest_publications = await self.session.execute(select(Publication).order_by(desc(Publication.datetime)).limit(1))
        return latest_publications.scalars().all()
        
        
