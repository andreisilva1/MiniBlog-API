from fastapi import APIRouter
from app.api.dependencies import BlockServiceDep, UserDep
from app.database.models import Tags

router = APIRouter(prefix="/block", tags=["Block"])


@router.post("/tags", response_model=None)
async def block_tags(current_user: UserDep, tag: Tags, service: BlockServiceDep):
    return await service.block_tag(tag, current_user)


@router.post("/users")
async def block_users_by_nickname():
    pass
