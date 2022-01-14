# Modules/Library Imports and initialization
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# Class to model the "Users" Attributes
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Class to model the "Users" response Attributes
class UserResponse(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr

    class Config:
        orm_mode = True


# Class to model the "Users" Login Attributes
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Class to model the "Votes" Attributes
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

    class Config:
        orm_mode = True


# Class to model the "Posts" Attributes
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Class to model the "Posts" response Attributes
class PostResponse(BaseModel):
    id: int
    owner_id: int
    created_at: datetime
    published: bool
    title: str
    content: str
    # Used to respond with the "owner" field from the "User" Class. Tied to SQL Alchemy "relationship" keyword
    owner: UserResponse

    class Config:
        orm_mode = True


# Class to model the "Posts" Response with "Votes" also added
class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


# Class to model the "Users" Token Response Attributes
class Token(BaseModel):
    access_token: str
    token_type: str


# Class to model the "Users" Token Data Attributes
class TokenData(BaseModel):
    id: Optional[str] = None
