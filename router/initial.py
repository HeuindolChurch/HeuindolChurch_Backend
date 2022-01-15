from fastapi import APIRouter, Depends, HTTPException
from provider import AuthProvider
from sqlalchemy.orm import Session
import jwt
from os import environ

from db import AccountMonth, Token, get_db
import body

router = APIRouter()


@router.post('/')
async def initialize_account(req: body.AccountMonth, db: Session = Depends(get_db),
                             auth_provider: AuthProvider = Depends(AuthProvider())):
    await auth_provider.check_authority(2)

    req.date = req.date.replace(day=1)

    db.add(AccountMonth(**req.dict()))
    db.commit()

    return req
