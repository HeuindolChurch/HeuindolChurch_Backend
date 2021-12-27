from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    email: str
    password: str
    level: int
    name: str
    isDeleted: bool
    date: datetime
