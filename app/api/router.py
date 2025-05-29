from fastapi import APIRouter
from .routers import user, publications, blocks

master_router = APIRouter()

master_router.include_router(user.router)
master_router.include_router(publications.router)
master_router.include_router(blocks.router)
