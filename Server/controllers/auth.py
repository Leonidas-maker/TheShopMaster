from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import pyotp
import uuid

from middleware.auth import (
    verify_refresh_token,
    create_tokens,
    get_token_payload,
    get_user_security,
)
from models import s_user, m_user, s_auth

# ~~~~~~~~~~~~~~ Middleware ~~~~~~~~~~~~~ #
from middleware.user import get_user, get_user_security, get_user_tokens, get_user_2fa
from middleware.auth import (
    check_password,
    verify_simple_otp,
    check_security_warns,
    create_totp,
    verify_totp,
    create_simple_otp,
    verify_access_token,
    create_backup_codes,
    verify_security_token,
    create_security_token,
    remove_older_security_token,
    revoke_token,
    raise_security_warns,
    remove_2fa,
)
from data.email import send_with_template, EmailSchema

# ~~~~~~~~~~~~~~ Controllers ~~~~~~~~~~~~~~ #
from controllers.user import create_user


def get_tokens(db: Session, refresh_token: str):
    payload = verify_refresh_token(db, refresh_token)
    if payload and payload.get("jti"):
        user_uuid = uuid.UUID(payload["sub"])
        user_security = get_user_security(db, user_uuid=user_uuid, with_tokens=True)
        refresh_token, access_token = create_tokens(
            db, user_security, str(user_uuid), payload.get("jti"), payload["aud"]
        )
        return {"refresh_token": refresh_token, "access_token": access_token}
    raise HTTPException(status_code=401, detail="Unauthorized")


def register(db: Session, user: s_user.UserCreate, background_tasks: BackgroundTasks):
    db_user = get_user(db, email=user.email, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user, user_uuid = create_user(db, user)
    user_security = get_user_security(db, user_id=user.user_id)

    verify_code = create_simple_otp(db, user_security)
    background_tasks.add_task(
        send_with_template,
        EmailSchema(
            email=user.email,
            body={"verify_code": str(verify_code)},
            type="verify-first",
        ),
    )
    response = s_auth.UserResRegister(**user.__dict__, user_uuid=user_uuid)
    return response


def login(
    db: Session,
    ident: str,
    password: str,
    application_id: str = None,
):
    if "@" in ident:
        user = get_user(db, email=ident, with_user_uuid=True)
    else:
        user = get_user(db, username=ident, with_user_uuid=True)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = user.user_id
    user_uuid = str(user.user_uuid.user_uuid)

    user_security = get_user_security(db, user_id=user_id, with_tokens=True)

    # Pre checks
    if not user_security.verified:
        raise HTTPException(status_code=401, detail="Account not verified")
    check_security_warns(user_security)

    if user_security._2fa_enabled:
        remove_older_security_token(db, user_security, "login-2fa")
        return {
            "secret_token": create_security_token(
                db,
                user_id,
                user_uuid,
                f"login-2fa::{application_id}" if application_id else "login-2fa",
            )
        }

    if not check_password(db, password, user_security=user_security):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    refresh_token, access_token = create_tokens(db, user_security, user_uuid, application_id)
    return {"refresh_token": refresh_token, "access_token": access_token}


def logout(db: Session, refresh_token: str, access_token: str):
    refresh_payload = verify_refresh_token(db, refresh_token)
    access_payload = get_token_payload(access_token)
    if refresh_payload and refresh_payload.get("jti"):
        delete_tokens = [refresh_payload["jti"], access_payload["jti"]]
        user_uuid = uuid.UUID(refresh_payload["sub"])
        token_ids = (
            db.query(m_user.UserTokens.token_id)
            .join(m_user.UserUUID, m_user.UserUUID.user_uuid == user_uuid)
            .filter(m_user.UserTokens.token_jti.in_(delete_tokens))
            .all()
        )
        token_ids = [token.token_id for token in token_ids]

        if token_ids:
            db.query(m_user.UserTokens).filter(m_user.UserTokens.token_id.in_(token_ids)).delete(
                synchronize_session=False
            )
            db.commit()
        return {"message": "Logout successful"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


def verify_account(db: Session, user_uuid: str, verify_code: str):
    user_security = get_user_security(db, user_uuid=user_uuid)
    if verify_simple_otp(user_security, verify_code):
        user_security.verified = True
        user_security.verify_otp = None
        db.commit()
        return {"message": "Account verified"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


###########################################################################
################################### 2FA ###################################
###########################################################################


def add_2fa(
    user_add_2fa_req: s_auth.UserReqActivate2FA, access_token: str, db: Session
) -> s_auth.UserResActivate2FA:
    access_payload = verify_access_token(db, access_token)
    if not access_payload:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_security = get_user_security(db, user_uuid=access_payload["sub"])
    user_id = user_security.user_id
    if user_security._2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA already enabled")

    _2fa_secret = create_totp(db, user_id)

    if user_add_2fa_req.need_qr_code:
        user = get_user(db, user_id=user_id)
        return s_auth.UserResActivate2FA(
            provisioning_uri=pyotp.totp.TOTP(_2fa_secret).provisioning_uri(
                name=user.email, issuer_name="TheShopMaster.com"
            ),
            _2fa_secret=None,
        )
    else:
        return s_auth.UserResActivate2FA(
            provisioning_uri=None,
            _2fa_secret=_2fa_secret,
        )


def verify_first_2fa(db: Session, access_token: str, otp: str):
    access_payload = verify_access_token(db, access_token)
    if access_payload:
        user_uuid = access_payload["sub"]
        if verify_totp(db, otp, user_uuid=user_uuid):
            backup_codes = create_backup_codes(db, user_uuid)
            response = s_auth.UserResVerifyFirst2FA(backup_codes=backup_codes)
            return response

    raise HTTPException(status_code=401, detail="Invalid credentials")


def verify_2fa(db: Session, secret_token: str, otp: str):
    secret_payload, user_security = verify_security_token(db, secret_token, is_2fa=True)
    if secret_payload:
        user_uuid = secret_payload["sub"]
        if verify_totp(db, otp, user_2fa=user_security.user_2fa):
            revoke_token(
                db, user_security.user_id, "Security", secret_payload["aud"], secret_payload["jti"]
            )

            aud_split = secret_payload["aud"].split("::")
            application_id = aud_split[1] if len(aud_split) > 1 else None

            refresh_token, access_token = create_tokens(
                db, user_security, user_uuid, secret_payload["jti"], application_id
            )
            return {"refresh_token": refresh_token, "access_token": access_token}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials | Type: 2FA")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
def verify_2fa_backup(db: Session, secret_token: str, otp: s_auth.BackupOTP):
    secret_payload, user_security = verify_security_token(db, secret_token, is_2fa=True)
    if secret_payload:
        user_uuid = secret_payload["sub"]
        user_2fa: m_user.User2FA = user_security.user_2fa
        count_correct = 0
        for backup_code in otp.backup_codes:
            if not backup_code in user_2fa._2fa_backup:
                raise_security_warns(db, user_security, "2FA Backup Codes")
            else:
                count_correct += 1
                
        if count_correct == len(otp.backup_codes): 
            revoke_token(
                db, user_security.user_id, "Security", secret_payload["aud"], secret_payload["jti"]
            )

            remove_2fa(db, user_security)

            aud_split = secret_payload["aud"].split("::")
            application_id = aud_split[1] if len(aud_split) > 1 else None

            refresh_token, access_token = create_tokens(
                db, user_security, user_uuid, secret_payload["jti"], application_id
            )
            return {"refresh_token": refresh_token, "access_token": access_token, "message": "2FA removed"}

        else:
            raise HTTPException(status_code=401, detail="Invalid credentials | Type: 2FA")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

def remove_2fa(db: Session, access_token: str, otp: str):
    access_payload = verify_access_token(db, access_token)
    if access_payload:
        user_security = get_user_security(db, user_uuid=access_payload["sub"])
        if not user_security._2fa_enabled:
            raise HTTPException(status_code=400, detail="2FA not enabled")
        if verify_totp(db, otp, user_2fa=user_security.user_2fa):
            remove_2fa(db, user_security)
            return {"message": "2FA removed"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials | Type: 2FA")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

