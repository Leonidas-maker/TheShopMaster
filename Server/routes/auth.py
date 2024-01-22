from fastapi import APIRouter, Depends, Path, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from models import s_auth, s_user

# ~~~~~~~~~~~~~~~ Middleware ~~~~~~~~~~~~~~ #
from middleware.database import get_db

# ~~~~~~~~~~~~~~ Controllers ~~~~~~~~~~~~~~ #
from controllers.auth import (
    get_tokens,
    register,
    login,
    logout,
    verify_account,
    add_2fa,
    verify_first_2fa,
)


###########################################################################
################################### MAIN ##################################
###########################################################################
auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post("/register-application")
def register_application():
    return {"Hello": "World"}


@auth_router.post("/register", response_model=s_auth.UserResRegister)
def user_register(
    user: s_user.UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    return register(db, user, background_tasks)


@auth_router.post("/login", response_model=s_auth.UserTokens)
def user_login(user_login: s_auth.UserLogin, db: Session = Depends(get_db)):
    return login(db, user_login.ident, user_login.password, user_login.application_id)


@auth_router.delete("/logout/{user_uuid}")
def user_logout(
    tokens: s_auth.UserTokens,
    user_uuid: str = Path(...),
    db: Session = Depends(get_db),
):
    return logout(db, user_uuid, tokens.refresh_token, tokens.access_token)


@auth_router.post("/forgot-password/{user_uuid}")
def user_forgot_password():
    return {"Hello": "World"}


@auth_router.post("/reset-password/{user_uuid}")
def user_reset_password():
    return {"Hello": "World"}


@auth_router.post("/verify-account/{user_uuid}")
def user_verify_account(
    verify_code: str, db: Session = Depends(get_db), user_uuid: str = Path(...)
):
    return verify_account(db, user_uuid, verify_code)


@auth_router.post("/add-2fa/", response_model=s_auth.UserResActivate2FA)
def user_add_2fa(
    req: s_auth.UserReqActivate2FA,
    access_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    return add_2fa(req, access_token, db)


@auth_router.get("/verify-first-2fa/")
def user_verify_first_2fa(
    access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    return verify_first_2fa(db, access_token)


@auth_router.delete("/remove-2fa/{user_uuid}")
def user_remove_2fa():
    return {"Hello": "World"}


@auth_router.post("/verify-2fa/{user_uuid}")
def user_verify_2fa():
    return {"Hello": "World"}


@auth_router.post("/verify-2fa-backup/{user_uuid}")
def user_verify_2fa_backup():
    return {"Hello": "World"}


@auth_router.post("/refresh-token", response_model=s_auth.UserTokens)
def refresh_token(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_tokens(db, refresh_token)
