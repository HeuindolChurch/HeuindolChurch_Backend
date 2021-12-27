from sqlalchemy import Column, Integer, String, Date, Boolean
from .connection import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=True)
    level = Column(Integer, nullable=False)
    name = Column(Integer, nullable=True)
    isDeleted = Column(Boolean, nullable=False)
    date = Column(Date, nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
