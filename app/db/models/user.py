from datetime import datetime
from typing import Optional
from sqlmodel import Field
from sqlmodel.main import SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True,index=True)
    hashed_password :str

    # Preferences
    preferred_language: Optional[str] = "en"
    verse_theme: Optional[str] = "gita"

    # Daily features
    last_checked: Optional[datetime]=None
    streak: int = 1

    # Timestamps
    created_at: datetime=Field(default_factory=datetime.utcnow)
