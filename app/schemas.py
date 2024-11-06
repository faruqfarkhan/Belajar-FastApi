from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    # title: str
    # content: str\
    owner_id: Optional[int] = Field(None, exclude=True)

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime



class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # type: ignore

class Post(PostBase):
    content: str
    title: str
    created_at: datetime
    id: int
    published: bool
    owner_id: int
    owner: UserOut


    class Config:
        orm_mode = True

class PostOut(PostBase):
    post: Post
    votes: int
    
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int

class TokenData(BaseModel):
    id: Optional[int] = None





