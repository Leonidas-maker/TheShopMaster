from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import MEDIUMBLOB

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute() / "config"))

from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    avatar = Column(MEDIUMBLOB)
    address_id = Column(Integer, ForeignKey("addresses.address_id"))
    is_active = Column(Boolean, default=True)
    last_modified = Column(TIMESTAMP, nullable=False)

class Address(Base):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String(255), nullable=False)
    address2 = Column(String(255))
    district = Column(String(255), nullable=False)
    postal_code = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.city_id"), nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)

class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True, index=True)
    city = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)

class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)

class UserSecurity(Base):
    __tablename__ = "users_security"

    security_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    password = Column(String(255), nullable=False)
    _2fa = Column(Boolean, default=False)
    forgot_password = Column(String(255))
    application_token = Column(JSON)
    verified = Column(Boolean, default=False)
    _2fa_backup = Column(String(255))
    last_modified = Column(TIMESTAMP, nullable=False)

class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    shoppingCart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, unique=True)
    quantity = Column(Integer, nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)

class FavoriteProduct(Base):
    __tablename__ = "favorite_products"

    favoriteProduct_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, unique=True)
    last_modified = Column(TIMESTAMP, nullable=False)

class Product(Base): #! Need to be changed (shipped to other database stucture)
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)

