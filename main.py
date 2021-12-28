from fastapi import FastAPI, Depends
from db import Account, get_db, Base, engine
from sqlalchemy.orm import Session

from router import account, auth, user

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(account.router)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
