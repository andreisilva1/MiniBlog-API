from fastapi import APIRouter

router = APIRouter(prefix="/block", tags=["Block"])

@router.post("/tags")
async def block_tags():
    pass

@router.post("/users")
async def block_users_by_nickname():
    pass