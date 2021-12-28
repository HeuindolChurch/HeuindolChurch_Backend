import bcrypt
from fastapi import APIRouter, Depends, HTTPException
import datetime
from sqlalchemy.orm import Session
from bcrypt import hashpw

from db import User, get_db
from provider.AuthProvider import AuthProvider
import body

router = APIRouter(
    prefix='/user'
)


@router.post('/')
async def create_user(req_user: body.User, db: Session = Depends(get_db)):
    user = req_user.dict()

    user['password'] = hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
    user['created_at'] = datetime.datetime.now()
    user['level'] = 0
    user['isDeleted'] = False

    db.add(User(**user))
    db.commit()

    return user


@router.get('/')
async def get_user(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.put('/{user_id}')
async def edit_user(req: body.User, user_id: int, db: Session = Depends(get_db),
                    auth_provider: AuthProvider = Depends(AuthProvider())):
    await auth_provider.check_authority(1)

    account = db.query(User).filter_by(id=user_id)
    new_account = req.dict()
    new_account['id'] = user_id

    request = {k: v for k, v in new_account.items()}

    for key, value in request.items():
        setattr(account, key, value)

    db.commit()


@router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db),
                      auth_provider: AuthProvider = Depends(AuthProvider())):
    await auth_provider.check_authority(3)
    user = db.query(User).filter_by(id=user_id).first()

    if user.isDeleted is True:
        raise HTTPException(status_code=403, detail='이미 삭제된 사용자 입니다.')

    user.isDeleted = True
    db.commit()

    return user
