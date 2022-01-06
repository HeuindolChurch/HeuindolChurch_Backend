from pydantic import BaseModel
from datetime import date


class Account(BaseModel):
    reason: str
    price: int
    note: str
    date: date
    insert: bool
