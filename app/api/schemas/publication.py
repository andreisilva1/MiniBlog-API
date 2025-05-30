from enum import Enum
from pydantic import BaseModel, Field, field_serializer
from app.database.models import Tags


class BasePublication(BaseModel):
    title: str
    description: str


class CreatePublication(BasePublication):
    tag: Tags | None = Field(default=Tags.others)
    pass


class ReadPublication(BasePublication):
    id: int
    creator_name: str
    views: int
    likes: int
    dislikes: int
    published_at: str
    last_update_at: str

    @field_serializer("description")
    def serialize_description(self, value, _info):
        return (
            value[:50] + "...Access the post to read more."
            if len(value) > 50
            else value
        )


class UpdatePublication(BaseModel):
    title: str
    description: str


class DateSearch(str, Enum):
    last = "last"
    up = "up"
