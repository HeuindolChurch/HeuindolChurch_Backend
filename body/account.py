from pydantic import BaseModel
from typing import Optional
from datetime import date


class Account(BaseModel):
    reason: str
    price: int
    balance: Optional[int]
    note: str
    date: date
