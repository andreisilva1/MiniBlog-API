from datetime import datetime
from uuid import UUID, uuid4
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.database.models import User
from app.api.schemas.user import CreateUser, DeleteUser, UpdateUser

from passlib.context import CryptContext

from app.utils import generate_access_token

password_context = CryptContext(deprecated="auto", schemes="bcrypt")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, nickname: str) -> User:
        result = await self.session.execute(
            select(User).where(User.nickname == nickname)
        )
        user = result.scalar_one_or_none()
        return user

    async def add(self, user_create: CreateUser) -> User:
        if await self.get(user_create.nickname):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The nickname given has already in use.",
            )
        new_user = User(
            **user_create.model_dump(exclude=["password"]),
            created_at=datetime.now(),
            id=uuid4(),
            password_hashed=password_context.hash(user_create.password),
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return await self.get(new_user.nickname)

    async def update(self, id: UUID, user_update: UpdateUser):
        user = await self.session.get(User, id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND(
                    "No user found with the id provided."
                )
            )
        user_update = {
            **user_update.model_dump(exclude=["password"]),
            "password_hashed": password_context.hash(user_update.password),
        }
        for key, value in user_update.items():
            setattr(user, key, value)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return await self.get(user.nickname)

    async def delete(self, delete_user: DeleteUser, current_user: User):
        if not current_user or not delete_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A error occurred. Verify if you are authenticated and provided a valid json.",
            )
        if password_context.verify(
            delete_user.password, current_user.password_hashed
        ) and (
            delete_user.model_dump(exclude=["password"])
            == current_user.model_dump(exclude=["password_hashed", "created_at"])
        ):
            await self.session.delete(await self.get(current_user.nickname))
            await self.session.commit()
            return {"detail": f"The user {current_user.nickname} has been deleted."}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You can't delete another user profile.",
        )

    async def token(self, nickname, password):
        user = await self.get(nickname)
        if not user or not password_context.verify(password, user.password_hashed):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The data provided is invalid.",
            )

        token = generate_access_token(
            {"user": {"username": user.nickname, "id": str(user.id)}}
        )

        return token
