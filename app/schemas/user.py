from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.traversals import _preconfigure_traversals
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    preferred_language: Optional[str] = "en"
    verse_theme: Optional[str] = "gita"

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    preferred_language: Optional[str]
    verse_theme: Optional[str]
    streak: int
    last_checked: Optional[datetime]

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None
    preferred_language: Optional[str] = None
    verse_theme: Optional[str] = None
    dark_mode_enabled: Optional[bool] = None

    class Config:
        orm_mode = True
