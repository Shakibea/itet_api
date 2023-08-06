from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Union, Any, Optional

from fastapi import Body, FastAPI
from typing_extensions import Annotated


# Client sending to Server
# Schemas Models
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreateRequest(PostBase):
    pass


# Server responding to Client
# Response Model
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    # owner_id: int
    owner: UserResponse

    # created_at: Union[datetime, None] = Body(default=None)

    class Config:
        orm_mode = True


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str


class UserLogin(UserCreateRequest):
    pass


class UserResponseData(UserResponse):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class UserInDB(BaseModel):
    hashed_password: str
