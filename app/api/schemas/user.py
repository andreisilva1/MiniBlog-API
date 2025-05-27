from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.database.models import Post


class BaseUser(BaseModel):
    name: str
    nickname: str

    
class CreateUser(BaseUser):
    password: str
    
class ReadUser(BaseUser):
    created_at: datetime
    posts: List[Post] = []
    class Config:
        orm_mode = True
    
class UpdateUser(BaseUser):
    name: str
    password: str
    
