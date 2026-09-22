from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    photo_path: Optional[str] = None
    created_at: datetime


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TagResponse(BaseModel):
    id: int
    name: str


class NewsResponse(BaseModel):
    id: int
    title: str
    subtitle: Optional[str] = None
    text: str
    image_path: Optional[str] = None
    author: UserResponse
    tags: List[TagResponse]
    created_at: datetime
    comments_count: Optional[int] = None


class PaginatedNewsResponse(BaseModel):
    items: List[NewsResponse]
    page: int
    per_page: int
    total: int


class CommentCreate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: int
    text: str
    author: UserResponse
    created_at: datetime


class ValidationError(BaseModel):
    loc: List[str | int]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    detail: List[ValidationError]