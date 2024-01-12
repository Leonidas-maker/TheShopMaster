from pydantic import BaseModel, EmailStr
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
class UserSecurityBase(BaseModel):
    password: str
    _2fa: Optional[str] = None
    verified: Optional[bool] = False

class UserSecurityCreate(UserSecurityBase):
    pass

class UserSecurity(UserSecurityBase):
    user_id: int
    security_id: int
    forgot_password: Optional[str] = None
    application_tokens: Optional[dict] 
    temporary_tokens: Optional[str] = None
    active_access_tokens: Optional[str] = None
    secutity_warns: Optional[int] = 0
    locked: Optional[bool] = False
    _2fa_backup: Optional[str] = None
    last_modified: datetime

    class Config:
        from_attributes = True

# ======================================================== #
# ========================= User ========================= #
# ======================================================== #
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    security: UserSecurityCreate
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