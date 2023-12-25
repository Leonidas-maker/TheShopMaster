
from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute() / "config"))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "controllers"))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "models"))

from sqlalchemy.orm import Session
from controllers import user_crud
from models import m_user, s_user
from database import SessionLocal, engine

m_user.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users/", response_model=s_user.User)
def create_user(user: s_user.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email_or_username(db, user.email, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db = db, user = user)