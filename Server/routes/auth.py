from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Import own modules
import sys
from pathlib import Path as parthlibPath 

sys.path.append(str(parthlibPath(__file__).parent.parent.absolute()))

from models import s_auth, s_user

# ~~~~~~~~~~~~~~~ Middleware ~~~~~~~~~~~~~~ #
from middleware.database import get_db
from middleware.auth import create_tokens
from middleware.user import get_user

# ~~~~~~~~~~~~~~ Controllers ~~~~~~~~~~~~~~ #
from controllers.auth import get_tokens, login, logout
from controllers.user import create_user


###########################################################################
################################### MAIN ##################################
###########################################################################
auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@auth_router.post("/register-application")
def register_application():
    return {"Hello": "World"}

@auth_router.post("/register", response_model=s_auth.UserRegister)
def user_register(user: s_user.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = create_user(db, user)
    refresh_token, access_token = create_tokens(db, user.user_id, None)
    tokens = s_auth.UserTokens(refresh_token = refresh_token, access_token = access_token)
    return {"user": user, "tokens": tokens}

@auth_router.post("/login", response_model=s_auth.UserTokens)
def user_login(user_login: s_auth.UserLogin, db: Session = Depends(get_db)):
    return login(db, user_login.ident, user_login.password, user_login.application_id)

@auth_router.delete("/logout/{user_id}")
def user_logout(tokens: s_auth.UserTokens, user_id: int = Path(...), db: Session = Depends(get_db)):
    return logout(db, user_id, tokens.refresh_token, tokens.access_token)

@auth_router.post("/forgot-password/{user_id}")
def user_forgot_password():
    return {"Hello": "World"}

@auth_router.post("/reset-password/{user_id}")
def user_reset_password():
    return {"Hello": "World"}

@auth_router.post("/verify-account/{user_id}")
def user_verify_account():
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

@auth_router.post("/refresh-token", response_model=s_auth.UserTokens)
def refresh_token(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_tokens(db, refresh_token) 
