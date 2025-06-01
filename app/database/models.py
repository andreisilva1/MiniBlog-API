from enum import Enum
from typing import List, Optional
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


class Blocked_Tags(SQLModel, table=True):
    user_id: UUID = Field(default=None, foreign_key="user.id", primary_key=True)
    tag: Tags = Field(sa_column_kwargs={"nullable": False}, primary_key=True)
    users: Optional["User"] = Relationship(back_populates="blocked_tags")


class LikedPublicationAndUsers(SQLModel, table=True):
    publication_id: int = Field(foreign_key="publications.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)


class DislikedPublicationAndUsers(SQLModel, table=True):
    publication_id: int = Field(foreign_key="publications.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)


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
    users_that_liked: List["User"] = Relationship(
        back_populates="liked_publications", link_model=LikedPublicationAndUsers
    )
    users_that_disliked: List["User"] = Relationship(
        back_populates="disliked_publications", link_model=DislikedPublicationAndUsers
    )


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

    blocked_tags: List[Blocked_Tags] = Relationship(back_populates="users")

    liked_publications: List["Publication"] = Relationship(
        back_populates="users_that_liked", link_model=LikedPublicationAndUsers
    )

    disliked_publications: List["Publication"] = Relationship(
        back_populates="users_that_disliked", link_model=DislikedPublicationAndUsers
    )
