from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import own modules
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute() / "controllers"))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "models"))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "middleware"))

from controllers.user import CrudUser
from models import s_user
from middleware.database import get_db


###########################################################################
################################### MAIN ##################################
###########################################################################
auth_router = APIRouter()

@auth_router.post("/register", response_model=s_user.User)
def user_register(user: s_user.UserCreate, db: Session = Depends(get_db)):
    crud_user = CrudUser(db)
    db_user = crud_user.get_user(user.email, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(user = user)

@auth_router.post("/login/{user_id}")
def user_login():
    return {"Hello": "World"}

@auth_router.post("/logout/{user_id}")
def user_logout():
    return {"Hello": "World"}

@auth_router.post("/forgot-password/{user_id}")
def user_forgot_password():
    return {"Hello": "World"}

@auth_router.post("/reset-password/{user_id}")
def user_reset_password():
    return {"Hello": "World"}

@auth_router.post("/verify-email/{user_id}")
def user_verify_email():
    return {"Hello": "World"}

@auth_router.post("/add-2fa/{user_id}")
def user_add_2fa():
    return {"Hello": "World"}

@auth_router.delete("/remove-2fa/{user_id}")
def user_remove_2fa():
    return {"Hello": "World"}

@auth_router.post("/verify-2fa/{user_id}")
def user_verify_2fa():
    return {"Hello": "World"}

@auth_router.post("/verify-2fa-backup/{user_id}")
def user_verify_2fa_backup():
    return {"Hello": "World"}
