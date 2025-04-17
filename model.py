import re
from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship
from typing import Optional, List
# Base class for models

class User(SQLModel, table=True):
    __table_args__=(
        UniqueConstraint("username", "email", name="unique username and email"),
    )
    id: int | None = Field(default= None, primary_key=True)
    username: str = Field(index= True, unique= True)
    email: str = Field(index= True, unique= True)
    password: str

    anime_list: List["Anime"]= Relationship(back_populates="author")

    

class Anime(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    anime_name: str
    anime_description: str
    user_id: int = Field(foreign_key='user.id')

    author: Optional['User']= Relationship(back_populates= "anime_list")