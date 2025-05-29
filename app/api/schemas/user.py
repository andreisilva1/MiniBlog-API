from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, field_serializer

from app.database.models import Publication


class BaseUser(BaseModel):
    name: str
    nickname: str


class CreateUser(BaseUser):
    password: str


class ReadUser(BaseUser):
    created_at: datetime
    publications: List[Publication]


class UpdateUser(BaseUser):
    name: str
    password: str


class DeleteUser(BaseUser):
    id: UUID
    password: str


class PublicUser(BaseUser):
    id: UUID
    created_at: datetime

    @field_serializer("created_at")
    def serialize_description(self, value, _info):
        return value.strftime("%d/%m/%Y")
