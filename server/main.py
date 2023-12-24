
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute() / "config"))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "models"))

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

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}