import datetime
import jwt
import os

from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session

from db import get_db, User


class AuthProvider:
    async def __call__(self, req: Request, db: Session = Depends(get_db)):
        authorization: str = req.headers.get('access-token')

        if not authorization:
            raise HTTPException(status_code=401, detail='Access Token Not Found')

        data = jwt.decode(authorization, os.environ['JWT_SECRET'], os.environ['JWT_ALGO'])

        if data.get('exp') < datetime.datetime.utcnow().timestamp():
            raise HTTPException(status_code=403, detail='Login Token Expired')

        user = db.query(User).filter_by(id=data.get('user_id')).first()

        self.level = user.level
        self.userId = user.id
        self.is_deleted = user.isDeleted

        return self

    async def check_authority(self, level: int):
        if self.level < level or self.is_deleted:
            raise HTTPException(status_code=403, detail='권한이 부족합니다.')
