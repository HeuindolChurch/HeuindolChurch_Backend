from sqlalchemy import Column, Integer, String, Date, Boolean
from .connection import Base


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, index=True)
    accessToken = Column(String(300), nullable=False)
    refreshToken = Column(String(300), nullable=True)
    userId = Column(Integer, nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
