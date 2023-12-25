from fastapi import FastAPI, APIRouter, Depends, HTTPException
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute() / "controllers"))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "models"))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "middleware"))

from sqlalchemy.orm import Session
from controllers.user import CrudUser
from models import s_user
from middleware.database import get_db

users_router = APIRouter()

@users_router.get("/me")
def read_me():
    return {"Hello": "World"}

@users_router.put("/me")
def update_me():
    return {"Hello": "World"}

@users_router.delete("/me")
def delete_me():
    return {"Hello": "World"}

@users_router.get("/me/all")
def read_me_all():
    return {"Hello": "World"}

@users_router.get("/me/address")
def read_me_address():
    return {"Hello": "World"}

@users_router.get("/me/shopping-cart")
def read_me_shopping_cart():
    return {"Hello": "World"}

@users_router.get("/me/favorite-products")
def read_me_favorite_products():
    return {"Hello": "World"}