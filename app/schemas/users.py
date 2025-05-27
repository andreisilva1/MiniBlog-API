from pydantic import BaseModel

from app.database.models import Post


class BaseUser(BaseModel):
    nickname: str
    
class CreateUser(BaseUser):
    name: str
    password: str
    
class ReadUser(BaseUser):
    posts: list[Post]
    
class UpdateUser(BaseUser):
    name: str
    password: str
    
