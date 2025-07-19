from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    avatar: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: UUID4

class PostBase(BaseModel):
    title: str
    text: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

class CommentBase(BaseModel):
    title: str
    text: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: UUID4
    post_id: UUID4
    user_id: UUID4
    created_at: datetime 