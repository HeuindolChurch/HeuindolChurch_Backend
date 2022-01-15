from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

import router
from db import Account, get_db, Base, engine
from sqlalchemy.orm import Session

from router import account, auth, user

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(router.router)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
