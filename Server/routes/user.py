from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from models import s_user
from middleware.database import get_db
from middleware.auth import verify_access_token
from middleware.user import get_user, merge_sqlalchemy_objs_to_dict

users_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@users_router.get("/me", response_model=s_user.TestUser)
def read_me(access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    jwt_payload = verify_access_token(access_token)
    if jwt_payload:
        user = get_user(db, user_uuid=jwt_payload["sub"])

        merged = merge_sqlalchemy_objs_to_dict(
            user,
            user.user_uuid,
            user.address,
            user.address.city.country,
            user.address.city,
        )
        merged["address"] = merge_sqlalchemy_objs_to_dict()
        return s_user.TestUser(**merged)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


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
