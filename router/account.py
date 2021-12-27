from fastapi import APIRouter, Depends, HTTPException, Request
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from db import Account, get_db
from provider import AuthProvider
import body

router = APIRouter(
    prefix='/account'
)


@router.get('/')
async def get_account(db: Session = Depends(get_db), date: datetime.date = datetime.date.today(),
                      auth_provider: AuthProvider = Depends(AuthProvider())):
    await auth_provider.check_authority(1)

    start_at = date.replace(day=1)
    end_at = start_at + relativedelta(months=1)

    return db.query(Account).filter(Account.date >= start_at, Account.date < end_at).order_by(Account.date).all()


@router.post('/')
async def post_account(req: body.Account, db: Session = Depends(get_db), token=Depends(AuthProvider()),
                       auth_provider: AuthProvider = Depends(AuthProvider())):
    await auth_provider.check_authority(2)

    account = req.dict()

    if token.level > 2:
        raise HTTPException(status_code=403, detail='권한이 부족합니다.')

    last_account = db.query(Account).filter(Account.date > req.date).order_by(desc(Account.id)).first()

    if last_account is not None:
        if req.date < last_account.as_dict()['date']:
            after_accounts = db.query(Account).filter(Account.date > req.date).all()
            account['balance'] = after_accounts[0].balance - after_accounts[0].price + account['price']

            for after_account in after_accounts:
                after_account.balance += account['price']
        else:
            account['balance'] = last_account.as_dict()['balance'] + account['price']

    db.add(Account(**account))
    db.commit()

    return req
