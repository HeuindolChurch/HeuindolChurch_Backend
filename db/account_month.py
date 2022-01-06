from sqlalchemy import Column, Integer, String, Date
from .connection import Base


class AccountMonth(Base):
    __tablename__ = 'account_month'

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Integer, nullable=True)
    date = Column(Date, nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
