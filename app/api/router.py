from fastapi import APIRouter
from .routers import user

master_router = APIRouter()

master_router.include_router(user.router)
