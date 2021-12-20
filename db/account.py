from sqlalchemy import Column, Integer, String, Date
from .connection import Base


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, index=True)
    reason = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=True)
    note = Column(String(300), nullable=True)
    date = Column(Date, nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
