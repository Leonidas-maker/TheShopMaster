from fastapi import HTTPException
from sqlalchemy.orm import Session
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)
from cryptography.hazmat.backends import default_backend
import asyncio

# import pyotp
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
import uuid

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from config.security import *
from models import s_user, m_user

###########################################################################
################################## TOKENS #################################
###########################################################################

# ======================================================== #
# ======================= Get Keys ======================= #
# ======================================================== #


# ~~~~~~~~~~~~~~ Private Keys ~~~~~~~~~~~~~ #
def get_tokens_private(
    folder_path: str = str(Path(__file__).parent.absolute() / "jwt_keys"),
):
    # Get the refresh private key
    with open(str(Path(folder_path) / "refresh_private_key.pem"), "rb") as key_file:
        refresh_private_key = load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    # Get the access private key
    with open(str(Path(folder_path) / "access_private_key.pem"), "rb") as key_file:
        access_private_key = load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    return refresh_private_key, access_private_key


# ~~~~~~~~~~~~~~ Public Keys ~~~~~~~~~~~~~ #
def get_refresh_token_public(
    folder_path: str = str(Path(__file__).parent.absolute() / "jwt_keys"),
):
    # Get the refresh public key
    with open(str(Path(folder_path) / "refresh_public_key.pem"), "rb") as key_file:
        public_key = load_pem_public_key(key_file.read(), backend=default_backend())

    return public_key


def get_access_token_public(
    folder_path: str = str(Path(__file__).parent.absolute() / "jwt_keys"),
):
    # Get the access public key
    with open(str(Path(folder_path) / "access_public_key.pem"), "rb") as key_file:
        public_key = load_pem_public_key(key_file.read(), backend=default_backend())

    return public_key


# ======================================================== #
# ======================== Verify ======================== #
# ======================================================== #


# ~~~~~~~~~~~~~~ Refresh Token ~~~~~~~~~~~~~ #
def verify_refresh_token(token: str):
    public_key = get_refresh_token_public()
    try:
        options = {"verify_aud": False}  # TODO Change this to True
        payload = jwt.decode(token, public_key, algorithms="ES512", options=options)
        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def check_jti(user_security: s_user.UserSecurity, application_id: str, jti: str): 
    if application_id and application_id != "webapplication":
        application_tokens = user_security.application_tokens
        if application_tokens[application_id] == jti:
            return True
        else:
            return False
    else:
        temporary_tokens = user_security.temporary_tokens.split(",")
        if jti in temporary_tokens:
            return True
        else:
            return False


# ~~~~~~~~~~~~~~ Access Token ~~~~~~~~~~~~~ #
def verify_access_token(token: str):
    public_key = get_access_token_public()
    try:
        options = {"verify_aud": False}  # TODO Change this to True
        payload = jwt.decode(token, public_key, algorithms="ES256", options=options)
        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def get_token_payload(token: str):
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload

# ======================================================== #
# ==================== Tokens-Rotation =================== #
# ======================================================== #
def create_tokens(
    db: Session, user_id: str, old_jti: str = None, application_id: str = None
):
    # Get the user_security try 3 times
    for _ in range(3):
        try:
            user_security = (
                db.query(m_user.UserSecurity).filter_by(user_id=user_id).first()
            )
            break
        except:
            asyncio.sleep(0.25)
            continue
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    # Check if the user is locked
    if user_security.secutity_warns >= MAX_WARNS:
        raise HTTPException(status_code=403, detail="Account temporarily locked")

    current_timestamp = unix_timestamp()

    # Remove expired tokens
    application_tokens, temp_tokens, active_access_tokens = remove_old_tokens(user_security, current_timestamp)
    
    if len(active_access_tokens) >= MAX_ACTIVE_ACCESS_TOKENS:
        raise_security_warns(db, user_security, "Too many access tokens active")

    if len(temp_tokens) >= MAX_WEB_REFRESH_TOKENS:
        raise HTTPException(
            status_code=403, detail="Too many active temporary instances"
        )
    
    if check_jti_timestamp(old_jti):
        if not check_jti(user_security, application_id, old_jti):
            raise_security_warns(db, user_security, "Invalid jti")

    # Get the private keys and create the jti
    refresh_private_key, access_private_key = get_tokens_private()
    refresh_jti = str(uuid.uuid4())
    access_jti = str(uuid.uuid4())

    # ~~~~~~~~ Create the refresh token ~~~~~~~ #
    if application_id and application_id != "webapplication":
        token_exp = unix_timestamp(days=30)
        payload = {
            "iss": "https://api.theshopmaster.com",  #! Change this to the domain of the api
            "sub": user_id,
            "aud": application_id,
            "exp": token_exp,
            "nbf": current_timestamp,
            "iat": current_timestamp,
            "jti": refresh_jti,
        }

        # Add the jti and application_id to the user_security
        application_tokens[application_id] = create_jti_timestamp(refresh_jti, token_exp)
    else:
        token_exp = unix_timestamp(minutes=15)  #! More then 15 minutes?
        payload = {
            "iss": "https://api.theshopmaster.com",  #! Change this to the domain of the api
            "sub": user_id,
            "aud": "webapplication",
            "exp": token_exp,
            "nbf": current_timestamp,
            "iat": current_timestamp,
            "jti": refresh_jti,
        }

        # Remove the old jti from the user_security
        if old_jti:
            temp_tokens.remove(old_jti)

        # Add the jti to the user_security
        temp_tokens.append(create_jti_timestamp(refresh_jti, token_exp))
       

    reftesh_token = jwt.encode(payload, refresh_private_key, algorithm="ES512")

    # ~~~~~~~~ Create the access token ~~~~~~~ #
    token_exp = unix_timestamp(minutes=8)
    payload = {
        "iss": "https://api.theshopmaster.com",  #! Change this to the domain of the api
        "sub": user_id,
        "aud": application_id if application_id else "webapplication",
        "exp": token_exp,
        "nbf": current_timestamp,
        "iat": current_timestamp,
        "jti": access_jti,
    }

    active_access_tokens.append(create_jti_timestamp(access_jti, token_exp))
    
    access_token = jwt.encode(payload, access_private_key, algorithm="ES256")

    # Update the user_security
    user_security.application_tokens = application_tokens
    user_security.temporary_tokens = ",".join(temp_tokens)
    user_security.active_access_tokens = ",".join(active_access_tokens)
    db.commit()

    return reftesh_token, access_token


# ======================================================== #
# ==================== Tokens-Revocation ================= #
# ======================================================== #


# ~~~~~~~~~~~~~~ Single Token ~~~~~~~~~~~~~ #
def revoke_application_token(user: s_user.User, application_id: str, db: Session):
    try:
        user_security = (
            db.query(m_user.UserSecurity).filter_by(user_id=user.user_id).first()
        )
        application_tokens = user_security.application_tokens
        del application_tokens[application_id]
        user_security.application_tokens = application_tokens
        db.commit()
        return True
    except:
        return False


# ~~~~~~~~~~~~~~ All Tokens ~~~~~~~~~~~~~ #
def revoke_all_application_tokens(user: s_user.User, db: Session):
    try:
        user_security = (
            db.query(m_user.UserSecurity).filter_by(user_id=user.user_id).first()
        )
        user_security.application_tokens = []
        db.commit()
        return True
    except:
        return False


# ======================================================== #
# ========================== OTP ========================= #
# ======================================================== #
def verify_otp(user: s_user.User, otp: str):
    pass


# ======================================================== #
# ======================= Password ======================= #
# ======================================================== #
def check_password(db: Session, user_id: str, password: str):
    db_user_security = db.query(m_user.UserSecurity).filter_by(user_id=user_id).first()
    if bcrypt.checkpw(
        password.encode("utf-8"), db_user_security.password.encode("utf-8")
    ):
        return True
    else:
        return False


# ======================================================== #
# ======================= Sonstiges ====================== #
# ======================================================== #
def unix_timestamp(
    days: int = 0,
    seconds: int = 0,
    microseconds: int = 0,
    milliseconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    weeks: int = 0,
) -> int:
    out = datetime.now(tz=timezone.utc) + timedelta(
        days,
        seconds,
        microseconds,
        milliseconds,
        minutes,
        hours,
        weeks,
    )
    return int(out.timestamp())


def create_jti_timestamp(jti: str, timestamp: int):
    return f"{jti}:{timestamp}"

def check_jti_timestamp(jti_timestamp: str):
    try:
        jti_timestamp.split(":")
        return True
    except:
        return False
    
def verify_jti_timestamp(jti_timestamp: str, current_timestamp: int = unix_timestamp()):
    _, timestamp = jti_timestamp.split(":")
    if int(timestamp) < current_timestamp:
        return False
    else:
        return True
    

def remove_old_tokens(user_security: m_user.UserSecurity, current_timestamp: int = unix_timestamp()):
    if user_security.application_tokens: #* Shouldn't be NULL but just in case
        # Remove expired application tokens
        application_tokens = user_security.application_tokens
        for key, value in application_tokens.items():
            if int(value.split(":")[1]) < current_timestamp:
                del application_tokens[key]
    else:
        application_tokens = {}

    if user_security.temporary_tokens:
        # Remove expired temporary tokens
        temp_tokens = user_security.temporary_tokens.split(",")
        for token in temp_tokens:
            if not verify_jti_timestamp(token, current_timestamp):
                temp_tokens.remove(token)
    else:
        temp_tokens = []

    if user_security.active_access_tokens:
        # Remove expired active access tokens
        active_access_tokens = user_security.active_access_tokens.split(",")
        for token in active_access_tokens:
            if not verify_jti_timestamp(token, current_timestamp):
                active_access_tokens.remove(token)
    else:
        active_access_tokens = []

    return application_tokens, temp_tokens, active_access_tokens

def raise_security_warns(db: Session, user_security: m_user.UserSecurity, error: str):
    security_warns = user_security.secutity_warns + 1
    user_security.secutity_warns = security_warns
    user_security.verified = False
    db.commit()
    raise HTTPException(status_code=403, detail=f"{error}! Warns:{security_warns}/{MAX_WARNS} until Account is locked")