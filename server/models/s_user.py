from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Pydantic models

class AddressBase(BaseModel):
    address1: str
    address2: Optional[str] = None
    district: str
    postal_code: str
    

class Address(AddressBase):
    address_id: int
    city_id: int
    last_modified: datetime

    class Config:
        from_attributes = True

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

class CountryBase(BaseModel):
    country: str

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    country_id: int
    last_modified: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True

class User(UserBase):
    user_id: int
    avatar: Optional[bytes] = None
    address_id: Optional[int] = None
    last_modified: datetime

    class Config:
        from_attributes = True

class UserSecurityBase(BaseModel):
    password: str
    _2fa: Optional[bool] = False
    verified: Optional[bool] = False

class UserSecurity(UserSecurityBase):
    user_id: int
    security_id: int
    forgot_password: Optional[str] = None
    application_token: Optional[dict] = None
    _2fa_backup: Optional[str] = None
    last_modified: datetime

    class Config:
        from_attributes = True

class ShoppingCartBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class ShoppingCart(ShoppingCartBase):
    shoppingCart_id: int
    last_modified: datetime

    class Config:
        from_attributes = True

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

class ProductBase(BaseModel):
    name: str
    description: str
    price: int

class Product(ProductBase):
    product_id: int
    last_modified: datetime

    class Config:
        from_attributes = True


# Pydantic create-models 

class AddressCreate(AddressBase):
    city: str
    country: str

class UserSecurityCreate(UserSecurityBase):
    pass

class UserCreate(UserBase):
    security: UserSecurityCreate
    address: Optional[AddressCreate] = None

class ShoppingCartCreate(ShoppingCartBase):
    pass

class ProductCreate(ProductBase):
    pass