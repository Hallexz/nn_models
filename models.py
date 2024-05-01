from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    password: str
    created_at: Optional[datetime] = None

class Post(BaseModel):
    id: Optional[str] = None
    user_id: str
    text: str
    media: List[str] = []
    likes: List[str] = []
    comments: List[dict] = []
    reposts: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Comment(BaseModel):
    user_id: str
    text: str
    created_at: Optional[datetime] = None