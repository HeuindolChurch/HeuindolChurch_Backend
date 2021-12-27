import bcrypt
from fastapi import APIRouter, Depends, HTTPException
import datetime
from sqlalchemy.orm import Session
from bcrypt import hashpw

from db import User, get_db
import body

router = APIRouter(
    prefix='/auth'
)


@router.post('/')
async def create_user(req_user: body.User, db: Session = Depends(get_db)):
    user = req_user.dict()

    user['password'] = hashpw(user['password'], bcrypt.gensalt())
    user['created_at'] = datetime.datetime.now()
    user['isDeleted'] = False

    db.add(User(**user))
    db.commit()

    return user


@router.get('/')
async def get_user(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()

    if user.isDeleted is True:
        raise HTTPException(status_code=403, detail='이미 삭제된 사용자 입니다.')

    user.isDeleted = True
    db.commit()

    return user
