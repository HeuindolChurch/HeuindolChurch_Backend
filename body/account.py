from pydantic import BaseModel
from typing import Optional
from datetime import date


class Account(BaseModel):
    reason: str
    price: int
    note: Optional[str]
    date: date
