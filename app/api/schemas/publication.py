from typing import List
import humanize
from pydantic import BaseModel, Field
from datetime import datetime
from app.database.models import Tags, Publication

class BasePublication(BaseModel):
    tag: Tags | None = Field(default=Tags.others)
    title: str
    description: str

class CreatePublication(BasePublication):
    pass

class ReadPublication(BasePublication):
    id: int
    creator_name: str
    views: int
    likes: int
    dislikes: int
    datetime: str

    
class UpdatePublication(BasePublication):
    pass