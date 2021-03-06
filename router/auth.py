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

router = APIRouter()


@router.post('/')
async def get_token(req_user: body.UserLogin, db: Session = Depends(get_db)):
    user = req_user.dict()
    check = db.query(User).filter_by(email=user['email']).first()

    if check is None:
        raise HTTPException(status_code=403, detail='사용자가 존재하지 않습니다.')
    if not checkpw(user['password'].encode('utf-8'), check.password.encode('utf-8')):
        raise HTTPException(status_code=403, detail='비밀번호가 틀렸습니다.')

    user_token = db.query(Token).filter_by(userId=check.id).first()

    access_token = jwt.encode({'user_id': check.as_dict()['id'],
                               'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)}, environ['JWT_SECRET'],
                              algorithm=environ['JWT_ALGO'])

    refresh_token = jwt.encode({'user_id': check.as_dict()['id'],
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)}, environ['JWT_SECRET'],
                               algorithm=environ['JWT_ALGO'])

    if user_token is None:
        db.add(Token(**{'accessToken': access_token, 'refreshToken': refresh_token, 'userId': check.id}))
    else:
        setattr(user_token, 'accessToken', access_token)
        setattr(user_token, 'refreshToken', refresh_token)

    db.commit()

    info = check.as_dict()

    return {'access-token': access_token, 'refresh-token': refresh_token, 'name': info['name'], 'level': info['level']}
