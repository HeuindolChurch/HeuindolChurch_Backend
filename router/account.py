from fastapi import APIRouter, Depends, HTTPException, Request, Response
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from db import Account, AccountMonth, get_db
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

    return db.query(Account).filter(Account.date >= start_at, Account.date < end_at).order_by(Account.date,
                                                                                              Account.price,
                                                                                              Account.id).all()


@router.put('/{account_id}')
async def edit_account(req: body.Account, account_id: int, db: Session = Depends(get_db),
                       auth_provider: AuthProvider = Depends(AuthProvider())):
    await auth_provider.check_authority(2)
    account = db.query(Account).filter_by(id=account_id)
    new_account = req.dict()
    new_account['id'] = account_id

    request = {k: v for k, v in new_account.items()}

    for key, value in request.items():
        setattr(account, key, value)

    db.commit()

    return account


@router.post('/')
async def post_account(req: body.Account, db: Session = Depends(get_db),
                       auth_provider: AuthProvider = Depends(AuthProvider())):
    await auth_provider.check_authority(2)

    account = req.dict()

    if auth_provider.level < 2:
        raise HTTPException(status_code=403, detail='권한이 부족합니다.')

    balance_date = req.date.replace(day=1)
    balance = db.query(Account).filter_by(date=balance_date).first()
    before_balance = db.query(Account).filter_by(date=balance_date - relativedelta(months=1)).first()

    if balance is None:
        db.add(AccountMonth(date=balance_date, balance=before_balance.balance + account['price']))
    elif req.insert is True:
        balances = db.query(Account).filter(AccountMonth.date >= balance_date).all()

        if before_balance is None:
            db.add(AccountMonth(date=balance_date, balance=balance.balance - account['price']))
        for bal in balances:
            bal.balance = bal.balance + req.price
    else:
        balance.balance += req.price

    db.add(Account(**account))
    db.commit()

    return req


@router.delete('/{account_id}')
async def delete_account(account_id: int, db: Session = Depends(get_db), auth_provider=Depends(AuthProvider)):
    await auth_provider.check_authority(2)
    account = db.query(Account).filter_by(id=account_id).first()

    db.delete(account)
    db.commit()

    return Response(status_code=200)
