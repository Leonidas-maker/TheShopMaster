from fastapi import HTTPException
from sqlalchemy.orm import Session
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from middleware.auth import verify_refresh_token, create_tokens, create_jti_timestamp, get_token_payload
from models import s_user, m_user

# ~~~~~~~~~~~~~~ Middleware ~~~~~~~~~~~~~ #
from middleware.user import get_user
from middleware.auth import check_password

def get_tokens(db: Session, refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    if payload and payload.get("jti"):
        old_jti = create_jti_timestamp(payload["jti"], payload["exp"])
        refresh_token, access_token = create_tokens(db, payload["sub"], old_jti, payload["aud"])
        return {"refresh_token": refresh_token, "access_token": access_token}
    else:
        raise HTTPException(status_code=401, detail="Forbidden")

def login(db: Session, ident: str, password: str, application_id: str = None):
    if "@" in ident:
        user = get_user(db, email=ident)
    else:
        user = get_user(db, username=ident)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not check_password(db, user.user_id, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    refresh_token, access_token = create_tokens(db, user.user_id, application_id)
    return {"refresh_token": refresh_token, "access_token": access_token}

def logout(db: Session, user_id: str, refresh_token: str, access_token: str):
    refresh_payload = verify_refresh_token(refresh_token)
    access_payload = get_token_payload(access_token)
    if refresh_payload and refresh_payload.get("jti"):
        user_security = db.query(m_user.UserSecurity).filter(m_user.UserSecurity.user_id == user_id).first()
        if user_security:
            # Remove refresh token
            try:
                temp_tokens = user_security.temporary_tokens.split(",")
            except:
                temp_tokens = []
            
            jti_timestamp = create_jti_timestamp(refresh_payload["jti"], refresh_payload["exp"])
            if jti_timestamp in user_security.application_tokens.values():
                user_security.application_tokens = {key:val for key, val in user_security.application_tokens.items() if val != jti_timestamp}
            elif jti_timestamp in temp_tokens:
                temp_tokens.remove(jti_timestamp)
                user_security.temporary_tokens = ",".join(temp_tokens)
            else:
                raise HTTPException(status_code=404, detail="Not Found")

            # Remove access token
            jti_timestamp = create_jti_timestamp(access_payload["jti"], access_payload["exp"])
            try:
                active_tokens = user_security.active_access_tokens.split(",")
            except:
                active_tokens = []
            if jti_timestamp in active_tokens:
                active_tokens.remove(jti_timestamp)
                user_security.active_access_tokens = ",".join(active_tokens)
            db.commit()
            return {"message": "Logout successful"}
            
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
