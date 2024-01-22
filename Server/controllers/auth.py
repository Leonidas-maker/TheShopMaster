from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import pyotp

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
)
from data.email import send_with_template, EmailSchema

# ~~~~~~~~~~~~~~ Controllers ~~~~~~~~~~~~~~ #
from controllers.user import create_user


def get_tokens(db: Session, refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    if payload and payload.get("jti"):
        user_security = get_user_security(db, user_uuid=payload["sub"])
        refresh_token, access_token = create_tokens(
            db, user_security, payload.get("jti"), payload["aud"]
        )
        return {"refresh_token": refresh_token, "access_token": access_token}
    else:
        raise HTTPException(status_code=401, detail="Forbidden")


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
    _2fa_code: str = None,
    application_id: str = None,
):
    if "@" in ident:
        user = get_user(db, email=ident)
    else:
        user = get_user(db, username=ident)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_security = get_user_security(db, user_id=user.user_id)

    # Pre checks
    if not user_security.verified:
        raise HTTPException(status_code=401, detail="Account not verified")
    check_security_warns(user_security)

    # if user_security._2fa_enabled:
    #    if _2fa_code:
    #        if not verify_totp(user_security, _2fa_code):
    #            raise HTTPException(status_code=401, detail="Invalid credentials")
    #    else:
    #        raise HTTPException(status_code=401, detail="2FA code required")

    if not check_password(db, password, user_security=user_security):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    refresh_token, access_token = create_tokens(
        db, user_security, str(user.user_uuid.user_uuid), application_id
    )
    return {"refresh_token": refresh_token, "access_token": access_token}


def logout(db: Session, user_uuid: str, refresh_token: str, access_token: str):
    refresh_payload = verify_refresh_token(refresh_token)
    access_payload = get_token_payload(access_token)
    if refresh_payload and refresh_payload.get("jti"):
        delete_tokens = [refresh_payload["jti"], access_payload["jti"]]
        db.query(m_user.UserTokens).join(
            m_user.UserUUID, m_user.UserUUID.user_uuid == user_uuid
        ).filter(m_user.UserTokens.token_jti.in_(delete_tokens),).delete(synchronize_session=False)
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
    access_payload = verify_access_token(access_token)
    if not access_payload:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_security = get_user_security(db, user_uuid=access_payload["sub"])
    user_id = user_security.user_id
    if user_security._2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA already enabled")

    user_security._2fa_enabled = True
    _2fa_secret, backup_codes = create_totp(db, user_id)

    if user_add_2fa_req.need_qr_code:
        user = get_user(db, user_id=user_id)
        return s_auth.UserResActivate2FA(
            provisioning_uri=pyotp.totp.TOTP(_2fa_secret).provisioning_uri(
                name=user.email, issuer_name="TheShopMaster.com"
            ),
            _2fa_secret=None,
            backup_codes=backup_codes,
        )
    else:
        return s_auth.UserResActivate2FA(
            provisioning_uri=None,
            _2fa_secret=_2fa_secret,
            backup_codes=backup_codes,
        )


def verify_first_2fa(db: Session, access_token: str, otp: str):  # TODO
    access_payload = verify_access_token(access_token)
    if not access_payload:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_security = get_user_security(db, user_uuid=access_payload["sub"])
    user_id = user_security.user_id
    if not user_security._2fa_enabled and verify_totp(db, otp):
        {}
    user_security._2fa_enabled = True
    db.commit()
    return {"message": "2FA enabled"}
