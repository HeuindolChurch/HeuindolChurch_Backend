from fastapi import APIRouter, Depends, HTTPException
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
from bcrypt import checkpw
import jwt
from os import environ

from db import User, Token, get_db
import body

router = APIRouter(
    prefix='/auth'
)


@router.get('/')
async def get_token(req_user: body.User, db: Session = Depends(get_db)):
    user = req_user.dict()
    check = db.query(User).filter_by(email=req_user.email).one()

    if check is None:
        raise HTTPException(status_code=403, detail='사용자가 존재하지 않습니다.')
    if not checkpw(user['password'].encode('utf-8'), check.password):
        raise HTTPException(status_code=403, detail='비밀번호가 틀렸습니다.')

    access_token = jwt.encode({'user_id': check.as_dict()['id'], 'level': check.as_dict()['level'],
                               'is_deleted': check.as_dict()['isDeleted'],
                               'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)}, environ['JWT_SECRET'],
                              algorithm=environ['JWT_ALGO'])

    refresh_token = jwt.encode({'user_id': check.as_dict()['id'], 'level': check.as_dict()['level'],
                                'is_deleted': check.as_dict()['isDeleted'],
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)}, environ['JWT_SECRET'],
                               algorithm=environ['JWT_ALGO'])

    db.add(Token({'accessToken': access_token, 'refreshToken': refresh_token}))
    db.commit()

    return {access_token, refresh_token}
