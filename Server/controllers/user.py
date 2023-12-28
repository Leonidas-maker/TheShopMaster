from fastapi import HTTPException
import bcrypt
from sqlalchemy.orm import Session

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from models import m_user, s_user


def create_user(db: Session, user: s_user.UserCreate):
    # Check if request.address exists
    if user.address:
        # TODO: Performance improvements
        new_city = (
            db.query(m_user.Address)
            .join(m_user.City)
            .join(m_user.Country)
            .filter(
                m_user.City.city == user.address.city,
                m_user.Country.country == user.address.country,
            )
            .first()
        )

        if not new_city:
            # Check if country exists
            new_country = (
                db.query(m_user.Country).filter_by(country=user.address.country).first()
            )
            if not new_country:
                # Create new country
                new_country = m_user.Country(country=user.address.country)
                db.add(new_country)
                db.flush()

            # Create new city
            new_city = m_user.City(
                city=user.address.city, country_id=new_country.country_id
            )
            db.add(new_city)
            db.flush()

        # Check if address exists
        new_address = (
            db.query(m_user.Address)
            .filter_by(
                address1=user.address.address1,
                address2=user.address.address2,
                postal_code=user.address.postal_code,
                city_id=new_city.city_id,
            )
            .first()
        )
        if not new_address:
            # Create new address
            new_address = m_user.Address(
                address1=user.address.address1,
                address2=user.address.address2,
                district=user.address.district,
                postal_code=user.address.postal_code,
                city_id=new_city.city_id,
            )
            db.add(new_address)
            db.flush()

    # Create new user
    new_user = m_user.User(
        username=user.username,
        email=user.email,
        address_id=new_address.address_id if user.address else None,
        is_active=True,
    )
    db.add(new_user)
    db.flush()

    # Create new user_security
    new_user_security = m_user.UserSecurity(
        user_id=new_user.user_id,
        password=bcrypt.hashpw(
            user.security.password.encode("utf-8"), bcrypt.gensalt()
        ),
    )

    db.add(new_user_security)
    db.commit()
    return new_user


def update_user(db: Session, user: s_user.User):
    # TODO Check if something changed
    pass


def delete_user(db: Session, user_id: int):
    # TODO Recursive delete address, city, country
    # TODO Delete user_security
    # TODO Delete shopping_cart
    # TODO Delete favorite
    # TODO Delete user
    pass
