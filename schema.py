from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field
from typing import List, Optional
import re


class animeSchema(SQLModel):
    anime_name: str
    anime_description: str

class animeSchemaWithId(SQLModel):
    anime_name: str
    anime_description: str
    id: int

class userSchema(SQLModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def validate_username(cls, v):
        if len(v)<3:
            raise ValueError("Username must be at least 3 characters long")
        if len(v)>15:
            raise ValueError("Username must not be more than 15 characters long")
        if not re.match(r'^[a-z0-9_.]+$', v):
            raise ValueError("Username must be lowercase and can only contain letters, digits, underscores (_) and periods (.) without spaces")
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*()_\-+={};:,.<>?|\\/~`]', v):
            raise ValueError("Password must contain at least one special character")
        return v


class userSchema2(SQLModel):
    username: str
    email: EmailStr
    id: int

class animeSchemaShow(SQLModel):
    id: int
    anime_name: str
    anime_description: str
    author: userSchema2

class userSchemaShow(SQLModel):
    username: str
    email: EmailStr
    id: int
    anime_list: List[animeSchemaWithId]= Field(default_factory= list)


class loginSchema(SQLModel):
    username: str
    password: str
class Token(SQLModel):
    access_token: str
    token_type: str
class TokenData(SQLModel):
    username: Optional[str]= None