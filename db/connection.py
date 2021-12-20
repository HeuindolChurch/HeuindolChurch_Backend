from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

DB_URL = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
    environ['DATABASE_USER'],
    environ['DATABASE_PW'],
    environ['DATABASE_HOST'],
    environ['DATABASE_PORT'],
    environ['DATABASE_NAME'],
)

engine = create_engine(DB_URL, encoding='utf-8', echo=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
