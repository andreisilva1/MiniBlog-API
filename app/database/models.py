from enum import Enum
from typing import List
from uuid import UUID, uuid4
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects import postgresql
from datetime import datetime


class Tags(str, Enum):
    others = "Others"
    games = "Games"
    health = "Health"
    technology = "Technology"
    programming = "Programming"
    finances = "Finances"
    cience = "Cience"
    arts = "Arts"
    Sports = "Sports"
    news = "News"
    enternainment = "Enternainment"
    culture = "Culture"
    politics = "Politics"
    at_home = "At Home"
    free_time = "Free Time"


class Publication(SQLModel, table=True):
    __tablename__ = "publications"
    id: int | None = Field(default=None, primary_key=True)
    creator_id: UUID = Field(foreign_key="user.id")
    creator: "User" = Relationship(
        back_populates="publications", sa_relationship_kwargs={"lazy": "selectin"}
    )
    tag: Tags | None = Field(default=Tags.others)
    title: str = Field(max_length=100)
    description: str = Field(max_length=2000)
    views: int = Field(default=0)
    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
    published_at: datetime
    last_update_at: datetime | None = Field(default=None)


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True, index=True)
    )

    name: str
    nickname: str = Field(index=True, unique=True)
    password_hashed: str
    publications: List["Publication"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
    created_at: datetime
