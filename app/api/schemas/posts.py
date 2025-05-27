from pydantic import BaseModel, Field

from app.database.models import Tags


class BasePost(BaseModel):
    tag: Tags | None = Field(default=Tags.others)
    title: str
    description: str

class CreatePost(BasePost):
    pass

class ReadPost(BasePost):
    id: int
    creator_name: str
    views: int
    likes: int
    dislikes: int
    datetime: str
    
class UpdatePost(BasePost):
    pass