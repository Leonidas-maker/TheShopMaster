from pydantic import BaseModel, EmailStr, validator, UUID4
from typing import Optional

from .s_user import UserBase
class UserTokens(BaseModel):
    access_token: str
    refresh_token: str


class UserReqActivate2FA(BaseModel):
    password: str
    need_qr_code: Optional[bool] = False
class UserResActivate2FA(BaseModel):
    provisioning_uri: str
    _2fa_secret: str = None
    backup_codes: str

    @validator("provisioning_uri", always=True)
    def check_exclusivity(cls, v, values, **kwargs):
        if v is not None and values.get("_2fa_secret") is not None:
            raise ValueError("Only _2fa_secret or provisioning_uri may be set, not both.")
        if v is None and values.get("_2fa_secret") is None:
            raise ValueError("One of _2fa_secret or provisioning_uri must be set.")
        return v
    
class UserResRegister(UserBase):
    user_uuid: UUID4
    
class UserLogin(BaseModel):
    ident: str | EmailStr
    _2fa_code: Optional[str] = None
    password: str
    application_id: Optional[str] = None