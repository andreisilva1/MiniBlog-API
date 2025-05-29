from pydantic import BaseModel, Field, field_serializer
from app.database.models import Tags

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
    
    @field_serializer("description")
    def serialize_description(self, value, _info):
            return value[:50] + "...Access the post to read more." if len(value) > 50 else value

  
class UpdatePublication(BasePublication):
    pass

class PossibleCategoriesSearch(BaseModel):
    id: int
    creator_name: str
    tag: str
    word_in_title: str
    word_in_description: str
    days_before: int
    more_than_x_views: int
    less_than_x_views: int
    more_than_x_likes: int
    less_than_x_likes: int
    more_than_x_dislikes: int
    less_than_x_dislikes: int
    
    
    