from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    email: str
    password: str
    level: Optional[int]
    name: str
    isDeleted: Optional[bool]
    created_at: Optional[datetime]


class UserLogin(BaseModel):
    email: str
    password: str
