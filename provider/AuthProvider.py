import datetime
import jwt
import os

from fastapi import Request, HTTPException


class AuthProvider:
    async def __call__(self, req: Request):
        authorization: str = req.headers.get('access-token')

        if not authorization:
            raise HTTPException(status_code=401, detail='Access Token Not Found')

        data = jwt.decode(authorization, os.environ['JWT_SECRET'], os.environ['JWT_ALGO'])

        if data.get('exp') < datetime.datetime.now():
            raise HTTPException(status_code=403, detail='Login Token Expired')

        self.level = data.get('level')
        self.userId = data.get('id')
        self.is_deleted = data.get('is_deleted')


    async def check_authority(self, level: int):
        if self.level < level or self.is_deleted:
            raise HTTPException(status_code=403, detail='권한이 부족합니다.')