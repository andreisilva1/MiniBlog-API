from fastapi import APIRouter
from .routers import user, publications

master_router = APIRouter()

master_router.include_router(user.router)
master_router.include_router(publications.router)
