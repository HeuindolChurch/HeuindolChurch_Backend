from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    accessToken: str
    refreshToken: str
