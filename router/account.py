from fastapi import APIRouter, Depends
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from db import Account, get_db
import body

router = APIRouter(
    prefix='/account'
)


@router.get('/')
async def get_account(db: Session = Depends(get_db), date: datetime.date = datetime.date.today()):
    start_at = date.replace(day=1)
    end_at = start_at + relativedelta(months=1)

    return db.query(Account).filter(Account.date >= start_at, Account.date < end_at).order_by(Account.date).all()


@router.post('/')
async def post_account(req: body.Account, db: Session = Depends(get_db)):
    account = req.dict()

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
