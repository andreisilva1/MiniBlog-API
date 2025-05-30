from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from app.database.models import Blocked_Tags, Tags, User

class BlockService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def block_tag(self, tag_name: Tags, current_user: User):
        if tag_name not in Tags:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tag has been founded with this name, try select one that exists :)")
        result = await self.session.execute(select(User).options(selectinload(User.blocked_tags)).where(User.nickname == current_user.nickname))
        user = result.scalars().first()
        if tag_name in [blocked.tag for blocked in user.blocked_tags]:
            result = await self.session.execute(select(Blocked_Tags).where(Blocked_Tags.user_id == current_user.id, Blocked_Tags.tag == tag_name))
            connection = result.scalar_one_or_none()
            if connection:
                await self.session.delete(connection)
                await self.session.commit()
                return {"detail": f"The {tag_name} is now unblocked and you will see publications with this tag now."}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao desbloquear tag.")

        new_link = Blocked_Tags(user_id=current_user.id, tag=tag_name)
        self.session.add(new_link)
        await self.session.commit()
        return {"detail": f"The {tag_name} is now blocked. If you want to unblock, just select the tag and send the request again! :)"}