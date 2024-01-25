from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime


###########################################################################
############################# Pydantic models #############################
###########################################################################


# ======================================================== #
# ======================== Address ======================= #
# ======================================================== #
class AddressBase(BaseModel):
    address1: str
    address2: Optional[str] = None
    district: str
    postal_code: str


class AddressCreate(AddressBase):
    city: str
    country: str


class Address(AddressBase):
    address_id: int
    city_id: int
    last_modified: datetime

    class Config:
        from_attributes = True


# ======================================================== #
# ========================= City ========================= #
# ======================================================== #
class CityBase(BaseModel):
    city: str
    country_id: int


class CityCreate(CityBase):
    pass


class City(CityBase):
    city_id: int
    last_modified: datetime

    class Config:
        from_attributes = True


# ======================================================== #
# ======================== Country ======================= #
# ======================================================== #
class CountryBase(BaseModel):
    country: str


class CountryCreate(CountryBase):
    pass


class Country(CountryBase):
    country_id: int
    last_modified: datetime

    class Config:
        from_attributes = True


# ======================================================== #
# ===================== UserSecurity ===================== #
# ======================================================== #


class User2FA(BaseModel):
    _2fa_id: Optional[int]
    user_id: int
    _2fa_secret: str
    _2fa_last_used: Optional[int]
    _2fa_backup: str

    class Config:
        from_attributes = True


class UserTokens(BaseModel):
    token_id: Optional[int]
    user_id: int
    token_type: str
    token_jti: str
    token_value: str
    creation_time: int
    expiration_time: int

    class Config:
        from_attributes = True


class UserSecurityBase(BaseModel):
    password: str


class UserSecurityCeate(UserSecurityBase):
    pass


class UserSecurity(UserSecurityBase):
    user_id: int
    forgot_password: Optional[str]
    security_warns: Optional[int]
    locked: Optional[bool]
    verify_otp: Optional[str]
    verified: Optional[bool]
    _2fa_enabled: Optional[bool]
    last_modified: Optional[datetime]

    user_2fa: Optional[User2FA] = None

    class Config:
        from_attributes = True


# ======================================================== #
# ========================= User ========================= #
# ======================================================== #
class UserUUID(BaseModel):
    user_id: int
    user_uuid: UUID4


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    security: UserSecurityCeate
    address: Optional[AddressCreate] = None


class User(UserBase):
    user_id: int
    avatar: Optional[bytes] = None
    address_id: Optional[int] = None
    last_modified: datetime

    class Config:
        from_attributes = True


# ======================================================== #
# ===================== ShoppingCart ===================== #
# ======================================================== #
class ShoppingCartBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class ShoppingCartCreate(ShoppingCartBase):
    pass


class ShoppingCart(ShoppingCartBase):
    shoppingCart_id: int
    last_modified: datetime

    class Config:
        from_attributes = True


# ======================================================== #
# ==================== FavoriteProduct =================== #
# ======================================================== #
class FavoriteProductBase(BaseModel):
    user_id: int
    product_id: int


class FavoriteProductCreate(FavoriteProductBase):
    pass


class FavoriteProduct(FavoriteProductBase):
    favoriteProduct_id: int
    last_modified: datetime

    class Config:
        from_attributes = True


# ======================================================== #
# ======================== Product ======================= #
# ======================================================== #
class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    product_id: int
    last_modified: datetime

    class Config:
        from_attributes = True


class CompleteAdress(BaseModel):
    address1: str
    address2: Optional[str] = None
    district: str
    postal_code: str
    city: str
    country: str


class ResGetUser(UserBase):
    user_uuid: UUID4

    avatar: Optional[bytes] = None
    address: CompleteAdress
    last_modified: datetime

    class Config:
        from_attributes = True
