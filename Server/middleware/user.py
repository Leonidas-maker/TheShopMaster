from fastapi import HTTPException
from sqlalchemy.orm import Session

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from models import m_user

def get_user(db: Session, user_id: int = None, username: str = None, email: str = None):
    if user_id:
        return db.query(m_user.User).filter(m_user.User.user_id == user_id).first()
    elif username:
        return db.query(m_user.User).filter(m_user.User.username == username).first()
    elif email:
        return db.query(m_user.User).filter(m_user.User.email == email).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid parameters")

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(m_user.User).offset(skip).limit(limit).all()