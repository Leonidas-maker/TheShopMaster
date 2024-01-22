from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import MEDIUMBLOB, INTEGER as INT

from config.database import Base
from config.security import *
import uuid


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    avatar = Column(MEDIUMBLOB)
    address_id = Column(Integer, ForeignKey("addresses.address_id"))
    is_active = Column(Boolean, default=True)
    last_modified = Column(TIMESTAMP, nullable=False)

    user_security = relationship("UserSecurity", back_populates="user", uselist=False)
    user_uuid = relationship("UserUUID", back_populates="user", uselist=False)
    address = relationship("Address", uselist=False)


class UserUUID(Base):
    __tablename__ = "user_uuids"

    user_uuid = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="user_uuid")


class Address(Base):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String(255), nullable=False)
    address2 = Column(String(255))
    district = Column(String(255), nullable=False)
    postal_code = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.city_id"), nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)

    city = relationship("City")


class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True, index=True)
    city = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)

    country = relationship("Country")


class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)


# TODO New table for application tokens (application_id, user_id or security_id, refresh_token, last_modified) 1 to n relationship betweem user_security and application_tokens
class UserSecurity(Base):
    __tablename__ = "users_security"

    security_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    password = Column(String(255), nullable=False)

    forgot_password = Column(String(255))

    # ~~~~~~~~~~~~~~~~ Security ~~~~~~~~~~~~~~~ #
    secutity_warns = Column(
        Integer, default=0
    )  # * Number of times suspicious activity has been detected max. 10
    locked = Column(Boolean, default=False)

    # ~~~~~~~~~~~~~~ Verification ~~~~~~~~~~~~~ #
    verified = Column(Boolean, default=False)
    verify_otp = Column(String(255))  #! Equivalent to name simple_otp
    last_modified = Column(TIMESTAMP, nullable=False)
    _2fa_enabled = Column(Boolean)

    user = relationship("User", back_populates="user_security")
    user_tokens = relationship("UserTokens", back_populates="user_security")
    user_2fa = relationship("User2FA", back_populates="user_security", uselist=False)


class User2FA(Base):
    __tablename__ = "user_2fa"

    _2fa_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_security.user_id"), nullable=False)
    _2fa_secret = Column(String(255))
    _2fa_last_used = Column(INT(11))
    _2fa_backup = Column(String(255))
    last_modified = Column(TIMESTAMP, nullable=False)

    # Relationship to UserSecurity
    user_security = relationship("UserSecurity", back_populates="user_2fa")


class UserTokens(Base):
    __tablename__ = "user_tokens"

    token_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_security.user_id"), nullable=False)
    token_type = Column(String(255), nullable=False)
    token_jti = Column(String(255), nullable=False)
    token_value = Column(String(255), nullable=False)
    creation_time = Column(INT(11), nullable=False)
    expiration_time = Column(INT(11), nullable=False)

    user_security = relationship("UserSecurity", back_populates="user_tokens")


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


class Product(Base):  #! Need to be changed (shipped to other database stucture)
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    last_modified = Column(TIMESTAMP, nullable=False)
