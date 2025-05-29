from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel

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
    
