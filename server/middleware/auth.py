from fastapi import HTTPException
from sqlalchemy.orm import Session
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend
#import pyotp
import bcrypt
import jwt
from datetime import datetime,timezone,timedelta
import uuid

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from models import s_user, m_user

###########################################################################
################################## TOKENS #################################
###########################################################################

# ======================================================== #
# ======================= Get Keys ======================= #
# ======================================================== #

# ~~~~~~~~~~~~~~ Private Keys ~~~~~~~~~~~~~ #
def get_tokens_private(folder_path: str = str(Path(__file__).parent.absolute() / "jwt_keys")):
    # Get the refresh private key
    with open(str(Path(folder_path) / "refresh_private_key.pem"), 'rb') as key_file:
        refresh_private_key = load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    
    # Get the access private key
    with open(str(Path(folder_path) / "access_private_key.pem"), 'rb') as key_file:
        access_private_key = load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    return refresh_private_key, access_private_key


# ~~~~~~~~~~~~~~ Public Keys ~~~~~~~~~~~~~ #
def get_refresh_token_public(folder_path: str = str(Path(__file__).parent.absolute() / "jwt_keys")):
    # Get the refresh public key
    with open(str(Path(folder_path) / "refresh_public_key.pem"), 'rb') as key_file:
        public_key = load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    return public_key

def get_access_token_public(folder_path: str = str(Path(__file__).parent.absolute() / "jwt_keys")):
    # Get the access public key
    with open(str(Path(folder_path) / "access_public_key.pem"), 'rb') as key_file:
        public_key = load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    return public_key



# ======================================================== #
# ======================== Verify ======================== #
# ======================================================== #

# ~~~~~~~~~~~~~~ Refresh Token ~~~~~~~~~~~~~ #
def verify_refresh_token(token: str):
    public_key = get_refresh_token_public()
    try:
        options = {"verify_aud": False} #TODO Change this to True
        payload = jwt.decode(token, public_key, algorithms="ES512", options=options)
        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def check_jti(user: s_user.User, application_id:str, jti: str, db: Session):
    user_security = db.query(m_user.UserSecurity).filter_by(user_id=user.user_id).first()
    if application_id:
        application_tokens = user_security.application_tokens
        if application_tokens[application_id] == jti:
            return True
        else:
            return False
    else:
        temporary_tokens = user_security.temporary_tokens
        if jti in temporary_tokens:
            return True
        else:
            return False
    
# ~~~~~~~~~~~~~~ Access Token ~~~~~~~~~~~~~ #
def verify_access_token(token: str):
    public_key = get_access_token_public()
    try:
        options = {"verify_aud": False} #TODO Change this to True
        payload = jwt.decode(token, public_key, algorithms="ES256", options=options)
        return payload
    except jwt.ExpiredSignatureError:
        print("Expired")
        return False
    except jwt.InvalidTokenError as e:
        print(e)
        return False
    

# ======================================================== #
# ==================== Tokens-Rotation =================== #
# ======================================================== #
def create_tokens(db: Session, user_id: str, old_jti: str = None, application_id: str = None):
    # Get the user and user_security
    user = db.query(m_user.User).filter_by(user_id=user_id).first()
    user_security = db.query(m_user.UserSecurity).filter_by(user_id=user.user_id).first()

    # Get the private keys and create the jti
    refresh_private_key, access_private_key = get_tokens_private()
    refresh_jti = str(uuid.uuid4())
    access_jti = str(uuid.uuid4())

    # ~~~~~~~~ Create the refresh token ~~~~~~~ #
    if application_id and application_id != "webapplication":
        payload= {
            "iss": "https://api.theshopmaster.com", #! Change this to the domain of the api
            "sub": user.user_id,
            "aud": application_id,
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=30),
            "nbf": datetime.now(tz=timezone.utc),
            "iat": datetime.now(tz=timezone.utc),
            "jti": refresh_jti
        }

        # Add the jti and application_id to the user_security
        application_tokens = user_security.application_tokens
        application_tokens[application_id] = refresh_jti
        user_security.application_tokens = application_tokens
    else:
        payload= {
            "iss": "https://api.theshopmaster.com", #! Change this to the domain of the api
            "sub": user.user_id,
            "aud": "webapplication",
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=15), #! More then 15 minutes?
            "nbf": datetime.now(tz=timezone.utc),
            "iat": datetime.now(tz=timezone.utc),
            "jti": refresh_jti
        }
        # Add the jti to the user_security
        try:
            temp_tokens = user_security.temporary_tokens.split(",")
            for token in temp_tokens:
                tmp_payload = verify_refresh_token(token)
                if not tmp_payload:
                    temp_tokens.remove(token)
        except:
            temp_tokens = []
        active_tokens = len(temp_tokens)
        if active_tokens > 4: #! More then 5?
            raise HTTPException(status_code=403, detail="Too many active temporary instances")
        if old_jti:
            temp_tokens.remove(old_jti)
        temp_tokens.append(refresh_jti)
        user_security.temporary_tokens = ",".join(temp_tokens)
        
    reftesh_token = jwt.encode(payload, refresh_private_key, algorithm='ES512')

    # ~~~~~~~~ Create the access token ~~~~~~~ #
    payload= {
        "iss": "https://api.theshopmaster.com", #! Change this to the domain of the api
        "sub": user.user_id,
        "aud": application_id if application_id else "webapplication",
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=8),
        "nbf": datetime.now(tz=timezone.utc),
        "iat": datetime.now(tz=timezone.utc),
        "jti": access_jti
    }
    access_token = jwt.encode(payload, access_private_key, algorithm='ES256')
    db.commit()
    return reftesh_token, access_token


# ======================================================== #
# ==================== Tokens-Revocation ================= #
# ======================================================== #

# ~~~~~~~~~~~~~~ Single Token ~~~~~~~~~~~~~ #
def revoke_application_token(user: s_user.User, application_id: str, db: Session):
    user_security = db.query(m_user.UserSecurity).filter_by(user_id=user.user_id).first()
    old_application_tokens = user_security.application_tokens
    new_application_tokens = old_application_tokens.remove(application_id)

    user_security.application_tokens = new_application_tokens

    return True

# ~~~~~~~~~~~~~~ All Tokens ~~~~~~~~~~~~~ #
def revoke_all_application_tokens(user: s_user.User, db: Session):
    user_security = db.query(m_user.UserSecurity).filter_by(user_id=user.user_id).first()
    user_security.application_tokens = []

    return True

# ======================================================== #
# ========================== OTP ========================= #
# ======================================================== #



# ======================================================== #
# ======================= Password ======================= #
# ======================================================== #
def check_password(db: Session, user_id: str, password: str):
    db_user_security = db.query(m_user.UserSecurity).filter_by(user_id=user_id).first()
    if bcrypt.checkpw(password.encode("utf-8"), db_user_security.password.encode("utf-8")):
        return True
    else:
        return False