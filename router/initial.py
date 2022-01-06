from fastapi import APIRouter, Depends, HTTPException
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
from bcrypt import checkpw
import jwt
from os import environ

from db import AccountMonth, Token, get_db
import body

router = APIRouter(
    prefix='/init'
)


@router.post('/')
async def initialize_account(req: body.AccountMonth, db: Session = Depends(get_db)):
    db.add(AccountMonth(**req.dict()))
    db.commit()

    return req
