from ..dependencies import UserServiceDep
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from app.database.models import User
from app.api.schemas.user import CreateUser, DeleteUser, UpdateUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_user(nickname: str, service: UserServiceDep) -> User:
    user = await service.get(nickname)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found with the nickname provided.")
    return user

@router.post("/")
async def create_user(user: CreateUser, service: UserServiceDep) -> User:
    return await service.add(user)

@router.patch("/")
async def update_user(id: UUID, user: UpdateUser, service: UserServiceDep) -> User:
    updated_user = await service.update(id, user)
    return updated_user

@router.delete("/")
async def delete_user(user: DeleteUser, service: UserServiceDep):
    return await service.delete(user)
    
