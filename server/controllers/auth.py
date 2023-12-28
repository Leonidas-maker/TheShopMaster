from fastapi import HTTPException
from sqlalchemy.orm import Session
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from middleware.auth import verify_refresh_token, create_tokens
from models import s_user, m_user

# ~~~~~~~~~~~~~~ Middleware ~~~~~~~~~~~~~ #
from middleware.user import get_user
from middleware.auth import check_password

def get_tokens(db: Session, refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    print(payload)
    if payload and payload.get("jti"):
        refresh_token, access_token = create_tokens(db, payload["sub"], payload["jti"], payload["aud"])
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
    if refresh_payload and refresh_payload.get("jti"):
        user_security = db.query(m_user.UserSecurity).filter(m_user.UserSecurity.user_id == user_id).first()
        if user_security:
            try:
                deactivated_tokens = user_security.deactivated_tokens.split(",")
            except:
                deactivated_tokens = []
            user_security.deactivated_tokens = ",".join(deactivated_tokens + [refresh_payload["jti"]])

            try:
                temp_tokens = user_security.temporary_tokens.split(",")
            except:
                temp_tokens = []

            if refresh_payload["jti"] in user_security.application_tokens:
                user_security.application_tokens = {key:val for key, val in user_security.application_tokens.items() if val != refresh_payload["jti"]}
                db.commit()
                return {"message": "Logout successful"}
            elif refresh_payload["jti"] in temp_tokens:
                temp_tokens.remove(refresh_payload["jti"])
                user_security.temporary_tokens = ",".join(temp_tokens)
                db.commit()   
                return {"message": "Logout successful"}
    else:
        raise HTTPException(status_code=400, detail="Forbidden")
