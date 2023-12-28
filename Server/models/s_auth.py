from pydantic import BaseModel, EmailStr
from typing import Optional
from .s_user import User

class UserTokens(BaseModel):
    access_token: str
    refresh_token: str

class UserRegister(BaseModel):
    user: User
    tokens: UserTokens

class UserLogin(BaseModel):
    ident: str | EmailStr
    password: str
    application_id: Optional[str] = None