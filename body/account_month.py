from pydantic import BaseModel
from typing import Optional
from datetime import date


class AccountMonth(BaseModel):
    balance: Optional[int]
    date: date
