from fastapi import HTTPException
from typing import List
from sqlalchemy import desc
from sqlalchemy.orm import Session
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

import pyotp
import secrets
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
import uuid

from pathlib import Path

from config.security import *
from models import s_user, m_user
from middleware.user import get_user_security, get_user_2fa


###########################################################################
############################## Security Warns #############################
###########################################################################
def raise_security_warns(db: Session, user_security: m_user.UserSecurity, error: str) -> None:
    security_warns = user_security.secutity_warns + 1
    user_security.secutity_warns = security_warns
    user_security.verified = False
    db.commit()
    raise HTTPException(
        status_code=403,
        detail=f"{error}! Warns:{security_warns}/{MAX_WARNS} until Account is locked",
    )


def check_security_warns(user_security: m_user.UserSecurity) -> None:
    if user_security.secutity_warns >= MAX_WARNS:
        raise HTTPException(status_code=403, detail="Account locked please try again later")


###########################################################################
################################## Helper #################################
###########################################################################
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


###########################################################################
################################## TOKENS #################################
###########################################################################

# ======================================================== #
# ======================= Gen Keys ======================= #
# ======================================================== #


def generate_ecdsa_keys(curve: ec.EllipticCurve):
    # ~~~~~~~~~~~~~~ Access Token ~~~~~~~~~~~~~ #
    # Generate the private key
    private_key = ec.generate_private_key(curve)

    # Get the public key from the private key
    public_key = private_key.public_key()

    # Convert the keys to PEM format
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return pem_private_key, pem_public_key


# ======================================================== #
# ================== Key File Operations ================= #
# ======================================================== #


def save_key(key: bytes, file_name: str, folder_path: Path):
    with (folder_path / file_name).open("wb") as key_file:
        key_file.write(key)


def load_key(
    file_name: str,
    key_password: bytes = None,
    folder_path: Path = Path(__file__).parent.absolute() / "jwt_keys",
):
    if "private" in file_name:
        with (folder_path / file_name).open("rb") as key_file:
            key = load_pem_private_key(
                key_file.read(), password=key_password, backend=default_backend()
            )
    elif "public" in file_name:
        with (folder_path / file_name).open("rb") as key_file:
            key = load_pem_public_key(key_file.read(), backend=default_backend())
    else:
        raise ValueError("Invalid file_name")
    return key


def generate_keys(folder_path: Path = Path(__file__).parent.absolute() / "jwt_keys"):
    access_private_key, access_public_key = generate_ecdsa_keys(ec.SECP256R1())
    refresh_private_key, refresh_public_key = generate_ecdsa_keys(ec.SECP521R1())
    save_key(access_private_key, "access_private_key.pem", folder_path)
    save_key(access_public_key, "access_public_key.pem", folder_path)
    save_key(refresh_private_key, "refresh_private_key.pem", folder_path)
    save_key(refresh_public_key, "refresh_public_key.pem", folder_path)


# ======================================================== #
# ======================= Get Keys ======================= #
# ======================================================== #


# ~~~~~~~~~~~~~~ Private Keys ~~~~~~~~~~~~~ #
def get_tokens_private(
    folder_path: Path = Path(__file__).parent.absolute() / "jwt_keys",
) -> (ec.EllipticCurvePrivateKey, ec.EllipticCurvePrivateKey):
    if (
        not (folder_path / "refresh_private_key.pem").exists()
        and not (folder_path / "access_private_key.pem").exists()
    ):
        generate_keys()
    # Get the refresh private key
    refresh_private_key = load_key("refresh_private_key.pem")

    # Get the access private key
    access_private_key = load_key("access_private_key.pem")

    return refresh_private_key, access_private_key


def get_security_token_private(
    folder_path: Path = Path(__file__).parent.absolute() / "jwt_keys",
) -> ec.EllipticCurvePrivateKey:
    if not (folder_path / "security_private_key.pem").exists():
        security_private_key, security_public_key = generate_ecdsa_keys(ec.SECP256R1())
        save_key(security_private_key, "security_private_key.pem", folder_path)
        save_key(security_public_key, "security_public_key.pem", folder_path)
    security_private_key = load_key("security_private_key.pem")
    return security_private_key


# ~~~~~~~~~~~~~~ Public Keys ~~~~~~~~~~~~~ #
def get_refresh_token_public(
    folder_path: Path = Path(__file__).parent.absolute() / "jwt_keys",
) -> ec.EllipticCurvePublicKey:
    folder_path = Path(folder_path)
    if not (folder_path / "refresh_public_key.pem").exists():
        generate_keys()

    # Get the refresh public key
    public_key = load_key("refresh_public_key.pem")

    return public_key


def get_access_token_public(
    folder_path: Path = Path(__file__).parent.absolute() / "jwt_keys",
) -> ec.EllipticCurvePublicKey:
    folder_path = Path(folder_path)
    if not (folder_path / "access_public_key.pem").exists():
        generate_keys()

    # Get the access public key
    public_key = load_key("access_public_key.pem")

    return public_key


def get_security_token_public(
    folder_path: Path = Path(__file__).parent.absolute() / "jwt_keys",
) -> ec.EllipticCurvePublicKey:
    folder_path = Path(folder_path)
    if not (folder_path / "security_public_key.pem").exists():
        generate_keys()

    # Get the access public key
    public_key = load_key("security_public_key.pem")

    return public_key


# ======================================================== #
# ======================== Verify ======================== #
# ======================================================== #


def check_jti(
    db: Session,
    jti: str,
    user_id: str = None,
    user_uuid: str = None,
    user_security: m_user.UserSecurity = None,
    application_id: str = "webapplication",
) -> bool:
    if user_id:
        token_exists = (
            db.query(m_user.UserTokens)
            .filter(
                m_user.UserTokens.user_id == user_id,
                m_user.UserTokens.token_jti == jti,
                m_user.UserTokens.token_value == application_id,
            )
            .first()
            is not None
        )
    elif user_uuid:
        user_uuid = uuid.UUID(user_uuid)
        token_exists = (
            db.query(m_user.UserTokens)
            .join(m_user.UserUUID, m_user.UserUUID.user_uuid == user_uuid)
            .filter(
                m_user.UserTokens.token_jti == jti,
                m_user.UserTokens.token_value == application_id,
            )
            .first()
            is not None
        )
    elif user_security:
        tokens: [m_user.UserTokens] = user_security.user_tokens
        for token in tokens:
            if token.token_jti == jti and token.token_value == application_id:
                token_exists = True
                break
        else:
            token_exists = False

    return token_exists


# ~~~~~~~~~~~~~~ Refresh Token ~~~~~~~~~~~~~ #
def verify_refresh_token(db: Session, token: str):
    public_key = get_refresh_token_public()
    try:
        options = {"verify_aud": False}  # TODO Change this to True
        payload = jwt.decode(token, public_key, algorithms="ES512", options=options)

        if not check_jti(
            db=db,
            jti=payload["jti"],
            user_uuid=payload["sub"],
            application_id=payload["aud"],
        ):
            return False

        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


# ~~~~~~~~~~~~~~ Access Token ~~~~~~~~~~~~~ #
def verify_access_token(db: Session, token: str):
    public_key = get_access_token_public()
    try:
        options = {"verify_aud": False}  # TODO Change this to True
        payload = jwt.decode(token, public_key, algorithms="ES256", options=options)

        # Check if the jti is valid
        if not check_jti(
            db=db,
            jti=payload["jti"],
            user_uuid=payload["sub"],
            application_id=payload["aud"],
        ):
            return False
        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


# ~~~~~~~~~~~~~ Security Token ~~~~~~~~~~~~ #
def verify_security_token(db: Session, token: str, is_2fa: bool = False):
    public_key = get_security_token_public()
    try:
        reasons = ["login-2fa", "forgot-password"]  # TODO Update this
        payload = jwt.decode(token, public_key, algorithms="ES256", audience=reasons)

        user_security = get_user_security(db, user_uuid=payload["sub"], with_2fa=is_2fa)
        # Check if the jti is valid
        if not check_jti(
            db=db,
            jti=payload["jti"],
            user_security=user_security,
            application_id=payload["aud"],
        ):
            return False, None
        
        return payload, user_security
    except jwt.ExpiredSignatureError:
        return False, None
    except jwt.InvalidTokenError:
        return False, None


def get_token_payload(token: str):
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload


# ======================================================== #
# ==================== Tokens-Rotation =================== #
# ======================================================== #
def create_tokens(
    db: Session,
    user_security: m_user.UserSecurity,
    user_uuid: str,  # TODO Maybe use relationship between user_security and user_uuid
    old_jti: str = None,
    application_id: str = None,
) -> (str, str):
    user_id = user_security.user_id

    # Check if the user is locked
    check_security_warns(user_security)

    current_timestamp = unix_timestamp()

    # Remove expired tokens
    _, temporary_tokens, active_access_tokens = remove_old_tokens(
        db, user_security, current_timestamp, old_jti
    )

    if len(active_access_tokens) >= MAX_ACTIVE_ACCESS_TOKENS:
        raise_security_warns(db, user_security, "Too many access tokens active")

    if len(temporary_tokens) >= MAX_WEB_REFRESH_TOKENS:
        raise HTTPException(status_code=403, detail="Too many active temporary instances")

    # Get the private keys and create the jti
    refresh_private_key, access_private_key = get_tokens_private()
    refresh_jti = str(uuid.uuid4())
    access_jti = str(uuid.uuid4())

    # ~~~~~~~~ Create the refresh token ~~~~~~~ #
    if application_id and application_id != "webapplication":
        token_exp = unix_timestamp(days=30)
        payload = {
            "iss": "https://api.theshopmaster.com",  #! Change this to the domain of the api
            "sub": user_uuid,
            "aud": application_id,
            "exp": token_exp,
            "nbf": current_timestamp,
            "iat": current_timestamp,
            "jti": refresh_jti,
        }

        # Add the jti and application_id to the user_security
        new_reftesh_token = m_user.UserTokens(
            user_id=user_id,
            token_type="Application",
            token_jti=refresh_jti,
            token_value=application_id,
            creation_time=current_timestamp,
            expiration_time=token_exp,
        )
    else:
        token_exp = unix_timestamp(minutes=15)  #! More then 15 minutes?
        payload = {
            "iss": "https://api.theshopmaster.com",  #! Change this to the domain of the api
            "sub": user_uuid,
            "aud": "webapplication",
            "exp": token_exp,
            "nbf": current_timestamp,
            "iat": current_timestamp,
            "jti": refresh_jti,
        }
        new_reftesh_token = m_user.UserTokens(
            user_id=user_id,
            token_type="Temporary",
            token_jti=refresh_jti,
            token_value="webapplication",
            creation_time=current_timestamp,
            expiration_time=token_exp,
        )

    reftesh_token = jwt.encode(payload, refresh_private_key, algorithm="ES512")
    db.add(new_reftesh_token)
    db.flush()

    # ~~~~~~~~ Create the access token ~~~~~~~ #
    token_exp = unix_timestamp(minutes=8)
    payload = {
        "iss": "https://api.theshopmaster.com",  #! Change this to the domain of the api
        "sub": user_uuid,
        "aud": application_id if application_id else "webapplication",
        "exp": token_exp,
        "nbf": current_timestamp,
        "iat": current_timestamp,
        "jti": access_jti,
    }

    new_access_token = m_user.UserTokens(
        user_id=user_id,
        token_type="Access",
        token_jti=access_jti,
        token_value=application_id if application_id else "webapplication",
        creation_time=current_timestamp,
        expiration_time=token_exp,
    )

    access_token = jwt.encode(payload, access_private_key, algorithm="ES256")
    db.add(new_access_token)
    db.commit()

    return reftesh_token, access_token


def create_security_token(
    db: Session,
    user_id: str,
    user_uuid: str,  # TODO Maybe use relationship between user_security and user_uuid
    reason: str,
) -> (str, str):
    new_jti = str(uuid.uuid4())
    current_timestamp = unix_timestamp()
    token_exp = unix_timestamp(minutes=5)
    payload = {
        "iss": "https://api.theshopmaster.com",  #! Change this to the domain of the api
        "sub": user_uuid,
        "aud": reason,
        "exp": token_exp,
        "nbf": current_timestamp,
        "iat": current_timestamp,
        "jti": new_jti,
    }
    new_security_token = m_user.UserTokens(
        user_id=user_id,
        token_type="Security",
        token_jti=new_jti,
        token_value=reason,
        creation_time=current_timestamp,
        expiration_time=token_exp,
    )
    security_private_key = get_security_token_private()
    security_token = jwt.encode(payload, security_private_key, algorithm="ES256")
    db.add(new_security_token)
    db.commit()

    return security_token


# ======================================================== #
# ==================== Tokens-Revocation ================= #
# ======================================================== #


# ~~~~~~~~~~~~~~ Single Token ~~~~~~~~~~~~~ #
def revoke_token(db: Session, user_id: str, token_type: str, token_value: str, token_jti: uuid.UUID) -> bool:
    try:
        db.query(m_user.UserTokens).filter(
            m_user.UserTokens.user_id == user_id,
            m_user.UserTokens.token_type == token_type,
            m_user.UserTokens.token_value == token_value,
            m_user.UserTokens.token_jti == token_jti,
        ).delete(synchronize_session=False)
        db.commit()
        return True
    except:
        return False


# ~~~~~~~~~~~~~~ All Tokens ~~~~~~~~~~~~~ #
def revoke_all_tokens(db: Session, user_id: str, token_type: str = None, token_value: str = None):
    query = db.query(m_user.UserTokens).filter(m_user.UserTokens.user_id == user_id)
    
    if token_type:
        query = query.filter(m_user.UserTokens.token_type == token_type)
    elif token_value:
        query = query.filter(m_user.UserTokens.token_value == token_value)

    query.delete(synchronize_session=False)
    db.commit()

def revoke_all_application_tokens(db: Session, user: s_user.User):
    revoke_all_tokens(db, user.user_id, token_type="Application")

def revoke_all_security_tokens(db: Session, user_id: str):
    revoke_all_tokens(db, user_id, token_type="Security")

def revoke_all_temporary_tokens(db: Session, user_id: str):
    revoke_all_tokens(db, user_id, token_type="Temporary")

def revoke_all_access_tokens(db: Session, user_id: str):
    revoke_all_tokens(db, user_id, token_type="Access")

###########################################################################
################################### OTP ###################################
###########################################################################


# ======================================================== #
# ========================= TOTP ========================= #
# ======================================================== #
def verify_totp(db: Session, otp: str, user_uuid: str = None, user_2fa: m_user.User2FA = None) -> bool:
    if user_uuid:
        user_2fa = get_user_2fa(db, user_uuid=user_uuid)
    if not user_2fa:
        return False

    totp_secret = user_2fa._2fa_secret
    totp = pyotp.TOTP(totp_secret)
    if  user_2fa._2fa_last_used != otp and totp.verify(otp): #* short-circuit evaluation to prevent efficient timing attacks
        user_2fa._2fa_last_used = otp
        db.commit()
        return True
    else:
        return False


def create_totp(db: Session, user_id: str) -> str:
    totp_secret = pyotp.random_base32()

    user_2fa = m_user.User2FA(
        user_id=user_id,
        _2fa_secret=totp_secret,
        _2fa_backup=None,
    )
    db.add(user_2fa)
    db.commit()
    return totp_secret


def create_backup_codes(db: Session, user_uuid: str) -> List[str]:
    user_security = get_user_security(db, user_uuid=user_uuid, with_2fa=True)
    if not user_security._2fa_enabled:
        user_2fa: m_user.User2FA = user_security.user_2fa
        backup_codes = []
        for _ in range(6):
            tmp_number = secrets.randbelow(1000000)
            backup_codes.append(f"{tmp_number:06}")
        user_2fa._2fa_backup = ";".join(backup_codes)
        user_security._2fa_enabled = True
        db.commit()
        return backup_codes
    else:
        raise HTTPException(status_code=400, detail="2FA already enabled")

def remove_2fa(db: Session, users_security: m_user.UserSecurity):
    users_security.user_2fa.delete(synchronize_session=False)
    users_security._2fa_enabled = False
    db.commit()

# ======================================================== #
# ====================== Simple-OTP ====================== #
# ======================================================== #
def verify_simple_otp(user_security: m_user.UserSecurity, otp: str) -> bool:
    otp = otp.strip()
    verify_otp = user_security.verify_otp
    if verify_otp:
        verify_otp = verify_otp.split(":")
        if verify_otp[0] == otp and int(verify_otp[1]) > unix_timestamp():
            return True
        else:
            return False
    else:
        return False


def create_simple_otp(
    db: Session, user_security: m_user.UserSecurity, expire_time: int = 15
) -> int:
    # Create the otp: XXXXXX
    otp = secrets.randbelow(1000000)
    # Add the expire time: XXXXXX:XXXXXX and save it to the user_security
    user_security.verify_otp = f"{otp}:{unix_timestamp(minutes=expire_time)}"
    db.commit()
    return otp


# ======================================================== #
# ======================= Password ======================= #
# ======================================================== #
def check_password(
    db: Session,
    password: str,
    user_id: str = None,
    user_security: m_user.UserSecurity = None,
) -> bool:
    # TODO Maybe unnecessary
    if user_id:
        user_security = get_user_security(db, user_id)
    elif not user_security:
        raise ValueError("No user_security provided")
    # * until here

    # Check if the password is correct
    if bcrypt.checkpw(password.encode("utf-8"), user_security.password.encode("utf-8")):
        return True
    else:
        return False


###########################################################################
############################## Token Cleaners #############################
###########################################################################


def remove_old_tokens(
    db: Session,
    user_security: m_user.UserSecurity,
    current_timestamp: int = unix_timestamp(),
    old_jti: str = "",
) -> tuple:
    # Get all tokens
    tokens: List[m_user.UserTokens] = user_security.user_tokens

    # Split the tokens
    access_tokens = [token for token in tokens if token.token_type == "Access"]
    temporary_tokens = [token for token in tokens if token.token_type == "Temporary"]
    application_tokens = [token for token in tokens if token.token_type == "Application"]
    security_tokens = [token for token in tokens if token.token_type == "Security"]

    expired_tokens = []

    if application_tokens:  # * Shouldn't be NULL but just in case
        # Remove expired application tokens
        for token in application_tokens:
            if token.expiration_time < current_timestamp or token.token_jti == old_jti:
                application_tokens.remove(token)
                expired_tokens.append(token.token_id)
    else:
        application_tokens = []

    if temporary_tokens:
        # Remove expired temporary tokens
        for token in temporary_tokens:
            if token.expiration_time < current_timestamp or token.token_jti == old_jti:
                temporary_tokens.remove(token)
                expired_tokens.append(token.token_id)
    else:
        temporary_tokens = []

    if access_tokens:
        # Remove expired active access tokens
        for token in access_tokens:
            if token.expiration_time < current_timestamp:
                access_tokens.remove(token)
                expired_tokens.append(token.token_id)
    else:
        access_tokens = []

    if security_tokens:
        # Remove expired active security tokens
        for token in security_tokens:
            if token.expiration_time < current_timestamp:
                security_tokens.remove(token)
                expired_tokens.append(token.token_id)

    # Remove expired tokens from the database
    if expired_tokens:
        db.query(m_user.UserTokens).filter(
            m_user.UserTokens.user_id == user_security.user_id,
            m_user.UserTokens.token_id.in_(expired_tokens),
        ).delete(synchronize_session=False)
        db.commit()
    return application_tokens, temporary_tokens, access_tokens


def remove_older_security_token(
    db: Session, user_security: m_user.UserSecurity, reason: str, max_tokens: int = 2
):
    security_tokens: [m_user.UserTokens] = user_security.user_tokens
    if len(security_tokens) >= max_tokens:
        security_tokens = security_tokens[
            : len(security_tokens) - max_tokens + 1
        ]  # Remove the oldest token
        db.query(m_user.UserTokens).filter(
            m_user.UserTokens.user_id == user_security.user_id,
            m_user.UserTokens.token_type == "Security",
            m_user.UserTokens.token_value == reason,
            m_user.UserTokens.token_jti.in_([token.token_jti for token in security_tokens]),
        ).delete(synchronize_session=False)
        db.commit()
