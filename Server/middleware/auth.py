from fastapi import HTTPException
from typing import List
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


def check_jti(
    user_security: s_user.UserSecurity, application_id: str, jti: str
) -> bool:  # TODO Change to new table
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
    db: Session,
    user_security: m_user.UserSecurity,
    user_uuid: str, # TODO Maybe use relationship between user_security and user_uuid
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

    # TODO Check old jti if it is still valid

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


# ======================================================== #
# ==================== Tokens-Revocation ================= #
# ======================================================== #


# ~~~~~~~~~~~~~~ Single Token ~~~~~~~~~~~~~ #
def revoke_application_token(user: s_user.User, application_id: str, db: Session) -> bool:
    try:
        db.query(m_user.UserTokens).filter(
            m_user.UserTokens.user_id == user.user_id,
            m_user.UserTokens.token_value == "Application",
            m_user.UserTokens.token_value == application_id,
        ).delete(synchronize_session=False)
        db.commit()
        return True
    except:
        return False


# ~~~~~~~~~~~~~~ All Tokens ~~~~~~~~~~~~~ #
def revoke_all_application_tokens(user: s_user.User, db: Session) -> bool:
    try:
        db.query(m_user.UserTokens).filter(
            m_user.UserTokens.user_id == user.user_id,
            m_user.UserTokens.token_value == "Application",
        ).delete(synchronize_session=False)
        db.commit()
        return True
    except:
        return False


###########################################################################
################################### OTP ###################################
###########################################################################


# ======================================================== #
# ========================= TOTP ========================= #
# ======================================================== #
def verify_totp(db: Session, user_id: str, otp: str) -> bool:
    user_2fa = get_user_2fa(db, user_id)
    if not user_2fa:
        return False

    totp_secret = user_2fa._2fa_secret
    totp = pyotp.TOTP(totp_secret)
    if totp.verify(otp):
        user_2fa._2fa_last_used = otp
        db.commit()
        return True
    else:
        return False


def create_totp(db: Session, user_id: str) -> tuple:
    totp_secret = pyotp.random_hex()
    backup_codes = []
    for _ in range(6):
        backup_codes.append(hex(secrets.randbits(256)).replace("0x", ""))
    backup_codes = ",".join(backup_codes)
    user_2fa = m_user.User2FA(
        user_id=user_id,
        _2fa_secret=totp_secret,
        _2fa_backup=backup_codes,
    )
    db.add(user_2fa)
    db.commit()
    return totp_secret, backup_codes


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


def remove_old_tokens(
    db: Session,
    user_security: m_user.UserSecurity,
    current_timestamp: int = unix_timestamp(),
    old_jti: str = None,
) -> tuple:
    # Get all tokens
    tokens: List[m_user.UserTokens] = user_security.user_tokens

    # Split the tokens
    access_tokens = [token for token in tokens if token.token_type == "Access"]
    temporary_tokens = [token for token in tokens if token.token_type == "Temporary"]
    application_tokens = [token for token in tokens if token.token_type == "Application"]

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

    # Remove expired tokens from the database
    if expired_tokens:
        db.query(m_user.UserTokens).filter(
            m_user.UserTokens.user_id == user_security.user_id,
            m_user.UserTokens.token_id.in_(expired_tokens),
        ).delete(synchronize_session=False)
        db.commit()
    return application_tokens, temporary_tokens, access_tokens


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
