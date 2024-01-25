from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.inspection import inspect
import uuid

from models import m_user

###########################################################################
############################## Get functions ##############################
###########################################################################


def get_user(
    db: Session,
    user_uuid: uuid.UUID = None,
    user_id: int = None,
    username: str = None,
    email: str = None,
    with_user_uuid: bool = False,
):
    query_options = [joinedload(m_user.User.user_uuid)] if with_user_uuid else []
    query = db.query(m_user.User).options(*query_options)

    if user_uuid:
        if isinstance(user_uuid, str):
            user_uuid = uuid.UUID(user_uuid)
        return query.join(m_user.UserUUID, m_user.UserUUID.user_uuid == user_uuid).first()
    elif user_id:
        return query.filter(m_user.User.user_id == user_id).first()
    elif username:
        return query.filter(m_user.User.username == username).first()
    elif email:
        return query.filter(m_user.User.email == email).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid parameters")


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(m_user.User).offset(skip).limit(limit).all()


def get_user_security(
    db: Session,
    user_uuid: uuid.UUID = None,
    user_id: str = None,
    with_tokens: bool = False,
    with_2fa: bool = False,
) -> m_user.UserSecurity:
    query_options = []
    if with_tokens:
        query_options.append(joinedload(m_user.UserSecurity.user_tokens))
    if with_2fa:
        query_options.append(joinedload(m_user.UserSecurity.user_2fa))

    query = db.query(m_user.UserSecurity).options(*query_options)

    if user_id:
        user_security = query.filter_by(user_id=user_id).first()

    else:
        if isinstance(user_uuid, str):
            user_uuid = uuid.UUID(user_uuid)

        user_security = query.join(m_user.UserUUID, m_user.UserUUID.user_uuid == user_uuid).first()

    if user_security:
        return user_security
    else:
        raise HTTPException(status_code=400, detail="Invalid parameters")


def get_user_tokens(
    db: Session, user_uuid: uuid.UUID = None, user_id: str = None
) -> m_user.UserTokens:
    query = db.query(m_user.UserTokens)
    if user_id:
        user_tokens = query.filter_by(user_id=user_id).all()
    else:
        if isinstance(user_uuid, str):
            user_uuid = uuid.UUID(user_uuid)
        user_tokens = query.join(m_user.UserUUID, m_user.UserUUID.user_uuid == user_uuid).all()

    if user_tokens:
        return user_tokens
    else:
        raise HTTPException(status_code=400, detail="Invalid parameters")


def get_user_2fa(db: Session, user_uuid: uuid.UUID = None, user_id: str = None) -> m_user.User2FA:
    query = db.query(m_user.User2FA)
    if user_id:
        user_2fa = query.filter_by(user_id=user_id).first()
    else:
        if isinstance(user_uuid, str):
            user_uuid = uuid.UUID(user_uuid)
        user_2fa = query.join(m_user.UserUUID, m_user.UserUUID.user_uuid == user_uuid).first()

    if user_2fa:
        return user_2fa
    else:
        raise HTTPException(status_code=400, detail="Invalid parameters")


###########################################################################
############################# Helper functions ############################
###########################################################################


def merge_sqlalchemy_objs_to_dict(*objs):
    merged_dict = {}
    for obj in objs:
        if obj is not None:
            obj_dict = {
                c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs
                if c.key not in merged_dict
            }  # Ignoriert doppelte Schlüssel
            merged_dict.update(obj_dict)
    return merged_dict
