from typing import Annotated

from app.database.redis import add_jti_to_blacklist
from ..dependencies import UserServiceDep, return_the_access_token
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.models import User
from app.api.schemas.user import CreateUser, DeleteUser, UpdateUser
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_user(nickname: str, service: UserServiceDep) -> User:
    user = await service.get(nickname)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found with the nickname provided.")
    return user

@router.post("/signup")
async def create_user(user: CreateUser, service: UserServiceDep) -> User:
    return await service.add(user)

@router.patch("/")
async def update_user(id: UUID, user: UpdateUser, service: UserServiceDep) -> User:
    updated_user = await service.update(id, user)
    return updated_user

@router.delete("/")
async def delete_user(user: DeleteUser, service: UserServiceDep):
    return await service.delete(user)
    
@router.post("/login")
async def login_user(request_form: Annotated[OAuth2PasswordRequestForm,
                                             Depends()], service: UserServiceDep):
    
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }

@router.get("/logout")
async def logout_user(token_data: Annotated[dict, Depends(return_the_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {
        "detail": "Successfully Logged Out."
    }